"""Projet: Transferts d'énergies avancés - Simulation Thermique
3AS9 - ENSEM NRJ (FISA)
Simulation 1D de transferts thermiques (conduction, convection, radiation)"""

import numpy as np
import matplotlib.pyplot as plt

class Materiau:
    def __init__(self, nom, k, rho, cp, epsilon=0.9):
        self.nom = nom
        self.k = k       # Conductivité thermique [W/mK]
        self.rho = rho   # Masse volumique [kg/m3]
        self.cp = cp     # Capacité thermique massique [J/kgK]
        self.alpha = k / (rho * cp)  # Diffusivité thermique [m2/s]
        self.epsilon = epsilon       # Emissivité

    def __str__(self):
        return f"{self.nom} (k={self.k}, alpha={self.alpha:.2e})"

class SimulationThermique:
    def __init__(self, L=1.0, N=100, T_init=20.0):
        self.L = L                # Longueur [m]
        self.N = N                # Nombre de noeuds
        self.dx = L / (N - 1)     # Pas spatial [m]
        self.T = np.full(N, T_init)  # Profil de température [°C]
        self.materiau = None

    def set_materiau(self, materiau):
        self.materiau = materiau

    def conduction_step(self, dt):
        alpha = self.materiau.alpha
        r = alpha * dt / (self.dx**2)
        if r > 0.5:
            raise ValueError(f"Instabilité numérique: r={r:.3f} > 0.5. Réduire dt.")
        T_new = self.T.copy()
        T_new[1:-1] = self.T[1:-1] + r * (self.T[2:] - 2*self.T[1:-1] + self.T[:-2])
        return T_new

    def set_condition_limite_dirichlet(self, T_gauche, T_droite):
        self.T[0] = T_gauche
        self.T[-1] = T_droite

    def set_condition_limite_neumann(self, flux_gauche, flux_droite):
        self.T[0] = self.T[1] + flux_gauche * self.dx / self.materiau.k
        self.T[-1] = self.T[-2] + flux_droite * self.dx / self.materiau.k

    def convection(self, h, T_ext):
        flux = h * (self.T[0] - T_ext)
        return flux

    def radiation(self, sigma=5.67e-8, T_surr=20.0):
        T_k = self.T + 273.15
        flux = self.materiau.epsilon * sigma * (T_k[0]**4 - (T_surr+273.15)**4)
        return flux

    def simuler(self, dt, t_final, verbose=True):
        n_steps = int(t_final / dt)
        historique = [self.T.copy()]
        temps = [0]
        for i in range(n_steps):
            self.T = self.conduction_step(dt)
            if (i+1) % max(1, n_steps//10) == 0 and verbose:
                print(f"t = {(i+1)*dt:.1f}s, T min={self.T.min():.1f}, T max={self.T.max():.1f}")
            historique.append(self.T.copy())
            temps.append((i+1)*dt)
        return np.array(historique), np.array(temps)

    def tracer_profil(self, temps_select=None):
        x = np.linspace(0, self.L, self.N)
        if temps_select:
            for t in temps_select:
                idx = int(t / self.simuler.__defaults__[1]) if False else 0
            return
        plt.figure(figsize=(10, 6))
        plt.plot(x, self.T, 'b-', linewidth=2)
        plt.xlabel('Position [m]')
        plt.ylabel('Température [°C]')
        plt.title(f'Profil de température - {self.materiau}')
        plt.grid(True)
        plt.show()

def main():
    print("=== Transferts d'énergies avancés - Simulation 1D ===")
    cuivre = Materiau("Cuivre", 401, 8960, 385)
    acier = Materiau("Acier", 50, 7800, 460)
    beton = Materiau("Béton", 1.8, 2400, 880)
    isolant = Materiau("Laine de verre", 0.04, 30, 840)

    print(f"\nMatériaux disponibles: {cuivre}, {acier}, {beton}, {isolant}")

    sim = SimulationThermique(L=0.5, N=100, T_init=20.0)
    sim.set_materiau(acier)
    sim.set_condition_limite_dirichlet(200.0, 20.0)

    dt = 0.5
    print(f"\nSimulation: barreau acier L=0.5m, T_gauche=200°C, T_droite=20°C")
    print(f"Pas spatial dx={sim.dx*1000:.1f}mm, pas temporel dt={dt}s")
    historique, temps = sim.simuler(dt, 100)

    x = np.linspace(0, sim.L, sim.N)
    plt.figure(figsize=(12, 8))
    t_afficher = [0, 5, 20, 50, 100]
    for t in t_afficher:
        idx = int(t / dt)
        if idx < len(historique):
            plt.plot(x, historique[idx], label=f't={t}s')
    plt.xlabel('Position [m]')
    plt.ylabel('Température [°C]')
    plt.title('Transfert conductif dans un barreau en acier')
    plt.legend()
    plt.grid(True)
    plt.savefig('profil_temperature.png', dpi=150)
    print("\nGraphique sauvegardé: profil_temperature.png")

if __name__ == '__main__':
    main()
