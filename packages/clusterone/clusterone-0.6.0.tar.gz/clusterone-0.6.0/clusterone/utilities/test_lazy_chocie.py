from .lazy_choice import LazyChoice

def test_is_lazy(mocker):
    sample_callable = mocker.Mock(return_value="Sample return")

    choice = LazyChoice(sample_callable)
    assert not sample_callable.called

    assert choice.choices == "Sample return"
    assert sample_callable.called
