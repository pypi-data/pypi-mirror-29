from .client_exceptions import JobNameConflict

def test_name_conflict_error_message(mocker):
    exception = JobNameConflict(['6789-6789-6789', '4567-4567-4567'])

    assert str(exception) == """Job name resolves to multiple ids:
6789-6789-6789
4567-4567-4567
Cannot proceed. Please rerun this command with one of the id's above."""

