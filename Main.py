from scapy.all import *

while True:
    netflow = NetflowHeader()/NetflowHeaderV5(count=1)/NetflowRecordV5(dst="172.20.240.2")
    pkt = Ether()/IP()/UDP()/netflow

    print(pkt)

    UDP.payload_guess = [({}, NetflowHeader)] 
    pkts = sniff(iface="VIP-NET")

    print(netflow)



print(netflow)
print(pkts)
