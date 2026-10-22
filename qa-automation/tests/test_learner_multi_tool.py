"""Replay the copied multi-tool exercise without a live endpoint or key."""
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
    monkeypatch.setitem(sys.modules, 'openai', types.SimpleNamespace(OpenAI=lambda **kw: client))
    for name in ('MODEL_URL', 'MODEL_API_KEY', 'MODEL_NAME'):
        monkeypatch.setenv(name, 'synthetic')
    page = Path(__file__).resolve().parents[2] / 'content/modules/ROOT/pages/05-multi-tool-app.adoc'
    code = re.search(r"<< 'PYEOF'\n(.*?)\nPYEOF", page.read_text(), re.S).group(1)
    scope = {}
    exec(compile(code.split('# --- Test Queries ---')[0], str(page), 'exec'), scope)
    return scope, client


def call(name, args, identity):
    return types.SimpleNamespace(id=identity, function=types.SimpleNamespace(name=name, arguments=json.dumps(args)))


def reply(content=None, calls=()):
    return types.SimpleNamespace(choices=[types.SimpleNamespace(message=types.SimpleNamespace(content=content, tool_calls=calls))])


def test_dependent_roundtrip_uses_returned_office(learner):
    scope, client = learner
    client.chat.completions.create.side_effect = [
        reply(calls=[call('lookup_employee', {'employee_id': 12345}, 'employee')]),
        reply(calls=[call('get_weather', {'location': 'Boston'}, 'weather')]),
        reply('Alice works in Boston, where it is 72 F and partly cloudy.')]
    assert 'Boston' in scope['run_query']('employee weather', expected_tools={'lookup_employee', 'get_weather'}, require_employee_weather=True)
    history = client.chat.completions.create.call_args.kwargs['messages']
    results = [m for m in history if isinstance(m, dict) and m.get('role') == 'tool']
    assert [m['tool_call_id'] for m in results] == ['employee', 'weather']
    assert json.loads(results[0]['content'])['office'] == 'Boston'
    assert json.loads(results[1]['content'])['temp'] == 72


@pytest.mark.parametrize('location', ['Boston', 'Austin'])
def test_parallel_guess_does_not_prove_dependency(learner, location):
    scope, client = learner
    client.chat.completions.create.side_effect = [reply(calls=[
        call('lookup_employee', {'employee_id': 12345}, 'employee'),
        call('get_weather', {'location': location}, 'weather')]), reply('A plausible answer')]
    with pytest.raises(RuntimeError, match='Required tools'):
        scope['run_query']('employee weather', expected_tools={'lookup_employee', 'get_weather'}, require_employee_weather=True)


def test_text_only_reply_cannot_pass_tool_requirement(learner):
    scope, client = learner
    client.chat.completions.create.return_value = reply('We have 42 laptops.')
    with pytest.raises(RuntimeError, match='Required tools'):
        scope['run_query']('stock', expected_tools={'check_inventory'})


@pytest.mark.parametrize('raw', ['{', '[]', '{"employee_id":true}', '{"employee_id":"12345"}', '{"employee_id":12345,"extra":0}'])
def test_bad_arguments_are_rejected_before_dispatch(learner, raw):
    scope, _ = learner
    with pytest.raises((ValueError, TypeError)):
        scope['parse_arguments']('lookup_employee', raw)


def test_unknown_city_is_an_error_instead_of_invented_weather(learner):
    scope, _ = learner
    assert 'error' in scope['get_weather']('unlisted-city')


def test_oversized_batch_executes_no_tools(learner):
    scope, client = learner
    dispatch = Mock()
    scope['TOOL_FUNCTIONS']['get_weather'] = dispatch
    client.chat.completions.create.return_value = reply(calls=[call('get_weather', {'location': 'Boston'}, str(i)) for i in range(11)])
    with pytest.raises(RuntimeError, match='budget'):
        scope['run_query']('weather')
    dispatch.assert_not_called()


@pytest.mark.parametrize('ids', [('',), ('same', 'same')])
def test_invalid_correlation_ids_execute_no_tools(learner, ids):
    scope, client = learner
    dispatch = Mock()
    scope['TOOL_FUNCTIONS']['get_weather'] = dispatch
    client.chat.completions.create.return_value = reply(calls=[call('get_weather', {'location': 'Boston'}, identity) for identity in ids])
    with pytest.raises(RuntimeError, match='identifiers'):
        scope['run_query']('weather')
    dispatch.assert_not_called()


def test_round_limit_fails_explicitly(learner):
    scope, client = learner
    client.chat.completions.create.side_effect = [reply(calls=[call('unknown', {}, str(i))]) for i in range(8)]
    with pytest.raises(RuntimeError, match='round limit'):
        scope['run_query']('weather')
    assert client.chat.completions.create.call_count == 8
