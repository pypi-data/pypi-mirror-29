#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2018 jianglin
# File Name: test_quickapi.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2018-01-09 13:54:41 (CST)
# Last Update: 星期五 2018-02-23 10:50:32 (CST)
#          By:
# Description:
# **************************************************************************
import unittest
from main import User, Group, Permission
from test import TestBase
from flask_maple.views import QuickApi
import json


class Request(object):
    def __init__(self, app_test):
        self.app_test = app_test

    def get(self, url, **kwargs):
        return json.loads(self.app_test.get(url, **kwargs).data)

    def post(self, url, **kwargs):
        return json.loads(self.app_test.post(url, **kwargs).data)


class QuickAPITest(TestBase):
    def setUp(self):
        super(QuickAPITest, self).setUp()
        api = QuickApi(self.app)
        api.create_api(User)
        api.create_api(Group)
        api.create_api(Permission)
        self.app_test = self.app.test_client()
        self.app_request = Request(self.app_test)

    def test_get_user(self):
        r = self.app_request.get('/api/user')
        self.assertEqual(len(r['data']), 3)
        self.assertEqual(r['data'][0]['username'], 'user1')

        params = {'username': 'user1'}
        r = self.app_request.get('/api/user', query_string=params)
        self.assertEqual(len(r['data']), 1)
        self.assertEqual(r['data'][0]['id'], 1)

        params = {'username': 'user4'}
        r = self.app_request.get('/api/user', query_string=params)
        self.assertEqual(len(r['data']), 0)

    # def test_post_user(self):
        params = {'username': 'user4'}
        r = self.app_request.post('/api/user', data=params)
        print(r)


if __name__ == '__main__':
    unittest.main()
