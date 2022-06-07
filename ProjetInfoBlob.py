from random import randint, choices
from numpy import array
from matplotlib.pyplot import show, matshow, axis, pause, clf
from matplotlib.colors import ListedColormap, BoundaryNorm
from math import exp

tailleGenFloc = (9,9) # Taille des matrices de génération des flocons (doit rester impair)
taille=(101,101) # Taille de la carte (doit rester impair)
nbFlocon=13
tailleFloc=20 # Nombre de pixels par flocons
positionInit=(int((taille[0]-1)/2),int((taille[1]-1)/2)) # Premier pixel du blob
nbItération=1000 # Nombre d'opération d'extension du blob

couleurs=ListedColormap([[19/255,34/255,58/255],[254/255,245/255,188/255],[1.0,175/255,1/255],[207/255,117/255,12/255]])
palette=BoundaryNorm([0,1,2,3,4], couleurs.N)

phi = (5**(1/2)+1)/2 # Nombre d'or

def granti (p,f): # Fonction I calcule l'intensité olfactive
        d = ((p[0]-f[0])**2+(p[1]-f[1])**2)**0.5
        i = phi**(-d)
        return i

"""Génération de flocon"""

def prox(p,flocon): # Proximité cumulée du pixel avec l'ensemble des flocons
    if p in flocon: # Dans la matrice des intensités olfactives, les flocons sont à -1
        return 0
    else:
        return sum([granti(p,u) for u in flocon])

def voisin(p) : # Renvoie les voisins en haut, bas, gauche, droite du pixel
    liste = []
    if p[0]!=tailleGenFloc[0]-1 :
        liste.append((p[0]+1,p[1]))
    if p[0]!=0 :
        liste.append((p[0]-1,p[1]))
    if p[1]!=tailleGenFloc[1]-1 :
        liste.append((p[0],p[1]+1))
    if p[0]!=0 :
        liste.append((p[0],p[1]-1))
    return liste

def ainfloqu(proba,flocon) : # Ajout d'un pixel au flocon et réactualisation du champs de probabilité
    vois = []
    poids = []
    for f in flocon:
        l = voisin(f)
        for p in l:
            if not(p in vois) :
                vois.append(p)
                poids.append(proba[int(p[0])][int(p[1])])
    poids =[exp(p) for p in poids]
    flocon.extend(choices(vois, weights=poids, k=1))
    proba = [[prox((i,j),flocon) for j in range (tailleGenFloc[0])] for i in range (tailleGenFloc[1])] # Réactualisation du champs de probabilité
    return proba

def genFloc():
    flocon = [(int((tailleGenFloc[0]-1)/2),
               int((tailleGenFloc[1]-1)/2))] # Coordonnées du pixel initial au centre de sa matrice de génération
    proba = [[prox((i,j),flocon) for j in range (tailleGenFloc[0])] for i in range (tailleGenFloc[1])]
    for i in range(tailleFloc) :
        proba=ainfloqu(proba,flocon)
    return flocon

"""Matrice générale des flocons"""

def hum (p): # Fonction hum calcule l'intensité olfactive pour chaque centre de flocon en additionnant les odeurs de chacun des flocons 
    if p in listeFlocPix:
        return -1
    else:
        return sum([granti(p,u) for u in listeFlocCen])

listeFlocCen = [(randint(tailleGenFloc[0],taille[1]-(tailleGenFloc[0]+1)),
                 randint(tailleGenFloc[1],taille[0]-(tailleGenFloc[0]+1))) for n in range(nbFlocon)] # Liste des coordonnées des centres des flocons
listeIsol = [genFloc() for n in range(nbFlocon)] # Liste des listes des coodonnées des pixels de flocons
listeFlocPix = [] # Liste des pixels de flocons
for i in range(nbFlocon): # On ajoute les pixels de flocons (générés dans leur matrice de génération) dans la matrice globale par un changement de repère
    l=[(pix[0]-int((tailleGenFloc[0]-1)/2)+listeFlocCen[i][0],
               pix[1]-int((tailleGenFloc[1]-1)/2)+listeFlocCen[i][1]) for pix in listeIsol[i]]
    for p in l:
        if not p in listeFlocPix: # On fait en sorte de ne pas avoir de doublons
            listeFlocPix.append(p)

matriss = array([[hum((i,j)) for j in range (taille[0])] for i in range (taille[1])]) # Matrice de l'intensité olfactive cumulée de chaque pixel

mat = array([[0 for j in range (taille[0])] for i in range (taille[1])]) # Création de la matrice générale, initialement vide
for pix in listeFlocPix:
    mat[pix[0],pix[1]]=1 # Tous les points de la matrice qui sont des flocons prennent la valeur 1

"""le blob"""

def bordure(p) : # Renvoie les voisins en haut, bas, gauche, droite du pixel
    liste = []
    if p[0]!=taille[0]-1 :
        liste.append((p[0]+1,p[1]))
    if p[0]!=0 :
        liste.append((p[0]-1,p[1]))
    if p[1]!=taille[1]-1 :
        liste.append((p[0],p[1]+1))
    if p[1]!=0 :
        liste.append((p[0],p[1]-1))
    return liste

listePixBlob=[positionInit] # Liste des pixels de blob
mat[positionInit[0],positionInit[1]]=2
matshow(mat,fignum=1,cmap=couleurs,norm=palette)
axis("off")
pause(0.01)
clf()
i=0
while i<nbItération and listeFlocPix!=[] : # Afin que la boucle se termine quand il n'y a plus de flocon
    bord=[] # Liste des pixels en bordure du blob
    bordFloc=[] # Liste des pixels en bordure du blob qui sont des flocons
    odeur=[] # Odeur sur ces pixels
    for p in listePixBlob :
        l=bordure(p)
        for b in l :
            if not mat[b[0],b[1]] in [2,3] : # On vérifie si le pixel n'appartient pas déjà au blob
                bord.append(b)
                odeur.append(matriss[b[0],b[1]])
                if mat[b[0],b[1]]==1 and not b in bordFloc : # On vérifie si le pixel est un pixel de flocon
                    bordFloc.append(b)
    if bordFloc==[]:
        choisi=choices(bord, weights=odeur, k=1)
        listePixBlob.extend(choisi)
        mat[choisi[0][0],choisi[0][1]]=2
    else:
        listePixBlob.extend(bordFloc)
        for p in bordFloc :
            mat[p[0],p[1]]=3
            listeFlocPix.remove(p) # Suppression du pixel de flocon p de la liste des pixels de flocon
            if p in listeFlocCen : 
                listeFlocCen.remove(p) # Suppression du pixel de flocon p de la liste des centres de flocon
                matriss = array([[hum((i,j)) for j in range (taille[0])] for i in range (taille[1])]) # Actualisation de la matrice d'intensité olfactive
    matshow(mat,fignum=1,cmap=couleurs,norm=palette)
    axis("off")
    pause(0.01)
    clf()
    i+=1
print("fin")
matshow(mat,fignum=1,cmap=couleurs,norm=palette)
axis("off") # Pour enlever les axes
show()

