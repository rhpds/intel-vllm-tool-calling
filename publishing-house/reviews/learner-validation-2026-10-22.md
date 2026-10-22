# Tool Calling: learner validation and PH author review

Tracking: [GPTEINFRA-17784](https://issues.redhat.com/browse/GPTEINFRA-17784); [RHDPCD-2147](https://issues.redhat.com/browse/RHDPCD-2147).

## Reviewable fixes

The actual Module 4 loop now rejects text-only replies when a tool is required, validates tool arguments before dispatch, records successful tools, rejects empty final answers, and fails at the round limit. A synthetic SDK regression replays the tool-call/result/final-answer history. Module 2 now distinguishes basic generation from tool capability. Module 5 now validates arguments, correlation IDs, tool/round budgets and required-tool completion. Its dependent employee/weather query requires a prior-round employee result and the returned office; a same-round city guess cannot count as successful data flow. Fourteen additional synthetic regressions execute the actual multi-tool learner code.

## Verification boundary

32 local regression tests pass (including eight author-workspace auth checks). Antora 3.1.14 builds the current learner source. These are offline author-package results; synthetic service replies do not establish real model or catalog acceptance.

Fresh Dallas October 22 checks: granite-3-2-8b-instruct-cpu returned HTTP 400; qwen25-3b-cpu returned no structured tool_calls; qwen3-14b was not allocated. No full live tool round trip passed. The model/parser/chat-template combination is still an infrastructure gate; Oberon is an alternate dev candidate, not yet verified.

## Requested reviewer actions

Assign a tested tool-capable model/parser/chat template, run the exact auto-tool-choice exercises through a real tool result and final answer, then replay multi-tool/error/no-tool cases and time the learner pilot. Do not substitute a forced function name for successful auto selection.

PH maintainers must accept the intake/design, run supported RCARS/intake ingestion and generate the AgnosticV/QA wiring. Browser PH notes are the available reconciliation channel; local API access is unavailable. Dallas and Oberon are development environments, not catalog-onboarding substitutes. Do not advance acceptance tasks or PH stages from these offline checks. Preserve the related source/reference PR history and keep every RHDP PR linked to its onboarding Jira.
