"""Projet: Vision et Robotique
3AS9 - ENSEM NRJ (FISA)
Traitement d'images basique et simulation de contrôle robotique"""

import numpy as np

class Image:
    def __init__(self, largeur=640, hauteur=480):
        self.largeur = largeur
        self.hauteur = hauteur
        self.data = np.zeros((hauteur, largeur), dtype=np.uint8)

    def charger_synthetique(self, forme='cercle'):
        yy, xx = np.mgrid[:self.hauteur, :self.largeur]
        cx, cy = self.largeur//2, self.hauteur//2
        if forme == 'cercle':
            mask = (xx - cx)**2 + (yy - cy)**2 < 10000
        elif forme == 'carre':
            mask = (abs(xx - cx) < 100) & (abs(yy - cy) < 100)
        elif forme == 'triangle':
            mask = (yy < cy + 100) & (yy > cy - 100) & (abs(xx - cx) < (100 - abs(yy - cy)/2))
        self.data[mask] = 200
        return self

    def ajouter_bruit(self, niveau=0.1):
        bruit = np.random.randn(*self.data.shape) * 255 * niveau
        self.data = np.clip(self.data + bruit, 0, 255).astype(np.uint8)

    def filtre_moyenneur(self, taille=3):
        from scipy.ndimage import uniform_filter
        return uniform_filter(self.data.astype(float), taille).astype(np.uint8)

    def filtre_sobel(self):
        from scipy.ndimage import sobel
        gx = sobel(self.data.astype(float), axis=1)
        gy = sobel(self.data.astype(float), axis=0)
        return np.sqrt(gx**2 + gy**2).astype(np.uint8)

    def detecter_contours(self, seuil=50):
        edges = self.filtre_sobel()
        return (edges > seuil).astype(np.uint8) * 255

class Robot2D:
    def __init__(self):
        self.x, self.y = 0.0, 0.0
        self.theta = 0.0
        self.v = 0.0
        self.omega = 0.0

    def cmd_vel(self, v, omega):
        self.v = v
        self.omega = omega

    def step(self, dt=0.1):
        self.x += self.v * np.cos(self.theta) * dt
        self.y += self.v * np.sin(self.theta) * dt
        self.theta += self.omega * dt

    def distance_a(self, px, py):
        return np.sqrt((self.x - px)**2 + (self.y - py)**2)

    def angle_vers(self, px, py):
        return np.arctan2(py - self.y, px - self.x)

    def asservissement_position(self, cible_x, cible_y, dt=0.1):
        trajectoire = [(self.x, self.y)]
        while self.distance_a(cible_x, cible_y) > 0.1:
            dist = self.distance_a(cible_x, cible_y)
            angle_cible = self.angle_vers(cible_x, cible_y)
            err_angle = angle_cible - self.theta
            err_angle = np.arctan2(np.sin(err_angle), np.cos(err_angle))
            v = min(2.0, dist)
            omega = 3.0 * err_angle
            self.cmd_vel(v, omega)
            self.step(dt)
            trajectoire.append((self.x, self.y))
        return np.array(trajectoire)

def main():
    print("=" * 60)
    print("Vision et Robotique - Projet 3AS9")
    print("=" * 60)

    print("\n--- 1. Traitement d'images ---")
    img = Image(200, 200)
    img.charger_synthetique('cercle')
    img.ajouter_bruit(0.05)
    print(f"Image créée: {img.hauteur}x{img.largeur}")
    print("Contours détectés:", img.detecter_contours(seuil=30).sum())

    print("\n--- 2. Asservissement robotique ---")
    robot = Robot2D()
    cible = (8.0, 6.0)
    print(f"Robot à ({robot.x:.1f}, {robot.y:.1f}) → cible {cible}")
    traj = robot.asservissement_position(*cible)
    print(f"Trajectoire: {len(traj)} points")
    print(f"Position finale: ({robot.x:.2f}, {robot.y:.2f})")
    print(f"Erreur finale: {robot.distance_a(*cible):.4f}")
    print("Asservissement réussi!")

    print("\n--- 3. Simulation multi-robots ---")
    robots = [Robot2D() for _ in range(3)]
    cibles = [(3,3), (6,1), (9,5)]
    for i, (r, c) in enumerate(zip(robots, cibles)):
        r.asservissement_position(*c)
        print(f"Robot {i+1}: ({r.x:.1f}, {r.y:.1f}) → cible {c} atteinte ✓")

if __name__ == '__main__':
    main()
