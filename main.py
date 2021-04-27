from time import sleep
from random import randint
import json

#Direction 0 > horizontal / 1 > vertical

#Dictionnaire contenant les coordonnées de chaque bateau ainsi que leur direction
escadron=[
    {'type': 'porte-avion','initiale': 'K','localisation': '','direction': ''},   
    {'type': 'croiseur','initiale': 'C','localisation': '','direction': ''},    
    {'type': 'contre-torpilleur','initiale': 'P','localisation': '','direction': ''},    
    {'type': 'sous-marin','initiale': 'S','localisation': '','direction': ''},  
    {'type': 'torpilleur','initiale': 'T','localisation': '','direction': ''},
    ]

absc=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']#Axe des abscisses de la grille
lengths=[5,4,3,3,2]#Longueur de chaque bateau, du plus grand au plus petite, utile pour généré tout les bateaux à la suite 
taken=[]#Liste des coordonnées occupées par les bateaux uniquement
nms=[]#liste de coordonnées juxtaposées aux bateaux + les coordonnées des bateaux (nms pour no man's land)
user_reply=[]#Liste des coordonnées que l'utilisateur répond
hit=0#total des bateaux touchés
hit_k=0#nombre de fois que le porte-avion est touché
hit_c=0#nombre de fois que le croiseur est touché
hit_p=0#nombre de fois que le contre-torpilleur est touché
hit_s=0#nombre de fois que le sous-marin est touché
hit_t=0#nombre de fois que le torpilleur est touché
score=0#score du joueur
throw=0#Nombre de tir total

def valid(nms,coos_ind):
    """Parameters
    ----------
    nms : Fonction qui prend toutes les coordonnées occupés par les bateaux et celles jusxtaposés
    coos_ind : Coordonnées temporaire du bateau concerné, comparé avec les coordonnées déjà occupés

    Returns
    -------
    Cette fonction retourne vrai si le résultat de la comparaison des coordonnées occupés et celles des coordonées temporaire d'un bateau font doublons
    quelque-part, auquel-cas, les coordonnées temporaire du bateau devront être regénérées. """
    inc=0
    if len(coos_ind)==5:#Validé le premier bateau avait aucune coordonnées renverrai forcément False
        return False        
    for elt in nms:
        for i in range(len(coos_ind)):
            if elt==coos_ind[i]:
                inc+=1#Si l'une des coordonnées est déjà dans nms, l'incrément s'incrémente.
        if inc>0:
            return True
    if inc==0:
        return False
    
def koala(direction,nms,letter,number,boat_localisation,lengths,u):
    """Cette fonction est appelée uniquement si les bateaux sont validés par la fonction valid(), elle permet de crée toutes les coordonnées jusxtaposées 
    au bateau puis de les appliqués à la liste nms. 

        Parameters
        ----------
        direction : Prend en compte la direction du bateau
        nms : Prend en compte la liste de toute les coordonnées occupées
        letter : lettre initiale du bateau
        number : nombre initiale du bateau
        boat_localisation : coordonnées occupées par le bateau
        lengths : Prend en compte la liste des longueurs des bateaux
        u : indice qui permet de parcourir les listes

        Returns
        -------
        nms : Il retourne la nouvelle liste de toute les coordonnées occupées."""
    if direction==0:#Si le bateau est horizontal 
        for i in range(lengths[u]): #On génére le nombre de coordonnées qui est égal à la longueur du bateau
            nms.append((str(chr(ord(letter)+i)))+str(number+1))#coos du bateau à droite
            nms.append((str(chr(ord(letter)+i)))+str(number-1))#coos du bateau à gauche      
        nms.append(str(chr(ord(letter)-1)+str(number)))#extrémité gauche
        nms.append((str(chr(ord(letter)+lengths[u])))+str(number))#extrémité droite
        nms.append((str(chr(ord(letter)-1)))+str(number+1))#coin BG
        nms.append((str(chr(ord(letter)-1)))+str(number-1))#coin HG
        nms.append((str(chr(ord(letter)+lengths[u])))+str(number+1))#coin BD
        nms.append((str(chr(ord(letter)+lengths[u])))+str(number-1)) #coin HD
        
        for h in range(2):#On fait cette vérification 2 fois pour une raison incongru, sinon y a des bugs...
            for p,coos in enumerate(nms):#Ces conditions supprime les coordonnées générés précédemment si elles sont en dehors du cadre
                if ord(coos[0])>74:
                    del nms[p]
                if ord(coos[0])<65:
                    del nms[p]
                if int(coos[1:])>10:
                    del nms[p]
                if int(coos[1:])<1:
                    del nms[p]
            
    if direction==1:#Si le bateau est vertical
        for i in range(lengths[u]):
            nms.append((str(chr(ord(letter)+1)))+str(number+i))#coos du bateau à droite
            nms.append((str(chr(ord(letter)-1)))+str(number+i))#coos du bateau à gauche   
        nms.append((str(letter))+str(number-1))#extrémité haut
        nms.append((str(letter))+str(number+lengths[u]))#extrémité bas
        nms.append((str(chr(ord(letter)+1)))+str(number-1))#coin HD
        nms.append((str(chr(ord(letter)-1)))+str(number-1))#coin HG
        nms.append((str(chr(ord(letter)+1)))+str(number+lengths[u]))#coin BD
        nms.append((str(chr(ord(letter)-1)))+str(number+lengths[u]))#coin BG
        
        for h in range(2):#On fait cette vérification 2 fois pour une raison incongru, sinon y a des bugs...
            for p,coos in enumerate(nms):#Ces conditions supprime les coordonnées générés précédemment si elles sont en dehors du cadre
                if ord(coos[0])>74:
                    del nms[p]
                if ord(coos[0])<65:
                    del nms[p]           
                if int(coos[1:])>10:
                    del nms[p]
                if int(coos[1:])<1:
                    del nms[p]
    return nms 
        
def grid(y):
    """Parameters
    ----------
    y : Ce paramètre est la liste des coordonnées renseignées par l'utilisateur qui est localisé et placer dans la grille

    Returns
    -------
    grid : il retourne le plateau avec les coordonnées"""
    
    grid=[' ']*10#Création d'une matrice
    for i in range(len(grid)):#Toujours création d'une matrice
        grid[i]=[' ']*10 #La même qu'en haut
    
    for elt in y:   
        grid[int(elt[1:])-1][ord(elt[0])-65]='x'#On place la coordonnée dans le plateau en remplaçant le vide par un sobre "x"

    return grid

def user_grid(grid):
    """Cette fonction permet d'afficher correctement le plateau, progressivement de haut en bas afin d'avoir un plateau rangé
    
    Parameters
    ----------
    grid : Plateau, défini précdemment

    Returns
    -------
    None."""
    print(absc)#Insertion de l'axe des abscisses
    for i in grid:
        print(i)
        
def fastend():
    '''
    Cette fonction permet de généré des coordonnées aléatoires afin de terminer la partie.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    
    letter=str(chr(randint(65,74)))
    number=randint(1,10)
    return str(letter)+str(number)


##################################################################################################
#                                   Generations des bateaux                                      #
##################################################################################################

for u in range(len(lengths)):#On répète la génération le nombre de fois qu'il y a de bateau, soit la longueur de la liste des longueurs de bateaux 
    boat_localisation=[]#Liste des coordonnées des bateaux individuels
    boat_direction=randint(0,1)#Géneration de la direction du bateau, horizontal ou vertical
    if boat_direction==0:
        letter=str(chr(randint(65,74-lengths[u])))#On génère une lettre aléatoire
        number=randint(1,10)#On génère un nombre aléatoire 
    if boat_direction==1:
        letter=str(chr(randint(65,74)))#On génère une lettre aléatoire
        number=randint(1,10-lengths[u])#On génère un nombre aléatoire 
        
    init=str(letter)+str(number)#On assemble les 2 pour formés une coordonnées initiale
    
    if boat_direction==0:
        for i in range(lengths[u]):
            boat_localisation.append(str(chr(ord(init[0])+i))+str(number))#On étend les coordonnées en fonction de la longueur des bateaux, et en fonction de la direction
    if boat_direction==1:
        for i in range(lengths[u]):
            boat_localisation.append((str(letter))+(str(number+i)))#On étend les coordonnées en fonction de la longueur des bateaux, et en fonction de la direction
    
        
    while valid(nms,boat_localisation)==True:#On vérifie si les coordonnées sont valides et si elles ne font pas doublons avec les autres, ici, si elle n'est pas valide
        boat_localisation=[] #On répète le processus jusqu'à ce que les coordonnées soient valides
        boat_direction=randint(0,1)
        if boat_direction==0:
            letter=str(chr(randint(65,74-lengths[u])))
            number=randint(1,10)
        if boat_direction==1:
            letter=str(chr(randint(65,74)))
            number=randint(1,10-lengths[u])
            
        init=str(letter)+str(number)
        
        if boat_direction==0:
            for i in range(lengths[u]):
                boat_localisation.append(str(chr(ord(init[0])+i))+str(number))        
        if boat_direction==1:
            for i in range(lengths[u]):
                boat_localisation.append((str(letter))+(str(number+i)))
                
        if valid(nms,boat_localisation)==False:#Si les coordonnées sont valides
            taken.append(boat_localisation)#On les ajoutes à la liste taken
            for elt in boat_localisation:
                nms.append(elt)#On ajoute dans un premier-temps aux coordonnées interdites les coordonnées des bateaux dans un premier-temps
            koala(boat_direction,nms,letter,number,boat_localisation,lengths,u)#On appelle la fonction pour généré les coordonnées autour des bateaux
            escadron[u]['localisation']=taken[u]#On ajoute les coordonnées qui sont valides au dictionnaire, ce seront les coordonnées finales
            escadron[u]['direction']=boat_direction#On ajoute également la direction même si c'est pas très utile
            break#Lorsque que toutes les coordonnées sont valides, on arrête la boucle while
            
    else:#On effectue le même processus
        taken.append(boat_localisation)
        for elt in boat_localisation:
            nms.append(elt)
        koala(boat_direction,nms,letter,number,boat_localisation,lengths,u)
        escadron[u]['localisation']=taken[u]
        escadron[u]['direction']=boat_direction
        
##################################################################################################
#                                             START                                              #
##################################################################################################
        
print('<Bienvenue dans un jeu de Bataille Navale>\n')
sleep(1)#sleep qui repose l'utilisateur pour pas qu'il se sente agresser 
while hit<17:
    user_grid(grid(''))#Affichage du plateau 
    print('\n')
    print('Saisissez une coordonnée valide ex: E8')
    while True:#Cette boucle vérifie que la coordonnée renseigné est valide
        debug1=0#Cette variable permet d'éviter un doublon dans les affichages pour la suite
        print('\n')
        try:
            while True:#Cette boucle vérifie que la coordonnée renseigné n'a pas déjà été renseigné précedemment
                try:
                    user_response=str(input('>>> '))#L'utilisateur rentre sa coordonnée 
                    if user_response not in user_reply:#Ici on vérifie que la coordonnée valide a pas déjà été renseigné
                        break
                    else:
                        print('>>> Vous avez déjà renseigné cette coordonnée, entrez-en une autre')  
                        throw-=1#Empêche de compter 2 fois le tir si il y a un doublon
                except:
                    print('>>> Vous avez déjà renseigné cette coordonnée, entrez-en une autre')                   
            if user_response=='quit': #permet de quitter le jeu (très utile lors d'un débogage)
                hit+=17
                throw-=1
                break  
            
            #Je n'ai pas réussi à faire fonctionner cette partie du programme qui 
            #consiste à faire terminer le jeu en générant des coordonnées aléatoires comme le stipule le dernier critère
            '''if user_response=='end': 
                while hit<17:
                    user_response=fastend()'''

            if user_response[0]>chr(64) and user_response[0]<chr(75) and int(user_response[1:])>0 and int(user_response[1:])<11:#On vérifie que la coordonnée rentré est valide
                user_reply.append(user_response)#Si la coordonnée est valide, on l'a met dans la liste des coordonnée renseigné par l'utilisateur
                throw+=1#On compte le nombre de tir
                for elt in escadron:   
                    if user_response in elt['localisation']:#Si la coordonnée est dans le dictionnaire
                        debug1+=1#On incrémente cette variable afin de ne pas avoir de doublon dans l'affichage
                        hit+=1#On incrémente la variable si l'un des bateaux est touché
                        score+=1#Lors d'un hit, le score est incrémenté de 1
                        print('\n')
                        print('Féliciations vous avez touché', elt['type'])#On regarde quel bateau est touché
                        if elt['type']=='porte-avion':#Si le bateau touché est le porte-avion
                            hit_k+=1#On incrémente la variable de hit du porte-avion
                            if hit_k==5:#Si il est égal à sa longueur (élimination du bateau)
                                score+=5#Le score s'incrémente de 5 lorsqu'un bateau est détruit
                                print('\n')
                                print('>>> Vous avez éliminé porte-avion')                            
                        if elt['type']=='croiseur':#Si le bateau touché est le croiseur
                            hit_c+=1#On incrémente la variable de hit du croiseur
                            if hit_c==4:#Si il est égal à sa longueur (élimination du bateau)
                                score+=5#Le score s'incrémente de 5 lorsqu'un bateau est détruit
                                print('\n')
                                print('>>> Vous avez éliminé croiseur')                              
                        if elt['type']=='contre-torpilleur':#Si le bateau touché est le contre-torpilleur
                            hit_p+=1#On incrémente la variable de hit du contre-torpilleur
                            if hit_p==3:#Si il est égal à sa longueur (élimination du bateau)
                                score+=5#Le score s'incrémente de 5 lorsqu'un bateau est détruit
                                print('\n')
                                print('>>> Vous avez éliminé contre-torpilleur')                                 
                        if elt['type']=='sous-marin':#Si le bateau touché est le sous-marin
                            hit_s+=1#On incrémente la variable de hit du sous-marin
                            if hit_s==3:#Si il est égal à sa longueur (élimination du bateau)
                                score+=5#Le score s'incrémente de 5 lorsqu'un bateau est détruit
                                print('\n')
                                print('>>> Vous avez éliminé sous-marin')                          
                        if elt['type']=='torpilleur':#Si le bateau touché est le torpilleur
                            hit_t+=1#On incrémente la variable de hit du torpilleur
                            if hit_t==2:#Si il est égal à sa longueur (élimination du bateau)
                                score+=5#Le score s'incrémente de 5 lorsqu'un bateau est détruit
                                print('\n')
                                print('>>> Vous avez éliminé torpilleur')    
                                
                        print('\n')
                        print(user_grid(grid(user_reply)))#On met à jour le plateau par la liste des cooronnées renseigné par l'utilisateur
                        
                #Si le tir est dans l'eau      
                if debug1==0:#Eviter le doublon du plateau
                    throw+=1#On compte le nombre de tir
                    score-=1#Si le tir est dans l'eau, le score diminue de 1
                    print('\n')
                    print("Dans l'eau")
                    print('\n')
                    print(user_grid(grid(user_reply)))#On met à jour le plateau par la liste des cooronnées renseigné par l'utilisateur
                        
                if hit==17:#Détection de la fin du jeu
                    print('>>> Félicitations vous avez éliminé tout les bateaux')
                    print('>>> Votre score est', score)#Fin du jeu avec le score
                    break
            else:
                print("Coordonnées invalide, veuillez réessayer en suivant l'exemple")
        except:
            print("Coordonnées invalide, veuillez réessayer en suivant l'exemple")
     
#euuuw je galère à expliquer comment ça marche car ça vient beaucoup d'internet mais ouai
data={
    'throw': throw,#On met dans la base de données le nombre de tir
    'score': score,#Le score
    'porte-avion': escadron[0]['localisation'],#Coordonnées du porte-avion
    'croiseur': escadron[1]['localisation'],#Coordonnées du croiseur
    'contre-torpilleur': escadron[2]['localisation'],#Coordonnées contre-torpilleur
    'sous-marin': escadron[3]['localisation'],#Coordonnées sous-marin
    'torpilleur': escadron[4]['localisation'],#Coordonnées du torpilleur
    }

with open("a.txt", "r") as file:
    if len(file.read())==0:
        a=[]
    else:
        a=json.loads(open("a.txt", "r").read())
a.append(data)
open('a.txt', "w").write(json.dumps(a))


#22 mars 2021 >>> 26 avril 2021 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH