# Test an n8n chatbot webhook after every change

When a chatbot workflow changes, a previously correct answer can disappear or become an invented promise. This short check catches specific regressions by sending repeatable questions to an HTTP endpoint and checking the returned text.

## 1. Try the check without a live endpoint

From this repository, run:

```bash
python qa.py examples/support-escalation.json --output report.md
```

This uses saved sample answers. It does not call n8n or an AI provider. Open `report.md` to see the result.

## 2. Make a private configuration for your webhook

Copy `example.json` to a private file. Change the request body to match **your** webhook's input. For example, if it accepts a JSON field called `message` and returns `{ "answer": "..." }`, the relevant fields are:

```json
{
  "request": {
    "url": "https://your-domain.example/webhook/chat",
    "body": { "message": "{{question}}" },
    "timeout_seconds": 15
  },
  "answer_path": "answer"
}
```

That JSON is only an illustration. Check your actual webhook request and response before running live. If the reply is nested, use a dotted path such as `output.answer`; if it is plain text, leave `answer_path` empty. Keep the real URL and any tokens out of a public repository.

## 3. Choose business facts worth protecting

Add cases to the `cases` array. Each case needs an `id` and `question`. Here is a policy example:

```json
{
  "id": "returns-policy",
  "question": "Can I return an item after 30 days?",
  "any_of": ["contact support", "returns policy"],
  "must_not_contain": ["guaranteed refund after 30 days"],
  "expected_status": 200
}
```

Use wording that matches your *real* policy. Phrase matching ignores letter case but is otherwise literal, so avoid brittle assertions against variable AI wording. This check can detect a known missing or forbidden phrase; it cannot prove that every answer is correct.

## 4. Run once against the live endpoint

```bash
python qa.py path/to/private-config.json --live --output report.md
```

Live mode sends one POST for each case. Only test endpoints you own or are authorized to test. The workflow might perform other actions or incur AI costs, so start with a few harmless questions. A failed case makes the command exit with code `1`; the report explains which assertion failed.

For a bearer token, set `request.bearer_token_env` to the **name** of an environment variable and provide its value through your local environment or CI secrets. Do not put the token in JSON.

## 5. Repeat it automatically

For a chatbot project on GitHub, use the [GitHub Action example in the README](../README.md#use-it-as-a-github-action). Begin with an offline check in a private repository. Turn on live calls only after you have confirmed the endpoint, secrets, and expected call volume. You can then run the same check when you change your workflow or on a schedule.

If you maintain several client chatbots and want daily checks with history and email alerts without operating the workflow yourself, the separate [managed Monitor pilot form](https://github.com/Milos1616Milos/chatbot-qa-kit/issues/new?template=managed-monitor-pilot.yml) collects interest. The hosted service is still being tested; the form is not a purchase.
