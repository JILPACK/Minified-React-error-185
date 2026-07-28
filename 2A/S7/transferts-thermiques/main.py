"""Projet: Transferts thermiques
2AS7 - ENSEM NRJ (FISA)
Conduction, convection, rayonnement, echangeurs"""

import numpy as np

class Conduction1D:
    def __init__(self, L=1.0, k=50, A=0.01):
        self.L = L
        self.k = k
        self.A = A

    def mur_plan(self, T1, T2):
        R = self.L / (self.k * self.A)
        Q = (T1 - T2) / R
        return {'R': R, 'Q': Q}

    def mur_multicouche(self, couches, T1, T2):
        R_total = sum(e/(k*A) for e,k,A in couches)
        Q = (T1 - T2) / R_total
        T = T1
        print(f"  Profil temperature:")
        for i, (e, k, A) in enumerate(couches):
            dT = Q * e / (k * A)
            print(f"    Couche {i+1}: T_entree={T:.1f}C, T_sortie={T-dT:.1f}C")
            T -= dT
        return {'R': R_total, 'Q': Q}

class Ailette:
    def __init__(self, L=0.05, k=200, h=50, per=0.1, Ac=0.0001):
        self.L = L; self.k = k; self.h = h
        self.per = per; self.Ac = Ac
        self.m = np.sqrt(h * per / (k * Ac))

    def efficacite(self):
        return np.tanh(self.m * self.L) / (self.m * self.L)

    def flux(self, T_base, T_inf):
        eta = self.efficacite()
        S = self.per * self.L
        return eta * self.h * S * (T_base - T_inf)

class Convection:
    def __init__(self, h=100, A=0.5):
        self.h = h
        self.A = A

    def flux(self, T_paroi, T_fluide):
        return self.h * self.A * (T_paroi - T_fluide)

    @staticmethod
    def h_ecoulement_interne(Re, Pr, k, D, n=0.4):
        if Re > 4000:
            Nu = 0.023 * Re**0.8 * Pr**n
        elif Re < 2000:
            Nu = 3.66
        else:
            Nu = 3.66 + (0.023*Re**0.8*Pr**n - 3.66) * (Re-2000)/2000
        return Nu * k / D

class Rayonnement:
    def __init__(self, epsilon=0.9, A=1.0):
        self.eps = epsilon
        self.A = A
        self.sigma = 5.67e-8

    def flux(self, T1, T2):
        return self.eps * self.A * self.sigma * (T1**4 - T2**4)

class EchangeurTubeCoaxial:
    def __init__(self, D_int=0.02, D_ext=0.04, L=5):
        self.D_int = D_int; self.D_ext = D_ext; self.L = L
        self.A_int = np.pi * D_int * L
        self.A_ext = np.pi * D_ext * L

    def NTU_method(self, m_c, c_c, m_f, c_f, U, co_current=False):
        C_c = m_c * c_c; C_f = m_f * c_f
        C_min = min(C_c, C_f); C_max = max(C_c, C_f)
        NTU = U * self.A_int / C_min
        r = C_min / C_max
        if co_current:
            eps = (1 - np.exp(-NTU*(1+r))) / (1+r)
        else:
            eps = (1 - np.exp(-NTU*(1-r))) / (1 - r*np.exp(-NTU*(1-r))) if r < 1 else NTU/(1+NTU)
        Q = eps * C_min * 30
        return {'eps': eps, 'Q': Q/1000, 'NTU': NTU}

def main():
    print("=" * 60)
    print("Transferts thermiques")
    print("2AS7 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Conduction - Mur plan ---")
    mur = Conduction1D(L=0.3, k=0.8, A=10)
    res = mur.mur_plan(20, -5)
    print(f"  Resistance: {res['R']:.3f} K/W")
    print(f"  Flux thermique: {res['Q']:.0f} W")

    print("\n--- 2. Mur multicouche ---")
    couches = [(0.02, 0.04, 1), (0.20, 0.8, 1), (0.10, 0.03, 1)]
    mur.mur_multicouche(couches, 20, -5)

    print("\n--- 3. Ailette de refroidissement ---")
    ail = Ailette(L=0.06, k=200, h=60, per=0.12, Ac=0.0008)
    print(f"  m*L: {ail.m*ail.L:.2f}")
    print(f"  Efficacite: {ail.efficacite():.3f}")
    Q_ail = ail.flux(80, 25)
    print(f"  Flux dissipe: {Q_ail:.1f} W")

    print("\n--- 4. Convection forcee ---")
    k_air = 0.026; Pr = 0.71; D = 0.05
    for Re in [1000, 5000, 20000]:
        h = Convection.h_ecoulement_interne(Re, Pr, k_air, D)
        print(f"  Re={Re:<6} h={h:.1f} W/m2K")
    conv = Convection(h=150, A=2.5)
    print(f"  Flux convectif: {conv.flux(80, 25):.0f} W")

    print("\n--- 5. Rayonnement ---")
    rad = Rayonnement(epsilon=0.85, A=0.5)
    Q_rad = rad.flux(273+80, 273+25)
    print(f"  Flux radiatif (T1=80C, T2=25C): {Q_rad:.1f} W")

    print("\n--- 6. Echangeur tubulaire ---")
    ech = EchangeurTubeCoaxial(D_int=0.025, D_ext=0.045, L=10)
    res_cc = ech.NTU_method(0.5, 4180, 0.8, 4180, 800)
    print(f"  Co-courant: eps={res_cc['eps']:.3f}, Q={res_cc['Q']:.1f} kW")
    res_ct = ech.NTU_method(0.5, 4180, 0.8, 4180, 800, co_current=False)
    print(f"  Contre-courant: eps={res_ct['eps']:.3f}, Q={res_ct['Q']:.1f} kW")

if __name__ == '__main__':
    main()
