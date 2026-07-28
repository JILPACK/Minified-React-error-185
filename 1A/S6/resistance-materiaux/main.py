"""Projet: Resistance des materiaux
1AS6 - ENSEM NRJ (FISA)
Traction, compression, flexion, torsion, flambage"""

import numpy as np

class TractionCompression:
    def __init__(self, E=210e9, A=0.001):
        self.E = E
        self.A = A

    def contrainte(self, F):
        return F / self.A

    def deformation(self, F):
        return self.contrainte(F) / self.E

    def allongement(self, F, L):
        return self.deformation(F) * L

class FlexionPoutre:
    def __init__(self, E=210e9, b=0.1, h=0.2):
        self.E = E
        self.b = b
        self.h = h
        self.I = b * h**3 / 12

    def contrainte_max(self, Mf):
        return Mf * self.h/2 / self.I

    def fleche_console(self, F, L):
        return F * L**3 / (3 * self.E * self.I)

    def fleche_appuis(self, F, L):
        return F * L**3 / (48 * self.E * self.I)

    def fleche_repartie(self, q, L):
        return 5 * q * L**4 / (384 * self.E * self.I)

class Torsion:
    def __init__(self, G=80e9, d=0.05):
        self.G = G
        self.d = d
        self.I0 = np.pi * d**4 / 32

    def contrainte_max(self, Mt):
        return Mt * self.d/2 / self.I0

    def angle_unitaire(self, Mt):
        return Mt / (self.G * self.I0)

    def angle_total(self, Mt, L):
        return self.angle_unitaire(Mt) * L

class FlambageEuler:
    def __init__(self, E=210e9, section='rect', b=0.05, h=0.05):
        self.E = E
        if section == 'rect':
            self.I = b * h**3 / 12
        elif section == 'circ':
            self.I = np.pi * b**4 / 64

    def charge_critique(self, L, mu=1):
        return np.pi**2 * self.E * self.I / (mu * L)**2

    def elancement(self, L, i):
        return L / i

class EtatContrainte:
    @staticmethod
    def traction_simple(sig_x):
        return {'sig1': sig_x, 'sig2': 0, 'tau_max': sig_x/2}

    @staticmethod
    def cisaillement_pur(tau):
        return {'sig1': tau, 'sig2': -tau, 'tau_max': tau}

    @staticmethod
    def VonMises(sig_x, sig_y, tau_xy):
        return np.sqrt(sig_x**2 + sig_y**2 - sig_x*sig_y + 3*tau_xy**2)

def main():
    print("=" * 60)
    print("Resistance des materiaux")
    print("1AS6 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Traction simple ---")
    tc = TractionCompression(E=210e9, A=0.002)
    for F in [10000, 50000, 100000]:
        print(f"  F={F/1000:.0f} kN: sig={tc.contrainte(F)/1e6:.1f} MPa, "
              f"eps={tc.deformation(F)*100:.3f}%, dL={tc.allongement(F, 3)*1000:.2f} mm")

    print("\n--- 2. Flexion poutre ---")
    fp = FlexionPoutre(E=210e9, b=0.1, h=0.3)
    Mf = 50000
    print(f"  Poutre b={fp.b*1000:.0f}mm x h={fp.h*1000:.0f}mm, I={fp.I*1e8:.2f} cm4")
    print(f"  Contrainte max (Mf={Mf} Nm): {fp.contrainte_max(Mf)/1e6:.1f} MPa")
    print(f"  Fleche console (F=5kN, L=2m): {fp.fleche_console(5000, 2)*1000:.2f} mm")
    print(f"  Fleche appuis (F=5kN, L=2m): {fp.fleche_appuis(5000, 2)*1000:.2f} mm")
    print(f"  Fleche charge repartie (q=2kN/m, L=2m): {fp.fleche_repartie(2000, 2)*1000:.2f} mm")

    print("\n--- 3. Torsion ---")
    tor = Torsion(G=80e9, d=0.04)
    for Mt in [100, 500, 1000]:
        print(f"  Mt={Mt} Nm: tau_max={tor.contrainte_max(Mt)/1e6:.1f} MPa, "
              f"theta={tor.angle_total(Mt, 1):.4f} rad ({np.rad2deg(tor.angle_total(Mt, 1)):.1f} deg/m)")

    print("\n--- 4. Flambage d'Euler ---")
    fl = FlambageEuler(E=70e9, section='circ', b=0.03)
    print(f"  Aluminium E=70 GPa, d=30mm")
    for L, mu in [(1, 1), (2, 1), (2, 0.5), (3, 2)]:
        F_crit = fl.charge_critique(L, mu)
        print(f"  L={L}m, mu={mu}: F_crit={F_crit/1000:.1f} kN")

    print("\n--- 5. Criteres de resistance ---")
    ec = EtatContrainte()
    ts = ec.traction_simple(150e6)
    print(f"  Traction simple (150 MPa): sig1={ts['sig1']/1e6:.0f} MPa, tau_max={ts['tau_max']/1e6:.0f} MPa")
    cp = ec.cisaillement_pur(80e6)
    print(f"  Cisaillement pur (80 MPa): sig1={cp['sig1']/1e6:.0f} MPa, sig2={cp['sig2']/1e6:.0f} MPa")
    vm = ec.VonMises(120e6, 40e6, 30e6)
    print(f"  Von Mises (120, 40, 30 MPa): sig_vm={vm/1e6:.1f} MPa")

if __name__ == '__main__':
    main()
