# -*- coding: utf-8 -*-
from arm.models.device import ArmDevice
from arm.models.utils.kvs import CacheKvs


class DeviceStatus(object):
    @staticmethod
    def is_on():
        return ArmDevice.status()


class PartStatus(DeviceStatus):

    def __init__(self, part_id):
        self.part_id = part_id

    @property
    def _key(self):
        return "{}:{}:".format(self.__class__.__name__, self.part_id)

    @property
    def _cache(self):
        return CacheKvs(self._key)

    @property
    def position(self):
        position = self._cache.get()
        return int(position) if position else 0

    def incr(self, duration):
        # decrease when duration is minus
        self._cache.incr(duration)

    def reset(self):
        self._cache.reset()


class StatusMixin(object):
    """
    获取状态，修改状态，reset状态
    """
    @property
    def status(self):
        return PartStatus(self.PART_ID)

    def is_min(self):
        position = self.status.position
        if position <= self.MIN:
            return True
        return False

    def is_max(self):
        position = self.status.position
        if position >= self.MAX:
            return True
        return False

    def can_action(self, m_range):
        """
        判断是否可以移动
        """
        if not self.status.is_on():
            return False
        if m_range == 0:
            return False
        if m_range < 0 and self.is_min():
            return False
        if m_range > 0 and self.is_max():
            return False
        if self._block(m_range):
            return False
        return True

    def _block(self, m_range):
        pass
