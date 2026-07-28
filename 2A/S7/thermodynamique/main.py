"""Projet: Thermodynamique
2AS7 - ENSEM NRJ (FISA)
Gaz parfaits, bilans d'energie, transformations, machines"""

import numpy as np

class GazParfait:
    def __init__(self, nom, R=287, gamma=1.4, cp=1005, cv=718):
        self.nom = nom
        self.R = R
        self.gamma = gamma
        self.cp = cp
        self.cv = cv

    def lois(self, P, V, T, m=1):
        return P * V == m * self.R * T

class Transformation:
    def __init__(self, gaz=None):
        self.gaz = gaz or GazParfait("Air")

    def isochore(self, m, T1, T2):
        dU = m * self.gaz.cv * (T2 - T1)
        return {'dU': dU/1000, 'Q': dU/1000, 'W': 0}

    def isobare(self, m, T1, T2):
        dU = m * self.gaz.cv * (T2 - T1)
        W = m * self.gaz.R * (T2 - T1)
        Q = dU + W
        return {'dU': dU/1000, 'W': W/1000, 'Q': Q/1000}

    def isotherme(self, m, T, V1, V2):
        W = m * self.gaz.R * T * np.log(V2/V1)
        return {'dU': 0, 'W': W/1000, 'Q': W/1000}

    def adiabatique(self, m, T1, T2):
        dU = m * self.gaz.cv * (T2 - T1)
        return {'dU': dU/1000, 'W': -dU/1000, 'Q': 0}

    def polytropique(self, m, T1, T2, n=1.3):
        dU = m * self.gaz.cv * (T2 - T1)
        W = m * self.gaz.R * (T2 - T1) / (1 - n) if n != 1 else 0
        Q = dU + W
        return {'dU': dU/1000, 'W': W/1000, 'Q': Q/1000}

class CycleThermo:
    def __init__(self, gaz=None):
        self.gaz = gaz or GazParfait("Air")
        self.etapes = []

    def ajouter(self, etape):
        self.etapes.append(etape)

    def bilan(self):
        W_net = sum(e['W'] for e in self.etapes)
        Q_in = sum(e['Q'] for e in self.etapes if e['Q'] > 0)
        eta = W_net / Q_in * 100 if Q_in else 0
        return {'W_net': W_net, 'Q_in': Q_in, 'eta': eta}

class MelangeGaz:
    def __init__(self, fractions_molaires):
        self.y = fractions_molaires
        self.gaz_ref = {
            'N2': GazParfait('N2', R=297, gamma=1.4, cp=1040, cv=743),
            'O2': GazParfait('O2', R=260, gamma=1.4, cp=918, cv=658),
            'CO2': GazParfait('CO2', R=189, gamma=1.3, cp=844, cv=655),
            'CH4': GazParfait('CH4', R=518, gamma=1.31, cp=2235, cv=1717),
        }

    def R_eq(self):
        return sum(self.y[g] * self.gaz_ref[g].R for g in self.y)

class Exergie:
    def __init__(self, T0=298, P0=1e5):
        self.T0 = T0; self.P0 = P0

    def d_un_flux(self, H, S, T):
        return H - self.T0 * S

def main():
    print("=" * 60)
    print("Thermodynamique")
    print("2AS7 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Gaz parfaits - transformations ---")
    gaz = GazParfait("Air", R=287, gamma=1.4, cp=1005, cv=718)
    trans = Transformation(gaz)
    m = 2  # kg
    T1, T2 = 300, 600

    iso_v = trans.isochore(m, T1, T2)
    print(f"Isochore (m={m}kg, {T1}K->{T2}K):")
    print(f"  dU={iso_v['dU']:.1f} kJ, Q={iso_v['Q']:.1f} kJ, W={iso_v['W']:.1f} kJ")

    iso_p = trans.isobare(m, T1, T2)
    print(f"Isobare (m={m}kg, {T1}K->{T2}K):")
    print(f"  dU={iso_p['dU']:.1f} kJ, Q={iso_p['Q']:.1f} kJ, W={iso_p['W']:.1f} kJ")

    iso_t = trans.isotherme(m, 300, 0.5, 1.0)
    print(f"Isotherme (m={m}kg, T=300K, V1=0.5->V2=1.0):")
    print(f"  dU={iso_t['dU']:.1f} kJ, Q={iso_t['Q']:.1f} kJ, W={iso_t['W']:.1f} kJ")

    adia = trans.adiabatique(m, T1, T2)
    print(f"Adiabatique (m={m}kg, {T1}K->{T2}K):")
    print(f"  dU={adia['dU']:.1f} kJ, Q={adia['Q']:.1f} kJ, W={adia['W']:.1f} kJ")

    poly = trans.polytropique(m, T1, T2, n=1.3)
    print(f"Polytropique n=1.3 (m={m}kg, {T1}K->{T2}K):")
    print(f"  dU={poly['dU']:.1f} kJ, Q={poly['Q']:.1f} kJ, W={poly['W']:.1f} kJ")

    print("\n--- 2. Cycle thermodynamique ---")
    cycle = CycleThermo(gaz)
    cycle.etapes = [trans.adiabatique(1, 300, 700)]
    cycle.ajouter(trans.isobare(1, 700, 1500))
    cycle.ajouter(trans.adiabatique(1, 1500, 800))
    cycle.ajouter(trans.isobare(1, 800, 300))
    bilan = cycle.bilan()
    print(f"Cycle simple (4 transformations):")
    for i, e in enumerate(cycle.etapes):
        print(f"  Etape {i+1}: Q={e['Q']:.1f} kJ, W={e['W']:.1f} kJ")
    print(f"  W_net={bilan['W_net']:.1f} kJ")
    print(f"  Q_in={bilan['Q_in']:.1f} kJ")
    print(f"  Rendement: {bilan['eta']:.1f}%")

    print("\n--- 3. Melange de gaz ---")
    air = MelangeGaz({'N2': 0.79, 'O2': 0.21})
    print(f"Air: N2 79%, O2 21%")
    print(f"  R_eq = {air.R_eq():.1f} J/kgK")

    print("\n--- 4. Exergie ---")
    ex = Exergie(T0=298, P0=1e5)
    Q_chaud = 500  # kJ a 800K
    ex_chaud = ex.d_un_flux(Q_chaud, 0, 800)
    print(f"Exergie d'une source de chaleur Q={Q_chaud} kJ a T=800K:")
    print(f"  Exergie = {ex_chaud:.1f} kJ")

if __name__ == '__main__':
    main()
