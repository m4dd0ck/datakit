import pytest
import requests

import api_utils


class FakeSession:
    """Stands in for requests.Session: replays canned outcomes and records calls."""

    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = []
        self.headers = {}

    def request(self, method, url, **kwargs):
        self.calls.append((method, url))
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    def close(self):
        pass


def make_response(status_code, body=b"{}"):
    response = requests.Response()
    response.status_code = status_code
    response.reason = "test"
    response.url = "https://api.test/items"
    response._content = body
    return response


def make_client(outcomes):
    # Reason: two attempts keep the one real backoff sleep to a second.
    client = api_utils.APIClient("https://api.test", max_retries=2)
    client.session = FakeSession(outcomes)
    return client


def test_client_error_is_raised_without_retrying():
    client = make_client([make_response(404), make_response(200)])
    with pytest.raises(requests.HTTPError):
        client.get("/items")
    assert len(client.session.calls) == 1


def test_server_error_is_retried():
    client = make_client([make_response(503), make_response(200, b'{"ok": true}')])
    assert client.get("/items") == {"ok": True}
    assert len(client.session.calls) == 2


def test_connection_error_is_retried():
    client = make_client([requests.ConnectionError("down"), make_response(200, b"[]")])
    assert client.get("/items") == []
    assert len(client.session.calls) == 2


def test_last_error_is_raised_when_retries_run_out():
    client = make_client([make_response(500), make_response(502)])
    with pytest.raises(requests.HTTPError, match="502"):
        client.get("/items")
