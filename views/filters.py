# -*- coding: utf-8 -*-
from tuesday import app
from arm.constants import PART_NAME_DICT, PART_TYPE_DICT, \
    PART_TYPE_SWITCH, PART_TYPE_SWING_V, PART_TYPE_SWING_H


@app.template_filter(name='part_name')
def part_name(part_id):
    return u'{}'.format(PART_NAME_DICT.get(part_id))


@app.template_filter(name='type_is_switch')
def type_is_switch(part_id):
    return bool(PART_TYPE_DICT.get(part_id) is PART_TYPE_SWITCH)


@app.template_filter(name='type_is_swing_v')
def type_is_swing_v(part_id):
    return bool(PART_TYPE_DICT.get(part_id) is PART_TYPE_SWING_V)


@app.template_filter(name='type_is_swing_h')
def type_is_swing_h(part_id):
    return bool(PART_TYPE_DICT.get(part_id) is PART_TYPE_SWING_H)

