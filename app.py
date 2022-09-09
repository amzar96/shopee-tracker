from time import sleep
import function
import os
from dotenv import load_dotenv
import baserow as br
import re
import pandas as pd

load_dotenv()  # read .env

df_shopee = br.getData(95895)
df_shopee_count = br.getData(95895, count=True)
df_shopee_history = br.getData(96385)

df_shopee = df_shopee[df_shopee["Active"] == True]

delete_ids = []

for index, row in df_shopee.iterrows():
    URL = row["URL"]
    product_id = row["product_id"]
    active = row["Active"]

    df_history = df_shopee_history[df_shopee_history["product_id"] == product_id]

    shopee_product_link = URL.strip()
    shopee_product = function.getItem(shopee_product_link)

    if "% off" in shopee_product["desc"]:
        shopee_now_price = round(float(shopee_product["price"].split(" ")[1]), 2)

        try:
            shopee_now_percent = re.findall("[0-9][0-9]%", shopee_product["desc"])[0]
        except IndexError:
            shopee_now_percent = re.findall("[0-9]%", shopee_product["desc"])[0]

        shopee_now_percent = int(shopee_now_percent.split("%")[0])

        if not df_history.empty:
            min_discount, min_price = function.getMinMax(df_history)

            # delete row
            earliest_entry = function.getEarliestRecord(df_history)
            for x in earliest_entry:
                delete_ids.append(x)

        else:
            min_discount = 0
            min_price = 0.0

        br.pushData(product_id, shopee_now_percent, shopee_now_price)

        if (shopee_now_percent > int(min_discount)) or (
            float(shopee_now_price) < float(min_price)
        ):
            function.sendToSlack(shopee_product)


if (df_shopee_count > 2500) and (len(delete_ids) > 0):
    br.deleteData(delete_ids)
