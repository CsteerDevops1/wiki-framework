from flask import Flask, render_template, redirect, url_for, request
import requests
import services
import json

app = Flask(__name__)


BASENAME = "http://flask:5000/api/wiki"

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        "main.html",
        sidebar=services.get_page('sidebar'),
        content="Content",
        footer="All rights reserved"
    )


@app.route('/<name>')
def page(name):
    return render_template(
        "test.html",
        title="Wiki - Framework",
        sidebar=services.get_page('sidebar'),
        content=services.get_page(name),
        footer="All rights reserved"
    )


@app.route('/main')
def main():
    return render_template('main.html', sidebar=services.get_page('sidebar'))


@app.route('/create_new_topic', methods=['POST'])
def create_new_topic():
    services.save_topic_into_file(request)
    return redirect(url_for('main'))


@app.route('/postrequest', methods=['POST'])
def postrequest():
    services.send_image_to_server_by_post(request)
    return render_template("postrequest.html", sidebar='Side Bar')


@app.route('/getrequest')
def getrequest():
    resp = requests.get(BASENAME)
    json_data = json.loads(resp.text)
    return render_template(
        "getrequest.html",
        title="Wiki - Framework",
        sidebar="Side Bar",
        json=json_data,
        footer="All rights reserved"
    )


if __name__ == "__main__":
    val_post = {
        "name": "val_post1",
        "description": "val_post1",
        "tags": [],
        "text": "text",
        "creation_date": "2020-02-21",
        "synonyms": [],
        "relations": [],
        "attachments": [{"content_type": "image/jpg", "content_data": "bytes_to_str(image_file)"}]
    }
    json = json.loads(val_post)
    print(json["attachments"][0]["content_data"])
