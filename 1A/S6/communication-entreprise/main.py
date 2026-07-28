"""Projet: Communication d'entreprise
1AS6 - ENSEM NRJ (FISA)
Techniques de communication, rapport, presentation, CV, entretien"""

import datetime

class DocumentTechnique:
    def __init__(self, titre, auteur, date=None):
        self.titre = titre
        self.auteur = auteur
        self.date = date or datetime.date.today()
        self.sections = []

    def ajouter_section(self, titre, contenu):
        self.sections.append({'titre': titre, 'contenu': contenu})

    def generer(self):
        print(f"{'=' * 60}")
        print(f"{self.titre}")
        print(f"Auteur: {self.auteur}")
        print(f"Date: {self.date}")
        print(f"{'=' * 60}")
        for s in self.sections:
            print(f"\n{s['titre']}")
            print("-" * len(s['titre']))
            print(s['contenu'])

class PresentationOrale:
    def __init__(self, sujet, duree_min=10):
        self.sujet = sujet
        self.duree = duree_min
        self.diapos = []
        self.notes = []

    def ajouter_diapo(self, titre, contenu):
        self.diapos.append({'titre': titre, 'contenu': contenu})

    def structure(self):
        print(f"\nStructure de presentation: '{self.sujet}' ({self.duree} min)")
        print(f"{'=' * 50}")
        etapes = [
            ("Introduction", "1-2 min: accroche, contexte, plan"),
            ("Contexte/Problematique", "2 min: pourquoi ce sujet est important"),
            ("Developpement", "4-5 min: 3 points cles max, donnees, exemples"),
            ("Conclusion", "1 min: resume, message cle, perspectives"),
            ("Questions", "2 min: anticiper 3-5 questions"),
        ]
        for i, (titre, duree) in enumerate(etapes, 1):
            print(f"  {i}. {titre} ({duree})")

class CVFrancais:
    def __init__(self, nom, prenom, email, telephone):
        self.nom = nom; self.prenom = prenom
        self.email = email; self.tel = telephone
        self.formation = []; self.experience = []
        self.competences = []; self.langues = []

    def ajouter_formation(self, diplome, etablissement, annee):
        self.formation.append(f"{diplome}, {etablissement} ({annee})")

    def ajouter_experience(self, poste, entreprise, duree, description):
        self.experience.append(f"{poste} - {entreprise} ({duree}): {description}")

    def ajouter_competence(self, domaine, niveau):
        self.competences.append(f"{domaine}: {niveau}")

    def generer(self):
        print(f"\n{'=' * 50}")
        print(f"CURRICULUM VITAE")
        print(f"{'=' * 50}")
        print(f"{self.prenom.upper()} {self.nom}")
        print(f"{self.email} | {self.tel}")
        print(f"\nFORMATION:")
        for f in self.formation:
            print(f"  - {f}")
        print(f"\nEXPERIENCE:")
        for e in self.experience:
            print(f"  - {e}")
        print(f"\nCOMPETENCES:")
        for c in self.competences:
            print(f"  - {c}")

class LettreMotivation:
    def __init__(self, destinataire, poste):
        self.dest = destinataire
        self.poste = poste
        self.paragraphes = []

    def ajouter_para(self, texte):
        self.paragraphes.append(texte)

    def generer(self):
        date = datetime.date.today().strftime("%d/%m/%Y")
        print(f"\n{'=' * 50}")
        print(f"LETTRE DE MOTIVATION")
        print(f"{'=' * 50}")
        print(f"\n{date}")
        print(f"\nObjet: Candidature au poste de {self.poste}")
        print(f"\nA l'attention de {self.dest},")
        for p in self.paragraphes:
            print(f"\n{p}")
        print(f"\nCordialement,")

class EntretienSimulation:
    def __init__(self, poste):
        self.poste = poste

    def questions_type(self):
        print(f"\nSimulation d'entretien - Poste: {self.poste}")
        print(f"{'=' * 50}")
        questions = [
            "Parlez-moi de vous.",
            "Pourquoi avez-vous choisi cette formation ?",
            "Quelles sont vos principales qualites ?",
            "Quel est votre plus grand defaut ?",
            "Pourquoi voulez-vous travailler chez nous ?",
            "Parlez-moi d'un projet qui vous a marque.",
            "Ou vous voyez-vous dans 5 ans ?",
            "Avez-vous des questions ?",
        ]
        for i, q in enumerate(questions, 1):
            print(f"  Q{i}: {q}")

def main():
    print("=" * 60)
    print("Communication d'entreprise")
    print("1AS6 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Structure de document technique ---")
    doc = DocumentTechnique("Rapport de stage d'observation", "Etudiant 1A")
    doc.ajouter_section("Introduction", "Ce rapport presente les activites realisees lors du stage...")
    doc.ajouter_section("Presentation entreprise", "L'entreprise est specialisee dans le secteur de l'energie...")
    doc.ajouter_section("Travaux realises", "J'ai participe a la maintenance des installations electriques...")
    doc.ajouter_section("Conclusion", "Ce stage m'a permis de decouvrir le milieu professionnel...")
    doc.generer()

    print("\n\n--- 2. Structure de presentation orale ---")
    pres = PresentationOrale("L'energie solaire photovoltaique", 10)
    pres.structure()
    pres.ajouter_diapo("Introduction", "Contexte energetique actuel")
    pres.ajouter_diapo("Principe PV", "Effet photovoltaique, cellules, panneaux")
    pres.ajouter_diapo("Rendement", "Facteurs influencant le rendement")
    pres.ajouter_diapo("Conclusion", "Perspectives et innovations")
    print(f"\n  Diapos: {len(pres.diapos)}")
    for d in pres.diapos:
        print(f"    - {d['titre']}: {d['contenu']}")

    print("\n--- 3. CV ---")
    cv = CVFrancais("Durand", "Thomas", "thomas.durand@email.com", "06 12 34 56 78")
    cv.ajouter_formation("BAC S", "Lycee Victor Hugo", 2023)
    cv.ajouter_formation("1A ENSEM", "Nancy", 2024)
    cv.ajouter_experience("Stage ouvrier", "EDF", "1 mois", "Maintenance reseau")
    cv.ajouter_competence("Python", "Intermediaire")
    cv.ajouter_competence("Anglais", "B2")
    cv.generer()

    print("\n\n--- 4. Lettre de motivation ---")
    lm = LettreMotivation("Responsable RH", "Ingenieur energie debutant")
    lm.ajouter_para("Actuellement en 1ere annee a l'ENSEM, je suis interesse par le poste...")
    lm.ajouter_para("Au cours de ma formation, j'ai acquis des competences en...")
    lm.ajouter_para("Je suis motive, rigoureux et desireux d'apprendre...")
    lm.generer()

    print("\n\n--- 5. Simulation entretien ---")
    ent = EntretienSimulation("Stage en bureau d'etudes")
    ent.questions_type()

if __name__ == '__main__':
    main()
