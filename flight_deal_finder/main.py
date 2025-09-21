"""
main.py
--------
Orchestrates the workflow of the Flight Deal Finder:
1. Retrieves destinations and customer data.
2. Updates missing IATA codes.
3. Searches for direct and indirect flights.
4. Finds cheapest flights.
5. Sends notifications (SMS, WhatsApp, Email) to customers.
"""

import time
from datetime import datetime, timedelta
from typing import List, Dict

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData, find_cheapest_flight
from notification_manager import NotificationManager


# -------------------- SETUP --------------------

# Initialize modules
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Define origin airport
ORIGIN_CITY_IATA = "LON"

# -------------------- UPDATE DESTINATION CODES --------------------

sheet_data: List[Dict] = data_manager.get_destination_data()

for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        # Avoid hitting API rate limits
        time.sleep(2)

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()
print(f"Updated destination data:\n{sheet_data}")

# -------------------- RETRIEVE CUSTOMER EMAILS --------------------

customer_data: List[Dict] = data_manager.get_customer_emails()
# Extract emails from sheet; adjust column name if different
customer_email_list: List[str] = [row["whatIsYourEmail?"] for row in customer_data]

# -------------------- FLIGHT SEARCH --------------------

# Define date range for flights: tomorrow to 6 months from today
tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=6 * 30)

for destination in sheet_data:
    print(f"Searching flights to {destination['city']}...")

    # Search direct flights first
    flights = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_today,
        is_direct=True
    )

    cheapest_flight: FlightData = find_cheapest_flight(flights)

    print(f"{destination['city']} - Direct flight: £{cheapest_flight.price}")

    # If no direct flight found, search for indirect flights
    if cheapest_flight.price == "N/A":
        print(f"No direct flights to {destination['city']}. Checking indirect flights...")
        flights = flight_search.check_flights(
            origin_city_code=ORIGIN_CITY_IATA,
            destination_city_code=destination["iataCode"],
            from_time=tomorrow,
            to_time=six_months_from_today,
            is_direct=False
        )
        cheapest_flight = find_cheapest_flight(flights)
        print(f"{destination['city']} - Cheapest indirect flight: £{cheapest_flight.price}")

    # -------------------- SEND NOTIFICATIONS --------------------
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        # Customize message based on number of stops
        if cheapest_flight.stops == 0:
            message = (
                f"Low price alert! Only GBP {cheapest_flight.price} to fly direct "
                f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."
            )
        else:
            message = (
                f"Low price alert! Only GBP {cheapest_flight.price} to fly "
                f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport} "
                f"with {cheapest_flight.stops} stop(s), "
                f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."
            )

        print(f"Lower price found for {destination['city']}. Sending notifications...")

        # Send notifications
        # notification_manager.send_sms(message)  # Uncomment if SMS is configured
        notification_manager.send_whatsapp(message)
        notification_manager.send_emails(customer_email_list, message)

        print(f"Notifications sent for {destination['city']}.\n")

    # Respect API rate limits
    time.sleep(2)