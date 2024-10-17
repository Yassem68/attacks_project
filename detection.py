import csv
import time
from SniffnDetect.sniffndetect import SniffnDetect

def detect_attacks(interface):
    detector = SniffnDetect(interface)
    
    # Ouvrir le fichier CSV pour enregistrer les attaques détectées
    with open('detected_attacks.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Source IP", "Attack Type"])
        
        for packet in detector.sniff_packets():
            attack_type = detector.detect_attack(packet)
            if attack_type:
                # Enregistre l'attaque détectée avec l'IP source et le type d'attaque
                writer.writerow([time.time(), packet[0].src, attack_type])
                print(f"Attack detected from {packet[0].src}: {attack_type}")

if __name__ == "__main__":
    # Indiquer l'interface réseau sur laquelle surveiller (ex: "eth0", "wlan0")
    interface = "eth0"
    detect_attacks(interface)
