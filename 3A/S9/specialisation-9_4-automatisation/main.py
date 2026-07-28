"""Projet: Automatisation & Contrôle-Commande Nucléaire
3AS9 - Spécialisation 9_4 - ENSEM NRJ (FISA)
Régulation PID et logique de contrôle pour procédés industriels"""

import numpy as np
import matplotlib.pyplot as plt

class RegulateurPID:
    def __init__(self, Kp=1.0, Ki=0.1, Kd=0.05, setpoint=0, Ts=0.1):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.Ts = Ts
        self.integrale = 0
        self.derniere_erreur = 0
        self.sortie = 0

    def calculer(self, mesure):
        erreur = self.setpoint - mesure
        self.integrale += erreur * self.Ts
        derivee = (erreur - self.derniere_erreur) / self.Ts
        P = self.Kp * erreur
        I = self.Ki * self.integrale
        D = self.Kd * derivee
        self.sortie = P + I + D
        self.derniere_erreur = erreur
        return self.sortie

class ProcedeThermique:
    def __init__(self, tau=10.0, K=1.5, theta=2.0):
        self.tau = tau
        self.K = K
        self.theta = theta
        self.T = 20.0
        self.buffer_entree = [0] * int(theta / 0.1)

    def maj(self, puissance):
        self.buffer_entree.append(puissance)
        P_retardee = self.buffer_entree.pop(0)
        dT = (-self.T + self.K * P_retardee) / self.tau * 0.1
        self.T += dT
        return self.T

class SystemeSecuriteNucleaire:
    Niveaux = ['Normal', 'Surveillance', 'Alarme', 'Urgence']

    def __init__(self):
        self.niveau = 0
        self.temperatures = [30.0] * 5
        self.pression = 1.0
        self.debit_refroidissement = 100.0

    def evaluer(self, T_moy, P, debit):
        self.temperatures = self.temperatures[1:] + [T_moy]
        self.pression = P
        self.debit_refroidissement = debit
        derive_T = self.temperatures[-1] - self.temperatures[-2]
        if T_moy > 350 or P > 70 or derive_T > 10:
            self.niveau = 3  # Urgence
        elif T_moy > 300 or P > 60:
            self.niveau = 2  # Alarme
        elif T_moy > 250:
            self.niveau = 1  # Surveillance
        else:
            self.niveau = 0
        return self.Niveaux[self.niveau], self.action()

    def action(self):
        actions = {
            0: "Aucune",
            1: "Augmenter surveillance capteurs",
            2: f"Réduire puissance à 50%, débit refroidissement → {self.debit_refroidissement*1.3:.0f}",
            3: f"ARRÊT D'URGENCE - Injection bore, débit max {self.debit_refroidissement*2:.0f}"
        }
        return actions[self.niveau]

def main():
    print("=" * 60)
    print("Automatisation & Contrôle-Commande - 9_4")
    print("=" * 60)
    print("\n--- 1. Régulation PID d'un procédé thermique ---")
    pid = RegulateurPID(Kp=2.0, Ki=0.05, Kd=0.1, setpoint=150, Ts=0.1)
    proc = ProcedeThermique(tau=8.0, K=1.8, theta=1.5)
    temps = np.arange(0, 100, 0.1)
    T_hist = []
    cmd_hist = []
    for t in temps:
        cmd = pid.calculer(proc.T)
        T = proc.maj(cmd)
        T_hist.append(T)
        cmd_hist.append(cmd)
    print(f"Température initiale: {T_hist[0]:.1f}°C")
    print(f"Température finale: {T_hist[-1]:.1f}°C (consigne {pid.setpoint}°C)")
    T_regime = np.mean(T_hist[-200:])
    print(f"Erreur statique: {abs(pid.setpoint - T_regime):.2f}°C")
    print(f"Dépassement max: {max(T_hist)-pid.setpoint:.1f}°C")
    print("\n--- 2. Système de Sécurité Nucléaire ---")
    secu = SystemeSecuriteNucleaire()
    scenarios = [(180, 40, 100), (280, 55, 95), (320, 65, 80), (360, 75, 60)]
    for T, P, D in scenarios:
        niveau, action = secu.evaluer(T, P, D)
        print(f"  T={T}°C, P={P}bar, D={D}% → Niveau {niveau}: {action}")

if __name__ == '__main__':
    main()
