# Reference
# https://www.youtube.com/watch?v=Bg9r_yLk7VY
# https://qiita.com/yasunori/items/265d8db746742bb967c4
# Japanese Version of a Price Tracker
# -*- coding: utf-8 -*-
import requests
import smtplib
import time
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header

# source link
URL = 'https://www.amazon.co.jp/%E3%83%86%E3%82%A3%E3%83%95%E3%82%A1%E3%83%BC%E3%83%AB-%E9%9B%BB%E6%B0%97%E3%82%B1%E3%83%88%E3%83%AB-0-8L-%E3%83%91%E3%83%95%E3%82%A9%E3%83%BC%E3%83%9E-KO1538JP/dp/B07G12ZCHX/ref=zg_bs_kitchen_home_1?_encoding=UTF8&psc=1&refRID=TXATRBJQDTYHYR3J6024'

headers = {"User-Agent" : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

def checkPrice():
    page = requests.get(URL, headers = headers)

    # soup is extracted as all the tags, elements of the html
    soup = BeautifulSoup(page.content, 'html.parser')

    # get the title, price of the product by the id
    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()

    # convert the string to a float num so that could do comparison later
    convertedPrice = float(price[1] + price[3:6])

    # if the new price is smaller than a specific price, send a noticfication email
    if convertedPrice < 3000:
        sendMail(price)

    print(title.strip())
    print(price.strip())
    print(convertedPrice)

def sendMail(price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    # login the email with an app password (e.g. wrevpenygbkpfeyd) for two factor authentication // gmail in this case
    server.login('sender_email', 'app_password')

    cset = 'utf-8'
    subject = 'ティファール 電気ケトル 0.8L　価格'
    msgStr = f'ティファール電気ケトル0.8Lの価格を変更しました。 \n\n価格：{price}\n\nアマゾンのリンク: https://www.amazon.co.jp/%E3%83%86%E3%82%A3%E3%83%95%E3%82%A1%E3%83%BC%E3%83%AB-%E9%9B%BB%E6%B0%97%E3%82%B1%E3%83%88%E3%83%AB-0-8L-%E3%83%91%E3%83%95%E3%82%A9%E3%83%BC%E3%83%9E-KO1538JP/dp/B07G12ZCHX/ref=zg_bs_kitchen_home_1?_encoding=UTF8&psc=1&refRID=TXATRBJQDTYHYR3J6024'
    msg = MIMEText(msgStr, 'plain', cset)
    msg['Subject'] = Header(subject, cset)
    server.sendmail(
        'sender',
        ['receiver1','receiver2'],
        msg.as_string()
    )
    print('Email sent')

    server.quit()

while True:
    # check the price every hour
    checkPrice()
    time.sleep(3600)
