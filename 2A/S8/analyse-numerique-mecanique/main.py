"""Projet: Analyse numérique pour la mécanique
2AS8 - ENSEM NRJ (FISA)
Méthodes numériques : différences finies, éléments finis 1D,
intégration numérique, résolution d'EDO"""

import numpy as np
import matplotlib.pyplot as plt

class DifferencesFinies1D:
    def __init__(self, L=1.0, N=50, E=210e9, rho=7800):
        self.L = L
        self.N = N
        self.dx = L / (N - 1)
        self.E = E
        self.rho = rho
        self.x = np.linspace(0, L, N)

    def poutre_encastree(self, F=1000):
        """Poutre encastrée avec charge F à l'extrémité"""
        EI = self.E * (0.05**4 / 12)
        A = np.zeros((self.N, self.N))
        b = np.zeros(self.N)
        for i in range(1, self.N - 1):
            A[i, i-1] = 1
            A[i, i] = -2
            A[i, i+1] = 1
            b[i] = 0
        # Conditions limites
        A[0, 0] = 1; b[0] = 0  # déplacement nul
        A[-1, -2] = 1; A[-1, -1] = -1  # pente nulle
        u = np.linalg.solve(A, b)
        u *= F * self.dx**2 / EI
        return u

    def poutre_appuis_simples(self, q=5000):
        """Poutre sur deux appuis avec charge répartie q"""
        EI = self.E * (0.1**4 / 12)
        A = np.zeros((self.N-2, self.N-2))
        b = np.full(self.N-2, q * self.dx**4 / EI)
        for i in range(self.N-4):
            A[i, i] = 6
            A[i, i+1] = -4
            A[i, i+2] = 1
            A[i+1, i] = -4
            A[i+1, i+1] = 6
            A[i+1, i+2] = -4
            A[i+2, i] = 1
            A[i+2, i+1] = -4
            A[i+2, i+2] = 6
        u_int = np.linalg.solve(A, b)
        return np.concatenate([[0], u_int, [0]])

class ElementsFinis1D:
    def __init__(self, L=1.0, NE=10, E=210e9, A=0.01):
        self.L = L
        self.NE = NE
        self.E = E
        self.A = A
        self.Le = L / NE
        self.nn = NE + 1

    def assembler_matrice(self):
        K = np.zeros((self.nn, self.nn))
        ke = self.E * self.A / self.Le * np.array([[1, -1], [-1, 1]])
        for e in range(self.NE):
            K[e:e+2, e:e+2] += ke
        return K

    def barre_encastree(self, F=5000):
        K = self.assembler_matrice()
        # CL: noeud 0 encastré (u=0)
        K_r = K[1:, 1:]
        F_r = np.zeros(self.nn - 1)
        F_r[-1] = F
        u_r = np.linalg.solve(K_r, F_r)
        return np.concatenate([[0], u_r])

class IntegrationNumerique:
    @staticmethod
    def trapezes(f, a, b, n=100):
        h = (b - a) / n
        x = np.linspace(a, b, n+1)
        return h * (f(a)/2 + sum(f(x[1:-1])) + f(b)/2)

    @staticmethod
    def simpson(f, a, b, n=100):
        if n % 2: n += 1
        h = (b - a) / n
        x = np.linspace(a, b, n+1)
        return h/3 * (f(a) + f(b) + 4*sum(f(x[1:-1:2])) + 2*sum(f(x[2:-1:2])))

class Vibrations:
    def __init__(self, m=10, k=1000, c=20):
        self.m = m; self.k = k; self.c = c
        self.omega0 = np.sqrt(k/m)
        self.zeta = c / (2*np.sqrt(m*k))

    def reponse_impulsionnelle(self, t):
        if self.zeta < 1:
            wd = self.omega0 * np.sqrt(1 - self.zeta**2)
            return np.exp(-self.zeta*self.omega0*t) * np.sin(wd*t) / (wd*self.m)
        return t * np.exp(-self.omega0*t) / self.m

    def reponse_echelon(self, t):
        if self.zeta < 1:
            wd = self.omega0 * np.sqrt(1 - self.zeta**2)
            phi = np.arctan2(np.sqrt(1-self.zeta**2), self.zeta)
            return 1/self.k * (1 - np.exp(-self.zeta*self.omega0*t) * np.sin(wd*t+phi) / np.sqrt(1-self.zeta**2))
        return 0

def main():
    print("=" * 60)
    print("Analyse numérique pour la mécanique")
    print("2AS8 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Différences finies - Poutre encastrée ---")
    df = DifferencesFinies1D(L=2.0, N=100)
    u = df.poutre_encastree(F=2000)
    print(f"Flèche max: {abs(u).max()*1000:.2f} mm (à x={df.x[np.argmax(abs(u))]:.2f}m)")
    print(f"Flèche extrémité: {abs(u[-1])*1000:.2f} mm")

    print("\n--- 2. Éléments finis 1D - Barre en traction ---")
    ef = ElementsFinis1D(L=1.0, NE=20, A=0.005)
    u_ef = ef.barre_encastree(F=10000)
    allongement = u_ef[-1]
    print(f"Allongement total: {allongement*1000:.3f} mm")
    deformation = allongement / ef.L
    contrainte = deformation * ef.E / 1e6
    print(f"Déformation: {deformation*100:.4f}%")
    print(f"Contrainte: {contrainte:.1f} MPa")

    print("\n--- 3. Intégration numérique ---")
    f = lambda x: np.sin(x)**2 * np.exp(-x/5)
    a, b = 0, 10
    I_ref = 2.433
    I_trap = IntegrationNumerique.trapezes(f, a, b, 100)
    I_simp = IntegrationNumerique.simpson(f, a, b, 100)
    print(f"Référence: {I_ref:.4f}")
    print(f"Trapèzes:  {I_trap:.4f} (erreur {abs(I_trap-I_ref)*100:.2f}%)")
    print(f"Simpson:   {I_simp:.4f} (erreur {abs(I_simp-I_ref)*100:.2f}%)")

    print("\n--- 4. Vibrations - Système masse-ressort-amortisseur ---")
    vib = Vibrations(m=50, k=5000, c=100)
    print(f"Fréquence propre: {vib.omega0/(2*np.pi):.2f} Hz")
    print(f"Facteur d'amortissement ζ: {vib.zeta:.3f}")
    print(f"Régime: {'Apériodique' if vib.zeta>=1 else 'Pseudo-périodique'}")
    t = np.array([0.5, 1.0, 2.0])
    for ti in t:
        print(f"  t={ti:.1f}s: réponse échelon={vib.reponse_echelon(ti)*1000:.2f} mm")

if __name__ == '__main__':
    main()
