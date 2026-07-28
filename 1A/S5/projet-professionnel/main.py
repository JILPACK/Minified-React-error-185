"""Projet: Projet professionnel
1AS5 - ENSEM NRJ (FISA)
Projet personnel et professionnel, connaissance entreprise, metiers"""

import datetime

class ProfilPersonnel:
    def __init__(self, nom, prenom, formation):
        self.nom = nom
        self.prenom = prenom
        self.formation = formation
        self.competences = []
        self.interets = []
        self.objectifs = []
        self.forces = []
        self.faiblesses = []

    def auto_evaluation(self):
        print(f"\nAUTO-EVALUATION: {self.prenom} {self.nom}")
        print("-" * 50)
        print(f"Formation: {self.formation}")
        print(f"\nPoints forts: {', '.join(self.forces) if self.forces else 'A definir'}")
        print(f"Points a ameliorer: {', '.join(self.faiblesses) if self.faiblesses else 'A definir'}")
        print(f"Competences: {', '.join(self.competences) if self.competences else 'A definir'}")
        print(f"Interets: {', '.join(self.interets) if self.interets else 'A definir'}")

class MetiersEnergie:
    def __init__(self):
        self.metiers = {
            'Ingenieur R&D': 'Concevoir et innover dans le domaine energetique',
            'Ingenieur exploitation': 'Gerer le fonctionnement des installations',
            'Chef de projet': 'Coordonner les equipes et les budgets',
            'Consultant energie': 'Conseiller les entreprises sur leur strategie',
            'Ingenieur maintenance': 'Assurer la disponibilite des equipements',
            'Bureau d\'etudes': 'Dimensionner et concevoir des systemes',
        }

    def afficher(self):
        print(f"\nMETIERS DU SECTEUR ENERGETIQUE")
        print("-" * 50)
        for metier, desc in self.metiers.items():
            print(f"  {metier:<25}: {desc}")

class ProjetPro:
    def __init__(self, titre):
        self.titre = titre
        self.etapes = []

    def ajouter_etape(self, nom, deadline, actions):
        self.etapes.append({'nom': nom, 'deadline': deadline, 'actions': actions})

    def plan_action(self):
        print(f"\nPLAN D'ACTION - {self.titre}")
        print("=" * 50)
        for i, e in enumerate(self.etapes, 1):
            print(f"\n  Etape {i}: {e['nom']} (Deadline: {e['deadline']})")
            for action in e['actions']:
                print(f"    - {action}")

class ConnaissanceEntreprise:
    def __init__(self, nom, secteur, taille):
        self.nom = nom
        self.secteur = secteur
        self.taille = taille
        self.metiers_cles = []
        self.valeurs = []

    def description(self):
        print(f"\nENTREPRISE: {self.nom}")
        print("-" * 50)
        print(f"Secteur: {self.secteur}")
        print(f"Taille: {self.taille}")
        print(f"Metiers cles: {', '.join(self.metiers_cles) if self.metiers_cles else 'N/A'}")
        print(f"Valeurs: {', '.join(self.valeurs) if self.valeurs else 'N/A'}")

def questions_reflexion():
    print("\nQUESTIONS POUR REFLECHIR A SON PROJET")
    print("-" * 50)
    questions = [
        "Quelles sont vos motivations pour ce metier ?",
        "Quels sont vos atouts pour reussir ?",
        "Quel type d'entreprise vous attire ?",
        "Preferez-vous la recherche, le terrain ou le management ?",
        "Quelles competences voulez-vous developper ?",
        "Ou vous voyez-vous dans 5 ans ? 10 ans ?",
        "Quel impact voulez-vous avoir sur la societe ?",
    ]
    for i, q in enumerate(questions, 1):
        print(f"  Q{i}: {q}")

def main():
    print("=" * 60)
    print("Projet professionnel")
    print("1AS5 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Profil personnel ---")
    profil = ProfilPersonnel("Dupont", "Marie", "1A ENSEM - NRJ")
    profil.forces = ["Rigueur", "Curiosite scientifique", "Travail en equipe"]
    profil.faiblesses = ["Prise de parole en public", "Anglais technique"]
    profil.competences = ["Python", "Matlab", "Bases electrotechnique"]
    profil.interets = ["Energies renouvelables", "Efficacite energetique"]
    profil.auto_evaluation()

    print("\n--- 2. Metiers du secteur ---")
    metiers = MetiersEnergie()
    metiers.afficher()

    print("\n--- 3. Plan d'action ---")
    projet = ProjetPro("Devenir ingenieur en efficacite energetique")
    projet.ajouter_etape("Reussir la 1A", "Juin 2026", [
        "Valider tous les modules (10/10)",
        "Obtenir un stage d'observation",
        "Atteindre le niveau B2 en anglais"
    ])
    projet.ajouter_etape("Approfondir en 2A", "Juin 2027", [
        "Choisir les options NRJ pertinentes",
        "Trouver une alternance",
        "Participer a un projet etudiant"
    ])
    projet.ajouter_etape("Se professionaliser en 3A", "Juin 2028", [
        "Finaliser le projet de fin d'etudes",
        "Developper son reseau professionnel",
        "Preparer l'insertion professionnelle"
    ])
    projet.plan_action()

    print("\n--- 4. Connaissance entreprise ---")
    entreprise = ConnaissanceEntreprise("EDF", "Energie", ">100000 employes")
    entreprise.metiers_cles = ["Ingenieur production", "Ingenieur R&D", "Chef de projet"]
    entreprise.valeurs = ["Securite", "Performance", "Solidarite", "Innovation"]
    entreprise.description()

    print("\n--- 5. Reflexion personnelle ---")
    questions_reflexion()

    print("\n" + "=" * 60)
    print("LIVRABLES")
    print("=" * 60)
    livrables = [
        "Fiche de profil personnel",
        "Rapport sur un metier du secteur",
        "Plan d'action personnel (1 an)",
        "Fiche entreprise (1 page)",
        "Soutenance orale (5 min)",
    ]
    for i, liv in enumerate(livrables, 1):
        print(f"  {i}. {liv}")

if __name__ == '__main__':
    main()
