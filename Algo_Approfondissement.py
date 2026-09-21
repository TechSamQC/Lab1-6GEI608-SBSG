import numpy as np
import time

def AlgoApprofondissementIteratif(matriceinitiale, matricevoulue, compteur, Ex):
    """
    Algorithme de recherche en approfondissement pour résoudre le problème du jeu.
    
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
    parents = [None] # Liste pour garder l'index du parent de chaque état dans ListeFrontiere. L'état initial (index 0) n'a pas de parent (None)
    Pile = [(0, 0)]  # Pile pour la recherche en approfondissement, avec l'index de l'état et la profondeur de celui-ci

    # Pour l'approfondissement itératif, nous avons besoin d'utiliser une profondeur itérative pour limiter la recherche.
    limit = 0  # Limite de profondeur initiale
    couper = False  # 
    profondeur_max = 31  # Profondeur maximale pour l'approfondissement itératif, si on a pas trouvé de solution en 31 déplacement, il n'y a pas de solution.

    # Modification du set() en dictionnaire avec la matrice initiale et la profondeur minimale de l'état 
    # afin de vérifier si un état a déjà été exploré et si sa profondeur actuelle est inférieure à la profondeur 
    # minimale précédemment enregistrée, de facon performante
    vus = {matriceinitiale.tobytes(): 0} # Format {clé: profondeur_minimale}

    # Ouverture en mode écriture ("w") du fichier de sortie des informations avec encodage UTF-8 (pour gérer les accents)
    with open("output_Ex1-" + str(Ex) + "/Algo_Approfondissement_" + str(compteur) + "_stats.txt", "w", encoding="utf-8") as output:
        # Implémentation de l'algorithme de recherche par approfondissement itératif
        while True:
            if len(Pile) == 0:  # Si la pile est vide, cela signifie que nous avons exploré tous les états possibles à la profondeur actuelle
                limit += 1 # Augmenter la limite de profondeur pour l'approfondissement itératif

                # Vérifier si la limite de profondeur a été dépassée après l'augmentation
                if limit > profondeur_max:
                    # Code pour enregistrer les données dans le fichier de sortie
                    # Écriture des informations dans le fichier
                    output.write("***AUCUNE SOLUTION TROUVÉE***\n")
                    output.write("Execution " + str(compteur) + ". \t Taille de la frontière finale : " + str(len(ListeFrontiere)) + ".\n")
                    output.write("Nombre d'états explorés : " + str(it) + ".\n")
                    output.write("Temps d'exécution : " + str(round(time.time() - starttime, 4)) + " secondes.\n")
                    print("Aucune solution trouvée.") # Message de confirmation dans la console
                    break  # Sortir de la boucle principale après avoir enregistré l'absence de solution
                # Réinitialisation :
                ListeFrontiere = [matriceinitiale.copy()]  # Réinitialiser la liste des états à explorer avec l'état initial
                Pile = [(0, 0)]  # Réinitialiser la pile avec l'état initial et la profondeur 0
                parents = [None] # L'état initial (index 0) n'a pas de parent (None)
                vus = {matriceinitiale.tobytes(): 0}  # Réinitialiser le dictionnaire des états vus avec l'état initial à profondeur 0

            Index, profondeur = Pile.pop()  # Retirer et récupérer l'index et la profondeur de l'état sur le dessus de la pile

            xinit = np.where(ListeFrontiere[Index] == "*")[0][0]  # Coordonnée x de la case vide dans l'état sur le dessus de la pile
            yinit = np.where(ListeFrontiere[Index] == "*")[1][0]  # Coordonnée y de la case vide dans l'état sur le dessus de la pile

            if np.array_equal(ListeFrontiere[Index], matricevoulue):  # Vérifie si l'état sur le dessus de la pile correspond à l'état souhaité
                # Code pour enregistrer les données dans le fichier de sortie
                # Écriture des informations dans le fichier
                output.write("Execution " + str(compteur) + ". \t Taille de la frontière finale : " + str(len(ListeFrontiere)) + ".\n")
                output.write("Nombre d'états explorés : " + str(it) + ".\n")
                output.write("Temps d'exécution : " + str(round(time.time() - starttime, 4)) + " secondes.\n")

                # Code pour enregistrer la solution dans le fichier de sortie
                with open("output_Ex1-" + str(Ex) + "/Algo_Approfondissement_" + str(compteur) + "_chemin_solution.txt", "w", encoding="utf-8") as solution:
                    # Parcourir les parents pour reconstruire le chemin
                    chemin = [] # Liste pour stocker le chemin de la solution
                    index_courant = Index # Index de l'état courant (solution) dans ListeFrontiere
                    while index_courant is not None: # Tant que l'on n'a pas atteint l'état initial (parent None)
                        chemin.append(ListeFrontiere[index_courant]) # Ajouter la matrice de l'état courant à la liste du chemin
                        index_courant = parents[index_courant]  # On remonte vers le parent suivant
                    chemin.reverse()  # Inverser pour avoir le chemin de l'état initial à la solution

                    # Écriture de la taille du chemin de la solution dans le fichier
                    solution.write("Taille du chemin de la solution : " + str(len(chemin)) + ".\n")
                    
                    # Écriture du chemin de la solution dans le fichier
                    solution.write("Chemin de la solution (de l'état initial à l'état souhaité) :\n")
                    for etat in chemin: # Parcourir chaque état dans le chemin
                        # Écrire l'état dans le fichier de solution en transformant l'array en texte, en supprimant les caractères inutiles 
                        # et en ajoutant deux sauts de ligne entre chaque état pour une meilleure lisibilité 
                        solution.write(np.array2string(etat).replace("[", "").replace("]", "").replace(" ", "").replace("''", "\t").replace("'", "") + "\n\n") # Écrire l'état dans le fichier de solution

                print("Execution ", compteur, ": Solution trouvée !") # Message de confirmation dans la console
                break  # Sortir de la boucle si la solution est trouvée

            # Écriture de l'état courant dans le fichier de sortie
            output.write("Itération " + str(it) + ". \t Taille de la frontière : " + str(len(ListeFrontiere)) + ".\n")

            # On ne génère de nouveaux états que si la profondeur actuelle est inférieure à la limite
            if profondeur < limit:  # Vérifie si la profondeur actuelle est inférieure à la limite
                # Option 1 = gauche
                if yinit > 0:  # Vérifie si on peut se déplacer vers la gauche
                    matriceetat = np.copy(ListeFrontiere[Index])  # Copie de l'état sur le dessus de la pile
                    matriceetat[xinit, yinit], matriceetat[xinit, yinit - 1] = matriceetat[xinit, yinit - 1], matriceetat[xinit, yinit]  # Échange des valeurs

                    # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été exploré
                    cle = matriceetat.tobytes()
                    if cle not in vus or (profondeur + 1) < vus[cle]: # Si l'état n'a pas encore été exploré ou si la profondeur actuelle est inférieure à la profondeur minimale précédemment enregistrée
                        vus[cle] = profondeur + 1  # On l'ajoute au dictionnaire avec la profondeur actuelle
                        ListeFrontiere.append(matriceetat)  # Et à la liste d'origine
                        Pile.append((len(ListeFrontiere) - 1, profondeur + 1))  # Ajouter l'index de l'état avec sa profondeur sur le dessus de la pile pour exploration ultérieure
                        parents.append(Index)  # L'état courant (index) est le parent de ce nouvel état

                # Option 2 = droite
                if yinit < 2:  # Vérifie si on peut se déplacer vers la droite
                    matriceetat = np.copy(ListeFrontiere[Index])  # Copie de l'état sur le dessus de la pile
                    matriceetat[xinit, yinit], matriceetat[xinit, yinit + 1] = matriceetat[xinit, yinit + 1], matriceetat[xinit, yinit]  # Échange des valeurs

                    # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été exploré
                    cle = matriceetat.tobytes()
                    if cle not in vus or (profondeur + 1) < vus[cle]: # Si l'état n'a pas encore été exploré ou si la profondeur actuelle est inférieure à la profondeur minimale précédemment enregistrée
                        vus[cle] = profondeur + 1  # On l'ajoute au dictionnaire avec la profondeur actuelle
                        ListeFrontiere.append(matriceetat)  # Et à la liste d'origine
                        Pile.append((len(ListeFrontiere) - 1, profondeur + 1))  # Ajouter l'index de l'état avec sa profondeur sur le dessus de la pile pour exploration ultérieure
                        parents.append(Index)  # L'état courant (index) est le parent de ce nouvel état

                # Option 3 = haut
                if xinit > 0:  # Vérifie si on peut se déplacer vers le haut
                    matriceetat = np.copy(ListeFrontiere[Index])  # Copie de l'état sur le dessus de la pile
                    matriceetat[xinit, yinit], matriceetat[xinit - 1, yinit] = matriceetat[xinit - 1, yinit], matriceetat[xinit, yinit]  # Échange des valeurs

                    # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été exploré
                    cle = matriceetat.tobytes()
                    if cle not in vus or (profondeur + 1) < vus[cle]: # Si l'état n'a pas encore été exploré ou si la profondeur actuelle est inférieure à la profondeur minimale précédemment enregistrée
                        vus[cle] = profondeur + 1  # On l'ajoute au dictionnaire avec la profondeur actuelle
                        ListeFrontiere.append(matriceetat)  # Et à la liste d'origine
                        Pile.append((len(ListeFrontiere) - 1, profondeur + 1))  # Ajouter l'index de l'état avec sa profondeur sur le dessus de la pile pour exploration ultérieure
                        parents.append(Index)  # L'état courant (index) est le parent de ce nouvel état

                # Option 4 = bas
                if xinit < 2:  # Vérifie si on peut se déplacer vers le bas
                    matriceetat = np.copy(ListeFrontiere[Index])  # Copie de l'état sur le dessus de la pile
                    matriceetat[xinit, yinit], matriceetat[xinit + 1, yinit] = matriceetat[xinit + 1, yinit], matriceetat[xinit, yinit]  # Échange des valeurs

                    # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été exploré
                    cle = matriceetat.tobytes()
                    if cle not in vus or (profondeur + 1) < vus[cle]: # Si l'état n'a pas encore été exploré ou si la profondeur actuelle est inférieure à la profondeur minimale précédemment enregistrée
                        vus[cle] = profondeur + 1  # On l'ajoute au dictionnaire avec la profondeur actuelle
                        ListeFrontiere.append(matriceetat)  # Et à la liste d'origine
                        Pile.append((len(ListeFrontiere) - 1, profondeur + 1))  # Ajouter l'index de l'état avec sa profondeur sur le dessus de la pile pour exploration ultérieure
                        parents.append(Index)  # L'état courant (index) est le parent de ce nouvel état

            it += 1  # Incrémenter le compteur d'itérations