## app_monitor.py

### Purpose:

Program to check status of three services "httpd", "rabbitmq-server", "postgresql-11" on RHEL hosts. The output is in JSON format and written to a file.

### Usage:

The program doesnt need any argument and it is run as shown below.

`# python app_monitor.py`

### Output Files:

The status output files are stored under directory "/var/log/appmonitor"
Please do any required cleanup when the files are no longer required.

Filenames follow "{serviceName}-status-{@timestamp}.json" format.

### Example Filenames:

httpd-status-20200704045001.json

postgresql-11-status-20200704045001.json

rabbitmq-server-status-20200704045001.json

The program logs are stored in /var/log/appmonitor/monitor.log

### Tests:

Unittests are in app_monitor_test.py

### Note:

The program is written to be accommodating of different RHEL and Python versions as
much as possible.
