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
    ListeFrontiere = []  # Liste des états à explorer
    count1 = 0 # Compteur pour suivre le nombre d'itérations
    time = 0 # Variable pour suivre le temps d'exécution
    matriceetat = np.copy(matriceinitiale)  # Copie de la matrice initiale pour manipulation

    # Implémentation de l'algorithme de recherche en largeur
    