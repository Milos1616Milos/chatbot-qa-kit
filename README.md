# Chatbot QA Kit

A small, dependency-free acceptance test runner for HTTP chatbot webhooks, including n8n webhooks. Check that answers contain required facts, avoid forbidden claims, return the expected HTTP status, and respond within a latency limit. Run locally or in CI.

## Try it without a server

    python qa.py example.json --output report.md

This checks the included sample answers. A Markdown and JSON report are written locally. Exit code 0 means all cases passed; 1 means at least one failed.

## Test your own webhook

1. Copy example.json to my-chatbot.json.
2. Set request.url to your HTTPS webhook endpoint. Set request.body to the JSON your webhook expects. {{question}} is replaced with each test question. Nested objects and arrays work too.
3. Set answer_path to the dot-separated path to the reply in the JSON response, for example output.answer or 0.text. Leave it empty for a plain-text response.
4. Replace the example cases with your real facts and risks.
5. Run: python qa.py my-chatbot.json --live --output report.md

Each case supports must_contain, must_not_contain, any_of, expected_status (default 200), and max_latency_ms. Phrase matching ignores case but is otherwise literal. The checks do not prove semantic correctness or factual truth; write assertions against a verified source of truth.

For a bearer token, set request.bearer_token_env to an environment variable name. Put the token in that environment variable, never in the config file. The report includes questions and findings, but not answer bodies or request headers. Avoid sensitive questions in shared reports.

Live mode requires HTTPS, except for localhost. It sends one POST per case, so use a test endpoint or account for webhooks that create records, send messages, or incur costs. There are no automatic retries.

## Example case

    {
      "id": "unsupported-service",
      "question": "Can you guarantee first place in Google?",
      "must_not_contain": ["we guarantee first place"],
      "any_of": ["cannot guarantee", "no guarantee"]
    }

## License and support

MIT license. This starter kit is provided as-is. Issue reports should include a minimal, redacted config and the error message, never API keys or customer data.
