import smtplib
from os import getenv
from dotenv import load_dotenv
from threading import Thread

load_dotenv()

SENDER_EMAIL = getenv("SENDER_EMAIL")
SENDER_APP_PASSWORD = getenv("SENDER_APP_PASSWORD")

email_mapping = {}
email_mapping['ayush@giet.edu'] = 'ayushmantripathy2004@gmail.com'
email_mapping['tripathy@giet.edu'] = '23cse417.ayushmantripathy@giet.edu'
email_mapping['vishnu@giet.ed'] = "23cse417.ayushmantripathy@giet.edu"

if SENDER_EMAIL == None or SENDER_APP_PASSWORD == None:
    print("missing credentials")
    exit(1)

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(SENDER_EMAIL, SENDER_APP_PASSWORD)

updates = []

def send_mail(mail, message):
    if mail in email_mapping:
        mail = email_mapping[mail]
    s.sendmail(SENDER_EMAIL, mail, message)
    s.quit()

def send_otp(mail, otp):
    message = f"Subject: Requested Otp\nRequested otp is {otp}\n"
    send_mail(mail, message)

def send_update_mail():
    mail, message = updates.pop()
    send_mail(mail, message)

def add_faculty_update(mail, title):
    message = f"Subject: New Issue Raised\nnew issue titled '{title}' has been addressed to you.\n"
    updates.append((mail, message))
    Thread(target=send_update_mail).start()

def add_student_update(mail, title, status):
    message = f"Subject: Update regrading raised issue\nYour issue titled '{title}' has been {status}.\n"
    updates.append((mail, message))
    Thread(target=send_update_mail).start()
