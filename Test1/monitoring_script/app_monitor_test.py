#!/usr/bin/env python
from unittest import TestCase, main
import os.path
import socket
from app_monitor import AppMonitor

class TestServiceMonitor(TestCase):

    def test_get_service_state_systemd(self):
        '''
        this will fail on rhel6 and below
        '''
        appmon = AppMonitor()
        monitor_cmd = ['/usr/bin/systemctl', 'show', 'rabbitmq-server', "--property=ActiveState"]
        service_state_out = appmon.get_service_state(monitor_cmd)
        self.assertTrue(service_state_out)

    def test_get_service_state_service(self):
        '''
        this might fail on rhel6 and below
        '''
        appmon = AppMonitor()
        monitor_cmd = ['/usr/sbin/service', 'rabbitmq-server', 'show']
        service_state_out = appmon.get_service_state(monitor_cmd)
        self.assertTrue(service_state_out)

    def test_get_service_state_service_trad(self):
        '''
        this might fail on rhel7 and above
        '''
        appmon = AppMonitor()
        monitor_cmd = ['/sbin/service', 'rabbitmq-server', 'show']
        service_state_out = appmon.get_service_state(monitor_cmd)
        self.assertTrue(service_state_out)

    def test_process_state_servmq(self):
        '''
        testing Up for rabbitmq
        '''
        appmon = AppMonitor()
        proc_mgr = "service"
        service_name = "rabbitmq-server"
        service_state_out = "pid: 1111; uptime: 192"
        host_name = socket.getfqdn()
        expected_status = {"service_name": service_name, "service_status": "UP",
                           "host_name": host_name}
        actual_status = appmon.process_state(proc_mgr, service_name, service_state_out)
        self.assertEqual(expected_status, actual_status)

    def test_process_state_sysmq(self):
        '''
        testing Up for rabbitmq
        '''
        appmon = AppMonitor()
        proc_mgr = "systemd"
        service_name = "rabbitmq-server"
        service_state_out = "ActiveState=active"
        host_name = socket.getfqdn()
        expected_status = {"service_name": service_name, "service_status": "UP",
                           "host_name": host_name}
        actual_status = appmon.process_state(proc_mgr, service_name, service_state_out)
        self.assertEqual(expected_status, actual_status)

    def test_process_state_servmq_down(self):
        '''
        testing Down for rabbitmq
        '''
        appmon = AppMonitor()
        proc_mgr = "service"
        service_name = "rabbitmq-server"
        service_state_out = "pid: not available"
        host_name = socket.getfqdn()
        expected_status = {"service_name": service_name, "service_status": "DOWN",
                           "host_name": host_name}
        actual_status = appmon.process_state(proc_mgr, service_name, service_state_out)
        self.assertEqual(expected_status, actual_status)

    def test_process_state_sysmq_down(self):
        '''
        testing Down for rabbitmq
        '''
        appmon = AppMonitor()
        proc_mgr = "systemd"
        service_name = "rabbitmq-server"
        service_state_out = "ActiveState=failed"
        host_name = socket.getfqdn()
        expected_status = {"service_name": service_name, "service_status": "DOWN",
                           "host_name": host_name}
        actual_status = appmon.process_state(proc_mgr, service_name, service_state_out)
        self.assertEqual(expected_status, actual_status)

    def test_write_to_file(self):
        '''
        unit test for write_to_file
        '''
        appmon = AppMonitor()
        test_status = {"service_name": "httpd", "service_status": "DOWN",
                       "host_name": "test.example.com"}
        file_name = appmon.write_to_file("httpd", test_status)
        self.assertTrue(os.path.exists(file_name))

if __name__ == '__main__':
    main()
