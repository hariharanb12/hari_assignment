#!/usr/bin/env python
import json
import logging
import os.path
import socket
import subprocess
from datetime import datetime

class AppMonitor():
    '''
    script to collect service status and store in a file
    '''
    def __init__(self):
        self.monitored_services = ["httpd", "rabbitmq-server", "postgresql-11"]
        self.output_dir = "/var/log/appmonitor"
        self.host_name = socket.getfqdn()

    def _initialize_logging(self):
        '''
        initialize logging to /var/log/appmonitor/monitor.log
        '''
        log_filename = os.path.join(self.output_dir, 'monitor.log')
        fmt = '%(asctime)s %(levelname)s %(message)s'
        logging.basicConfig(filename=log_filename, level=logging.DEBUG, format=fmt)
        print("Logging is stored in %s", log_filename)

    def _get_procmgr(self):
        '''
        determine the process manager and the command used in the host
        systemctl most expected and /sbin/service least
        '''
        proc_systems = [('systemd', '/usr/bin/systemctl'),
                        ('service', '/usr/sbin/service'),
                        ('service', '/sbin/service')]
        for proc_system in proc_systems:
            proc_mgr, cmd = proc_system
            if os.path.exists(cmd):
                logging.info("this host uses %s %s", proc_mgr, cmd)
                return (proc_mgr, cmd)

    def get_service_state(self, monitor_cmd):
        '''
        get command output; try being python version neutral
        '''
        try:
            s_out = subprocess.Popen(monitor_cmd, shell=False, stdout=subprocess.PIPE)
        except OSError as err:
            logging.info("using incorrect command in this host, actual error %s", err)
            return
        except subprocess.CalledProcessError as err:
            logging.debug("service state query command execution failed, Error: %s", err)
            return
        service_state_out, service_err_out = s_out.communicate()
        logging.info("Gathered service status")
        return service_state_out

    def process_state(self, proc_mgr, service_name, service_state):
        '''
        return the json based on the service status
        '''
        if proc_mgr == "service":
            if service_name == "rabbitmq-server":
                # rabbitmq needs special handling in init systems
                if "pid" in str(service_state) and "uptime" in str(service_state):
                    service_status = "UP"
                else:
                    service_status = "DOWN"
            else:
                if "pid" in str(service_state):
                    service_status = "UP"
                else:
                    service_status = "DOWN"
        elif proc_mgr == "systemd":
            if str(service_state).split("=")[1].rstrip('\n') == "active":
                service_status = "UP"
            else:
                service_status = "DOWN"
        application_status = {"service_name": service_name, "service_status": service_status,
                              "host_name": self.host_name}
        logging.info("created status results for %s", service_name)
        return application_status

    def write_to_file(self, service_name, service_state):
        '''
        writes the given json object to file
        '''
        time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "{0}-status-{1}.json".format(service_name, time_stamp)
        service_json_file = os.path.join(self.output_dir, file_name)
        try:
            with open(service_json_file, "a+") as outfile:
                json.dump(service_state, outfile)
        except IOError as err:
            logging.debug("Couldnt write to file %s", err)
        logging.info("Service %s status has been written to %s", service_name, service_json_file)
        return service_json_file

    def main(self):
        '''
        loop over the services to be monitored and get their state
        '''
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self._initialize_logging()
        logging.info("Colleting service status from %s", socket.getfqdn())

        proc_mgr, cmd = self._get_procmgr()
        for service_name in self.monitored_services:
            if proc_mgr == "systemd":
                monitor_cmd = [cmd, 'show', service_name, "--property=ActiveState"]
            elif proc_mgr == "service":
                monitor_cmd = [cmd, service_name, "status"]
            service_state = self.get_service_state(monitor_cmd)
            if service_state:
                application_status = self.process_state(proc_mgr, service_name, service_state)
            else:
                continue
            self.write_to_file(service_name, application_status)

if __name__ == '__main__':
    app_monitor = AppMonitor()
    app_monitor.main()
