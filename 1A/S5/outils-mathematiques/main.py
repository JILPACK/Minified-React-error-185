"""Projet: Outils mathematiques
1AS5 - ENSEM NRJ (FISA)
Trigonometric, calcul vectoriel, statistiques, probabilites"""

import numpy as np
import math
import random

class Trigonometrie:
    @staticmethod
    def degres_radians(angle_deg):
        return angle_deg * np.pi / 180

    @staticmethod
    def radians_degres(angle_rad):
        return angle_rad * 180 / np.pi

    @staticmethod
    def identites(theta):
        s = np.sin(theta)
        c = np.cos(theta)
        return {
            'sin^2 + cos^2': s**2 + c**2,
            'sin(2theta)': np.sin(2*theta),
            'cos(2theta)': np.cos(2*theta),
        }

    @staticmethod
    def triangle_rectangle(cote_a, cote_b, angle_C_deg=None):
        if angle_C_deg:
            C = np.deg2rad(angle_C_deg)
            return np.sqrt(cote_a**2 + cote_b**2 - 2*cote_a*cote_b*np.cos(C))
        return np.sqrt(cote_a**2 + cote_b**2)

class CalculVectoriel:
    @staticmethod
    def somme(u, v):
        return [u[i]+v[i] for i in range(len(u))]

    @staticmethod
    def produit_scalaire(u, v):
        return sum(a*b for a,b in zip(u,v))

    @staticmethod
    def norme(v):
        return math.sqrt(sum(x**2 for x in v))

    @staticmethod
    def produit_vectoriel(u, v):
        if len(u) != 3 or len(v) != 3:
            return None
        return [
            u[1]*v[2] - u[2]*v[1],
            u[2]*v[0] - u[0]*v[2],
            u[0]*v[1] - u[1]*v[0]
        ]

    @staticmethod
    def angle(u, v):
        ps = CalculVectoriel.produit_scalaire(u, v)
        nu = CalculVectoriel.norme(u)
        nv = CalculVectoriel.norme(v)
        return np.rad2deg(math.acos(ps/(nu*nv))) if nu*nv else 0

class Statistiques:
    @staticmethod
    def moyenne(vals):
        return sum(vals)/len(vals) if vals else 0

    @staticmethod
    def variance(vals):
        m = Statistiques.moyenne(vals)
        return sum((x-m)**2 for x in vals)/(len(vals)-1) if len(vals)>1 else 0

    @staticmethod
    def ecart_type(vals):
        return math.sqrt(Statistiques.variance(vals))

    @staticmethod
    def mediane(v):
        return sorted(v)[len(v)//2] if v else None

    @staticmethod
    def histogramme(vals, classes=5):
        mini, maxi = min(vals), max(vals)
        pas = (maxi - mini) / classes
        hist = []
        for i in range(classes):
            debut = mini + i*pas
            fin = mini + (i+1)*pas
            count = sum(1 for v in vals if debut <= v < fin)
            hist.append({'classe': f"[{debut:.1f}, {fin:.1f}[", 'effectif': count})
        return hist

class Probabilite:
    @staticmethod
    def combinatoire(n, k):
        if k > n: return 0
        return math.factorial(n) // (math.factorial(k) * math.factorial(n-k))

    @staticmethod
    def probabilite_binomiale(n, k, p):
        return Probabilite.combinatoire(n, k) * p**k * (1-p)**(n-k)

    @staticmethod
    def esperance(valeurs, probabilites):
        return sum(v*p for v,p in zip(valeurs, probabilites))

def main():
    print("=" * 60)
    print("Outils mathematiques")
    print("1AS5 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Trigonometrie ---")
    for angle in [0, 30, 45, 60, 90]:
        rad = Trigonometrie.degres_radians(angle)
        print(f"  {angle} deg = {rad:.3f} rad, sin={math.sin(rad):.3f}, cos={math.cos(rad):.3f}")
    triangle = Trigonometrie.triangle_rectangle(3, 4)
    print(f"  Triangle 3-4-5: hypotenuse={triangle}")
    tri2 = Trigonometrie.triangle_rectangle(5, 6, 60)
    print(f"  Triangle (a=5, b=6, angle=60): cote={tri2:.2f}")

    print("\n--- 2. Calcul vectoriel ---")
    u = [2, -1, 3]
    v = [1, 4, -2]
    print(f"  u = {u}, v = {v}")
    print(f"  u+v = {CalculVectoriel.somme(u, v)}")
    print(f"  u.v = {CalculVectoriel.produit_scalaire(u, v)}")
    print(f"  u x v = {CalculVectoriel.produit_vectoriel(u, v)}")
    print(f"  |u| = {CalculVectoriel.norme(u):.2f}")
    print(f"  angle(u,v) = {CalculVectoriel.angle(u, v):.1f} deg")

    print("\n--- 3. Statistiques ---")
    np.random.seed(42)
    notes = [random.gauss(12, 3) for _ in range(30)]
    notes = [max(0, min(20, round(n,1))) for n in notes]
    print(f"  Echantillon ({len(notes)} notes): {notes[:10]}...")
    print(f"  Moyenne: {Statistiques.moyenne(notes):.2f}")
    print(f"  Ecart-type: {Statistiques.ecart_type(notes):.2f}")
    hist = Statistiques.histogramme(notes, 5)
    print("  Histogramme:")
    for h in hist:
        bar = '#' * h['effectif']
        print(f"    {h['classe']:>14}: {h['effectif']:2d} {bar}")

    print("\n--- 4. Probabilites ---")
    pr = Probabilite()
    print(f"  C(10,3) = {pr.combinatoire(10, 3)}")
    print(f"  C(52,5) = {pr.combinatoire(52, 5)}")
    for k in range(5):
        p = pr.probabilite_binomiale(10, k, 0.5)
        print(f"  P(X={k}) loi binomiale n=10, p=0.5: {p:.3f}")
    vals = [-1, 0, 1, 2]
    probs = [0.1, 0.3, 0.4, 0.2]
    print(f"  Esperance = {pr.esperance(vals, probs):.2f}")

if __name__ == '__main__':
    main()
