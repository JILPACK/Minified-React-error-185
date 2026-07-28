"""Projet: Gestion et Comptabilité financière
2AS8 - ENSEM NRJ (FISA)
Analyse financière, comptabilité d'entreprise, calcul de coûts"""

import numpy as np

class CompteResultat:
    def __init__(self, CA=0):
        self.CA = CA
        self.achats = 0
        self.frais_personnel = 0
        self.autres_charges = 0
        self.dotations = 0
        self.impots = 0

    def ajouter_charge(self, type, montant):
        types = {'achats': 'achats', 'personnel': 'frais_personnel',
                 'autres': 'autres_charges', 'amortissement': 'dotations',
                 'impots': 'impots'}
        if type in types:
            setattr(self, types[type], getattr(self, types[type]) + montant)

    def marge_brute(self):
        return self.CA - self.achats

    def EBITDA(self):
        return self.marge_brute() - self.frais_personnel - self.autres_charges

    def EBIT(self):
        return self.EBITDA() - self.dotations

    def resultat_net(self):
        return self.EBIT() - self.impots

    def afficher(self):
        print(f"\n=== Compte de Résultat ===")
        print(f"Chiffre d'affaires:       {self.CA:>10.0f} €")
        print(f"Achats:                  {self.achats:>10.0f} €")
        print(f"Marge brute:             {self.marge_brute():>10.0f} €")
        print(f"Frais personnel:         {self.frais_personnel:>10.0f} €")
        print(f"Autres charges:          {self.autres_charges:>10.0f} €")
        print(f"EBITDA:                  {self.EBITDA():>10.0f} €")
        print(f"Dotations:               {self.dotations:>10.0f} €")
        print(f"EBIT:                    {self.EBIT():>10.0f} €")
        print(f"Impôts:                  {self.impots:>10.0f} €")
        print(f"Résultat net:            {self.resultat_net():>10.0f} €")

class BilanComptable:
    def __init__(self):
        self.actif_immobilise = 0
        self.actif_circulant = 0
        self.tresorerie = 0
        self.capitaux_propres = 0
        self.dettes_financieres = 0
        self.dettes_fournisseurs = 0

    def total_actif(self):
        return self.actif_immobilise + self.actif_circulant + self.tresorerie

    def total_passif(self):
        return self.capitaux_propres + self.dettes_financieres + self.dettes_fournisseurs

    def fonds_roulement(self):
        return self.capitaux_propres + self.dettes_financieres - self.actif_immobilise

    def besoin_fr(self):
        return self.actif_circulant - self.dettes_fournisseurs

    def trésorerie_nette(self):
        return self.fonds_roulement() - self.besoin_fr()

class AnalyseRatios:
    def __init__(self, cr, bilan):
        self.cr = cr
        self.bilan = bilan

    def rentabilite_nette(self):
        return self.cr.resultat_net() / self.cr.CA if self.cr.CA else 0

    def rentabilite_economique(self):
        return self.cr.EBIT() / self.bilan.total_actif() if self.bilan.total_actif() else 0

    def rentabilite_financiere(self):
        return self.cr.resultat_net() / self.bilan.capitaux_propres if self.bilan.capitaux_propres else 0

    def ratio_endettement(self):
        return self.bilan.dettes_financieres / self.bilan.capitaux_propres if self.bilan.capitaux_propres else 0

    def ratio_liquidite(self):
        return self.bilan.actif_circulant / self.bilan.dettes_fournisseurs if self.bilan.dettes_fournisseurs else 0

    def afficher(self):
        print(f"\n=== Ratios Financiers ===")
        print(f"Rentabilité nette:       {self.rentabilite_nette():.1%}")
        print(f"Rentabilité économique:  {self.rentabilite_economique():.1%}")
        print(f"Rentabilité financière:  {self.rentabilite_financiere():.1%}")
        print(f"Ratio d'endettement:     {self.ratio_endettement():.2f}")
        print(f"Ratio de liquidité:      {self.ratio_liquidite():.2f}")

class CalculCouts:
    def __init__(self):
        self.charges_directes = {}
        self.charges_indirectes = {}
        self.cles_repartition = {}

    def ajouter_charge_directe(self, produit, montant):
        self.charges_directes[produit] = self.charges_directes.get(produit, 0) + montant

    def ajouter_charge_indirecte(self, centre, montant, cle):
        self.charges_indirectes[centre] = montant
        self.cles_repartition[centre] = cle

    def cout_complet(self, produit, assiette):
        cout_direct = self.charges_directes.get(produit, 0)
        cout_indirect = sum(
            montant * assiette.get(cle, 0) / max(sum(assiette.values()), 1)
            for centre, (montant, cle) in zip(
                self.charges_indirectes.keys(),
                [(m, self.cles_repartition[c]) for c, m in self.charges_indirectes.items()]
            )
            if cle in assiette
        )
        return cout_direct + cout_indirect

class AnalyseInvestissement:
    def __init__(self, investissement, flux_annuels, duree, taux=0.08):
        self.I = investissement
        self.F = flux_annuels
        self.n = duree
        self.taux = taux

    def VAN(self):
        van = -self.I
        for t in range(1, self.n + 1):
            van += self.F[t-1] / (1 + self.taux)**t
        return van

    def TRI(self):
        f = lambda r: -self.I + sum(ft / (1+r)**(t+1) for t, ft in enumerate(self.F))
        from scipy.optimize import brentq
        try: return brentq(f, -0.5, 5)
        except: return None

    def delai_recup(self):
        cumul = -self.I
        for t, ft in enumerate(self.F, 1):
            cumul += ft
            if cumul >= 0: return t - 1 + (ft - cumul) / ft
        return None

def main():
    print("=" * 60)
    print("Gestion et Comptabilité financière")
    print("2AS8 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Compte de résultat ---")
    cr = CompteResultat(CA=2500000)
    cr.ajouter_charge('achats', 950000)
    cr.ajouter_charge('personnel', 720000)
    cr.ajouter_charge('autres', 280000)
    cr.ajouter_charge('amortissement', 120000)
    cr.ajouter_charge('impots', 65000)
    cr.afficher()
    print(f"Taux de marge brute: {cr.marge_brute()/cr.CA:.1%}")
    print(f"Taux d'EBITDA: {cr.EBITDA()/cr.CA:.1%}")

    print("\n--- 2. Bilan comptable ---")
    bilan = BilanComptable()
    bilan.actif_immobilise = 1200000
    bilan.actif_circulant = 600000
    bilan.tresorerie = 150000
    bilan.capitaux_propres = 950000
    bilan.dettes_financieres = 500000
    bilan.dettes_fournisseurs = 500000
    print(f"Total actif: {bilan.total_actif():,.0f} €")
    print(f"Total passif: {bilan.total_passif():,.0f} €")
    print(f"Fonds de roulement: {bilan.fonds_roulement():,.0f} €")
    print(f"BFR: {bilan.besoin_fr():,.0f} €")
    print(f"Trésorerie nette: {bilan.trésorerie_nette():,.0f} €")

    print("\n--- 3. Ratios financiers ---")
    ratios = AnalyseRatios(cr, bilan)
    ratios.afficher()

    print("\n--- 4. Calcul de coûts ---")
    couts = CalculCouts()
    couts.ajouter_charge_directe("Produit A", 45000)
    couts.ajouter_charge_directe("Produit B", 32000)
    couts.ajouter_charge_indirecte("Maintenance", 15000, 'heures_machine')
    couts.ajouter_charge_indirecte("Contrôle qualité", 8000, 'nb_lots')
    couts.ajouter_charge_directe("Produit C", 28000)
    ca = CalculCouts()
    print("Coûts directs définis pour 3 produits")

    print("\n--- 5. Analyse d'investissement ---")
    inv = AnalyseInvestissement(500000, [120000, 150000, 180000, 200000, 220000], 5)
    print(f"Investissement: {inv.I:,.0f} €")
    print(f"VAN (taux={inv.taux:.0%}): {inv.VAN():,.0f} €")
    tri = inv.TRI()
    if tri: print(f"TRI: {tri:.1%}")
    print(f"Délai récupération: {inv.delai_recup():.1f} ans")

if __name__ == '__main__':
    main()
