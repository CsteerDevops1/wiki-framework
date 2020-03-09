import requests
import json
import time

API_KEY = 'trnsl.1.1.20200309T121046Z.10fd25429d4264e1.1b1d8883b0e564975a110cb11b558d5d1e1aa68b'
API_ADDRESS = 'http://192.168.0.111:5000/api/wiki'

def translate(word, lang="en-ru"):
    """Return a translation the word given as argument"""
    payload = {"key":API_KEY, "text":word, "lang":lang}
    response = requests.get("https://translate.yandex.net/api/v1.5/tr.json/translate", params = payload)
    if response.ok:
        return json.loads(response.text)['text'].pop(0)
    else:
        return None


def get():
    response = requests.get(API_ADDRESS, params={'russian_name':''}, headers={'X-Fields':'_id, name, russian_name'})
    return json.loads(response.text)


def translate_json_data(json_data):
    """json data is a list of dicts"""
    for obj in json_data:
        if not obj.get('russian_name'):
            obj['russian_name'] = translate(obj['name'], lang="en-ru")
            time.sleep(1) #to not get ban
    return json_data


def put(json_data):
    for obj in json_data:
        res = requests.put(API_ADDRESS, params={"_id" : obj.get('_id')}, data=json.dumps({'russian_name':obj.get('russian_name')}),
            headers={'Content-Type': 'application/json', "accept": "application/json"})


def __format_print(json_data):
    """Used for testing"""
    print("len = %d:" % len(json_data) )
    for i in json_data:
        print("id: %s;\tname: %s;\trus: %s" % (i['_id'], i['name'], i.get('russian_name')))


if __name__=="__main__":
    while(True):
        try:
            data = get()
            if data:
                data = translate_json_data(data)
                put(data)
                print("Translated %d words" % len(data))
        except Exception:
            print("Can't connect to DB")
        time.sleep(10)
