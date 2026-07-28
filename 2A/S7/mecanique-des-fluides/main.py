"""Projet: Mecanique des fluides
2AS7 - ENSEM NRJ (FISA)
Ecoulements incompressibles, pertes de charge, similitudes"""

import numpy as np

class Fluide:
    def __init__(self, nom, rho=1000, mu=1e-3, nu=None):
        self.nom = nom
        self.rho = rho
        self.mu = mu
        self.nu = nu if nu else mu / rho

class EcoulementConduite:
    def __init__(self, D=0.1, L=10, fluide=None):
        self.D = D
        self.R = D/2
        self.L = L
        self.A = np.pi * D**2 / 4
        self.fluide = fluide or Fluide("Eau")

    def vitesse_debit(self, Q):
        return Q / self.A

    def Re(self, Q):
        V = self.vitesse_debit(Q)
        return V * self.D / self.fluide.nu

    def perte_charge_lineaire(self, Q, epsilon=0.046e-3):
        V = self.vitesse_debit(Q)
        Re = self.Re(Q)
        if Re < 2000:
            f = 64 / Re
        else:
            from scipy.optimize import fsolve
            def eq(f):
                return 1/np.sqrt(f) + 2*np.log10(epsilon/self.D/3.7 + 2.51/(Re*np.sqrt(f)))
            try: f = fsolve(eq, 0.02)[0]
            except: f = 0.02
        dh = f * self.L / self.D * V**2 / (2*9.81)
        dp = f * self.L / self.D * self.fluide.rho * V**2 / 2
        return {'f': f, 'dh': dh, 'dp': dp/1e5, 'Re': Re}

class EcoulementCoucheLimite:
    def __init__(self, U_inf=10, L=2, nu=1e-5):
        self.U_inf = U_inf
        self.L = L
        self.nu = nu

    def epaisseur_couche_limite(self, x):
        return 5.0 * x / np.sqrt(self.U_inf * x / self.nu)

    def contrainte_paroi(self, x):
        cf = 0.664 / np.sqrt(self.U_inf * x / self.nu)
        return cf * 0.5 * 1.2 * self.U_inf**2

class TubeVenturi:
    def __init__(self, D1=0.1, D2=0.05, beta=None):
        self.D1 = D1; self.D2 = D2
        self.A1 = np.pi*D1**2/4; self.A2 = np.pi*D2**2/4
        self.beta = beta or D2/D1

    def debit(self, dp, rho=1000, Cd=0.98):
        return Cd * self.A2 / np.sqrt(1 - self.beta**4) * np.sqrt(2*dp/rho)

class PertesChargeSingulieres:
    @staticmethod
    def coude(K=0.5, V=2, rho=1000):
        return K * rho * V**2 / 2

    @staticmethod
    def vanne(ouverture_pct, V=2, rho=1000):
        K = max(0.2, 10 * (1 - ouverture_pct/100))
        return K * rho * V**2 / 2

def main():
    print("=" * 60)
    print("Mecanique des fluides")
    print("2AS7 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Pertes de charge en conduite ---")
    eau = Fluide("Eau", rho=1000, mu=1e-3)
    cond = EcoulementConduite(D=0.15, L=50, fluide=eau)
    Q = 0.03  # m3/s
    res = cond.perte_charge_lineaire(Q)
    print(f"Conduite D={cond.D*1000:.0f}mm, L={cond.L:.0f}m, Q={Q*1000:.1f} L/s")
    print(f"  Vitesse: {cond.vitesse_debit(Q):.2f} m/s")
    print(f"  Re: {res['Re']:.0f}")
    print(f"  f: {res['f']:.4f}")
    print(f"  Perte de charge: {res['dh']:.2f} mCE ({res['dp']:.2f} bar)")

    print("\n--- 2. Couche limite sur plaque plane ---")
    cl = EcoulementCoucheLimite(U_inf=15, L=1.5, nu=1.5e-5)
    for x in [0.1, 0.5, 1.0, 1.5]:
        d = cl.epaisseur_couche_limite(x)
        tau = cl.contrainte_paroi(x)
        print(f"  x={x:.1f}m: delta={d*1000:.1f}mm, tau_paroi={tau:.3f}Pa")

    print("\n--- 3. Tube de Venturi ---")
    vent = TubeVenturi(D1=0.1, D2=0.04)
    for dp in [5000, 10000, 20000]:
        Q = vent.debit(dp)
        print(f"  dp={dp/1000:.1f} kPa -> Q={Q*1000:.1f} L/s")

    print("\n--- 4. Pertes de charge singulieres ---")
    pcs = PertesChargeSingulieres()
    print(f"  Coude standard (V=3m/s): {pcs.coude(0.5, 3)/1000:.1f} kPa")
    print(f"  Vanne 50% (V=3m/s): {pcs.vanne(50, 3)/1000:.1f} kPa")
    print(f"  Vanne 25% (V=3m/s): {pcs.vanne(25, 3)/1000:.1f} kPa")

    print("\n--- 5. Analyse dimensionnelle - Nombre de Reynolds ---")
    for (D, V, nu) in [(0.1, 0.5, 1e-6), (0.05, 2, 1e-6), (0.02, 5, 1e-6)]:
        Re = V*D/nu
        regime = "Turbulent" if Re > 4000 else ("Laminaire" if Re < 2000 else "Transition")
        print(f"  D={D*1000:.0f}mm, V={V:.1f}m/s -> Re={Re:.0f} ({regime})")

if __name__ == '__main__':
    main()
