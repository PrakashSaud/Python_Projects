"""
data_manager.py
----------------
Handles interaction with the Sheety API for retrieving and updating:
1. Destination data (city names, IATA codes, prices)
2. Customer emails
"""

import os
from typing import List, Dict
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt

# Load environment variables from .env file
load_dotenv()


class DataManager:
    """
    Manages all operations related to data stored in Google Sheets via Sheety API.
    """

    def __init__(self) -> None:
        self._user: str = os.environ["SHEETY_USERNAME"]
        self._password: str = os.environ["SHEETY_PASSWORD"]

        # Sheety endpoints
        self.prices_endpoint: str = os.environ["SHEETY_PRICES_ENDPOINT"]
        self.users_endpoint: str = os.environ["SHEETY_USERS_ENDPOINT"]

        # Authorization for HTTP Basic Auth
        self._authorization = HTTPBasicAuth(self._user, self._password)

        # Stores data after fetching from API
        self.destination_data: List[Dict] = []
        self.customer_data: List[Dict] = []

    @retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
    def get_destination_data(self) -> List[Dict]:
        """
        Fetches destination data from the Sheety API.
        
        Returns:
            List[Dict]: List of destination dictionaries with city, IATA code, and lowest price.
        """
        response = requests.get(url=self.prices_endpoint, auth=self._authorization)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
        self.destination_data = data.get("prices", [])
        return self.destination_data

    @retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
    def update_destination_codes(self) -> None:
        """
        Updates the IATA codes for each destination in the Google Sheet via Sheety API.
        Loops through the stored destination_data and performs PUT requests.
        """
        for city in self.destination_data:
            new_data = {"price": {"iataCode": city["iataCode"]}}
            response = requests.put(
                url=f"{self.prices_endpoint}/{city['id']}",
                json=new_data,
                auth=self._authorization
            )
            response.raise_for_status()
            print(f"Updated {city['city']} with IATA code {city['iataCode']}")

    @retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
    def get_customer_emails(self) -> List[Dict]:
        """
        Fetches customer emails from Sheety API.

        Returns:
            List[Dict]: List of customer dictionaries including email addresses.
        """
        response = requests.get(url=self.users_endpoint, auth=self._authorization)
        response.raise_for_status()
        data = response.json()
        self.customer_data = data.get("users", [])
        return self.customer_data