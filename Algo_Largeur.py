import numpy as np

def AlgoLargeur(matriceinitiale, matricevoulue, compteur):
    """
    Algorithme de recherche en largeur pour résoudre le problème du jeu.
    
    Arguments:
        matriceinitiale (np.ndarray): La matrice représentant l'état initial du jeu.
        matricevoulue (np.ndarray): La matrice représentant l'état souhaité du jeu.
        compteur (int): Le numéro de l'exécution (pour créer le fichier de sortie).
    """
    # Définition des variables nécessaires pour l'algorithme
    it = 0 # Compteur pour suivre le nombre d'itérations
    time = 0 # Variable pour suivre le temps d'exécution
    matriceetat = np.copy(matriceinitiale)  # Copie de la matrice initiale pour manipulation
    ListeFrontiere = []  # Liste des états à explorer
    ListeFrontiere.append(matriceetat)  # Ajouter l'état initial à la liste des états à explorer
    xdest = 0 # Coordonnée x de la case de destination de la case vide
    ydest = 0 # Coordonnée y de la case de destination de la case vide
    xinit = np.where(matriceinitiale == "*")[0][0] # Coordonnée x de la case initiale de la case vide
    yinit = np.where(matriceinitiale == "*")[1][0] # Coordonnée y de la case initiale de la case vide

    # Implémentation de l'algorithme de recherche en largeur
    boucle (iterations)
        option1 = haut
            si on est deja en haut, ca va pas plus haut (y=0)
            sinon
                matriceetat[xinit, yinit], matriceetat[xinit, yinit - 1] = matriceetat[xinit, yinit - 1], matriceetat[xinit, yinit]
                Liste.append(matriceetat)
        option2 = bas
            matriceetat = Liste[iterations]
            si on est deja en bas, ca va pas plus bas (y=2)
            sinon
                matriceetat[xinit, yinit], matriceetat[xinit, yinit + 1] = matriceetat[xinit, yinit + 1], matriceetat[xinit, yinit]
                Liste.append(matriceetat)
        option3 = gauche
            matriceetat = Liste[iterations]
            si on est deja full gauche, ca va pas plus loin (x=0)
            sinon
                matriceetat[xinit, yinit], matriceetat[xinit - 1, yinit] = matriceetat[xinit - 1, yinit], matriceetat[xinit, yinit]
                Liste.append(matriceetat)
        option4 = droite
            matriceetat = Liste[iterations]
            si on est deja full droite, ca va pas plus loin (x=2)
            sinon
                matriceetat[xinit, yinit], matriceetat[xinit + 1, yinit] = matriceetat[xinit + 1, yinit], matriceetat[xinit, yinit]
                Liste.append(matriceetat)
    