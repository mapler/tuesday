# -*- coding: utf-8 -*-
from flask.ext.login import UserMixin
from utils.kvs import Kvs
from config import SESSION_EXPIRES


class IDGenerator(object):

    def __init__(self, key):
        self._key = '{}_id'.format(key)
        self._store = Kvs(self._key)

    def new(self):
        return self._store.incr()

    def get(self):
        return self._store.get()

    def reset(self):
        return self._store.delete()

    def get_current(self):
        return self.get()


class UserCreateError(Exception):
    pass


class UserManager(object):
    
    user_session = Kvs('user_session', SESSION_EXPIRES)
    id_generator = IDGenerator('user')

    def create_user(self, name):
        id = str(self.id_generator.new())
        user_data = {'id': id, 'name': name}
        if not self.user_session.hmset(user_data, nx=True):
            raise UserCreateError('User Created Failure. Arm is in use.')
        return User(id, name)

    def get_user(self, id):
        current_user = self.get_current_user()
        if current_user and current_user.id == id:
            return current_user
        else:
            return None

    def get_current_user(self):
        user_data = self.user_session.hgetall()
        if user_data:
            return User(**user_data)
        else:
            return None

    def get_ttl(self):
        return self.user_session.ttl()

    def clear(self):
        self.user_session.delete()

        
user_manager = UserManager()


class User(UserMixin):

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def is_authenticated(self):
        user = user_manager.get_user(self.id)
        return bool(user)

    def is_active(self):
        return self.is_authenticated()

    @property
    def ttl(self):
        if self.is_active():
            return user_manager.get_ttl()
        else:
            return 0

