#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
import config
import os

app = Flask(__name__)
app.debug = config.DEBUG

if 'ARM_APP_SECRET_KEY' in os.environ:
    app.secret_key = os.environ['ARM_APP_SECRET_KEY']
if not app.secret_key:
    raise Warning("You have to set a 'ARM_APP_SECRET_KEY' in environment variables.")
