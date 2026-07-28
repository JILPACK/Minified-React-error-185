"""Projet: Physique - Mecanique
1AS5 - ENSEM NRJ (FISA)
Mecanique du point, optique geometrique, oscillateurs, ondes"""

import numpy as np
import math

class MecaniquePoint:
    @staticmethod
    def position_MRU(x0, v, t):
        return x0 + v*t

    @staticmethod
    def position_MRUV(x0, v0, a, t):
        return x0 + v0*t + 0.5*a*t**2

    @staticmethod
    def chute_libre(h0, t, g=9.81):
        return h0 - 0.5*g*t**2

    @staticmethod
    def vitesse_chute(t, g=9.81):
        return g*t

    @staticmethod
    def parabole(v0, angle_deg, t):
        a = np.deg2rad(angle_deg)
        x = v0*np.cos(a)*t
        y = v0*np.sin(a)*t - 0.5*9.81*t**2
        return x, y

class OptiqueGeometrique:
    @staticmethod
    def refraction(n1, n2, theta1_deg):
        t1 = np.deg2rad(theta1_deg)
        sin_t2 = n1/n2 * np.sin(t1)
        if sin_t2 > 1:
            return None
        return np.rad2deg(np.arcsin(sin_t2))

    @staticmethod
    def lentille_mince(f, p):
        if p == 0: return None
        return 1/(1/f + 1/p)  # p: distance objet

    @staticmethod
    def grandissement(f, p):
        q = OptiqueGeometrique.lentille_mince(f, p)
        return -q/p if p else None

class Oscillateur:
    def __init__(self, m=1, k=100):
        self.m = m
        self.k = k
        self.omega0 = np.sqrt(k/m)
        self.f0 = self.omega0/(2*np.pi)
        self.T = 1/self.f0

    def position(self, t, x0=0.1, v0=0):
        A = np.sqrt(x0**2 + (v0/self.omega0)**2)
        phi = np.arctan2(v0, self.omega0*x0)
        return A*np.cos(self.omega0*t - phi)

    def energie_cinetique(self, t, x0=0.1, v0=0):
        v = -self.omega0*self.position(t, x0, v0)
        return 0.5*self.m*v**2

class Ondes:
    @staticmethod
    def sinusoidale(A, f, t, phi=0):
        return A*np.sin(2*np.pi*f*t + phi)

    @staticmethod
    def battement(f1, f2, A=1, t=None):
        if t is None:
            t = np.linspace(0, 2, 500)
        return A*(np.sin(2*np.pi*f1*t) + np.sin(2*np.pi*f2*t))

def main():
    print("=" * 60)
    print("Physique - Mecanique")
    print("1AS5 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Mecanique du point ---")
    mc = MecaniquePoint()
    for t in [0, 1, 2, 3]:
        x = mc.position_MRU(0, 10, t)
        print(f"  MRU (v=10): t={t}s, x={x}m")

    print("\n  Chute libre (h0=50m):")
    for t in np.linspace(0, 3, 4):
        h = mc.chute_libre(50, t)
        v = mc.vitesse_chute(t)
        if h >= 0:
            print(f"  t={t:.1f}s: h={h:.1f}m, v={v:.1f}m/s")

    print("\n  Parabole (v0=30m/s, angle=45):")
    for t in np.arange(0, 5, 1):
        x, y = mc.parabole(30, 45, t)
        if y >= 0:
            print(f"  t={t:.0f}s: x={x:.1f}m, y={y:.1f}m")

    print("\n--- 2. Optique geometrique ---")
    og = OptiqueGeometrique()
    for angle in [0, 20, 40, 60]:
        t2 = og.refraction(1.0, 1.5, angle)
        if t2:
            print(f"  Air->Verre (n1=1, n2=1.5): i={angle} -> r={t2:.1f} deg")
        else:
            print(f"  Air->Verre: i={angle} -> Reflexion totale")

    print("\n  Lentille convergente (f=10cm):")
    for p in [5, 10, 20, 50]:
        q = og.lentille_mince(10, p)
        G = og.grandissement(10, p)
        if q:
            print(f"  p={p}cm: q={q:.1f}cm, G={G:.2f}")
        else:
            print(f"  p={p}cm: image a l'infini")

    print("\n--- 3. Oscillateur harmonique ---")
    osc = Oscillateur(m=0.5, k=100)
    print(f"  m=0.5kg, k=100N/m")
    print(f"  omega0={osc.omega0:.1f} rad/s, T={osc.T:.3f}s")
    for t in [0, 0.05, 0.1, 0.2, 0.3]:
        x = osc.position(t, 0.05, 0)
        Ec = osc.energie_cinetique(t, 0.05, 0)
        print(f"  t={t:.3f}s: x={x*1000:.1f}mm, Ec={Ec:.3f}J")

    print("\n--- 4. Ondes ---")
    onde = Ondes()
    for t in [0, 0.01, 0.02, 0.05]:
        y = onde.sinusoidale(2, 50, t)
        print(f"  A=2, f=50Hz, t={t:.3f}s: y={y:.3f}")
    print(f"  Battement (f1=440Hz, f2=444Hz): 2 sources")

if __name__ == '__main__':
    main()
