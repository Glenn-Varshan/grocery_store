from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from jinja2 import Template

SMTP_HOST="localhost"
SMTP_PORT = 1025
SENDER_EMAIL = "grocery@gmail.com"
SENDER_PASSWORD = ''

def send_message(to,subject,content_body):
    msg = MIMEMultipart()
    msg['To']=to
    msg['Subject']=subject
    msg['From']=SENDER_EMAIL
    msg_body =MIMEText(content_body,'html')
    msg.attach(msg_body)
    client = SMTP(host=SMTP_HOST, port = SMTP_PORT)
    client.send_message(msg=msg)
    client.quit()

def send_message_daily(to,subject,content_body):
    msg = MIMEMultipart()
    msg['To']=to
    msg['Subject']=subject
    msg['From']=SENDER_EMAIL
    msg_body =MIMEText(content_body,'html')
    msg.attach(msg_body)
    client = SMTP(host=SMTP_HOST, port = SMTP_PORT)
    client.send_message(msg=msg)
    client.quit()




