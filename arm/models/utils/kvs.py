# -*- coding: utf-8 -*-
import redis


class CacheKvs(object):

    _POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)
    _CONNECT = redis.Redis(connection_pool=_POOL)
    
    def __init__(self, key):
        self._pipe = self._CONNECT.pipeline()
        self._key = key

    @property
    def key(self):
        return self._key

    def _set(self, key, value, expires=None, nx=False):
        self._pipe.set(key, value, expires, nx)
        self._pipe.execute()

    def _get(self, key):
        self._pipe.get(key)
        return self._pipe.execute()[0]

    def _incr(self, key, delta):
        self._pipe.incr(key, delta)
        self._pipe.execute()

    def _decr(self, key, delta):
        self._pipe.decr(key, delta)
        self._pipe.execute()

    def get(self):
        return self._get(self.key)

    def set(self, value, expires=None, nx=False):
        self._set(self.key, value, expires, nx)

    def incr(self, delta=1):
        self._incr(self.key, delta)

    def reset(self):
        self._set(self.key, 0)

    def delete(self):
        self._pipe.delete(self.key)