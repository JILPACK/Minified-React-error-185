"""Projet: Science et Comportement Mécanique des Matériaux
3AS9 - Spécialisation 9_14 - ENSEM NRJ (FISA)
Simulation de propriétés mécaniques et essais de traction"""

import numpy as np
import matplotlib.pyplot as plt

class MateriauMecanique:
    def __init__(self, nom, E, nu, Re, Rm, A, rho=7800):
        self.nom = nom
        self.E = E * 1e9           # Module Young [Pa]
        self.nu = nu               # Coefficient Poisson
        self.Re = Re * 1e6         # Limite élastique [Pa]
        self.Rm = Rm * 1e6         # Résistance max [Pa]
        self.A = A                 # Allongement [%]
        self.rho = rho
        self.G = E / (2 * (1 + nu)) * 1e9  # Module cisaillement [Pa]

    def contrainte_deformation(self, deformation, plastique=False):
        if not plastique or deformation <= self.Re / self.E:
            return self.E * deformation
        else:
            e_elas = self.Re / self.E
            K = self.Rm / (self.A/100)**0.2
            eps_plas = deformation - e_elas
            return self.Re + K * eps_plas**0.2

    def __str__(self):
        return f"{self.nom}: E={self.E/1e9:.0f}GPa, Re={self.Re/1e6:.0f}MPa, Rm={self.Rm/1e6:.0f}MPa"

class EssaiTraction:
    def __init__(self, materiau, L0=50e-3, S0=100e-6):
        self.materiau = materiau
        self.L0 = L0
        self.S0 = S0
        self.force = 0
        self.allongement = 0

    def simuler(self, F_max=50000, pas=1000):
        forces = np.linspace(0, F_max, pas)
        deformations = []
        contraintes = []
        for F in forces:
            sigma = F / self.S0
            if sigma <= self.materiau.Re:
                eps = sigma / self.materiau.E
            else:
                eps = self.materiau.Re / self.materiau.E
                eps += ((sigma - self.materiau.Re) / 500e6)**(1/0.2)
            deformations.append(eps)
            contraintes.append(sigma)
            self.force = F
            self.allongement = eps * self.L0
        return np.array(contraintes)/1e6, np.array(deformations)*100

    def resumer(self):
        return {
            'Module Young': f"{self.materiau.E/1e9:.0f} GPa",
            'Limite élastique': f"{self.materiau.Re/1e6:.0f} MPa",
            'Résistance max': f"{self.materiau.Rm/1e6:.0f} MPa",
            'Allongement': f"{self.materiau.A:.1f}%",
            'Module cisaillement': f"{self.materiau.G/1e9:.1f} GPa"
        }

class SimulationContrainte:
    def __init__(self, materiau):
        self.materiau = materiau

    def cercle_mohr(self, sigma_x, sigma_y, tau_xy):
        centre = (sigma_x + sigma_y) / 2
        rayon = np.sqrt(((sigma_x - sigma_y)/2)**2 + tau_xy**2)
        sigma_1 = centre + rayon
        sigma_2 = centre - rayon
        tau_max = rayon
        angle = np.degrees(0.5 * np.arctan2(2*tau_xy, sigma_x - sigma_y))
        return {'sigma_1': sigma_1, 'sigma_2': sigma_2, 'tau_max': tau_max, 'angle': angle}

    def critere_von_mises(self, sigma_x, sigma_y, sigma_z=0, tau_xy=0, tau_yz=0, tau_zx=0):
        VM = np.sqrt(0.5 * ((sigma_x-sigma_y)**2 + (sigma_y-sigma_z)**2 +
                           (sigma_z-sigma_x)**2 + 6*(tau_xy**2+tau_yz**2+tau_zx**2)))
        securite = self.materiau.Re / VM if VM > 0 else float('inf')
        return VM, securite

def main():
    print("=" * 60)
    print("Science et Comportement des Matériaux - 9_14")
    print("=" * 60)
    acier = MateriauMecanique("Acier S355", 210, 0.3, 355, 510, 22)
    alu = MateriauMecanique("Alu 6061-T6", 69, 0.33, 275, 310, 12, rho=2700)
    cuivre = MateriauMecanique("Cuivre OFHC", 130, 0.34, 70, 220, 45, rho=8960)

    print("\nMatériaux disponibles:")
    for mat in [acier, alu, cuivre]:
        print(f"  {mat}")

    print("\n--- 1. Essai de traction simulé ---")
    essai = EssaiTraction(acier, L0=50e-3, S0=78.5e-6)
    contraintes, deformations = essai.simuler(F_max=60000)
    print(f"Acier S355: σ_max={contraintes[-1]:.0f}MPa, ε_max={deformations[-1]:.1f}%")
    for k, v in essai.resumer().items():
        print(f"  {k}: {v}")

    print("\n--- 2. Analyse des contraintes (cercle de Mohr) ---")
    sim = SimulationContrainte(acier)
    etat = sim.cercle_mohr(200e6, -50e6, 80e6)
    print(f"σ₁ = {etat['sigma_1']/1e6:.1f} MPa")
    print(f"σ₂ = {etat['sigma_2']/1e6:.1f} MPa")
    print(f"τ_max = {etat['tau_max']/1e6:.1f} MPa")
    print(f"Angle plan principal: {etat['angle']:.1f}°")

    print("\n--- 3. Critère de von Mises ---")
    VM, S = sim.critere_von_mises(200e6, 50e6, tau_xy=50e6)
    print(f"Contrainte von Mises: {VM/1e6:.1f} MPa")
    print(f"Coefficient de sécurité: {S:.2f}")
    print(f"Matériau {'ADAPTÉ' if S >= 1.5 else 'NON ADAPTÉ'} (S ≥ 1.5)")

if __name__ == '__main__':
    main()
