"""Projet: Mecanique generale
1AS6 - ENSEM NRJ (FISA)
Cinematique, dynamique du point et du solide, PFD, energie"""

import numpy as np

class Cinematique:
    @staticmethod
    def MRU(x0, v, t):
        return x0 + v*t

    @staticmethod
    def MRUV(x0, v0, a, t):
        return x0 + v0*t + 0.5*a*t**2

    @staticmethod
    def MCU(theta0, omega, t):
        return theta0 + omega*t

    @staticmethod
    def projectile(v0, theta, t):
        g = 9.81
        rad = np.deg2rad(theta)
        x = v0*np.cos(rad)*t
        y = v0*np.sin(rad)*t - 0.5*g*t**2
        return x, y

class DynamiquePoint:
    def __init__(self, m=1):
        self.m = m

    def PFD(self, F):
        return F / self.m

    def poids(self, g=9.81):
        return self.m * g

    def frottement_visqueux(self, v, k=0.1):
        return -k * v

    def ressort(self, x, k=100):
        return -k * x

class TravailEnergie:
    @staticmethod
    def travail(F, d, theta=0):
        return F * d * np.cos(np.deg2rad(theta))

    @staticmethod
    def energie_cinetique(m, v):
        return 0.5 * m * v**2

    @staticmethod
    def energie_potentielle_pesanteur(m, h, g=9.81):
        return m * g * h

    @staticmethod
    def energie_potentielle_ressort(k, x):
        return 0.5 * k * x**2

class DynamiqueSolide:
    def __init__(self, m=10, I=0.5):
        self.m = m
        self.I = I

    def moment_inertie_barre(self, L):
        self.I = self.m * L**2 / 12
        return self.I

    def moment_inertie_cylindre(self, R):
        self.I = 0.5 * self.m * R**2
        return self.I

    def PFD_rotation(self, M):
        return M / self.I

class Pendule:
    def __init__(self, L=1, m=1, theta0=10):
        self.L = L; self.m = m; self.g = 9.81
        self.theta0 = np.deg2rad(theta0)

    def periode_petites_oscillations(self):
        return 2*np.pi * np.sqrt(self.L/self.g)

    def position(self, t):
        omega = np.sqrt(self.g/self.L)
        return self.theta0 * np.cos(omega*t)

class Frottement:
    @staticmethod
    def Coulomb(Fn, mu=0.3):
        return mu * Fn

    @staticmethod
    def plan_incline(m, theta, mu=0.2):
        g = 9.81
        rad = np.deg2rad(theta)
        P_para = m*g*np.sin(rad)
        F_frot = mu*m*g*np.cos(rad)
        a = (P_para - F_frot) / m
        return {'a': a, 'P_para': P_para, 'F_frot': F_frot,
                'glisse': P_para > F_frot}

def main():
    print("=" * 60)
    print("Mecanique generale")
    print("1AS6 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Cinematique ---")
    t = np.array([0, 1, 2, 3, 4, 5])
    print("MRU (x0=0, v=5 m/s):")
    for ti in t:
        print(f"  t={ti}s: x={Cinematique.MRU(0, 5, ti):.0f}m")
    print("MRUV (x0=0, v0=10, a=-2 m/s2):")
    for ti in t:
        print(f"  t={ti}s: x={Cinematique.MRUV(0, 10, -2, ti):.0f}m")

    print("\n--- 2. Projectile ---")
    for t_m in np.linspace(0, 3, 7):
        x, y = Cinematique.projectile(20, 45, t_m)
        if y >= 0:
            print(f"  t={t_m:.1f}s: x={x:.1f}m, y={y:.1f}m")

    print("\n--- 3. Dynamique du point ---")
    dyn = DynamiquePoint(m=2)
    a = dyn.PFD(50)
    print(f"  F=50N, m=2kg: a={a:.1f} m/s2")
    print(f"  Poids: {dyn.poids():.1f} N")
    print(f"  Frottement visqueux (v=10): {dyn.frottement_visqueux(10):.1f} N")
    print(f"  Rappel ressort (x=0.1, k=200): {dyn.ressort(0.1, 200):.0f} N")

    print("\n--- 4. Travail et energie ---")
    te = TravailEnergie()
    print(f"  Travail (F=100N, d=5m): {te.travail(100, 5):.0f} J")
    print(f"  Ec (m=10kg, v=15): {te.energie_cinetique(10, 15):.0f} J")
    print(f"  Epp (m=10kg, h=20): {te.energie_potentielle_pesanteur(10, 20):.0f} J")
    print(f"  Epe (k=500, x=0.1): {te.energie_potentielle_ressort(500, 0.1):.0f} J")

    print("\n--- 5. Pendule simple ---")
    pen = Pendule(L=1.5, m=2, theta0=10)
    print(f"  Periode (L=1.5m): {pen.periode_petites_oscillations():.2f} s")
    for t_p in [0, 0.5, 1, 1.5, 2]:
        print(f"  t={t_p:.1f}s: theta={np.rad2deg(pen.position(t_p)):.1f} deg")

    print("\n--- 6. Frottement - Plan incline ---")
    for theta in [10, 20, 30, 45]:
        pi = Frottement.plan_incline(5, theta, mu=0.3)
        etat = "Glisse" if pi['glisse'] else "Immobile"
        print(f"  theta={theta:2d}: a={pi['a']:.2f} m/s2 ({etat})")

if __name__ == '__main__':
    main()
