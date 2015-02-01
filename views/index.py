# -*- coding: utf-8 -*-
from flask import url_for, render_template
from config import *
from arm.constants import BASE_DURATION
from arm import ArmManager
from tuesday import app


@app.route('/')
def index():
    part_ids = ArmManager.parts.keys()
    context = {
        'STATIC_URL': url_for('static', filename=''),
        'part_ids': part_ids,
        'BASE_DURATION': BASE_DURATION,
    }
    return render_template('index.html', **context)

