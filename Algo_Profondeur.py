import numpy as np
import time

def AlgoProfondeur(matriceinitiale, matricevoulue, compteur, Ex):
    """
    Algorithme de recherche en profondeur pour résoudre le problème du jeu.
    
    Arguments:
        matriceinitiale (np.ndarray): La matrice représentant l'état initial du jeu.
        matricevoulue (np.ndarray): La matrice représentant l'état souhaité du jeu.
        compteur (int): Le numéro de l'exécution (pour créer le fichier de sortie).
        Ex (int): Le numéro de l'exemple pour créer le dossier de sortie.
    """
    # Définition des variables nécessaires pour l'algorithme
    it = 0 # Compteur pour suivre le nombre d'itérations
    starttime = time.time() # Variable pour suivre le temps d'exécution
    matriceetat = np.copy(matriceinitiale)  # Copie de la matrice initiale pour manipulation
    ListeFrontiere = []  # Liste des états à explorer
    ListeFrontiere.append(matriceetat)  # Ajouter l'état initial à la liste des états à explorer
    Pile = [0]  # Pile pour la recherche en profondeur

    # Création d'un set() avec la matrice initiale sous forme d'octets afin de vérifier si un état a déjà été exploré de facon performante
    vus = set()
    vus.add(matriceinitiale.tobytes())

    # Ouverture en mode écriture ("w") du fichier de sortie des informations avec encodage UTF-8 (pour gérer les accents)
    with open("output_Ex1-" + str(Ex) + "/Algo_Profondeur_" + str(compteur) + ".txt", "w", encoding="utf-8") as output:
        # Implémentation de l'algorithme de recherche en profondeur
        while True:
            # Sécurité pour éviter un crash si aucune solution n'existe
            if it >= len(ListeFrontiere) or len(Pile) == 0:
                # Code pour enregistrer les données dans le fichier de sortie
                # Écriture des informations dans le fichier
                output.write("***AUCUNE SOLTUION TROUVÉE, TOUTS LES ÉTATS ONT ÉTÉ EXPLORÉS***\n")
                output.write("Execution " + str(compteur) + ". \t Taille de la frontière finale : " + str(len(ListeFrontiere)) + ".\n")
                output.write("Nombre d'états explorés : " + str(it) + ".\n")
                output.write("Temps d'exécution : " + str(round(time.time() - starttime, 4)) + " secondes.\n")
                print("Aucune solution trouvée (tous les états ont été explorés).") # Message de confirmation dans la console
                break

            Index = Pile.pop()  # Retirer et récupérer l'index de l'état sur le dessus de la pile

            xinit = np.where(ListeFrontiere[Index] == "*")[0][0]  # Coordonnée x de la case vide dans l'état sur le dessus de la pile
            yinit = np.where(ListeFrontiere[Index] == "*")[1][0]  # Coordonnée y de la case vide dans l'état sur le dessus de la pile

            if np.array_equal(ListeFrontiere[Index], matricevoulue):  # Vérifie si l'état sur le dessus de la pile correspond à l'état souhaité
                # Code pour enregistrer les données dans le fichier de sortie
                # Écriture des informations dans le fichier
                output.write("Execution " + str(compteur) + ". \t Taille de la frontière finale : " + str(len(ListeFrontiere)) + ".\n")
                output.write("Nombre d'états explorés : " + str(it) + ".\n")
                output.write("Temps d'exécution : " + str(round(time.time() - starttime, 4)) + " secondes.\n")
                print("Execution ", compteur, ": Solution trouvée !") # Message de confirmation dans la console
                break  # Sortir de la boucle si la solution est trouvée

            # Écriture de l'état courant dans le fichier de sortie
            output.write("Itération " + str(it) + ". \t Taille de la frontière : " + str(len(ListeFrontiere)) + ".\n")

            # Option 1 = gauche
            if yinit > 0:  # Vérifie si on peut se déplacer vers la gauche
                matriceetat = np.copy(ListeFrontiere[Index])  # Copie de l'état sur le dessus de la pile
                matriceetat[xinit, yinit], matriceetat[xinit, yinit - 1] = matriceetat[xinit, yinit - 1], matriceetat[xinit, yinit]  # Échange des valeurs

                # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été exploré
                cle = matriceetat.tobytes()
                if cle not in vus: # Si l'état n'a pas encore été exploré
                    vus.add(cle)  # On l'ajoute au set
                    ListeFrontiere.append(matriceetat)  # Et à la liste d'origine
                    Pile.append(len(ListeFrontiere) - 1)  # Ajouter l'index de l'état sur le dessus de la pile pour exploration ultérieure

            # Option 2 = droite
            if yinit < 2:  # Vérifie si on peut se déplacer vers la droite
                matriceetat = np.copy(ListeFrontiere[Index])  # Copie de l'état sur le dessus de la pile
                matriceetat[xinit, yinit], matriceetat[xinit, yinit + 1] = matriceetat[xinit, yinit + 1], matriceetat[xinit, yinit]  # Échange des valeurs

                # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été exploré
                cle = matriceetat.tobytes()
                if cle not in vus: # Si l'état n'a pas encore été exploré
                    vus.add(cle)  # On l'ajoute au set
                    ListeFrontiere.append(matriceetat)  # Et à la liste d'origine
                    Pile.append(len(ListeFrontiere) - 1)  # Ajouter l'index de l'état sur le dessus de la pile pour exploration ultérieure

            # Option 3 = haut
            if xinit > 0:  # Vérifie si on peut se déplacer vers le haut
                matriceetat = np.copy(ListeFrontiere[Index])  # Copie de l'état sur le dessus de la pile
                matriceetat[xinit, yinit], matriceetat[xinit - 1, yinit] = matriceetat[xinit - 1, yinit], matriceetat[xinit, yinit]  # Échange des valeurs

                # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été exploré
                cle = matriceetat.tobytes()
                if cle not in vus: # Si l'état n'a pas encore été exploré
                    vus.add(cle)  # On l'ajoute au set
                    ListeFrontiere.append(matriceetat)  # Et à la liste d'origine
                    Pile.append(len(ListeFrontiere) - 1)  # Ajouter l'index de l'état sur le dessus de la pile pour exploration ultérieure

            # Option 4 = bas
            if xinit < 2:  # Vérifie si on peut se déplacer vers le bas
                matriceetat = np.copy(ListeFrontiere[Index])  # Copie de l'état sur le dessus de la pile
                matriceetat[xinit, yinit], matriceetat[xinit + 1, yinit] = matriceetat[xinit + 1, yinit], matriceetat[xinit, yinit]  # Échange des valeurs

                # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été exploré
                cle = matriceetat.tobytes()
                if cle not in vus: # Si l'état n'a pas encore été exploré
                    vus.add(cle)  # On l'ajoute au set
                    ListeFrontiere.append(matriceetat)  # Et à la liste d'origine
                    Pile.append(len(ListeFrontiere) - 1)  # Ajouter l'index de l'état sur le dessus de la pile pour exploration ultérieure

            it += 1  # Incrémenter le compteur d'itérations