import numpy as np  # Importe NumPy pour copier les grilles, comparer les états et repérer la case vide.
import time  # Importe le chronomètre utilisé pour mesurer la durée de la recherche.
from pathlib import Path  # Importe Path pour créer les dossiers et écrire les fichiers de résultats.

def AlgoApprofondissement(matriceinitiale, matricevoulue, compteur, dossier_sortie=None):  # Définit la recherche avec le départ, l'objectif, le numéro d'essai et un dossier facultatif.
    """
    Recherche en profondeur à approfondissement itératif pour le 8-puzzle.

    Arguments:
        matriceinitiale (np.ndarray): La grille de départ, avec * pour le vide.
        matricevoulue (np.ndarray): La grille objectif.
        compteur (int): Le numéro de l'exécution, utilisé pour nommer les fichiers.
        dossier_sortie : Le dossier où écrire les mesures et le chemin.

   
    """
    starttime = time.perf_counter()  # Démarre le chronomètre avant l'initialisation de la recherche.
    limite = 0  # Commence par vérifier uniquement l'état initial, sans autoriser de déplacement.
    count1 = 0  # Compte tous les états retirés de la pile, en cumulant les différents passages.
    tailles_frontiere = []  # Conserve les tailles de frontière de tous les passages dans l'ordre chronologique.
    nombre_precedent = 0  # Mémorise le nombre d'états distincts du passage précédent pour détecter l'épuisement de l'espace.
    cle_initiale = matriceinitiale.tobytes()  # Construit la clé de l'état initial pour les dictionnaires.
    cle_solution = None  # Indique qu'aucun état objectif n'a encore été trouvé.

    while True:  # Répète les recherches limitées jusqu'à trouver une solution ou épuiser les états accessibles.
        ListeFrontiere = [(np.copy(matriceinitiale), 0)]  # Repart de la grille initiale et mémorise aussi sa profondeur, égale à zéro.
        profondeurs = {cle_initiale: 0}  # Remet à zéro les meilleurs nombres de mouvements connus pour ce nouveau passage.
        parents = {cle_initiale: None}  # Réinitialise les parents ; l'état initial n'a pas de prédécesseur.
        actions = {}  # Réinitialise les mouvements utilisés pour atteindre les états pendant ce passage.

        while ListeFrontiere:  # Poursuit la recherche limitée tant que la pile contient des états.
            tailles_frontiere.append(len(ListeFrontiere))  # Note le nombre d'entrées en attente avant le retrait courant.
            matricecourante, profondeur = ListeFrontiere.pop()  # Retire le dernier état ajouté avec le nombre de mouvements utilisés pour l'atteindre.
            cle_courante = matricecourante.tobytes()  # Construit la clé de l'état courant pour consulter les informations mémorisées.
            count1 += 1  # Compte ce retrait dans le total de l'exécution, sans remettre le compteur à zéro entre les limites.

            if profondeur > profondeurs[cle_courante]:  # Vérifie si cette entrée est devenue moins intéressante qu'un chemin plus court déjà découvert.
                continue  # Écarte cette ancienne entrée ; l'entrée plus courte pourra explorer au moins les mêmes suites de mouvements.
            if np.array_equal(matricecourante, matricevoulue):  # Compare la grille courante à l'objectif, même lorsque la limite est atteinte.
                cle_solution = cle_courante  # Mémorise l'objectif pour pouvoir reconstruire son chemin.
                break  # Arrête la recherche limitée dès que l'objectif est trouvé.
            if profondeur == limite:  # Vérifie si le nombre maximal de mouvements de ce passage est atteint.
                continue  # N'ajoute aucun voisin qui dépasserait cette limite de profondeur.

            xinit = np.where(matricecourante == "*")[0][0]  # Repère la ligne contenant la case vide.
            yinit = np.where(matricecourante == "*")[1][0]  # Repère la colonne contenant la case vide.
            nouvelle_profondeur = profondeur + 1  # Calcule le nombre de mouvements nécessaire pour atteindre un voisin de l'état courant.

            # Option 1 = gauche.
            if yinit > 0:  # Autorise le mouvement à gauche si le vide n'est pas dans la première colonne.
                matriceetat = np.copy(matricecourante)  # Copie la grille courante avant de construire le voisin de gauche.
                matriceetat[xinit, yinit], matriceetat[xinit, yinit - 1] = matriceetat[xinit, yinit - 1], matriceetat[xinit, yinit]  # Échange le vide et la case située à sa gauche.
                cle = matriceetat.tobytes()  # Construit la clé du nouvel état.
                if cle not in profondeurs or nouvelle_profondeur < profondeurs[cle]:  # Accepte un état nouveau ou un accès plus court à un état déjà rencontré.
                    profondeurs[cle] = nouvelle_profondeur  # Retient le meilleur nombre de mouvements connu pour cet état pendant ce passage.
                    ListeFrontiere.append((matriceetat, nouvelle_profondeur))  # Ajoute le voisin et sa profondeur au sommet de la pile.
                    parents[cle] = cle_courante  # Mémorise l'état courant comme parent du voisin.
                    actions[cle] = "gauche"  # Mémorise le mouvement ayant produit ce voisin.

            # Option 2 = droite.
            if yinit < 2:  # Autorise le mouvement à droite si le vide n'est pas dans la dernière colonne.
                matriceetat = np.copy(matricecourante)  # Copie la grille courante avant de construire le voisin de droite.
                matriceetat[xinit, yinit], matriceetat[xinit, yinit + 1] = matriceetat[xinit, yinit + 1], matriceetat[xinit, yinit]  # Échange le vide et la case située à sa droite.
                cle = matriceetat.tobytes()  # Construit la clé de ce voisin pour consulter sa meilleure profondeur connue.
                if cle not in profondeurs or nouvelle_profondeur < profondeurs[cle]:  # Accepte ce voisin s'il est nouveau ou atteint avec moins de mouvements.
                    profondeurs[cle] = nouvelle_profondeur  # Enregistre la profondeur améliorée de cet état.
                    ListeFrontiere.append((matriceetat, nouvelle_profondeur))  # Place la grille et sa profondeur au sommet de la pile.
                    parents[cle] = cle_courante  # Enregistre le parent associé au chemin retenu.
                    actions[cle] = "droite"  # Enregistre le mouvement du vide vers la droite.

            # Option 3 = haut.
            if xinit > 0:  # Autorise le mouvement vers le haut si le vide n'est pas sur la première ligne.
                matriceetat = np.copy(matricecourante)  # Copie la grille courante avant de construire le voisin du haut.
                matriceetat[xinit, yinit], matriceetat[xinit - 1, yinit] = matriceetat[xinit - 1, yinit], matriceetat[xinit, yinit]  # Échange le vide et la case située au-dessus.
                cle = matriceetat.tobytes()  # Construit la clé de ce voisin.
                if cle not in profondeurs or nouvelle_profondeur < profondeurs[cle]:  # Autorise la découverte d'un état ou sa reprise depuis un chemin plus court.
                    profondeurs[cle] = nouvelle_profondeur  # Retient le meilleur nombre de mouvements pour cet état.
                    ListeFrontiere.append((matriceetat, nouvelle_profondeur))  # Ajoute la grille et sa profondeur à la pile.
                    parents[cle] = cle_courante  # Retient l'état courant comme parent du voisin.
                    actions[cle] = "haut"  # Retient le déplacement du vide vers le haut.

            # Option 4 = bas.
            if xinit < 2:  # Autorise le mouvement vers le bas si le vide n'est pas sur la dernière ligne.
                matriceetat = np.copy(matricecourante)  # Copie la grille courante avant de construire le voisin du bas.
                matriceetat[xinit, yinit], matriceetat[xinit + 1, yinit] = matriceetat[xinit + 1, yinit], matriceetat[xinit, yinit]  # Échange le vide et la case située en dessous.
                cle = matriceetat.tobytes()  # Construit la clé de ce voisin pour détecter les accès déjà connus.
                if cle not in profondeurs or nouvelle_profondeur < profondeurs[cle]:  # Accepte le voisin seulement s'il est nouveau ou si son chemin est plus court.
                    profondeurs[cle] = nouvelle_profondeur  # Mémorise la meilleure profondeur connue pour ce voisin.
                    ListeFrontiere.append((matriceetat, nouvelle_profondeur))  # Ajoute ce dernier voisin au sommet pour l'examiner en priorité s'il est accepté.
                    parents[cle] = cle_courante  # Mémorise l'état qui a permis d'atteindre ce voisin.
                    actions[cle] = "bas"  # Mémorise le mouvement du vide vers le bas.

        if cle_solution is not None:  # Vérifie si la recherche limitée vient de trouver l'objectif.
            break  # Termine l'approfondissement : aucune limite plus grande n'est nécessaire.
        if len(profondeurs) == nombre_precedent:  # Vérifie si augmenter la limite n'a découvert aucun état distinct supplémentaire.
            break  # Conclut à l'absence de solution puisque tous les états accessibles ont été couverts.
        nombre_precedent = len(profondeurs)  # Retient le nombre d'états distincts du passage qui vient de se terminer.
        limite += 1  # Autorise un mouvement supplémentaire pour la prochaine recherche repartant du début.

    # Reconstruction du chemin après la dernière recherche limitée.
    chemin = None  # Conserve None si tous les états accessibles ont été parcourus sans atteindre l'objectif.
    if cle_solution is not None:  # Vérifie qu'une solution a été trouvée.
        chemin = []  # Prépare la liste des mouvements de la solution.
        cle = cle_solution  # Commence la reconstruction à partir de l'objectif.
        while parents[cle] is not None:  # Remonte les parents jusqu'à la grille initiale.
            chemin.append(actions[cle])  # Récupère le mouvement ayant permis d'atteindre l'état actuellement remonté.
            cle = parents[cle]  # Passe à l'état parent pour poursuivre la reconstruction.
        chemin.reverse()  # Replace les mouvements dans l'ordre allant du départ vers l'objectif.

    temps_execution = time.perf_counter() - starttime  # Mesure l'ensemble des passages et la reconstruction avant les écritures sur disque.

    # Enregistrement des mesures au même format que pour les deux autres recherches.
    if dossier_sortie is None:  # Vérifie si aucun dossier de sortie n'a été précisé.
        dossier_sortie = Path(__file__).resolve().parent / "resultats" / "approfondissement"  # Choisit le dossier de cet algorithme situé à côté du script.
    dossier_sortie = Path(dossier_sortie)  # Convertit le chemin en objet Path pour gérer les fichiers.
    dossier_sortie.mkdir(parents=True, exist_ok=True)  # Crée le dossier de résultats et ses parents si nécessaire.

    fichier_mesures = dossier_sortie / f"execution_{compteur:02d}.txt"  # Nomme le fichier de mesures selon le numéro d'essai, écrit sur deux chiffres.
    temporaire = fichier_mesures.with_suffix(".tmp")  # Prépare un fichier temporaire avant l'installation du résultat final.
    with temporaire.open("w", encoding="utf-8", newline="\n") as f:  # Ouvre le fichier temporaire et le referme automatiquement après l'écriture.
        for numero, taille in enumerate(tailles_frontiere, start=1):  # Numérote toutes les itérations sans recommencer à 1 lorsque la limite augmente.
            f.write(f"{numero}\t{taille}\n")  # Écrit l'itération et la taille de la frontière séparées par une tabulation.
        f.write(f"{count1}\n")  # Écrit à l'avant-dernière ligne le total des examens, répétitions comprises.
        f.write(f"{temps_execution:.9f}\n")  # Écrit à la dernière ligne le temps en secondes avec neuf décimales.
    temporaire.replace(fichier_mesures)  # Donne au fichier terminé son nom définitif.

    fichier_chemin = dossier_sortie / f"execution_{compteur:02d}_chemin.txt"  # Nomme le fichier séparé contenant le chemin de la solution.
    temporaire = fichier_chemin.with_suffix(".tmp")  # Prépare un fichier temporaire pour le chemin.
    with temporaire.open("w", encoding="utf-8", newline="\n") as f:  # Ouvre le fichier temporaire du chemin en écriture UTF-8.
        if chemin is None:  # Vérifie si aucune solution n'a été trouvée.
            f.write("Aucune solution trouvee.\n")  # Enregistre le résultat sans solution.
        else:  # Traite le cas où une solution a été trouvée.
            f.write(f"Nombre de deplacements : {len(chemin)}\n")  # Enregistre la longueur du chemin trouvé.
            f.write("Mouvements de la case vide (*) :\n")  # Précise que les actions décrivent les déplacements de la case vide.
            for numero, action in enumerate(chemin, start=1):  # Parcourt tous les mouvements dans l'ordre de leur exécution.
                f.write(f"{numero}\t{action}\n")  # Écrit le numéro du mouvement et son nom, séparés par une tabulation.
    temporaire.replace(fichier_chemin)  # Installe le fichier de chemin terminé à son emplacement final.

    if chemin is None:  # Choisit le message correspondant à l'absence de solution.
        print("Execution", compteur, ": aucune solution (tous les etats accessibles ont ete examines).")  # Annonce l'absence de chemin après épuisement de l'espace accessible.
    else:  # Choisit les messages correspondant à une solution trouvée.
        print("Execution", compteur, ": solution trouvee !")  # Annonce la réussite de cette exécution.
        print("Nombre de deplacements :", len(chemin))  # Affiche la longueur minimale du chemin trouvé par approfondissement itératif.
        apercu = " -> ".join(chemin[:20]) if chemin else "Deja a l'objectif"  # Prépare au plus vingt mouvements pour garder l'affichage lisible.
        if len(chemin) > 20:  # Vérifie si certains mouvements ne sont pas présents dans l'aperçu.
            apercu += " -> ... (chemin complet dans le fichier)"  # Indique que tous les mouvements figurent dans le fichier du chemin.
        print("Chemin du vide :", apercu)  # Affiche le chemin ou ses vingt premiers mouvements.
    print("Derniere limite de profondeur :", limite)  # Indique la dernière limite utilisée avant de trouver la solution ou de conclure à son absence.
    print("Nombre total d'etats examines (repetitions comprises) :", count1)  # Affiche le total des examens de tous les passages, qui peut dépasser le nombre d'états distincts.
    print("Temps d'execution :", round(temps_execution, 4), "secondes")  # Affiche la durée totale de recherche arrondie à quatre décimales.
    print("Mesures :", fichier_mesures)  # Indique où trouver le fichier contenant les mesures demandées.
    print("Chemin :", fichier_chemin)  # Indique où trouver le fichier contenant tous les mouvements de la solution.
    return chemin  # Renvoie les mouvements de la solution, ou None si aucun chemin n'existe.