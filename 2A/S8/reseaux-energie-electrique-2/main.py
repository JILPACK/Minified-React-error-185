"""Projet: Réseaux d'énergie électrique 2
2AS8 - ENSEM NRJ (FISA)
Analyse de réseaux électriques, court-circuit, et protection"""

import numpy as np

class LigneElectrique:
    def __init__(self, R=0.15, L=1.3e-3, C=10e-9, longueur_km=50, Vnom=63e3):
        self.R = R / 1000       # Résistance linéique [Ω/m]
        self.L = L / 1000       # Inductance linéique [H/m]
        self.C = C / 1000       # Capacité linéique [F/m]
        self.L_km = longueur_km
        self.longueur = longueur_km * 1000
        self.Vnom = Vnom
        self.Z = np.sqrt((R/1000)**2 + (2*np.pi*50*L/1000)**2) * self.longueur

    def impedance(self, f=50):
        R_total = self.R * self.longueur
        X_total = 2 * np.pi * f * self.L * self.longueur
        return np.sqrt(R_total**2 + X_total**2)

    def chute_tension(self, I, phi=30):
        R_total = self.R * self.longueur
        X_total = 2 * np.pi * 50 * self.L * self.longueur
        dV = I * (R_total * np.cos(np.deg2rad(phi)) + X_total * np.sin(np.deg2rad(phi)))
        return dV

class CalculateurCourtCircuit:
    def __init__(self, S_cc=500e6, V_base=63e3):
        self.S_cc = S_cc
        self.V_base = V_base
        self.I_cc = S_cc / (np.sqrt(3) * V_base)

    def courant_cc_triphase(self, Z_eq):
        return self.V_base / (np.sqrt(3) * Z_eq)

    def courant_cc_biphas(self, Z_eq):
        return self.V_base / (2 * Z_eq)

    def courant_cc_monophase(self, Z_eq, Z_n=0):
        return self.V_base / (np.sqrt(3) * (2*Z_eq + Z_n))

    def puissance_cc(self, I_cc):
        return np.sqrt(3) * self.V_base * I_cc / 1e6  # MVA

class ProtectionReseau:
    def __init__(self):
        self.relais = []

    def ajouter_relais(self, nom, seuil_I, temps, courbe='DI'):
        self.relais.append({'nom': nom, 'seuil': seuil_I, 'temps': temps, 'courbe': courbe})

    def coordonner(self, I_defaut):
        print(f"\nCoordination des protections (I_défaut={I_defaut:.0f} A):")
        actifs = sorted([r for r in self.relais if I_defaut > r['seuil']],
                       key=lambda x: x['temps'])
        for i, r in enumerate(actifs):
            print(f"  {r['nom']}: seuil={r['seuil']:.0f}A, t={r['temps']:.2f}s {'OK DECLENCHE' if i==0 else ''}")

class AnalysePoste:
    def __init__(self, Vnom=63e3):
        self.Vnom = Vnom
        self.transformateurs = []
        self.disjoncteurs = []

    def ajouter_transfo(self, Sn, V1, V2, Uk=0.08):
        self.transformateurs.append({
            'Sn': Sn, 'V1': V1, 'V2': V2, 'Uk': Uk,
            'Icc': Sn / (np.sqrt(3) * Uk * min(V1, V2))
        })

    def plan_protection(self):
        print(f"\nPlan de protection - Poste {self.Vnom/1e3:.0f} kV")
        for t in self.transformateurs:
            print(f"  Transfo {t['Sn']/1e6:.0f} MVA {t['V1']/1e3:.0f}/{t['V2']/1e3:.0f} kV")
            print(f"    I_cc max: {t['Icc']:.0f} A")
            calibre = t['Sn'] / (np.sqrt(3) * t['V2']) * 1.4
            print(f"    Calibre disjoncteur: {calibre:.0f} A")

def main():
    print("=" * 60)
    print("Réseaux d'énergie électrique 2")
    print("2AS8 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Ligne électrique - paramètres et chute de tension ---")
    ligne = LigneElectrique(R=0.12, L=1.2e-3, C=11e-9, longueur_km=40, Vnom=63e3)
    print(f"Ligne 63kV, {ligne.L_km}km")
    print(f"Impédance totale: {ligne.impedance():.2f} Ω")
    I_charge = 200
    dV = ligne.chute_tension(I_charge)
    print(f"Chute de tension à {I_charge}A: {dV:.0f} V ({dV/ligne.Vnom*100:.2f}%)")

    print("\n--- 2. Calcul de court-circuit ---")
    cc = CalculateurCourtCircuit(S_cc=800e6, V_base=63e3)
    print(f"I_cc source: {cc.I_cc:.0f} A")
    Z_ligne = ligne.impedance()
    I_cc_tri = cc.courant_cc_triphase(Z_ligne)
    print(f"I_cc triphasé (fin de ligne): {I_cc_tri:.0f} A")
    print(f"S_cc: {cc.puissance_cc(I_cc_tri):.1f} MVA")

    print("\n--- 3. Coordination des protections ---")
    prot = ProtectionReseau()
    prot.ajouter_relais("Disjoncteur A (amont)", seuil_I=800, temps=0.5)
    prot.ajouter_relais("Disjoncteur B (aval)", seuil_I=600, temps=0.3)
    prot.ajouter_relais("Fusible C (branche)", seuil_I=300, temps=0.1)
    prot.coordonner(I_defaut=1200)

    print("\n--- 4. Dimensionnement poste source ---")
    poste = AnalysePoste(Vnom=63e3)
    poste.ajouter_transfo(Sn=36e6, V1=63e3, V2=20e3)
    poste.ajouter_transfo(Sn=36e6, V1=63e3, V2=20e3)
    poste.plan_protection()

if __name__ == '__main__':
    main()
