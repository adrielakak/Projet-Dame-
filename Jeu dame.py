# importation des librairies
import pygame
import sys

#définition de la taille du damier

TAILLE_CASE = 80
LARGEUR_PLATEAU = 8
HAUTEUR_PLATEAU = 8

#création de la classe pion contenant la méthode promouvoir

class Pion:
    def __init__(self, couleur):
        self.couleur = couleur
        self.dame = False

    def promouvoir(self):
        self.dame = True

#Création de la classe plateau contenant la méthode [initialiser_pions; deplacer_pion; est_deplacement_valide; nombre_pions_restants]

class Plateau:
    def __init__(self):
        # Crée une grille vide de 8x8 pour le plateau
        self.grille = [[None for _ in range(LARGEUR_PLATEAU)] for _ in range(HAUTEUR_PLATEAU)]
        self.initialiser_pions()
        self.partie_terminee = False

    def initialiser_pions(self):
        # Initialise les pions sur le plateau
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.grille[row][col] = Pion("Blanc")
                    elif row > 4:
                        self.grille[row][col] = Pion("Noir")

    def deplacer_pion(self, depart, arrivee):
        x1, y1 = depart
        x2, y2 = arrivee
        pion = self.grille[y1][x1]

        if not pion:
            return False

        if not self.est_deplacement_valide(x1, y1, x2, y2, pion):
            return False

        # Effectue le déplacement du pion
        self.grille[y2][x2] = pion
        self.grille[y1][x1] = None

        if (y2 == 0 and pion.couleur == "Noir") or (y2 == 7 and pion.couleur == "Blanc"):
            pion.promouvoir()

        pions_blancs, pions_noirs = self.nombre_pions_restants()
        if pions_blancs == 0 or pions_noirs == 0:
            self.partie_terminee = True

        return True

    def est_deplacement_valide(self, x1, y1, x2, y2, pion):
        if pion.dame:
            # Les dames peuvent se déplacer en diagonale dans toutes les directions
            return abs(x2 - x1) == abs(y2 - y1)
        else:
            # Les pions ne peuvent se déplacer qu'en avant en diagonale d'une case
            if pion.couleur == "Blanc":
                return (abs(x2 - x1) == 1 and abs(y2 - y1) == 1 and y2 > y1)
            else:
                return (abs(x2 - x1) == 1 and abs(y2 - y1) == 1 and y2 < y1)

    def nombre_pions_restants(self):
        pions_blancs = 0
        pions_noirs = 0

        for row in self.grille:
            for case in row:
                if case and case.couleur == "Blanc":
                    pions_blancs += 1
                elif case and case.couleur == "Noir":
                    pions_noirs += 1

        return pions_blancs, pions_noirs

#Création de la classe JeuDeDames contenant les méthodes [afficher_plateau; gerer_evenements; boucle_principale; quitter_jeu]
class JeuDeDames:
    def __init__(self):
        pygame.init()
        self.ecran = pygame.display.set_mode((LARGEUR_PLATEAU * TAILLE_CASE, HAUTEUR_PLATEAU * TAILLE_CASE))
        pygame.display.set_caption("Jeu de Dames")
        self.clock = pygame.time.Clock()
        self.plateau = Plateau()
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

                if (row + col) % 2 == 0:
                    pygame.draw.rect(self.ecran, (255, 255, 0), (x, y, TAILLE_CASE, TAILLE_CASE))
                else:
                    pygame.draw.rect(self.ecran, (0, 0, 139), (x, y, TAILLE_CASE, TAILLE_CASE))

                if pion:
                    couleur = (255, 255, 255) if pion.couleur == "Blanc" else (0, 0, 0)
                    pygame.draw.circle(self.ecran, couleur, (x + TAILLE_CASE // 2, y + TAILLE_CASE // 2), TAILLE_CASE // 2 - 5)
                    if pion.dame:
                        pygame.draw.circle(self.ecran, (255, 0, 0), (x + TAILLE_CASE // 2, y + TAILLE_CASE // 2), TAILLE_CASE // 2 - 15)

        pygame.display.flip()

    def gerer_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quitter_jeu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = x // TAILLE_CASE, y // TAILLE_CASE
                pion = self.plateau.grille[row][col]

                if pion and pion.couleur == self.joueur_actuel:
                    self.selected_pion = (col, row)
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.selected_pion:
                    x, y = pygame.mouse.get_pos()
                    col, row = x // TAILLE_CASE, y // TAILLE_CASE
                    arrivee = (col, row)

                    if self.plateau.deplacer_pion(self.selected_pion, arrivee):
                        self.joueur_actuel = "Noir" if self.joueur_actuel == "Blanc" else "Blanc"

                    self.selected_pion = None

    def boucle_principale(self):
        while not self.plateau.partie_terminee:
            self.gerer_evenements()
            self.afficher_plateau()
            self.clock.tick(60)

        pions_blancs, pions_noirs = self.plateau.nombre_pions_restants()
        if pions_blancs > pions_noirs:
            print("Partie terminée! L'équipe Blanc a gagné!")
        elif pions_noirs > pions_blancs:
            print("Partie terminée! L'équipe Noir a gagné!")
        else:
            print("Partie terminée! Match nul!")

    def quitter_jeu(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    jeu = JeuDeDames()
    jeu.boucle_principale()

#Create by Adriel 
