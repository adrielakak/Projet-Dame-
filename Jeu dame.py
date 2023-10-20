"""
Ce projet est un jeu de dame qui se joue avec deux joueurs 
avec les règles classiques de ce jeu. Ce programme fonctionne 
avec des classes + méthodes pour respecter le cahier des charges.
"""

# importation des librairies
import pygame
import sys

TAILLE_CASE = 80
LARGEUR_PLATEAU = 8
HAUTEUR_PLATEAU = 8

class Pion:
    def __init__(self, couleur):
        # Initialise un pion avec une couleur et sans être une dame au départ
        self.couleur = couleur
        self.dame = False

    def promouvoir(self):
        # Promouvoir le pion en dame
        self.dame = True

class Plateau:
    def __init__(self):
        # Crée une grille vide de 8x8 pour le plateau
        self.grille = [[None for _ in range(LARGEUR_PLATEAU)] for _ in range(HAUTEUR_PLATEAU)]
        # Initialise les pions sur le plateau
        self.initialiser_pions()
        # Indique si la partie est terminée
        self.partie_terminee = False

    def initialiser_pions(self):
        # Initialise les pions sur le plateau
        for row in range(8):
            for col in range(8):
                # Les pions sont placés sur les cases impaires du plateau
                if (row + col) % 2 == 1:
                    if row < 3:
                        # Les trois premières lignes sont réservées aux pions blancs
                        self.grille[row][col] = Pion("Blanc")
                    elif row > 4:
                        # Les trois dernières lignes sont réservées aux pions noirs
                        self.grille[row][col] = Pion("Noir")

    def deplacer_pion(self, depart, arrivee):
        # Récupère les coordonnées de départ et d'arrivée
        x1, y1 = depart
        x2, y2 = arrivee
        # Récupère le pion à la position de départ
        pion = self.grille[y1][x1]

        # Vérifie si la case de départ est vide
        if not pion:
            # Si la case de départ est vide, retourne False (pas de déplacement)
            return False

        # Vérifie si le déplacement est valide
        if not self.est_deplacement_valide(x1, y1, x2, y2, pion):
            # Si le déplacement n'est pas valide, retourne False
            return False

        # Effectue le déplacement du pion
        self.grille[y2][x2] = pion
        self.grille[y1][x1] = None

        # Si le déplacement est un saut (manger un pion), supprime le pion mangé
        if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
            x_mange = (x1 + x2) // 2
            y_mange = (y1 + y2) // 2
            self.grille[y_mange][x_mange] = None

        # Si le pion atteint le bord opposé, le promouvoir en dame
        if (y2 == 0 and pion.couleur == "Noir") or (y2 == 7 and pion.couleur == "Blanc"):
            pion.promouvoir()

        # Vérifie si la partie est terminée
        pions_blancs, pions_noirs = self.nombre_pions_restants()
        if pions_blancs == 0 or pions_noirs == 0:
            self.partie_terminee = True

        return True

    def est_deplacement_valide(self, x1, y1, x2, y2, pion):
        # Vérifie si le déplacement est valide en fonction du type de pion
        if pion.dame:
            # Si c'est une dame, vérifie si le déplacement est valide pour une dame
            return self.peut_manger(x1, y1, x2, y2, pion.couleur) or \
                   (abs(x2 - x1) == abs(y2 - y1) and self.case_vide(x2, y2) and not self.pion_adverse_entre(x1, y1, x2, y2))
        else:
            direction = 1 if pion.couleur == "Blanc" else -1
            # Bloque le déplacement vers l'arrière pour les pions non dames
            if direction == 1:
                return (abs(x2 - x1) == 1 and abs(y2 - y1) == 1 and self.case_vide(x2, y2)) or \
                       (abs(x2 - x1) == 2 and abs(y2 - y1) == 2 and self.peut_manger(x1, y1, x2, y2, direction))
            else:
                return (abs(x2 - x1) == 1 and y2 - y1 == direction and self.case_vide(x2, y2)) or \
                       (abs(x2 - x1) == 2 and y2 - y1 == 2 * direction and self.peut_manger(x1, y1, x2, y2, direction))

    def case_vide(self, x, y):
        # Vérifie si la case est vide
        return self.grille[y][x] is None

    def pion_adverse_entre(self, x1, y1, x2, y2):
        # Vérifie si un pion adverse se trouve entre deux positions
        x_mange = (x1 + x2) // 2
        y_mange = (y1 + y2) // 2
        return self.grille[y_mange][x_mange] and self.grille[y_mange][x_mange].couleur != self.grille[y1][x1].couleur

    def peut_manger(self, x1, y1, x2, y2, direction):
        # Vérifie si le pion peut manger un pion adverse
        x_mange = (x1 + x2) // 2
        y_mange = (y1 + y2) // 2
        return self.case_vide(x2, y2) and self.pion_adverse_entre(x1, y1, x2, y2) and \
               self.grille[y_mange][x_mange] and self.grille[y_mange][x_mange].couleur != self.grille[y1][x1].couleur

    def nombre_pions_restants(self):
        # Compte le nombre de pions restants pour chaque joueur
        pions_blancs = 0
        pions_noirs = 0

        for row in self.grille:
            for case in row:
                if case and case.couleur == "Blanc":
                    pions_blancs += 1
                elif case and case.couleur == "Noir":
                    pions_noirs += 1

        return pions_blancs, pions_noirs

class JeuDeDames:
    def __init__(self):
        pygame.init()
        # Crée une fenêtre avec les dimensions du plateau
        self.ecran = pygame.display.set_mode((LARGEUR_PLATEAU * TAILLE_CASE, HAUTEUR_PLATEAU * TAILLE_CASE))
        pygame.display.set_caption("Jeu de Dames")
        self.clock = pygame.time.Clock()
        self.plateau = Plateau()
        # Initialise le joueur actuel
        self.joueur_actuel = "Blanc"
        self.selected_pion = None

    def afficher_plateau(self):
        # Affiche le plateau de jeu avec les pions
        self.ecran.fill((0, 0, 0))

        for row in range(8):
            for col in range(8):
                x = col * TAILLE_CASE
                y = row * TAILLE_CASE
                pion = self.plateau.grille[row][col]

                # Dessine les cases du plateau en alternant les couleurs
                if (row + col) % 2 == 0:
                    pygame.draw.rect(self.ecran, (255, 255, 0), (x, y, TAILLE_CASE, TAILLE_CASE))
                else:
                    pygame.draw.rect(self.ecran, (0, 0, 139), (x, y, TAILLE_CASE, TAILLE_CASE))

                if pion:
                    # Dessine les pions en fonction de leur couleur et de leur statut (dame ou non)
                    couleur = (255, 255, 255) if pion.couleur == "Blanc" else (0, 0, 0)
                    pygame.draw.circle(self.ecran, couleur, (x + TAILLE_CASE // 2, y + TAILLE_CASE // 2), TAILLE_CASE // 2 - 5)
                    if pion.dame:
                        pygame.draw.circle(self.ecran, (255, 0, 0), (x + TAILLE_CASE // 2, y + TAILLE_CASE // 2), TAILLE_CASE // 2 - 15)

        pygame.display.flip()

    def gerer_evenements(self):
        # Gère les événements pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quitte le jeu si la fenêtre est fermée
                self.quitter_jeu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Récupère les coordonnées de la souris au clic
                x, y = pygame.mouse.get_pos()
                col, row = x // TAILLE_CASE, y // TAILLE_CASE
                pion = self.plateau.grille[row][col]

                # Sélectionne un pion si la case n'est pas vide et le pion appartient au joueur actuel
                if pion and pion.couleur == self.joueur_actuel:
                    self.selected_pion = (col, row)
            elif event.type == pygame.MOUSEBUTTONUP:
                # Effectue le déplacement au relâchement du clic
                if self.selected_pion:
                    x, y = pygame.mouse.get_pos()
                    col, row = x // TAILLE_CASE, y // TAILLE_CASE
                    arrivee = (col, row)

                    if self.plateau.deplacer_pion(self.selected_pion, arrivee):
                        # Change le joueur actuel si le déplacement est valide
                        self.joueur_actuel = "Noir" if self.joueur_actuel == "Blanc" else "Blanc"

                    self.selected_pion = None

    def boucle_principale(self):
        # Boucle principale du jeu
        while not self.plateau.partie_terminee:
            # Gère les événements, affiche le plateau, limite la vitesse à 60 FPS
            self.gerer_evenements()
            self.afficher_plateau()
            self.clock.tick(60)

        # Affiche le résultat de la partie à la fin
        pions_blancs, pions_noirs = self.plateau.nombre_pions_restants()
        if pions_blancs > pions_noirs:
            print("Partie terminée! L'équipe Blanc a gagné!")
        elif pions_noirs > pions_blancs:
            print("Partie terminée! L'équipe Noir a gagné!")
        else:
            print("Partie terminée! Match nul!")

    def quitter_jeu(self):
        # Quitte le jeu en fermant la fenêtre pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # Crée une instance du jeu et lance la boucle principale
    jeu = JeuDeDames()
    jeu.boucle_principale()

#Create by Adriel 
