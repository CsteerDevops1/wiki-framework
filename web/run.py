from collections import namedtuple

from flask import Flask, render_template, redirect, url_for, request
import os.path
import function

app = Flask(__name__)


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
