"""Projet: Projet integre S6
1AS6 - ENSEM NRJ (FISA)
Projet pluridisciplinaire de synthese"""

import numpy as np
import json
import datetime

class GestionProjet:
    def __init__(self, nom, equipe):
        self.nom = nom
        self.equipe = equipe
        self.taches = []
        self.debut = datetime.date.today()
        self.budget = 0

    def ajouter_tache(self, nom, duree_j, responsables, prerequis=None):
        self.taches.append({
            'nom': nom, 'duree': duree_j,
            'responsables': responsables,
            'prerequis': prerequis or [],
            'statut': 'A faire'
        })

    def planifier(self):
        print(f"\nPlanification - Projet: {self.nom}")
        print(f"Equipe: {', '.join(self.equipe)}")
        print(f"{'Tache':<25} {'Duree':<8} {'Responsable':<15} {'Statut':<12}")
        print("-" * 60)
        for t in self.taches:
            resp = ', '.join(t['responsables'])
            print(f"{t['nom']:<25} {t['duree']:<8} {resp:<15} {t['statut']:<12}")

    def cout_estime(self, taux_horaire=50):
        cout_total = 0
        for t in self.taches:
            cout_total += t['duree'] * 7 * taux_horaire
        return cout_total

class SimulationSysteme:
    def __init__(self):
        self.composants = {}

    def ajouter_composant(self, nom, type, params):
        self.composants[nom] = {'type': type, 'params': params}

    def simuler_chaine_energie(self, P_source):
        P = P_source
        bilan = {'source': P}
        for nom, comp in self.composants.items():
            eta = comp['params'].get('rendement', 0.9)
            P *= eta
            bilan[nom] = P
        return bilan

    def evaluer_performances(self):
        resultats = {}
        for nom, comp in self.composants.items():
            if comp['type'] == 'moteur':
                P = comp['params'].get('P', 1000)
                eta = comp['params'].get('rendement', 0.85)
                resultats[nom] = {'P_utile': P*eta, 'Pertes': P*(1-eta)}
        return resultats

class AnalyseDonnees:
    def __init__(self):
        self.mesures = []

    def ajouter_mesure(self, t, valeur, capteur):
        self.mesures.append({'t': t, 'valeur': valeur, 'capteur': capteur})

    def statistiques(self, capteur=None):
        vals = [m['valeur'] for m in self.mesures
                if capteur is None or m['capteur'] == capteur]
        if not vals:
            return {}
        return {
            'moyenne': np.mean(vals),
            'ecart_type': np.std(vals),
            'min': min(vals),
            'max': max(vals),
            'n': len(vals)
        }

    def tendance(self, capteur):
        vals = [(m['t'], m['valeur']) for m in self.mesures
                if m['capteur'] == capteur]
        if len(vals) < 2:
            return 0
        t_vals = np.array([v[0] for v in vals])
        v_vals = np.array([v[1] for v in vals])
        coeffs = np.polyfit(t_vals, v_vals, 1)
        return coeffs[0]

def main():
    print("=" * 60)
    print("Projet integre S6")
    print("1AS6 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Gestion de projet ---")
    projet = GestionProjet(
        "Systeme de monitoring energetique",
        ["Alice (chef)", "Bob", "Charlie", "Diana"]
    )
    projet.ajouter_tache("Analyse fonctionnelle", 5, ["Alice", "Bob"])
    projet.ajouter_tache("Dimensionnement", 8, ["Bob", "Charlie"])
    projet.ajouter_tache("Acquisition donnees", 10, ["Charlie"])
    projet.ajouter_tache("Developpement interface", 12, ["Alice", "Diana"])
    projet.ajouter_tache("Tests et validation", 5, ["Tous"])
    projet.ajouter_tache("Rapport final", 4, ["Alice"])
    projet.planifier()
    cout = projet.cout_estime(45)
    print(f"\nCout total estime: {cout:,.0f} EUR ({cout/len(projet.equipe):,.0f} EUR/pers)")

    print("\n--- 2. Simulation chaine energetique ---")
    sim = SimulationSysteme()
    sim.ajouter_composant("Panneau solaire", "generateur", {'rendement': 0.20})
    sim.ajouter_composant("Regulateur", "convertisseur", {'rendement': 0.95})
    sim.ajouter_composant("Batterie", "stockage", {'rendement': 0.90})
    sim.ajouter_composant("Onduleur", "convertisseur", {'rendement': 0.93})
    P_dispo = 1000
    bilan = sim.simuler_chaine_energie(P_dispo)
    print(f"Chaine: Panneau -> Regulateur -> Batterie -> Onduleur")
    for nom, P in bilan.items():
        print(f"  {nom:<20}: P={P:.1f} W")
    print(f"  Rendement global: {bilan['Onduleur']/P_dispo*100:.1f}%")

    print("\n--- 3. Analyse de donnees ---")
    ad = AnalyseDonnees()
    np.random.seed(42)
    for t in np.linspace(0, 24, 50):
        ad.ajouter_mesure(t, 300 + 200*np.sin(np.pi*t/12 - np.pi/2) + np.random.randn()*20, "Panneau")
        ad.ajouter_mesure(t, 23 + 5*np.sin(np.pi*t/12) + np.random.randn()*0.5, "Temperature")
    stats_p = ad.statistiques("Panneau")
    stats_t = ad.statistiques("Temperature")
    print(f"Capteur Panneau solaire:")
    for k, v in stats_p.items():
        if k != 'n':
            print(f"  {k}: {v:.1f}")
    print(f"Capteur Temperature:")
    for k, v in stats_t.items():
        if k != 'n':
            print(f"  {k}: {v:.1f}")

    print("\n--- 4. Synthese et rendu final ---")
    print("Livrables:")
    livrables = [
        "Cahier des charges fonctionnel",
        "Schema de principe et dimensionnement",
        "Programme d'acquisition et traitement",
        "Interface de supervision",
        "Rapport technique (15-20 pages)",
        "Soutenance orale (15 min)",
    ]
    for i, liv in enumerate(livrables, 1):
        print(f"  {i}. {liv}")

if __name__ == '__main__':
    main()
