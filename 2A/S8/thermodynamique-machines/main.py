"""Projet: Thermodynamique des machines et des systèmes
2AS8 - ENSEM NRJ (FISA)
Cycles thermodynamiques (Rankine, Brayton, Carnot, frigorifique)
et bilans énergétiques"""

import numpy as np
import matplotlib.pyplot as plt

class Fluide:
    def __init__(self, nom, cp=1005, cv=718, R=287, gamma=1.4):
        self.nom = nom
        self.cp = cp
        self.cv = cv
        self.R = R
        self.gamma = gamma

class CycleRankine:
    def __init__(self, P_basse=0.08e5, P_haute=100e5, T_vapeur=500):
        self.P_basse = P_basse        # Pression condenseur [Pa]
        self.P_haute = P_haute        # Pression chaudière [Pa]
        self.T_vapeur = T_vapeur + 273  # Température vapeur [K]
        self.eta = 0

    def calculer_rendement(self):
        # Approximation simplifiée du cycle de Rankine
        T_basse = 273 + 41.5  # Température sat à 0.08 bar
        T_haute = self.T_vapeur
        self.eta_carnot = 1 - T_basse / T_haute
        self.eta = 0.85 * self.eta_carnot  # Rendement réel ~85% de Carnot
        return self.eta

    def puissance(self, debit_kg_s=10):
        h1 = 4200e3        # Enthalpie vapeur surchauffée [J/kg]
        h2 = 2400e3        # Enthalpie sortie turbine [J/kg]
        W_turbine = (h1 - h2) * debit_kg_s / 1e6
        return W_turbine   # [MW]

    def bilan(self, debit=10):
        print(f"\nBilan thermique du cycle de Rankine:")
        P = self.puissance(debit)
        Q_chaudiere = P / self.eta
        Q_condenseur = Q_chaudiere - P
        print(f"  Puissance turbine: {P:.1f} MW")
        print(f"  Puissance chaudière: {Q_chaudiere:.1f} MW")
        print(f"  Rejet condenseur: {Q_condenseur:.1f} MW")
        print(f"  Rendement: {self.eta:.1%}")

class CycleBrayton:
    def __init__(self, tau_c=15, T_entree=288, T_combustion=1400):
        self.tau_c = tau_c            # Taux de compression
        self.T1 = T_entree            # Température entrée compresseur [K]
        self.T3 = T_combustion        # Température sortie chambre [K]
        self.air = Fluide("Air", 1005, 718, 287, 1.4)

    def calculer(self):
        rp = self.tau_c
        g = self.air.gamma
        # Compresseur
        self.T2 = self.T1 * rp**((g-1)/g)
        Wc = self.air.cp * (self.T2 - self.T1)
        # Turbine
        self.T4 = self.T3 / rp**((g-1)/g)
        Wt = self.air.cp * (self.T3 - self.T4)
        W_net = Wt - Wc
        Q_in = self.air.cp * (self.T3 - self.T2)
        self.eta = W_net / Q_in
        return {'Wc': Wc/1e3, 'Wt': Wt/1e3, 'Wnet': W_net/1e3, 'eta': self.eta}

class CycleFrigorifique:
    def __init__(self, T_froid=-10, T_chaud=40):
        self.T_froid = T_froid + 273
        self.T_chaud = T_chaud + 273

    def COP(self):
        COP_carnot = self.T_froid / (self.T_chaud - self.T_froid)
        COP_reel = 0.6 * COP_carnot
        return COP_carnot, COP_reel

class MachineThermique:
    def __init__(self, T_source, T_puits):
        self.T_source = T_source + 273
        self.T_puits = T_puits + 273

    def rendement_carnot(self):
        return 1 - self.T_puits / self.T_source

def main():
    print("=" * 60)
    print("Thermodynamique des machines et des systèmes")
    print("2AS8 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Cycle de Rankine (centrale thermique) ---")
    rankine = CycleRankine(P_haute=120e5, T_vapeur=540)
    eta = rankine.calculer_rendement()
    print(f"Rendement de Carnot: {rankine.eta_carnot:.1%}")
    print(f"Rendement réel: {eta:.1%}")
    rankine.bilan(debit=15)

    print("\n--- 2. Cycle de Brayton (turbine à gaz) ---")
    brayton = CycleBrayton(tau_c=14, T_entree=288, T_combustion=1300)
    res = brayton.calculer()
    print(f"Température sortie compresseur: {brayton.T2-273:.0f}°C")
    print(f"Température sortie turbine: {brayton.T4-273:.0f}°C")
    print(f"Travail compresseur: {res['Wc']:.0f} kJ/kg")
    print(f"Travail turbine: {res['Wt']:.0f} kJ/kg")
    print(f"Travail net: {res['Wnet']:.0f} kJ/kg")
    print(f"Rendement: {res['eta']:.1%}")

    print("\n--- 3. Cycle frigorifique ---")
    froid = CycleFrigorifique(T_froid=-5, T_chaud=45)
    COP_c, COP_r = froid.COP()
    print(f"COP Carnot: {COP_c:.2f}")
    print(f"COP réel (60%): {COP_r:.2f}")
    print(f"Puissance frigo pour 10kW électrique: {10*COP_r:.1f} kW")

    print("\n--- 4. Rendement de Carnot ---")
    for T_s, T_p in [(500, 30), (800, 40), (1000, 50)]:
        mt = MachineThermique(T_s, T_p)
        print(f"T_source={T_s}°C, T_puits={T_p}°C → η_carnot={mt.rendement_carnot():.1%}")

if __name__ == '__main__':
    main()
