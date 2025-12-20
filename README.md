# NetFlowV5 collector and InfluxDB and Grafana

Here I'll try integrating both NetFlow and sFlow into my python code so that either can be choosen. 

It works.

## Python script
Install required modules with 
```
pip install -r requirements.txt
```

Then change InfluxDB variables.

### INFLUXDB.py vs INFLUXDBmthrd.py
First one runs on one thread and should work when there isn't much data on the network.

Second is when there are a ton of flows that need to be collected. More flows aka more data.

## sysctl.d
Place it in /etc/sysctl.d/ and apply with ```sysctl -p```

