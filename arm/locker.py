# -*- coding: utf-8 -*-
from utils.kvs import Kvs


class Locker(object):
    """
    locker for move the locker
    """

    LOCKER_KEY = 'locker'
    _EXPIRES = 5  # 5 sec

    def __init__(self, key=None):
        self.key = self.LOCKER_KEY
        if key:
            self.key = '{}_{}'.format(key, self.key)
        self.locker = Kvs(self.key, expires=self._EXPIRES)

    def lock(self):
        return self.locker.set('locked', nx=True)

    def unlock(self):
        return self.locker.delete()

arm_locker = Locker('arm')

def on_lock(func):
    def wrapper(*args, **kwargs):
        if arm_locker.lock():
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise e
            finally:
                arm_locker.unlock()
    return wrapper
