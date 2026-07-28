"""Projet: Analyse des Risques et Sécurité Fonctionnelle
3AS9 - Spécialisation 9_1 - ENSEM NRJ (FISA)
AMDEC, arbre de défaillances et SIL"""

import numpy as np
import itertools

class AMDEC:
    def __init__(self, systeme="Système de refroidissement"):
        self.systeme = systeme
        self.modes = []

    def ajouter_mode(self, composant, mode, cause, effet, gravite=3, frequence=2, detection=2):
        self.modes.append({
            'composant': composant,
            'mode': mode,
            'cause': cause,
            'effet': effet,
            'gravite': gravite,
            'frequence': frequence,
            'detection': detection
        })

    def calculer_ipp(self):
        for mode in self.modes:
            mode['IPP'] = mode['gravite'] * mode['frequence'] * mode['detection']
        return sorted(self.modes, key=lambda x: x['IPP'], reverse=True)

    def afficher(self):
        print(f"\n=== AMDEC: {self.systeme} ===")
        print(f"{'Composant':<15} {'Mode':<25} {'G':<4} {'F':<4} {'D':<4} {'IPP':<6}")
        print("-" * 60)
        for m in self.calculer_ipp():
            print(f"{m['composant']:<15} {m['mode']:<25} {m['gravite']:<4} {m['frequence']:<4} {m['detection']:<4} {m['IPP']:<6}")

class ArbreDefaillances:
    def __init__(self):
        self.evenements = {}

    def ajouter_base(self, nom, proba):
        self.evenements[nom] = {'type': 'base', 'proba': proba}

    def ajouter_porte(self, nom, type_porte, enfants):
        self.evenements[nom] = {'type': 'porte', 'porte': type_porte, 'enfants': enfants}

    def calculer_proba(self, nom=None):
        if nom is None:
            nom = list(self.evenements.keys())[-1]
        evt = self.evenements[nom]
        if evt['type'] == 'base':
            return evt['proba']
        probs = [self.calculer_proba(e) for e in evt['enfants']]
        if evt['porte'] == 'OU':
            return 1 - np.prod([1 - p for p in probs])
        elif evt['porte'] == 'ET':
            return np.prod(probs)
        return 0

class SIL:
    def __init__(self):
        self.PFD_avg = 0
        self.PFH = 0

    def evaluer(self, taux_defaillance, duree_mission, architecture='1oo1'):
        lambda_du = taux_defaillance
        TI = duree_mission
        if architecture == '1oo1':
            self.PFD_avg = lambda_du * TI / 2
        elif architecture == '1oo2':
            self.PFD_avg = (lambda_du * TI)**2 / 3
        elif architecture == '2oo3':
            self.PFD_avg = (lambda_du * TI)**2
        self.PFH = self.PFD_avg / TI
        return self._niveau_sil()

    def _niveau_sil(self):
        if self.PFD_avg < 1e-4: return 4
        elif self.PFD_avg < 1e-3: return 3
        elif self.PFD_avg < 1e-2: return 2
        elif self.PFD_avg < 1e-1: return 1
        return 0

def main():
    print("=" * 60)
    print("Analyse des Risques et Sécurité Fonctionnelle - 9_1")
    print("=" * 60)
    print("\n--- 1. AMDEC Pompe de refroidissement ---")
    amdec = AMDEC("Circuit primaire")
    amdec.ajouter_mode("Pompe P-01", "Refus démarrage", "Défaut électrique", "Perte débit", 4, 2, 3)
    amdec.ajouter_mode("Pompe P-01", "Cavitation", "NPSH insuffisant", "Dégradation roue", 3, 1, 2)
    amdec.ajouter_mode("Vanne V-03", "Blocage ouvert", "Corrosion", "Débit excessif", 3, 3, 4)
    amdec.ajouter_mode("Capteur T-02", "Dérive mesure", "Vieillissement", "Mauvaise régulation", 4, 3, 1)
    amdec.ajouter_mode("Automate", "Perde programme", "Bug logiciel", "Perte contrôle", 5, 1, 4)
    amdec.afficher()
    print("\n--- 2. Arbre de défaillances ---")
    arbre = ArbreDefaillances()
    arbre.ajouter_base("Défaut pompe", 0.01)
    arbre.ajouter_base("Défaut vanne", 0.005)
    arbre.ajouter_base("Défaut capteur", 0.02)
    arbre.ajouter_base("Défaut automate", 0.001)
    arbre.ajouter_porte("Perte contrôle", "OU", ["Défaut pompe", "Défaut vanne"])
    arbre.ajouter_porte("Perte mesure", "OU", ["Défaut capteur", "Défaut automate"])
    arbre.ajouter_porte("Défaillance système", "ET", ["Perte contrôle", "Perte mesure"])
    proba = arbre.calculer_proba("Défaillance système")
    print(f"Probabilité défaillance système: {proba:.4e}")
    print(f"Disponibilité: {(1-proba)*100:.6f}%")
    print("\n--- 3. Évaluation SIL ---")
    for arch in ['1oo1', '1oo2', '2oo3']:
        sil = SIL()
        niveau = sil.evaluer(1e-5, 8760, arch)
        print(f"Architecture {arch}: PFD_avg={sil.PFD_avg:.2e}, SIL {niveau}")

if __name__ == '__main__':
    main()
