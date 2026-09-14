import sys

def initialiser_application():
    """Préparation des ressources ou de la configuration."""
    print("Initialisation des composants...")


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