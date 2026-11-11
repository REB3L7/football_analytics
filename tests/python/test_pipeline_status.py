import unittest
from unittest.mock import MagicMock, patch
from requests.exceptions import HTTPError

from src.pipeline.run_pipeline import run_pipeline
from src.pipeline.run_pipeline import determine_run_status


class TestPipelineStatus(unittest.TestCase):

    def test_success(self):
        self.assertEqual(
            determine_run_status(5, 0, False),
            "success"
        )

    def test_failure(self):
        self.assertEqual(
            determine_run_status(0, 1, False),
            "failed"
        )

    def test_rate_limited(self):
        self.assertEqual(
            determine_run_status(0, 1, True),
            "rate_limited"
        )

    def test_partial_success(self):
        self.assertEqual(
            determine_run_status(5, 1, True),
            "partial_success"
        )

    @patch("src.pipeline.run_pipeline.finish_run")
    @patch("src.pipeline.run_pipeline.start_run", return_value=99)
    @patch("src.pipeline.run_pipeline.fetch_all_matches")
    @patch("src.pipeline.run_pipeline.SoccerDataClient")
    def test_discovery_rate_limit(
        self,
        mock_client,
        mock_fetch,
        mock_start,
        mock_finish
    ):
        response = MagicMock()
        response.status_code = 429
        response.headers = {"Retry-After": "60000"}

        mock_fetch.side_effect = HTTPError(
            "429 Too Many Requests",
            response=response
        )

        with self.assertRaises(SystemExit) as exit_context:
            run_pipeline(batch_size=5)

        self.assertEqual(exit_context.exception.code, 1)

        mock_fetch.assert_called_once_with(
            client=mock_client.return_value
        )

        mock_finish.assert_called_once()
        logged_values = mock_finish.call_args.kwargs

        self.assertEqual(
            logged_values["status"],
            "rate_limited"
        )
        self.assertEqual(
            logged_values["matches_discovered"],
            0
        )
        self.assertEqual(
            logged_values["matches_processed"],
            0
        )
        self.assertEqual(
            logged_values["matches_failed"],
            1
        )
    @patch("src.pipeline.run_pipeline.finish_run")
    @patch("src.pipeline.run_pipeline.start_run", return_value=100)
    @patch("src.pipeline.run_pipeline.ingest_match", return_value=40)
    @patch("src.pipeline.run_pipeline.match_exists", return_value=False)
    @patch("src.pipeline.run_pipeline.get_connection")
    @patch("src.pipeline.run_pipeline.fetch_all_matches")
    @patch("src.pipeline.run_pipeline.SoccerDataClient")
    def test_partial_ingestion_rate_limit(
        self, mock_client, mock_fetch, mock_connection,
        mock_exists, mock_ingest, mock_start, mock_finish
    ):
        matches = [
            {
                "id": f"match_{i}",
                "home_team": {"name": "Home"},
                "away_team": {"name": "Away"},
            }
            for i in range(3)
        ]

        mock_fetch.return_value = matches

        response = MagicMock()
        response.status_code = 429
        response.headers = {"Retry-After": "60000"}

        mock_client.return_value.get_player_stats.side_effect = [
            [],
            [],
            HTTPError("429 Too Many Requests", response=response),
        ]

        with self.assertRaises(SystemExit) as context:
            run_pipeline(batch_size=3)

        self.assertEqual(context.exception.code, 1)
        self.assertEqual(mock_ingest.call_count, 2)

        logged = mock_finish.call_args.kwargs

        self.assertEqual(logged["status"], "partial_success")
        self.assertEqual(logged["matches_discovered"], 3)
        self.assertEqual(logged["matches_processed"], 2)
        self.assertEqual(logged["matches_failed"], 1)
        self.assertEqual(logged["player_records_processed"], 80)
if __name__ == "__main__":
    unittest.main()