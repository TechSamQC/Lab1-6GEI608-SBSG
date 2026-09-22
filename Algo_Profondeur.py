import numpy as np  # Importe NumPy pour copier les matrices, repérer le vide et comparer les grilles.
import time  # Importe les outils nécessaires pour mesurer le temps de recherche.
from pathlib import Path  # Importe Path pour construire les chemins et écrire les fichiers de résultats.

def AlgoProfondeur(matriceinitiale, matricevoulue, compteur, dossier_sortie=None):  # Définit la recherche avec le départ, l'objectif, le numéro d'essai et un dossier facultatif.
    """
    Algorithme de recherche en profondeur pour résoudre le problème du jeu.

    Arguments:
        matriceinitiale (np.ndarray): La matrice représentant l'état initial du jeu.
        matricevoulue (np.ndarray): La matrice représentant l'état souhaité du jeu.
        compteur (int): Le numéro de l'exécution, utilisé pour nommer les fichiers.
        dossier_sortie : Le dossier où enregistrer les mesures et le chemin.

    La frontière est une pile : le dernier état ajouté est examiné en premier.
    Les voisins sont ajoutés dans l'ordre gauche, droite, haut, bas.
    Le dernier voisin nouveau et autorisé est donc examiné en premier.
    Les états déjà découverts ne sont pas ajoutés une deuxième fois.

    Retourne les mouvements de la case vide, ou None si aucune solution n'existe.
    La recherche en profondeur ne garantit pas le chemin le plus court.
    """
    # Définition des variables nécessaires pour l'algorithme.
    starttime = time.perf_counter()  # Mémorise l'instant de départ avant l'initialisation de la recherche.
    ListeFrontiere = []  # Crée la pile des matrices qui attendent d'être examinées.
    count1 = 0  # Initialise le nombre d'états examinés, qui sera aussi le nombre d'itérations.
    matriceetat = np.copy(matriceinitiale)  # Copie la matrice initiale pour ne pas modifier celle reçue en argument.
    ListeFrontiere.append(matriceetat)  # Place la matrice initiale au sommet de la pile.
    cle_initiale = matriceetat.tobytes()  # Transforme la matrice initiale en une clé d'octets utilisable dans un ensemble ou un dictionnaire.
    vus = {cle_initiale}  # Mémorise les états déjà découverts afin d'éviter les doublons et les boucles.
    parents = {cle_initiale: None}  # Associe chaque état à son parent ; l'état initial n'a pas de parent.
    actions = {}  # Associera chaque nouvel état au mouvement du vide qui a permis de le découvrir.
    tailles_frontiere = []  # Conservera la taille de la pile avant chaque retrait d'un état.
    cle_solution = None  # Indique qu'aucune solution n'a encore été trouvée.

    # Implémentation de la recherche en profondeur avec une pile.
    while ListeFrontiere:  # Continue tant qu'il reste au moins un état dans la pile.
        tailles_frontiere.append(len(ListeFrontiere))  # Enregistre le nombre d'états en attente avant le traitement de cette itération.
        matricecourante = ListeFrontiere.pop()  # Retire le dernier état ajouté : c'est le principe de la recherche en profondeur.
        cle_courante = matricecourante.tobytes()  # Récupère la clé de l'état courant pour mémoriser les parents de ses voisins.
        count1 += 1  # Compte l'état retiré parmi les états examinés, y compris l'objectif s'il est atteint.

        if np.array_equal(matricecourante, matricevoulue):  # Vérifie si toutes les cases correspondent à la matrice objectif.
            cle_solution = cle_courante  # Retient la clé de l'objectif pour reconstruire le chemin après la recherche.
            break  # Arrête la recherche dès qu'une solution est trouvée.

        xinit = np.where(matricecourante == "*")[0][0]  # Trouve l'indice de la ligne contenant la case vide.
        yinit = np.where(matricecourante == "*")[1][0]  # Trouve l'indice de la colonne contenant la case vide.

        # Option 1 = gauche.
        if yinit > 0:  # Autorise le mouvement à gauche si le vide n'est pas dans la première colonne.
            matriceetat = np.copy(matricecourante)  # Copie l'état courant avant de déplacer le vide vers la gauche.
            matriceetat[xinit, yinit], matriceetat[xinit, yinit - 1] = matriceetat[xinit, yinit - 1], matriceetat[xinit, yinit]  # Échange le vide et la case immédiatement à gauche.
            cle = matriceetat.tobytes()  # Convertit la nouvelle matrice en clé pour vérifier si elle est déjà connue.
            if cle not in vus:  # Vérifie que cet état n'a pas encore été découvert.
                vus.add(cle)  # Marque immédiatement le nouvel état pour éviter de l'ajouter plusieurs fois.
                ListeFrontiere.append(matriceetat)  # Ajoute le nouvel état au sommet de la pile.
                parents[cle] = cle_courante  # Mémorise l'état courant comme parent du nouvel état.
                actions[cle] = "gauche"  # Mémorise le mouvement ayant produit le nouvel état.

        # Option 2 = droite.
        if yinit < 2:  # Autorise le mouvement à droite si le vide n'est pas dans la dernière colonne.
            matriceetat = np.copy(matricecourante)  # Copie l'état courant avant de déplacer le vide vers la droite.
            matriceetat[xinit, yinit], matriceetat[xinit, yinit + 1] = matriceetat[xinit, yinit + 1], matriceetat[xinit, yinit]  # Échange le vide et la case immédiatement à droite.
            cle = matriceetat.tobytes()  # Convertit la nouvelle matrice en clé pour détecter les doublons.
            if cle not in vus:  # Vérifie que cet état n'a pas encore été découvert.
                vus.add(cle)  # Ajoute la clé à l'ensemble des états connus.
                ListeFrontiere.append(matriceetat)  # Place le nouvel état au sommet de la pile.
                parents[cle] = cle_courante  # Associe le nouvel état à son parent.
                actions[cle] = "droite"  # Retient le mouvement du vide vers la droite.

        # Option 3 = haut.
        if xinit > 0:  # Autorise le mouvement vers le haut si le vide n'est pas sur la première ligne.
            matriceetat = np.copy(matricecourante)  # Copie l'état courant avant de déplacer le vide vers le haut.
            matriceetat[xinit, yinit], matriceetat[xinit - 1, yinit] = matriceetat[xinit - 1, yinit], matriceetat[xinit, yinit]  # Échange le vide et la case immédiatement au-dessus.
            cle = matriceetat.tobytes()  # Convertit la nouvelle matrice en clé pour rechercher un éventuel doublon.
            if cle not in vus:  # Vérifie que cet état n'a pas encore été découvert.
                vus.add(cle)  # Marque le nouvel état comme découvert.
                ListeFrontiere.append(matriceetat)  # Ajoute le nouvel état au sommet de la pile.
                parents[cle] = cle_courante  # Retient la clé de l'état qui a produit ce voisin.
                actions[cle] = "haut"  # Retient le mouvement du vide vers le haut.

        # Option 4 = bas.
        if xinit < 2:  # Autorise le mouvement vers le bas si le vide n'est pas sur la dernière ligne.
            matriceetat = np.copy(matricecourante)  # Copie l'état courant avant de déplacer le vide vers le bas.
            matriceetat[xinit, yinit], matriceetat[xinit + 1, yinit] = matriceetat[xinit + 1, yinit], matriceetat[xinit, yinit]  # Échange le vide et la case immédiatement en dessous.
            cle = matriceetat.tobytes()  # Convertit la nouvelle matrice en clé pour vérifier si elle est déjà connue.
            if cle not in vus:  # Vérifie que cet état n'a pas encore été découvert.
                vus.add(cle)  # Ajoute la clé de ce nouvel état aux états connus.
                ListeFrontiere.append(matriceetat)  # Ajoute ce dernier voisin au sommet ; il sera examiné en premier s'il est nouveau.
                parents[cle] = cle_courante  # Enregistre l'état courant comme parent de ce voisin.
                actions[cle] = "bas"  # Enregistre le mouvement du vide vers le bas.

    # Reconstruction du chemin depuis l'objectif jusqu'à l'état initial.
    chemin = None  # Garde None comme résultat lorsqu'aucune solution n'a été trouvée.
    if cle_solution is not None:  # Vérifie que la recherche a atteint l'objectif.
        chemin = []  # Prépare la liste des déplacements à reconstituer.
        cle = cle_solution  # Commence la reconstruction à partir de la clé de l'objectif.
        while parents[cle] is not None:  # Remonte les parents jusqu'à l'état initial, dont le parent vaut None.
            chemin.append(actions[cle])  # Récupère le mouvement ayant permis d'arriver à cet état.
            cle = parents[cle]  # Remonte à l'état précédent du chemin.
        chemin.reverse()  # Remet les mouvements dans l'ordre de l'état initial vers l'objectif.
    

    temps_execution = time.perf_counter() - starttime  # Mesure la recherche et la reconstruction du chemin, comme dans AlgoLargeur.

    # Écriture après le chronométrage : le temps d'accès au disque n'est pas inclus.
    if dossier_sortie is None:  # Vérifie si aucun dossier de résultats n'a été donné en argument.
        dossier_sortie = Path(__file__).resolve().parent / "resultats" / "profondeur"  # Choisit alors le dossier resultats/profondeur situé à côté de ce script.
    dossier_sortie = Path(dossier_sortie)  # Convertit le chemin reçu en objet Path.
    dossier_sortie.mkdir(parents=True, exist_ok=True)  # Crée le dossier de résultats et ses parents si nécessaire.

    fichier_mesures = dossier_sortie / f"execution_{compteur:02d}.txt"  # Nomme le fichier de mesures selon le numéro d'essai, avec deux chiffres.
    temporaire = fichier_mesures.with_suffix(".tmp")  # Prépare un fichier temporaire pour écrire les mesures avant de remplacer le fichier final.
    with temporaire.open("w", encoding="utf-8", newline="\n") as f:  # Ouvre le fichier temporaire et le referme automatiquement après l'écriture.
        for numero, taille in enumerate(tailles_frontiere, start=1):  # Numérote les itérations à partir de 1 et récupère la taille de la pile à chacune.
            f.write(f"{numero}\t{taille}\n")  # Écrit l'itération et la taille de la frontière, séparées par une tabulation.
        f.write(f"{count1}\n")  # Écrit le nombre total d'états examinés sur l'avant-dernière ligne.
        f.write(f"{temps_execution:.9f}\n")  # Écrit le temps d'exécution en secondes sur la dernière ligne.
    temporaire.replace(fichier_mesures)  # Donne au fichier terminé son nom définitif.

    # Enregistrement du chemin dans un fichier distinct de celui des mesures.
    fichier_chemin = dossier_sortie / f"execution_{compteur:02d}_chemin.txt"  # Nomme le fichier qui contiendra tous les mouvements de la solution.
    temporaire = fichier_chemin.with_suffix(".tmp")  # Prépare un fichier temporaire pour le chemin.
    with temporaire.open("w", encoding="utf-8", newline="\n") as f:  # Ouvre le fichier temporaire du chemin en écriture UTF-8.
        if chemin is None:  # Vérifie si l'examen de tous les états accessibles n'a donné aucune solution.
            f.write("Aucune solution trouvee.\n")  # Enregistre l'absence de solution.
        else:  # Traite le cas où une solution a été trouvée.
            f.write(f"Nombre de deplacements : {len(chemin)}\n")  # Enregistre le nombre total de mouvements dans le chemin trouvé.
            f.write("Mouvements de la case vide (*) :\n")  # Précise que les actions décrivent les déplacements de la case vide.
            for numero, action in enumerate(chemin, start=1):  # Parcourt tous les mouvements dans leur ordre d'exécution.
                f.write(f"{numero}\t{action}\n")  # Écrit le numéro du mouvement et l'action correspondante.
    temporaire.replace(fichier_chemin)  # Remplace le fichier de chemin final par celui qui vient d'être entièrement écrit.

    if chemin is None:  # Choisit le message correspondant à une recherche sans solution.
        print("Execution", compteur, ": aucune solution (tous les etats accessibles ont ete examines).")  # Annonce l'absence de solution après exploration complète.
    else:  # Choisit les messages correspondant à une solution trouvée.
        print("Execution", compteur, ": solution trouvee !")  # Annonce la réussite de cet essai.
        print("Nombre de deplacements :", len(chemin))  # Affiche la longueur du chemin, qui n'est pas forcément minimale en profondeur.
        apercu = " -> ".join(chemin[:20]) if chemin else "Deja a l'objectif"  # Prépare les vingt premiers mouvements au maximum pour garder un terminal lisible.
        if len(chemin) > 20:  # Vérifie si le chemin est trop long pour être affiché entièrement dans le terminal.
            apercu += " -> ... (chemin complet dans le fichier)"  # Indique où lire les autres mouvements sans en retirer du fichier enregistré.
        print("Chemin du vide :", apercu)  # Affiche le chemin ou son aperçu lorsqu'il contient plus de vingt mouvements.
    print("Nombre total d'etats examines :", count1)  # Affiche le total des états examinés pendant cet essai.
    print("Temps d'execution :", round(temps_execution, 4), "secondes")  # Affiche la durée de recherche arrondie à quatre décimales.
    print("Mesures :", fichier_mesures)  # Affiche le chemin du fichier contenant les mesures demandées.
    print("Chemin :", fichier_chemin)  # Affiche le chemin du fichier contenant tous les mouvements.
    return chemin  # Renvoie la liste complète des mouvements, ou None si aucune solution n'existe.
