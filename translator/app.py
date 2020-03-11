import requests
import json
import time
from itertools import cycle
import os


API_KEY = os.getenv('API_KEY')
API_ADDRESS = os.getenv('API_ADDRESS')


def translate(word, lang="en-ru"):
    """Return a translation the word given as argument"""
    payload = {"key":API_KEY, "text":word, "lang":lang}
    response = requests.get("https://translate.yandex.net/api/v1.5/tr.json/translate", params = payload)
    if response.ok:
        return json.loads(response.text)['text'].pop(0)
    else:
        return None


def get(field_name):
    response = requests.get(API_ADDRESS, params={'russian_%s' % field_name:''},
            headers={'X-Fields':'_id, {0}, russian_{0}'.format(field_name)})
    return json.loads(response.text)


def translate_json_data(json_data, field_name):
    """json data is a list of dicts"""
    for obj in json_data:
        if not obj.get('russian_%s' % field_name):
            obj['russian_%s' % field_name] = translate(obj[field_name], lang="en-ru")
            time.sleep(1) #to not get ban
    return json_data


def put(json_data, field_name):
    for obj in json_data:
        res = requests.put(API_ADDRESS, params={"_id" : obj.get('_id')},
                data=json.dumps({'russian_%s' % field_name:obj.get('russian_%s' % field_name)}),
                    headers={'Content-Type': 'application/json', "accept": "application/json"})


def __format_print(json_data, field_name):
    """Used for testing"""
    print("len = %d:" % len(json_data) )
    for i in json_data:
        print("id: %s;\tname: %s;\trus: %s" % (i['_id'], i[field_name], i.get('russian_%s' % field_name)))


if __name__=="__main__":
    field_name_iterator = cycle(("name", "description"))
    while(True):
        try:
            field_name = next(field_name_iterator)
            data = get(field_name)
            if data:
                data = translate_json_data(data, field_name)
                put(data, field_name)
                print("Translated %d %s fields" % (len(data), field_name))
        except Exception:
            print("Can't connect to DB")
        time.sleep(10)
