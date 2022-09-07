import requests
import os
import json
from dotenv import load_dotenv
import pandas as pd
import datetime

load_dotenv()  # read .env

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Token {os.environ.get('BASEROW_TOKEN')}",
}
base_url = "https://api.baserow.io/api/"


def getData(table_id, count=False):
    res = requests.get(
        url=f"{base_url}database/rows/table/{table_id}/?user_field_names=true",
        headers=headers,
    )

    if res.status_code == 200:
        data = res.json()
        res_data = data["results"]
        df = pd.DataFrame(res_data)

        if count:
            return int(data["count"])

        return df
    else:
        return []


def pushData(prod_id, discount, price):
    currentts = datetime.datetime.utcnow().isoformat() + "Z"
    json = {
        "product_id": prod_id,
        "created_at": currentts,
        "modified_at": currentts,
        "discount": discount,
        "current_price": price,
    }

    res = requests.post(
        url=f"{base_url}database/rows/table/96385/?user_field_names=true",
        headers=headers,
        json=json,
    )

    print("push", res.status_code)


def deleteData(ids):
    json = {"items": ids}

    res = requests.post(
        url=f"{base_url}database/rows/table/96385/batch-delete/",
        headers=headers,
        json=json,
    )

    print("delete", res.status_code)
