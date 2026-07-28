"""Projet: Modélisation et Optimisation des Machines Électriques
3AS9 - Spécialisation 9_6 - ENSEM NRJ (FISA)
Modèle analytique de machine synchrone et optimisation"""

import numpy as np
import matplotlib.pyplot as plt

class MachineSynchrone:
    def __init__(self, Pnom=100e3, Vnom=400, f=50, p=2, R=0.05, Ld=1.5e-3, Lq=1.5e-3, psi_f=0.5):
        self.Pnom = Pnom
        self.Vnom = Vnom
        self.f = f
        self.p = p
        self.R = R
        self.Ld = Ld
        self.Lq = Lq
        self.psi_f = psi_f
        self.omega_s = 2 * np.pi * f
        self.omega_m = self.omega_s / p

    def couple_electromagnetique(self, Id, Iq):
        return 1.5 * self.p * (self.psi_f * Iq + (self.Ld - self.Lq) * Id * Iq)

    def tension(self, Id, Iq, omega_r):
        Vd = self.R * Id - omega_r * self.Lq * Iq
        Vq = self.R * Iq + omega_r * (self.Ld * Id + self.psi_f)
        return np.sqrt(Vd**2 + Vq**2)

    def courant_max(self, Vdc):
        return Vdc / (np.sqrt(3) * np.sqrt(self.R**2 + (self.omega_s * self.Ld)**2))

    def point_optimal_MTPA(self, I_max, omega_r):
        Ids = np.linspace(-I_max, 0, 200)
        Iqs = np.sqrt(I_max**2 - Ids**2)
        couples = np.array([self.couple_electromagnetique(Id, Iq) for Id, Iq in zip(Ids, Iqs)])
        idx = np.argmax(couples)
        return Ids[idx], Iqs[idx], couples[idx]

    def caracteristiques(self, Id, Iq, omega_r):
        T = self.couple_electromagnetique(Id, Iq)
        V = self.tension(Id, Iq, omega_r)
        P = T * omega_r / self.p
        return T, V, P

class MachineAsynchrone:
    def __init__(self, Pnom=75e3, Vnom=400, f=50, p=2, Rs=0.1, Rr=0.08, Ls=10e-3, Lr=10e-3, Lm=200e-3):
        self.Pnom = Pnom
        self.Vnom = Vnom
        self.f = f
        self.p = p
        self.Rs = Rs
        self.Rr = Rr
        self.Ls = Ls
        self.Lr = Lr
        self.Lm = Lm
        self.omega_s = 2 * np.pi * f

    def courant_rotorique(self, s):
        V_phase = self.Vnom / np.sqrt(3)
        Rr_s = self.Rr / s
        Z = self.Rs + 1j * self.omega_s * (self.Ls - self.Lm**2/self.Lr) + (1j * self.omega_s * self.Lm * Rr_s) / (Rr_s + 1j * self.omega_s * self.Lr)
        return V_phase / Z

    def couple(self, s):
        Ir = self.courant_rotorique(s)
        T = 3 * self.p * (self.Lm / self.Lr) * abs(Ir)**2 * self.Rr / (s * self.omega_s)
        return T

    def courbe_couple_vitesse(self):
        slips = np.linspace(0.001, 0.1, 50)
        couples = [self.couple(s) for s in slips]
        return slips, couples

class OptimisationMachine:
    def __init__(self, machine):
        self.machine = machine

    def optimiser_rendement(self, gamme_puissance):
        meilleur = {'rendement': 0}
        for Ld in np.linspace(1e-3, 3e-3, 10):
            for Lq in np.linspace(1e-3, 3e-3, 10):
                self.machine.Ld = Ld
                self.machine.Lq = Lq
                pertes_cuivre = 3 * self.machine.R * (100)**2
                P_sortie = gamme_puissance
                rendement = P_sortie / (P_sortie + pertes_cuivre)
                if rendement > meilleur['rendement']:
                    meilleur = {'Ld': Ld, 'Lq': Lq, 'rendement': rendement}
        return meilleur

def main():
    print("=" * 60)
    print("Machines Électriques - Modélisation et Optimisation 9_6")
    print("=" * 60)
    print("\n--- 1. Machine Synchrone ---")
    ms = MachineSynchrone(Pnom=100e3)
    print(f"Machine synchrone {ms.Pnom/1000:.0f}kW, {ms.p} paires de pôles")
    I_max = ms.courant_max(560)
    print(f"Courant max: {I_max:.1f}A")
    Id_opt, Iq_opt, T_max = ms.point_optimal_MTPA(I_max, ms.omega_m)
    print(f"MTPA: Id={Id_opt:.1f}A, Iq={Iq_opt:.1f}A, T={T_max:.0f}Nm")
    T, V, P = ms.caracteristiques(Id_opt, Iq_opt, ms.omega_m)
    print(f"Caractéristiques: T={T:.0f}Nm, V={V:.1f}V, P={P/1000:.1f}kW")
    print("\n--- 2. Machine Asynchrone ---")
    ma = MachineAsynchrone(Pnom=75e3)
    print(f"Machine asynchrone {ma.Pnom/1000:.0f}kW")
    s_nom = 0.025
    T_nom = ma.couple(s_nom)
    print(f"Couple nominal (s={s_nom}): {T_nom:.0f}Nm")
    print(f"Vitesse nominale: {ma.omega_s/ma.p*(1-s_nom)/np.pi*30:.0f} tr/min")
    print("\n--- 3. Optimisation du rendement ---")
    opt = OptimisationMachine(ms)
    resultat = opt.optimiser_rendement(80e3)
    print(f"Ld optimal: {resultat['Ld']*1000:.2f}mH")
    print(f"Lq optimal: {resultat['Lq']*1000:.2f}mH")
    print(f"Rendement max: {resultat['rendement']:.1%}")

if __name__ == '__main__':
    main()
