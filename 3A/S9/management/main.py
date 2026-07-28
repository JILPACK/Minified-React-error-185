"""Projet: Management
3AS9 - ENSEM NRJ (FISA)
Gestion de projet, analyse financière et management d'équipe"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class TacheProjet:
    def __init__(self, nom, duree_jours, predecesseurs=None, ressources=1, cout_journalier=500):
        self.nom = nom
        self.duree = duree_jours
        self.predecesseurs = predecesseurs or []
        self.ressources = ressources
        self.cout_journalier = cout_journalier
        self.debut = None
        self.fin = None
        self.marge = 0

    def __str__(self):
        return f"{self.nom} ({self.duree}j, {self.ressources} res)"

class DiagrammeGantt:
    def __init__(self, taches):
        self.taches = taches

    def calculer_chemin_critique(self):
        for t in self.taches:
            if not t.predecesseurs:
                t.debut = 0
            else:
                t.debut = max(p.fin for p in t.predecesseurs)
            t.fin = t.debut + t.duree

        fin_projet = max(t.fin for t in self.taches)
        for t in reversed(self.taches):
            successeurs = [s for s in self.taches if t in s.predecesseurs]
            if not successeurs:
                t.fin_max = fin_projet
            else:
                t.fin_max = min(s.debut for s in successeurs)
            t.marge = t.fin_max - t.fin

        return [t for t in self.taches if t.marge == 0]

    def afficher(self):
        print(f"\n=== Diagramme de Gantt ===")
        fin_projet = max(t.fin for t in self.taches)
        print(f"Durée totale: {fin_projet} jours")
        print(f"{'Tâche':<25} {'Début':<8} {'Fin':<8} {'Marge':<8} {'Critique':<8}")
        print("-" * 60)
        chemin_critique = self.calculer_chemin_critique()
        for t in self.taches:
            critique = "OUI" if t in chemin_critique else ""
            print(f"{t.nom:<25} {t.debut:<8.0f} {t.fin:<8.0f} {t.marge:<8.0f} {critique:<8}")

class AnalyseFinanciere:
    def __init__(self, investissement, flux_tresorerie, taux_actualisation=0.08):
        self.I = investissement
        self.F = flux_tresorerie
        self.taux = taux_actualisation

    def VAN(self):
        van = -self.I
        for t, ft in enumerate(self.F, 1):
            van += ft / (1 + self.taux)**t
        return van

    def TRI(self):
        from scipy.optimize import brentq
        f = lambda r: -self.I + sum(ft / (1+r)**(t+1) for t, ft in enumerate(self.F))
        try:
            return brentq(f, -0.99, 10)
        except (ValueError, RuntimeError):
            return None

    def delai_recuperation(self):
        cumul = -self.I
        for t, ft in enumerate(self.F, 1):
            cumul += ft
            if cumul >= 0:
                return t - 1 + (cumul - ft) / ft if t > 1 else t
        return None

    def IP(self):
        van = self.VAN()
        return (van + self.I) / self.I if self.I != 0 else 0

class GestionEquipe:
    def __init__(self):
        self.membres = []
        self.taches_assignees = {}

    def ajouter_membre(self, nom, competences, charge_max=1.0):
        self.membres.append({'nom': nom, 'competences': competences, 'charge': 0, 'charge_max': charge_max})

    def assigner(self, tache, competence_requise, charge):
        dispo = [m for m in self.membres
                 if competence_requise in m['competences']
                 and m['charge'] + charge <= m['charge_max']]
        if dispo:
            m = min(dispo, key=lambda x: x['charge'])
            m['charge'] += charge
            return m['nom']
        return None

    def bilan_charge(self):
        print(f"\n=== Bilan des charges ===")
        for m in self.membres:
            barre = '█' * int(m['charge'] / m['charge_max'] * 20)
            print(f"{m['nom']:<15} {m['charge']/m['charge_max']*100:5.0f}% {barre}")

def main():
    print("=" * 60)
    print("Management - Gestion de Projet")
    print("3AS9 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Planification de projet (Gantt / Chemin critique) ---")
    t1 = TacheProjet("Étude préliminaire", 5)
    t2 = TacheProjet("Spécifications", 8, [t1])
    t3 = TacheProjet("Développement hardware", 25, [t2])
    t4 = TacheProjet("Développement logiciel", 20, [t2])
    t5 = TacheProjet("Tests unitaires", 10, [t3, t4])
    t6 = TacheProjet("Intégration", 7, [t5])
    t7 = TacheProjet("Validation", 5, [t6])
    t8 = TacheProjet("Documentation", 8, [t2], ressources=1)
    t9 = TacheProjet("Déploiement", 3, [t7, t8])

    projet = DiagrammeGantt([t1, t2, t3, t4, t5, t6, t7, t8, t9])
    chemin_critique = projet.calculer_chemin_critique()
    projet.afficher()
    print(f"\nChemin critique: {' → '.join(t.nom for t in chemin_critique)}")

    print("\n--- 2. Analyse financière ---")
    af = AnalyseFinanciere(50000, [15000, 18000, 22000, 25000, 30000], taux_actualisation=0.10)
    print(f"Investissement: {af.I:,.0f} €")
    print(f"VAN (taux={af.taux:.0%}): {af.VAN():,.0f} €")
    tri = af.TRI()
    if tri: print(f"TRI: {tri:.1%}")
    print(f"Délai de récupération: {af.delai_recuperation():.1f} ans")
    print(f"Indice de profitabilité: {af.IP():.2f}")

    print("\n--- 3. Gestion d'équipe ---")
    equipe = GestionEquipe()
    equipe.ajouter_membre("Alice", ["mécanique", "thermique"], 1.0)
    equipe.ajouter_membre("Bob", ["électrique", "contrôle"], 1.0)
    equipe.ajouter_membre("Charlie", ["logiciel", "électrique"], 0.8)
    equipe.ajouter_membre("Diana", ["thermique", "matériaux"], 1.0)

    assign = [
        ("Conception échangeur", "thermique", 0.4),
        ("Câblage armoire", "électrique", 0.3),
        ("Programmation API", "logiciel", 0.6),
        ("Analyse thermique", "thermique", 0.5),
        ("Schémas électriques", "électrique", 0.4),
        ("Tests matériaux", "matériaux", 0.3),
    ]
    for tache, comp, charge in assign:
        result = equipe.assigner(tache, comp, charge)
        print(f"  {tache:<30} → {result if result else 'PAS ASSIGNÉ'}")

    equipe.bilan_charge()

if __name__ == '__main__':
    main()
