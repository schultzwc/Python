from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
from datetime import datetime
import smtplib
from email.message import EmailMessage
import ssl
import psycopg2


def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}', format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None and content_type.find('html') > -1)


def log_error(e):
    print(e)


def get_release():
    website = 'https://docs.microsoft.com/en-us/power-bi/desktop-latest-update'
    page = simple_get(website)
    page_parse = BeautifulSoup(page, 'lxml')
    release_date_line = page_parse.find('meta', {'name':'ms.date'})
    release_date = release_date_line['content']
    new_date = datetime.strptime(release_date, '%m/%d/%Y')

    return new_date


def send_mail():
    port =  465
    email = 'wcschultz42@gmail.com'
    password = '2433006Ws'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        msg = EmailMessage()
        msg.set_content('A new version of Power BI has been released.')
        msg['Subject'] = 'New Power BI Update'
        msg['From'] = email
        msg['To'] = '6124994263@vtext.com'
        server.login(email, password)
        server.send_message(msg)
        server.quit()


def get_last_update(connection):
    select_query = "SELECT dbo.\"usp_SEL_Application_Last_Update\"('Power BI Desktop')"
    cursor = connection.cursor()
    try:
        cursor.execute(select_query)
        records = cursor.fetchall()

        for record in records:
            previous_update = record[0]
            old_update = datetime.strptime(str(previous_update), '%Y-%m-%d')
        return old_update
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        return datetime.strptime(str('01/01/2000'), '%m/%d/%Y')
    finally:
        cursor.close()


def set_last_update(connection, latest_update_date):
    update_query = "select dbo.\"usp_UPD_Application_Update_Date\"('Power BI Desktop', '" + latest_update_date + "')"
    cursor = connection.cursor()
    try:
        cursor.execute(update_query)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        cursor.close()


connection = psycopg2.connect(host="192.168.0.175", port="5432", database="Power_BI", user="wschultz", password="2433006Ws")
now = datetime.now()

last_update = get_last_update(connection).date()
latest_release_date = get_release().date()

if latest_release_date > last_update:
    send_mail()
    set_last_update(connection, str(latest_release_date))

if connection:
    connection.close()


