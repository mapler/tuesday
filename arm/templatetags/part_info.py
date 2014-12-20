# -*- coding: utf-8 -*-
from django import template
register = template.Library()
from ..constants import PART_RANGE_DICT, PART_NAME_DICT, \
    PART_TYPE_DICT, PART_TYPE_SWITCH, PART_TYPE_SWING_V, PART_TYPE_SWING_H


@register.filter(name='part_name')
def part_name(part_id):
    return u'{}'.format(PART_NAME_DICT.get(part_id))


@register.filter(name='part_range')
def part_range(part_id):
    return u'{}'.format(PART_RANGE_DICT.get(part_id))

@register.filter(name='type_is_switch')
def type_is_switch(part_id):
    return bool(PART_TYPE_DICT.get(part_id) is PART_TYPE_SWITCH)

@register.filter(name='type_is_swing_v')
def type_is_swing_v(part_id):
    return bool(PART_TYPE_DICT.get(part_id) is PART_TYPE_SWING_V)

@register.filter(name='type_is_swing_h')
def type_is_swing_h(part_id):
    return bool(PART_TYPE_DICT.get(part_id) is PART_TYPE_SWING_H)