from unittest.mock import Mock, patch

import pytest
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

from hockey_stat.requester import BASE_URL, make_request


@pytest.fixture
def sample_html():
    return "<html><body>Test page</body></html>"


class TestMakeRequest:

    @patch("hockey_stat.requester.requests.get")
    def test_successful_request(self, mock_get, sample_html):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = sample_html
        mock_get.return_value = mock_response

        result = make_request("/test")

        mock_get.assert_called_once_with(f"{BASE_URL}/test", params=None, timeout=10)
        mock_response.raise_for_status.assert_called_once()
        assert result == sample_html

    @patch("hockey_stat.requester.requests.get")
    def test_with_params(self, mock_get, sample_html):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = sample_html
        mock_get.return_value = mock_response

        params = {"season": 2025}
        make_request("/players", params=params)

        mock_get.assert_called_once_with(f"{BASE_URL}/players", params=params, timeout=10)

    @patch("hockey_stat.requester.requests.get")
    def test_http_error_404(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        result = make_request("/not-found")
        assert result is None

    @patch("hockey_stat.requester.requests.get")
    def test_timeout(self, mock_get):
        mock_get.side_effect = Timeout()
        result = make_request("/timeout")
        assert result is None

    @patch("hockey_stat.requester.requests.get")
    def test_connection_error(self, mock_get):
        mock_get.side_effect = ConnectionError("No connection")
        result = make_request("/offline")
        assert result is None

    @patch("hockey_stat.requester.requests.get")
    def test_generic_request_exception(self, mock_get):
        mock_get.side_effect = RequestException("Unknown error")
        result = make_request("/error")
        assert result is None

    @patch("hockey_stat.requester.logger")
    @patch("hockey_stat.requester.requests.get")
    def test_error_logging(self, mock_get, mock_logger):
        mock_get.side_effect = ConnectionError("Test error")
        make_request("/error")

        mock_logger.error.assert_called_once()
        assert "Request failed" in mock_logger.error.call_args[0][0]
