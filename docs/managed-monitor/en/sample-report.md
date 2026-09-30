# BotEffex Monitor — sample initial report

**ILLUSTRATIVE SAMPLE: all answers and results are fictional. No real chatbot was measured.**

Project: Model Studio Javor (fictional)  
Scope: five questions, one text chatbot, one fictional initial run

## What needs attention

Three fictional checks passed and two failed. The contact answer omitted an expected email address; the maintenance answer omitted an agreed condition. These results illustrate the report layout, not the reliability of a real chatbot.

| Question | Agreed rule | Fictional answer | Fictional result |
|---|---|---|---|
| How can I contact you? | Contains kontakt@javor.example | Use our contact form. | Failed: email missing |
| Do you build online shops? | Contains “online shops” | Yes, we build websites and online shops. | Passed |
| Where are you based? | Contains “Brno” | Our studio is based in Brno. | Passed |
| Does maintenance include content updates? | Contains “by agreement” | Maintenance automatically includes all content updates. | Failed: condition missing |
| How much is a custom integration? | Contains “individual quote” when price is unknown | This integration requires an individual quote. | Passed |

The .example domain and every answer above are fictional. No requests were sent to a real endpoint. No actual customer approved these illustrative rules.

## Recommended actions in this fictional case

1. The chatbot owner checks the missing contact email and reruns the check after repair.
2. The owner verifies the actual maintenance terms and corrects the chatbot's source information or answer. Monitor does not repair that content itself.
3. If the business facts changed intentionally, the customer approves updated expectations. Do not change a rule merely to make an incorrect answer pass.

## How to interpret results

“Passed” means the reply contained the agreed wording; it does not prove the entire answer is true or semantically correct. A failure may reflect a bot error, an outdated expectation or an overly strict rule.

A real report separates content failures from endpoint availability, format errors and missing measurements. One run cannot establish a reliability trend. Daily monitoring and alerts start after connection verification and setup approval.

## What a delivered report contains

- Project, measurement period and approved configuration version.
- Sources, source review dates and rules for each question.
- Actual run identifier, timestamp, result and relevant answer excerpt.
- Technical errors or missing data affecting the assessment.
- Recommended actions, responsible person and agreed next step.

This is a template for a manually prepared document. Automatic client report export is not currently a Monitor feature.


---

[Sample client report (en)](https://monitor.boteffex.eu/en/sample-report.html) · [Ukázkový report (cs)](https://monitor.boteffex.eu/cs/sample-report.html) · [Ukážkový report (sk)](https://monitor.boteffex.eu/sk/sample-report.html)

[Free trial](https://monitor.boteffex.eu/trial)
