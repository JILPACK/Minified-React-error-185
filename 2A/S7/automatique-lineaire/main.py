"""Projet: Automatique lineaire
2AS7 - ENSEM NRJ (FISA)
Fonctions de transfert, Bode, stabilite, PID, asservissement"""

import numpy as np
import matplotlib.pyplot as plt

class FonctionTransfert:
    def __init__(self, num, den):
        self.num = np.array(num, dtype=float)
        self.den = np.array(den, dtype=float)

    def gain_static(self):
        return self.num[-1] / self.den[-1] if self.den[-1] != 0 else 0

    def poles(self):
        return np.roots(self.den)

    def zeros(self):
        return np.roots(self.num)

    def evalue(self, s):
        return np.polyval(self.num, s) / np.polyval(self.den, s)

class SystemeOrdre1(FonctionTransfert):
    def __init__(self, K=1.0, tau=1.0):
        super().__init__([K], [tau, 1])
        self.K = K; self.tau = tau

    def reponse_indicielle(self, t):
        return self.K * (1 - np.exp(-t/self.tau))

    def temps_montee(self):
        return self.tau * np.log(9)

    def temps_reponse_5(self):
        return 3 * self.tau

class SystemeOrdre2(FonctionTransfert):
    def __init__(self, K=1.0, omega0=10, zeta=0.7):
        super().__init__([K*omega0**2], [1, 2*zeta*omega0, omega0**2])
        self.K = K; self.omega0 = omega0; self.zeta = zeta

    def reponse_indicielle(self, t):
        if self.zeta < 1:
            wd = self.omega0 * np.sqrt(1 - self.zeta**2)
            phi = np.arctan2(np.sqrt(1-self.zeta**2), self.zeta)
            return self.K * (1 - np.exp(-self.zeta*self.omega0*t) * np.sin(wd*t+phi) / np.sqrt(1-self.zeta**2))
        elif self.zeta == 1:
            return self.K * (1 - (1+self.omega0*t)*np.exp(-self.omega0*t))
        else:
            return self.K * (1 - np.exp(-self.zeta*self.omega0*t) * np.cosh(self.omega0*np.sqrt(self.zeta**2-1)*t))

    def depassement(self):
        if self.zeta < 1:
            return 100 * np.exp(-np.pi*self.zeta/np.sqrt(1-self.zeta**2))
        return 0

class DiagrammeBode:
    def __init__(self, num, den):
        self.ft = FonctionTransfert(num, den)

    def gain_dB(self, f):
        s = 1j*2*np.pi*f
        G = self.ft.evalue(s)
        return 20*np.log10(abs(G))

class CorrecteurPID:
    def __init__(self, Kp=1.0, Ki=0, Kd=0):
        self.Kp = Kp; self.Ki = Ki; self.Kd = Kd
        self.I = 0; self.e_prev = 0

    def calculer(self, e, dt=0.01):
        self.I += e * dt
        D = (e - self.e_prev) / dt if dt > 0 else 0
        self.e_prev = e
        return self.Kp*e + self.Ki*self.I + self.Kd*D

class LieuRacines:
    @staticmethod
    def tracer(K_range, num, den):
        racines = []
        for K in K_range:
            den_K = den.copy()
            den_K[-1] += K * num[-1] if len(num) <= len(den) else 0
            racines.append(np.roots(den_K))
        return racines

def main():
    print("=" * 60)
    print("Automatique lineaire")
    print("2AS7 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Systeme du 1er ordre ---")
    s1 = SystemeOrdre1(K=2.5, tau=2.0)
    t = np.linspace(0, 12, 60)
    print(f"Gain statique: {s1.gain_static()}")
    print(f"Constante temps: {s1.tau} s")
    print(f"Pole: {s1.poles()[0]:.2f}")
    print(f"Temps montee: {s1.temps_montee():.2f} s")
    print(f"Temps reponse 5%: {s1.temps_reponse_5():.2f} s")
    for ti in [1, 2, 5, 10]:
        print(f"  t={ti:.0f}s: y={s1.reponse_indicielle(ti):.3f}")

    print("\n--- 2. Systeme du 2nd ordre ---")
    s2 = SystemeOrdre2(K=1, omega0=5, zeta=0.3)
    print(f"Omega0={s2.omega0} rad/s, zeta={s2.zeta}")
    print(f"Depassement: {s2.depassement():.1f}%")
    poles = s2.poles()
    for i, p in enumerate(poles):
        print(f"  Pole {i+1}: {p.real:.2f} + j{p.imag:.2f}")

    s2b = SystemeOrdre2(K=1, omega0=5, zeta=0.7)
    print(f"\nDepassement (zeta=0.7): {s2b.depassement():.1f}%")

    print("\n--- 3. Diagramme de Bode ---")
    bode = DiagrammeBode([100], [1, 10, 100])
    for f in [0.1, 0.5, 1, 5, 10, 50]:
        Gdb = bode.gain_dB(f)
        print(f"  f={f:.1f} Hz: G={Gdb:.1f} dB")

    print("\n--- 4. Correcteur PID ---")
    pid = CorrecteurPID(Kp=2.0, Ki=0.5, Kd=0.1)
    process = lambda y, u: y + 0.1*(u - y)
    y = 0; SP = 1
    print(f"{'t(s)':<8} {'PV':<8} {'MV':<8}")
    for k in range(50):
        e = SP - y
        MV = pid.calculer(e)
        y = process(y, MV)
        if k % 10 == 0:
            print(f"{k*0.01:<8.2f} {y:<8.3f} {MV:<8.3f}")
    print(f"PV finale: {y:.3f}")

    print("\n--- 5. Lieu des racines ---")
    lr = LieuRacines()
    racines = lr.tracer(np.linspace(0, 50, 10), [1], [1, 5, 6])
    for i, r in enumerate(racines):
        print(f"  K={i*50/9:.1f}: poles = {r[0]:.2f}, {r[1]:.2f}")

if __name__ == '__main__':
    main()
