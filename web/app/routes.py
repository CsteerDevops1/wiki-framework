# -*- coding: utf-8 -*-
from app import app
from flask import render_template
from app.config_provider import ConfigProvider
from app import function
import os.path


config = ConfigProvider()


def get_page(name):
    page = os.path.join(config.pages_folder, name + ".md")
    if os.path.isfile(page):
        return function.markdown_to_html_from_file(page)
    else:
        return config.not_found_text


@app.route('/')
@app.route('/index')
def index():
    return render_template(
            "test.html",
            title=config.main_title,
            sidebar=get_page(config.side_bar),
            content=get_page(config.start_page),
            footer="the footer"
    )


@app.route('/<name>')
def page(name):
    return render_template(
            "test.html",
            title=config.main_title,
            sidebar=get_page(config.side_bar),
            content=get_page(name),
            footer="the footer"
    )

