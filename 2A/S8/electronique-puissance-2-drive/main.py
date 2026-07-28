"""Projet: Électronique de puissance 2 et Drive
2AS8 - ENSEM NRJ (FISA)
Convertisseurs DC/DC, onduleurs MLI, commande de moteurs"""

import numpy as np
import matplotlib.pyplot as plt

class HacheurBuck:
    def __init__(self, Vin=48, Vout=12, L=100e-6, C=470e-6, f=50000):
        self.Vin = Vin
        self.Vout = Vout
        self.L = L
        self.C = C
        self.f = f
        self.T = 1 / f
        self.D = Vout / Vin  # Rapport cyclique

    def calculer_ondulation(self, Iout=10):
        dIL = (self.Vin - self.Vout) * self.D / (self.L * self.f)
        dVout = dIL / (8 * self.C * self.f)
        return dIL, dVout

    def simuler(self, duree_ms=2):
        t = np.linspace(0, duree_ms*1e-3, 1000)
        dt = t[1] - t[0]
        IL, Vout = 0, 0
        IL_hist, Vout_hist = [], []
        for ti in t:
            phase = (ti % self.T) / self.T
            if phase < self.D:
                IL += (self.Vin - Vout) / self.L * dt
            else:
                IL += -Vout / self.L * dt
            Vout += (IL - Vout/5) / self.C * dt
            IL_hist.append(IL); Vout_hist.append(Vout)
        return np.array(t)*1000, np.array(IL_hist), np.array(Vout_hist)

class OnduleurMLI:
    def __init__(self, Vdc=560, f_sortie=50, f_mli=2000, m=0.85):
        self.Vdc = Vdc
        self.f = f_sortie
        self.f_mli = f_mli
        self.m = m  # Indice de modulation
        self.omega = 2 * np.pi * f_sortie

    def tension_fondamentale(self):
        V1 = self.m * self.Vdc / 2
        return V1

    def simuler_mli(self, duree_ms=40):
        t = np.linspace(0, duree_ms*1e-3, 5000)
        dt = t[1] - t[0]
        V_ref = self.m * self.Vdc/2 * np.sin(self.omega * t)
        V_porteuse = self.Vdc/2 * (2 * ((self.f_mli * t) % 1) - 1)
        V_sortie = np.where(V_ref > V_porteuse, self.Vdc/2, -self.Vdc/2)
        return t*1000, V_ref, V_porteuse, V_sortie

    def THD(self, V_sortie, f_max=5000):
        N = len(V_sortie)
        Y = np.fft.fft(V_sortie - np.mean(V_sortie))
        freq = np.fft.fftfreq(N, d=1/(self.f_mli*2))
        mask = (freq > 0) & (freq < f_max)
        harm = np.abs(Y[mask])**2
        f_harm = freq[mask]
        f1 = 50
        idx_f1 = np.argmin(np.abs(f_harm - f1))
        V1 = np.abs(Y[mask])[idx_f1] if idx_f1 < len(harm) else 1
        return np.sqrt(np.sum(harm) - V1**2) / V1 if V1 > 0 else 0

class VariateurVitesse:
    def __init__(self, Pnom=7.5e3, Vnom=400, Inom=15, fnom=50):
        self.Pnom = Pnom
        self.Vnom = Vnom
        self.Inom = Inom
        self.fnom = fnom
        self.Vdc = Vnom * np.sqrt(2) * 1.1

    def loi_U_f(self, f):
        if f <= self.fnom:
            V = self.Vnom * f / self.fnom
        else:
            V = self.Vnom
        return V

    def couple_max(self, f):
        V = self.loi_U_f(f)
        return 3 * (V / (2*np.pi*f))**2 / (2 * np.pi * 60 * 0.05)

class RedresseurMLI:
    def __init__(self, V_reseau=400, L_filtre=5e-3):
        self.V_reseau = V_reseau
        self.L = L_filtre
        self.Vdc_ref = 650

    def facteur_puissance(self, I_fond, I_harm):
        return I_fond / np.sqrt(I_fond**2 + I_harm**2)

def main():
    print("=" * 60)
    print("Électronique de puissance 2 et Drive")
    print("2AS8 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Hacheur Buck (DC/DC) ---")
    buck = HacheurBuck(Vin=48, Vout=12, L=150e-6, f=100000)
    D = buck.D
    dIL, dVout = buck.calculer_ondulation(Iout=8)
    print(f"Rapport cyclique: {D:.2%}")
    print(f"Ondulation courant: {dIL:.2f} A")
    print(f"Ondulation tension: {dVout*1000:.1f} mV")
    t, IL, Vout = buck.simuler(duree_ms=1)
    print(f" Tension sortie moyenne: {np.mean(Vout[200:]):.2f} V")
    print(f" Courant inductance moyen: {np.mean(IL[200:]):.2f} A")

    print("\n--- 2. Onduleur MLI triphasé ---")
    onduleur = OnduleurMLI(Vdc=560, f_sortie=50, f_mli=2000, m=0.85)
    V1 = onduleur.tension_fondamentale()
    print(f"Tension fondamentale: {V1:.1f} V")
    print(f"Tension composée efficace: {V1*np.sqrt(3)/np.sqrt(2):.0f} V")
    t_mli, V_ref, V_port, V_sort = onduleur.simuler_mli(40)
    # Visualiser quelques périodes
    fenetre = 500
    thd = onduleur.THD(V_sort)
    print(f"THD tension: {thd:.2%}")

    print("\n--- 3. Variateur de vitesse (loi U/f) ---")
    var = VariateurVitesse(Pnom=7.5e3)
    print(f"{'f (Hz)':<10} {'V (V)':<10} {'C max (Nm)':<12}")
    for f in [10, 25, 50, 60]:
        V = var.loi_U_f(f)
        print(f"{f:<10} {V:<10.0f}")

    print("\n--- 4. Redresseur à MLI ---")
    red = RedresseurMLI(V_reseau=400)
    FP = red.facteur_puissance(100, 15)
    print(f"Facteur de puissance: {FP:.3f}")
    print(f"Tension bus DC: {red.Vdc_ref:.0f} V")

if __name__ == '__main__':
    main()
