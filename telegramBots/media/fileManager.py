import json
import requests

from telegramBots.initBot.config import TG_TOKEN
from telegramBots.media.config import *


def check_the_file_size():
    pass


# def search_file(description):
#     res = requests.get(ADDRESS, params={"description": description})
#     my_dict = eval((res.content))
#     attachments = my_dict[0]["attachments"][0]["content_data"]
#     content_data = bytes_from_str(attachments)
#     id = my_dict[0]["_id"]
#     # with open(f"photos/{id}", "wb") as file:
#     #     file.write(content_data)
#
#     return id


def send_file_through_api(json_file):
    res = requests.post(ADDRESS, data=json.dumps(json_file),
                        headers={'Content-Type': 'application/json', "accept": "application/json", })
    created_id = json.loads(res.text).get("_id", None)
    code = res.status_code
    print("POST : ", f" Code : {code}" " _id : ", created_id)


def show_photo_info(response):
    largest = {}
    dct_info = eval(response)
    print("Photo info ", dct_info)
    if "photo" in dct_info:
        largest = dct_info["photo"][-1:]
    else:
        if "photos" in dct_info:
            largest = dct_info["photos"][-1:]
    file_id = largest[0]["file_id"]
    ans = f"I received photo \n" \
          f"Width: {largest[0]['width']}\n" \
          f"Height: {largest[0]['height']}\n" \
          f"Size: {(largest[0]['file_size'] / 1024):.{2}f} Kb\n" \
          f"Caption: {dct_info['caption']}"
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
        EXAMPLE_DOC["name"] = _name
        EXAMPLE_DOC["description"] = dct_info["caption"]
        image_bytes = answ.content
        EXAMPLE_DOC["attachments"] = [{"content_type": "image/jpg", "content_data": bytes_to_str(image_bytes)}]
        # save photo in mongodb through API
        send_file_through_api(EXAMPLE_DOC)
    # with open(f"photos/{_name}", "wb") as out:
    #     out.write(answ.content)
    # print(f"File {_name} is saved")
    except:
        print("ERROR: Can not connect to the server, use a VPN to resolve problem. Can't save the photo")


def show_video_info(response):
    largest = {}
    dct_info = eval(response)
    # print(f"show video info\n {dct_info}")
    if "video" in dct_info:
        largest = dct_info["video"]
    else:
        if "videos" in dct_info:
            largest = dct_info["videos"]
    file_id = largest["file_id"]
    ans = f"I received the video \n" \
          f"Width: {largest['width']}\n" \
          f"Height: {largest['height']}\n" \
          f"Duration: {largest['duration']} seconds\n" \
          f"Size: {(largest['file_size'] / 1024):.{2}f} Kb\n"
    return ans


def save_video(response):
    largest = {}
    dct_info = eval(response)
    # print(f"show video info\n {dct_info}")
    if "video" in dct_info:
        largest = dct_info["video"]
    else:
        if "videos" in dct_info:
            largest = dct_info["videos"]
    file_id = largest["file_id"]
    try:
        url_img = f"https://api.telegram.org/bot{TG_TOKEN}/getFile?file_id={file_id}"  # use VPN if doesn't working
        answ = requests.get(url_img)
        dict = json.loads((answ.content).decode(encoding='UTF-8'))
        file_path = dict["result"]["file_path"]
        _name = str(file_path).split("/")[1]
        answ = requests.get(f"https://api.telegram.org/file/bot{TG_TOKEN}/{file_path}")
        EXAMPLE_DOC["name"] = _name
        video_bytes = answ.content
        EXAMPLE_DOC["attachments"] = [{"content_type": "video/mp4", "content_data": bytes_to_str(video_bytes)}]
        send_file_through_api(EXAMPLE_DOC)
        # with open(f"videos/{_name}", "wb") as out:
        #     out.write(answ.content)
        # print(f"File {_name} is saved")
    except:
        print("ERROR: Can not connect to the server, use a VPN to resolve problem. Can't save the video")


def show_audio_info(response):
    largest = {}
    dct_info = eval(response)
    # print(f"show audio info\n {dct_info}")
    if "audio" in dct_info:
        largest = dct_info["audio"]
    else:
        if "audios" in dct_info:
            largest = dct_info["audios"]
    file_id = largest["file_id"]
    ans = f"I received the audio \n" \
          f"Duration: {largest['duration']} seconds\n" \
          f"Size: {(largest['file_size'] / 1024):.{2}f} Kb\n"
    return ans


def save_audio(response):
    largest = {}
    dct_info = eval(response)
    if "audio" in dct_info:
        largest = dct_info["audio"]
    else:
        if "audios" in dct_info:
            largest = dct_info["audios"]
    file_id = largest["file_id"]
    try:
        url_img = f"https://api.telegram.org/bot{TG_TOKEN}/getFile?file_id={file_id}"  # use VPN if doesn't working
        answ = requests.get(url_img)
        dict = json.loads((answ.content).decode(encoding='UTF-8'))
        file_path = dict["result"]["file_path"]
        _name = str(file_path).split("/")[1]
        answ = requests.get(f"https://api.telegram.org/file/bot{TG_TOKEN}/{file_path}")
        EXAMPLE_DOC["name"] = _name
        audio_bytes = answ.content
        EXAMPLE_DOC["attachments"] = [{"content_type": "audio/mp3", "content_data": bytes_to_str(audio_bytes)}]
        send_file_through_api(EXAMPLE_DOC)
    except:
        print("ERROR: Can not connect to the server, use a VPN to resolve problem. Can't save the document")


def show_document_info(response):
    largest = {}
    dct_info = eval(response)
    if "document" in dct_info:
        largest = dct_info["document"]
    else:
        if "documents" in dct_info:
            largest = dct_info["documents"]
    file_id = largest["file_id"]
    ans = f"I received the document \n" \
          f"Document name: {largest['file_name']} \n" \
          f"Size: {(largest['file_size'] / 1024):.{2}f} Kb\n"
    return ans


def save_document(response):
    largest = {}
    dct_info = eval(response)
    if "document" in dct_info:
        largest = dct_info["document"]
    else:
        if "documents" in dct_info:
            largest = dct_info["documents"]
    file_id = largest["file_id"]
    try:
        url_img = f"https://api.telegram.org/bot{TG_TOKEN}/getFile?file_id={file_id}"  # use VPN if doesn't working
        answ = requests.get(url_img)
        dict = json.loads((answ.content).decode(encoding='UTF-8'))
        file_path = dict["result"]["file_path"]
        _name = str(file_path).split("/")[1]
        answ = requests.get(f"https://api.telegram.org/file/bot{TG_TOKEN}/{file_path}")
        # EXAMPLE_DOC["name"] = _name
        # audio_bytes = answ.content
        # EXAMPLE_DOC["attachments"] = [{"content_type": "doc/doc", "content_data": bytes_to_str(audio_bytes)}]
        # send_file_through_api(EXAMPLE_DOC)
    except:
        print("ERROR: Can not connect to the server, use a VPN to resolve problem. Can't save the document")
