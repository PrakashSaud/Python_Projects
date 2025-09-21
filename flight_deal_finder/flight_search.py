"""
flight_search.py
----------------
Handles all interactions with the Amadeus API for:
1. Retrieving IATA codes for cities.
2. Searching for flights (direct and indirect) between origin and destination.
"""

import os
from datetime import datetime
from typing import Optional, Dict
import requests
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt

# Load environment variables from .env file
load_dotenv()

# Amadeus API endpoints
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"


class FlightSearch:
    """
    Provides methods to search flights and get IATA codes using Amadeus API.
    """

    def __init__(self) -> None:
        """
        Initialize FlightSearch instance.
        Retrieves API credentials from environment variables and obtains a new access token.
        """
        self._api_key: str = os.environ["AMADEUS_API_KEY"]
        self._api_secret: str = os.environ["AMADEUS_SECRET"]
        self._token: str = self._get_new_token()

    @retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
    def _get_new_token(self) -> str:
        """
        Generates a new OAuth2 token for Amadeus API.

        Returns:
            str: Access token for API calls.
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=headers, data=body)
        response.raise_for_status()
        token_data = response.json()
        print(f"New Amadeus token obtained. Expires in {token_data['expires_in']} seconds.")
        return token_data['access_token']

    @retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
    def get_destination_code(self, city_name: str) -> str:
        """
        Retrieves the IATA airport code for a given city.

        Args:
            city_name (str): Name of the city to search.

        Returns:
            str: IATA code if found, "N/A" if not found due to IndexError,
                 or "Not Found" if key is missing.
        """
        headers = {"Authorization": f"Bearer {self._token}"}
        params = {"keyword": city_name, "max": "2", "include": "AIRPORTS"}

        response = requests.get(IATA_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()

        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"No airport code found for {city_name} (IndexError).")
            return "N/A"
        except KeyError:
            print(f"No airport code found for {city_name} (KeyError).")
            return "Not Found"

        return code

    @retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
    def check_flights(
        self,
        origin_city_code: str,
        destination_city_code: str,
        from_time: datetime,
        to_time: datetime,
        is_direct: bool = True
    ) -> Optional[Dict]:
        """
        Searches for flights between two cities within the given date range.

        Args:
            origin_city_code (str): IATA code of the origin city.
            destination_city_code (str): IATA code of the destination city.
            from_time (datetime): Departure date.
            to_time (datetime): Return date.
            is_direct (bool): Whether to search only direct flights.

        Returns:
            Optional[Dict]: Flight offers data from Amadeus API, or None if error occurs.
        """
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true" if is_direct else "false",
            "currencyCode": "GBP",
            "max": "10",
        }

        response = requests.get(FLIGHT_ENDPOINT, headers=headers, params=query)

        if response.status_code != 200:
            print(f"Flight search failed for {origin_city_code} -> {destination_city_code}. "
                  f"Status code: {response.status_code}")
            print("Response:", response.text)
            return None

        return response.json()