"""Projet: Chimie et thermochimie
1AS5 - ENSEM NRJ (FISA)
Atomistique, liaisons, thermochimie, cinetique chimique"""

import numpy as np
import math

class Atomistique:
    def __init__(self):
        self.masse_electron = 9.109e-31
        self.masse_proton = 1.673e-27
        self.masse_neutron = 1.675e-27
        self.e = 1.602e-19
        self.h = 6.626e-34
        self.c = 3e8

    def energie_niveau(self, Z, n):
        E0 = 13.6
        return -E0 * Z**2 / n**2

    def longueur_onde_transition(self, Z, n1, n2):
        E1 = self.energie_niveau(Z, n1)
        E2 = self.energie_niveau(Z, n2)
        delta_E = abs(E2 - E1) * self.e
        return self.h * self.c / delta_E if delta_E else 0

class LiaisonsChimiques:
    @staticmethod
    def energie_liaison(type):
        energies = {'H-H': 436, 'C-C': 348, 'C=C': 614, 'C-H': 413,
                    'O-H': 463, 'O=O': 498, 'N-H': 391, 'C-O': 360}
        return energies.get(type, None)

    @staticmethod
    def enthalpie_reaction(liaisons_rompues, liaisons_formees):
        E_rupture = sum(LiaisonsChimiques.energie_liaison(l) or 0 for l in liaisons_rompues)
        E_formation = sum(LiaisonsChimiques.energie_liaison(l) or 0 for l in liaisons_formees)
        return E_rupture - E_formation

class Thermochimie:
    def __init__(self):
        self.R = 8.314

    def chaleur_sensible(self, m, cp, T1, T2):
        return m * cp * (T2 - T1)

    def changement_etat(self, m, L):
        return m * L

    def enthalpie_standard(self, H_produits, H_reactifs):
        return H_produits - H_reactifs

class CinetiqueChimique:
    def __init__(self, k=0.1, ordre=1):
        self.k = k
        self.ordre = ordre

    def concentration(self, C0, t):
        if self.ordre == 0:
            return max(0, C0 - self.k*t)
        elif self.ordre == 1:
            return C0 * np.exp(-self.k*t)
        elif self.ordre == 2:
            return C0 / (1 + self.k*C0*t) if self.k*C0*t >= 0 else 0
        return None

    def temps_demi_vie(self, C0):
        if self.ordre == 0:
            return C0/(2*self.k)
        elif self.ordre == 1:
            return np.log(2)/self.k
        elif self.ordre == 2:
            return 1/(self.k*C0)
        return None

    @staticmethod
    def Arrhenius(A, Ea, T):
        R = 8.314
        return A * np.exp(-Ea/(R*T))

class Solutions:
    @staticmethod
    def concentration_massique(m, V):
        return m / V

    @staticmethod
    def concentration_molaire(n, V):
        return n / V

    @staticmethod
    def dilution(C1, V1, V2):
        return C1 * V1 / V2

    @staticmethod
    def pH_acide_fort(Ca):
        return -np.log10(Ca)

    @staticmethod
    def pH_base_forte(Cb):
        return 14 + np.log10(Cb)

def main():
    print("=" * 60)
    print("Chimie et thermochimie")
    print("1AS5 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Atomistique ---")
    at = Atomistique()
    for n in [1, 2, 3, 4]:
        E = at.energie_niveau(1, n)
        print(f"  Hydrogene, n={n}: E={E:.2f} eV")
    l = at.longueur_onde_transition(1, 2, 1)
    print(f"  Transition n=2 -> n=1: lambda={l*1e9:.1f} nm")
    l2 = at.longueur_onde_transition(1, 3, 2)
    print(f"  Transition n=3 -> n=2: lambda={l2*1e9:.1f} nm")

    print("\n--- 2. Liaisons chimiques ---")
    print(f"  Energie liaison H-H: {LiaisonsChimiques.energie_liaison('H-H')} kJ/mol")
    print(f"  Energie liaison O=O: {LiaisonsChimiques.energie_liaison('O=O')} kJ/mol")
    # Combustion H2
    delta_H = LiaisonsChimiques.enthalpie_reaction(['H-H', 'O=O'], ['O-H', 'O-H'])
    print(f"  Combustion H2: delta_H = {delta_H} kJ/mol")

    print("\n--- 3. Thermochimie ---")
    th = Thermochimie()
    ch = th.chaleur_sensible(1, 4180, 20, 100)
    print(f"  Chauffe 1kg eau 20->100C: Q={ch/1000:.0f} kJ")
    vap = th.changement_etat(1, 2260e3)
    print(f"  Vaporisation 1kg eau: Q={vap/1000:.0f} kJ")

    print("\n--- 4. Cinetique chimique ---")
    ci = CinetiqueChimique(k=0.05, ordre=1)
    for t in [0, 10, 20, 40, 60]:
        C = ci.concentration(1.0, t)
        print(f"  Ordre 1 (k=0.05), t={t}s: C={C:.3f} mol/L")
    print(f"  t1/2 = {ci.temps_demi_vie(1.0):.1f} s")

    print("\n  Loi d'Arrhenius:")
    for T in [300, 400, 500, 600]:
        k = CinetiqueChimique.Arrhenius(1e12, 75e3, T)
        print(f"  T={T}K: k={k:.2e}")

    print("\n--- 5. Solutions et pH ---")
    print(f"  Acide fort HCl 0.01M: pH={Solutions.pH_acide_fort(0.01):.2f}")
    print(f"  Base forte NaOH 0.01M: pH={Solutions.pH_base_forte(0.01):.2f}")
    C2 = Solutions.dilution(1.0, 10, 100)
    print(f"  Dilution 10mL 1M -> 100mL: C={C2:.3f} M")

if __name__ == '__main__':
    main()
