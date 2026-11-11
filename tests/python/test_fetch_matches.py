
import unittest

from src.pipeline.fetch_matches import fetch_all_matches


class FakeClient:
    def __init__(self):
        self.pages_requested = []

    def get_matches(self, **params):
        page = params["page"]
        self.pages_requested.append(page)

        if page > 5:
            raise AssertionError(
                "Requested a page beyond total_pages"
            )

        return {
            "data": [
                {"id": f"match_{page}_{i}"}
                for i in range(20)
            ],
            "meta": {
                "page": page,
                "per_page": 20,
                "total": 100,
                "total_pages": 5
            }
        }


class TestFetchMatches(unittest.TestCase):
    def test_stops_at_last_page(self):
        client = FakeClient()

        matches = fetch_all_matches(client=client)

        self.assertEqual(len(matches), 100)
        self.assertEqual(
            client.pages_requested,
            [1, 2, 3, 4, 5]
        )


if __name__ == "__main__":
    unittest.main()
