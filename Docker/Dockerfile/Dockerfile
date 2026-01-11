FROM alpine:latest

RUN apk update && \
    apk add python3 py3-pip su-exec curl wget unzip && \
    mkdir -p /netflowParser

WORKDIR /netflowParser

# Copy over IP2Loc, INFLUXDB, proto and wahtDomain

COPY ../Code/* /netflowParser/
COPY ./entrypoint.sh /entrypoint.sh
COPY ./updateIP2Lbin.sh /netflowParser/

RUN chmod +x /entrypoint.sh

RUN python3 -m venv venv && \
    /netflowParser/venv/bin/python3 -m pip install --upgrade pip && \
    /netflowParser/venv/bin/pip3 install -r requirements.txt
    # venv/bin/pip3 install -r requirements.txt 

# Set user. No need for root past this point
# USER "${USER}"

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 2055

CMD ["/netflowParser/venv/bin/python3", "/netflowParser/INFLUXDB.py"]
