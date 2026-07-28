"""Projet: Compétences Entreprise S9
3AS9 - ENSEM NRJ (FISA)
Bilan des compétences techniques, méthodologiques et relationnelles"""

BILAN_TECHNIQUE = """
COMPÉTENCES TECHNIQUES (EC_Compétence technique)
================================================
Domaines évalués:
  1. Conception et dimensionnement de systèmes énergétiques
  2. Modélisation et simulation (Python, MATLAB/Simulink)
  3. Automatisme et contrôle-commande
  4. Réseaux électriques et électronique de puissance
  5. Analyse de données et expérimentation

Niveau d'acquisition:
  [ ] 1 - Notions
  [ ] 2 - Appliqué avec assistance
  [ ] 3 - Autonome
  [ ] 4 - Avancé (peut former)
  [ ] 5 - Expert

Projets réalisés en S9:
  1. Transferts d'énergies avancés (simulation thermique)
  2. Dimensionnement de systèmes PV-Batterie
  3. Analyse de flux de puissance (Newton-Raphson)
  4. Modélisation de machines électriques
  5. Spécialisation au choix (9_4, 9_1, 9_6, 9_10, 9_14, 9_13)

Auto-évaluation:
  Compétence                    | Avant S9 | Après S9 | Progression
  ------------------------------|----------|----------|------------
  Programmation (Python)        |          |          |
  Simulation numérique          |          |          |
  Dimensionnement énergétique   |          |          |
  Analyse de données            |          |          |
  Travail en équipe projet      |          |          |
"""

BILAN_METHODOLOGIQUE = """
COMPÉTENCES MÉTHODOLOGIQUES (EC_Compétence méthodologique)
========================================================
1. GESTION DE PROJET
   - Cahier des charges et spécifications
   - Planning (Gantt, chemin critique)
   - Revue de projet et jalons
   - Livrables et documentation

2. DÉMARCHE QUALITÉ
   - AMDEC / Analyse des risques
   - Indicateurs de performance
   - Amélioration continue

3. MÉTHODOLOGIE EXPÉRIMENTALE
   - Protocole de mesure
   - Analyse d'incertitudes (Type A, Type B)
   - Validation de modèles

4. OUTILS NUMÉRIQUES
   - Python (NumPy, SciPy, Matplotlib)
   - Simulation et optimisation
   - Traitement de données
"""

BILAN_RELATIONNEL = """
COMPÉTENCES RELATIONNELLES (EC_Compétence relationnelle)
========================================================
1. COMMUNICATION TECHNIQUE
   - Présentation technique en anglais
   - Rédaction de rapports et documentation
   - Schémas et diagrammes techniques

2. TRAVAIL EN ÉQUIPE
   - Répartition des tâches
   - Communication interfilière (mécanique/électricité/info)
   - Gestion de conflits

3. RELATION CLIENT / PARTENAIRE
   - Compréhension du besoin
   - Proposition technique et financière
   - Suivi et reporting

4. ANGLAIS TECHNIQUE
   - Vocabulaire spécifique (smart grids, power electronics, etc.)
   - Présentation orale
   - Lecture de documentation technique
"""

RAPPORT_STRUCTURE = """
STRUCTURE DU RAPPORT D'ACTIVITÉ
===============================
1. Présentation de l'entreprise (1 page)
   - Secteur d'activité, effectifs, organisation

2. Missions confiées (2-3 pages)
   - Description des tâches techniques
   - Contexte et objectifs

3. Démarche et méthodologie (2-3 pages)
   - Outils et méthodes utilisés
   - Difficultés rencontrées et solutions

4. Résultats et livrables (1-2 pages)
   - Travaux réalisés
   - Compétences acquises

5. Bilan personnel (1 page)
   - Apports techniques et humains
   - Perspectives pour la suite du cursus
"""

def main():
    print("=" * 60)
    print("Entreprise S9 - Bilan de Compétences")
    print("3AS9 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print(BILAN_TECHNIQUE)
    print(BILAN_METHODOLOGIQUE)
    print(BILAN_RELATIONNEL)
    print(RAPPORT_STRUCTURE)

    print("\n" + "=" * 60)
    print("GUIDE DE RÉDACTION DU RAPPORT 2A")
    print("=" * 60)
    print("""
Le rapport 2A doit comprendre:
  - 8-10 pages (hors annexes)
  - Une partie technique détaillée
  - Une analyse critique de votre travail
  - Un bilan des compétences acquises
  - Une version anglaise du résumé (abstract)

Échéance: à définir avec votre tuteur pédagogique
    """)

if __name__ == '__main__':
    main()
