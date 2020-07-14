#!/usr/bin/env python
import requests

class GetStatus():
    def __init__(self):
        self.status_url = "https://localhost:5000"
        self.app_status_url = self.status_url + "/health_check"
        self.service_status_url = self.status_url + "/health_check/rbcapp1"

    def get_app_status(self):
        '''
        testing availability, response code on /health_check
        '''
        app_status = requests.get(self.app_status_url, verify=False)
        print(app_status.text)

    def get_service_status(self):
        '''
        testing availability, response code on /health_check/rbcapp1
        '''
        service_status = requests.get(self.service_status_url, verify=False)
        print(service_status.text)

if __name__ == '__main__':
    getstatus = GetStatus()
    getstatus.get_app_status()
    getstatus.get_service_status()
