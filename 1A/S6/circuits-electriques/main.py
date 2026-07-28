"""Projet: Circuits electriques
1AS6 - ENSEM NRJ (FISA)
Regime transitoire, regime sinusoidal, triphase, puissance"""

import numpy as np

class CircuitRC:
    def __init__(self, R=1000, C=1e-6):
        self.R = R
        self.C = C
        self.tau = R * C

    def charge(self, E, t):
        return E * (1 - np.exp(-t/self.tau))

    def decharge(self, V0, t):
        return V0 * np.exp(-t/self.tau)

    def i_charge(self, E, t):
        return E/self.R * np.exp(-t/self.tau)

class CircuitRL:
    def __init__(self, R=10, L=0.1):
        self.R = R
        self.L = L
        self.tau = L / R

    def etablissement(self, E, t):
        return E/self.R * (1 - np.exp(-t/self.tau))

    def extinction(self, I0, t):
        return I0 * np.exp(-t/self.tau)

class CircuitRLC:
    def __init__(self, R=100, L=0.1, C=1e-6):
        self.R = R; self.L = L; self.C = C
        self.omega0 = 1/np.sqrt(L*C)
        self.alpha = R/(2*L)
        self.zeta = self.alpha/self.omega0

    def reponse(self, V0, t):
        if self.zeta < 1:
            wd = self.omega0 * np.sqrt(1-self.zeta**2)
            return V0 * np.exp(-self.alpha*t) * (np.cos(wd*t) + self.alpha/wd*np.sin(wd*t))
        elif self.zeta == 1:
            return V0 * np.exp(-self.alpha*t) * (1 + self.alpha*t)
        else:
            r1 = -self.alpha + self.alpha*np.sqrt(1-1/self.zeta**2)
            r2 = -self.alpha - self.alpha*np.sqrt(1-1/self.zeta**2)
            A = V0 * r2/(r2-r1); B = V0 - A
            return A*np.exp(r1*t) + B*np.exp(r2*t)

class RegimeSinusoidal:
    def __init__(self, f=50):
        self.f = f
        self.w = 2*np.pi*f

    def impedance_RC(self, R, C):
        Z = R + 1/(1j*self.w*C)
        return abs(Z), np.angle(Z)

    def impedance_RL(self, R, L):
        Z = R + 1j*self.w*L
        return abs(Z), np.angle(Z)

    def resonance_RLC(self, R, L, C):
        omega0 = 1/np.sqrt(L*C)
        Z_min = R
        Q = 1/R * np.sqrt(L/C)
        return {'f0': omega0/(2*np.pi), 'Zmin': Z_min, 'Q': Q}

class Triphase:
    def __init__(self, V=230, f=50):
        self.V = V
        self.f = f

    def tensions(self):
        Va = self.V * np.sqrt(2)
        Vb = Va * np.exp(-1j*2*np.pi/3)
        Vc = Va * np.exp(1j*2*np.pi/3)
        return Va, Vb, Vc

    def V_composee(self):
        return self.V * np.sqrt(3)

    def puissance_active(self, I, cos_phi=0.85):
        return np.sqrt(3) * self.V * I * cos_phi

class PuissanceElectrique:
    @staticmethod
    def monophase(V, I, phi):
        P = V*I*np.cos(phi)
        Q = V*I*np.sin(phi)
        S = V*I
        return {'P': P, 'Q': Q, 'S': S, 'fp': np.cos(phi)}

    @staticmethod
    def triphase(V, I, cos_phi):
        return np.sqrt(3)*V*I*cos_phi

def main():
    print("=" * 60)
    print("Circuits electriques")
    print("1AS6 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Circuit RC - regime transitoire ---")
    rc = CircuitRC(R=1000, C=100e-6)
    print(f"Constante de temps tau = {rc.tau*1000:.1f} ms")
    for t in [0.001, 0.01, 0.05, 0.1, 0.3]:
        print(f"  t={t*1000:.0f}ms: Vc={rc.charge(12, t):.2f}V, i={rc.i_charge(12, t)*1000:.1f}mA")

    print("\n--- 2. Circuit RL - regime transitoire ---")
    rl = CircuitRL(R=100, L=0.5)
    print(f"Constante de temps tau = {rl.tau*1000:.1f} ms")
    for t in [0.001, 0.005, 0.01, 0.05]:
        print(f"  t={t*1000:.0f}ms: I={rl.etablissement(24, t)*1000:.1f}mA")

    print("\n--- 3. Circuit RLC - amortissement ---")
    rlc_amort = CircuitRLC(R=200, L=0.1, C=10e-6)
    print(f"RLC: f0={rlc_amort.omega0/(2*np.pi):.0f} Hz, zeta={rlc_amort.zeta:.2f}")
    regime = "Pseudo-periodique" if rlc_amort.zeta < 1 else ("Critique" if rlc_amort.zeta == 1 else "Aperiodique")
    print(f"  Regime: {regime}")
    for t in [0.001, 0.005, 0.01, 0.02]:
        print(f"  t={t*1000:.0f}ms: V={rlc_amort.reponse(100, t):.1f}V")

    print("\n--- 4. Regime sinusoidal ---")
    rs = RegimeSinusoidal(f=50)
    Z, phi = rs.impedance_RC(100, 10e-6)
    print(f"  RC (R=100, C=10uF) a 50Hz: |Z|={Z:.0f} ohms, phi={np.rad2deg(phi):.1f} deg")
    Z, phi = rs.impedance_RL(10, 0.1)
    print(f"  RL (R=10, L=100mH) a 50Hz: |Z|={Z:.1f} ohms, phi={np.rad2deg(phi):.1f} deg")
    res = rs.resonance_RLC(10, 0.1, 100e-6)
    print(f"  RLC resonance: f0={res['f0']:.0f} Hz, Q={res['Q']:.1f}")

    print("\n--- 5. Triphase ---")
    tri = Triphase(V=230)
    print(f"V simple = {tri.V} V, V composee = {tri.V_composee():.0f} V")
    for I in [10, 50, 100]:
        P = tri.puissance_active(I)
        print(f"  I={I}A, cos_phi=0.85: P={P/1000:.1f} kW")

    print("\n--- 6. Puissance electrique ---")
    p = PuissanceElectrique.monophase(230, 10, np.deg2rad(30))
    print(f"Monophase (230V, 10A, phi=30): P={p['P']:.0f}W, Q={p['Q']:.0f}VAR, S={p['S']:.0f}VA")

if __name__ == '__main__':
    main()
