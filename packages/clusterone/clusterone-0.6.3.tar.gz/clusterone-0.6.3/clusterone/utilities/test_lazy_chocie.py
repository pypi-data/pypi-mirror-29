from .lazy_choice import LazyChoice, lazify

def test_choice_is_lazy(mocker):
    sample_callable = mocker.Mock(return_value="Sample return")

    choice = LazyChoice(sample_callable)
    assert not sample_callable.called

    assert choice.choices == "Sample return"
    assert sample_callable.called

def test_lazify(mocker):
    test_function = mocker.Mock(return_value="dummy")

    under_test = lazify(test_function)
    assert not test_function.called
    # function evalution shall be delayed after decorator aplication

    precalled_under_test = under_test("params")
    assert not test_function.called
    # function evalution shall be delayed after passing parameters to original function

    assert precalled_under_test() == "dummy"
    assert test_function.called
