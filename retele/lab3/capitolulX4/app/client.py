import sys
import time
from scapy.all import IP, UDP, Raw, send

if len(sys.argv) != 2:
    print("Utilizare: python client.py <adresa_server>")
    sys.exit(1)

SERVER_IP = sys.argv[1]
SERVER_PORT = 9999
MESSAGE = "Salut de la George"

time.sleep(5)

try:
    packet = IP(dst=SERVER_IP) / UDP(dport=SERVER_PORT, sport=12345) / Raw(load=MESSAGE)

    print(f"Trimit pachet UDP către {SERVER_IP}:{SERVER_PORT}...")
    send(packet, verbose=0)
    print("Pachet trimis.")

except Exception as e:
    print(f"Eroare la trimiterea pachetului: {e}")