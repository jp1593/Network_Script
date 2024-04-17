#Libraries
import scapy.all as scapy
import ifaddr
import time
import socket
import struct

def get_default_gateway_linux():
    # Subnet mask
    adapters = ifaddr.get_adapters()
    for adapter in adapters:
        if adapter.nice_name == "wlp0s20f3":
            for ip in adapter.ips:
                    prefix = ip.network_prefix
                    break

    # Gateway IP
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue
            gateway_ip = socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
            return f"{gateway_ip}/{prefix}"

#Data display
print(get_default_gateway_linux())
start_time = time.time()
result = scapy.arping(get_default_gateway_linux())
end_time = time.time()
scan_duration = end_time - start_time
num_hosts_scanned = len(result[0])
print("\nNumber of hosts scanned:", num_hosts_scanned, "Scan duration: %.2f seconds" % scan_duration)