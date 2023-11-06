"""
Ce projet est un jeu de dame qui se joue avec deux joueurs 
avec les règles classiques de ce jeu. Ce programme fonctionne 
avec des classes + méthodes pour respecter le cahier des charges.
"""

import pygame  # Importe la bibliothèque Pygame pour la création de jeux.
import sys  # Importe le module sys pour accéder à certaines fonctionnalités du système.

TAILLE_CASE = 80  # Définit la taille d'une case du plateau.
LARGEUR_PLATEAU = 8  # Définit la largeur du plateau en nombre de cases.
HAUTEUR_PLATEAU = 8  # Définit la hauteur du plateau en nombre de cases.

class Pion:  # Définit une classe pour les pions du jeu de dames.
    def __init__(self, couleur):  # Constructeur de la classe Pion.
        self.couleur = couleur  # Initialise la couleur du pion.
        self.dame = False  # Initialise le statut "dame" du pion à False.

    def promouvoir(self):  # Méthode pour promouvoir un pion en dame.
        self.dame = True  # Change le statut "dame" du pion à True.




class Plateau:  # Définit une classe pour le plateau de jeu.
    def __init__(self):  # Constructeur de la classe Plateau.
        self.grille = [[None for _ in range(LARGEUR_PLATEAU)] for _ in range(HAUTEUR_PLATEAU)]  # Initialise la grille du plateau.
        self.partie_terminee = False  # Initialise le statut de fin de partie à False.
        self.initialiser_pions()  # Appelle la méthode pour initialiser les pions sur le plateau.

    def initialiser_pions(self):  # Méthode pour initialiser les pions sur le plateau.
        for row in range(8):  # Boucle sur les lignes du plateau.
            for col in range(8):  # Boucle sur les colonnes du plateau.
                if (row + col) % 2 == 1:  # Vérifie si la somme de la ligne et de la colonne est impaire (cases où les pions peuvent être placés).
                    if row < 3:  # Si la ligne est inférieure à 3, place un pion blanc.
                        self.grille[row][col] = Pion("Blanc")
                    elif row > 4:  # Si la ligne est supérieure à 4, place un pion noir.
                        self.grille[row][col] = Pion("Noir")

    def deplacer_pion(self, depart, arrivee):  # Méthode pour déplacer un pion sur le plateau.
        x1, y1 = depart  # Récupère les coordonnées de départ.
        x2, y2 = arrivee  # Récupère les coordonnées d'arrivée.
        pion = self.grille[y1][x1]  # Récupère le pion à déplacer.

        # Si aucune pièce n'est présente à la position de départ, retourne False.
        if not pion:
            return False

        # Si le déplacement n'est pas valide, retourne False.
        if not self.est_deplacement_valide(x1, y1, x2, y2, pion):
            return False

        self.grille[y2][x2] = pion  # Place le pion à la nouvelle position.
        self.grille[y1][x1] = None  # Supprime le pion de l'ancienne position.

        # Si le déplacement est un saut (manger une pièce adverse), supprime la pièce adverse entre le départ et l'arrivée.
        if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
            x_mange = (x1 + x2) // 2
            y_mange = (y1 + y2) // 2
            self.grille[y_mange][x_mange] = None

        # Si le pion atteint le bord opposé, le promouvoir en dame.
        if (y2 == 0 and pion.couleur == "Noir") or (y2 == 7 and pion.couleur == "Blanc"):
            pion.promouvoir()

        # Vérifie si la partie est terminée en comptant le nombre de pions restants.
        pions_blancs, pions_noirs = self.nombre_pions_restants()
        if pions_blancs == 0 or pions_noirs == 0:
            self.partie_terminee = True

        return True

    def est_deplacement_valide(self, x1, y1, x2, y2, pion):  # Méthode pour vérifier la validité d'un déplacement.
                # Vérifie la validité du déplacement en fonction du type de pion (dame ou non).
        if pion.dame:
            return self.peut_manger(x1, y1, x2, y2, pion.couleur) or \
                   (abs(x2 - x1) == abs(y2 - y1) and self.case_vide(x2, y2) and self.toutes_cases_libres(x1, y1, x2, y2)) #  or\ permet de continuer sur la même ligne
        else:
            direction = 1 if pion.couleur == "Blanc" else -1
            if direction == 1:
                return (y2 - y1 == direction and abs(x2 - x1) == 1 and self.case_vide(x2, y2)) or \
                       (abs(x2 - x1) == 2 and y2 - y1 == 2 * direction and self.peut_manger(x1, y1, x2, y2, direction))
            else:
                return (y2 - y1 == direction and abs(x2 - x1) == 1 and self.case_vide(x2, y2)) or \
                       (abs(x2 - x1) == 2 and y2 - y1 == 2 * direction and self.peut_manger(x1, y1, x2, y2, direction))

    def case_vide(self, x, y):  # Méthode pour vérifier si une case est vide.
        return self.grille[y][x] is None

    def pion_adverse_entre(self, x1, y1, x2, y2):  # Méthode pour vérifier la présence d'un pion adverse entre deux positions.
        x_mange = (x1 + x2) // 2
        y_mange = (y1 + y2) // 2
        return self.grille[y_mange][x_mange] and self.grille[y_mange][x_mange].couleur != self.grille[y1][x1].couleur

    def peut_manger(self, x1, y1, x2, y2, direction):  # Méthode pour vérifier si un pion peut manger une pièce adverse.
        x_mange = (x1 + x2) // 2
        y_mange = (y1 + y2) // 2
        return self.case_vide(x2, y2) and self.pion_adverse_entre(x1, y1, x2, y2) and \
               self.grille[y_mange][x_mange] and self.grille[y_mange][x_mange].couleur != self.grille[y1][x1].couleur

    def toutes_cases_libres(self, x1, y1, x2, y2):  # Méthode pour vérifier si toutes les cases entre deux positions sont libres.
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        min_y = min(y1, y2)
        max_y = max(y1, y2)

        for x in range(min_x + 1, max_x):
            for y in range(min_y + 1, max_y):
                if not self.case_vide(x, y):
                    return False

        return True

    def nombre_pions_restants(self):  # Méthode pour compter le nombre de pions restants sur le plateau.
        pions_blancs = 0
        pions_noirs = 0

        for row in self.grille:
            for case in row:
                if case and case.couleur == "Blanc":
                    pions_blancs += 1
                elif case and case.couleur == "Noir":
                    pions_noirs += 1

        return pions_blancs, pions_noirs




class JeuDeDames:  # Définit une classe pour le jeu de dames.
    def __init__(self):  # Constructeur de la classe JeuDeDames.
        pygame.init()  # Initialise Pygame.
        self.ecran = pygame.display.set_mode((LARGEUR_PLATEAU * TAILLE_CASE, HAUTEUR_PLATEAU * TAILLE_CASE))  # Crée la fenêtre du jeu.
        pygame.display.set_caption("Jeu de Dames")  # Définit le titre de la fenêtre.
        self.clock = pygame.time.Clock()  # Initialise l'horloge Pygame.
        self.plateau = Plateau()  # Crée un objet plateau.
        self.joueur_actuel = "Blanc"  # Initialise le joueur actuel.
        self.selected_pion = None  # Initialise le pion sélectionné.

    def afficher_plateau(self):  # Méthode pour afficher le plateau de jeu.
        self.ecran.fill((0, 0, 0))  # Remplit l'écran avec une couleur de fond.

        for row in range(8):  # Boucle sur les lignes du plateau.
            for col in range(8):  # Boucle sur les colonnes du plateau.
                x = col * TAILLE_CASE  # Calcule la position x de la case.
                y = row * TAILLE_CASE  # Calcule la position y de la case.
                pion = self.plateau.grille[row][col]  # Récupère le pion à la position actuelle.

                # Dessine la case en fonction de sa couleur.
                if (row + col) % 2 == 0:
                    pygame.draw.rect(self.ecran, (255, 255, 0), (x, y, TAILLE_CASE, TAILLE_CASE))
                else:
                    pygame.draw.rect(self.ecran, (0, 0, 139), (x, y, TAILLE_CASE, TAILLE_CASE))

                # Dessine le pion s'il est présent.
                if pion:
                    couleur = (255, 255, 255) if pion.couleur == "Blanc" else (0, 0, 0)
                    pygame.draw.circle(self.ecran, couleur, (x + TAILLE_CASE // 2, y + TAILLE_CASE // 2), TAILLE_CASE // 2 - 5)
                    # Dessine un cercle rouge à l'intérieur du pion s'il est une dame.
                    if pion.dame:
                        pygame.draw.circle(self.ecran, (255, 0, 0), (x + TAILLE_CASE // 2, y + TAILLE_CASE // 2), TAILLE_CASE // 2 - 15)

        pygame.display.flip()  # Actualise l'affichage.

    def gerer_evenements(self):  # Méthode pour gérer les événements du jeu.
        for event in pygame.event.get():  # Boucle sur les événements Pygame.
            if event.type == pygame.QUIT:  # Si l'événement est de fermer la fenêtre, quitte le jeu.
                self.quitter_jeu()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Si un bouton de la souris est enfoncé.
                x, y = pygame.mouse.get_pos()  # Récupère les coordonnées de la souris.
                col, row = x // TAILLE_CASE, y // TAILLE_CASE  # Convertit les coordonnées en indices de la grille.
                pion = self.plateau.grille[row][col]  # Récupère le pion à la position cliquée.

                # Si un pion du joueur actuel est cliqué, le sélectionne.
                if pion and pion.couleur == self.joueur_actuel:
                    self.selected_pion = (col, row)
            elif event.type == pygame.MOUSEBUTTONUP:  # Si un bouton de la souris est relâché.
                if self.selected_pion:  # Si un pion est sélectionné.
                    x, y = pygame.mouse.get_pos()  # Récupère les coordonnées de la souris.
                    col, row = x // TAILLE_CASE, y // TAILLE_CASE  # Convertit les coordonnées en indices de la grille.
                    arrivee = (col, row)  # Définit la position d'arrivée.

                    # Déplace le pion sélectionné et change le joueur actuel si le déplacement est valide.
                    if self.plateau.deplacer_pion(self.selected_pion, arrivee):
                        self.joueur_actuel = "Noir" if self.joueur_actuel == "Blanc" else "Blanc"

                    self.selected_pion = None  # Réinitialise le pion sélectionné.

    def boucle_principale(self):  # Méthode pour la boucle principale du jeu.
        while not self.plateau.partie_terminee:  # Boucle tant que la partie n'est pas terminée.
            self.gerer_evenements()  # Gère les événements du jeu.
            self.afficher_plateau()  # Affiche le plateau de jeu.
            self.clock.tick(60)  # Limite la fréquence d'actualisation à 60 images par seconde.

        # Affiche le résultat de la partie.
        pions_blancs, pions_noirs = self.plateau.nombre_pions_restants()
        if pions_blancs > pions_noirs:
            print("Partie terminée! L'équipe Blanc a gagné!")
        elif pions_noirs > pions_blancs:
            print("Partie terminée! L'équipe Noir a gagné!")
        else:
            print("Partie terminée! Match nul!")

    def quitter_jeu(self):  # Méthode pour quitter le jeu.
        pygame.quit()  # Quitte Pygame.
        sys.exit()  # Quitte le programme.

if __name__ == "__main__":  # Exécute le jeu si le script est exécuté directement.
    jeu = JeuDeDames()  # Crée un objet JeuDeDames.
    jeu.boucle_principale()  # Lance la boucle principale du jeu.
