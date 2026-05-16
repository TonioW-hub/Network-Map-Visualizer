from scapy.all import ARP, Ether, srp
import keyboard, socket, ipaddress

def arp_scan(cidr):
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=cidr) # crée un trame ethernet avec tout le monde, ARP crée des paquet ARP pour demandé qui possède l'adresse ip correspondant à cidr
    answered, _ = srp(pkt, timeout=3) # srp envoie le paquet et écoute les réponses pendant 3 secondes. Retourne deux listes : (answered, unanswered)
    return [{"ip": r.psrc, "mac": r.hwsrc} for _, r in answered] # _ correspond au paquet envoyé donc on s'en fout

# Pour récupérer l'adresse ip 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INET => IPv4, DGRAM => UDP type de connexion
sock.connect(("8.8.8.8", 80)) # C'est une astuce pour forcer l'OS à nous dire quelle interface il utiliserait — sans jamais envoyer un seul paquet !
ip = sock.getsockname()[0]
sock.close()
ipc = ipaddress.ip_interface(f"{ip}/24") # pour concatèner l'IP

ports = [22, 80, 443, 445, 3389, 8080]

"""
port 22 ouvert   →  Linux / Mac (SSH)
port 3389 ouvert →  Windows (Bureau à distance)
port 80/443      →  routeur ou serveur web
port 5900        →  VNC
port 62078       →  iPhone
"""

a = arp_scan(str(ipc.network)) # ipc.network → 192.168.1.0/24 (l'adresse du réseau entier)
for device in a:
    print(f"\nIP: {device['ip']} | MAC: {device['mac']}")
    for i in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP et non udp
        s.settimeout(0.1)
        result = s.connect_ex((device['ip'], i))
        s.close()
        if result == 0:
            print(f"Port {i} ouvert")