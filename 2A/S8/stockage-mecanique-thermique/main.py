"""Projet: Stockage mécanique et thermique, conversion d'énergie fluide
2AS8 - ENSEM NRJ (FISA)
Simulation de systèmes de stockage par pompage-turbinage, volant d'inertie
et stockage thermique"""

import numpy as np
import matplotlib.pyplot as plt

class StockagePompage:
    def __init__(self, hauteur=200, debit_max=50, rendement_turbine=0.9,
                 rendement_pompe=0.85, volume_bassin=5e5):
        self.hauteur = hauteur            # Hauteur de chute [m]
        self.debit_max = debit_max        # Débit max [m3/s]
        self.eta_t = rendement_turbine
        self.eta_p = rendement_pompe
        self.volume = volume_bassin       # Volume du bassin [m3]
        self.V_stocke = 0                 # Volume stocké [m3]
        self.rho = 1000                   # Masse volumique eau [kg/m3]
        self.g = 9.81

    def puissance_turbine(self, debit):
        P = self.rho * self.g * self.hauteur * debit * self.eta_t / 1e6
        return P  # [MW]

    def puissance_pompage(self, debit):
        P = self.rho * self.g * self.hauteur * debit / (self.eta_p * 1e6)
        return P  # [MW]

    def stocker(self, duree_h, debit):
        debit = min(debit, self.debit_max)
        volume_pompe = debit * duree_h * 3600
        self.V_stocke = min(self.V_stocke + volume_pompe, self.volume)
        return self.puissance_pompage(debit) * duree_h * 1000  # kWh

    def turbiner(self, duree_h, debit):
        debit = min(debit, self.debit_max)
        volume_turbine = debit * duree_h * 3600
        if self.V_stocke >= volume_turbine:
            self.V_stocke -= volume_turbine
            return self.puissance_turbine(debit) * duree_h * 1000
        else:
            return 0

    def energie_stockee(self):
        masse = self.V_stocke * self.rho
        return masse * self.g * self.hauteur * self.eta_t / 3.6e6  # [kWh]

class VolantInertie:
    def __init__(self, masse=5000, rayon=1.5, omega_max=3000):
        self.masse = masse
        self.rayon = rayon
        self.I = 0.5 * masse * rayon**2
        self.omega_max = omega_max * 2 * np.pi / 60
        self.omega = 0

    def E_max(self):
        return 0.5 * self.I * self.omega_max**2 / 1e6  # [MJ]

    def stocker(self, P_kW, duree_s):
        E = P_kW * 1000 * duree_s
        omega_new = np.sqrt(self.omega**2 + 2 * E / self.I)
        if omega_new <= self.omega_max:
            self.omega = omega_new
            return True
        return False

    def degager(self, P_kW, duree_s):
        E = P_kW * 1000 * duree_s
        if 0.5 * self.I * self.omega**2 >= E:
            self.omega = np.sqrt(self.omega**2 - 2 * E / self.I)
            return True
        return False

class StockageThermique:
    def __init__(self, materiau, masse, T_init=20, Cp=1000):
        self.materiau = materiau
        self.masse = masse
        self.T = T_init
        self.Cp = Cp  # J/kgK

    def chauffer(self, P_kW, duree_h):
        E = P_kW * 1000 * duree_h * 3600
        delta_T = E / (self.masse * self.Cp)
        self.T += delta_T
        return self.T

    def energie_contenue(self, T_ref=20):
        return self.masse * self.Cp * (self.T - T_ref) / 3.6e6  # [kWh]

class SystemeHydraulique:
    def __init__(self, P_nom=1e5, H=50, Q=0.5):
        self.P_nom = P_nom        # Puissance nominale [W]
        self.H = H                # Hauteur [m]
        self.Q = Q                # Débit [m3/s]
        self.rho = 1000
        self.g = 9.81

    def puissance_hydraulique(self):
        return self.rho * self.g * self.H * self.Q

    def rendement_turbine(self, P_elec):
        return P_elec / self.puissance_hydraulique()

def main():
    print("=" * 60)
    print("Stockage mécanique et thermique, conversion d'énergie fluide")
    print("2AS8 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Station de pompage-turbinage ---")
    step = StockagePompage(hauteur=300, debit_max=80)
    print(f"STEP: H={step.hauteur}m, V={step.volume/1e3:.0f} m3")
    print(f"Puissance turbine max: {step.puissance_turbine(step.debit_max):.1f} MW")
    print(f"Puissance pompage max: {step.puissance_pompage(step.debit_max):.1f} MW")
    # Cycle journalier
    print("\nCycle journalier:")
    step.stocker(6, 50)     # Pompage la nuit
    print(f"  Stockage 6h (nuit): {step.V_stocke/1e3:.1f} m3 → {step.energie_stockee():.0f} kWh")
    prod = step.turbiner(4, 60)  # Turbinage aux heures de pointe
    print(f"  Turbinage 4h (pointe): {prod:.0f} kWh produits")

    print("\n--- 2. Volant d'inertie ---")
    volant = VolantInertie(masse=8000, rayon=2.0, omega_max=3600)
    print(f"Volant: I={volant.I:.0f} kg·m2, E_max={volant.E_max():.1f} MJ")
    volant.stocker(100, 30)  # 100 kW pendant 30s
    print(f"  Stockage 100kW/30s: ω={volant.omega*60/(2*np.pi):.0f} tr/min")
    volant.degager(80, 20)
    print(f"  Dégagement 80kW/20s: ω={volant.omega*60/(2*np.pi):.0f} tr/min")

    print("\n--- 3. Stockage thermique (sel fondu) ---")
    sel = StockageThermique("Sel fondu", 50000, T_init=290, Cp=1500)
    print(f"Sels fondus: {sel.masse} kg, Cp={sel.Cp} J/kgK")
    sel.chauffer(1000, 4)
    print(f"  Après chauffage 1MW/4h: T={sel.T:.0f}°C, E={sel.energie_contenue():.0f} kWh")

    print("\n--- 4. Conversion d'énergie fluide ---")
    hyd = SystemeHydraulique(P_nom=50000, H=45, Q=0.12)
    print(f"Puissance hydraulique: {hyd.puissance_hydraulique()/1e3:.1f} kW")
    P_elec = 42000
    print(f"Puissance électrique: {P_elec/1e3:.1f} kW")
    print(f"Rendement turbine: {hyd.rendement_turbine(P_elec):.1%}")

if __name__ == '__main__':
    main()
