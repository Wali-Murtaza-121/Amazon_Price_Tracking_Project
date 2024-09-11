import smtplib

import requests
import os
from bs4 import BeautifulSoup
from smtplib import SMTP

TARGET_PRICE = 120.10
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
SMTPEMAIL = os.environ["SMTPEMAIL"]
USEREMAIL = os.environ["USEREMAIL"]
ENDPOINT = os.environ["ENDPOINT"]
URL = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

response = requests.get(url=ENDPOINT, headers={"Accept-Language": "en-US,en;q=0.9",
                                               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"})
response = response.text

soup = BeautifulSoup(response, "html.parser")
price_tag = soup.find(name="span", class_="a-offscreen").get_text()
price = float(price_tag.split("$")[1])
product_title = soup.find(name="span", class_="a-size-large product-title-word-break").get_text().strip()
if price < TARGET_PRICE:
    with smtplib.SMTP(SMTPEMAIL, 587) as connection:
        connection.starttls()
        connection.login(user=USERNAME, password=PASSWORD)
        connection.sendmail(from_addr=USERNAME, to_addrs=USEREMAIL,
                            msg=f"Subject: Amazon Price Alert!\n\n{product_title},10 programs is now ${price}\n{URL}".encode(
                                "utf-8"))
