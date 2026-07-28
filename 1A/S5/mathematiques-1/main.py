"""Projet: Mathematiques 1
1AS5 - ENSEM NRJ (FISA)
Nombres complexes, algebre lineaire, fonctions, integration"""

import numpy as np
import math

class NombresComplexes:
    @staticmethod
    def cartesien(re, im):
        return complex(re, im)

    @staticmethod
    def polaire(module, arg_deg):
        arg = np.deg2rad(arg_deg)
        return module * (np.cos(arg) + 1j*np.sin(arg))

    @staticmethod
    def module(z):
        return abs(z)

    @staticmethod
    def argument(z):
        return np.rad2deg(np.angle(z))

    @staticmethod
    def racines(n, z):
        r = abs(z)
        theta = np.angle(z)
        return [r**(1/n) * (np.cos((theta + 2*k*np.pi)/n) + 1j*np.sin((theta + 2*k*np.pi)/n)) for k in range(n)]

class Vecteurs:
    @staticmethod
    def produit_scalaire(u, v):
        return sum(a*b for a,b in zip(u,v))

    @staticmethod
    def norme(v):
        return math.sqrt(sum(x**2 for x in v))

    @staticmethod
    def angle_entre(u, v):
        ps = Vecteurs.produit_scalaire(u, v)
        nu = Vecteurs.norme(u)
        nv = Vecteurs.norme(v)
        return np.rad2deg(math.acos(ps/(nu*nv))) if nu*nv else 0

class Matrices:
    def __init__(self, data):
        self.data = np.array(data, dtype=float)
        self.lignes, self.colonnes = self.data.shape

    def determinant(self):
        return np.linalg.det(self.data)

    def inverse(self):
        return np.linalg.inv(self.data)

    def valeurs_propres(self):
        return np.linalg.eigvals(self.data)

    def produit(self, autre):
        return self.data @ autre.data if isinstance(autre, Matrices) else self.data @ autre

class Fonctions:
    @staticmethod
    def ln(x):
        return math.log(x) if x > 0 else None

    @staticmethod
    def exp(x):
        return math.exp(x)

    @staticmethod
    def derivee(f, x, h=1e-6):
        return (f(x+h) - f(x-h)) / (2*h)

    @staticmethod
    def tangente(f, x):
        d = Fonctions.derivee(f, x)
        return lambda t: f(x) + d*(t-x)

class Integration:
    @staticmethod
    def rectangles(f, a, b, n=100):
        h = (b-a)/n
        return h * sum(f(a + i*h + h/2) for i in range(n))

    @staticmethod
    def primitive(F, a, b):
        return F(b) - F(a)

def main():
    print("=" * 60)
    print("Mathematiques 1")
    print("1AS5 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Nombres complexes ---")
    z1 = NombresComplexes.cartesien(3, 4)
    z2 = NombresComplexes.polaire(5, 53.13)
    print(f"  z1 = 3+4j: |z1|={abs(z1):.2f}, arg={np.rad2deg(np.angle(z1)):.2f} deg")
    print(f"  z2 (5 angle 53.13): {z2}")
    print(f"  z1+z2 = {z1+z2}")
    print(f"  z1*z2 = {z1*z2}")
    print(f"  Racines 3eme de 1:")
    for r in NombresComplexes.racines(3, 1+0j):
        print(f"    {r:.3f}")

    print("\n--- 2. Vecteurs ---")
    u = [3, 1, -2]
    v = [2, -3, 1]
    print(f"  u = {u}, v = {v}")
    print(f"  u.v = {Vecteurs.produit_scalaire(u, v)}")
    print(f"  |u| = {Vecteurs.norme(u):.3f}")
    print(f"  |v| = {Vecteurs.norme(v):.3f}")
    print(f"  angle = {Vecteurs.angle_entre(u, v):.1f} deg")

    print("\n--- 3. Matrices ---")
    A = Matrices([[2, 1], [1, 3]])
    B = Matrices([[1, -1], [2, 1]])
    print(f"  A = {A.data.tolist()}")
    print(f"  B = {B.data.tolist()}")
    print(f"  det(A) = {A.determinant():.2f}")
    print(f"  A*B = {A.produit(B).tolist()}")
    print(f"  VP(A) = {A.valeurs_propres()}")

    print("\n--- 4. Fonctions et derivation ---")
    f = lambda x: x**2 - 3*x + 2
    for x in [0, 1, 2, 3]:
        d = Fonctions.derivee(f, x)
        print(f"  f({x})={f(x):.2f}, f'({x})={d:.2f}")
    tan = Fonctions.tangente(f, 2)
    print(f"  Tangente en x=2: t(2.5)={tan(2.5):.2f}")

    print("\n--- 5. Integration ---")
    carre = lambda x: x**2
    I = Integration.rectangles(carre, 0, 2)
    print(f"  Integrale x^2 de 0 a 2: {I:.4f} (exact: 2.6667)")
    sinf = lambda x: math.sin(x)
    I2 = Integration.rectangles(sinf, 0, math.pi)
    print(f"  Integrale sin(x) de 0 a pi: {I2:.4f} (exact: 2.0000)")
    expf = lambda x: math.exp(-x)
    I3 = Integration.rectangles(expf, 0, 5)
    print(f"  Integrale exp(-x) de 0 a 5: {I3:.4f} (exact: 0.9933)")

if __name__ == '__main__':
    main()
