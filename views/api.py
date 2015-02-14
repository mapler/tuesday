# -*- coding: utf-8 -*-
from flask import url_for, jsonify, request, flash
from flask.ext.login import login_required
from config import *
from arm import ArmManager
from tuesday import app
from views.login import login_manager
from user import user_manager


def _response_json(context):
    return jsonify(**context)


def _get_context_data():
    """
    get status and make into a dict
    """
    user_ttl = user_manager.get_ttl()

    response_data = {
        'power_on': ArmManager.is_on(),
        'user_ttl': user_ttl,
        'user_in_use': '',
        }
    if user_ttl:
        user_in_use = user_manager.get_current_user()
        user_in_use_name = user_in_use.name
        response_data.update({'user_in_use': user_in_use_name})
    return response_data


@app.route('/api/arm/')
def get_status(part_id=None):
    context = _get_context_data()
    return _response_json(context)


@app.route('/api/arm/<part_id>/', methods=['POST'])
@login_required
def post_action(part_id=None):

    duration = request.form.get('duration', 0)
    part_ids = ArmManager.parts.keys()

    if part_id and duration:
        part_id = int(part_id)
        duration = int(duration)

        action = request.form.get('action')
        try:
            is_acted = getattr(ArmManager, action)(part_id, duration)
        except AttributeError:
            is_acted = False

    context = _get_context_data()
    return _response_json(context)
