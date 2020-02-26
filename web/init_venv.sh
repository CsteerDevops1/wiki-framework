#! /bin/bash
python3.7 -m venv venv && \
source venv/bin/activate && \
pip install flask markdown && \
export FLASK_APP=wiki.py
