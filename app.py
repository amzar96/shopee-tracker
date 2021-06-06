from time import sleep
import function
import os
from dotenv import load_dotenv

load_dotenv() # read .env

itemToCheck = [
    "https://shopee.com.my/setel.os/3555941670",
    "https://shopee.com.my/boschmy/100199746",
    "https://shopee.com.my/drcardin.os/8254227005",
]

for each in itemToCheck:
    item = function.getItem(each)

    if "% off" in item["desc"]:
        function.sendToSlack(item)
    sleep(6)