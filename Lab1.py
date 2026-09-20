import sys  # Permet de lire les arguments du terminal et de renvoyer le code de sortie du programme.
import numpy as np  # Importe NumPy pour représenter et manipuler les grilles sous forme de matrices.
from pathlib import Path  # Importe Path pour construire les chemins des fichiers et des dossiers.

from Algo_Largeur import AlgoLargeur  # Importe la fonction AlgoLargeur définie dans le fichier Algo_Largeur.py.
from Algo_Profondeur import AlgoProfondeur  # Importe la fonction AlgoProfondeur définie dans le fichier Algo_Profondeur.py.

count = 0  # Initialise le compteur global des essais ; il sera remis à 1 pour chaque fichier d'entrée.
matriceinitiale = np.array([])  # Crée la variable qui contiendra la grille de départ après la lecture du fichier.
matricevoulue = np.array([])  # Crée la variable qui contiendra la grille objectif.
DOSSIER = Path(__file__).resolve().parent  # Récupère le dossier contenant ce script pour construire les chemins par défaut.

def initialiser_application(fichier=None):  # Définit la fonction qui lit une entrée et prépare les deux matrices du jeu.
    """Préparation des ressources ou de la configuration."""
    print("Initialisation des composants...")  # Affiche le début de la préparation des données.

    # Lire le fichier .txt de l'exemple pour initialiser la matrice "initiale"
    # Mode "r" (read) : lit le contenu
    if fichier is None:  # Vérifie si aucun fichier d'entrée n'a été précisé à l'appel de la fonction.
        fichier = DOSSIER / "input-Ex1" / "Ex1-1.txt"  # Choisit alors Ex1-1.txt dans le dossier input-Ex1 situé à côté de ce script.
    with open(fichier, "r", encoding="utf-8-sig") as f:  # Ouvre le fichier en lecture UTF-8 ; with le referme automatiquement à la fin du bloc.
        # Tout lire dans une seule chaîne
        JeuInitiale = f.read()  # Place tout le contenu du fichier dans la chaîne de caractères JeuInitiale.
    print ("Contenu du fichier exemple du jeu :")  # Affiche un titre pour présenter le contenu brut du fichier.
    print(JeuInitiale)  # Affiche les trois lignes du fichier telles qu'elles ont été lues.

    # Initialisation de la matrice "initiale"
    global matriceinitiale  # Permet à cette fonction de modifier la variable matriceinitiale déclarée en début de fichier.
    lignes = JeuInitiale.splitlines()  # Découpe le texte en lignes pour lire séparément les trois rangées de la grille.
    if len(lignes) != 3:  # Vérifie que le fichier contient exactement trois lignes.
        raise ValueError("Le fichier doit contenir exactement trois lignes.")  # Signale une entrée incorrecte si le nombre de lignes n'est pas égal à trois.
    cases = []  # Prépare une liste qui recevra les trois rangées de cases.
    for ligne in lignes:  # Parcourt les lignes du fichier une par une.
        # Conserver aussi les cases vides des fichiers originaux, sans '*'.
        valeurs = ligne.split("\t") if "\t" in ligne else ligne.split()  # Sépare les cases par les tabulations en gardant les cases vides ; sinon utilise les espaces.
        if len(valeurs) != 3:  # Vérifie que la rangée courante possède exactement trois cases.
            raise ValueError("Chaque ligne doit contenir exactement trois cases.")  # Signale une entrée incorrecte si une rangée ne contient pas trois cases.
        cases.append([valeur.strip() if valeur.strip() else "*" for valeur in valeurs])  # Nettoie les espaces autour des valeurs, remplace une case vide par * et ajoute la rangée.
    matriceinitiale = np.array(cases)  # Transforme les trois rangées en une matrice NumPy 3 x 3.
    if sorted(matriceinitiale.ravel().tolist()) != ["*", "1", "2", "3", "4", "5", "6", "7", "8"]:  # Met les cases à plat et les trie pour vérifier la présence unique de * et des chiffres 1 à 8.
        raise ValueError("Il faut les chiffres 1 a 8 une fois chacun et une case vide '*'.")  # Signale une grille contenant une valeur manquante, répétée ou interdite.
    print("Matrice initiale :")  # Affiche un titre avant la grille de départ.
    print(matriceinitiale)  # Affiche la matrice initiale qui sera transmise à la recherche.

    # Initialisation de la matrice voulue
    global matricevoulue  # Permet à cette fonction de modifier la variable globale matricevoulue.
    matricevoulue = np.array([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '*']])  # Définit la grille à atteindre : les chiffres dans l'ordre et la case vide en bas à droite.
    print("Matrice voulue :")  # Affiche un titre avant la grille objectif.
    print(matricevoulue)  # Affiche la matrice que l'algorithme doit atteindre.

def main():  # Définit la fonction principale qui choisit les entrées et lance les essais.
    """Fonction principale contenant le flux d'exécution."""
    arguments = sys.argv[1:]  # Récupère les arguments du terminal en laissant de côté le nom du script.
    algorithme = "largeur"  # Garde la recherche en largeur par défaut pour conserver les anciennes commandes.
    if arguments and arguments[0] in ("largeur", "profondeur"):  # Vérifie si le premier argument choisit explicitement l'un des deux algorithmes.
        algorithme = arguments.pop(0)  # Retient ce choix et retire ce premier argument pour traiter ensuite le fichier d'entrée.
    if len(arguments) > 1:  # Refuse plus d'un argument restant après le choix facultatif de l'algorithme.
        print("Utilisation : python Lab1.py [largeur | profondeur] [chemin_du_fichier | --tous]")  # Explique comment choisir la recherche et les entrées.
        return 1  # Termine main avec le code 1 pour signaler une mauvaise utilisation.
    if arguments and arguments[0] == "--tous":  # Vérifie si l'utilisateur demande de traiter les quatre fichiers d'entrée.
        fichiers = [DOSSIER / "input-Ex1" / f"Ex1-{i}.txt" for i in range(1, 5)]  # Construit les chemins de Ex1-1.txt à Ex1-4.txt ; range(1, 5) produit 1, 2, 3 et 4.
    elif arguments:  # Traite le cas où l'utilisateur a fourni un chemin de fichier à la place de --tous.
        fichiers = [Path(arguments[0])]  # Construit le chemin de l'unique fichier à traiter.
    else:  # Traite le lancement sans argument supplémentaire.
        fichiers = [DOSSIER / "input-Ex1" / "Ex1-1.txt"]  # Sélectionne uniquement Ex1-1.txt pour le lancement par défaut.
    fonction_recherche = AlgoLargeur if algorithme == "largeur" else AlgoProfondeur  # Sélectionne la fonction correspondant à la recherche demandée.

    # Logique principale du programme
    print("Application en cours d'exécution.")  # Annonce le lancement de l'application dans le terminal.

    # Boucle d'application de l'algorithme choisi pour résoudre le jeu.
    global count  # Permet à main de modifier le compteur global des essais.
    for fichier in fichiers:  # Traite successivement chaque fichier sélectionné.
        try:  # Prépare la gestion d'une éventuelle erreur de lecture ou de contenu.
            initialiser_application(fichier)  # Lit le fichier courant et prépare matriceinitiale et matricevoulue.
        except (OSError, ValueError) as erreur:  # Intercepte les erreurs d'accès au fichier et les erreurs de validation de la grille.
            print("Erreur de lecture :", erreur)  # Affiche la raison de l'erreur pour permettre de corriger le fichier ou son chemin.
            return 1  # Arrête l'application avec le code 1 quand la préparation de l'entrée échoue.

        # Un dossier par entrée évite de mélanger les quatre séries de mesures.
        dossier_sortie = DOSSIER / "resultats" / algorithme / fichier.stem  # Sépare les résultats par algorithme et par entrée ; fichier.stem donne le nom sans .txt.
        count = 1  # Commence la numérotation des essais à 1 pour ce fichier d'entrée.
        while (count <= 10):  # Répète la recherche pour les essais 1 à 10 inclus, soit exactement dix exécutions.
            print("Execution", algorithme, "#", count, "-", fichier.name)  # Affiche l'algorithme choisi, le numéro de l'essai et le fichier d'entrée.
            fonction_recherche(matriceinitiale, matricevoulue, count, dossier_sortie)  # Lance l'algorithme choisi avec les matrices, le numéro d'essai et le dossier de sortie.
            count += 1  # Passe au numéro d'essai suivant après la fin de la recherche.
    
    # Retour d'un code de sortie (0 = succès)
    return 0  # Renvoie le code 0 lorsque tous les essais demandés se sont déroulés normalement.

if __name__ == "__main__":  # Exécute ce bloc lorsque Lab1.py est lancé comme programme principal.
    # sys.exit assure que le script retourne un code d'erreur propre au système
    sys.exit(main())  # Appelle main puis transmet son code de retour au terminal.