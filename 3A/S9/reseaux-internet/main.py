"""Projet: Réseaux Internet
3AS9 - ENSEM NRJ (FISA)
Simulation de protocoles réseau (TCP, UDP, routage)"""

import socket
import threading
import time
import struct
import hashlib
import random

class PaquetIP:
    def __init__(self, src, dst, ttl=64, proto='TCP'):
        self.src = src
        self.dst = dst
        self.ttl = ttl
        self.proto = proto
        self.header_len = 20
        self.total_len = 0
        self.checksum = 0

    def encapsuler(self, donnees, id_paquet=0):
        version_ihl = 0x45
        dscp_ecn = 0
        total_len = self.header_len + len(donnees)
        flags_fragment = 0
        header = struct.pack('!BBHHHBBH4s4s',
            version_ihl, dscp_ecn, total_len, id_paquet,
            flags_fragment, self.ttl, 6, 0,
            socket.inet_aton(self.src), socket.inet_aton(self.dst))
        return header + donnees.encode() if isinstance(donnees, str) else header + donnees

class SegmentTCP:
    def __init__(self, src_port, dst_port, seq=0, ack=0):
        self.src_port = src_port
        self.dst_port = dst_port
        self.seq = seq
        self.ack = ack
        self.flags = {'SYN': False, 'ACK': False, 'FIN': False, 'RST': False}
        self.window = 65535

    def set_flags(self, **flags):
        self.flags.update(flags)

    def encapsuler(self, donnees=''):
        offset = 5
        flags_byte = 0
        if self.flags.get('SYN'): flags_byte |= 0x02
        if self.flags.get('ACK'): flags_byte |= 0x10
        if self.flags.get('FIN'): flags_byte |= 0x01
        if self.flags.get('RST'): flags_byte |= 0x04
        header = struct.pack('!HHIIBBHHH',
            self.src_port, self.dst_port, self.seq, self.ack,
            offset << 4, flags_byte, self.window, 0, 0)
        return header + donnees.encode() if isinstance(donnees, str) else header + donnees

class SimulateurReseau:
    def __init__(self):
        self.noeuds = {}
        self.connexions = []

    def ajouter_noeud(self, nom, ip):
        self.noeuds[nom] = {'ip': ip, 'routes': [], 'compteurs': {'tx': 0, 'rx': 0, 'drop': 0}}

    def ajouter_lien(self, n1, n2, delai_ms=10, perte=0.0):
        self.connexions.append({'n1': n1, 'n2': n2, 'delai': delai_ms, 'perte': perte})

    def ajouter_route(self, noeud, destination, next_hop):
        self.noeuds[noeud]['routes'].append((destination, next_hop))

    def trouver_chemin(self, src, dst, visite=None):
        if visite is None: visite = set()
        if src == dst: return [src]
        visite.add(src)
        for conn in self.connexions:
            voisin = None
            if conn['n1'] == src: voisin = conn['n2']
            elif conn['n2'] == src: voisin = conn['n1']
            if voisin and voisin not in visite:
                chemin = self.trouver_chemin(voisin, dst, visite)
                if chemin: return [src] + chemin
        return None

    def transferer_paquet(self, src, dst, donnees):
        chemin = self.trouver_chemin(src, dst)
        if not chemin:
            self.noeuds[src]['compteurs']['drop'] += 1
            return f"PAQUET PERDU: aucun chemin {src}→{dst}"
        delai_total = 0
        for i in range(len(chemin)-1):
            for conn in self.connexions:
                if ((conn['n1'] == chemin[i] and conn['n2'] == chemin[i+1]) or
                    (conn['n2'] == chemin[i] and conn['n1'] == chemin[i+1])):
                    if random.random() < conn['perte']:
                        self.noeuds[chemin[i]]['compteurs']['drop'] += 1
                        return f"PAQUET PERDU sur {chemin[i]}→{chemin[i+1]}"
                    delai_total += conn['delai']
                    break
            self.noeuds[chemin[i]]['compteurs']['tx'] += 1
        self.noeuds[dst]['compteurs']['rx'] += 1
        return f"OK: {chemin}, delai={delai_total}ms, '{donnees}'"

    def handshake_TCP(self, src, dst):
        print(f"\n=== Handshake TCP: {src} → {dst} ===")
        SYN = SegmentTCP(12345, 80, seq=random.randint(0, 10000))
        SYN.set_flags(SYN=True)
        print(f"[1] {src} → {dst}: SYN(seq={SYN.seq})")
        res = self.transferer_paquet(src, dst, SYN.encapsuler("SYN"))
        print(f"    {res}")

        SYN_ACK = SegmentTCP(80, 12345, seq=random.randint(0, 10000), ack=SYN.seq+1)
        SYN_ACK.set_flags(SYN=True, ACK=True)
        print(f"[2] {dst} → {src}: SYN-ACK(seq={SYN_ACK.seq}, ack={SYN_ACK.ack})")
        res = self.transferer_paquet(dst, src, SYN_ACK.encapsuler("SYN-ACK"))
        print(f"    {res}")

        ACK = SegmentTCP(12345, 80, seq=SYN.seq+1, ack=SYN_ACK.seq+1)
        ACK.set_flags(ACK=True)
        print(f"[3] {src} → {dst}: ACK(seq={ACK.seq}, ack={ACK.ack})")
        res = self.transferer_paquet(src, dst, ACK.encapsuler("ACK"))
        print(f"    {res}")
        print("Connexion TCP établie!")

    def afficher_statistiques(self):
        print("\n=== Statistiques réseau ===")
        for nom, noeud in self.noeuds.items():
            c = noeud['compteurs']
            print(f"  {nom} ({noeud['ip']}): TX={c['tx']}, RX={c['rx']}, Perte={c['drop']}")

def simulate_http():
    print("=== Simulation HTTP simple ===")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)
    try:
        client.connect(("example.com", 80))
        client.send(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
        reponse = client.recv(4096)
        print(f"HTTP Response ({len(reponse)} octets):")
        print(reponse.decode('utf-8', errors='ignore')[:300])
    except Exception as e:
        print(f"Erreur HTTP: {e}")
    finally:
        client.close()

def main():
    print("=" * 60)
    print("Réseaux Internet - Simulation de protocoles")
    print("=" * 60)
    sim = SimulateurReseau()
    sim.ajouter_noeud("Client", "192.168.1.10")
    sim.ajouter_noeud("Routeur_A", "10.0.0.1")
    sim.ajouter_noeud("Routeur_B", "10.0.0.2")
    sim.ajouter_noeud("Serveur", "93.184.216.34")
    sim.ajouter_lien("Client", "Routeur_A", delai_ms=5, perte=0.0)
    sim.ajouter_lien("Routeur_A", "Routeur_B", delai_ms=20, perte=0.01)
    sim.ajouter_lien("Routeur_B", "Serveur", delai_ms=10, perte=0.0)
    sim.ajouter_route("Routeur_A", "93.184.216.34", "Routeur_B")
    sim.ajouter_route("Routeur_B", "192.168.1.10", "Routeur_A")
    print("\nTopologie: Client ←5ms→ Routeur_A ←20ms/1%→ Routeur_B ←10ms→ Serveur")
    sim.handshake_TCP("Client", "Serveur")
    for i in range(5):
        msg = f"Paquet de donnees #{i+1}"
        res = sim.transferer_paquet("Client", "Serveur", msg)
        print(f"  Transfert {i+1}: {res}")
    sim.afficher_statistiques()

if __name__ == '__main__':
    main()
