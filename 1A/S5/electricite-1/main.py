"""Projet: Electricite 1
1AS5 - ENSEM NRJ (FISA)
Lois de base, courant continu, theoremes, puissance"""

import numpy as np
import math

class LoisKirchhoff:
    @staticmethod
    def loi_ohm(R, I):
        return R * I

    @staticmethod
    def puissance(R, I=None, V=None):
        if I: return R * I**2
        if V: return V**2 / R
        return 0

    @staticmethod
    def serie_resistances(Rs):
        return sum(Rs)

    @staticmethod
    def parallele_resistances(Rs):
        return 1 / sum(1/R for R in Rs)

class DiviseurTension:
    def __init__(self, R1=100, R2=200):
        self.R1 = R1
        self.R2 = R2

    def V_out(self, Ve):
        return Ve * self.R2 / (self.R1 + self.R2)

class DiviseurCourant:
    def __init__(self, R1=100, R2=200):
        self.R1 = R1
        self.R2 = R2

    def I_out(self, Ie):
        return Ie * self.R1 / (self.R1 + self.R2)

class Thevenin:
    def __init__(self, Vth=12, Rth=50):
        self.Vth = Vth
        self.Rth = Rth

    def V_sortie(self, R_charge):
        return self.Vth * R_charge / (self.Rth + R_charge)

    def I(self, R_charge):
        return self.Vth / (self.Rth + R_charge)

class Norton:
    def __init__(self, In=0.24, Rn=50):
        self.In = In
        self.Rn = Rn

    def V_sortie(self, R_charge):
        return self.In * (self.Rn * R_charge) / (self.Rn + R_charge)

class PontDiviseur:
    def __init__(self, R1=100, R2=100, R3=100, R4=100):
        self.R1 = R1; self.R2 = R2; self.R3 = R3; self.R4 = R4

    def V_out(self, Ve):
        return Ve * (self.R2/(self.R1+self.R2) - self.R4/(self.R3+self.R4))

class PuissanceElectrique:
    @staticmethod
    def continue_(V, I):
        return V * I

    @staticmethod
    def rendement(P_utile, P_absorbee):
        return P_utile / P_absorbee if P_absorbee else 0

    @staticmethod
    def cout(P_kW, duree_h, prix_kWh=0.15):
        return P_kW * duree_h * prix_kWh

class CircuitsRC:
    def __init__(self, R=1000, C=1e-6):
        self.R = R
        self.C = C
        self.tau = R * C

    def charge(self, E, t):
        return E * (1 - np.exp(-t/self.tau))

    def decharge(self, V0, t):
        return V0 * np.exp(-t/self.tau)

def main():
    print("=" * 60)
    print("Electricite 1")
    print("1AS5 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Loi d'Ohm et associations ---")
    print(f"  Loi d'Ohm (R=100, I=0.5): V={LoisKirchhoff.loi_ohm(100, 0.5)}V")
    print(f"  Puissance (R=100, I=0.5): P={LoisKirchhoff.puissance(100, I=0.5)}W")
    Rs = LoisKirchhoff.serie_resistances([100, 200, 300])
    Rp = LoisKirchhoff.parallele_resistances([100, 200])
    print(f"  Serie (100+200+300): Req={Rs} ohms")
    print(f"  Parallele (100//200): Req={Rp:.1f} ohms")

    print("\n--- 2. Diviseur de tension ---")
    dt = DiviseurTension(R1=100, R2=300)
    for Ve in [5, 12, 24]:
        print(f"  Ve={Ve}V: Vs={dt.V_out(Ve):.2f}V")

    print("\n--- 3. Theoreme de Thevenin ---")
    th = Thevenin(Vth=12, Rth=50)
    for Rc in [10, 50, 100, 500]:
        print(f"  R_charge={Rc}: Vs={th.V_sortie(Rc):.2f}V, I={th.I(Rc)*1000:.1f}mA")

    print("\n--- 4. Pont de Wheatstone ---")
    pd = PontDiviseur(R1=100, R2=100, R3=100, R4=120)
    print(f"  Pont equilibre (R1=R2=R3=100, R4=120):")
    for Ve in [5, 10]:
        print(f"  Ve={Ve}V: Vs={pd.V_out(Ve):.3f}V")

    print("\n--- 5. Puissance et cout ---")
    print(f"  Puissance continue (12V, 2A): {PuissanceElectrique.continue_(12, 2)}W")
    P = 1500
    h = 5
    cout = PuissanceElectrique.cout(P/1000, h)
    print(f"  Cout 1.5kW pendant 5h: {cout:.2f} EUR")
    cout_an = PuissanceElectrique.cout(P/1000, 5*365)
    print(f"  Cout annuel: {cout_an:.2f} EUR")

    print("\n--- 6. Circuit RC transitoire ---")
    rc = CircuitsRC(R=1000, C=100e-6)
    print(f"  RC: R=1k, C=100uF, tau={rc.tau*1000:.1f}ms")
    for t in [0.05, 0.1, 0.2, 0.5]:
        print(f"  t={t*1000:.0f}ms: Vc={rc.charge(12, t):.2f}V")

if __name__ == '__main__':
    main()
