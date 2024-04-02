import scapy.all as scapy
import ifaddr
import time
import socket, struct
import os

IP_entered = input(
    "\nEnter the IP addres to analize (ex 192.168.1.0/24): ")

start_time = time.time()
result = scapy.arping(IP_entered)
end_time = time.time()

scan_duration = end_time - start_time
print("\nScan duration: %.2f seconds" % scan_duration)