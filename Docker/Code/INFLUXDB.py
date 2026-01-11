import netflow, socket, json, time, os, influxdb_client, ipaddress
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS, WriteOptions
from datetime import timedelta
from proto import manWhatTheProto
from IP2Loc import ermWhatTheCountry
from whatDomain import ermWhatATheIpFromDomainYaCrazy, ermWhatAAAATheIpFromDomainYaCrazy
from typing import Annotated

# Netentry preconf
# WHAT_THE_NETFLOW_PORT: Final[int] = os.getenv("WHAT_THE_NETFLOW_PORT", "2055")
WHAT_THE_NETFLOW_PORT = 2055
WHAT_THE_NETFLOW_IP = "0.0.0.0"


# INFLUXDB config

token: Final[str] = os.getenv("token", "NotPresent")
# token = "apg1gysUeCcxdcRTMmosJTenbEppmUNi9rXlANDB2oNadBdWAu2GVTDc_q_dyo0iyYsckKaOvPRm6ba2NK0y_A==" 
bucket: Final[str] = os.getenv("bucket", "NotPresent")
# bucket = "NETFLOW-7"
org: Final[str] = os.getenv("org", "NotPresent")
# org = "staging"
url: Final[str] = os.getenv("url", "NotPresent")
# url = "http://localhost:8086"
measurement: Final[str] = os.getenv("measurement", "OPNsense-NetFlow-Parser")
# measurement = "testNetFlowPython"
MACHINE_TAG: Final[str] = os.getenv("MACHINE_TAG", socket.gethostname())
# MACHINE_TAG = "YUKIKAZE"
ROUTER_TAG: Final[str] = os.getenv("ROUTER_TAG", socket.gethostname())
# ROUTER_TAG = "HQ"
INFLX_SEPARATE_POINTS: Final[float] = os.getenv("INFLX_SEPARATE_POINTS", 0.1)
# INFLX_SEPARATE_POINTS = 0.1

# Emulate sFlow behaviour 
SAMPLING_SIZE: Final(int) = os.getenv("SAMPLING_SIZE", 100)

# Initialize InfluxDB client and influxdb API
inflxdb_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = inflxdb_client.write_api(write_options=SYNCHRONOUS)

# Other preconf
bigDict = {}
inflxdb_Datazz_To_Send = []

# Bind
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((WHAT_THE_NETFLOW_IP, WHAT_THE_NETFLOW_PORT)) 

print("Ready")


# Flightchecks
flightlist = [token, bucket, org, url]

if "NotPresent" in flightlist:
    return 1


while True:
    # Get netentry data ig?
    payload, client = sock.recvfrom(4096)  # experimental, tested with 1464 bytes
    p = netflow.parse_packet(payload)  # Test result: <ExportPacket v5 with 30 records>
    #print(p.entrys)  # Test result: 5

    #yesyes = p.flows
    #print(yesyes.data)
    #exit()

   
    
    for i, entry in enumerate(p.flows, 1):
        # prep dict
        #tmpEntry = str(entry)
        #tmpEntry = tmpEntry[22:-1]
        #tmpEntry2 = tmpEntry.replace("'", '"')
    
        #print(tmpEntry2)
        #print(entry
        #exit()
        #dictEntry = json.loads(tmpEntry2)
        #bigDict[i] = (dictEntry)
    
    
        # take data out from netentry 
        inEntry = entry.data

        print(inEntry)
        exit()
    
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

        inflxdb_Datazz_To_Send.append(inflxdb_Data_To_Send)
    
        #i+=1
        #type(tmpEntry)
        #print(dictEntry)
        #print(tmpEntry.lstrip(20))
    
        print("----------------")
        bigDict[i] = (inEntry)

    # end while True
       
    print()
    print(bigDict)
    exit()
    
    # Send data to InfluxDB
    write_api.write(bucket=bucket, org="staging", record=inflxdb_Data_To_Send)
    time.sleep(INFLX_SEPARATE_POINTS) # separate points 

    print(f"{len(bigDict)} <--- This many entrys")


    # Clean up before another loop
    bigDict.clear()
    inflxdb_Datazz_To_Send.clear()

    #print(bigDict)
