"""Projet: Mathematiques appliquees
1AS6 - ENSEM NRJ (FISA)
Equations differentielles, transformees, series de Fourier, statistiques"""

import numpy as np
import math

class EquationDifferentielle:
    @staticmethod
    def Euler(f, y0, t):
        y = np.zeros(len(t))
        y[0] = y0
        for i in range(1, len(t)):
            h = t[i] - t[i-1]
            y[i] = y[i-1] + h * f(t[i-1], y[i-1])
        return y

    @staticmethod
    def RK4(f, y0, t):
        y = np.zeros(len(t))
        y[0] = y0
        for i in range(1, len(t)):
            h = t[i] - t[i-1]; ti = t[i-1]; yi = y[i-1]
            k1 = f(ti, yi)
            k2 = f(ti + h/2, yi + h*k1/2)
            k3 = f(ti + h/2, yi + h*k2/2)
            k4 = f(ti + h, yi + h*k3)
            y[i] = yi + h/6*(k1 + 2*k2 + 2*k3 + k4)
        return y

class TransformeeLaplace:
    @staticmethod
    def echelon(K=1, tau=1, t=None):
        if t is None:
            t = np.linspace(0, 10, 100)
        return K * (1 - np.exp(-t/tau))

    @staticmethod
    def sinusoidal(K=1, omega=1, phi=0, t=None):
        if t is None:
            t = np.linspace(0, 10, 100)
        return K * np.sin(omega*t + phi)

class SerieFourier:
    def __init__(self, f, T=2*np.pi, N=10):
        self.f = f
        self.T = T
        self.N = N

    def calculer_coeffs(self):
        a0 = (2/self.T) * self.f(self.T/2)
        an = []
        bn = []
        for n in range(1, self.N+1):
            an.append(0)
            bn.append(2/self.T * self.f(self.T/4))
        return a0, an, bn

class StatistiquesDescriptives:
    @staticmethod
    def moyenne(x):
        return np.mean(x)

    @staticmethod
    def mediane(x):
        return np.median(x)

    @staticmethod
    def ecart_type(x):
        return np.std(x, ddof=1)

    @staticmethod
    def correlation(x, y):
        return np.corrcoef(x, y)[0,1]

class Probabilites:
    @staticmethod
    def loi_normale(x, mu=0, sigma=1):
        return 1/(sigma*np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2/(2*sigma**2))

    @staticmethod
    def intervalle_confiance(m, s, n, niveau=0.95):
        import scipy.stats as st
        if niveau == 0.95:
            t = 1.96
        elif niveau == 0.99:
            t = 2.576
        else:
            t = 1.645
        return m - t*s/np.sqrt(n), m + t*s/np.sqrt(n)

def main():
    print("=" * 60)
    print("Mathematiques appliquees")
    print("1AS6 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Equations differentielles ---")
    tau, K = 2, 5
    f = lambda t, y: (K - y) / tau
    t = np.linspace(0, 10, 50)
    y_euler = EquationDifferentielle.Euler(f, 0, t)
    y_rk4 = EquationDifferentielle.RK4(f, 0, t)
    y_exact = K * (1 - np.exp(-t/tau))
    print(f"dy/dt = ({K} - y)/{tau}, y(0)=0")
    for idx in [0, 10, 25, -1]:
        print(f"  t={t[idx]:.1f}s: exact={y_exact[idx]:.3f}, Euler={y_euler[idx]:.3f}, RK4={y_rk4[idx]:.3f}")

    print("\n--- 2. Transformee de Laplace - Reponses temporelles ---")
    tl = TransformeeLaplace()
    t = np.array([0.5, 1, 2, 5, 10])
    print("Reponse indicielle 1er ordre (K=2, tau=3):")
    for ti in t:
        y = tl.echelon(K=2, tau=3, t=np.array([ti]))[0]
        print(f"  t={ti:.0f}s: y={y:.3f}")
    print("Reponse sinusoidale (A=3, f=0.5Hz):")
    for ti in t:
        y = tl.sinusoidal(K=3, omega=np.pi, t=np.array([ti]))[0]
        print(f"  t={ti:.0f}s: y={y:.3f}")

    print("\n--- 3. Series de Fourier ---")
    carree = lambda t: 1 if t % (2*np.pi) < np.pi else -1
    sf = SerieFourier(carree, 2*np.pi, 5)
    a0, an, bn = sf.calculer_coeffs()
    print(f"Signal carre (T=2pi): a0={a0:.2f}")
    for n in range(5):
        print(f"  a{n+1}={an[n]:.3f}, b{n+1}={bn[n]:.3f}")

    print("\n--- 4. Statistiques descriptives ---")
    np.random.seed(42)
    x = np.random.normal(15, 3, 100)
    y = 2*x + np.random.normal(0, 2, 100)
    print(f"X ~ N(15, 3), n=100")
    print(f"  Moyenne: {StatistiquesDescriptives.moyenne(x):.2f}")
    print(f"  Mediane: {StatistiquesDescriptives.mediane(x):.2f}")
    print(f"  Ecart-type: {StatistiquesDescriptives.ecart_type(x):.2f}")
    print(f"  Correlation X-Y: {StatistiquesDescriptives.correlation(x, y):.3f}")

    print("\n--- 5. Probabilites et intervalle de confiance ---")
    p = Probabilites()
    for x in [-2, -1, 0, 1, 2]:
        print(f"  N(0,1) en x={x:+.0f}: {p.loi_normale(x):.4f}")
    IC = p.intervalle_confiance(15.2, 2.8, 50, 0.95)
    print(f"  IC 95% (m=15.2, s=2.8, n=50): [{IC[0]:.2f}, {IC[1]:.2f}]")

if __name__ == '__main__':
    main()
