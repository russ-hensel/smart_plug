# -*- coding: utf-8 -*-



"""
Simple Network Scanner with Python and Scapy - Maksym Postument - Medium
    *>url  https://medium.com/@777rip777/simple-network-scanner-with-python-and-scapy-802645073190


RuntimeError: Sniffing and sending packets is not available at layer 2: winpcap is not installed. You may use conf.L3socket orconf.L3socket6 to access layer 3


----------- or look at

Using python nmap to scan subnet. Any way to speed it up? : Python
    *>url  https://www.reddit.com/r/Python/comments/9v1fwy/using_python_nmap_to_scan_subnet_any_way_to_speed/

---- best??
lanscan · PyPI
    *>url  https://pypi.org/project/lanscan/


"""

import scapy.all as scapy
import argparse
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target",
                        help="Target IP/IP Range")
    options = parser.parse_args()
    return options
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1,
                              verbose=False)[0]
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list
def print_result(results_list):
    print("IP\t\t\tMAC Address")
    print("----------------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])
options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)