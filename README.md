# NetFlowV5 collector and InfluxDB and Grafana

It works.

## IP2Location-DB

To get IP2Locatio-Lite-DB go to [lite.ip2location](https://lite.ip2location.com/) and create a account.

Then you need to get your **Token**. You can find it [here](https://lite.ip2location.com/database-download) and under **Download Token**

Then pass that token as ```IP2LOC_TOKEN``` environment variable to the container

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


