# -*- coding: utf-8 -*-
import redis


class CacheKvs(object):

    _POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)
    _CONNECT = redis.Redis(connection_pool=_POOL)
    _EXPIRES = 60 * 1000
    
    def __init__(self, key, expires=None):
        self._key = key
        self._redis = self._CONNECT
        self._pipe = self._redis.pipeline()
        self._expires = expires if expires else self._EXPIRES

    @property
    def key(self):
        return self._key

    def _set(self, key, value, expires=None, nx=False):
        self._redis.set(key, value, ex=expires, nx=nx)

    def _get(self, key):
        return self._redis.get(key)

    def _incr(self, key, delta):
        self._pipe.incr(key, delta)
        self._pipe.expire(key, self._expires)
        self._pipe.execute()

    def _decr(self, key, delta):
        self._pipe.decr(key, delta)
        self._pipe.expire(key, self._expires)
        self._pipe.execute()

    def delete(self):
        self._redis.delete(self.key)
 
    def get(self):
        return self._get(self.key)

    def set(self, value, expires=None, nx=False):
        self._set(self.key, value, expires, nx)

    def incr(self, delta=1):
        self._incr(self.key, delta)

    def reset(self):
        self._set(self.key, 0)
