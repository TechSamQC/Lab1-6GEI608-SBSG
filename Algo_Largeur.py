import numpy as np
import time

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
    starttime = time.time() # Variable pour suivre le temps d'exécution
    matriceetat = np.copy(matriceinitiale)  # Copie de la matrice initiale pour manipulation
    ListeFrontiere = []  # Liste des états à explorer
    ListeFrontiere.append(matriceetat)  # Ajouter l'état initial à la liste des états à explorer

    # Création d'un set() avec la matrice initiale sous forme d'octets afin de vérifier si un état a déjà été exploré de facon performante
    vus = set()
    vus.add(matriceinitiale.tobytes())

    # Implémentation de l'algorithme de recherche en largeur
    while True:
        # Sécurité pour éviter un crash si aucune solution n'existe
        if it >= len(ListeFrontiere):
            print("Aucune solution trouvée (tous les états ont été explorés).")
            break

        xinit = np.where(ListeFrontiere[it] == "*")[0][0]  # Coordonnée x de la case vide dans l'état courant de cet itération
        yinit = np.where(ListeFrontiere[it] == "*")[1][0]  # Coordonnée y de la case vide dans l'état courant de cet itération

        if np.array_equal(ListeFrontiere[it], matricevoulue):  # Vérifie si l'état courant correspond à l'état souhaité
            # Code pour enregistrer les données dans un fichier de sortie
            # Ouverture en mode écriture ("w") avec encodage UTF-8 (pour gérer les accents)
            with open("Algo_Largeur_" + str(compteur) + ".txt", "w", encoding="utf-8") as fichier:
                # Écriture des informations dans le fichier
                fichier.write("Execution " + str(compteur) + ". \t Taille de la frontière : " + str(len(ListeFrontiere)) + ".\n")
                fichier.write("Nombre d'états explorés : " + str(it) + ".\n")
                fichier.write("Temps d'exécution : " + str(round(time.time() - starttime, 4)) + " secondes.\n")
            print("Execution ", compteur, ": Solution trouvée !") # Message de confirmation dans la console
            break  # Sortir de la boucle si la solution est trouvée

        # Option 1 = gauche
        if yinit > 0:  # Vérifie si on peut se déplacer vers la gauche
            matriceetat = np.copy(ListeFrontiere[it])  # Copie de l'état courant
            matriceetat[xinit, yinit], matriceetat[xinit, yinit - 1] = matriceetat[xinit, yinit - 1], matriceetat[xinit, yinit]  # Échange des valeurs

            # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été exploré
            cle = matriceetat.tobytes()
            if cle not in vus: # Si l'état n'a pas encore été exploré
                vus.add(cle)  # On l'ajoute au set
                ListeFrontiere.append(matriceetat)  # Et à ta liste d'origine

        # Option 2 = droite
        if yinit < 2:  # Vérifie si on peut se déplacer vers la droite
            matriceetat = np.copy(ListeFrontiere[it])  # Copie de l'état courant
            matriceetat[xinit, yinit], matriceetat[xinit, yinit + 1] = matriceetat[xinit, yinit + 1], matriceetat[xinit, yinit]  # Échange des valeurs

            # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été exploré
            cle = matriceetat.tobytes()
            if cle not in vus: # Si l'état n'a pas encore été exploré
                vus.add(cle)  # On l'ajoute au set
                ListeFrontiere.append(matriceetat)  # Et à ta liste d'origine

        # Option 3 = haut
        if xinit > 0:  # Vérifie si on peut se déplacer vers le haut
            matriceetat = np.copy(ListeFrontiere[it])  # Copie de l'état courant
            matriceetat[xinit, yinit], matriceetat[xinit - 1, yinit] = matriceetat[xinit - 1, yinit], matriceetat[xinit, yinit]  # Échange des valeurs

            # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été exploré
            cle = matriceetat.tobytes()
            if cle not in vus: # Si l'état n'a pas encore été exploré
                vus.add(cle)  # On l'ajoute au set
                ListeFrontiere.append(matriceetat)  # Et à ta liste d'origine

        # Option 4 = bas
        if xinit < 2:  # Vérifie si on peut se déplacer vers le bas
            matriceetat = np.copy(ListeFrontiere[it])  # Copie de l'état courant
            matriceetat[xinit, yinit], matriceetat[xinit + 1, yinit] = matriceetat[xinit + 1, yinit], matriceetat[xinit, yinit]  # Échange des valeurs

            # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été exploré
            cle = matriceetat.tobytes()
            if cle not in vus: # Si l'état n'a pas encore été exploré
                vus.add(cle)  # On l'ajoute au set
                ListeFrontiere.append(matriceetat)  # Et à ta liste d'origine

        it += 1  # Incrémenter le compteur d'itérations