# -*- coding: utf-8 -*-
import datetime

from roboarm import DeviceNotFound, Arm as RoboArm
from usb import USBError
from django.conf import settings

from arm.constants import DEVICE_STATUS_KEY, STATUS_ON, STATUS_OFF, FETCH_TIMEOUT
from arm.models.utils.kvs import CacheKvs


class DeviceFetchTimeout(Exception):
    """
    timeout error
    """
    pass


class ArmDevice(object):
    """
    an device obj
    interact with the truly usb device
    """
    status_cache = CacheKvs(DEVICE_STATUS_KEY)

    @classmethod
    def arm(cls):
        """
        使用设备的唯一接口
        """
        if hasattr(settings, 'ARM_DEBUG') and settings.ARM_DEBUG:
            return
        arm = cls.fetch_for_loop()
        return arm

    @classmethod
    def status(cls):
        """
        外部用来判断是否可以使用设备
        只给 PartStatus 和 DeviceStatus 类使用
        """
        cls.fetch()
        if hasattr(settings, 'ARM_DEBUG') and settings.ARM_DEBUG:
            return True
        return bool(int(cls.status_cache.get()))

    @classmethod
    def fetch(cls):
        """
        get arm from usb device
        manage the device status
        从 USB 获取设备的唯一接口，
        保证获取到设备都同时修改状态
        """
        try:
            arm = RoboArm()
            cls.status_cache.set(STATUS_ON)
            return arm
        except (USBError, DeviceNotFound) as e:
            cls.status_cache.set(STATUS_OFF)

    @classmethod
    def fetch_for_loop(cls):
        """
        使用设备发生错误时，重新获取设备
        设定超时 FETCH_TIMEOUT
        超时时 raise DeviceFetchTimeout
        """
        start_at = datetime.datetime.now().second
        while FETCH_TIMEOUT > datetime.datetime.now().second - start_at:
            return cls.fetch()
        raise DeviceFetchTimeout
