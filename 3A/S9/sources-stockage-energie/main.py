"""Projet: Sources et moyens de stockage de l'énergie électrique
3AS9 - ENSEM NRJ (FISA)
Modélisation de systèmes PV-Batterie avec simulateur temporel"""

import numpy as np
import matplotlib.pyplot as plt

class CellulePV:
    def __init__(self, Isc=8.21, Voc=0.72, Ns=60, T_ref=25):
        self.Isc = Isc
        self.Voc = Voc
        self.Ns = Ns
        self.T_ref = T_ref
        self.q = 1.602e-19
        self.k = 1.381e-23
        self.n = 1.3

    def courant(self, V, G=1000, T=25):
        Vth = self.Ns * self.n * self.k * (T + 273) / self.q
        Iph = self.Isc * G / 1000 * (1 + 0.0005 * (T - self.T_ref))
        I0 = 1e-10
        I = Iph - I0 * (np.exp(V / Vth) - 1) - V / (1000 * self.Ns)
        return max(I, 0)

    def puissance_max(self, G=1000, T=25):
        Vs = np.linspace(0, self.Ns * self.Voc * 0.8, 100)
        Is = np.array([self.courant(v, G, T) for v in Vs])
        Ps = Vs * Is
        idx_max = np.argmax(Ps)
        return Vs[idx_max], Is[idx_max], Ps[idx_max]

class BatterieLiion:
    def __init__(self, Cnom=100, Vnom=3.7, SOC_init=0.5):
        self.Cnom = Cnom             # Capacité nominale [Ah]
        self.Vnom = Vnom             # Tension nominale [V]
        self.SOC = SOC_init          # State of Charge
        self.R0 = 0.05               # Résistance interne [Ohm]
        self.Enom = Cnom * Vnom / 1000  # Energie nominale [kWh]

    def tension(self):
        return self.Vnom * (0.8 + 0.4 * self.SOC - 0.2 * self.SOC**2)

    def courant_max(self, duree_h):
        return self.Cnom / duree_h

    def simuler_cycle(self, I, dt_h):
        self.SOC -= I * dt_h / self.Cnom
        self.SOC = np.clip(self.SOC, 0, 1)
        V = self.tension() - I * self.R0
        P = V * I
        return V, P

class SystemeStockagePV:
    def __init__(self, Ppv_kwc=3, Cbat_kwh=10, Pbat_kw=5):
        self.Ppv_kwc = Ppv_kwc
        self.batterie = BatterieLiion(Cnom=Cbat_kwh*1000/48, Vnom=48)
        self.Pbat_kw = Pbat_kw
        self.historique = []

    def simuler_jour(self, G_Wh_m2, conso_kwh, pas_h=0.25):
        n_pas = int(24 / pas_h)
        bilan = {'prod': 0, 'conso': 0, 'grid_in': 0, 'grid_out': 0}
        for h in np.arange(0, 24, pas_h):
            idx = int(h / pas_h) % len(G_Wh_m2)
            G = G_Wh_m2[idx]
            prod = self.Ppv_kwc * G / 1000 * pas_h
            conso = conso_kwh * (0.05 + 0.95 * np.exp(-0.5*((h-19)/4)**2)) / (24/pas_h)
            delta = prod - conso
            if delta > 0:
                exc_charge = min(delta, (1 - self.batterie.SOC) * self.batterie.Enom / pas_h)
                self.batterie.SOC += exc_charge / self.batterie.Enom * pas_h
                bilan['grid_out'] += delta - exc_charge
            else:
                dispo = min(-delta, self.batterie.SOC * self.batterie.Enom / pas_h, self.Pbat_kw * pas_h)
                self.batterie.SOC -= dispo / self.batterie.Enom * pas_h
                bilan['grid_in'] += -delta - dispo
            bilan['prod'] += prod
            bilan['conso'] += conso
            self.historique.append((h, prod, conso, self.batterie.SOC))
        return bilan

def main():
    print("=" * 60)
    print("Sources et stockage - Simulation PV + Batterie")
    print("=" * 60)

    cel = CellulePV(Isc=8.21, Voc=0.72)
    Vmp, Imp, Pmax = cel.puissance_max(G=800, T=35)
    print(f"\nCellule PV (G=800, T=35°C): Vmp={Vmp:.2f}V, Imp={Imp:.2f}A, Pmax={Pmax:.2f}W")

    bat = BatterieLiion(Cnom=100, Vnom=3.7)
    print(f"Batterie Li-ion: {bat.Enom:.2f}kWh, SOC initiale={bat.SOC:.0%}")

    print("\n--- Simulation journalière PV+Batterie ---")
    G_jour = [0]*6 + [200, 400, 600, 800, 900, 950, 950, 900, 800, 600, 400, 200, 50, 0, 0, 0, 0, 0]
    sys = SystemeStockagePV(Ppv_kwc=3, Cbat_kwh=10)
    bilan = sys.simuler_jour(G_jour, conso_kwh=15)
    print(f"Production PV: {bilan['prod']:.1f} kWh")
    print(f"Consommation:  {bilan['conso']:.1f} kWh")
    print(f"Réseau (achat): {bilan['grid_in']:.1f} kWh")
    print(f"Réseau (vente): {bilan['grid_out']:.1f} kWh")
    print(f"Autoconsommation: {(1 - bilan['grid_in']/bilan['conso'])*100:.0f}%")

if __name__ == '__main__':
    main()
