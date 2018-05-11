#!/usr/bin/python3

from requests import get
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import time

dir_name = os.path.abspath(os.path.dirname(__file__))

def main():
    print(time.time(), "\tEmail: " + os.environ["CMC_EMAIL"] + "Pass: " + os.environ["CMC_PASSWORD"])
    fetched_names = fetch_names()
    stored_names = load_stored_names()

    new_names = []
    for x in fetched_names:
        if x not in stored_names:
            new_names.append(x)

    if len(new_names) > 0:
        notify(new_names)

    save_names(fetched_names)


def fetch_names():
    html = get('https://coinmarketcap.com/new', stream=True).content
    soup = BeautifulSoup(html, 'html.parser')
    name_elements = soup.select(".currency-name a")

    names = []
    for name in name_elements:
        names.append(name.getText())

    return names


def load_stored_names():
    file = open(dir_name + "/files/new.txt", "r")
    names = file.read().split("\n")
    file.close()
    return names


def save_names(names):
    file = open(dir_name + "/files/new.txt", "w")
    file.write("\n".join(names))
    file.close()


def notify(names):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.environ["CMC_EMAIL"], os.environ["CMC_PASSWORD"])

    msg = MIMEMultipart()
    msg['From'] = os.environ["CMC_EMAIL"]
    msg['To'] = os.environ["CMC_EMAIL"]
    msg['Subject'] = "New CoinMarketCap Coins!"

    body = "New coins have been added to CoinMarketCap!\n\n" + "\n".join(names)
    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()
    server.sendmail(os.environ["CMC_EMAIL"], os.environ["CMC_EMAIL"], text)
    server.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
