import json
import requests

from telegramBots.initBot.config import TG_TOKEN


def show_photo_info(response):
    largest = {}
    dct_info = eval(response)
    if "photo" in dct_info:
        largest = dct_info["photo"][-1:]
    else:
        if "photos" in dct_info:
            largest = dct_info["photos"][-1:]
    file_id = largest[0]["file_id"]
    ans = f"I received photo \n" \
          f"Width: {largest[0]['width']}\n" \
          f"Height: {largest[0]['height']}\n" \
          f"Size: {(largest[0]['file_size'] / 1024):.{2}f} Kb\n"
    return ans


def save_pthoto(response):
    largest = {}
    dct_info = eval(response)
    if "photo" in dct_info:
        largest = dct_info["photo"][-1:]
    else:
        if "photos" in dct_info:
            largest = dct_info["photos"][-1:]
    file_id = largest[0]["file_id"]
    try:
        url_img = f"https://api.telegram.org/bot{TG_TOKEN}/getFile?file_id={file_id}"  # use VPN if doesn't working
        answ = requests.get(url_img)
        dict = json.loads((answ.content).decode(encoding='UTF-8'))
        file_path = dict["result"]["file_path"]
        _name = str(file_path).split("/")[1]
        answ = requests.get(f"https://api.telegram.org/file/bot{TG_TOKEN}/{file_path}")
        with open(f"photos/{_name}", "wb") as out:
            out.write(answ.content)
        print(f"File {_name} is saved")
    except:
        print("ERROR: Network isn't working, use VPN to resolve problem")

