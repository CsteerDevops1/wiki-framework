import os
import markdown


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
