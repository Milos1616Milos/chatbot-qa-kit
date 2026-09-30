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

Using n8n? Follow the [step-by-step chatbot webhook regression check](docs/n8n-chatbot-regression-check.md).

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

**BotEffex Monitor** is a separate hosted service: approved daily checks, email alerts and 30-day history. Request a **14-day assisted trial with no card**; it begins after we verify a working connection. The hosted pilot supports public HTTPS endpoints returning JSON without credentials. This is narrower than the free kit's authentication options.

Starter continuation is optional, €19/month for one chatbot and up to 10 questions; Paddle shows the final total and renewal terms. An optional **one-off setup service has a proposed €99 pilot price**, subject to a confirmed quote, tax treatment, scope and date. It does not create a subscription and has no dedicated checkout yet.

| Language | Free trial | Setup offer | Illustrative report | Repository documents |
|---|---|---|---|---|
| English | [Trial](https://monitor.boteffex.eu/trial) | [Offer](https://monitor.boteffex.eu/en/setup.html) | [Sample](https://monitor.boteffex.eu/en/sample-report.html) | [Docs](docs/managed-monitor/en/setup.md) |
| Čeština | [Zkouška](https://monitor.boteffex.eu/cs/trial.html) | [Nabídka](https://monitor.boteffex.eu/cs/setup.html) | [Ukázka](https://monitor.boteffex.eu/cs/sample-report.html) | [Dokumenty](docs/managed-monitor/cs/setup.md) |
| Slovenčina | [Skúška](https://monitor.boteffex.eu/sk/trial.html) | [Ponuka](https://monitor.boteffex.eu/sk/setup.html) | [Ukážka](https://monitor.boteffex.eu/sk/sample-report.html) | [Dokumenty](docs/managed-monitor/sk/setup.md) |

Sample report answers and results are fictional; they are not customer measurements. Reports for the setup service are manually prepared. Automatic client report export and a multi-client agency dashboard are not current features. Contact [info@marketingsrdcem.com](mailto:info@marketingsrdcem.com) to discuss compatibility and a quote. Never post credentials or customer data in public issues.

## License and support

MIT license. The kit is provided as-is. To report a bug, open an issue with a minimal redacted config and the error message. Never post credentials or customer data. The hosted service is a separate product; its private code is not in this repository.
