import json
import requests

from config import TG_TOKEN
from apiConfig import *


def check_the_file_size():
    pass


def search_all_by_word(word):
    res = requests.get(ADDRESS, params={})
    result_list = eval(res.content)
    if word == "*":
        return result_list
    found_dict_list = []
    if word == '':
        return []
    for file_dict in result_list:
        if file_dict in found_dict_list:
            continue
        if if_word_in_dict(word, file_dict):
            found_dict_list.append(file_dict)
    return found_dict_list


def delete_by_id(id):
    try:
        res = requests.get(ADDRESS, params={'_id': id})
        result_name = eval(res.content)[0]['name']
        result_type = eval(res.content)[0]["attachments"][0]["content_type"].split('/')[0]
        requests.delete(ADDRESS, params={'_id': id})
        os.remove(f"../../coreService/tests/content/{result_type}s/{result_name}")
        print("Delete successfully")
        return True
    except:
        return False


def if_word_in_dict(word, file_dict):
    for value in file_dict.values():
        for data_str in str(value).split():
            if data_str == word:
                return True
    return False


def send_file_through_api(json_file):
    res = requests.post(ADDRESS, data=json.dumps(json_file),
                        headers={'Content-Type': 'application/json', "accept": "application/json", })
    created_id = json.loads(res.text).get("_id", None)
    code = res.status_code
    print("POST : ", f" Code : {code}" " _id : ", created_id)
    return res.__bool__()


def show_photo_info(response):
    largest_photo = {}
    dct_info = eval(response)
    if "photo" in dct_info:
        largest_photo = dct_info["photo"][-1:]
    elif "photos" in dct_info:
        largest_photo = dct_info["photos"][-1:]
    ans = f"I received photo \n" \
          f"Width: {largest_photo[0]['width']}\n" \
          f"Height: {largest_photo[0]['height']}\n" \
          f"Size: {(largest_photo[0]['file_size'] / 1024):.{2}f} Kb\n"
    if 'caption' in dct_info:
        ans += f"Caption: {dct_info['caption']}"
    return ans


def save_photo(response):
    largest_photo = {}
    dict_info = eval(response)
    if "photo" in dict_info:
        largest_photo = dict_info["photo"][-1:]
    elif "photos" in dict_info:
        largest_photo = dict_info["photos"][-1:]
    file_id = largest_photo[0]["file_id"]
    try:
        return save_file(file_id, dict_info, 'image')
    except Exception as exception:
        print("ERROR: ", exception, ". Can't save the video")
        return False


def show_video_info(response):
    largest_video = {}
    dct_info = eval(response)
    if "video" in dct_info:
        largest_video = dct_info["video"]
    elif "videos" in dct_info:
        largest_video = dct_info["videos"]
    ans = f"I received the video \n" \
          f"Width: {largest_video['width']}\n" \
          f"Height: {largest_video['height']}\n" \
          f"Duration: {largest_video['duration']} seconds\n" \
          f"Size: {(largest_video['file_size'] / 1024):.{2}f} Kb\n"
    return ans


def save_video(response):
    largest_video = {}
    dict_info = eval(response)
    if "video" in dict_info:
        largest_video = dict_info["video"]
    elif "videos" in dict_info:
        largest_video = dict_info["videos"]
    file_id = largest_video["file_id"]
    try:
        return save_file(file_id, dict_info, 'video')
    except Exception as exception:
        print("ERROR: ", exception, ". Can't save the video")
        return False


def show_audio_info(response):
    largest_audio = {}
    dct_info = eval(response)
    if "audio" in dct_info:
        largest_audio = dct_info["audio"]
    elif "audios" in dct_info:
        largest_audio = dct_info["audios"]
    ans = f"I received the audio \n" \
          f"Duration: {largest_audio['duration']} seconds\n" \
          f"Size: {(largest_audio['file_size'] / 1024):.{2}f} Kb\n"
    return ans


def save_audio(response):
    largest_audio = {}
    dict_info = eval(response)
    if "audio" in dict_info:
        largest_audio = dict_info["audio"]
    elif "audios" in dict_info:
        largest_audio = dict_info["audios"]
    file_id = largest_audio["file_id"]
    try:
        return save_file(file_id, dict_info, 'audio')
    except Exception as exception:
        print("ERROR: ", exception, ". Can't save the audio")
        return False


def save_file(file_id, dict_info, type):
    url_img = f"https://api.telegram.org/bot{TG_TOKEN}/getFile?file_id={file_id}"  # use VPN if doesn't working
    answer = requests.get(url_img)
    json_dict = json.loads(answer.content.decode(encoding='UTF-8'))
    file_path = json_dict["result"]["file_path"]
    _name = str(file_path).split("/")[1]
    answer = requests.get(f"https://api.telegram.org/file/bot{TG_TOKEN}/{file_path}")
    EXAMPLE_DOC["name"] = _name
    if 'caption' in dict_info:
        EXAMPLE_DOC["description"] = dict_info["caption"]
    video_bytes = answer.content
    EXAMPLE_DOC["attachments"] = [{"content_type": type + "/mp4", "content_data": bytes_to_str(video_bytes)}]
    if not send_file_through_api(EXAMPLE_DOC):
        return False
    try:
        with open(f"../../coreService/tests/content/{type}s/{_name}", "wb") as out:
            out.write(answer.content)
            print(f"File {_name} is saved")
            return True
    except:
        print("No such file or directory")


def show_document_info(response):
    largest = {}
    dct_info = eval(response)
    if "document" in dct_info:
        largest = dct_info["document"]
    elif "documents" in dct_info:
        largest = dct_info["documents"]
    ans = f"I received the document \n" \
          f"Document name: {largest['file_name']} \n" \
          f"Size: {(largest['file_size'] / 1024):.{2}f} Kb\n"
    return ans


def save_document(response):
    largest = {}
    dct_info = eval(response)
    if "document" in dct_info:
        largest = dct_info["document"]
    elif "documents" in dct_info:
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
    except Exception as exception:
        print("ERROR: ", exception, ". Can't save the document")
