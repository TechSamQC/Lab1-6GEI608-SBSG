# LAB 1 - 6GEI608 - Intelligence artificielle et reconnaissance des formes (SBSG)

## À noter : Changements apportés aux fichiers exemples
Les fichiers exemples ont été modifiés afin d'y intégrer le caractère "*" à l'emplacement de l'espace vide pour faciliter le code.

## Explication du fonctionnement de base des algorithmes
### 1. Recherche en largeur
Pour la recherche en largeur, l'algorithme fait les opérations suivantes :
1. Ajoute itérativement les enfants d'un état (haut, bas, gauche, droite) dans une liste sous forme de matrice.
2. Après avoir ajouté tous les enfants possibles, l'itération augmente de 1 et passe ainsi à l'élément suivant de la liste et retourne à l'étape 1. avec cet élément. (Principe FIFO)
3. Pour retrouver le chemin de la solution, l'algorithme remonte les parents à partir de l'état final jusqu'à l'état initial.

**PARTICULARITÉS :**
+ SI on atteint la fin de la liste (quand l'itération est plus haut que la longueur de la liste), tous les états ont été explorés et on n’a pas de solution.
+ Les états déjà explorés ne reviennent pas dans la liste frontière, permettant d'éviter les boucles.
+ La vérification d'états vue se fait à l'aide d'un "set". Le "set" permet d'avoir une liste de suite d'octets, plutôt que de matrice. Lors de la comparaison et vérification si un état a déjà été vu, c'est beaucoup plus rapide de comparer des suites d'octets que des matrices complètes\.
+ Une liste de parents est maintenue pour chaque état afin de pouvoir reconstruire le chemin de la solution. Cette liste contient le numéro de l'index de l'état parent de l'état à l'index courant, ce qui permet de retrouver le parent dans la liste frontière.
+ La solution est écrite dans le fichier Algo_Largeur_x_chemin_solution.txt
+ Les statistiques et les détails de l'exécution sont dans le fichier Algo_Largeur_x_stats.txt

### 2. Recherche en profondeur
Pour la recherche en profondeur, l'algorithme fait les opérations suivantes :
1. Ajoute itérativement les enfants d'un état (haut, bas, gauche, droite) dans une liste sous forme de matrice.
2. Ajoute le numéro de l'index des enfants dans une pile.
3. Suit le même principe que la recherche en largeur, mais à chaque itération, l'algorithme prend l'index du dernier élément ajouté dans la pile pour explorer l'état correspondant dans la liste des états (au lieu de l'itération séquentielle). (Principe LIFO)
4. Pour retrouver le chemin de la solution, l'algorithme remonte les parents à partir de l'état final jusqu'à l'état initial.

**PARTICULARITÉS :**
+ SI on atteint la fin de la liste (quand l'itération est plus haut que la longueur de la liste), tous les états ont été explorés et on n’a pas de solution. C'est également le cas si la pile est vide.
+ Les états déjà explorés ne reviennent pas dans la liste frontière ou dans la pile, permettant d'éviter les boucles.
+ La vérification d'états vue se fait à l'aide d'un "set". Le "set" permet d'avoir une liste de suite d'octets, plutôt que de matrice. Lors de la comparaison et vérification si un état a déjà été vu, c'est beaucoup plus rapide de comparer des suites d'octets que des matrices complètes\.
+ Une liste de parents est maintenue pour chaque état afin de pouvoir reconstruire le chemin de la solution. Cette liste contient le numéro de l'index de l'état parent de l'état à l'index courant, ce qui permet de retrouver le parent dans la liste frontière.
+ La solution est écrite dans le fichier Algo_Profondeur_x_chemin_solution.txt
+ Les statistiques et les détails de l'exécution sont dans le fichier Algo_Profondeur_x_stats.txt

### 3. Recherche à approfondissement itératif
Pour la recherche à approfondissement itératif, l'algorithme fait les opérations suivantes :
1. Initialise une profondeur maximale initiale à 0 et maximale finale à 40.
2. Applique une recherche en profondeur (même principe que la recherche en profondeur classique (LIFO)) limitée par la profondeur maximale. On respecte la limite en arrêtant d'ajouter les enfants qui dépasseraient cette profondeur.
3. Si la solution n'est pas trouvée dans la profondeur maximale actuelle (la pile se vide), augmente la profondeur maximale de 1, réinitialise les variables et répète l'étape 2.
4. Continue jusqu'à ce que la solution soit trouvée ou que la profondeur maximale finale soit atteinte.
5. Pour retrouver le chemin de la solution, l'algorithme remonte les parents à partir de l'état final jusqu'à l'état initial.

**PARTICULARITÉS :**
+ L'algorithme combine les avantages de la recherche en profondeur et de la recherche en largeur.
+ Il explore les états de manière itérative en profondeur croissante, ce qui permet de trouver des solutions optimales tout en limitant l'utilisation de la mémoire.
+ Le défaut est que l'exécution est plus lente, étant donné qu'on doit recommencer la recherche à partir du début pour chaque augmentation de la profondeur maximale.
+ Les états déjà explorés ne reviennent pas dans la liste frontière ou dans la pile, permettant d'éviter les boucles.
+ La vérification d'états vue se fait à l'aide d'un "set". Le "set" permet d'avoir une liste de suite d'octets, plutôt que de matrice. Lors de la comparaison et vérification si un état a déjà été vu, c'est beaucoup plus rapide de comparer des suites d'octets que des matrices complètes\.
+ Une liste de parents est maintenue pour chaque état afin de pouvoir reconstruire le chemin de la solution. Cette liste contient le numéro de l'index de l'état parent de l'état à l'index courant, ce qui permet de retrouver le parent dans la liste frontière.
+ La solution est écrite dans le fichier Algo_ApprofondissementIteratif_x_chemin_solution.txt
+ Les statistiques et les détails de l'exécution sont dans le fichier Algo_ApprofondissementIteratif_x_stats.txt

## Comparaison des algorithmes
+Largeur : Donne toujours la solution la plus courte en termes de nombre de mouvements (profondeur minimale).

-Largeur : Peut consommer beaucoup de mémoire pour des problèmes avec un grand nombre d'états.

-Profondeur : Peut trouver une solution plus rapidement si elle est proche de l'état initial.

-Profondeur : Ne garantis pas de trouver la solution la plus courte (souvent très loin de l'optimal). Consomme souvent autant de mémoire que la recherche en largeur.

+Approfondissement itératif : Consomme peu de mémoire et son temps d'exécution est presque stable.

-Approfondissement itératif : Lenteur d'exécution due au redémarrage de la recherche à chaque augmentation de la profondeur maximale.

En résumé, on constate que cela dépend énormément du cas de départ. Par exemple, l'état initial 1 est résolu rapidement par la recherche en profondeur, moins rapidement par la recherche en largeur et de manière intermédiaire par l'approfondissement itératif. En général, on remarque que l'approfondissement itératif prend plus de temps à s'exécuter, ce qui s'explique par le redémarrage de la recherche à chaque augmentation de la profondeur maximale.
Si l’on compare les solutions, on remarque que la recherche en largeur donne toujours la solution la plus courte, tandis que la recherche en profondeur peut donner une solution plus rapide, mais souvent plus longue, et l'approfondissement itératif offre un compromis entre les deux. 
Pour ce qui est de la consommation de mémoire, la recherche en approfondissement itératif a un clair avantage par rapport aux autres méthodes. En effet, on remarque que la liste frontière finale de cette méthode est toujours plus petite comparée à celle des autres méthodes. 
Donc, si l'on cherche à trouver la solution la plus courte, la recherche en largeur est la meilleure option. Si on cherche à trouver une solution avec une allocation de mémoire limitée, l'approfondissement itératif est à privilégier. Pour avoir le meilleur temps d'exécution, il n'y a pas de solution unique, mais la recherche en largeur est souvent la plus rapide, en plus de garantir la solution la plus courte.

## Ce que nous avons appris

Ce laboratoire nous a permis de comprendre concrètement comment les algorithmes de recherche explorent les états du 8-puzzle pour atteindre une configuration souhaitée. Nous avons appris à représenter les états sous forme de matrices et à générer leurs voisins en déplaçant la case vide.
L'utilisation des principes FIFO et LIFO nous a montré que l'ordre d'exploration influence le temps de recherche et la longueur du chemin obtenu. Nous avons également compris l'importance de mémoriser les états déjà rencontrés pour éviter les boucles et de conserver les liens entre parents et enfants pour reconstruire la solution. Pour l'approfondissement itératif, nous avons constaté que l'augmentation progressive de la limite de profondeur entraîne des explorations répétées, ce qui peut allonger l'exécution. Les dix essais réalisés pour chaque entrée nous ont permis de comparer les temps d'exécution, les tailles de frontière et le nombre d'états examinés. Ces observations nous ont montré que les performances dépendent de l'état initial et qu'une solution trouvée rapidement peut demander beaucoup plus de déplacements.
