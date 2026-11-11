import os
import requests
import time

from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


load_dotenv()

BASE_URL = "https://api.soccer-data.co/v1"


class SoccerDataClient:

    def __init__(self):
        self.api_key = os.getenv("SOCCER_DATA_KEY")

        if not self.api_key:
            raise ValueError(
                "SOCCER_DATA_KEY is missing from .env"
            )

        self.session = requests.Session()

        # Diagnostic mode: disable automatic retries
        # so rate-limit responses are visible.
        retry_strategy = Retry(
            total=0,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            respect_retry_after_header=False,
            raise_on_status=False
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy
        )

        self.session.mount("https://", adapter)

        # API authentication
        self.session.headers.update({
            "X-Api-Key": self.api_key
        })

    def get(self, endpoint, params=None, include_meta=False):
        url = f"{BASE_URL}/{endpoint.lstrip('/')}"

        for attempt in range(2):
            response = self.session.get(
                url,
                params=params,
                timeout=30
            )

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")

                print("\nAPI RATE LIMIT DETECTED")
                print("Retry-After:", retry_after or "Not provided")

                try:
                    wait_seconds = float(retry_after)
                except (TypeError, ValueError):
                    wait_seconds = None

                if (
                    attempt == 0
                    and wait_seconds is not None
                    and 0 <= wait_seconds <= 60
                ):
                    print(f"Waiting {wait_seconds:g} seconds before retry...")
                    time.sleep(wait_seconds)
                    continue

                print("Stopping request due to rate limit.")

            response.raise_for_status()

            payload = response.json()

            if not isinstance(payload, dict):
                raise ValueError("Unexpected API response")

            if payload.get("error") or payload.get("errors"):
                raise RuntimeError(
                    f"API error: "
                    f"{payload.get('error') or payload.get('errors')}"
                )

            if include_meta:
                return payload

            return payload.get("data", payload)

    def get_matches(self, include_meta=False, **params):
        payload = self.get(
            "matches",
            params=params,
            include_meta=True
        )

        if not isinstance(payload.get("data"), list):
            raise ValueError("Unexpected matches data")

        if not isinstance(payload.get("meta"), dict):
            raise ValueError("Missing pagination metadata")

        if include_meta:
            return payload

        return payload["data"]

        response.raise_for_status()
        payload = response.json()

        if not isinstance(payload, dict):
            raise ValueError("Unexpected API response")

        if payload.get("error") or payload.get("errors"):
            raise RuntimeError(
                f"API error: {payload.get('error') or payload.get('errors')}"
        )

        if not isinstance(payload.get("data"), list):
            raise ValueError("Unexpected matches data")

        if not isinstance(payload.get("meta"), dict):
            raise ValueError("Missing pagination metadata")

        return payload

    def get_player_stats(self, match_id):
        return self.get(
            f"matches/{match_id}/player-stats"
        )
