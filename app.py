from time import sleep
import function
import os
from dotenv import load_dotenv
import baserow as br

load_dotenv() # read .env

# itemToCheck = [
#     "https://shopee.com.my/setel.os/3555941670",
#     "https://shopee.com.my/boschmy/100199746",
#     "https://shopee.com.my/drcardin.os/8254227005",
#     "https://shopee.com.my/switch_os/4752491426",
#     "https://shopee.com.my/switch_os/7152493367"
# ]

itemToCheck = br.getData()

print(itemToCheck)

if len(itemToCheck) == 0:
    function.sendToSlack(None, no_data=True)

for each in itemToCheck:
    each = each.strip()
    item = function.getItem(each)

    if "% off" in item["desc"]:
        function.sendToSlack(item)
    sleep(6)