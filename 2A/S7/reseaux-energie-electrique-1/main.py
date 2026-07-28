"""Projet: Reseaux d'energie electrique 1
2AS7 - ENSEM NRJ (FISA)
Lignes, transformateurs, modele per-unit, ecoulement de puissance"""

import numpy as np

class LigneElectrique:
    def __init__(self, R=0.15, L=1.3e-3, C=10e-9, l=50, Vn=63e3):
        self.Rl = R/1000; self.Ll = L/1000; self.Cl = C/1000
        self.l = l; self.Vn = Vn

    def modele_pi(self, f=50):
        w = 2*np.pi*f
        Z = (self.Rl + 1j*w*self.Ll) * self.l
        Y = 1j*w*self.Cl * self.l
        return Z, Y/2

    def regul_T(self, I, cos_phi=0.9, f=50):
        Z, _ = self.modele_pi(f)
        R, X = Z.real, Z.imag
        phi = np.arccos(cos_phi)
        dV = I*(R*cos_phi + X*np.sin(phi))
        return dV / self.Vn * 100

class Transformateur:
    def __init__(self, Sn=36e6, V1=63e3, V2=20e3, Uk=0.08, Pk=150e3):
        self.Sn = Sn; self.V1 = V1; self.V2 = V2
        self.Uk = Uk; self.Pk = Pk
        self.Zb1 = V1**2 / Sn
        self.Zb2 = V2**2 / Sn

    def impedance_ramenee(self, secondaire=True):
        Vb = self.V2 if secondaire else self.V1
        Zb = Vb**2 / self.Sn
        R = self.Pk / self.Sn * Zb
        X = np.sqrt((self.Uk*Zb)**2 - R**2)
        return R, X

class SystemePerUnit:
    def __init__(self, Sbase=100e6, Vbase=63e3):
        self.Sb = Sbase; self.Vb = Vbase
        self.Ib = Sbase / (np.sqrt(3)*Vbase)
        self.Zb = Vbase**2 / Sbase

    def en_pu(self, Z_reel):
        return Z_reel / self.Zb

class AnalyseLoadFlow:
    def __init__(self):
        self.noeuds = {}
        self.branches = []

    def ajouter_noeud(self, nom, type='PV', P=0, Q=0, V=1.0, theta=0):
        self.noeuds[nom] = {'type': type, 'P': P, 'Q': Q, 'V': V, 'theta': theta}

    def ajouter_ligne(self, de, vers, R, X, B=0):
        self.branches.append({'de': de, 'vers': vers, 'R': R, 'X': X, 'B': B})

    def calculer_courants(self):
        for nom, n in self.noeuds.items():
            n['I'] = (n['P'] - 1j*n['Q']) / n['V'] if n['V'] else 0
        return self.noeuds

class CourtCircuit:
    def __init__(self, S_cc=500e6, V=63e3):
        self.S_cc = S_cc; self.V = V

    def I_cc_ini(self):
        return self.S_cc / (np.sqrt(3)*self.V)

    def S_cc_ligne(self, Z_ligne):
        I = self.V / (np.sqrt(3)*abs(Z_ligne))
        return np.sqrt(3)*self.V*I

def main():
    print("=" * 60)
    print("Reseaux d'energie electrique 1")
    print("2AS7 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Ligne electrique - modele pi ---")
    ligne = LigneElectrique(R=0.12, L=1.2e-3, C=11e-9, l=60, Vn=90e3)
    Z, Y = ligne.modele_pi()
    print(f"Ligne {ligne.l}km, {ligne.Vn/1e3:.0f} kV")
    print(f"  Z = {Z.real:.2f} + j{Z.imag:.2f} ohms")
    print(f"  Y/2 = {Y:.2e} S")
    reg = ligne.regul_T(150, 0.92)
    print(f"  Chute tension: {reg:.2f}%")
    reg2 = ligne.regul_T(300, 0.85)
    print(f"  Chute tension (I=300A, pf=0.85): {reg2:.2f}%")

    print("\n--- 2. Transformateur ---")
    tf = Transformateur(Sn=36e6, V1=63e3, V2=20e3, Uk=0.08, Pk=120e3)
    R, X = tf.impedance_ramenee(secondaire=True)
    print(f"Transfo {tf.Sn/1e6:.0f} MVA, {tf.V1/1e3:.0f}/{tf.V2/1e3:.0f} kV")
    print(f"  R = {R:.4f} ohms (cote BT)")
    print(f"  X = {X:.4f} ohms (cote BT)")
    print(f"  Zbase BT: {tf.Zb2:.2f} ohms")

    print("\n--- 3. Systeme per-unit ---")
    pu = SystemePerUnit(Sbase=100e6, Vbase=63e3)
    print(f"Sb = {pu.Sb/1e6:.0f} MVA, Vb = {pu.Vb/1e3:.0f} kV")
    print(f"Ib = {pu.Ib:.0f} A, Zb = {pu.Zb:.2f} ohms")
    Z_reel = 15 + 1j*20
    print(f"Z = {Z_reel} ohms -> Z_pu = {pu.en_pu(Z_reel):.4f}")

    print("\n--- 4. Analyse d'ecoulement de puissance ---")
    lf = AnalyseLoadFlow()
    lf.ajouter_noeud('N1', 'SL', P=0, Q=0, V=1.0)
    lf.ajouter_noeud('N2', 'PQ', P=-50e6, Q=-20e6, V=0.97)
    lf.ajouter_ligne('N1', 'N2', R=2.5, X=8.0, B=5e-6)
    lf.calculer_courants()
    print(f"Noeud {list(lf.noeuds.keys())[0]}: V={lf.noeuds['N1']['V']:.2f} pu")
    print(f"Noeud N2: V={lf.noeuds['N2']['V']:.2f} pu, P={lf.noeuds['N2']['P']/1e6:.0f} MW")

    print("\n--- 5. Court-circuit ---")
    cc = CourtCircuit(S_cc=1000e6, V=63e3)
    print(f"I_cc initial: {cc.I_cc_ini():.0f} A")
    S_cc_ligne = cc.S_cc_ligne(15 + 1j*20)
    print(f"S_cc en bout de ligne: {S_cc_ligne/1e6:.1f} MVA")

if __name__ == '__main__':
    main()
