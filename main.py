from scapy.all import ARP, Ether, srp
import keyboard, socket, ipaddress, pyvis
from pyvis.network import Network

class Appareil :
    
    def __init__(self, ip, mac):
        self.ip = ip
        self.mac = mac
        self.portsOpen = []
        self.couleur = None
        self.type = []
        
    def ajouterPort(self, port):
        self.portsOpen.append(port)
        
    def definirType(self, type):
        self.type.append(type)
    
    def sortirAppareil(self):
        print(f"\nIP: {self.ip} | MAC: {self.mac} | Type : {', '.join(self.type)}")

listeAppareils = []

def arp_scan(cidr):
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=cidr) # crée un trame ethernet avec tout le monde, ARP crée des paquet ARP pour demandé qui possède l'adresse ip correspondant à cidr
    answered, _ = srp(pkt, timeout=3) # srp envoie le paquet et écoute les réponses pendant 3 secondes. Retourne deux listes : (answered, unanswered)
    return [{"ip": r.psrc, "mac": r.hwsrc} for _, r in answered] # _ => correspond au paquet envoyé donc on s'en préoccupe pas

# Pour récupérer l'adresse ip 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INET => IPv4, DGRAM => UDP type de connexion
sock.connect(("8.8.8.8", 80)) # C'est une astuce pour forcer l'OS à nous dire quelle interface il utiliserait — sans jamais envoyer un seul paquet !
ip = sock.getsockname()[0]
print(f"IP détectée : {ip}")
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
    app = Appareil(device['ip'], device['mac'])
    for i in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP et non udp
        s.settimeout(0.1)
        result = s.connect_ex((device['ip'], i))
        s.close()
        if result == 0:
            app.ajouterPort(i)

    if 22 in app.portsOpen:
            app.definirType("Linux / Mac (SSH)")
    if 3389 in app.portsOpen or 445 in app.portsOpen:
            app.definirType("Windows")
    if 80 in app.portsOpen or 443 in app.portsOpen:
            app.definirType("routeur ou serveur web")
    if 5900 in app.portsOpen:
            app.definirType("VNC")
    if 62078 in app.portsOpen:
            app.definirType("iPhone")
    
    listeAppareils.append(app)
    
for app in listeAppareils:
    app.sortirAppareil()
    
gateway = str(list(ipaddress.ip_network(str(ipc.network)).hosts())[-1])

net = Network(height="100vh", width="100%", bgcolor="#0a0e1a", font_color="white")

net.add_node(gateway, label=f"🌐 Routeur\n{gateway}", color="#00ff9f", size=30)

couleurs = {
    "Linux / Mac (SSH)": "#fd79a8",
    "Windows": "#74b9ff",
    "routeur ou serveur web": "#00ff9f",
    "VNC": "#a29bfe",
    "iPhone": "#fdcb6e",
}

for app in listeAppareils:
    if not app.type:
        continue
    type_label = ", ".join(app.type)
    couleur = couleurs.get(app.type[0], "#636e72")
    label = f"{type_label}\n{app.ip}\n{app.mac}"
    net.add_node(app.ip, label=label, color=couleur, size=20)
    net.add_edge(gateway, app.ip)

net.show("map.html", notebook=False)