# -*- coding: utf-8 -*-
#!/usr/bin/env python
from flask import Flask
from config import *
import os

app = Flask(__name__)
app.debug = DEBUG

if 'ARM_APP_SECRET_KEY' in os.environ:
    app.secret_key = os.environ['ARM_APP_SECRET_KEY']
if not app.secret_key:
    raise Warning("You have to set a 'ARM_APP_SECRET_KEY' in environment variables.")
