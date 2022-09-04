import requests
from bs4 import BeautifulSoup
import json
import os
import re


def getItem(link):
    URL = link
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": link,
    }
    page = requests.get(URL, headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        link = soup.find("meta", {"property": "og:url"}).get("content")
        img_link = soup.find("meta", {"property": "twitter:image"}).get("content")
        desc = soup.find("meta", {"property": "og:description"}).get("content")
        item = soup.find_all("div", {"class": "item-title"})

        for each in item:
            name = each.find("meta", {"itemprop": "name"}).get("content")
            currencey = each.find("meta", {"itemprop": "priceCurrency"}).get("content")
            price = each.find("meta", {"itemprop": "price"}).get("content")
            fullprice = "{} {}".format(currencey, price)

        return {
            "product_name": name,
            "price": fullprice,
            "link": link,
            "img_link": img_link,
            "desc": desc,
        }


def getPayloadEmpty():
    payload = {
        "blocks": [
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": "No available link, please add/check",
                },
            }
        ]
    }

    return payload


def getPayload(itemRes):
    product_name = itemRes["product_name"]
    price = itemRes["price"]
    link = itemRes["link"]
    image = itemRes["img_link"]
    desc = itemRes["desc"]
    try:
        percent = re.findall("[0-9][0-9]%", desc)[0]
    except IndexError:
        percent = re.findall("[0-9]%", desc)[0]

    payload = {
        "blocks": [
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": "*DISCOUNT {}* <{}|{}> \n\n :mag: {}".format(
                        percent, link, product_name, price
                    ),
                },
                "accessory": {
                    "type": "image",
                    "image_url": image,
                    "alt_text": product_name,
                },
            }
        ]
    }

    return payload


def sendToSlack(itemRes, no_data=False):
    if no_data:
        payload = getPayloadEmpty()
    else:
        payload = getPayload(itemRes)

    slack_webhook = os.environ.get("SLACK_URL")
    requests.post(slack_webhook, json=payload)
