#!/usr/bin python3

from requests import get
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


def main():
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
    file = open("./files/new.txt", "r")
    return file.read().split("\n")


def save_names(names):
    file = open("./files/new.txt", "w")
    file.write("\n".join(names))


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
    main()
