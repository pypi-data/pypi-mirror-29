# About

Microservice to manage the downloads of biomaj.

A protobuf interface is available in biomaj_download/message/message_pb2.py to exchange messages between BioMAJ and the download service.
Messages go through RabbitMQ (to be installed).

# Protobuf

To compile protobuf, in biomaj_download/message:

    protoc --python_out=. message.proto

# Development

    flake8  biomaj_download/\*.py biomaj_download/download


# Run

## Message consumer:

    export BIOMAJ_CONFIG=path_to_config.yml
    python bin/biomaj_download_consumer.py

## Web server

If package is installed via pip, you need a file named *gunicorn_conf.py* containing somehwhere on local server:

    def worker_exit(server, worker):
        from prometheus_client import multiprocess
        multiprocess.mark_process_dead(worker.pid)

If you cloned the repository and installed it via python setup.py install, just refer to the *gunicorn_conf.py* in the cloned repository.


    export BIOMAJ_CONFIG=path_to_config.yml
    rm -rf ..path_to/prometheus-multiproc
    mkdir -p ..path_to/prometheus-multiproc
    export prometheus_multiproc_dir=..path_to/prometheus-multiproc
    gunicorn -c gunicorn_conf.py biomaj_download.biomaj_download_web:app

Web processes should be behind a proxy/load balancer, API base url /api/download

Prometheus endpoint metrics are exposed via /metrics on web server


3.0.15:
  Fix progress download control where could have infinite loop
  Add irods download

3.0.14:
  Allow setup of local_endpoint per service, else use default local_endpoint

3.0.13:
  In rate limiting, add progress vs total of download
  Fix rate limiting submission

3.0.12:
  Add retry in case of session creation failure
  disable web thread logging

3.0.11:
  Display progress of download by percent of downloads
  In case of contact error in downloadclient, retry connection

3.0.10:
  Feature #3: Add rate limiting option to limit number of parallel downloads for a client

3.0.9:
  Add host in prometheus stats
  Fix #2: allow setting http.group.file.size or http.group.file.date to -1 if not avalaible in http(s) page for regexp

3.0.8:
  Fix prometheus stats
  Add consul supervision

3.0.7:
  Change size type to int64

3.0.6:
  Fix download_or_copy to avoid downloading a file  existing in a previous production directory

3.0.4:
  Fixes on messages

3.0.3:
  Fix management of timeout leading to a crash when using biomaj.download parameter.

3.0.2:
  set rabbitmq parameter optional

3.0.1:
  add missing README etc.. in package

3.0.0:
  move download management out of biomaj main package


