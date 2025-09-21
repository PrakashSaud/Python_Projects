"""
notification_manager.py
-----------------------
Handles sending notifications to customers via:
1. SMS
2. WhatsApp
3. Email
"""

import os
import smtplib
from typing import List
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class NotificationManager:
    """
    Manages sending notifications for flight deals via SMS, WhatsApp, and email.
    """

    def __init__(self) -> None:
        """
        Initializes Twilio client and email SMTP connection using environment variables.
        """
        # Email configuration
        self.smtp_address: str = os.environ["EMAIL_PROVIDER_SMTP_ADDRESS"]
        self.email: str = os.environ["MY_EMAIL"]
        self.email_password: str = os.environ["MY_EMAIL_PASSWORD"]

        # Twilio configuration
        self.twilio_virtual_number: str = os.environ["TWILIO_VIRTUAL_NUMBER"]
        self.twilio_verified_number: str = os.environ["TWILIO_VERIFIED_NUMBER"]
        self.whatsapp_number: str = os.environ["TWILIO_WHATSAPP_NUMBER"]
        self.client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_AUTH_TOKEN"])

        # SMTP connection (initialized lazily)
        self.connection = smtplib.SMTP(self.smtp_address)

        # Track already sent messages to avoid duplicates
        self.sent_messages: set[str] = set()

    def send_sms(self, message_body: str) -> None:
        """
        Sends an SMS message via Twilio API.

        Args:
            message_body (str): Text content of the SMS.
        """
        if message_body in self.sent_messages:
            print("SMS already sent, skipping duplicate.")
            return

        message = self.client.messages.create(
            from_=self.twilio_virtual_number,
            body=message_body,
            to=self.twilio_verified_number
        )
        self.sent_messages.add(message_body)
        print(f"SMS sent successfully. SID: {message.sid}")

    def send_whatsapp(self, message_body: str) -> None:
        """
        Sends a WhatsApp message via Twilio API.

        Args:
            message_body (str): Text content of the WhatsApp message.
        """
        if message_body in self.sent_messages:
            print("WhatsApp message already sent, skipping duplicate.")
            return

        message = self.client.messages.create(
            from_=f'whatsapp:{self.whatsapp_number}',
            body=message_body,
            to=f'whatsapp:{self.twilio_verified_number}'
        )
        self.sent_messages.add(message_body)
        print(f"WhatsApp message sent successfully. SID: {message.sid}")

    def send_emails(self, email_list: List[str], email_body: str, subject: str = "New Low Price Flight!") -> None:
        """
        Sends emails to a list of recipients with the specified message body.

        Args:
            email_list (List[str]): List of recipient email addresses.
            email_body (str): Content of the email message.
            subject (str): Email subject line (default: "New Low Price Flight!").
        """
        with self.connection:
            self.connection.starttls()
            self.connection.login(self.email, self.email_password)
            for email in email_list:
                message_text = f"Subject:{subject}\n\n{email_body}"
                self.connection.sendmail(
                    from_addr=self.email,
                    to_addrs=email,
                    msg=message_text.encode('utf-8')
                )
                print(f"Email sent to {email}")