from robobrowser import RoboBrowser
import re
from dotenv import load_dotenv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

username = os.getenv('LDAP')
password = os.getenv('PASSWORD')
roll_number = os.getenv('ROLL_NUMBER')
sender_id = os.getenv('MAIL_SENDER_ID')
receiver_id = os.getenv('MAIL_RECEIVER_ID')
sender_pwd = os.getenv('MAIL_SENDER_PASSWORD')

browser = RoboBrowser()
base_url = "http://172.16.100.161:8080/Aryabhatta/"
mails = "http://intra.iitj.ac.in:8080/Aryabhatta/inboxStudent.do"
browser.open(base_url)
form = browser.get_form()
form['userid'].value = username
form['password'].value = password
browser.submit_form(form)

fetch_mail_link = browser.find_all('a', href=re.compile('inbox'))
mail_link = base_url + fetch_mail_link[0]['href']
browser.open(mail_link)


def search_mail(browser):
    tables = browser.find_all('table')
    mails = []
    for table in tables:
        parent = browser.find_all('table')[0].parent
        id = parent.find_all('a')[1]['href'][1:]
        mail = browser.find("div", {"id": id})
        if not table.find("tr", {"class": "read checked"}):
            row = table.find_all('tr')[0]
            row = row.find_all('td')
            subject = ""
            for i in range(5):
                # print(row[i].text.strip(), end=" ")
                subject += row[i].text.strip()
                if i == 0:
                    subject += " from "
                    # print("from", end=" ")
                if i == 1:
                    subject += " sent "
                    # print("sent", end=" ")
                if i == 2:
                    subject += " on "
                    # print("on", end="")
            # print()
            print(subject)
            print(mail)
            mails.append((subject, mail))

    return mails


def fetch_mail_attachment(browser):
    # Mail Attachments URL
    mail_attachments = browser.find("a", href=re.compile('Attachment'))
    for mail_attachment in mail_attachments:
        attachment_url = base_url[:-1] + "_Attachment/" + mail_attachment
        print(attachment_url)


def fetch_mail_text(browser):
    mail_text = browser.find("div", {"class": "panel_text"}).text
    print(mail_text)


def send_mail(fetched_mails):
    # sender == my email address
    # receiver == recipient's email address
    sender = sender_id
    receiver = receiver_id

    gmail = smtplib.SMTP('smtp.gmail.com', 587)

    gmail.ehlo()

    gmail.starttls()

    gmail.login(sender_id, sender_pwd)

    for mail in fetched_mails:
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = mail[0]
        msg['From'] = sender
        msg['To'] = receiver

        # Create the body of the message (a plain-text and an HTML version).
        # text = "Hi!\nHow are receiver?\nHere is the link receiver wanted:\nhttp://www.python.org"
        html = mail[1]

        # Record the MIME types of both parts - text/plain and text/html.
        # part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        # msg.attach(part1)
        msg.attach(part2)
        # Send the message via local SMTP server.

        gmail.sendmail(sender, receiver, msg.as_string())

    gmail.quit()


if __name__ == "__main__":
    fetched_mails = search_mail(browser)
    if fetched_mails:
        send_mail(fetched_mails)
