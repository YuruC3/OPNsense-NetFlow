from scapy.all import *
import struct

# Define NetFlow v5 header and record formats
NETFLOW_V5_HEADER_LEN = 24
NETFLOW_V5_RECORD_LEN = 48

def parse_netflow_v5(packet):
    if not packet.haslayer(UDP):
        return

    udp_payload = bytes(packet[UDP].payload)

    if len(udp_payload) < NETFLOW_V5_HEADER_LEN:
        print("Invalid NetFlow v5 header length")
        return

    # Parse header
    header = struct.unpack('!HHIIIIBBH', udp_payload[:NETFLOW_V5_HEADER_LEN])
    version, count, uptime, unix_secs, unix_nsecs, flow_seq, engine_type, engine_id, sampling = header

    print(f"\n--- NetFlow v5 Packet ---")
    print(f"Version: {version}, Record count: {count}, Sys uptime: {uptime}")
    print(f"Unix secs: {unix_secs}, Flow sequence: {flow_seq}")

    # Parse flow records
    offset = NETFLOW_V5_HEADER_LEN
    for i in range(count):
        if offset + NETFLOW_V5_RECORD_LEN > len(udp_payload):
            print("Incomplete record")
            break

        record = struct.unpack('!IIIHHIIIIHHBBBBHHBBH', udp_payload[offset:offset + NETFLOW_V5_RECORD_LEN])
        src_addr = inet_ntoa(struct.pack('!I', record[0]))
        dst_addr = inet_ntoa(struct.pack('!I', record[1]))
        next_hop = inet_ntoa(struct.pack('!I', record[2]))
        src_port = record[10]
        dst_port = record[11]
        packets = record[4]
        bytes_ = record[5]

        print(f"\nFlow #{i+1}")
        print(f"Src IP: {src_addr}:{src_port} → Dst IP: {dst_addr}:{dst_port}")
        print(f"Next hop: {next_hop}, Packets: {packets}, Bytes: {bytes_}")

        offset += NETFLOW_V5_RECORD_LEN

# Sniff on a given interface or from a pcap file
def start_sniff(interface=None, pcap_file=None):
    if pcap_file:
        packets = rdpcap(pcap_file)
        for pkt in packets:
            parse_netflow_v5(pkt)
    elif interface:
        sniff(iface=interface, filter="udp port 2055", prn=parse_netflow_v5)

# Example usage
if __name__ == "__main__":
    # Provide either an interface or a pcap file
    start_sniff(pcap_file="netflowv5_sample.pcap")
    # start_sniff(interface="eth0")

