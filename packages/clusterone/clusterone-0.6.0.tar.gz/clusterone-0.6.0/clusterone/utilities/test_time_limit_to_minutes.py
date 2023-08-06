import pytest
from .time_limit_to_minutes import main

def test_hours_only():
    assert main("5h") == 300

def test_minutes_only():
    assert main("22m") == 22

def test_hours_and_minutes():
    assert main("5h22m") == 322

def test_different_case():
    assert main("5H22m") == 322
    assert main("5h22M") == 322
    assert main("5H22M") == 322

def test_invalid_path():
    with pytest.raises(ValueError):
        main('xxx22h55mxxxxx')
