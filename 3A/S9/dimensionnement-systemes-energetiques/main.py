"""Projet: Dimensionnement des systèmes énergétiques
3AS9 - ENSEM NRJ (FISA)
Outil de pré-dimensionnement pour systèmes photovoltaïques et éoliens"""

class PanneauSolaire:
    def __init__(self, Pmax=300, Vmp=33.0, Imp=9.1, Voc=40.0, Isc=9.8, surface=1.6):
        self.Pmax = Pmax        # Puissance crête [W]
        self.Vmp = Vmp          # Tension max puissance [V]
        self.Imp = Imp          # Courant max puissance [A]
        self.Voc = Voc          # Tension circuit ouvert [V]
        self.Isc = Isc          # Courant court-circuit [A]
        self.surface = surface  # Surface [m2]
        self.rendement = Pmax / (surface * 1000)

    def production_journaliere(self, ensoleillement_kwh_m2_j, nb_heures_soleil=5):
        return self.Pmax * ensoleillement_kwh_m2_j * nb_heures_soleil / 1000

    def __str__(self):
        return f"Panneau {self.Pmax}W, η={self.rendement:.1%}"

class Eolienne:
    def __init__(self, Pnom=5000, D_rotor=3.0, hauteur=12):
        self.Pnom = Pnom          # Puissance nominale [W]
        self.D_rotor = D_rotor    # Diamètre rotor [m]
        self.A_rotor = np.pi * (D_rotor/2)**2  # Surface balayée [m2]
        self.hauteur = hauteur    # Hauteur du mât [m]

    def puissance(self, v_vent, rho_air=1.225):
        Cp = 0.45  # Coefficient de puissance (limite Betz=0.593)
        P_dispo = 0.5 * rho_air * self.A_rotor * v_vent**3
        P_elec = P_dispo * Cp
        return min(P_elec, self.Pnom)

    def production_annuelle(self, vitesses, frequences):
        prod = 0
        for v, f in zip(vitesses, frequences):
            prod += self.puissance(v) * 8760 * f
        return prod / 1000  # kWh

class Batterie:
    def __init__(self, capacite_kwh=10, tension=48, DOD_max=0.8, rendement=0.95):
        self.capacite_kwh = capacite_kwh
        self.tension = tension
        self.capacite_ah = capacite_kwh * 1000 / tension
        self.DOD_max = DOD_max
        self.rendement = rendement
        self.SOC = 0.5  # State of Charge initial

    def stocker(self, energie_kwh):
        delta = energie_kwh * self.rendement
        self.SOC = min(self.SOC + delta / self.capacite_kwh, 1.0)

    def decharger(self, besoin_kwh):
        dispo = self.SOC * self.capacite_kwh * self.DOD_max
        preleve = min(besoin_kwh, dispo)
        self.SOC -= preleve / self.capacite_kwh
        return preleve

class SystemeHybride:
    def __init__(self, panneaux=[], eoliennes=[], batterie=None):
        self.panneaux = panneaux
        self.eoliennes = eoliennes
        self.batterie = batterie

    def dimensionner_pv(self, conso_journaliere_kwh, ensolleillement):
        besoin_kwh = conso_journaliere_kwh / 0.85  # 15% pertes
        for pv in self.panneaux:
            prod = pv.production_journaliere(ensolleillement)
            n = int(np.ceil(besoin_kwh / prod))
            print(f"  {pv}: besoin {besoin_kwh:.1f}kWh/j, {n} panneaux (production {n*prod:.1f}kWh/j)")

def main():
    print("=" * 60)
    print("Dimensionnement des systèmes énergétiques")
    print("=" * 60)
    import numpy as np

    pv_std = PanneauSolaire(Pmax=400, Vmp=34.5, Imp=11.6, surface=1.8)
    eolienne = Eolienne(Pnom=3000, D_rotor=4.0)
    batterie = Batterie(capacite_kwh=13.5, tension=48)

    print(f"\nPanneau standard: {pv_std}")
    print(f"Eolienne: {eolienne.Pnom//1000:.0f}kW, rotor D={eolienne.D_rotor}m")
    print(f"Batterie: {batterie.capacite_kwh}kWh, {batterie.tension}V")

    print("\n--- Dimensionnement PV pour maison individuelle ---")
    systeme = SystemeHybride(panneaux=[pv_std], batterie=batterie)
    systeme.dimensionner_pv(conso_journaliere_kwh=10, ensolleillement=4.5)

    print("\n--- Production éolienne ---")
    vitesses = np.arange(1, 26)
    freqs = np.exp(-0.5*((vitesses-8)/4)**2)
    freqs /= freqs.sum()
    prod_annuelle = eolienne.production_annuelle(vitesses, freqs)
    print(f"Production annuelle estimée: {prod_annuelle:.0f} kWh/an")

    print("\n--- Stockage batterie journalier ---")
    for jour in range(5):
        prod = 8 + np.random.randn() * 2
        conso = 10 + np.random.randn() * 3
        if prod > conso:
            batterie.stocker(prod - conso)
        else:
            batterie.decharger(conso - prod)
        print(f"  Jour {jour+1}: prod={prod:.1f}, conso={conso:.1f}, SOC={batterie.SOC:.0%}")

if __name__ == '__main__':
    main()
