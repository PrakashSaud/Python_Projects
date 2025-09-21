"""
flight_data.py
----------------
Defines FlightData class to store flight details and a helper function to find the cheapest flight
from API response data.
"""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class FlightData:
    """
    Stores information about a flight.
    
    Attributes:
        price (float | str): Price of the flight in GBP, or "N/A" if unavailable.
        origin_airport (str): IATA code of origin airport.
        destination_airport (str): IATA code of destination airport.
        out_date (str): Departure date (YYYY-MM-DD).
        return_date (str): Return date (YYYY-MM-DD).
        stops (int | str): Number of stops; 0 for direct flights, "N/A" if unavailable.
    """
    price: float | str
    origin_airport: str
    destination_airport: str
    out_date: str
    return_date: str
    stops: int | str


def find_cheapest_flight(data: Dict[str, Any]) -> FlightData:
    """
    Finds the cheapest flight from a given Amadeus API response.
    
    Args:
        data (dict): JSON data returned by Amadeus flight search API.
    
    Returns:
        FlightData: Object representing the cheapest flight found.
                    If no valid flights are found, all fields are "N/A".
    """
    # Handle empty or invalid data
    if not data or not data.get('data'):
        print("No flight data available.")
        return FlightData(
            price="N/A",
            origin_airport="N/A",
            destination_airport="N/A",
            out_date="N/A",
            return_date="N/A",
            stops="N/A"
        )

    # Start with the first flight as the initial cheapest
    first_flight = data['data'][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    nr_stops = len(first_flight["itineraries"][0]["segments"]) - 1
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination = first_flight["itineraries"][0]["segments"][nr_stops]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, nr_stops)

    # Loop through all flights to find the cheapest one
    for flight in data["data"]:
        price = float(flight["price"]["grandTotal"])
        if price < lowest_price:
            lowest_price = price
            nr_stops = len(flight["itineraries"][0]["segments"]) - 1
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = flight["itineraries"][0]["segments"][nr_stops]["arrival"]["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, nr_stops)
            print(f"New lowest price to {destination}: £{lowest_price}")

    return cheapest_flight