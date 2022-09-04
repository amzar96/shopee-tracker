import requests
import os
import json
from dotenv import load_dotenv
import pandas as pd

load_dotenv()  # read .env

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Token {os.environ.get('BASEROW_TOKEN')}",
}
base_url = "https://api.baserow.io/api/"


def getData():
    res = requests.get(
        url=f"{base_url}database/rows/table/95895/?user_field_names=true",
        headers=headers,
    )

    if res.status_code == 200:
        data = res.json()

        res_data = data["results"]
        df = pd.DataFrame(res_data)
        df = df[df["Active"] == True]
        shopee_url = df["URL"].unique().tolist()

        return shopee_url
    else:
        return []


