import sys
sys.path.append(".")
import os
from requests import get, put, delete, post
import json
from config import *
from pathlib import Path


def check_content(content_type : str):
    """
        content_type : audio/video/image

        loads everything from ./content/{conten_type}s and sends to db, 
        chacks if it recieves same back and delete after
    """
    file_path = (os.path.dirname(__file__) or ".") + "/"
    contents = []
    for fname in Path(f"{file_path}content/{content_type}s").iterdir():
        name, ext = fname.name.split(".")[-2:]
        with open(fname.resolve(), "rb") as cont_file:
            contents.append([cont_file.read(), name, ext])

    for cont in contents:
        data, name, ext = cont
        print(f"Cheking {name}.{ext} : ", end="")
        EXAMPLE_DOC["attachments"] = [{"content_type" : f"{content_type}/{ext}", "content_data" : bytes_to_str(data)}]
        EXAMPLE_DOC["name"] = name
        res = post(ADDRESS, data=json.dumps(EXAMPLE_DOC), 
                    headers={'Content-Type': 'application/json', "accept": "application/json"})
        res = json.loads(res.text)
        print(bytes_from_str(res["attachments"][0]["content_data"]) == data)
        print("Delete status code : ", delete(ADDRESS, params={"_id" : res["_id"]}).status_code, end="\n\n")


print("AUDIOS : \n")
check_content("audio")
print("-" * 20)

print("VIDEOS : \n")
check_content("video")
print("-" * 20)

print("IMAGES : \n")
check_content("image")
print("-" * 20)
