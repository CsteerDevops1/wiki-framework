from collections import namedtuple
from flask import Flask, render_template, redirect, url_for, request
import os.path
import function
import requests
import base64


app = Flask(__name__)


def bytes_to_str(bstr):
    '''convert any content to string representation'''
    return base64.b64encode(bstr).decode('utf-8')

    #отправляем строку сначала bytes_from_str потом bytes_to_str
    #картинки только bytes_to_str
def bytes_from_str(ustr):
    '''convert content back to bytes from string representation'''
    return base64.b64decode(ustr.encode('utf-8'))

def get_page(name):
    page = os.path.join('./pages/', name + ".md")
    if os.path.isfile(page):
        return function.markdown_to_html_from_file(page)
    else:
        return "Not Found"


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        "test.html",
        title="Wiki - Framework",
        sidebar=get_page('sidebar'),
        content="Content",
        footer="All rights reserved"
    )

@app.route('/<name>')
def page(name):
    return render_template(
        "test.html",
        title="Wiki - Framework",
        sidebar=get_page('sidebar'),
        content=get_page(name),
        footer="All rights reserved"
    )


@app.route('/main')
def main():
    return render_template('main.html', sidebar=get_page('sidebar'))


@app.route('/create_new_topic', methods=['POST'])
def create_new_topic():
    title = request.form['title']
    tag = request.form['tag']
    file = open("./pages/" + title + ".md", "w")
    file.write("##" + title + "##\n" + tag)
    file.close()

    topics = open("./pages/sidebar.md", "a")
    topics.write("* [" + title + "](/" + title + ")\n")
    topics.close()

    return redirect(url_for('main'))

# test method to send post request with data to api
@app.route('/senddata')
def testdata():
    image_file = open("/usr/src/app/image.jpg", "rb").read()
    val_post = {
            "name" : "val_post1",
            "description" : "val_post1",
            "tags" : [],
            "text" : "text",
            "creation_date" : "2020-02-21",
            "synonyms" : [],
            "relations" : [],
            "attachments" : [{"content_type" : "image/png", "content_data" : bytes_to_str(image_file)}]
            }
    ##localhost:5000
    resp = requests.post("http://172.18.0.3:5000/api/wiki", json = val_post)

    
    return render_template(
                "test.html",
                title="Wiki - Framework",
                sidebar="Side Bar",
                content=resp.content,
                footer="All rights reserved"
                )    
