import requests
from twilio.rest import Client

# Twilio configuration: Replace with your actual Twilio virtual number 
# and the phone number you have verified with Twilio.
VIRTUAL_TWILIO_NUMBER = "your virtual twilio number"
VERIFIED_NUMBER = "your own phone number verified with Twilio"

# Stock and company details for monitoring
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

# API endpoints for stock data (Alpha Vantage) and news (News API)
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# API keys for Alpha Vantage and News API
STOCK_API_KEY = "Y79J01PZ6HSK5GJVS"
NEWS_API_KEY = "3EM9FZY8VJX39X50"

# Twilio account credentials
TWILIO_SID = "YOUR TWILIO ACCOUNT SID"
TWILIO_AUTH_TOKEN = "YOUR TWILIO AUTH TOKEN"

# -------------------- STEP 1: Get Stock Price Data --------------------

# Set parameters to request daily stock data for the given company
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

# Fetch stock price data from Alpha Vantage
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]

# Convert stock data into a list to easily access the most recent days
data_list = [value for (key, value) in data.items()]

# Extract yesterday's closing stock price
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

# Extract the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

# Calculate the absolute difference in stock closing prices
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)

# Determine if the stock went up or down
up_down = "🔺" if difference > 0 else "🔻"

# Calculate the percentage difference between the two days
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)

# -------------------- STEP 2: Get Relevant News Articles --------------------

# Only fetch news if the stock moved significantly (threshold = 1% for testing)
if abs(diff_percent) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    # Fetch company-related news from News API
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    # Select the first 3 articles to avoid spamming with too much news
    three_articles = articles[:3]
    print(three_articles)

    # Format each article with stock movement, headline, and description
    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}"
        for article in three_articles
    ]
    print(formatted_articles)

    # -------------------- STEP 3: Send Alerts via Twilio --------------------

    # Initialize Twilio client with your account credentials
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    # Send each article as a separate SMS message
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )