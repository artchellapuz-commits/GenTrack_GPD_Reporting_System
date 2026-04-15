#!/bin/bash
pip install -r requirements.txt
gunicorn npc_reporting.wsgi:application --bind 0.0.0.0:$PORT
