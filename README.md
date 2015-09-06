# Collector - Collect Metrics via Protocol Buffers

Collector is a small WSGI app that uses googles protocol buffers for efficient transmission of metrics. Since it uses HTTP(s) it can be easily load balanced.

## Backends

Right now, there is only one backend: [InfluxDB](https://influxdb.com). It is a quite new open source timeseries database. 

## What's next?

This is still work in progress. I mainly wanted to have an endpoint where I can send metrics to, which has a stable interface (which InfluxDB has not (yet)), transmits the data efficient (using googles protocol buffers) and is easily scalable (HTTP(S), stateless).

It works for me, covering my currents needs. I just want to share the code that is produced during my efforts to create a new monitoring system.
