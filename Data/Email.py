import sqlite3
import csv
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.mime.base import MIMEBase
from email import encoders
from Data.Sensordb import SensorDatabase

class Email_Notification:
    @staticmethod
    def send_email(sender_address, receiver_address, email_subject, email_text, attachment_filename="SensorMessungen.csv"):
        # E-Mail erstellen
        mail = MIMEMultipart()
        mail['Subject'] = email_subject
        mail['From'] = sender_address
        mail['To'] = receiver_address

        # E-Mail-Text hinzufügen
        mail.attach(MIMEText(email_text, 'plain'))

        if attachment_filename:
            attachment = open(attachment_filename, 'rb')
            attachment_data = MIMEBase('application', 'octet-stream')
            attachment_data.set_payload(attachment.read())
            encoders.encode_base64(attachment_data)
            attachment_data.add_header('Content-Disposition', f'attachment; filename={attachment_filename}')
            mail.attach(attachment_data)
            attachment.close()

        # E-Mail senden
        sender = smtplib.SMTP("smtp.zoho.eu", 587)
        sender.ehlo()
        sender.starttls()
        sender.ehlo()

        sender.login(sender_address,"MeinPasswort2023")
        sender.send_message(mail)
        sender.close()

        print(f'E-Mail erfolgreich versendet: {email_subject}')
