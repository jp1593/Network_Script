#Libraries
import ifaddr
import time
import socket
import struct
import subprocess

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

def scan_network(gateway, subnet_prefix):
  #Variables & subproces - nmap
  start_time = time.time()
  command = ["nmap", "-v", "-sn", "-oG", "-", f"{gateway}/{subnet_prefix}"]
  process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
  scan_output = process.communicate()[0].decode("utf-8")
  end_time = time.time()
  scan_duration = end_time - start_time
  host_count = 0

  #Loop for hosts scanned
  for line in scan_output.splitlines():
      if "Starting Nmap" in line or not line.strip():
          continue
      if line.split()[1] != "Nmap" and line.split()[4] != "Down" and line.split()[1] != "Ports":
          host_count += 1
          print("Name: " + line.split()[2] + " IP: " + line.split()[1] + " Status: " + line.split()[4])
  print(f"\nNumber of hosts: {host_count} Scan duration: {scan_duration:.2f} seconds")  # Print scan duration

#Data display & functions call
print("Scanning network: " + get_default_gateway_linux() + "\n")
gateway = get_default_gateway_linux()
scan_network(gateway.split("/")[0], gateway.split("/")[1])

