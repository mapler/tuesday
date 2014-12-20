# -*- coding: utf-8 -*-
from django.conf import settings

from arm.constants import PART_NAME_DICT, PART_RANGE_DICT
from arm.constants import (
    PART_BASE,
    PART_ELBOW,
    PART_GRIPS,
    PART_LED,
    PART_SHOULDER,
    PART_WRIST
)
from device import ArmDevice, DeviceFetchTimeout
from arm.models.status import StatusMixin


class ArmPartBase(StatusMixin):

    PART_ID = None
    MIN = 0

    def __init__(self):
        self.part_name = PART_NAME_DICT.get(self.PART_ID)

    @property
    def arm(self):
        return ArmDevice.arm()

    def action(self, duration):
        is_acted = False
        if self.can_action(duration):
            if hasattr(settings, 'ARM_DEBUG') and settings.ARM_DEBUG:
                is_acted = True
            else:
                try:
                    is_acted = self._action(duration)
                except:
                    # 尝试一次重新获取设备
                    try:
                        ArmDevice.fetch_for_loop()
                        is_acted = self._action(duration)
                    except DeviceFetchTimeout:
                        # error发生切再次获取设备超时时，给部件发送停止信号
                        self.stop()
                        # todo write log
            if is_acted:
                self.status.incr(duration)
                # todo write log
        return is_acted

    def stop(self):
        if hasattr(settings, 'ARM_DEBUG') and settings.ARM_DEBUG:
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
    MAX = PART_RANGE_DICT.get(PART_ID, 0)

    def _increase(self, duration):
        return self.arm.grips.open(duration)
    
    def _decrease(self, duration):
        return self.arm.grips.close(duration)

    def _stop(self):
        return self.arm.grips.stop()

    def _block(self, duration):
        pass
    
    
class ArmWrist(ArmPartBase):

    PART_ID = PART_WRIST
    MAX = PART_RANGE_DICT.get(PART_ID, 0)

    def _increase(self, duration):
        return self.arm.wrist.up(duration)
    
    def _decrease(self, duration):
        return self.arm.wrist.down(duration)

    def _stop(self):
        return self.arm.wrist.stop()

    def _block(self, duration):
        pass


class ArmElbow(ArmPartBase):

    PART_ID = PART_ELBOW
    MAX = PART_RANGE_DICT.get(PART_ID, 0)

    def _increase(self, duration):
        return self.arm.elbow.up(duration)
    
    def _decrease(self, duration):
        return self.arm.elbow.down(duration)

    def _stop(self):
        return self.arm.elbow.stop()

    def _block(self, duration):
        pass    
    
    
class ArmShoulder(ArmPartBase):

    PART_ID = PART_SHOULDER
    MAX = PART_RANGE_DICT.get(PART_ID, 0)

    def _increase(self, duration):
        return self.arm.shoulder.up(duration)
    
    def _decrease(self, duration):
        return self.arm.shoulder.down(duration)

    def _stop(self):
        return self.arm.shoulder.stop()

    def _block(self, duration):
        pass
    

class ArmBase(ArmPartBase):

    PART_ID = PART_BASE
    MAX = PART_RANGE_DICT.get(PART_ID, 0)

    def _increase(self, duration):
        return self.arm.base.rotate_clock(duration)
    
    def _decrease(self, duration):
        return self.arm.base.rotate_counter(duration)

    def _stop(self):
        return self.arm.base.stop()

    def _block(self, duration):
        pass


class ArmLed(ArmPartBase):

    PART_ID = PART_LED
    MAX = PART_RANGE_DICT.get(PART_ID, 0)

    def _increase(self, duration):
        return self.arm.led.on()

    def _decrease(self, duration):
        return self.arm.led.off()

    def _stop(self):
        return self.arm.led.stop()

    def _block(self, duration):
        pass