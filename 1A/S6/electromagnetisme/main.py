"""Projet: Electromagnetisme
1AS6 - ENSEM NRJ (FISA)
Champs electrique et magnetique, induction, equations de Maxwell"""

import numpy as np

class ChampElectrique:
    def __init__(self, epsilon0=8.854e-12):
        self.eps0 = epsilon0
        self.k = 1/(4*np.pi*epsilon0)

    def charge_ponctuelle(self, Q, r):
        return self.k * Q / r**2

    def dipoles(self, p, r, theta):
        Er = 2*self.k * p*np.cos(theta) / r**3
        Et = self.k * p*np.sin(theta) / r**3
        return np.sqrt(Er**2 + Et**2)

class PotentielElectrique:
    @staticmethod
    def charge_ponctuelle(Q, r):
        k = 9e9
        return k * Q / r

    @staticmethod
    def condensateur_plan(Q, S, d, eps_r=1):
        eps0 = 8.854e-12
        C = eps0 * eps_r * S / d
        V = Q / C
        E = V / d
        return {'C': C, 'V': V, 'E': E}

class ChampMagnetique:
    def __init__(self, mu0=4*np.pi*1e-7):
        self.mu0 = mu0

    def fil_infini(self, I, r):
        return self.mu0 * I / (2*np.pi*r)

    def solenoide(self, I, N, L):
        return self.mu0 * N * I / L

    def force_laplace(self, I, L, B, theta=90):
        return I * L * B * np.sin(np.deg2rad(theta))

class InductionElectromagnetique:
    def __init__(self):
        self.phi = 0

    def flux(self, B, S, theta=0):
        return B * S * np.cos(np.deg2rad(theta))

    def force_electromotrice(self, dphi_dt):
        return -dphi_dt

class CircuitMagnetique:
    def __init__(self, l=0.5, S=1e-4, mu_r=1000):
        self.l = l
        self.S = S
        self.mu_r = mu_r
        self.mu0 = 4*np.pi*1e-7

    def reluctance(self):
        return self.l / (self.mu0 * self.mu_r * self.S)

    def inductance(self, N):
        return N**2 / self.reluctance()

class OndeEM:
    def __init__(self, f=1e6):
        self.f = f
        self.c = 3e8
        self.lmbda = self.c / f

    def impedance_vide(self):
        return np.sqrt(4*np.pi*1e-7 / 8.854e-12)

def main():
    print("=" * 60)
    print("Electromagnetisme")
    print("1AS6 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Champ electrique ---")
    ce = ChampElectrique()
    for r in [0.1, 0.5, 1, 5]:
        E = ce.charge_ponctuelle(1e-6, r)
        print(f"  r={r:.1f}m: E={E:.0f} V/m")
    print(f"  Dipole (p=1e-9 C.m, r=1m, 90deg): E={ce.dipoles(1e-9, 1, np.pi/2):.1f} V/m")

    print("\n--- 2. Potentiel et condensateur ---")
    pe = PotentielElectrique()
    V = pe.charge_ponctuelle(1e-6, 0.5)
    print(f"  Potentiel a 0.5m (Q=1uC): V={V:.0f} V")
    cp = pe.condensateur_plan(1e-6, 0.01, 0.001, 2)
    print(f"  Condensateur plan (eps_r=2):")
    print(f"    C={cp['C']*1e9:.1f} nF, V={cp['V']:.1f} V, E={cp['E']/1e3:.1f} kV/m")

    print("\n--- 3. Champ magnetique ---")
    cm = ChampMagnetique()
    print(f"  Fil infini (I=10A, r=0.1m): B={cm.fil_infini(10, 0.1)*1e6:.1f} uT")
    print(f"  Solenoide (I=5A, N=500, L=0.3m): B={cm.solenoide(5, 500, 0.3)*1e3:.0f} mT")
    print(f"  Force Laplace (I=10A, L=0.2m, B=1T): F={cm.force_laplace(10, 0.2, 1):.1f} N")

    print("\n--- 4. Induction electromagnetique ---")
    ind = InductionElectromagnetique()
    phi = ind.flux(0.5, 0.1)
    print(f"  Flux (B=0.5T, S=0.1m2): phi={phi:.3f} Wb")
    fem = ind.force_electromotrice(50)
    print(f"  FEM (dphi/dt=50 Wb/s): e={fem:.0f} V")

    print("\n--- 5. Circuit magnetique ---")
    cmag = CircuitMagnetique(l=0.2, S=1e-4, mu_r=1500)
    R = cmag.reluctance()
    L = cmag.inductance(100)
    print(f"  Reluctance: R={R:.0f} A/Wb")
    print(f"  Inductance (N=100): L={L*1000:.1f} mH")
    L2 = cmag.inductance(200)
    print(f"  Inductance (N=200): L={L2*1000:.1f} mH")

    print("\n--- 6. Propagation ondes EM ---")
    onde = OndeEM(f=100e6)
    print(f"  f=100 MHz: lambda={onde.lmbda:.2f} m")
    print(f"  Impedance du vide: Z0={onde.impedance_vide():.0f} ohms")

if __name__ == '__main__':
    main()
