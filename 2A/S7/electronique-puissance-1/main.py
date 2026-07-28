"""Projet: Electronique de puissance 1
2AS7 - ENSEM NRJ (FISA)
Diodes, thyristors, redresseurs, hacheurs, onduleurs"""

import numpy as np

class Diode:
    def __init__(self, Vf=0.7, If_max=10, Vr_max=1000):
        self.Vf = Vf
        self.If_max = If_max
        self.Vr_max = Vr_max

    def conduit(self, Va, Vk):
        return (Va - Vk) > self.Vf

class Thyristor:
    def __init__(self, Vf=1.2, If_max=50, Vr_max=1200):
        self.Vf = Vf
        self.If_max = If_max
        self.Vr_max = Vr_max
        self.amorce = False

    def amorcer(self, angle):
        self.amorce = True
        self.angle_amorce = angle

    def bloquer(self):
        self.amorce = False

class RedresseurMonophase:
    def __init__(self, V_s=230, f=50):
        self.V_s = V_s
        self.f = f
        self.w = 2*np.pi*f

    def simple_alternance(self, R=10):
        Vm = self.V_s * np.sqrt(2)
        Vmoy = Vm / np.pi
        Imoy = Vmoy / R
        return {'Vmoy': Vmoy, 'Imoy': Imoy, 'Veff': Vm/2, 'P': Vmoy*Imoy}

    def double_alternance(self, R=10):
        Vm = self.V_s * np.sqrt(2)
        Vmoy = 2*Vm / np.pi
        Imoy = Vmoy / R
        return {'Vmoy': Vmoy, 'Imoy': Imoy, 'Veff': Vm/np.sqrt(2), 'P': Vmoy*Imoy}

    def commande_angle(self, alpha_deg, R=10):
        alpha = np.deg2rad(alpha_deg)
        Vm = self.V_s * np.sqrt(2)
        Vmoy = Vm/(2*np.pi) * (1 + np.cos(alpha))
        return {'Vmoy': Vmoy, 'alpha': alpha_deg}

class RedresseurTriphase:
    def __init__(self, V_s=400, f=50):
        self.V_s = V_s
        self.f = f

    def pont_P3(self, R=10):
        Vm = self.V_s * np.sqrt(2) / np.sqrt(3)
        Vmoy = 3*np.sqrt(3)*Vm / (2*np.pi)
        return {'Vmoy': Vmoy, 'Imoy': Vmoy/R, 'V_phase': Vm/np.sqrt(2)}

    def pont_P6(self, R=10):
        Vm = self.V_s * np.sqrt(2) / np.sqrt(3)
        Vmoy = 3*np.sqrt(3)*Vm / np.pi
        return {'Vmoy': Vmoy, 'Imoy': Vmoy/R}

class Hacheur:
    def __init__(self, Ve=100, f=1000):
        self.Ve = Ve
        self.f = f
        self.T = 1/f

    def buck(self, alpha, R=10, L=0.01):
        Vs = alpha * self.Ve
        Is = Vs / R
        dI = self.Ve * alpha * (1-alpha) / (L * self.f)
        return {'Vs': Vs, 'Is': Is, 'dI': dI, 'alpha': alpha}

    def boost(self, alpha, R=10):
        Vs = self.Ve / (1 - alpha)
        Is = Vs**2 / (R * self.Ve) if self.Ve else 0
        return {'Vs': Vs, 'Is': Is, 'alpha': alpha}

class Onduleur:
    def __init__(self, Vdc=400, f=50):
        self.Vdc = Vdc
        self.f = f

    def monophase_pleine_onde(self, R=10):
        V_eff = self.Vdc / np.sqrt(2)
        I_eff = V_eff / R
        return {'V_eff': V_eff, 'I_eff': I_eff, 'P': V_eff*I_eff}

    def triphase_MLI(self, m=0.8, V_fond=None):
        V_fond = V_fond or m * self.Vdc / 2
        return {'V_fond': V_fond, 'm': m}

def main():
    print("=" * 60)
    print("Electronique de puissance 1")
    print("2AS7 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Diode et thyristor ---")
    d = Diode(Vf=0.7, If_max=10)
    print(f"Diode: Vf={d.Vf}V, If_max={d.If_max}A")
    print(f"  Etat (Va=10V, Vk=0V): {'Conduit' if d.conduit(10,0) else 'Bloque'}")
    print(f"  Etat (Va=0V, Vk=10V): {'Conduit' if d.conduit(0,10) else 'Bloque'}")
    th = Thyristor()
    th.amorcer(30)
    print(f"Thyristor amorce angle={th.angle_amorce} deg")

    print("\n--- 2. Redresseur monophase ---")
    red = RedresseurMonophase(V_s=230)
    sa = red.simple_alternance(R=10)
    print(f"Simple alternance: Vmoy={sa['Vmoy']:.1f}V, Imoy={sa['Imoy']:.2f}A, P={sa['P']:.0f}W")
    da = red.double_alternance(R=10)
    print(f"Double alternance: Vmoy={da['Vmoy']:.1f}V, Imoy={da['Imoy']:.2f}A, P={da['P']:.0f}W")
    for angle in [0, 30, 60, 90, 120]:
        ca = red.commande_angle(angle, R=10)
        print(f"  Angle {angle:3d} deg: Vmoy={ca['Vmoy']:.1f}V")

    print("\n--- 3. Redresseur triphase ---")
    red3 = RedresseurTriphase(V_s=400)
    p3 = red3.pont_P3(R=10)
    print(f"Pont P3: Vmoy={p3['Vmoy']:.1f}V")
    p6 = red3.pont_P6(R=10)
    print(f"Pont P6: Vmoy={p6['Vmoy']:.1f}V")

    print("\n--- 4. Hacheur Buck et Boost ---")
    h = Hacheur(Ve=100, f=1000)
    for alpha in [0.25, 0.5, 0.75]:
        bk = h.buck(alpha)
        bo = h.boost(alpha)
        print(f"Buck alpha={alpha}: Vs={bk['Vs']:.1f}V, dI={bk['dI']:.1f}A")
        print(f"Boost alpha={alpha}: Vs={bo['Vs']:.1f}V")

    print("\n--- 5. Onduleur ---")
    ond = Onduleur(Vdc=400)
    om = ond.monophase_pleine_onde(R=10)
    print(f"Pleine onde (R=10): V_eff={om['V_eff']:.1f}V, P={om['P']:.0f}W")
    omt = ond.triphase_MLI(m=0.85)
    print(f"MLI triphase (m=0.85): V_fond={omt['V_fond']:.1f}V")

if __name__ == '__main__':
    main()
