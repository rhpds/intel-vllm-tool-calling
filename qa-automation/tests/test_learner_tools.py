"""Run the learner's actual tool loop with a synthetic SDK and model replies."""
import json
import re
import sys
import types
from pathlib import Path
from unittest.mock import Mock
import pytest

@pytest.fixture
def learner(monkeypatch):
    client = Mock()
    monkeypatch.setitem(sys.modules, "openai", types.SimpleNamespace(OpenAI=lambda **kw: client))
    for name in ("MODEL_URL", "MODEL_API_KEY", "MODEL_NAME"):
        monkeypatch.setenv(name, "synthetic")
    page = Path(__file__).resolve().parents[2] / "content/modules/ROOT/pages/04-build-tool-loop.adoc"
    code = re.search(r"<< 'PYEOF'\n(.*?)\nPYEOF", page.read_text(), re.S).group(1)
    scope = {}
    exec(compile(code.split("# --- Run Three Queries ---")[0], str(page), "exec"), scope)
    return scope, client

def reply(content=None, calls=()):
    return types.SimpleNamespace(choices=[types.SimpleNamespace(message=types.SimpleNamespace(content=content, tool_calls=calls))])

def call(name="get_weather", args='{"location":"Paris"}'):
    return types.SimpleNamespace(id="call-1", function=types.SimpleNamespace(name=name, arguments=args))

def test_round_trip_carries_tool_result_and_final_answer(learner):
    scope, client = learner
    client.chat.completions.create.side_effect = [reply(calls=[call()]), reply("Paris is sunny, 22 C.")]
    assert scope["run_query"]("Paris weather", expected_tool="get_weather") == "Paris is sunny, 22 C."
    history = client.chat.completions.create.call_args.kwargs["messages"]
    assert history[-1]["tool_call_id"] == "call-1"
    assert json.loads(history[-1]["content"])["temp"] == 22

def test_text_only_is_not_a_required_tool_success(learner):
    scope, client = learner
    client.chat.completions.create.return_value = reply("It is sunny.")
    with pytest.raises(RuntimeError, match="Required tool"):
        scope["run_query"]("Paris weather", expected_tool="get_weather")

@pytest.mark.parametrize("name,args", [("shell", "{}"), ("get_weather", "not json"), ("get_weather", "[]"), ("get_weather", '{"location":5}'), ("get_weather", '{"location":"Paris","extra":1}')])
def test_untrusted_arguments_do_not_execute(learner, name, args):
    scope, _ = learner
    assert "error" in scope["dispatch_tool"](name, args)

def test_invalid_tool_result_cannot_satisfy_required_tool(learner):
    scope, client = learner
    client.chat.completions.create.side_effect = [reply(calls=[call(args="[]")]), reply("Done")]
    with pytest.raises(RuntimeError, match="Required tool"):
        scope["run_query"]("Paris weather", expected_tool="get_weather")

def test_round_limit_fails_instead_of_silent_success(learner):
    scope, client = learner
    client.chat.completions.create.return_value = reply(calls=[call()])
    with pytest.raises(RuntimeError, match="round limit"):
        scope["run_query"]("Paris weather", expected_tool="get_weather")
    assert client.chat.completions.create.call_count == 5

def test_no_tool_question_can_finish_directly(learner):
    scope, client = learner
    client.chat.completions.create.return_value = reply("Tokyo")
    assert scope["run_query"]("Capital of Japan") == "Tokyo"
