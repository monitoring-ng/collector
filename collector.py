#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
 
from flask import Flask
from flask import request
from flask.views import MethodView

from lib.flask_pbj import api, json, protobuf

from lib.metric_pb2 import MetricBatch, Status

from influxdb import InfluxDBClient


class MetricEndpoint(MethodView):
    decorators = [api(json, protobuf(receives=MetricBatch, sends=Status))]

    def _get_prefix(self, path):
        return path.split('.')[0]

    def _get_value(self, path):
        return path.split('.')[-1:][0]

    def _get_measurement(self, path):
        items = path.split('.')
        if len(items) == 5:
            return ".".join(path.split('.')[-3:-1])
        else:
            return ".".join(path.split('.')[-2:-1])

    def post(self):
        metricbatch = request.data_dict
        influx_points = []
        for metric in metricbatch['metric']:
            influx_points.append({
                'measurement': self._get_measurement(metric['path']),
                'tags': {
                    'hostname': metric['host'],
                    'type': self._get_value(metric['path'])
                },
                'time': int(metric['timestamp']),
                'fields': {
                    'value': metric['value']
                }
            })

        client = InfluxDBClient(config.db_host, config.db_port, config.db_user, config.db_pass, config.db_name)
        client.write_points(influx_points,  time_precision='s')

        return {
            'code': 200,
            'message': 'OK',
        }


class MetricCollector(Flask):
    def __init__(self, name):
        Flask.__init__(self, name)
        metric_endpoint = MetricEndpoint.as_view('metric')
        self.add_url_rule('/', view_func=metric_endpoint)


def main():
    app = MetricCollector(__name__)
    app.run(debug=config.debug, host='0.0.0.0')

if __name__ == '__main__':
    main()
