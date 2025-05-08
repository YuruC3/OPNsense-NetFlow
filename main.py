import netflow
import socket
import json

i=1
bigDict = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 2055))
payload, client = sock.recvfrom(4096)  # experimental, tested with 1464 bytes
p = netflow.parse_packet(payload)  # Test result: <ExportPacket v5 with 30 records>
#print(p.flows)  # Test result: 5

for entry in p.flows:
    # prep dict
    tmpEntry = str(entry)
    tmpEntry = tmpEntry[22:-1]
    tmpEntry2 = tmpEntry.replace("'", '"')

    #print(tmpEntry2)



    dictEntry = json.loads(tmpEntry2)
    bigDict[i] = (dictEntry)
    i+=1
    #type(tmpEntry)
    #print(dictEntry)
    #print(tmpEntry.lstrip(20))
    print("----------------")
print(bigDict)
