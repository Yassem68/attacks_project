from scapy.all import *

packet= IP(dst"8.8.8.8")/ICMP()
packet.show()