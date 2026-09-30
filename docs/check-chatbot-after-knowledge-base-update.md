# How to check an n8n chatbot's answers after a knowledge-base update

A chatbot endpoint can return HTTP 200 while giving customers the wrong contact details or an unsupported promise. A useful regression check asks the same important questions again and compares the answers with rules you agreed in advance.

This walkthrough uses the free, open-source Chatbot QA Kit. It starts with saved answers, so you can see a failure and a repair without connecting to n8n or paying for AI calls. You can then adapt the configuration to an authorized chatbot webhook.

**All business details, answers and results in this walkthrough are fictional.** The example demonstrates literal checks; it is not a customer case study or evidence of real chatbot reliability.

## 1. Start with five facts your client cares about

For our fictional studio, we protect a contact email, a service name, a location, a maintenance condition and the response to an unknown price.

| Question | Expected detail | Why we check it |
|---|---|---|
| How can I contact you? | hello@javor.example | Customers need the agreed contact address. |
| Do you build online shops? | online shops | A supported service should not disappear. |
| Where are you based? | Brno | The bot should preserve an agreed location. |
| Does maintenance include content updates? | by agreement | A conditional service must not become an unlimited promise. |
| How much is a custom integration? | individual quote | The bot should not invent a fixed price. |

For a real chatbot, ask its owner to approve the facts, source pages and expected wording. Stable identifiers such as email addresses make stronger literal assertions than sentences that can be paraphrased in many valid ways.

## 2. Run the saved-answer example

Download or clone the repository. Python 3.10 or later is required; the runner has no third-party dependencies.

```bash
git clone https://github.com/Milos1616Milos/chatbot-qa-kit.git
cd chatbot-qa-kit
python qa.py examples/knowledge-base-update.json --output before-report.md
```

This command runs offline. It uses the sample answers stored in the JSON file and does not contact any website. The example deliberately contains one missing email address, so the command exits with code 1.

The expected result is four passed checks and one failed check. The generated before-report.md identifies the contact question and its missing required phrase. The companion before-report.json contains the structured result.

Here is the failing case:

```json
{
  "id": "contact",
  "question": "How can I contact you?",
  "sample_answer": "Please use our contact form.",
  "must_contain": ["hello@javor.example"]
}
```

HTTP 200 alone would not detect this omission. The required-phrase assertion does.

## 3. See what a repaired answer changes

Run the repaired offline example:

```bash
python qa.py examples/knowledge-base-update-fixed.json --output after-report.md
```

Only the fictional contact answer has changed: it now includes hello@javor.example. All five checks pass and the command exits with code 0. The questions and rules are unchanged.

In real work, verify the actual source information and repair the chatbot or its knowledge base before rerunning. Do not loosen an assertion merely to make an incorrect answer pass. If a business fact changed intentionally, get approval for the new expectation.

## 4. Adapt the example to your n8n webhook

Copy the example to a private configuration file. Confirm the request and response formats of your actual workflow. The example expects a POST with a message field and a JSON response with an answer field:

```json
{
  "request": {
    "url": "https://your-domain.example/webhook/chat",
    "body": {"message": "{{question}}"},
    "timeout_seconds": 15
  },
  "answer_path": "answer"
}
```

This is a configuration fragment; keep the cases array in your complete file. Replace the placeholder URL, fictional questions and rules. Use output.answer for a nested response such as {"output":{"answer":"..."}}, or an empty answer_path for plain-text responses.

If the endpoint uses bearer authentication, request.bearer_token_env should contain the name of an environment variable. Supply its value locally or through CI secrets. Never commit a token or share private endpoint details in a public issue.

Then run one authorized live check:

```bash
python qa.py path/to/private-config.json --live --output live-report.md
```

Live mode sends one POST per case and can incur AI-provider charges. It can also trigger downstream workflow actions. Confirm authorization, request volume and side effects before testing. With five cases, one run makes five requests; the runner does not retry failed calls.

## 5. Interpret a failure before acting on it

Phrase matching ignores case but is otherwise literal. A correct paraphrase may fail a narrow rule; an incorrect sentence may contain the required phrase and pass. These checks do not establish general factual accuracy or understand the entire answer.

The kit also supports forbidden phrases, alternative acceptable phrases, expected HTTP status and latency limits. Its reports omit answer bodies and request headers, but include questions and findings. Review them before sharing because a question itself can contain sensitive information.

Compare the returned answer privately with the approved source. Distinguish a missing business detail from a timeout, a changed JSON response format or an outdated expectation. One run does not establish a reliability trend.

## 6. Repeat after changes, then consider daily monitoring

For workflows you maintain yourself, run the same approved checks after a knowledge-base or workflow change. The repository includes a GitHub Action for CI use. Enable scheduled live calls only after agreeing on the endpoint and volume.

If you prefer an assisted service, BotEffex Monitor offers a 14-day trial with no card, starting after a working connection is verified. The hosted pilot currently supports public HTTPS endpoints returning JSON without credentials; this is narrower than the free kit's bearer-token support.

Starter continuation is voluntary: €19 per month for one chatbot and up to 10 questions, with daily checks, email alerts and 30-day history. Paddle displays the final total and renewal terms. Optional one-time setup is a separate service; see the offer for scope and ordering details.

Use the free kit if you want to operate the checks yourself. Request a Monitor trial if you want help connecting a compatible chatbot and running approved daily checks.

## Resources

- Free tool and runnable examples: https://github.com/Milos1616Milos/chatbot-qa-kit
- Assisted trial: https://monitor.boteffex.eu/trial
- Optional setup service: https://monitor.boteffex.eu/en/setup.html
- Illustrative client report: https://monitor.boteffex.eu/en/sample-report.html

Miloš Brisuda · BotEffex Monitor · info@marketingsrdcem.com

Disclosure: this guide was prepared with AI assistance and checked against the runnable examples. Published 30 September 2026.
