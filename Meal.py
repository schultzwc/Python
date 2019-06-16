import psycopg2
import ssl
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from datetime import timedelta


def get_meal(connection):
    return 'macaroni'


#def get_ingredients(connection, meal):



def get_recipient(connection):
    return 'schultzwc@yahoo.com'


def send_email(recipient, email_message):
    port = 465
    sender_email = 'wcschultz42@gmail.com'
    receiver_email = recipient
    password = '2433006Ws'
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Test Meals'
    message['From'] = sender_email
    message['To'] = receiver_email
    html_message = MIMEText(email_message, 'html')
    message.attach(html_message)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())



connection = psycopg2.connect(host="192.168.0.175", port="5432", database="Power_BI", user="wschultz", password="2433006Ws")

days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
meals = []

now = datetime.today()
future = now + timedelta(days=7)
WeekStart = datetime.strftime(now, '%B %d, %Y')
WeekEnd = datetime.strftime(future, '%B %d, %Y')

email_message = '''
<html>
    <body>
        <p>Meals for ''' + WeekStart + ' to ' + WeekEnd + '''<br><br>'''

for day in days:
    day_meal = get_meal(connection)
    meals.append(day_meal)
    email_message = email_message + '''
        ''' + day + ''':<br>
            &nbsp&nbsp&nbsp&nbsp''' + day_meal + '<br>'

email_message = email_message + '''
        </p>
    </body>
</html>'''

recipient = get_recipient(connection)
send_email(recipient, email_message)

if connection:
    connection.close()