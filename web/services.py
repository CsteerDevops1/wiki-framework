import os

import markdown
import base64


def markdown_to_html(text):
    """
    Transforming Markdown text to HTML code
    """
    return markdown.markdown(text, extensions=['codehilite'])


def markdown_to_html_from_file(mdfile):
    """
    Transforming Markdown file to HTML code
    """
    with open(mdfile, 'r', encoding="utf-8") as f:
        text = f.read()
    return markdown_to_html(text)


def bytes_to_str(bstr):
    """convert any content to string representation"""
    return base64.b64encode(bstr).decode('utf-8')

    # отправляем строку сначала bytes_from_str потом bytes_to_str
    # картинки только bytes_to_str


def bytes_from_str(ustr):
    """convert content back to bytes from string representation"""
    return base64.b64decode(ustr.encode('utf-8'))


def get_page(name):
    page = os.path.join('./pages/', name + ".md")
    return markdown_to_html_from_file(page) if os.path.isfile(page) else "Not Found"

def save_topic_into_file(request):
    title = request.form['title']
    tag = request.form['tag']
    file = open("./pages/" + title + ".md", "w")
    file.write("##" + title + "##\n" + tag)
    file.close()

    topics = open("./pages/sidebar.md", "a")
    topics.write("* [" + title + "](/" + title + ")\n")
    topics.close()

def send_image_to_server_by_post(request):
    image_file = open("/usr/src/app/image.jpg", "rb").read()

    val_post = {
        "name": request.form['dbitemName'],
        "description": request.form['dbitemDescription'],
        "tags": [],
        "text": request.form['dbitemText'],
        "creation_date": "2020-02-21",
        "synonyms": [],
        "relations": [],
        "attachments": [{"content_type": "image/jpg", "content_data": bytes_to_str(image_file)}]
    }
    ##localhost:5000
    return request.post("http://172.18.0.3:5000/api/wiki", json=val_post)