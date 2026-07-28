"""Projet: Réseaux d'énergie électrique 3 - Analyse de flux de puissance
3AS9 - ENSEM NRJ (FISA)
Newton-Raphson pour l'écoulement de puissance dans un réseau électrique"""

import numpy as np

class ReseauElectrique:
    def __init__(self):
        self.noeuds = {}
        self.lignes = []
        self.Ybus = None
        self.n = 0

    def ajouter_noeud(self, nom, type, V=1.0, theta=0.0, Pg=0, Qg=0, Pd=0, Qd=0):
        self.noeuds[nom] = {
            'type': type,    # 'SL' = slack, 'PV' = génération, 'PQ' = charge
            'V': V, 'theta': np.deg2rad(theta),
            'Pg': Pg, 'Qg': Qg, 'Pd': Pd, 'Qd': Qd,
            'P': Pg - Pd, 'Q': Qg - Qd
        }

    def ajouter_ligne(self, de, vers, R=0.0, X=0.01, B=0.0):
        self.lignes.append({'de': de, 'vers': vers, 'R': R, 'X': X, 'B': B})

    def construire_Ybus(self):
        ordre = list(self.noeuds.keys())
        self.n = len(ordre)
        self.ordre = ordre
        Y = np.zeros((self.n, self.n), dtype=complex)
        for l in self.lignes:
            i, j = ordre.index(l['de']), ordre.index(l['vers'])
            z = complex(l['R'], l['X'])
            if abs(z) > 0:
                y = 1.0 / z
                Y[i,i] += y
                Y[j,j] += y
                Y[i,j] -= y
                Y[j,i] -= y
        self.Ybus = Y
        return Y

    def resoudre_newton_raphson(self, tol=1e-6, max_iter=20):
        ordre = self.ordre
        n = self.n
        slack_idx = None
        pv_idx = []
        pq_idx = []
        for i, nom in enumerate(ordre):
            t = self.noeuds[nom]['type']
            if t == 'SL': slack_idx = i
            elif t == 'PV': pv_idx.append(i)
            elif t == 'PQ': pq_idx.append(i)

        V = np.array([self.noeuds[nom]['V'] for nom in ordre])
        theta = np.array([self.noeuds[nom]['theta'] for nom in ordre])

        for iteration in range(max_iter):
            P_calc, Q_calc = self._calculer_puissances(V, theta)

            dP = np.array([self.noeuds[ordre[i]]['P'] - P_calc[i] for i in range(n) if i != slack_idx])
            dQ = np.array([self.noeuds[ordre[i]]['Q'] - Q_calc[i] for i in pq_idx])

            if max(abs(dP)) < tol and max(abs(dQ)) < tol:
                print(f"Convergence en {iteration+1} itérations")
                break

            J = self._construire_jacobienne(V, theta, slack_idx, pv_idx, pq_idx)
            dx = np.linalg.solve(J, np.concatenate([dP, dQ]))

            n_theta = n - 1  # sans slack
            for k, i in enumerate([i for i in range(n) if i != slack_idx]):
                theta[i] += dx[k]
            for k, i in enumerate(pq_idx):
                V[i] += dx[n_theta + k]

        print(f"V: {V}")
        print(f"Theta (deg): {np.rad2deg(theta)}")

    def _calculer_puissances(self, V, theta):
        n = self.n
        P = np.zeros(n)
        Q = np.zeros(n)
        for i in range(n):
            for j in range(n):
                Yij = self.Ybus[i,j]
                Gij, Bij = Yij.real, Yij.imag
                angle = theta[i] - theta[j]
                P[i] += V[i] * V[j] * (Gij * np.cos(angle) + Bij * np.sin(angle))
                Q[i] += V[i] * V[j] * (Gij * np.sin(angle) - Bij * np.cos(angle))
        return P, Q

    def _construire_jacobienne(self, V, theta, slack_idx, pv_idx, pq_idx):
        n = self.n
        n_theta = n - 1
        n_v = len(pq_idx)
        J = np.zeros((n_theta + n_v, n_theta + n_v))
        indices_theta = [i for i in range(n) if i != slack_idx]
        for a, i in enumerate(indices_theta):
            for b, j in enumerate(indices_theta):
                J[a,b] = self._dP_dtheta(i, j, V, theta)
        for a, i in enumerate(indices_theta):
            for b, j in enumerate(pq_idx):
                J[a, n_theta + b] = self._dP_dV(i, j, V, theta)
        for a, i in enumerate(pq_idx):
            for b, j in enumerate(indices_theta):
                J[n_theta + a, b] = self._dQ_dtheta(i, j, V, theta)
        for a, i in enumerate(pq_idx):
            for b, j in enumerate(pq_idx):
                J[n_theta + a, n_theta + b] = self._dQ_dV(i, j, V, theta)
        return J

    def _dP_dtheta(self, i, j, V, theta):
        if i == j:
            s = 0
            for k in range(self.n):
                if k != i:
                    Yik = self.Ybus[i,k]
                    angle = theta[i] - theta[k]
                    s += V[k] * (Yik.real * np.sin(angle) - Yik.imag * np.cos(angle))
            return -V[i] * s
        else:
            Yij = self.Ybus[i,j]
            angle = theta[i] - theta[j]
            return V[i] * V[j] * (Yij.real * np.sin(angle) - Yij.imag * np.cos(angle))

    def _dP_dV(self, i, j, V, theta):
        if i == j:
            return self._calculer_puissances(V, theta)[0][i] / V[i] + V[i] * self.Ybus[i,i].real
        else:
            Yij = self.Ybus[i,j]
            angle = theta[i] - theta[j]
            return V[i] * (Yij.real * np.cos(angle) + Yij.imag * np.sin(angle))

    def _dQ_dtheta(self, i, j, V, theta):
        if i == j:
            s = 0
            for k in range(self.n):
                if k != i:
                    Yik = self.Ybus[i,k]
                    angle = theta[i] - theta[k]
                    s += V[k] * (Yik.real * np.cos(angle) + Yik.imag * np.sin(angle))
            return -V[i] * s
        else:
            Yij = self.Ybus[i,j]
            angle = theta[i] - theta[j]
            return -V[i] * V[j] * (Yij.real * np.cos(angle) + Yij.imag * np.sin(angle))

    def _dQ_dV(self, i, j, V, theta):
        if i == j:
            return self._calculer_puissances(V, theta)[1][i] / V[i] - V[i] * self.Ybus[i,i].imag
        else:
            Yij = self.Ybus[i,j]
            angle = theta[i] - theta[j]
            return V[i] * (Yij.real * np.sin(angle) - Yij.imag * np.cos(angle))

def main():
    print("=" * 60)
    print("Analyse de flux de puissance - Newton-Raphson")
    print("Réseau 3 noeuds (Slack - PV - PQ)")
    print("=" * 60)
    reseau = ReseauElectrique()
    reseau.ajouter_noeud("N1", "SL", V=1.06, theta=0)
    reseau.ajouter_noeud("N2", "PV", V=1.04, Pg=0.5, Pd=0.3)
    reseau.ajouter_noeud("N3", "PQ", Pd=0.6, Qd=0.25)

    reseau.ajouter_ligne("N1", "N2", R=0.02, X=0.06, B=0.03)
    reseau.ajouter_ligne("N1", "N3", R=0.05, X=0.20, B=0.02)
    reseau.ajouter_ligne("N2", "N3", R=0.04, X=0.15, B=0.02)

    Ybus = reseau.construire_Ybus()
    print(f"\nMatrice admittance Ybus:\n{Ybus}\n")
    reseau.resoudre_newton_raphson()

if __name__ == '__main__':
    main()
