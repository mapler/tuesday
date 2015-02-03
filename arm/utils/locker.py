# -*- coding: utf-8 -*-
from kvs import CacheKvs


class Locker(object):
    """
    locker for move the locker
    """

    LOCKER_KEY = 'locker'
    EXPIRES = 5  # 5 sec

    def __init__(self, key=None):
        self.key = self.LOCKER_KEY
        if key:
            self.key += '.{}'.format(key)
        self.locker = CacheKvs(self.key)

    def lock(self):
        self.locker.set('locked', expires=self.EXPIRES, nx=True)

    def unlock(self):
        self.locker.delete()

    def is_lock(self):
        return self.locker.get() == 'locked'

    def on_lock(self, func):
        def wrapper(*args, **kwargs):
            if self.lock():
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    raise e
                finally:
                    self.unlock()
        return wrapper
