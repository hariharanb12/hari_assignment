## APIservice

This API service provides for users to upload individual service status files that contain JSON output of
service status and hostname details.
Users also can query the status of the Application that is made up of three services (httpd, rabbitmq-server, postgresql-11).

The service provides the following endpoints.

### /health_check
This endpoint can be used to query the application status.
A highlevel status is returned

Example when app is healthy:
{"appstatus": "UP"}

Example when app is unhealthy:
{"appstatus": "DOWN"}

### /health_check/rbcapp1

Thie endpoint is used to query the application status along with the individual
service statuses.

Example status returned by this endpoint
{"httpd": "UP", "rabbitmq-server": "DOWN", "postgresql-11": "UP", "rbcapp1": "DOWN"}

### /add

This endpoint is used to upload the service status files containing the JSON object
to the service.

### /register
This is for users to be registered in the service.

### /auth
This is the endpoint that users send their credentials and exchance for a JWT token
that can be used for future calls to the service.


## Deployment

The service is containerized using docker-compose tool.
There are two containers created by the docker-compose tool.
Container One: apiservice
Container Two: Elasticsearch service

Command to deploy:

Change directory to this directory, then run below -

`$ docker-compose up -d`

Both containers have health checks configured, and initial settling period of thirty seconds
to make sure the services are healthy.

The health of the services can be queried with the below command.

`$ docker-compose ps`

Once the status is healthy, the services are ready to receive files and queries.

Example:

```
(base) webservice hari$ docker-compose ps
       Name                      Command                  State               Ports
--------------------------------------------------------------------------------------------
webservice_eshost_1   /tini -- /usr/local/bin/do ...   Up (healthy)   9200/tcp, 9300/tcp
webservice_web_1      /home/flasky/boot.sh             Up (healthy)   0.0.0.0:5000->5000/tcp
```

Once we see the above output, we can rock n roll.

## Client Scripts:

The containers dont contain any data when they start, a directory containing client scripts
for testing convenience is provided along with the code in this repo.

The sample files to upload to the service are also provided in "client_scripts" directory
located in this repo.

Initial File upload:

`cd client_scripts`
`python initial_upload.py`

To get the application and individual services statuses, the script get_status.py in the
client_scripts directory can be used.

`cd client_scripts`
`python get_status.py`

## Tests:

Tests are available in the tests directory.

`cd tests`
`python apiservicetests.py`
