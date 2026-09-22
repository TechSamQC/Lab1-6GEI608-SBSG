import numpy as np  # Importe NumPy pour copier les matrices, repérer le vide et comparer les grilles.
import time  # Importe les outils nécessaires pour chronométrer la recherche.
from pathlib import Path  # Importe Path pour créer les dossiers et les fichiers de résultats.

def AlgoLargeur(matriceinitiale, matricevoulue, compteur, dossier_sortie=None):  # Définit la recherche avec une grille de départ, un objectif, un numéro d'essai et un dossier facultatif.
    """
    Algorithme de recherche en largeur pour résoudre le problème du jeu.
    
    Arguments:
        matriceinitiale (np.ndarray): La matrice représentant l'état initial du jeu.
        matricevoulue (np.ndarray): La matrice représentant l'état souhaité du jeu.
        compteur (int): Le numéro de l'exécution (pour créer le fichier de sortie).
        dossier_sortie : Le dossier où enregistrer les mesures et le chemin.

    Retourne la liste des mouvements du vide, ou None s'il n'y a pas de solution.
    """
    # Définition des variables nécessaires pour l'algorithme
    it = 0  # Initialise l'indice du prochain état à examiner ; à la fin, il donnera le total des états examinés.
    starttime = time.perf_counter()  # Mémorise l'instant de départ avec un chronomètre adapté à la mesure des durées.
    matriceetat = np.copy(matriceinitiale)  # Copie la grille initiale pour disposer d'une matrice propre à cette recherche.
    ListeFrontiere = []  # Crée la liste de tous les états découverts, qui conservera aussi les états déjà traités.
    ListeFrontiere.append(matriceetat)  # Place la grille initiale en première position dans la liste.

    # Création d'un set() avec la matrice initiale sous forme d'octets afin de vérifier rapidement si un état a déjà été découvert
    vus = set()  # Crée l'ensemble des clés des états déjà découverts pour détecter rapidement les doublons.
    vus.add(matriceinitiale.tobytes())  # Marque la grille initiale comme découverte en utilisant sa représentation en octets.

    # Même indice que dans ListeFrontiere : parent et action ayant créé l'état.
    ListeParents = [None]  # Associe None à l'état initial puisqu'il ne provient d'aucun état précédent.
    ListeActions = [None]  # Associe None à l'état initial puisqu'aucun déplacement n'a été nécessaire pour le créer.
    tailles_frontiere = []  # Prépare la liste des nombres d'états en attente à chaque itération.
    indice_solution = None  # Indique qu'aucun état objectif n'a encore été trouvé.

    # Implémentation de l'algorithme de recherche en largeur
    while True:  # Répète la recherche jusqu'à l'une des conditions d'arrêt utilisant break.
        # Sécurité pour éviter un crash si aucune solution n'existe
        if it >= len(ListeFrontiere):  # Vérifie si tous les états de la liste ont déjà été examinés.
            break  # Arrête la recherche lorsqu'il ne reste aucun état à examiner.

        # Les états d'indices 0 à it-1 sont déjà traités : ils ne sont plus en attente.
        # Mesure AVANT le traitement de l'état courant.
        tailles_frontiere.append(len(ListeFrontiere) - it)  # Enregistre les états encore en attente, en retirant du total les it états déjà traités.

        if np.array_equal(ListeFrontiere[it], matricevoulue):  # Compare toutes les cases de la grille courante avec celles de la grille objectif.
            indice_solution = it  # Retient la position de la grille objectif pour pouvoir reconstruire son chemin.
            it += 1  # Compte également la grille objectif parmi les états examinés.
            break  # Arrête la recherche dès que l'objectif est atteint.

        xinit = np.where(ListeFrontiere[it] == "*")[0][0]  # Récupère l'indice de la ligne où se trouve la case vide *.
        yinit = np.where(ListeFrontiere[it] == "*")[1][0]  # Récupère l'indice de la colonne où se trouve la case vide *.

        # Option 1 = gauche
        if yinit > 0:  # Autorise le déplacement à gauche si le vide n'est pas dans la première colonne.
            matriceetat = np.copy(ListeFrontiere[it])  # Copie l'état courant pour construire le voisin obtenu par un mouvement à gauche.
            matriceetat[xinit, yinit], matriceetat[xinit, yinit - 1] = matriceetat[xinit, yinit - 1], matriceetat[xinit, yinit]  # Échange le vide avec la case située immédiatement à sa gauche.

            # Transformation de la matrice en octets pour vérifier si l'état a déjà été découvert
            cle = matriceetat.tobytes()  # Convertit cette nouvelle grille en une clé d'octets utilisable dans l'ensemble vus.
            if cle not in vus:  # Vérifie que cette grille n'a encore jamais été découverte pendant cet essai.
                vus.add(cle)  # Marque immédiatement cette grille comme découverte pour éviter de l'ajouter à nouveau.
                ListeFrontiere.append(matriceetat)  # Ajoute le nouvel état en fin de liste pour l'examiner après les états déjà en attente.
                ListeParents.append(it)  # Mémorise l'indice de l'état courant comme parent du nouvel état.
                ListeActions.append("gauche")  # Mémorise que le vide s'est déplacé vers la gauche pour produire cet état.
                

        # Option 2 = droite
        if yinit < 2:  # Autorise le déplacement à droite si le vide n'est pas dans la dernière colonne, d'indice 2.
            matriceetat = np.copy(ListeFrontiere[it])  # Copie l'état courant pour construire le voisin obtenu par un mouvement à droite.
            matriceetat[xinit, yinit], matriceetat[xinit, yinit + 1] = matriceetat[xinit, yinit + 1], matriceetat[xinit, yinit]  # Échange le vide avec la case située immédiatement à sa droite.

            # Transformation de la matrice en octets pour vérifier si l'état a déjà été découvert
            cle = matriceetat.tobytes()  # Convertit cette nouvelle grille en une clé d'octets pour rechercher un éventuel doublon.
            if cle not in vus:  # Vérifie que cette grille n'a pas déjà été découverte.
                vus.add(cle)  # Ajoute la clé de cette grille à l'ensemble des états découverts.
                ListeFrontiere.append(matriceetat)  # Place le nouvel état en fin de liste pour un examen ultérieur.
                ListeParents.append(it)  # Associe au nouvel état l'indice de son parent.
                ListeActions.append("droite")  # Mémorise le déplacement du vide vers la droite ayant produit cet état.

        # Option 3 = haut
        if xinit > 0:  # Autorise le déplacement vers le haut si le vide n'est pas sur la première ligne.
            matriceetat = np.copy(ListeFrontiere[it])  # Copie l'état courant pour construire le voisin obtenu par un mouvement vers le haut.
            matriceetat[xinit, yinit], matriceetat[xinit - 1, yinit] = matriceetat[xinit - 1, yinit], matriceetat[xinit, yinit]  # Échange le vide avec la case située immédiatement au-dessus de lui.

            # Transformation de la matrice en octets pour vérifier si l'état a déjà été découvert
            cle = matriceetat.tobytes()  # Convertit cette nouvelle grille en une clé d'octets pour vérifier si elle est déjà connue.
            if cle not in vus:  # Vérifie que cette grille n'a pas déjà été découverte.
                vus.add(cle)  # Ajoute la clé de cette grille à l'ensemble des états découverts.
                ListeFrontiere.append(matriceetat)  # Ajoute le nouvel état en fin de liste, après les états précédemment découverts.
                ListeParents.append(it)  # Enregistre l'indice du parent qui a permis de produire cet état.
                ListeActions.append("haut")  # Enregistre le déplacement du vide vers le haut.

        # Option 4 = bas
        if xinit < 2:  # Autorise le déplacement vers le bas si le vide n'est pas sur la dernière ligne, d'indice 2.
            matriceetat = np.copy(ListeFrontiere[it])  # Copie l'état courant pour construire le voisin obtenu par un mouvement vers le bas.
            matriceetat[xinit, yinit], matriceetat[xinit + 1, yinit] = matriceetat[xinit + 1, yinit], matriceetat[xinit, yinit]  # Échange le vide avec la case située immédiatement en dessous de lui.

            # Transformation de la matrice en octets pour vérifier si l'état a déjà été découvert
            cle = matriceetat.tobytes()  # Convertit cette nouvelle grille en une clé d'octets pour détecter les doublons.
            if cle not in vus:  # Vérifie que cette grille n'a pas déjà été découverte.
                vus.add(cle)  # Ajoute la clé de cette grille à l'ensemble des états découverts.
                ListeFrontiere.append(matriceetat)  # Ajoute le nouvel état à la fin de la liste des états découverts.
                ListeParents.append(it)  # Retient l'indice de l'état courant comme parent de ce nouvel état.
                ListeActions.append("bas")  # Retient le déplacement du vide vers le bas ayant créé ce nouvel état.

        it += 1  # Passe à l'état suivant dans l'ordre de découverte, ce qui réalise la recherche en largeur.

    # Reconstituer le chemin en remontant les parents depuis l'objectif.
    chemin = None  # Prépare le résultat None, qui sera conservé si aucune solution n'existe.
    if indice_solution is not None:  # Vérifie qu'une grille objectif a bien été trouvée.
        chemin = []  # Crée une liste vide pour recevoir les déplacements de la solution.
        indice = indice_solution  # Commence la reconstruction du chemin à partir de l'état objectif.
        while ListeParents[indice] is not None:  # Remonte les parents jusqu'à l'état initial, dont le parent vaut None.
            chemin.append(ListeActions[indice])  # Récupère le mouvement qui a permis d'arriver à l'état actuellement remonté.
            indice = ListeParents[indice]  # Passe à l'état parent pour continuer à remonter vers le départ.
        chemin.reverse()  # Inverse les actions obtenues pour les remettre dans l'ordre départ vers objectif.

    temps_execution = time.perf_counter() - starttime  # Calcule la durée en secondes de la recherche et de la reconstruction du chemin.

    # Écriture APRÈS le chronométrage : les accès au disque ne sont pas mesurés.
    if dossier_sortie is None:  # Vérifie si aucun dossier de sortie n'a été transmis à la fonction.
        dossier_sortie = Path(__file__).resolve().parent / "resultats" / "largeur"  # Choisit alors resultats/largeur à côté de ce fichier Python.
    dossier_sortie = Path(dossier_sortie)  # Convertit le dossier reçu en objet Path pour faciliter les opérations sur les chemins.
    dossier_sortie.mkdir(parents=True, exist_ok=True)  # Crée le dossier de sortie et ses parents si nécessaire.

    fichier_mesures = dossier_sortie / f"execution_{compteur:02d}.txt"  # Construit le nom du fichier de mesures avec un numéro à deux chiffres, comme execution_01.txt.
    temporaire = fichier_mesures.with_suffix(".tmp")  # Prépare un fichier temporaire dans lequel écrire toutes les mesures avant leur publication finale.
    with temporaire.open("w", encoding="utf-8", newline="\n") as f:  # Ouvre le fichier temporaire en écriture UTF-8 et le referme automatiquement à la fin du bloc.
        for numero, taille in enumerate(tailles_frontiere, start=1):  # Parcourt les tailles enregistrées en numérotant les itérations à partir de 1.
            f.write(f"{numero}\t{taille}\n")  # Écrit le numéro d'itération, une tabulation, la taille de la frontière et un retour à la ligne.
        f.write(f"{it}\n")  # Écrit à l'avant-dernière ligne le total des états examinés, objectif compris s'il est atteint.
        f.write(f"{temps_execution:.9f}\n")  # Écrit à la dernière ligne la durée en secondes avec neuf décimales.
    temporaire.replace(fichier_mesures)  # Installe le fichier terminé à son emplacement final et remplace l'ancien fichier s'il existe.

    # Le chemin va dans un autre fichier pour respecter le format des mesures.
    fichier_chemin = dossier_sortie / f"execution_{compteur:02d}_chemin.txt"  # Construit le nom du fichier séparé qui contiendra les mouvements de la solution.
    temporaire = fichier_chemin.with_suffix(".tmp")  # Prépare un fichier temporaire pour écrire le chemin entièrement avant de le rendre disponible.
    with temporaire.open("w", encoding="utf-8", newline="\n") as f:  # Ouvre ce fichier temporaire en écriture et prévoit sa fermeture automatique.
        if chemin is None:  # Vérifie si la recherche s'est terminée sans trouver de solution.
            f.write("Aucune solution trouvee.\n")  # Enregistre l'absence de solution dans le fichier du chemin.
        else:  # Traite le cas où une solution existe, même si aucun mouvement n'est nécessaire.
            f.write(f"Nombre de deplacements : {len(chemin)}\n")  # Écrit le nombre de mouvements nécessaires pour suivre la solution.
            f.write("Mouvements de la case vide (*) :\n")  # Précise que les actions écrites ensuite sont celles de la case vide *.
            for numero, action in enumerate(chemin, start=1):  # Parcourt les mouvements du chemin dans leur ordre d'exécution en les numérotant à partir de 1.
                f.write(f"{numero}\t{action}\n")  # Écrit le numéro du déplacement et le nom de l'action, séparés par une tabulation.
    temporaire.replace(fichier_chemin)  # Donne au fichier de chemin terminé son nom définitif, en remplaçant l'ancien fichier s'il existe.

    if chemin is None:  # Choisit le message à afficher lorsque la recherche n'a trouvé aucune solution.
        print("Execution", compteur, ": aucune solution (tous les etats accessibles ont ete examines).")  # Annonce l'échec après l'examen de tous les états accessibles depuis la grille initiale.
    else:  # Choisit les affichages correspondant à une solution trouvée.
        print("Execution", compteur, ": solution trouvee !")  # Annonce la réussite et indique le numéro de l'essai.
        print("Nombre de deplacements :", len(chemin))  # Affiche la longueur du chemin, c'est-à-dire le nombre de déplacements à effectuer.
        print("Chemin du vide :", " -> ".join(chemin) if chemin else "Deja a l'objectif")  # Affiche les actions dans l'ordre, ou précise que la grille était déjà à l'objectif.
    print("Nombre total d'etats examines :", it)  # Affiche le nombre total d'états examinés pendant cet essai.
    print("Temps d'execution :", round(temps_execution, 4), "secondes")  # Affiche le temps en secondes arrondi à quatre décimales pour faciliter sa lecture.
    print("Mesures :", fichier_mesures)  # Indique l'emplacement du fichier contenant les mesures demandées.
    print("Chemin :", fichier_chemin)  # Indique l'emplacement du fichier contenant les actions à suivre.
    return chemin  # Renvoie la liste des actions trouvées, ou None si aucune solution n'existe.
