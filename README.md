# BlobSimulation
Le projet est de modéliser des Blobs (Physarum polycephalum) sur Python pour ma première année en CPES à Janson de Sailly.
Le blob est un être vivant unicellulaire qui se nourrit principalement en laboratoire de flocons d’avoine. Il est capable d’atteindre des tailles conséquentes (de l’ordre du centimètre) et est doué de capacités d’optimisation de ses déplacements intéressantes à étudier. Des expériences ont déjà été réalisées sur cet être : il sait sortir d’un labyrinthe de façon optimisée, ou même former un réseau pertinent pour relier plusieurs points sur une carte par exemple. C’est pourquoi je souhaite l’étudier et le modéliser à travers ce projet.
### Objectif
Modéliser sur Python un blob fluide, cohérent et esthétique capable de se déplacer pour se nourrir et de se reproduire. 
### Réalisation
**Fonctionnement général du code:** 

Il y a plusieurs fonctions pour les odeurs dégagées par les flocons d'avoine, la formation de flocons de plusieurs pixels et le blob. Le code se divise en 4 parties: d’abord il place des flocons de façon aléatoire dans une matrice, puis il calcule leur odeur, ensuite il génère des flocons de forme aléatoire. Enfin il fait évoluer le blob qui va essayer de trouver le chemin le plus court pour atteindre les flocons grâce au champ olfactif.
Les fonctions pour former un champ olfactif qui va déterminer le déplacement du blob:
“granti” permet de calculer l'intensité olfactive de chaque pixel de flocon avec notamment “phi” (le nombre d’or) pour obtenir une décroissance de cette même intensité olfactive.

“hum” additionne les intensités olfactives de chaque pixel calculées par “granti” pour ensuite former une matrice des odeurs cumulées.
Les fonctions pour créer un flocon de forme aléatoire formé de plusieurs pixels:

“prox” calcul avec “granti” un champs de probabilité autour du premier pixel de flocon

“voisin” ajoute dans une liste les coordonnées des voisins (haut, bas, gauche, droite) d’un pixel de flocon et vérifie s’il n’est pas une limite de la taille du flocon. 

“ainfloqu” détermine lequel des voisins sera un nouveau pixel de flocon grâce à “prox”
La fonction pour faire grandir le blob:

“bordure” cherche tous les voisins d’un pixel de blob (si le pixel est sur le bord gauche alors la fonction ne renverra que 3 voisins: celui du haut, du bas, de droite).

**Méthode de construction du réseau:**

Le blob, à chaque itération, cherche quels sont les flocons les plus proches par l’intensité olfactive. Il détermine quelles zones de son réseau sont les plus proches de ces flocons pour s’en servir de départ pour de nouvelles branches pour atteindre de façon optimisée ces derniers. 

**Optimisation:**

Dualité liste/matrice: 

Avec une liste, le coût d'accès à tous les éléments d’un certain type est linéaire au nombre de ces derniers, alors qu’avec la matrice, il serait linéaire au nombre de tous les éléments (par exemple, si l’on veut accéder aux pixels de flocons dans la matrice générale, on peut soit vérifier tous les pixels en utilisant la matrice, soit lire les éléments de la liste des pixels de flocon “listeFlocPix”).
Pour savoir l’état d’un pixel (vide, blob, flocon ou flocon mangé), on peut y accéder en temps constant par une matrice, mais si l’on utilise que des listes, on devra vérifier dans quelle liste le pixel est, ce qui a un coût linéaire au nombre total de pixel

J'ai accéléré le code en réduisant le nombre de calculs:

en évitant de calculer la matrice des odeurs chaque fois que le blob mange un pixel de flocon mais en l’actualisant seulement une fois le centre du flocon mangé. En ne calculant l’intensité olfactive que du centre de chaque flocons et non de tous leurs pixels.
