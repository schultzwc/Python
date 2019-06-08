from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import datetime
import smtplib
from email.message import EmailMessage
import ssl

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

def check_release(wildcard):
    website = 'https://docs.microsoft.com/en-us/power-bi/desktop-latest-update'
    page = simple_get(website)
    page_parse = BeautifulSoup(page, 'lxml')
    release_date_line = page_parse.find('meta', {'name':'ms.date'})
    release_date = release_date_line['content']
    date_wildcard = re.compile(wildcard)

    if date_wildcard.findall(release_date):
        return 'match'
    else:
        return 'no match'

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
        msg['To'] = '6124994263@tmomail.net'
        server.login(email, password)
        server.send_message(msg)
        server.quit()


now = datetime.datetime.now()
wildcard = str(now.month) + '/../' + str(now.year)
result = check_release(wildcard)

if result == 'match':
    send_mail()