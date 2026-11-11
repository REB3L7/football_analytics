import unittest
from unittest.mock import MagicMock, patch

from requests.exceptions import HTTPError

from src.pipeline.api_client import SoccerDataClient


class TestAPIRateLimits(unittest.TestCase):

    def setUp(self):
        with patch.dict("os.environ", {"SOCCER_DATA_KEY": "test-key"}):
            self.client = SoccerDataClient()

    def make_response(self, status, retry_after=None):
        response = MagicMock()
        response.status_code = status
        response.headers = {}

        if retry_after is not None:
            response.headers["Retry-After"] = retry_after

        if status >= 400:
            response.raise_for_status.side_effect = HTTPError(
                f"HTTP {status}",
                response=response
            )

        response.json.return_value = {"data": []}
        return response

    @patch("src.pipeline.api_client.time.sleep")
    def test_short_rate_limit_retries_once(self, mock_sleep):
        limited = self.make_response(429, "5")
        success = self.make_response(200)

        self.client.session.get = MagicMock(
            side_effect=[limited, success]
        )

        result = self.client.get("matches")

        self.assertEqual(result, [])
        self.assertEqual(self.client.session.get.call_count, 2)
        mock_sleep.assert_called_once_with(5.0)

    @patch("src.pipeline.api_client.time.sleep")
    def test_long_rate_limit_stops(self, mock_sleep):
        limited = self.make_response(429, "60000")
        self.client.session.get = MagicMock(return_value=limited)

        with self.assertRaises(HTTPError):
            self.client.get("matches")

        self.assertEqual(self.client.session.get.call_count, 1)
        mock_sleep.assert_not_called()

    @patch("src.pipeline.api_client.time.sleep")
    def test_missing_retry_after_stops(self, mock_sleep):
        limited = self.make_response(429)
        self.client.session.get = MagicMock(return_value=limited)

        with self.assertRaises(HTTPError):
            self.client.get("matches")

        self.assertEqual(self.client.session.get.call_count, 1)
        mock_sleep.assert_not_called()

    @patch("src.pipeline.api_client.time.sleep")
    def test_second_rate_limit_stops(self, mock_sleep):
        first = self.make_response(429, "2")
        second = self.make_response(429, "2")

        self.client.session.get = MagicMock(
            side_effect=[first, second]
        )

        with self.assertRaises(HTTPError):
            self.client.get("matches")

        self.assertEqual(self.client.session.get.call_count, 2)
        mock_sleep.assert_called_once_with(2.0)


if __name__ == "__main__":
    unittest.main()