"""Projet: Automatismes industriels - Commande et Supervision
2AS8 - ENSEM NRJ (FISA)
Simulation d'automate programmable (API), régulation et IHM"""

import numpy as np
import time

class API:
    def __init__(self, nom, cycle_ms=100):
        self.nom = nom
        self.cycle_ms = cycle_ms
        self.entrees = {}
        self.sorties = {}
        self.memories = {}
        self.timers = {}
        self.compteurs = {}
        self.programme = []
        self.en_marche = False

    def ajouter_entree(self, nom, valeur=False):
        self.entrees[nom] = valeur

    def ajouter_sortie(self, nom, valeur=False):
        self.sorties[nom] = valeur

    def ecrire_sortie(self, nom, valeur):
        if nom in self.sorties:
            self.sorties[nom] = bool(valeur)
            print(f"  [API {self.nom}] Sortie {nom} = {self.sorties[nom]}")

    def lire_entree(self, nom):
        return self.entrees.get(nom, False)

    def temporisation(self, nom, preset_ms, reset=False):
        if reset:
            self.timers[nom] = 0
        t = self.timers.get(nom, 0)
        if t < preset_ms:
            self.timers[nom] = t + self.cycle_ms
            return False
        return True

    def compter(self, nom, incrementer=False, decrementer=False, reset=False):
        c = self.compteurs.get(nom, 0)
        if reset: c = 0
        elif incrementer: c += 1
        elif decrementer: c -= 1
        self.compteurs[nom] = c
        return c

    def ajouter_reseau(self, description, logique):
        self.programme.append({'desc': description, 'logique': logique})

    def executer_cycle(self):
        for reseau in self.programme:
            reseau['logique']()

class RegulationPID:
    def __init__(self, Kp=1.0, Ki=0.2, Kd=0.05, SP=50, Ts=1.0):
        self.Kp = Kp; self.Ki = Ki; self.Kd = Kd
        self.SP = SP; self.Ts = Ts
        self.I = 0; self.e_prev = 0; self.MV = 0

    def calculer(self, PV):
        e = self.SP - PV
        self.I += e * self.Ts
        D = (e - self.e_prev) / self.Ts if self.Ts > 0 else 0
        P = self.Kp * e; I = self.Ki * self.I; D = self.Kd * D
        self.MV = P + I + D
        self.e_prev = e
        return np.clip(self.MV, 0, 100)

class SuperviseurSCADA:
    def __init__(self):
        self.variables = {}
        self.alarmes = []
        self.historique = []
        self.log = []

    def ajouter_variable(self, nom, valeur=0, min_v=0, max_v=100, unite=''):
        self.variables[nom] = {'valeur': valeur, 'min': min_v, 'max': max_v, 'unite': unite}

    def mettre_a_jour(self, nom, valeur):
        if nom in self.variables:
            v = self.variables[nom]
            v['valeur'] = valeur
            self.historique.append((nom, valeur, time.time()))
            if valeur < v['min'] or valeur > v['max']:
                self.alarmes.append(f"ALARME: {nom} = {valeur}{v['unite']} (hors plage)")
                self.log.append(f"[{time.strftime('%H:%M:%S')}] ALARME {nom}")

    def afficher_synoptique(self):
        print(f"\n=== SYNOPTIQUE - {len(self.variables)} points ===")
        for nom, v in self.variables.items():
            barre = '█' * int(v['valeur'] / v['max'] * 20)
            etat = '⚠' if (v['valeur'] < v['min'] or v['valeur'] > v['max']) else '✓'
            print(f"  {etat} {nom:<20} {v['valeur']:8.1f} {v['unite']:<5} {barre}")

class ProcedeIndustriel:
    def __init__(self, tau=5.0, K=1.0):
        self.tau = tau
        self.K = K
        self.PV = 20.0
        self.bruit = 0.0

    def step(self, MV):
        dPV = (-self.PV + self.K * MV) / self.tau
        self.PV += dPV
        self.PV += np.random.randn() * self.bruit
        return self.PV

def main():
    print("=" * 60)
    print("Automatismes industriels - Commande et Supervision")
    print("2AS8 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Automate programmable (API) - Gestion cuve ---")
    api = API("CUVE-01", cycle_ms=100)
    api.ajouter_entree("Capteur_Haut", False)
    api.ajouter_entree("Capteur_Bas", True)
    api.ajouter_entree("BP_Démarrage", False)
    api.sorties["Vanne_Remplissage"] = False
    api.sorties["Pompe_Vidange"] = False
    api.sorties["Vanne_Chauffage"] = False
    api.ajouter_sortie("Alarme", False)

    niveau = 20
    def logique_cuve():
        nonlocal niveau
        bp = api.lire_entree("BP_Démarrage")
        if bp:
            if niveau < 80 and not api.sorties["Pompe_Vidange"]:
                api.ecrire_sortie("Vanne_Remplissage", True)
                niveau = min(100, niveau + 2)
            if niveau >= 80:
                api.ecrire_sortie("Vanne_Remplissage", False)
                api.ecrire_sortie("Vanne_Chauffage", True)
    api.ajouter_reseau("Contrôle niveau cuve", logique_cuve)

    print("Simulation cuve API (3 cycles):")
    for c in range(3):
        api.entrees["BP_Démarrage"] = (c == 0)
        api.executer_cycle()
        print(f"  Cycle {c+1}: niveau={niveau}%")

    print("\n--- 2. Régulation PID d'un échangeur ---")
    pid = RegulationPID(Kp=2.0, Ki=0.15, Kd=0.3, SP=60, Ts=0.5)
    proc = ProcedeIndustriel(tau=4.0, K=1.5)
    proc.bruit = 0.1
    print(f"{'t(s)':<8} {'PV':<8} {'MV':<8}")
    for t in np.arange(0, 30, 0.5):
        MV = pid.calculer(proc.PV)
        PV = proc.step(MV)
        if t % 5 < 0.5:
            print(f"{t:<8.1f} {PV:<8.1f} {MV:<8.1f}")

    print("\n--- 3. Supervision SCADA ---")
    scada = SuperviseurSCADA()
    scada.ajouter_variable("Température réacteur", 185, min_v=150, max_v=250, unite='°C')
    scada.ajouter_variable("Pression cuve", 12.5, min_v=0, max_v=20, unite='bar')
    scada.ajouter_variable("Débit alimentation", 85, min_v=30, max_v=120, unite='m3/h')
    scada.ajouter_variable("Niveau ballon", 65, min_v=20, max_v=90, unite='%')
    scada.mettre_a_jour("Température réacteur", 192)
    scada.mettre_a_jour("Pression cuve", 15.2)
    scada.mettre_a_jour("Débit alimentation", 78)
    scada.mettre_a_jour("Niveau ballon", 62)
    scada.afficher_synoptique()
    for alarme in scada.alarmes[-3:]:
        print(f"  {alarme}")

if __name__ == '__main__':
    main()
