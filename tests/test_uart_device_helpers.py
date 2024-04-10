import pytest
from app.uart_device import is_valid, extract_data, get_result


def test_is_valid_valid_message():
    message = "$123.45,678.90,012.34\n"
    assert is_valid(message)


def test_is_valid_invalid_message_missing_newline():
    message = "$123.45,678.90,012.34"
    assert not is_valid(message)


def test_is_valid_invalid_message_wrong_prefix():
    message = "#123.45,678.90,012.34\n"
    assert not is_valid(message)


def test_extract_data_valid_message():
    message = "$123.45,678.90,012.34\n"
    value1, value2, value3 = extract_data(message)
    assert value1 == 123.45
    assert value2 == 678.90
    assert value3 == 012.34


def test_extract_data_invalid_message():
    message = "invalid message"
    with pytest.raises(ValueError):
        extract_data(message)


def test_get_result_valid_message():
    message = "$command_prefix,data\n"
    result = get_result(message, 'command_prefix')
    assert result == "data"


def test_get_result_invalid_message_missing_prefix():
    message = "$data\n"
    assert get_result(message, "command_prefix") is None


def test_get_result_invalid_message_missing_newline():
    message = "${command_prefix},data"
    assert get_result(message, "command_prefix") is None
