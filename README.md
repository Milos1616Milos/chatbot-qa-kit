# Chatbot QA Kit

**Catch broken chatbot answers before your customers do.** Run repeatable acceptance checks against an HTTP chatbot or n8n webhook. The kit sends questions, checks required and forbidden phrases, status codes, and latency, then writes a readable report and exits with a CI-friendly status code.

- Python 3.10+; no third-party packages or account required.
- Works with JSON or plain-text responses, including nested JSON via `answer_path`.
- Runs locally, in GitHub Actions, or in another CI system.
- Offline sample mode lets you inspect the checks without contacting a chatbot.

## See a result in one minute

```bash
python qa.py example.json --output report.md
```

The included sample runs **offline**. It writes `report.md` and `report.json`. Exit code `0` means all checks passed; `1` means at least one failed. Open the Markdown report to see which question failed and why.

Two more editable examples are in [`examples/`](examples/):

- [`ecommerce-policy.json`](examples/ecommerce-policy.json): shipping, returns, and invented prices.
- [`support-escalation.json`](examples/support-escalation.json): support hours, escalation, and unsupported guarantees.

These files contain placeholder URLs and sample answers. Running them without `--live` does not contact a website.

## Check your own chatbot endpoint

1. Copy `example.json` to a **private** file such as `my-chatbot.json`.
2. Set `request.url` to your chatbot's HTTPS API or webhook URL. Set `request.body` to the JSON it expects. Every `{{question}}` in the body is replaced with a case's question.
3. Set `answer_path` to the response field containing the reply, such as `output.answer` or `0.text`. Leave it empty for a plain-text reply.
4. Replace the sample cases with facts your chatbot must say and claims it must avoid.
5. Run:

```bash
python qa.py my-chatbot.json --live --output report.md
```

Live mode sends **one POST per case**. Use an endpoint you own or are authorized to test. These requests can trigger downstream actions or AI provider charges. Live mode requires HTTPS, except for localhost. It does not retry failed calls.

For an authenticated endpoint, set `request.bearer_token_env` to the *name* of an environment variable containing a bearer token. Put the token in your local environment or CI secrets, never in the JSON file or a GitHub commit. The report includes questions and findings, but not answer bodies or request headers. Avoid sensitive customer data in shared reports.

## What a case looks like

```json
{
  "id": "unsupported-service",
  "question": "Can you guarantee first place in Google?",
  "must_not_contain": ["we guarantee first place"],
  "any_of": ["cannot guarantee", "no guarantee"],
  "expected_status": 200,
  "max_latency_ms": 5000
}
```

Cases support `must_contain`, `must_not_contain`, `any_of`, `expected_status` (default `200`), and `max_latency_ms`. Phrase matching ignores case but is otherwise literal. This is a **deterministic acceptance check**, not a semantic judge or proof that every answer is factually correct. Write assertions against facts you have verified.

## Automate it

The repository's [sample GitHub Action](.github/workflows/test.yml) runs the offline examples on each push and pull request. For your own chatbot, call `python qa.py path/to/private-config.json --live --output report.md` from your CI job and configure endpoint credentials as CI secrets. Schedule it only after confirming the endpoint and request volume; each run can use paid AI calls. A failing case makes the process exit with code `1`.

### Use it as a GitHub Action

For an offline check in another repository, add this job to a workflow after committing your own JSON test configuration:

```yaml
name: Chatbot acceptance checks
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: Milos1616Milos/chatbot-qa-kit@v0.2.0
        with:
          config: tests/chatbot.json
          live: 'false'
```

Set `live: 'true'` only for an endpoint you own or are authorized to test. Put credentials in GitHub Actions secrets and pass them as environment variables; never commit them. Each live run sends one POST per case and may incur provider charges.

## Managed daily monitoring

A separate hosted **Chatbot Monitor** is being tested. The intended paid service runs approved checks every day, keeps history, and emails when an answer breaks or recovers. It is **not open for customer purchases yet**. If you build or operate an HTTP chatbot and want to try the private pilot, [open a public issue](https://github.com/Milos1616Milos/chatbot-qa-kit/issues/new?template=managed-monitor-pilot.yml) titled `Managed Monitor pilot interest` and describe your endpoint type **without posting URLs, tokens, or customer data**. This is an expression of interest, not a checkout or a promise of access.

## License and support

MIT license. The kit is provided as-is. To report a bug, open an issue with a minimal redacted config and the error message. Never post credentials or customer data. The hosted service, when ready, will be a separate product; its private code is not in this repository.
