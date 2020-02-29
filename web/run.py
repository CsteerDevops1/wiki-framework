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
                title="Title",
                sidebar="Side Bar",
                content="Content",
                footer="Footer"
                )


@app.route('/<name>')
def page(name):
    return render_template(
                "test.html",
                title="Title",
                sidebar="Side Bar",
                content=get_page(name),
                footer="Footer"
                )
