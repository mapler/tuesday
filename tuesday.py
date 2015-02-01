# -*- coding: utf-8 -*-
#!/usr/bin/env python
from flask import Flask
from config import *

app = Flask(__name__)
app.debug = DEBUG
