# 📈 Stock News Alert System  

A Python script that monitors stock price changes using **Alpha Vantage API**, fetches related company news via the **News API**, and sends alerts as **SMS messages** using **Twilio**.  

---

## 🚀 Features
- Tracks daily stock price changes for a given company (e.g., Tesla – TSLA).
- Calculates the percentage difference between consecutive closing prices.
- Fetches the latest 3 news articles about the company if stock movement crosses a threshold.
- Sends each news article as a separate SMS via Twilio.

---

## 🛠️ Technologies Used
- [Alpha Vantage API](https://www.alphavantage.co/documentation/) – Stock price data.  
- [News API](https://newsapi.org/) – Latest company news.  
- [Twilio](https://www.twilio.com/) – SMS notifications.  
- [Requests](https://docs.python-requests.org/en/latest/) – For API calls.  

---

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/PrakashSaud/stock-news-alert.git
   cd stock-news-alert