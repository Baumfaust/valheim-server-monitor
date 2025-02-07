from monitor.valheim_log_parser import (
    LogEntry,
    ValheimSession,
    handle_message,
    parse_valheim_log,
)  # Import the dataclass


def test_parse_valheim_log():
    """Tests the parse_valheim_log function with various log entries."""
    # Positive test cases
    test_cases = [
        (
            'Session "MyServer" with join code 12345 and IP 192.168.1.100:2456 is active with 5 player(s)',
            ValheimSession("MyServer", 12345, "192.168.1.100:2456", 5),
        ),
        (
            'Session "AnotherServer" with join code 987654321 and IP 10.0.0.1:2457 is active with 0 player(s)',
            ValheimSession("AnotherServer", 987654321, "10.0.0.1:2457", 0),
        ),
        (
            'Session "Server with spaces" with join code 00000 and IP 127.0.0.1:1234 is active with 1 player(s)',
            ValheimSession("Server with spaces", 0, "127.0.0.1:1234", 1),
        ),
        (
            # test for dash in join code. should fail
            'Session "Server-with-dashes" with join code 123-456 and IP 127.0.0.1:1234 is active with 1 player(s)',
            None,
        ),
        (
            # correct test case for dash in servername
            'Session "Server-with-dashes" with join code 123456 and IP 127.0.0.1:1234 is active with 1 player(s)',
            ValheimSession("Server-with-dashes", 123456, "127.0.0.1:1234", 1),
        ),
    ]

    for log_entry, expected_result in test_cases:
        actual_result = parse_valheim_log(log_entry)
        assert actual_result == expected_result, (
            f"Test failed for input: '{log_entry}'. Expected: {expected_result}, Got: {actual_result}"
        )

    # Negative test cases (no match)
    negative_test_cases = [
        "This is not a valid log entry.",
        'Session "Missing IP" with join code 12345 is active with 2 player(s)',
        'Session "Missing players" with join code 12345 and IP 192.168.1.1:2456 is active with player(s)',
        'Session "Wrong format" with join code abcde and IP 192.168.1.1:2456 is active with 2 player(s)',
    ]
    for log_entry in negative_test_cases:
        actual_result = parse_valheim_log(log_entry)
        assert actual_result is None, (
            f"Negative test failed for input: '{log_entry}'. Expected None, Got: {actual_result}"
        )


def test_handle_message_with_callback():
    called_with = []

    def mock_callback(log_entry: LogEntry):
        called_with.append(log_entry)

    test_entry = {
        "MESSAGE": 'Session "TestServer" with join code 12345 and IP 127.0.0.1:2456 is active with 2 player(s)',
    }
    handle_message(mock_callback, test_entry)
    assert len(called_with) == 1
    assert isinstance(called_with[0], LogEntry)
    assert called_with[0].session_name == "TestServer"


def test_handle_message_no_callback():
    test_entry = {
        "MESSAGE": 'Session "TestServer" with join code 12345 and IP 127.0.0.1:2456 is active with 2 player(s)',
    }
    handle_message(None, test_entry)


def test_handle_message_no_message_key():
    called_with = []

    def mock_callback(log_entry: LogEntry):
        called_with.append(log_entry)

    test_entry = {"OTHER_KEY": "some value"}
    handle_message(mock_callback, test_entry)
    assert len(called_with) == 0


def test_handle_message_parse_returns_none():
    called_with = []

    def mock_callback(log_entry: LogEntry):
        called_with.append(log_entry)

    test_entry = {"MESSAGE": "This is not a valid log entry"}
    handle_message(mock_callback, test_entry)
    assert len(called_with) == 0
