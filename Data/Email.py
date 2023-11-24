from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import smtplib

class Email_Notification:
    @staticmethod
    def send_email(sender_address, receiver_address, email_subject, multi_line_text, csv_filename="SensorMessungen.csv", pdf_filename="SensorMessungen.pdf", excel_filename="SensorMessungen.xlsx"):
        #E-Mail erstellen
        mail = MIMEMultipart()
        mail['Subject'] = email_subject
        mail['From'] = sender_address
        mail['To'] = receiver_address

        #E-Mail-Text hinzufügen
        mail.attach(MIMEText(multi_line_text, 'plain'))

        #CSV-Anhang hinzufügen
        if csv_filename:
            attachment = open(csv_filename, 'rb')
            csv_attachment_data = MIMEBase('application', 'octet-stream')
            csv_attachment_data.set_payload(attachment.read())
            encoders.encode_base64(csv_attachment_data)
            csv_attachment_data.add_header('Content-Disposition', f'attachment; filename={csv_filename}')
            mail.attach(csv_attachment_data)
            attachment.close()

        #PDF-Anhang hinzufügen
        if pdf_filename:
            pdf_attachment = open(pdf_filename, 'rb')
            pdf_attachment_data = MIMEApplication(pdf_attachment.read(), _subtype="pdf")
            pdf_attachment.close()
            pdf_attachment_data.add_header('Content-Disposition', f'attachment; filename={pdf_filename}')
            mail.attach(pdf_attachment_data)
            attachment.close()

        #Excel-Anhang hinzufügen
        if excel_filename:
            excel_attachment = open(excel_filename, 'rb')
            excel_attachment_data = MIMEApplication(excel_attachment.read(), _subtype="xlsx")
            excel_attachment.close()
            excel_attachment_data.add_header('Content-Disposition', f'attachment; filename={excel_filename}')
            mail.attach(excel_attachment_data)
            attachment.close()

        #E-Mail senden
        sender = smtplib.SMTP("smtp.zoho.eu", 587)
        sender.ehlo()
        sender.starttls()
        sender.ehlo()

        sender.login(sender_address,"MeinPasswort2023")
        sender.send_message(mail)
        sender.close()

        print(f'E-Mail erfolgreich versendet: {email_subject}')
