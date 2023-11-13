import smtplib
from email.mime.text import MIMEText


subject = "Betreff"
sender_adress ="Erik <test_email10@zohomail.eu>"
reciever_adress ="test_email10@zohomail.eu"

class Email_Notification:
    def send_notification(temperature_string):
        mail = MIMEText(temperature_string)
        mail['Subject'] = subject
        mail['From'] = sender_adress
        mail['To'] = reciever_adress

        sender = smtplib.SMTP("smtp.zoho.eu", 587)
        sender.ehlo()
        sender.starttls()
        sender.ehlo()

        sender.login("test_email10@zohomail.eu","MeinPasswort2023")
        sender.send_message(mail)
        sender.close()