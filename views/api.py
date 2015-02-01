# -*- coding: utf-8 -*-
from flask import url_for, jsonify, request
from config import *
from arm import ArmManager
from tuesday import app


@app.route('/arm/status/')
@app.route('/arm/status/<part_id>/', methods=['POST'])
def api(part_id=None):

    def _response_json(context):
        return jsonify(**context)

    def _get_context_data(message=u''):
        """
        get status and make into a dict
        """
        response_data = dict()
        response_data['is_on'] = ArmManager.is_on()
        response_data['message'] = message
        return response_data

    message = u''

    if request.method == 'POST':
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

            if is_acted:
                message = u'ACTED.'

    context = _get_context_data(message)
    return _response_json(context)
