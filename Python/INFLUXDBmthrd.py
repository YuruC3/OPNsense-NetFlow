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

# INFLUXDB config
token = "apg1gysUeCcxdcRTMmosJTenbEppmUNi9rXlANDB2oNadBdWAu2GVTDc_q_dyo0iyYsckKaOvPRm6ba2NK0y_A=="
#token = os.getenv("INFLUX_TOKEN")
bucket = "NETFLOW-7"
# bucket = os.getenv("INFLUX_BUCKET")
org = "staging"
# org = os.getenv("INFLUX_ORG")
url = "http://localhost:8086"
# url = os.getenv("INFLUX_URL")
measurement = "testNetFlowPython"
# measurement = os.getenv("INFLUX_MEASUREMENT")
MACHINE_TAG = "YUKIKAZE"
# MACHINE_TAG = os.getenv("INFLUX_MACHINE_TAG")
ROUTER_TAG = "HQ"
# ROUTER_TAG = os.getenv("INFLUX_ROUTER_TAG")
INFLX_SEPARATE_POINTS = 0.05

# Initialize InfluxDB client and influxdb API
inflxdb_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
#write_api = inflxdb_client.write_api(write_options=SYNCHRONOUS)
write_api = inflxdb_client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=1000))

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

    # Prep InfluxDB data
    inflxdb_Data_To_Send = (
        influxdb_client.Point(f"{measurement}-script")
        .tag("MACHINE", MACHINE_TAG)
        .tag("ROUTER", ROUTER_TAG)
        .field("dstAddr", inEntry["IPV4_DST_ADDR"])
        .field("srcAddr", inEntry["IPV4_SRC_ADDR"])
        .field("nextHop", inEntry["NEXT_HOP"])
        .field("inptInt", inEntry["INPUT"])
        .field("outptInt", inEntry["OUTPUT"])
        .field("inPackt", inEntry["IN_PACKETS"])
        .field("outPakt", inEntry["IN_OCTETS"])
        .field("frstSwtchd", inEntry["FIRST_SWITCHED"])
        .field("lstSwtchd", inEntry["LAST_SWITCHED"])
        .field("srcPort", inEntry["SRC_PORT"])
        .field("dstPort", inEntry["DST_PORT"])
        .field("tcpFlags", inEntry["TCP_FLAGS"])
        .tag("proto", manWhatTheProto(int(inEntry["PROTO"])))
        .field("tos", inEntry["TOS"])
        .field("srcAS", inEntry["SRC_AS"])
        .field("dstAS", inEntry["DST_AS"])
        .field("srcMask", inEntry["SRC_MASK"])
        .field("dstMask", inEntry["DST_MASK"])
        .field("dstCntr", ermWhatTheCountry(str(inEntry["IPV4_DST_ADDR"])))
        .field("srcCntr", ermWhatTheCountry(str(inEntry["IPV4_SRC_ADDR"])))
    )

    print("----------------")
    return (i, inflxdb_Data_To_Send, inEntry)

# Bind
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((WHAT_THE_NETFLOW_IP, WHAT_THE_NETFLOW_PORT)) 

print("Ready")

with ThreadPoolExecutor(max_workers=8) as executor:
    # With means that when exiting the "executor" will be cleanly shut down
    # as executor is an object that is then used to give jobs to

    while True:
        # Get netentry data ig?
        sock.settimeout(5)


        payload, client = sock.recvfrom(4096)  # experimental, tested with 1464 bytes
        # Tajes UPD packets that are at max 4096 bytes
        # payload has the raw netflow data
        # client has source IP address as well as port

        p = netflow.parse_packet(payload)  # Test result: <ExportPacket v5 with 30 records>
        #print(p.entrys)  # Test result: 5

        # Submit all entries to thread pool
        futures = [executor.submit(process_flow, i, entry) for i, entry in enumerate(p.flows, 1)]
        # Big thinkg happen here
        # Here I give an executor a job. That job is to run function <process_flow> with arguments i and entry. Then it becomes one thread
        # Furthermore for each entry, so flow record, we submit a task to a thread
        # In comparasion, without multithreading it only had one for function
        # for i, entry in enumerate(p.flows, 1)
        # And the results from a job on a thread (executor) are stored in futures ____list____


        bigDict = {}
        inflxdb_Datazz_To_Send = []

        for future in futures:
            i, point, inEntry = future.result()
            # goes through every job done by executor.
            # i is being reused from the original enumerate
            # point is the InfluxDB-ready data object
            # inEntry is what a single flow in the 30 flow dictionary in Netflow

            inflxdb_Datazz_To_Send.append(point)
            bigDict[i] = inEntry

        # Send data to InfluxDB
        write_api.write(bucket=bucket, org=org, record=inflxdb_Datazz_To_Send)
        time.sleep(INFLX_SEPARATE_POINTS) # separate points 

        print(f"{len(bigDict)} <--- This many entrys")

        # Clean up before another loop
        bigDict.clear()
        inflxdb_Datazz_To_Send.clear()
        #print(bigDict)

