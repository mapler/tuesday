# -*- coding: utf-8 -*-
from flask import url_for, render_template
import config
from arm.constants import BASE_DURATION
from arm import ArmManager
from tuesday import app
from user import user_manager
from form import LoginForm


@app.route('/')
def index():
    part_ids = ArmManager.parts.keys()
    login_form = LoginForm()
    user_in_use = user_manager.get_current_user()
    user_ttl = user_manager.get_ttl()
    user_ttl_percent = 100 * user_ttl / config.SESSION_EXPIRES
    context = {
        'STATIC_URL': url_for('static', filename=''),
        'part_ids': part_ids,
        'BASE_DURATION': BASE_DURATION,
        'SESSION_EXPIRES': config.SESSION_EXPIRES,
        'power_on': ArmManager.is_on(),
        'user_in_use': user_in_use,
        'login_form': login_form,
        'user_ttl': user_ttl,
        'user_ttl_percent': user_ttl_percent,
    }
    return render_template('index.html', **context)
