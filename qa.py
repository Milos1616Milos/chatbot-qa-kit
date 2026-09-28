#!/usr/bin/env python3
"""Small, dependency-free acceptance test runner for HTTP chatbots."""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def get_path(data, path):
    if not path:
        return data
    for part in path.split("."):
        if isinstance(data, list):
            data = data[int(part)]
        else:
            data = data[part]
    return data


def render_question(value, question):
    if isinstance(value, str):
        return value.replace("{{question}}", question)
    if isinstance(value, list):
        return [render_question(item, question) for item in value]
    if isinstance(value, dict):
        return {key: render_question(item, question) for key, item in value.items()}
    return value


def check_case(case, answer, status, elapsed_ms):
    failures = []
    normalized = answer.casefold()
    for phrase in case.get("must_contain", []):
        if phrase.casefold() not in normalized:
            failures.append(f"missing required phrase: {phrase}")
    for phrase in case.get("must_not_contain", []):
        if phrase.casefold() in normalized:
            failures.append(f"contains forbidden phrase: {phrase}")
    any_of = case.get("any_of", [])
    if any_of and not any(phrase.casefold() in normalized for phrase in any_of):
        failures.append("none of the alternative phrases appeared")
    expected_status = case.get("expected_status", 200)
    if status != expected_status:
        failures.append(f"HTTP {status}, expected {expected_status}")
    limit = case.get("max_latency_ms")
    if limit is not None and elapsed_ms > limit:
        failures.append(f"latency {elapsed_ms} ms exceeds {limit} ms")
    return failures


def fetch_answer(config, case):
    request = config["request"]
    question = case["question"]
    body = json.dumps(render_question(request["body"], question)).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    headers.update(request.get("headers", {}))
    token_var = request.get("bearer_token_env")
    if token_var:
        token = os.environ.get(token_var)
        if not token:
            raise ValueError(f"missing environment variable: {token_var}")
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(request["url"], body, headers, method="POST")
    start = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=request.get("timeout_seconds", 15)) as response:
            status = response.status
            raw = response.read(1_000_001)
    except urllib.error.HTTPError as exc:
        status = exc.code
        raw = exc.read(1_000_001)
    elapsed_ms = round((time.monotonic() - start) * 1000)
    if len(raw) > 1_000_000:
        raise ValueError("response exceeded 1 MB limit")
    content = raw.decode("utf-8", errors="replace")
    try:
        parsed = json.loads(content)
        answer = get_path(parsed, config.get("answer_path", ""))
        if not isinstance(answer, str):
            answer = json.dumps(answer, ensure_ascii=False)
    except json.JSONDecodeError:
        if config.get("answer_path"):
            raise ValueError("answer_path requires a JSON response")
        answer = content
    return answer, status, elapsed_ms


def markdown_report(results):
    passed = sum(row["passed"] for row in results)
    lines = ["# Chatbot QA report", "", f"Run: {datetime.now(timezone.utc).isoformat()}",
             f"Passed: {passed}/{len(results)}", ""]
    for row in results:
        lines += [f"## {'PASS' if row['passed'] else 'FAIL'} — {row['id']}",
                  f"Question: {row['question']}",
                  f"HTTP: {row['status']} · Latency: {row['latency_ms']} ms", ""]
        if row["failures"]:
            lines += ["Findings:"] + [f"- {item}" for item in row["failures"]] + [""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Run acceptance checks against a chatbot webhook")
    parser.add_argument("config", type=Path, help="JSON configuration file")
    parser.add_argument("--live", action="store_true", help="allow HTTP requests to the configured webhook")
    parser.add_argument("--output", type=Path, default=Path("report.md"), help="Markdown report path")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    if not isinstance(config.get("cases"), list) or not config["cases"]:
        parser.error("config must contain a non-empty cases array")
    if args.live and not config.get("request", {}).get("url", "").startswith(("https://", "http://localhost", "http://127.0.0.1")):
        parser.error("live URL must use HTTPS, or HTTP on localhost")
    results = []
    for case in config["cases"]:
        try:
            if args.live:
                answer, status, elapsed_ms = fetch_answer(config, case)
            else:
                if "sample_answer" not in case:
                    parser.error(f"{case.get('id', '?')}: sample_answer required without --live")
                answer, status, elapsed_ms = case["sample_answer"], case.get("sample_status", 200), 0
            failures = check_case(case, answer, status, elapsed_ms)
        except (ValueError, KeyError, IndexError, urllib.error.URLError, TimeoutError) as exc:
            status, elapsed_ms = None, None
            failures = [f"request or configuration error: {exc}"]
        row = {"id": case["id"], "question": case["question"], "passed": not failures,
               "status": status, "latency_ms": elapsed_ms, "failures": failures}
        results.append(row)
        print(f"{'PASS' if row['passed'] else 'FAIL'} {row['id']}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown_report(results), encoding="utf-8")
    args.output.with_suffix(".json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Report: {args.output}")
    return 0 if all(row["passed"] for row in results) else 1


if __name__ == "__main__":
    sys.exit(main())
