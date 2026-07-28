"""Projet: Entreprise S8 - Soutenance 1A
2AS8 - ENSEM NRJ (FISA)
Bilan des compétences et préparation soutenance de stage"""

GUIDE_SOUTENANCE = """
PRÉPARATION SOUTENANCE 1A
=========================
Durée: 15-20 minutes + 10 minutes questions

STRUCTURE RECOMMANDÉE:
---------------------
1. Présentation de l'entreprise (2 min)
   - Secteur d'activité, taille, organisation
   - Contexte du stage

2. Missions confiées (4 min)
   - Description des tâches techniques
   - Objectifs et livrables attendus
   - Périmètre de responsabilité

3. Démarche et méthodologie (5 min)
   - Outils et méthodes utilisés
   - Difficultés rencontrées
   - Solutions apportées

4. Résultats obtenus (3 min)
   - Travaux réalisés (chiffres clés)
   - Compétences mises en œuvre
   - Valeur ajoutée pour l'entreprise

5. Bilan personnel et perspectives (2 min)
   - Apports techniques et humains
   - Lien avec la formation ENSEM
   - Projets futurs (2A, 3A)

CONSEILS:
---------
✓ Préparer un support visuel clair (10-12 slides max)
✓ Soigner la première impression
✓ Anticiper les questions du jury
✓ Prévoir une version anglaise du résumé
"""

GRILLE_EVALUATION = """
GRILLE D'ÉVALUATION SOUTENANCE 1A
==================================
Critère                    | Poids | Note /20
----------------------------|-------|---------
Qualité du fond technique   |  30%  |
Clarté de l'exposé          |  20%  |
Qualité du support          |  15%  |
Capacité de synthèse        |  15%  |
Réponses aux questions      |  10%  |
Anglais (résumé)            |  10%  |
----------------------------|-------|---------
TOTAL                       | 100%  |   /20
"""

BILAN_COMPETENCES = """
BILAN DE COMPÉTENCES - FIN DE 1ÈRE ANNÉE
========================================

COMPÉTENCES TECHNIQUES:
  [ ] Sciences fondamentales (mécanique, thermodynamique, électricité)
  [ ] Programmation et algorithmes
  [ ] Mathématiques pour l'ingénieur
  [ ] Circuits électriques et magnétisme
  [ ] Signaux et systèmes

COMPÉTENCES HUMAINES:
  [ ] Anglais technique
  [ ] Communication professionnelle
  [ ] Gestion de projet
  [ ] Sécurité au travail

COMPÉTENCES ENTREPRISE:
  [ ] Intégration en milieu professionnel
  [ ] Travail en équipe
  [ ] Rédaction de rapports techniques
  [ ] Présentation orale

NIVEAU:
  1 = Débutant
  2 = Intermédiaire
  3 = Autonome
  4 = Avancé
  5 = Expert
"""

RAPPORT_STRUCTURE = """
STRUCTURE DU RAPPORT DE STAGE 1A
================================
Pages recommandées: 15-20 (hors annexes)

1. Résumé (1 page) - français + anglais
2. Introduction (1 page)
   - Contexte et objectifs du stage

3. Présentation de l'entreprise (2-3 pages)
   - Secteur, historique, organisation
   - Place du stage dans l'organigramme

4. Étude bibliographique (2-3 pages)
   - État de l'art sur le sujet traité

5. Travaux réalisés (5-7 pages)
   - Méthodologie et outils
   - Résultats et analyse
   - Difficultés et solutions

6. Discussion (1-2 pages)
   - Limites du travail
   - Pistes d'amélioration

7. Conclusion et perspectives (1 page)

8. Annexes (documents techniques, code, schémas)

FORMAT:
  - Police: 12pt, interligne 1.5
  - Marges: 2.5 cm
  - Reliure: spirale ou thermocollée
"""

def main():
    print("=" * 60)
    print("Entreprise S8 - Soutenance 1A")
    print("2AS8 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- Planification soutenance ---")
    from datetime import datetime, timedelta
    date_soutenance = datetime.now() + timedelta(days=30)
    print(f"Date estimée: {date_soutenance.strftime('%d/%m/%Y')}")
    print(f"Échéances:")
    print(f"  J-30: Finaliser le rapport écrit")
    print(f"  J-21: Envoyer le rapport au tuteur")
    print(f"  J-14: Préparer le support (slides)")
    print(f"  J-7:  Répétition devant un public")
    print(f"  J-1:  Derniers ajustements")

    print(GUIDE_SOUTENANCE)
    print(GRILLE_EVALUATION)
    print(BILAN_COMPETENCES)
    print(RAPPORT_STRUCTURE)

    print("\n" + "=" * 60)
    print("CHECKLIST FINALE")
    print("=" * 60)
    items = [
        "Rapport imprimé (2 exemplaires)",
        "Support de présentation (clé USB + backup cloud)",
        "Tenue professionnelle",
        "Arriver 15 min avant",
        "Prévoir montre pour gérer le temps",
        "Eau et notes discrètes",
        "Résumé anglais préparé",
    ]
    for i, item in enumerate(items, 1):
        print(f"  [{i}] {item}")

if __name__ == '__main__':
    main()
