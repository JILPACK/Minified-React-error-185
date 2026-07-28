"""Projet: Informatique industrielle
2AS7 - ENSEM NRJ (FISA)
Programmation temps reel, communication, acquisition, supervision"""

import time
import random
import threading
import numpy as np

class TaskTempsReel:
    def __init__(self, nom, periode, priorite=1):
        self.nom = nom
        self.periode = periode
        self.priorite = priorite
        self.deadline = 0
        self.executions = 0
        self.duree_moy = 0

    def executer(self, duree):
        debut = time.time()
        time.sleep(duree)
        self.executions += 1
        d = time.time() - debut
        self.duree_moy = (self.duree_moy*(self.executions-1) + d) / self.executions
        return d

class OrdonnanceurTempsReel:
    def __init__(self):
        self.taches = []

    def ajouter(self, tache):
        self.taches.append(tache)

    def ordonnancement_RM(self):
        return sorted(self.taches, key=lambda t: t.periode)

    def ordonnancement_EDF(self, temps):
        return sorted(self.taches, key=lambda t: t.deadline)

    def test_ordonnanabilite_RM(self):
        n = len(self.taches)
        U = sum(t.duree_moy / t.periode for t in self.taches)
        seuil = n * (2**(1/n) - 1)
        return U <= seuil, U, seuil

class CommunicationSerie:
    def __init__(self, baud=9600, data_bits=8, parity='N', stop=1):
        self.baud = baud
        self.bit_time = 1 / baud
        self.frame_bits = data_bits + (1 if parity != 'N' else 0) + stop + 1

    def temps_transmission(self, octets):
        return octets * self.frame_bits * self.bit_time

    def debit_theorique(self, octets):
        return octets / self.temps_transmission(octets)

class AcquisitionAnalogique:
    def __init__(self, can_bits=12, V_ref=10):
        self.N = 2**can_bits
        self.V_ref = V_ref
        self.q = V_ref / self.N

    def numeriser(self, V):
        return int(V / self.q)

    def tension(self, code):
        return code * self.q

class LogicateurAPI:
    def __init__(self, nom):
        self.nom = nom
        self.I = {}
        self.Q = {}
        self.M = {}
        self.T = {}
        self.C = {}

    def ecrire_entree(self, nom, val):
        self.I[nom] = bool(val)

    def lire_sortie(self, nom):
        return self.Q.get(nom, False)

    def set_M(self, nom, val):
        self.M[nom] = bool(val)

    def get_M(self, nom):
        return self.M.get(nom, False)

    def timer(self, nom, preset, reset=False):
        if reset:
            self.T[nom] = 0
            return False
        self.T[nom] = self.T.get(nom, 0) + 1
        return self.T[nom] >= preset

    def cycle(self):
        pass

def main():
    print("=" * 60)
    print("Informatique industrielle")
    print("2AS7 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Ordonnancement temps reel ---")
    ordonn = OrdonnanceurTempsReel()
    t1 = TaskTempsReel("Acquisition", 0.1, 1)
    t1.duree_moy = 0.02
    t2 = TaskTempsReel("Regulation", 0.2, 2)
    t2.duree_moy = 0.03
    t3 = TaskTempsReel("Communication", 0.5, 3)
    t3.duree_moy = 0.05
    ordonn.ajouter(t1); ordonn.ajouter(t2); ordonn.ajouter(t3)
    ok, U, seuil = ordonn.test_ordonnanabilite_RM()
    print(f"Taches:")
    for t in [t1, t2, t3]:
        print(f"  {t.nom}: periode={t.periode}s, WCET={t.duree_moy:.3f}s")
    print(f"Utilisation CPU: U={U:.3f}, seuil={seuil:.3f}")
    print(f" Ordonnanable RM: {'OUI' if ok else 'NON'}")

    print("\n--- 2. Laison serie (RS-232/485) ---")
    com = CommunicationSerie(baud=115200)
    for octets in [1, 10, 100, 1000]:
        print(f"  {octets} octets: {com.temps_transmission(octets)*1000:.2f} ms")

    print("\n--- 3. Acquisition analogique (CAN) ---")
    can = AcquisitionAnalogique(can_bits=12, V_ref=10)
    print(f"CAN {can.N} niveaux (12 bits), q={can.q*1000:.2f} mV")
    for V in [0, 2.5, 5, 7.5, 10]:
        code = can.numeriser(V)
        V_r = can.tension(code)
        print(f"  V={V:.1f}V -> code={code:4d} -> V_numerisee={V_r:.3f}V")

    print("\n--- 4. Automate programmable (API) ---")
    api = LogicateurAPI("API-MOTEUR")
    api.ecrire_entree("BP_START", True)
    api.ecrire_entree("CAPTEUR_TEMP", False)
    api.Q["MOTEUR"] = api.I["BP_START"] and not api.I["CAPTEUR_TEMP"]
    print(f"API {api.nom}")
    print(f"  BP_START={api.I['BP_START']}, CAPTEUR_TEMP={api.I['CAPTEUR_TEMP']}")
    print(f"  MOTEUR={api.Q['MOTEUR']}")

    print("\n--- 5. Supervision et monitoring ---")
    print(f"{'Temps':<12} {'Capteur1':<10} {'Capteur2':<10} {'Alarme':<10}")
    for k in range(10):
        temps = k * 0.5
        c1 = 20 + 5*np.sin(temps) + random.uniform(-0.5, 0.5)
        c2 = 100 + 10*np.cos(temps*0.7) + random.uniform(-2, 2)
        alarme = 'OUI' if c1 > 25 or c2 > 110 else '---'
        if k % 3 == 0:
            print(f"  {temps:<8.1f}s  {c1:<9.1f} {c2:<9.1f} {alarme:<10}")
    print("  (Systeme supervise sur 5s)")

if __name__ == '__main__':
    main()
