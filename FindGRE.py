import netflow, socket, json, time, os, influxdb_client, ipaddress
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS, WriteOptions
from datetime import timedelta
from proto import manWhatTheProto
from IP2Loc import ermWhatTheCountry
from whatDomain import ermWhatATheIpFromDomainYaCrazy, ermWhatAAAATheIpFromDomainYaCrazy
from concurrent.futures import ThreadPoolExecutor

# Netentry preconf
WHAT_THE_NETFLOW_PORT = 2055
WHAT_THE_NETFLOW_IP = "0.0.0.0"



# Threaded flow processor
def process_flow(i, entry):
    # prep dict
    #tmpEntry = str(entry)
    #tmpEntry = tmpEntry[22:-1]
    #tmpEntry2 = tmpEntry.replace("'", '"')

    #print(tmpEntry2)
    #print(entry)
    #exit()
    #dictEntry = json.loads(tmpEntry2)
    #bigDict[i] = (dictEntry)

    # take data out from netentry
    inEntry = entry.data

    # Convert IPs and time duration
    # IPs
    inEntry["IPV4_SRC_ADDR"] = str(ipaddress.IPv4Address(inEntry["IPV4_SRC_ADDR"]))
    inEntry["IPV4_DST_ADDR"] = str(ipaddress.IPv4Address(inEntry["IPV4_DST_ADDR"]))
    inEntry["NEXT_HOP"] = str(ipaddress.IPv4Address(inEntry["NEXT_HOP"]))

    # Convert time from ms to HH:MM:SS
    first = int(inEntry["FIRST_SWITCHED"])
    last = int(inEntry["LAST_SWITCHED"])

    inEntry["FIRST_SWITCHED_HR"] = str(timedelta(milliseconds=first))
    inEntry["LAST_SWITCHED_HR"] = str(timedelta(milliseconds=last))

    protoHereWhat = manWhatTheProto(int(inEntry["PROTO"]))

    if protoHereWhat == "GRE" or inEntry["PROTO"] == 47:
        print("skibidi")
        exit()

    print("----------------")
    print(inEntry["PROTO"])
    return (i, inEntry)

# Bind
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((WHAT_THE_NETFLOW_IP, WHAT_THE_NETFLOW_PORT))

print("Ready")

with ThreadPoolExecutor(max_workers=8) as executor:
    while True:
        # Get netentry data ig?
        sock.settimeout(5)


        payload, client = sock.recvfrom(4096)  # experimental, tested with 1464 bytes
        p = netflow.parse_packet(payload)  # Test result: <ExportPacket v5 with 30 records>
        #print(p.entrys)  # Test result: 5

        # Submit all entries to thread pool
        futures = [executor.submit(process_flow, i, entry) for i, entry in enumerate(p.flows, 1)]

        bigDict = {}
        # inflxdb_Datazz_To_Send = []

        for future in futures:
            i, inEntry = future.result()
            # inflxdb_Datazz_To_Send.append(point)
            bigDict[i] = inEntry

        # Send data to InfluxDB
        # write_api.write(bucket=bucket, org=org, record=inflxdb_Datazz_To_Send)
        # time.sleep(INFLX_SEPARATE_POINTS) # separate points

        print(f"{len(bigDict)} <--- This many entrys")

        # Clean up before another loop
        bigDict.clear()
        # inflxdb_Datazz_To_Send.clear()
        #print(bigDict)

