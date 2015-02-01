# -*- coding: utf-8 -*-

# KVS KEY
DEVICE_STATUS_KEY = 'Arm_Device_Status'

# device action duration
BASE_DURATION = 1

# device part id
PART_GRIPS = 1
PART_WRIST = 2
PART_ELBOW = 3
PART_SHOULDER = 4
PART_BASE = 5
PART_LED = 6

PART_TYPE_SWITCH = 1
PART_TYPE_SWING_V = 3
PART_TYPE_SWING_H = 2

PART_NAME_DICT = {
    PART_GRIPS: 'grips',
    PART_WRIST: 'wrist',
    PART_ELBOW: 'elbow',
    PART_SHOULDER: 'shoulder',
    PART_BASE: 'base',
    PART_LED: 'led',
}

PART_TYPE_DICT = {
    PART_GRIPS: PART_TYPE_SWITCH,
    PART_WRIST: PART_TYPE_SWING_V,
    PART_ELBOW: PART_TYPE_SWING_V,
    PART_SHOULDER: PART_TYPE_SWING_V,
    PART_BASE: PART_TYPE_SWING_H,
    PART_LED: PART_TYPE_SWITCH
}


# ArmDevice Status Code
STATUS_OFF = 0
STATUS_ON = 1

# fetch device error timeout
FETCH_TIMEOUT = 3

SLEEP_TIME = 1
