# -*- coding: utf-8 -*-
import redis
from config import REDIS_CONF

_pool = redis.ConnectionPool(
        host=REDIS_CONF['host'],
        port=REDIS_CONF['port'],
        db=REDIS_CONF['db'],
        )
_redis = redis.Redis(connection_pool=_pool)

class Kvs(object):

    def __init__(self, key, expires=None):
        self._key = key
        self._redis = _redis
        self._pipe = self._redis.pipeline()
        self._expires = expires if expires else None

    @property
    def key(self):
        return self._key

    @property
    def expires(self):
        return self._expires

    def get(self):
        return self._redis.get(self.key)

    def set(self, value, nx=False):
        return self._redis.set(self.key, value, ex=self.expires, nx=nx)

    def set_expires(self, ex):
        self._expires = ex
        return self._redis.expire(self.key, self.expires)

    def _incr_with_expires(self, key, amount=1):
        """
        Called only if self.expires is not None
        """
        self._pipe.incr(key, amount)
        self._pipe.expire(key, self.expires)
        return self._pipe.execute()

    def _decr_with_expires(self, key, amount=1):
        """
        Called only if self.expires is not None
        """
        self._pipe.decr(key, amount)
        self._pipe.expire(key, self.expires)
        return self._pipe.execute()
 
    def incr(self, amount=1):
        if self.expires:
            return self._incr_with_expires(self.key, amount)
        else:
            return self._redis.incr(self.key, amount)

    def decr(self, amount=1):
        if self.expires:
            return self._decr_with_expires(self.key, amount)
        else:
            return self._redis.decr(self.key, amount)
        
    def delete(self):
        return self._redis.delete(self.key)

