# -*- coding: utf-8 -*-

from parts import (
    ArmGrips,
    ArmWrist,
    ArmElbow,
    ArmShoulder,
    ArmBase,
    ArmLed,
)
from constants import (
    PART_BASE,
    PART_ELBOW,
    PART_GRIPS,
    PART_LED,
    PART_SHOULDER,
    PART_WRIST
)
from device import ArmDevice
from utils.locker import Locker


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

    locker = Locker()

    @classmethod
    def get_part(cls, part_id):
        return cls.parts.get(part_id)

    @classmethod
    def is_on(cls):
        return ArmDevice.is_on()

    @classmethod
    @locker.on_lock
    def _action(cls, part_id, duration):
        is_acted = False
        if part_id in cls.parts.keys() and duration:
            try:
                is_acted = ArmManager.get_part(part_id).action(duration)
            except Exception as e:
                print e
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
        for part in self.parts.values():
           part.stop()
