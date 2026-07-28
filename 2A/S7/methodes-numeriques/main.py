"""Projet: Methodes numeriques pour l'ingenieur
2AS7 - ENSEM NRJ (FISA)
Resolution numerique d'equations, interpolation, integration, EDO"""

import numpy as np

class ResolutionEquations:
    @staticmethod
    def dichotomie(f, a, b, tol=1e-10, max_iter=100):
        if f(a)*f(b) > 0:
            return None
        for _ in range(max_iter):
            c = (a+b)/2
            if abs(f(c)) < tol or (b-a)/2 < tol:
                return c
            if f(a)*f(c) < 0:
                b = c
            else:
                a = c
        return (a+b)/2

    @staticmethod
    def Newton(f, df, x0, tol=1e-10, max_iter=100):
        x = x0
        for _ in range(max_iter):
            fx = f(x)
            if abs(fx) < tol:
                return x
            x -= fx / df(x)
        return x

class Interpolation:
    @staticmethod
    def Lagrange(x, y, x_eval):
        n = len(x)
        result = 0
        for i in range(n):
            L = 1.0
            for j in range(n):
                if i != j:
                    L *= (x_eval - x[j]) / (x[i] - x[j])
            result += y[i] * L
        return result

    @staticmethod
    def spline_cubique_naturelle(x, y):
        n = len(x)
        h = np.diff(x)
        A = np.zeros((n, n))
        b = np.zeros(n)
        A[0,0] = 1; A[-1,-1] = 1
        for i in range(1, n-1):
            A[i, i-1] = h[i-1]
            A[i, i] = 2*(h[i-1]+h[i])
            A[i, i+1] = h[i]
            b[i] = 3*((y[i+1]-y[i])/h[i] - (y[i]-y[i-1])/h[i-1])
        c = np.linalg.solve(A, b)
        a = y[:-1]
        b_spl = (y[1:]-y[:-1])/h - h*(2*c[:-1]+c[1:])/3
        d_spl = (c[1:]-c[:-1])/(3*h)
        return a, b_spl, c[:-1], d_spl, h

class IntegrationNumerique:
    @staticmethod
    def rectangles(f, a, b, n=100):
        h = (b-a)/n
        return h * sum(f(a + i*h) for i in range(n))

    @staticmethod
    def trapezes(f, a, b, n=100):
        h = (b-a)/n
        x = np.linspace(a, b, n+1)
        return h * (f(a)/2 + sum(f(x[1:-1])) + f(b)/2)

    @staticmethod
    def simpson(f, a, b, n=100):
        if n % 2: n += 1
        h = (b-a)/n
        x = np.linspace(a, b, n+1)
        return h/3 * (f(a) + f(b) + 4*sum(f(x[1:-1:2])) + 2*sum(f(x[2:-1:2])))

    @staticmethod
    def gauss_legendre(f, a, b, n=5):
        x_gl = {-2: [-0.57735, 0.57735], -3: [-0.77460, 0, 0.77460],
                -5: [-0.90618, -0.53847, 0, 0.53847, 0.90618]}
        w_gl = {-2: [1, 1], -3: [0.55555, 0.88889, 0.55555],
                -5: [0.23693, 0.47863, 0.56889, 0.47863, 0.23693]}
        xg = np.array(x_gl[-n]); wg = np.array(w_gl[-n])
        t = (b-a)/2 * xg + (a+b)/2
        return (b-a)/2 * sum(wg[i]*f(t[i]) for i in range(n))

class EDO:
    @staticmethod
    def Euler(f, y0, t, args=()):
        y = np.zeros(len(t))
        y[0] = y0
        for i in range(1, len(t)):
            h = t[i] - t[i-1]
            y[i] = y[i-1] + h * f(t[i-1], y[i-1], *args)
        return y

    @staticmethod
    def RK4(f, y0, t, args=()):
        y = np.zeros(len(t))
        y[0] = y0
        for i in range(1, len(t)):
            h = t[i] - t[i-1]; ti = t[i-1]; yi = y[i-1]
            k1 = f(ti, yi, *args)
            k2 = f(ti + h/2, yi + h*k1/2, *args)
            k3 = f(ti + h/2, yi + h*k2/2, *args)
            k4 = f(ti + h, yi + h*k3, *args)
            y[i] = yi + h/6*(k1 + 2*k2 + 2*k3 + k4)
        return y

class SystemesLineaires:
    @staticmethod
    def LU(A, b):
        n = len(A)
        L = np.eye(n); U = A.astype(float)
        for k in range(n-1):
            for i in range(k+1, n):
                L[i,k] = U[i,k] / U[k,k]
                U[i,k:] -= L[i,k] * U[k,k:]
        y = np.linalg.solve(L, b)
        x = np.linalg.solve(U, y)
        return x

def main():
    print("=" * 60)
    print("Methodes numeriques pour l'ingenieur")
    print("2AS7 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Resolution d'equations non-lineaires ---")
    f = lambda x: x**3 - 2*x - 5
    df = lambda x: 3*x**2 - 2
    r1 = ResolutionEquations.dichotomie(f, 2, 3)
    r2 = ResolutionEquations.Newton(f, df, 2)
    print(f"f(x)=x^3-2x-5 = 0")
    print(f"  Dichotomie: x = {r1:.6f}")
    print(f"  Newton:     x = {r2:.6f}")
    print(f"  Verif: f(x) = {f(r2):.2e}")

    print("\n--- 2. Interpolation de Lagrange ---")
    x = np.array([0, 1, 2, 3, 4])
    y = np.array([0, 1, 4, 9, 16])
    for xe in [0.5, 1.5, 2.5, 3.5]:
        interp = Interpolation.Lagrange(x, y, xe)
        exact = xe**2
        print(f"  x={xe:.1f}: interpole={interp:.3f}, exact={exact:.3f}")

    print("\n--- 3. Integration numerique ---")
    f_int = lambda x: np.exp(-x**2/2)
    a, b = 0, 3
    print(f"Integrale de exp(-x^2/2) de {a} a {b}")
    print(f"  Rectangles: {IntegrationNumerique.rectangles(f_int, a, b):.6f}")
    print(f"  Trapezes:   {IntegrationNumerique.trapezes(f_int, a, b):.6f}")
    print(f"  Simpson:    {IntegrationNumerique.simpson(f_int, a, b):.6f}")
    print(f"  Gauss-Leg:  {IntegrationNumerique.gauss_legendre(f_int, a, b):.6f}")

    print("\n--- 4. Resolution d'EDO - Circuit RL ---")
    def dI(t, I, R=10, L=2, E=24):
        return (E - R*I) / L
    t = np.linspace(0, 0.5, 50)
    I_euler = EDO.Euler(dI, 0, t)
    I_rk4 = EDO.RK4(dI, 0, t)
    I_exact = 24/10 * (1 - np.exp(-t*10/2))
    print(f"Circuit RL: R=10, L=2H, E=24V")
    for idx in [0, 10, 25, -1]:
        e = abs(I_euler[idx] - I_exact[idx])
        r = abs(I_rk4[idx] - I_exact[idx])
        print(f"  t={t[idx]:.3f}s: exact={I_exact[idx]:.4f}, Euler={I_euler[idx]:.4f}, RK4={I_rk4[idx]:.4f}")

    print("\n--- 5. Resolution de systemes lineaires ---")
    A = np.array([[4, -1, 0], [-1, 4, -1], [0, -1, 4]], dtype=float)
    b = np.array([15, 10, 15], dtype=float)
    x = SystemesLineaires.LU(A, b)
    print(f"Ax = b, solution x = {x}")

if __name__ == '__main__':
    main()
