import unittest

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


if __name__ == "__main__":
    unittest.main()