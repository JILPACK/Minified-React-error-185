"""Projet: Expression et communication
1AS5 - ENSEM NRJ (FISA)
Techniques d'expression, methode de travail, compte-rendu, synthese"""

class MethodesTravail:
    @staticmethod
    def methode_APC(objectif, plan=None, controle=None):
        return {
            'Analyser': objectif,
            'Planifier': plan or "Etablir un echeancier",
            'Controler': controle or "Verifier les resultats"
        }

    @staticmethod
    def fiche_lecture(titre, auteur, idee_principale, mots_cles):
        return {'titre': titre, 'auteur': auteur,
                'idee': idee_principale, 'mots_cles': mots_cles}

class CompteRendu:
    def __init__(self, titre, date):
        self.titre = titre
        self.date = date
        self.contenu = []

    def ajouter_observation(self, observation):
        self.contenu.append({'type': 'observation', 'texte': observation})

    def ajouter_resultat(self, resultat):
        self.contenu.append({'type': 'resultat', 'texte': resultat})

    def generer(self):
        print(f"\nCompte rendu: {self.titre}")
        print(f"Date: {self.date}")
        print("-" * 40)
        for elem in self.contenu:
            print(f"  [{elem['type']}] {elem['texte']}")

class Synthese:
    def __init__(self, sujet):
        self.sujet = sujet
        self.arguments = []
        self.conclusion = ""

    def ajouter_argument(self, idee, source):
        self.arguments.append({'idee': idee, 'source': source})

    def rediger(self):
        print(f"\nSYNTHESE: {self.sujet}")
        print("=" * 40)
        for i, arg in enumerate(self.arguments, 1):
            print(f"  Arg {i}: {arg['idee']} ({arg['source']})")
        print(f"\n  Conclusion: {self.conclusion}")

class ExpressionOrale:
    @staticmethod
    def structure_expose(sujet, duree_min):
        return {
            'Introduction': f"1/4 temps: presenter le sujet, annoncer le plan",
            'Developpement': f"1/2 temps: 2-3 parties avec transitions",
            'Conclusion': f"1/4 temps: resumer, ouvrir une perspective",
        }

    @staticmethod
    def conseils():
        return [
            "Parler lentement et distinctement",
            "Regarder le public (pas les notes)",
            "Faire des phrases courtes",
            "Utiliser des supports visuels clairs",
            "Prevoir une introduction et une conclusion",
            "Anticiper les questions",
        ]

def main():
    print("=" * 60)
    print("Expression et communication")
    print("1AS5 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Methodes de travail ---")
    mt = MethodesTravail()
    apc = mt.methode_APC("Reussir le module", "Planning hebdomadaire", "Auto-evaluation")
    for k, v in apc.items():
        print(f"  {k}: {v}")

    fiches = [
        mt.fiche_lecture("L'energie en 2050", "J-C Jancovici",
                         "Transition energetique necessaire", ["energie", "climat", "transition"])
    ]
    for f in fiches:
        print(f"  Fiche: {f['titre']} - {f['idee']}")

    print("\n--- 2. Compte rendu ---")
    cr = CompteRendu("TP Mesures electriques", "15/09/2025")
    cr.ajouter_observation("Circuit monte selon le schema")
    cr.ajouter_resultat("Tension mesuree: 11.9V (theorique 12V)")
    cr.ajouter_resultat("Courant mesure: 245mA")
    cr.ajouter_observation("Ecart de 0.8% entre mesure et theorie")
    cr.generer()

    print("\n--- 3. Synthese de documents ---")
    syn = Synthese("Energies renouvelables")
    syn.ajouter_argument("Le solaire PV progresse de 30%/an", "Rapport AIE 2024")
    syn.ajouter_argument("L'eolien offshore devient competitif", "Etude ADEME")
    syn.ajouter_argument("Le stockage par batteries explose", "BloombergNEF")
    syn.conclusion = "La transition energetique s'accelere, portee par la baisse des couts."
    syn.rediger()

    print("\n--- 4. Expression orale ---")
    eo = ExpressionOrale()
    struct = eo.structure_expose("Mon parcours et mes objectifs", 5)
    for k, v in struct.items():
        print(f"  {k}: {v}")
    print("\n  Conseils pour l'oral:")
    for c in eo.conseils():
        print(f"    - {c}")

    print("\n--- 5. Exercice pratique ---")
    print("  Sujet: Preparez une fiche de synthese sur un theme")
    print("  de votre choix (30 min, 1 page max)")

if __name__ == '__main__':
    main()
