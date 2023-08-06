from . import main
silent_prompt = main.silent_prompt

def test_silence(capsys, monkeypatch):
    " Does not output to stdout "

    monkeypatch.setattr('sys.stdin.readline', lambda: "Mark")
    silent_prompt()

    captured = capsys.readouterr()

    assert captured.out == ""
    assert captured.err == ""

def test_calls_prompt(mocker):
    main.prompt = mocker.Mock()

    silent_prompt()

    assert main.prompt.called

def test_calls_with_aditional_args(mocker):
    main.prompt = mocker.Mock()

    silent_prompt(testparam="Test value")

    args, kwargs = main.prompt.call_args
    assert kwargs['testparam'] == "Test value"

# Test random name generator

def test_random_job_name(mocker):
    random_name = main.random_job_name()

    tokens = random_name.split('-')
    assert tokens[0] in main.adjs
    assert tokens[1] in main.nouns
    # Range excludes the last number, so 999 would fails, though it's ok
    assert tokens[2] in [str(_) for _ in range(main.MIN_NUM, main.MAX_NUM+1)]
