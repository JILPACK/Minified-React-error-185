"""Projet: P-HIL - Power Hardware-in-the-Loop
3AS9 - Spécialisation 9_10 - ENSEM NRJ (FISA)
Simulation temps réel et validation HIL de systèmes de puissance"""

import numpy as np
import time
import matplotlib.pyplot as plt

class ModeleEmulation:
    def __init__(self, dt=1e-4):
        self.dt = dt
        self.t = 0

    def step(self, u):
        raise NotImplementedError

class ReseauEquivalent(ModeleEmulation):
    def __init__(self, Vg=230, f=50, R=0.5, L=5e-3, dt=1e-4):
        super().__init__(dt)
        self.Vg = Vg
        self.f = f
        self.R = R
        self.L = L
        self.I = 0

    def step(self, V_in):
        Vg_t = self.Vg * np.sin(2 * np.pi * self.f * self.t)
        dI = (Vg_t - V_in - self.R * self.I) / self.L
        self.I += dI * self.dt
        self.t += self.dt
        return self.I

class SimulateurPHIL:
    def __init__(self, modele, HIL_factor=1):
        self.modele = modele
        self.HIL_factor = HIL_factor
        self.I_mesure = 0
        self.V_cmd = 0
        self.retards = []
        self.temps_reel = 0

    def un_pas(self, V_applique):
        debut = time.perf_counter()
        I_sim = self.modele.step(V_applique)
        self.I_mesure = I_sim * self.HIL_factor
        self.V_cmd = self.I_mesure * 10
        fin = time.perf_counter()
        duree = fin - debut
        self.retards.append(duree)
        self.temps_reel += duree
        return self.I_mesure

    def verifier_temps_reel(self):
        retard_max = max(self.retards)
        pas = self.modele.dt
        if retard_max < pas:
            return f"OK: max retard={retard_max*1e6:.1f}us < pas={pas*1e6:.1f}us"
        else:
            return f"WARNING: max retard={retard_max*1e6:.1f}us > pas={pas*1e6:.1f}us"

class FPGAEmulation:
    def __init__(self, n_bits=16):
        self.n_bits = n_bits
        self.max_val = 2**(n_bits-1) - 1
        self.min_val = -2**(n_bits-1)

    def quantifier(self, valeur, echelle=1.0):
        q = int(valeur / echelle * self.max_val)
        q = max(self.min_val, min(self.max_val, q))
        return q

    def dequantifier(self, valeur_quantifiee, echelle=1.0):
        return valeur_quantifiee / self.max_val * echelle

class ScenarioDefaut:
    def __init__(self, type_defaut, t_debut, duree):
        self.type = type_defaut
        self.t_debut = t_debut
        self.duree = duree

    def appliquer(self, t, V, I):
        if self.t_debut <= t <= self.t_debut + self.duree:
            if self.type == 'court-circuit':
                return 0, I * 10
            elif self.type == 'coupure':
                return 0, 0
            elif self.type == 'surtension':
                return V * 1.5, I
        return V, I

def main():
    print("=" * 60)
    print("P-HIL: Power Hardware-in-the-Loop - 9_10")
    print("=" * 60)
    print("\n--- 1. Simulation temps réel du réseau ---")
    reseau = ReseauEquivalent(Vg=230, R=0.5, L=5e-3, dt=1e-4)
    phil = SimulateurPHIL(reseau)
    print(f"Réseau: Vg={reseau.Vg}V, R={reseau.R}Ω, L={reseau.L*1000:.1f}mH")
    print("Simulation de 1000 pas...")
    for i in range(1000):
        phil.un_pas(0)
    print(f"  Courant final: {phil.I_mesure:.3f}A")
    print(f"  {phil.verifier_temps_reel()}")
    print("\n--- 2. Quantification FPGA ---")
    fpga = FPGAEmulation(n_bits=12)
    V_test = 150.0
    V_q = fpga.quantifier(V_test, echelle=230)
    V_dq = fpga.dequantifier(V_q, echelle=230)
    erreur = abs(V_test - V_dq)
    print(f"Tension {V_test}V → quantifié {V_q} → déquantifié {V_dq:.2f}V")
    print(f"Erreur de quantification: {erreur:.4f}V ({(erreur/V_test)*100:.2f}%)")
    print("\n--- 3. Scénarios de défauts ---")
    defauts = [
        ScenarioDefaut('court-circuit', 0.02, 0.005),
        ScenarioDefaut('coupure', 0.05, 0.01),
        ScenarioDefaut('surtension', 0.08, 0.008),
    ]
    print(f"{'Temps (s)':<10} {'V (V)':<10} {'I (A)':<10} {'État':<15}")
    mesh = ReseauEquivalent(dt=1e-4)
    for t in np.arange(0, 0.12, 1e-4):
        I = mesh.step(0)
        V = mesh.Vg * np.sin(2*np.pi*50*t)
        for defaut in defauts:
            V, I = defaut.appliquer(t, V, I)
        if abs(t - round(t, 3)) < 1e-5:
            etat = "Normal" if abs(V - mesh.Vg * np.sin(2*np.pi*50*t)) < 1 else defaut.type
            print(f"{t:<10.3f} {V:<10.1f} {I:<10.3f} {etat:<15}")

if __name__ == '__main__':
    main()
