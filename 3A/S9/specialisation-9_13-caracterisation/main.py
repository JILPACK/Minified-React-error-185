"""Projet: Méthodologie et Caractérisation Expérimentale
3AS9 - Spécialisation 9_13 - ENSEM NRJ (FISA)
Analyse de données expérimentales et simulations numériques"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit

class AcquisitionDonnees:
    def __init__(self):
        self.donnees = {}

    def generer_mesure(self, nom, f_reele, amplitude, bruit=0.05, n_points=100):
        x = np.linspace(0, 10, n_points)
        y_reel = f_reele(x) * amplitude
        y_mesure = y_reel + np.random.randn(n_points) * amplitude * bruit
        self.donnees[nom] = {'x': x, 'y': y_mesure, 'y_reel': y_reel, 'sigma': amplitude * bruit}
        return self.donnees[nom]

class AnalyseurIncertitude:
    def __init__(self):
        self.sources = []

    def ajouter_source(self, nom, valeur, incertitude, type='Type B'):
        self.sources.append({'nom': nom, 'valeur': valeur, 'u': incertitude, 'type': type})

    def incertitude_type_A(self, mesures):
        n = len(mesures)
        moyenne = np.mean(mesures)
        ecart_type = np.std(mesures, ddof=1)
        return moyenne, ecart_type / np.sqrt(n)

    def incertitude_composee(self, sensibilites=None):
        if sensibilites:
            u_c = np.sqrt(sum((c * s['u'])**2 for c, s in zip(sensibilites, self.sources)))
        else:
            u_c = np.sqrt(sum(s['u']**2 for s in self.sources))
        return u_c

    def incertitude_elargie(self, k=2):
        return self.incertitude_composee() * k

class AjustementModele:
    def __init__(self):
        self.params = {}
        self.cov = None

    def ajustement_lineaire(self, x, y, sigma_y=None):
        if sigma_y is None:
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        else:
            weights = 1 / sigma_y**2
            A = np.vander(x, 2)
            W = np.diag(weights)
            self.cov = np.linalg.inv(A.T @ W @ A)
            beta = self.cov @ (A.T @ W @ y)
            slope, intercept = beta
        self.params = {'pente': slope, 'ordonnee': intercept}
        return self.params

    def ajustement_non_lineaire(self, f, x, y, p0, sigma_y=None):
        popt, pcov = curve_fit(f, x, y, p0=p0, sigma=sigma_y, absolute_sigma=True)
        self.params = {f'p{i}': v for i, v in enumerate(popt)}
        self.cov = pcov
        return self.params

class SimulationNumerique:
    def __init__(self, L=1.0, N=50):
        self.L = L
        self.N = N
        self.dx = L / N

    def conductivite_thermique_1D(self, k=50, q=1e6, T0=20):
        dx = self.dx
        A = np.zeros((self.N-1, self.N-1))
        b = np.full(self.N-1, -q * dx**2 / k)
        for i in range(self.N-2):
            A[i,i] = 2
            A[i,i+1] = -1
            A[i+1,i] = -1
        A[self.N-2, self.N-2] = 2
        T = np.linalg.solve(A, b)
        T = np.concatenate([[T0], T + T0, [T0]])
        return np.linspace(0, self.L, self.N+1), T

    def convergence_maillage(self, k=50, q=1e6, T0=20):
        maillages = [5, 10, 20, 50, 100]
        T_centre = []
        for N in maillages:
            sim = SimulationNumerique(self.L, N)
            x, T = sim.conductivite_thermique_1D(k, q, T0)
            T_centre.append(T[len(T)//2])
        return maillages, T_centre

def main():
    print("=" * 60)
    print("Caractérisation Expérimentale et Simulation - 9_13")
    print("=" * 60)
    print("\n--- 1. Acquisition et analyse de mesures ---")
    acquis = AcquisitionDonnees()
    mesure = acquis.generer_mesure("Loi d'Ohm", lambda x: x, 10, bruit=0.03, n_points=50)
    print(f"Mesure 'Loi d'Ohm': {len(mesure['x'])} points, bruit σ={mesure['sigma']:.2f}")
    print("\n--- 2. Analyse d'incertitude ---")
    an = AnalyseurIncertitude()
    an.ajouter_source("Tension", 230, 1.5, "Type B")
    an.ajouter_source("Courant", 10, 0.2, "Type B")
    an.ajouter_source("Résistance", 23, 0.5, "Type B")
    u_c = an.incertitude_composee()
    U = an.incertitude_elargie(k=2)
    print(f"Incertitude-type composée: u_c = {u_c:.3f}")
    print(f"Incertitude élargie (k=2): U = {U:.3f}")
    print("\n--- 3. Ajustement de modèle ---")
    x = np.array([0, 2, 4, 6, 8, 10])
    y = np.array([0.1, 2.1, 3.8, 6.2, 7.9, 10.3])
    sigma = np.full_like(y, 0.3)
    ajust = AjustementModele()
    params = ajust.ajustement_lineaire(x, y, sigma)
    print(f"Ajustement linéaire: V = {params['pente']:.3f} × I + {params['ordonnee']:.3f}")
    print(f"Résistance estimée: R = {params['pente']:.3f} Ω")
    print("\n--- 4. Simulation numérique (éléments finis 1D) ---")
    sim = SimulationNumerique(L=0.5, N=50)
    x_sim, T = sim.conductivite_thermique_1D(k=50, q=5e5)
    print(f"Température max: {T.max():.1f}°C (x={x_sim[T.argmax()]*100:.1f}cm)")
    print(f"Température min: {T.min():.1f}°C")
    print("\n--- 5. Étude de convergence ---")
    maillages, T_centres = sim.convergence_maillage()
    print(f"{'Maillage N':<12} {'T centre (°C)':<15}")
    for N, Tc in zip(maillages, T_centres):
        print(f"{N:<12} {Tc:<15.2f}")

if __name__ == '__main__':
    main()
