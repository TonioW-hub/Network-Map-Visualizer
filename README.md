# Network Map Visualizer

Scanne ton réseau local et génère une carte interactive des appareils connectés, avec identification automatique du type d'appareil et code couleur.

## Aperçu

Le script découvre toutes les machines actives sur ton réseau local, scanne leurs ports ouverts, déduit leur type, et génère un fichier `map.html` — un graphe interactif navigable dans le navigateur.

## Fonctionnalités

- Découverte des appareils via scan ARP (scapy)
- Scan des ports ouverts sur chaque appareil
- Identification automatique du type d'appareil selon les ports
- Carte interactive générée en HTML (pyvis) avec couleurs par type
- Fonctionne sur tout réseau local en /24

## Identification des appareils

| Port ouvert | Type détecté | Couleur |
|-------------|--------------|---------|
| 22 | Linux / Mac (SSH) | Rose |
| 3389 ou 445 | Windows | Bleu |
| 80 ou 443 | Routeur / Serveur web | Vert |
| 5900 | VNC | Violet |
| 62078 | iPhone | Jaune |

## Installation

```bash
git clone https://github.com/ton-repo/network-map-visualizer
cd network-map-visualizer
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

Générer le `requirements.txt` depuis le venv :

```bash
pip freeze > requirements.txt
```

Sur **Windows**, installer aussi Npcap (obligatoire pour scapy) : https://npcap.com/#download  
Cocher *"Install Npcap in WinPcap API-compatible Mode"* pendant l'installation.

## Utilisation

Lancer en **administrateur** (obligatoire pour le scan ARP) :

```bash
python main.py
```

Le fichier `map.html` s'ouvre automatiquement dans le navigateur.

## Structure du projet

```
network-map-visualizer/
├── main.py            # Script principal
├── requirements.txt   # Dépendances
└── README.md
```

## Avertissement

Cet outil est destiné à un usage **éducatif et personnel** sur ton propre réseau.
Scanner un réseau sans autorisation est illégal.