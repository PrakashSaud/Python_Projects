# Flight Deal Finder

A Python project that searches for the cheapest flights from a specified origin to multiple destinations, and notifies customers when flight prices drop. This project integrates **Sheety API**, **Amadeus API**, and **Twilio** for notifications (SMS, WhatsApp, Email).

---

## Features

1. **Retrieve Destination Data**  
   - Fetches destination cities, IATA codes, and target prices from a Google Sheet via **Sheety API**.  
   - Automatically updates missing IATA codes.

2. **Retrieve Customer Emails**  
   - Fetches customer email addresses from Google Sheet.  
   - Allows sending notifications to all customers.

3. **Flight Search**  
   - Searches for both **direct** and **indirect flights** using **Amadeus API**.  
   - Finds the **cheapest available flight** within a specified date range.  
   - Supports multiple destinations.

4. **Notifications**  
   - Sends **WhatsApp messages**, **emails**, and optionally **SMS** alerts.  
   - Formats messages dynamically based on flight details (price, stops, dates).  
   - Tracks sent messages to avoid duplicates.

5. **Configurable & Safe**  
   - Uses `.env` file to store API keys, email credentials, and phone numbers securely.  
   - Includes **retry mechanisms** for API requests to handle temporary errors.  
   - Adds delays to respect API rate limits.

---

## Project Structure
flight_deal_finder/
│
├── main.py                 # Orchestrates the workflow
├── data_manager.py         # Handles Sheety API (destinations & customers)
├── flight_search.py        # Handles Amadeus API for flights & IATA codes
├── flight_data.py          # Parses flight data and finds cheapest flights
├── notification_manager.py # Sends WhatsApp, SMS, and email notifications
├── requirements.txt        # Dependencies
└── .env                    # Stores API keys and credentials (not tracked in Git)

## Run the Program
python main.py

## 