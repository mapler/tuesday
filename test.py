#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from utils.kvs import Kvs
import time


class KvsTestCase(unittest.TestCase):

    def setUp(self):
        self.kvs = Kvs('test')
        self.data = {'test': '111', 'test2': '222', 'test3': '333'}
        self.data2 = {'test5': '555', 'test6': '666', 'test3': '3322'}

    def tearDown(self):
        self.kvs.delete()

    def test_hmset(self):
        ret = self.kvs.hmset(self.data)
        assert ret == True
        assert self.kvs.hgetall() == self.data
        ret = self.kvs.hmset(self.data2)
        assert ret == True
        data = self.data
        data.update(self.data2)
        assert self.kvs.hgetall() == data

    def test_hmset_nx(self):
        ret = self.kvs.hmset(mapping=self.data)
        assert ret == True
        assert self.kvs.hgetall() == self.data
        ret = self.kvs.hmset(mapping=self.data2, nx=True)
        data = self.data
        data.update(self.data2)
        assert self.kvs.hgetall() != data
        assert ret == None

class KvsTestCaseWithSession(KvsTestCase):

    def setUp(self):
        self.kvs = Kvs('test', 1)
        self.data = {'test': '111', 'test2': '222', 'test3': '333'}
        self.data2 = {'test7': '555', 'test6': '666', 'test3': '3322'}

    def test_hmset_session(self):
        ret = self.kvs.hmset(mapping=self.data)
        assert ret == True
        assert self.kvs.hgetall() == self.data
        time.sleep(1)
        assert self.kvs.get() == None
 
