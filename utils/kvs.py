# -*- coding: utf-8 -*-
import redis
from config import REDIS_CONF

_pool = redis.ConnectionPool(
        host=REDIS_CONF['host'],
        port=REDIS_CONF['port'],
        db=REDIS_CONF['db'],
        )
redis = redis.Redis(connection_pool=_pool)


def _with_expires(command):
    """
    Execute redis command and 
    Keeping updated expires if object's expires was set.
    """
    def wrapper(obj, *args, **kwargs):
        if obj.expires:
            # monkey patch obj's handler to pipeline.
            _handler = obj.handler
            obj.handler = obj.pipe
            pipe = command(obj, *args, **kwargs)
            obj.handler = _handler
            if pipe:
                pipe.expire(obj.key, obj.expires)
                ret = pipe.execute()[:-1]  # exclude the expire_set result
                if len(ret) == 1:
                    return ret[0]
                else:
                    return ret
        else:
            return command(obj, *args, **kwargs)
    return wrapper


class Kvs(object):

    def __init__(self, key, expires=None):
        self._key = key
        self.redis = redis
        self.pipe = self.redis.pipeline()
        self._expires = expires if expires else None
        self.handler = self.redis

    @property
    def key(self):
        return self._key

    @property
    def expires(self):
        return self._expires

    def get(self):
        return self.handler.get(self.key)

    @_with_expires
    def set(self, value, nx=False):
        return self.handler.set(self.key, value, ex=self.expires, nx=nx)

    def set_expires(self, ex):
        self._expires = ex
        return self.handler.expire(self.key, self.expires)

    def ttl(self):
        ttl = self.handler.ttl(self.key)
        return ttl if ttl else 0

    @_with_expires
    def incr(self, amount=1):
        return self.handler.incr(self.key, amount)
 
    @_with_expires
    def decr(self, amount=1):
        return self.handler.decr(self.key, amount)

    def hget(self, key):
        return self.handler.hget(self.key, key)
    
    @_with_expires
    def hset(self, key, value, nx=False):
        if nx:
            return self.handler.hsetnx(self.key, key, value)
        else:
            return self.handler.hset(self.key, key, value)

    def hgetall(self):
        return self.handler.hgetall(self.key)

    def hkeys(self):
        return self.handler.hkeys(self.key)

    def hmget(self, keys, *args):
        return self.handler.hmget(self.key, keys, *args)

    @_with_expires
    def hmset(self, mapping, nx=False):
        if nx and self.redis.exists(self.key):
            return
        else:
            return self.handler.hmset(self.key, mapping)

    def delete(self):
        return self.handler.delete(self.key)
