"""Projet: Sciences industrielles
1AS5 - ENSEM NRJ (FISA)
Statique, mecanismes, materiaux, dessin technique"""

import numpy as np
import math

class Statique:
    def __init__(self):
        self.g = 9.81

    def equilibre_forces(self, forces):
        Fx = sum(f['module'] * np.cos(np.deg2rad(f['angle'])) for f in forces)
        Fy = sum(f['module'] * np.sin(np.deg2rad(f['angle'])) for f in forces)
        return math.sqrt(Fx**2 + Fy**2), np.rad2deg(math.atan2(Fy, Fx))

    def moment(self, F, d, angle=90):
        return F * d * np.sin(np.deg2rad(angle))

    def levier(self, F1, d1, d2):
        return F1 * d1 / d2

class Materiaux:
    def __init__(self):
        self.materiaux = {
            'Acier': {'E': 210e9, 'rho': 7800, 'Re': 235e6, 'Rm': 400e6},
            'Aluminium': {'E': 70e9, 'rho': 2700, 'Re': 110e6, 'Rm': 200e6},
            'Cuivre': {'E': 110e9, 'rho': 8960, 'Re': 70e6, 'Rm': 220e6},
            'Beton': {'E': 30e9, 'rho': 2400, 'Re': 3e6, 'Rm': 30e6},
            'Bois': {'E': 10e9, 'rho': 600, 'Re': 8e6, 'Rm': 40e6},
        }

    def afficher_caracteristiques(self, nom):
        if nom in self.materiaux:
            m = self.materiaux[nom]
            print(f"  {nom}: E={m['E']/1e9:.0f} GPa, rho={m['rho']} kg/m3, "
                  f"Re={m['Re']/1e6:.0f} MPa")

    def critere_choix(self, charge_N, longueur_m, masse_max_kg):
        print(f"\n  Choix materiau (F={charge_N/1000:.0f}kN, L={longueur_m}m, m<{masse_max_kg}kg):")
        for nom, m in self.materiaux.items():
            section_min = charge_N / m['Re']
            volume = section_min * longueur_m
            masse = volume * m['rho']
            if masse <= masse_max_kg:
                print(f"    {nom}: section={section_min*1e4:.1f} cm2, masse={masse:.0f} kg (OK)")

class Mecanismes:
    @staticmethod
    def rapport_transmission(d1, d2):
        return d2 / d1

    @staticmethod
    def rendement_mecanique(P_sortie, P_entree):
        return P_sortie / P_entree if P_entree else 0

    @staticmethod
    def vitesse_engrenages(Z1, Z2, omega1):
        return omega1 * Z1 / Z2

class DessinTechnique:
    @staticmethod
    def normalisation():
        formats = {
            'A0': (841, 1189), 'A1': (594, 841),
            'A2': (420, 594), 'A3': (297, 420),
            'A4': (210, 297)
        }
        return formats

class Energies:
    @staticmethod
    def travail(F, d):
        return F * d

    @staticmethod
    def puissance(Travail, temps):
        return Travail / temps if temps else 0

    @staticmethod
    def rendement(E_utile, E_totale):
        return E_utile / E_totale if E_totale else 0

def main():
    print("=" * 60)
    print("Sciences industrielles")
    print("1AS5 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Statique ---")
    stat = Statique()
    forces = [
        {'module': 100, 'angle': 0},
        {'module': 150, 'angle': 90},
        {'module': 50, 'angle': 180},
    ]
    R, a = stat.equilibre_forces(forces)
    print(f"  Resultante de 3 forces: R={R:.1f}N a {a:.1f} deg")
    print(f"  Moment (F=50N, d=2m): {stat.moment(50, 2, 90)} Nm")
    print(f"  Levier (F1=100N, d1=0.5, d2=2): F2={stat.levier(100, 0.5, 2):.0f}N")

    print("\n--- 2. Materiaux ---")
    mat = Materiaux()
    mat.afficher_caracteristiques("Acier")
    mat.afficher_caracteristiques("Aluminium")
    mat.afficher_caracteristiques("Cuivre")
    mat.afficher_caracteristiques("Beton")
    mat.critere_choix(50000, 3, 500)

    print("\n--- 3. Mecanismes ---")
    meca = Mecanismes()
    Z1, Z2 = 20, 60
    print(f"  Engrenages Z1={Z1}, Z2={Z2}")
    print(f"    Rapport: 1:{meca.rapport_transmission(Z1, Z2):.2f}")
    omega1 = 1500  # tr/min
    omega2 = meca.vitesse_engrenages(Z1, Z2, omega1)
    print(f"    Entree={omega1} tr/min -> Sortie={omega2:.0f} tr/min")
    print(f"    Rendement (P_out=800W, P_in=1000W): {meca.rendement_mecanique(800, 1000):.0%}")

    print("\n--- 4. Dessin technique - Formats normalises ---")
    dt = DessinTechnique()
    formats = dt.normalisation()
    for fmt, dim in formats.items():
        print(f"  {fmt}: {dim[0]}x{dim[1]} mm")

    print("\n--- 5. Energies ---")
    en = Energies()
    print(f"  Travail (F=500N, d=10m): {en.travail(500, 10):.0f} J")
    print(f"  Puissance (Travail=5000J, temps=50s): {en.puissance(5000, 50):.0f} W")
    print(f"  Rendement (E_utile=800J, E_totale=1000J): {en.rendement(800, 1000):.0%}")

if __name__ == '__main__':
    main()
