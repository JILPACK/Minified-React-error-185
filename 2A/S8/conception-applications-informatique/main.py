"""Projet: Conception d'applications informatique
2AS8 - ENSEM NRJ (FISA)
Application de simulation et monitoring énergétique avec interface"""

import json
import time
import numpy as np

class GestionnaireDonnees:
    def __init__(self):
        self.donnees = {}
        self.meta = {}

    def creer_serie(self, nom, type='float', unite='', description=''):
        self.donnees[nom] = []
        self.meta[nom] = {'type': type, 'unite': unite, 'description': description}

    def ajouter_point(self, nom, valeur, timestamp=None):
        if nom in self.donnees:
            t = timestamp or time.time()
            self.donnees[nom].append({'t': t, 'v': valeur})
            if len(self.donnees[nom]) > 10000:
                self.donnees[nom].pop(0)

    def exporter_json(self, fichier):
        data = {
            'meta': self.meta,
            'donnees': {k: v[-500:] for k, v in self.donnees.items()}
        }
        with open(fichier, 'w') as f:
            json.dump(data, f, indent=2)
        return len(data['donnees'])

    def statistiques(self, nom):
        if nom not in self.donnees or not self.donnees[nom]:
            return {}
        vals = [p['v'] for p in self.donnees[nom]]
        return {
            'moyenne': np.mean(vals),
            'ecart_type': np.std(vals),
            'min': min(vals),
            'max': max(vals),
            'n_points': len(vals)
        }

class SimulateurBatiment:
    def __init__(self):
        self.T_int = 20.0
        self.T_ext = 10.0
        self.P_chauffage = 0
        self.consommation = 0
        self.gestionnaire = GestionnaireDonnees()
        self._initialiser_capteurs()

    def _initialiser_capteurs(self):
        self.gestionnaire.creer_serie('T_int', unite='°C', description='Température intérieure')
        self.gestionnaire.creer_serie('T_ext', unite='°C', description='Température extérieure')
        self.gestionnaire.creer_serie('P_chauffage', unite='kW', description='Puissance chauffage')
        self.gestionnaire.creer_serie('Conso_journaliere', unite='kWh', description='Consommation cumulée')

    def step(self, dt_h=0.25, T_consigne=20, puissance_max=10):
        UA = 0.2  # Coefficient déperdition [kW/K]
        C = 20    # Capacité thermique [kWh/K]
        delta_T = T_consigne - self.T_int
        besoin = max(0, UA * (self.T_int - self.T_ext))
        if delta_T > 0.5:
            besoin += C * delta_T / dt_h
            besoin = min(besoin, puissance_max)
        self.P_chauffage = besoin
        self.T_int += (-UA * (self.T_int - self.T_ext) + self.P_chauffage) / C * dt_h
        self.consommation += self.P_chauffage * dt_h
        self.gestionnaire.ajouter_point('T_int', self.T_int)
        self.gestionnaire.ajouter_point('T_ext', self.T_ext)
        self.gestionnaire.ajouter_point('P_chauffage', self.P_chauffage)
        return {'T_int': self.T_int, 'P_chauffage': self.P_chauffage, 'conso': self.consommation}

class GestionnaireTaches:
    def __init__(self):
        self.taches = []

    def ajouter(self, nom, priorite=1, duree_h=1):
        self.taches.append({'nom': nom, 'priorite': priorite, 'duree': duree_h, 'statut': 'todo'})

    def executer(self, nom):
        for t in self.taches:
            if t['nom'] == nom and t['statut'] == 'todo':
                t['statut'] = 'en_cours'
                return True
        return False

    def completer(self, nom):
        for t in self.taches:
            if t['nom'] == nom:
                t['statut'] = 'fait'
                return True
        return False

    def rapport(self):
        total = len(self.taches)
        faits = sum(1 for t in self.taches if t['statut'] == 'fait')
        en_cours = sum(1 for t in self.taches if t['statut'] == 'en_cours')
        return f"{faits}/{total} tâches faites ({faits/total*100:.0f}%), {en_cours} en cours"

class APIApplication:
    def __init__(self):
        self.batiment = SimulateurBatiment()
        self.taches = GestionnaireTaches()
        self.utilisateurs = {}

    def enregistrer_utilisateur(self, nom, role='operateur'):
        self.utilisateurs[nom] = {'role': role, 'actif': True}
        print(f"Utilisateur '{nom}' enregistré ({role})")

    def executer_commande(self, cmd, *args):
        if cmd == 'simuler':
            return self.batiment.step(*args)
        elif cmd == 'stats':
            return self.batiment.gestionnaire.statistiques(args[0]) if args else {}
        return None

def main():
    print("=" * 60)
    print("Conception d'applications informatique")
    print("2AS8 - ENSEM NRJ (FISA)")
    print("=" * 60)

    print("\n--- 1. Gestionnaire de données et monitoring ---")
    gd = GestionnaireDonnees()
    gd.creer_serie('Puissance', 'float', 'W', 'Puissance électrique')
    for i in range(100):
        gd.ajouter_point('Puissance', 1500 + 500*np.sin(i/10) + np.random.randn()*50)
    gd.ajouter_point('Puissance', 1200)
    stats = gd.statistiques('Puissance')
    print(f"Statistiques puissance:")
    for k, v in stats.items():
        print(f"  {k}: {v:.2f}")
    n = gd.exporter_json('donnees.json')
    print(f"Exporté {n} séries")

    print("\n--- 2. Application de simulation bâtiment ---")
    sim = SimulateurBatiment()
    sim.T_int = 18
    print(f"{'Heure':<8} {'T_int':<8} {'T_ext':<8} {'P_chauffage':<12} {'Conso':<8}")
    for h in np.arange(6, 24, 0.5):
        sim.T_ext = 5 + 8 * np.sin(np.pi * (h - 8) / 16)
        T_consigne = 15 if (h < 7 or h > 22) else 20
        res = sim.step(0.5, T_consigne)
        if h % 2 == 0:
            print(f"{h:.0f}h    {res['T_int']:<8.1f} {sim.T_ext:<8.1f} {res['P_chauffage']:<12.1f} {res['conso']:<8.1f}")

    print("\n--- 3. Gestionnaire de tâches ---")
    gt = GestionnaireTaches()
    gt.ajouter("Analyse besoins", 3, 4)
    gt.ajouter("Maquette interface", 2, 8)
    gt.ajouter("Dev backend", 1, 20)
    gt.ajouter("Tests", 1, 10)
    print(gt.rapport())
    gt.executer("Analyse besoins")
    gt.completer("Analyse besoins")
    print(gt.rapport())

    print("\n--- 4. Application avec API ---")
    app = APIApplication()
    app.enregistrer_utilisateur("Alice", "ingenieur")
    app.enregistrer_utilisateur("Bob", "operateur")
    res = app.executer_commande('simuler', 0.25, 21, 8)
    print(f"Simulation: T_int={res['T_int']:.1f}°C, P={res['P_chauffage']:.1f}kW")

if __name__ == '__main__':
    main()
