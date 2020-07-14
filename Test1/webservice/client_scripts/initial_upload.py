#!/usr/bin/env python3
import json
import argparse
import os.path
import requests

class InitialUpload():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.status_url = "https://localhost:5000"
        self.register_url = self.status_url + "/register"
        self.auth_url = self.status_url + "/auth"
        self.upload_url = self.status_url + "/add"
        self.status_files_dir = os.path.abspath(os.path.curdir)

    def get_user_payload(self):
        if self.username and self.password:
            return {"username": self.username, "password": self.password}
        return {"username": "default", "password": "default"}

    def make_initial_upload(self):
        '''
        initial upload of three files in the current dir
        '''
        payload = self.get_user_payload()
        register_status = requests.post(self.register_url, verify=False, data=payload)
        api_status = requests.post(self.auth_url, verify=False, json=payload)
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
        print(upload_status)

def collect_user_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', action='store', dest='username',
                        help='username to use for this session')
    parser.add_argument('-p', '--pasword', action='store', dest='password',
                        help='password to use for this session')
    return parser.parse_args()

if __name__ == '__main__':
    args = collect_user_args()
    initial_upload = InitialUpload(args.username, args.password)
    initial_upload.make_initial_upload()
