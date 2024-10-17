import csv
import time
from scapy.all import sniff, IP  # Importation de IP pour les paquets réseau
from SniffnDetect.sniffndetect import SniffnDetect

def detect_attacks():
    # Initialiser l'objet SniffnDetect
    detector = SniffnDetect()

    # Fonction de callback pour traiter chaque paquet capturé
    def process_packet(packet):
        try:
            # Utiliser la méthode analyze_packet pour analyser le paquet
            detector.analyze_packet(packet)
            attack_type = detector.RECENT_ACTIVITIES[-1][-1]  # Récupérer le type d'attaque
            if attack_type:
                # Enregistrer l'attaque détectée
                with open('detected_attacks.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([time.time(), packet[IP].src, attack_type])  # Utiliser IP pour l'adresse source
                    print(f"Attack detected from {packet[IP].src}: {attack_type}")
        except Exception as e:
            print(f"Erreur lors du traitement du paquet : {e}")

    # Utiliser Scapy pour capturer les paquets en temps réel
    sniff(prn=process_packet)

if __name__ == "__main__":
    detect_attacks()
