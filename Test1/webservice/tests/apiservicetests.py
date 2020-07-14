#!/usr/bin/env python3
import requests
import os.path
import json
from unittest import TestCase, main

class ApiTest(TestCase):
    def __init__(self, *args, **kwars):
        self.status_url = "https://localhost:5000"
        self.register_url = self.status_url + "/register"
        self.auth_url = self.status_url + "/auth"
        self.upload_url = self.status_url + "/add"
        self.app_status_url = self.status_url + "/health_check"
        self.service_status_url = self.status_url + "/health_check/rbcapp1"
        self.status_files_dir = os.path.abspath(os.path.curdir)
        self.acceptable_code = 200
        super(ApiTest, self).__init__(*args, **kwars)

    def test_user_registration(self):
        '''
        testing availability, response code on /register
        '''
        test_user = {"username": "testuser", "password": "testsecret"}
        register_status = requests.post(self.register_url, verify=False, data=test_user)
        acceptable_codes = [201, 400]
        self.assertIn(register_status.status_code, acceptable_codes)

    def test_user_auth(self):
        '''
        testing availability, response code on /auth
        '''
        test_user = {"username": "testuser", "password": "testsecret"}
        register_status = requests.post(self.register_url, verify=False, data=test_user)
        api_status = requests.post(self.auth_url, verify=False, json=test_user)
        self.assertEqual(api_status.status_code, self.acceptable_code)

    def test_file_upload(self):
        '''
        testing availability, response code on /add
        '''
        test_user = {"username": "testuser", "password": "testsecret"}
        register_status = requests.post(self.register_url, verify=False, data=test_user)
        api_status = requests.post(self.auth_url, verify=False, json=test_user)
        api_status_dict = json.loads(api_status.text)
        headers = {'Authorization': "JWT " + api_status_dict['access_token'] }

        httpd_file = os.path.join(self.status_files_dir, "httpd-status-20200704045001.json")
        rabbitmq_file = os.path.join(self.status_files_dir, "rabbitmq-server-status-20200704045001.json")
        postgresql_file = os.path.join(self.status_files_dir, "postgresql-11-status-20200704045001.json")
        httpd_fh = open(httpd_file, "r")
        rabbitmq_fh = open(rabbitmq_file, "r")
        postgresql_fh = open(postgresql_file, "r")
        upload_files = {"httpd_file": httpd_fh, "rabbitmq_file": rabbitmq_fh,
                        "postgresql_file": postgresql_fh}
        upload_status = requests.post(self.upload_url, verify=False, headers=headers, files=upload_files)
        httpd_fh.close()
        rabbitmq_fh.close()
        postgresql_fh.close()
        self.assertEqual(upload_status.status_code, self.acceptable_code)

    def test_app_status(self):
        '''
        testing availability, response code on /health_check
        '''
        app_status = requests.get(self.app_status_url, verify=False)
        self.assertEqual(app_status.status_code, self.acceptable_code)

    def test_service_status(self):
        '''
        testing availability, response code on /health_check/rbcapp1
        '''
        service_status = requests.get(self.service_status_url, verify=False)
        self.assertEqual(service_status.status_code, self.acceptable_code)

if __name__ == '__main__':
    main(warnings='ignore')
