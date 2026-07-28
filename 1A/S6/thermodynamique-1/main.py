"""Projet: Thermodynamique 1
1AS6 - ENSEM NRJ (FISA)
Premier et second principes, gaz parfaits, bilans d'energie"""

import numpy as np

class FluideThermo:
    def __init__(self, nom, R=287, cp=1005, cv=718, gamma=1.4):
        self.nom = nom
        self.R = R
        self.cp = cp
        self.cv = cv
        self.gamma = gamma

class TransformationsThermo:
    def __init__(self, fluide=None):
        self.fluide = fluide or FluideThermo("Air")

    def detente(self, P1, V1, T1, P2=None, V2=None, n=None):
        if n is None:
            n = self.fluide.gamma
        P1, V1, T1 = float(P1), float(V1), float(T1)
        if P2 and not V2:
            V2 = V1 * (P1/P2)**(1/n)
            T2 = T1 * (P2/P1)**((n-1)/n)
        elif V2 and not P2:
            P2 = P1 * (V1/V2)**n
            T2 = T1 * (V1/V2)**(n-1)
        else:
            return None
        m = P1*V1/(self.fluide.R*T1)
        if n == 1:
            W = m*self.fluide.R*T1*np.log(V2/V1)
        elif n == self.fluide.gamma:
            W = (P2*V2 - P1*V1)/(1-n)
        else:
            W = (P2*V2 - P1*V1)/(1-n)
        return {'P2': P2, 'V2': V2, 'T2': T2, 'W': W, 'm': m}

class BilanEnergie:
    @staticmethod
    def systeme_ferme(dU, W, Q):
        return dU == Q - W

    @staticmethod
    def chauffe_eau(m, T1, T2, cp_eau=4180):
        Q = m * cp_eau * (T2 - T1)
        return Q / 1e3  # kJ

class CycleSimple:
    def __init__(self, fluide=None):
        self.fluide = fluide or FluideThermo("Air")
        self.etats = []
        self.W = 0
        self.Q = 0

    def ajouter_etat(self, P, V, T):
        self.etats.append({'P': P, 'V': V, 'T': T})

    def travail_cycle(self):
        if len(self.etats) < 3:
            return 0
        n = len(self.etats)
        W = 0
        for i in range(n):
            j = (i+1) % n
            Pi, Vi = self.etats[i]['P'], self.etats[i]['V']
            Pj, Vj = self.etats[j]['P'], self.etats[j]['V']
            W += (Pi + Pj) * (Vj - Vi) / 2
        return W

class ChangementEtat:
    def __init__(self, Lv=2260e3, Lf=334e3, cp_eau=4180, cp_glace=2090):
        self.Lv = Lv; self.Lf = Lf
        self.cp_eau = cp_eau; self.cp_glace = cp_glace

    def chauffe_glace(self, m, T1, T2):
        if T2 <= 0:
            return m * self.cp_glace * (T2 - T1)
        if T1 < 0 < T2:
            Q1 = m * self.cp_glace * (0 - T1)
            Q2 = m * self.Lf
            Q3 = m * self.cp_eau * (T2 - 0)
            return Q1 + Q2 + Q3
        return m * self.cp_eau * (T2 - T1)

def main():
    print("=" * 60)
    print("Thermodynamique 1")
    print("1AS6 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Fluides et gaz parfaits ---")
    air = FluideThermo("Air", R=287, cp=1005, cv=718, gamma=1.4)
    eau = FluideThermo("Vapeur", R=462, cp=1870, cv=1408, gamma=1.33)
    print(f"Air: R={air.R} J/kgK, cp={air.cp} J/kgK, gamma={air.gamma}")
    print(f"Vapeur: R={eau.R} J/kgK, cp={eau.cp} J/kgK, gamma={eau.gamma}")

    print("\n--- 2. Transformations ---")
    trans = TransformationsThermo(air)
    # Detente isotherme
    res = trans.detente(2e5, 0.5, 300, V2=1.0, n=1)
    if res: print(f"Detente isotherme: P2={res['P2']/1e5:.2f} bar, T2={res['T2']:.0f} K, W={res['W']/1000:.1f} kJ")
    # Detente adiabatique
    res = trans.detente(2e5, 0.5, 300, V2=1.0, n=air.gamma)
    if res: print(f"Detente adiabatique: P2={res['P2']/1e5:.2f} bar, T2={res['T2']:.0f} K, W={res['W']/1000:.1f} kJ")
    # Compression isotherme
    res = trans.detente(1e5, 1.0, 300, V2=0.5, n=1)
    if res: print(f"Compression isotherme: P2={res['P2']/1e5:.1f} bar, W={res['W']/1000:.1f} kJ")

    print("\n--- 3. Bilan d'energie ---")
    be = BilanEnergie()
    Q = be.chauffe_eau(50, 15, 60)
    print(f"Chauffage 50L eau 15->60C: Q={Q:.0f} kJ")
    Q2 = be.chauffe_eau(50, 60, 90)
    print(f"Chauffage 50L eau 60->90C: Q={Q2:.0f} kJ")

    print("\n--- 4. Cycle thermodynamique ---")
    cyc = CycleSimple(air)
    cyc.ajouter_etat(1e5, 1, 300)
    cyc.ajouter_etat(5e5, 1, 1500)
    cyc.ajouter_etat(1e5, 5, 1500)
    W = cyc.travail_cycle()
    print(f"Cycle a 3 points: W_net = {W/1000:.1f} kJ")

    print("\n--- 5. Changement d'etat ---")
    ce = ChangementEtat()
    Q_glace = ce.chauffe_glace(1, -10, 20)
    print(f"Chauffe 1kg glace -10C -> eau 20C: Q={Q_glace/1000:.0f} kJ")
    Q_vap = ce.chauffe_glace(1, 0, 100) + 1*2260
    print(f"1kg eau 0C -> vapeur 100C: Q={Q_vap/1000:.0f} kJ")

    print("\n--- 6. Second principe ---")
    T1, T2 = 500, 300
    eta_carnot = 1 - T2/T1
    print(f"Rendement Carnot (T1=500K, T2=300K): {eta_carnot:.1%}")

if __name__ == '__main__':
    main()
