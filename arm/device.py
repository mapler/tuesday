# -*- coding: utf-8 -*-
import datetime

from roboarm import DeviceNotFound, Arm as RoboArm
from usb import USBError

import config

from constants import DEVICE_STATUS_KEY, STATUS_ON, STATUS_OFF, FETCH_TIMEOUT
from utils.kvs import Kvs


class DeviceFetchTimeout(Exception):
    """
    timeout error
    """
    pass


class ArmDevice(object):
    """
    an device obj
    interact with the usb device
    """
    status = Kvs(DEVICE_STATUS_KEY)

    @classmethod
    def arm(cls):
        if config.DEVICE_DEBUG:
            return
        arm = cls.fetch_for_loop()
        return arm

    @classmethod
    def get_status(cls):
        cls.fetch()
        if config.DEVICE_DEBUG:
            return True
        return int(cls.status.get())

    @classmethod
    def is_on(cls):
        return bool(cls.get_status())

    @classmethod
    def fetch(cls):
        """
        get arm from usb device
        set arm on/off status
        """
        try:
            arm = RoboArm()
            cls.status.set(STATUS_ON)
            return arm
        except (USBError, DeviceNotFound) as e:
            cls.status.set(STATUS_OFF)

    @classmethod
    def fetch_for_loop(cls):
        """
        refetch the device when error
        raise DeviceFetchTimeout when fetch timeout
        """
        start_at = datetime.datetime.now().second
        while FETCH_TIMEOUT > datetime.datetime.now().second - start_at:
            return cls.fetch()
        raise DeviceFetchTimeout
