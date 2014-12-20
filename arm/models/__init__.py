# -*- coding: utf-8 -*-

from parts import (
    ArmGrips,
    ArmWrist,
    ArmElbow,
    ArmShoulder,
    ArmBase,
    ArmLed,
)
from ..constants import (
    PART_BASE,
    PART_ELBOW,
    PART_GRIPS,
    PART_LED,
    PART_SHOULDER,
    PART_WRIST
)
from status import DeviceStatus
from .utils.kvs import CacheKvs


class Locker(object):
    """
    临时用 locker
    TODO, change to MQ
    """

    LOCKER_KEY = 'locker'
    locker = CacheKvs(LOCKER_KEY)

    @classmethod
    def lock(cls):
        """
        lock expires: 5秒
        """
        cls.locker.set('locked', expires=5)

    @classmethod
    def unlock(cls):
        cls.locker.delete()

    @classmethod
    def is_lock(cls):
        return cls.locker.get() == 'locked'

    @classmethod
    def on_lock(cls, func):
        def wrapper(*args, **kwargs):
            if cls.is_lock():
                return
            cls.lock()
            ret = func(*args, **kwargs)
            cls.unlock()
            return ret
        return wrapper


class ArmManager(object):
    """
    View 与 Model 之间的接口
    """
    grips = ArmGrips()
    wrist = ArmWrist()
    elbow = ArmElbow()
    shoulder = ArmShoulder()
    base = ArmBase()
    led = ArmLed()

    parts = {
        PART_GRIPS: grips,
        PART_WRIST: wrist,
        PART_ELBOW: elbow,
        PART_SHOULDER: shoulder,
        PART_BASE: base,
        PART_LED: led,
    }

    @classmethod
    def get_part(cls, part_id):
        return cls.parts.get(part_id)

    @classmethod
    def is_on(cls):
        return DeviceStatus.is_on()

    @classmethod
    @Locker.on_lock
    def _action(cls, part_id, duration):
        is_acted = False
        if part_id in cls.parts.keys() and duration:
            try:
                is_acted = ArmManager.get_part(part_id).action(duration)
            except:
                print 'except'
                pass

        return is_acted

    @classmethod
    def decr(cls, part_id, duration, *args):
        duration = -duration
        return cls._action(part_id, duration)

    @classmethod
    def incr(cls, part_id, duration, *args):
        return cls._action(part_id, duration)

    @classmethod
    def stop(cls, part_id, *args):
        return cls.get_part(part_id).stop()
