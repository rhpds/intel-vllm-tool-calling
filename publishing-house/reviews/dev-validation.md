# Dev validation evidence

## Development validation — 2026-10-20

Dallas OCP 4.18.16 is a dev environment, separate from the proposed published target. Tests did not order a catalog item or establish published-lab acceptance. Existing dev model credentials were used only in memory for short synthetic requests; they were not copied into fixture workloads.

- Catalog terminal image: Python 3.12, virtual environment and OpenAI client installation PASS with its normal HOME.
- `granite-3-2-8b-instruct-cpu`: HTTP 400; serving response identifies missing auto-tool-choice/parser flags.
- `qwen25-3b-cpu`: HTTP success but no structured tool call, including with a system prompt. Tool-call acceptance FAIL.
- Proposed `qwen3-14b` is absent from the existing dev allocation. Obtain a tested tool-capable model and matching parser/template through PH infrastructure review. Do not substitute an unverified model.
- Full tool-result round trip remains blocked on that endpoint.

Source fixes and this migration draft need author/reviewer acceptance. No workstream is marked complete.
