"""Projet: Gestion de projet et entreprise
2AS7 - ENSEM NRJ (FISA)
Planification, PERT, Gantt, couts, risques, equipe"""

import numpy as np
from datetime import datetime, timedelta

class TacheProjet:
    def __init__(self, nom, duree_j, predecesseurs=None):
        self.nom = nom
        self.duree = duree_j
        self.predecesseurs = predecesseurs or []
        self.successeurs = []
        self.debut_au_plus_tot = 0
        self.fin_au_plus_tot = 0
        self.debut_au_plus_tard = 0
        self.fin_au_plus_tard = 0
        self.marge = 0

class ReseauPERT:
    def __init__(self):
        self.taches = {}

    def ajouter(self, nom, duree, predecs=None):
        t = TacheProjet(nom, duree, predecs or [])
        self.taches[nom] = t
        for p in t.predecesseurs:
            if p in self.taches:
                self.taches[p].successeurs.append(nom)

    def calcul_rang(self):
        taches_list = list(self.taches.values())
        for t in taches_list:
            if not t.predecesseurs:
                t.debut_au_plus_tot = 0
            else:
                t.debut_au_plus_tot = max(self.taches[p].fin_au_plus_tot for p in t.predecesseurs)
            t.fin_au_plus_tot = t.debut_au_plus_tot + t.duree

        duree_totale = max(t.fin_au_plus_tot for t in taches_list)
        for t in reversed(taches_list):
            if not t.successeurs:
                t.fin_au_plus_tard = duree_totale
            else:
                t.fin_au_plus_tard = min(self.taches[s].debut_au_plus_tard for s in t.successeurs)
            t.debut_au_plus_tard = t.fin_au_plus_tard - t.duree
            t.marge = t.debut_au_plus_tard - t.debut_au_plus_tot
        return duree_totale

    def chemin_critique(self):
        return [t.nom for t in self.taches.values() if t.marge == 0]

class DiagrammeGantt:
    def __init__(self, debut_projet):
        self.debut = debut_projet

    def afficher(self, taches):
        print(f"{'Tache':<25} {'Debut':<12} {'Fin':<12} {'Marge':<8} {'Barre':<30}")
        print("-" * 90)
        for t in sorted(taches.values(), key=lambda x: x.debut_au_plus_tot):
            deb = self.debut + timedelta(days=t.debut_au_plus_tot)
            fin = self.debut + timedelta(days=t.fin_au_plus_tot)
            barre = '#' * max(1, t.duree) + '.' * max(0, t.marge)
            critique = '*' if t.marge == 0 else ' '
            print(f"{critique}{t.nom:<24} {deb.strftime('%d/%m'):<12} {fin.strftime('%d/%m'):<12} {t.marge:<8.0f} {barre[:30]:<30}")

class AnalyseRisques:
    def __init__(self):
        self.risques = []

    def ajouter(self, nom, proba, impact, categorie='technique'):
        self.risques.append({
            'nom': nom, 'proba': proba, 'impact': impact,
            'criticite': proba * impact, 'categorie': categorie
        })

    def matrice(self):
        print(f"\nMatrice des risques:")
        print(f"{'Risque':<25} {'Prob':<8} {'Impact':<8} {'Criticite':<10} {'Cat':<12}")
        print("-" * 65)
        for r in sorted(self.risques, key=lambda x: -x['criticite']):
            niv = 'ELEVE' if r['criticite'] > 0.5 else ('MOYEN' if r['criticite'] > 0.2 else 'FAIBLE')
            print(f"{r['nom']:<25} {r['proba']:<8.2f} {r['impact']:<8.2f} {r['criticite']:<10.2f} {niv:<12}")

class BudgetProjet:
    def __init__(self, budget_total):
        self.budget = budget_total
        self.postes = {}

    def ajouter_poste(self, nom, montant):
        self.postes[nom] = montant

    def cout_total(self):
        return sum(self.postes.values())

    def ecart(self):
        return self.budget - self.cout_total()

def main():
    print("=" * 60)
    print("Gestion de projet et entreprise")
    print("2AS7 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Reseau PERT ---")
    pert = ReseauPERT()
    pert.ajouter("Etude preliminaire", 5)
    pert.ajouter("Analyse besoins", 8, ["Etude preliminaire"])
    pert.ajouter("Conception", 15, ["Analyse besoins"])
    pert.ajouter("Developpement", 20, ["Conception"])
    pert.ajouter("Tests unitaires", 8, ["Developpement"])
    pert.ajouter("Integration", 5, ["Tests unitaires"])
    pert.ajouter("Documentation", 10, ["Conception"])
    pert.ajouter("Validation", 5, ["Integration", "Documentation"])
    pert.ajouter("Deploiement", 3, ["Validation"])
    duree = pert.calcul_rang()
    print(f"Duree totale du projet: {duree} jours")
    cc = pert.chemin_critique()
    print(f"Chemin critique: {' -> '.join(cc)}")
    print(f"\nTaches et marges:")
    for t in sorted(pert.taches.values(), key=lambda x: x.debut_au_plus_tot):
        crit = " [CRITIQUE]" if t.marge == 0 else ""
        print(f"  {t.nom:<25} debut={t.debut_au_plus_tot:3.0f} fin={t.fin_au_plus_tot:3.0f} marge={t.marge:3.0f}{crit}")

    print("\n--- 2. Diagramme de Gantt ---")
    gantt = DiagrammeGantt(datetime.now())
    gantt.afficher(pert.taches)

    print("\n--- 3. Analyse des risques ---")
    risques = AnalyseRisques()
    risques.ajouter("Retard fournisseur", 0.4, 0.6, 'externe')
    risques.ajouter("Sous-dimensionnement", 0.3, 0.8, 'technique')
    risques.ajouter("Changement requis", 0.5, 0.5, 'fonctionnel')
    risques.ajouter("Absence personnel cle", 0.3, 0.7, 'humain')
    risques.ajouter("Problemes integration", 0.4, 0.4, 'technique')
    risques.matrice()

    print("\n--- 4. Budget ---")
    budget = BudgetProjet(150000)
    budget.ajouter_poste("RH (equipe projet)", 85000)
    budget.ajouter_poste("Materiel & logiciels", 25000)
    budget.ajouter_poste("Sous-traitance", 15000)
    budget.ajouter_poste("Deplacements", 8000)
    budget.ajouter_poste("Imprevus (10%)", 12000)
    print(f"Budget total: {budget.budget:,.0f} EUR")
    for nom, montant in budget.postes.items():
        print(f"  {nom:<25} {montant:>8,.0f} EUR")
    print(f"  {'Total':<25} {budget.cout_total():>8,.0f} EUR")
    print(f"  {'Ecart':<25} {budget.ecart():>8,.0f} EUR")

    print("\n--- 5. Equipe projet ---")
    equipe = {
        "Chef de projet": {"nom": "Alice", "charge": 100},
        "Ingenieur etudes": {"nom": "Bob", "charge": 80},
        "Developpeur": {"nom": "Charlie", "charge": 100},
        "Technicien": {"nom": "Diana", "charge": 50},
        "Stagiaire": {"nom": "Eve", "charge": 100},
    }
    print(f"{'Role':<25} {'Nom':<12} {'Charge':<10}")
    print("-" * 47)
    for role, info in equipe.items():
        barre = '#' * (info['charge'] // 10)
        print(f"{role:<25} {info['nom']:<12} {info['charge']:<3}% {barre}")

if __name__ == '__main__':
    main()
