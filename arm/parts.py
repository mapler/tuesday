# -*- coding: utf-8 -*-
import config as settings

from constants import (
    PART_NAME_DICT,
    PART_BASE,
    PART_ELBOW,
    PART_GRIPS,
    PART_LED,
    PART_SHOULDER,
    PART_WRIST
)
from device import ArmDevice, DeviceFetchTimeout, USBError


class ArmPartBase(object):

    PART_ID = None

    def __init__(self):
        self.part_name = PART_NAME_DICT.get(self.PART_ID)

    @property
    def arm(self):
        return ArmDevice.arm()

    @property
    def can_action(self):
        return ArmDevice.is_on()

    def action(self, duration):
        is_acted = False
        if self.can_action:
            if settings.DEVICE_DEBUG:
                is_acted = True
            else:
                try:
                    is_acted = self._action(duration)
                except USBError:
                    try:
                        ArmDevice.fetch_for_loop()
                        is_acted = self._action(duration)
                    except DeviceFetchTimeout:
                        self.stop()
        return is_acted

    def stop(self):
        if settings.DEVICE_DEBUG:
            return True
        if self.arm:
            is_stop = self._stop()
        else:
            is_stop = None
        return is_stop

    def _action(self, duration):
        if duration > 0:
            self._increase(duration)
            return True
        elif duration < 0:
            self._decrease(-duration)
            return True
        else:
            return False

    def _increase(self, duration):
        pass

    def _decrease(self, duration):
        pass

    def _stop(self):
        pass


class ArmGrips(ArmPartBase):

    PART_ID = PART_GRIPS

    def _increase(self, duration):
        return self.arm.grips.open(duration)
    
    def _decrease(self, duration):
        return self.arm.grips.close(duration)

    def _stop(self):
        return self.arm.grips.stop()
    
    
class ArmWrist(ArmPartBase):

    PART_ID = PART_WRIST

    def _increase(self, duration):
        return self.arm.wrist.up(duration)
    
    def _decrease(self, duration):
        return self.arm.wrist.down(duration)

    def _stop(self):
        return self.arm.wrist.stop()


class ArmElbow(ArmPartBase):

    PART_ID = PART_ELBOW

    def _increase(self, duration):
        return self.arm.elbow.up(duration)
    
    def _decrease(self, duration):
        return self.arm.elbow.down(duration)

    def _stop(self):
        return self.arm.elbow.stop()
    
    
class ArmShoulder(ArmPartBase):

    PART_ID = PART_SHOULDER

    def _increase(self, duration):
        return self.arm.shoulder.up(duration)
    
    def _decrease(self, duration):
        return self.arm.shoulder.down(duration)

    def _stop(self):
        return self.arm.shoulder.stop()


class ArmBase(ArmPartBase):

    PART_ID = PART_BASE

    def _increase(self, duration):
        return self.arm.base.rotate_clock(duration)
    
    def _decrease(self, duration):
        return self.arm.base.rotate_counter(duration)

    def _stop(self):
        return self.arm.base.stop()


class ArmLed(ArmPartBase):

    PART_ID = PART_LED

    def _increase(self, duration):
        return self.arm.led.on()

    def _decrease(self, duration):
        return self.arm.led.off()

    def _stop(self):
        return self.arm.led.stop()
