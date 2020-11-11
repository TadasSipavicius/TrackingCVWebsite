import requests
from bs4 import BeautifulSoup
import smtplib
import time

# CONSTANTS
URL = 'https://www.cvbankas.lt/?miestas=Kaunas&padalinys%5B0%5D=76'
headers = {"User Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/83.0.4103.61 Safari/537.36'}


# Functions
def take_html_code():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def find_date():
    time_passed = []
    soup2 = take_html_code()
    posted_time = soup2.find_all(class_="txt_list_2")
    for x in posted_time:
        title = x.get_text()
        words = title.split(' ')
        if words[2] == 'd.':
            time_passed.append(int(words[1]) * 86400)
        elif words[2] == 'val.':
            time_passed.append(int(words[1]) * 3600)
        else:
            continue

    return time_passed


def check_status():
    soup = take_html_code()
    title_words = soup.find_all(class_='list_h3')

    time_passed = find_date()

    res = dict(zip(title_words, time_passed))
    for job_name, time_passed_away in res.items():
        Statement = False
        if time_passed_away < 100000:
            title = job_name.get_text()
            words = title.split(' ')
            for job_each_word in words:
                word = job_each_word.upper()
                if word == ("PYTHON" or "JUNIOR" or "JAVASCRIPT" or "REACT"):
                    send_email()
                    Statement = True
                    break
        if Statement:
            break


def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('tasipas@gmail.com', 'leboeczugetircof')

    subject = 'Atsirado darbo pasiulymas'
    body = 'Atsirado darbo pasiulymas! Patikrink svetaine - https://www.cvbankas.lt/?miestas=Kaunas&padalinys%5B0%5D=76'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'tasipas@gmail.com',
        'tasipas@gmail.com',
        msg
    )
    server.quit()


# Main code
while True:
    check_status()
    time.sleep(10)
    print("Checked website")
