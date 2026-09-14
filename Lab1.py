import sys
import numpy as np

count = 0 # Variable globale pour compter les occurrences
matriceinitiale = np.array([]) # matrice colonne "initiale" du jeu
matricevoulue = np.array([]) # matrice voulue du jeu
matriceresultat = np.array([]) # matrice résultat du mouvement (jeu actuel)
matriceidentite = np.array([[0]]) # matrice identité

def initialiser_application():
    """Préparation des ressources ou de la configuration."""
    print("Initialisation des composants...")
    # Lire le fichier .txt de l'exemple pour initialiser la matrice colonne "initiale"
    global matriceinitiale
    

    # Initialisation de la matrice voulue
    global matricevoulue
    matricevoulue = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    # Initialisation de la matrice résultat
    global matriceresultat
    matriceresultat = np.copy(matriceinitiale)

    # Initialisation de la matrice identité
    global matriceidentite
    matriceidentite = np.eye(9)


def main():
    """Fonction principale contenant le flux d'exécution."""
    initialiser_application()

    # Logique principale du programme
    print("Application en cours d'exécution.")

    # Retour d'un code de sortie (0 = succès)
    return 0

if __name__ == "__main__":
    # sys.exit assure que le script retourne un code d'erreur propre au système
    sys.exit(main())