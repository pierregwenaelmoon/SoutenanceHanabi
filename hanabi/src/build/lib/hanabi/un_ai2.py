import hanabi.ai
import hanabi

import itertools


from hanabi.ai import AI 





class Recommander(AI):

    def __init__(self, game):
        self.game = game
        self.actions_depuis_le_dernier_indice=[0,0,10] #[nombre de cartes jouees,nombre de cartes defaussees,dernier indice]
        #nombre de cartes jouees + nombre de cartes = nombre de tour depuis le dernier indice.
        self.list_players = ['Alice','Benji','Clara','Dante','Elric']
        self.actions = [6]*5 
        self.recommandation_dictionnary =   {0 : ('rank',0), 1 : ('rank',1), 2 : ('rank',2), 3 : ('rank',3), 4 : ('suit',0), 5 : ('suit',1), 6 : ('suit',2), 7 : ('suit',3)}
                                      
                                     
                                      
                                     
                                     
                                     

    @property
    def other_hands(self):
        "The list of other players' hands."
        return self.game.hands[1:]

    
    @property
    def other_players_cards(self):
        "All of other players's cards, concatenated in a single list."
        return list(itertools.chain.from_iterable([hand.cards for hand in self.other_hands]))

# FONCTION CLUE : elle donner l'indice a donne aux autres joueurs


    def clue(self,game,Somme_valeur,Valeur_joueurs,les_cartes_des_autres,nombre_de_joueurs,nombre_de_cartes):
            for i in range(nombre_de_joueurs-1): # On boucle sur les joueurs
                carte_a_jetee = [6,6] # Cartes de rang maximal que l'on puisse jetees (il y en a deux pour faire des comparaisons a chaque boucle)

                recommandation = 5 # On se place à la pire recommandation possible au début, à chaque iteration on peut l'ameliorer (i.e. la reduire)

                for k in range(nombre_de_cartes):   # On boucle sur la main d'un joueur
                
                    ki=k+i*nombre_de_cartes
                    carte_oscultee=les_cartes_des_autres[ki]

                    #Si le joueur a une carte 5 qui est jouable, il faut la jouer a tout prix, on est donc a la recommandation minimal 1

                    if game.piles[carte_oscultee.color]+1 == carte_oscultee.number and carte_oscultee.number == 5:
                        valeur_main = k
                        recommandation = 1

                    #Sinon on cherche dans la main du joueur une carte jouable de cout minimal

                    elif game.piles[carte_oscultee.color]+1 == carte_oscultee.number and carte_oscultee.number<carte_a_jetee[0] and recommandation >= 2:
                        valeur_main = k
                        carte_a_jetee[0] = carte_oscultee.number
                        recommandation = 2

                    #Sinon on cherche dans la main du joueur une carte morte et donc jetable

                    elif game.piles[carte_oscultee.color] >= carte_oscultee.number and recommandation > 3:
                        valeur_main = k + nombre_de_cartes
                        recommandation = 3

                    #On cherche a savoir si une carte de sa main est indispensable et donc injetable grace aux cartes deja defaussees

                    nombre_jetees=0
                    for jetees in game.discard_pile.cards:
                        if jetees == carte_oscultee:
                            nombre_jetees += 1

                    #Si le joueur ne possede pas non plus de carte morte, on lui indique de discard la carte non indispendable de rang le plus faible

                    if (nombre_jetees == game.deck.card_count[carte_oscultee.number]-1) and carte_oscultee.number > carte_a_jetee[1] and recommandation >= 4: 
                        valeur_main = k%nombre_de_cartes + nombre_de_cartes
                        carte_a_jetee[1] = carte_oscultee.number
                        recommandation = 4

                #Si la dernière recommandation n'est pas possible on passe a un defaussage de la première carte

                if recommandation == 5 :
                    valeur_main = nombre_de_cartes 
            
                
                Valeur_joueurs[i] = valeur_main # A chaque iteration sur i on connait la valeur de la main d'un des joueurs
                Somme_valeur += valeur_main

            return(Somme_valeur % (2*nombre_de_cartes)) #Somme_valeur permet de savoir quel indice il faut donner si on doit en donner un


# FONCTION CLUE_END : elle donne l'indice a donner aux autres joueurs au dernier tour, le dernier tour cree des cas particuliers sur certaines boucles d'ou la distinction

    def clue_end(self,game,Somme_valeur,Valeur_joueurs,les_cartes_des_autres,nombre_de_joueurs,nombre_de_cartes):
        
        tampon = hanabi.deck.Card(hanabi.deck.Color.Blue,-1) # Carte permettant de combler le manque de carte dans une main

        for i in range(nombre_de_joueurs-1):
            
            carte_a_jetee = [6,6]
            recommandation = 10 

            for k in range(nombre_de_cartes):
         
                ki=k+i*nombre_de_cartes
                carte_oscultee = les_cartes_des_autres[ki]
                if carte_oscultee != tampon: # le cas particulier ou on etudie une fausse carte tampon

              
                    if game.piles[carte_oscultee.color]+1 == carte_oscultee.number and carte_oscultee.number == 5:
                        valeur_main = k
                        recommandation = 1

                    elif game.piles[carte_oscultee.color]+1 == carte_oscultee.number and carte_oscultee.number<carte_a_jetee[0] and recommandation >= 2:
                        valeur_main = k
                        carte_a_jetee[0] = carte_oscultee.number
                        recommandation = 2

                 
                    elif game.piles[carte_oscultee.color] >= carte_oscultee.number and recommandation > 3:
                        valeur_main = k + nombre_de_cartes
                        recommandation = 3


                    nombre_jetees=0
                    for jetees in game.discard_pile.cards:
                        if jetees == carte_oscultee:
                            nombre_jetees += 1

                    
                    if (nombre_jetees == game.deck.card_count[carte_oscultee.number]-1) and carte_oscultee.number > carte_a_jetee[1] and recommandation >= 4: 
                        valeur_main = k + nombre_de_cartes
                        carte_a_jetee[1] = carte_oscultee.number
                        recommandation = 4
                else:
                    continue

            if recommandation == 10 :
                valeur_main = nombre_de_cartes 
                
            
            Valeur_joueurs[i] = valeur_main

            Somme_valeur += valeur_main

        return(Somme_valeur % (2*nombre_de_cartes))



#FONCTION AGIR : ELLE DONNE L'ACTION QUE LE JOUEUR DOIT EFFECTUER POUR RESPECTER LA STRATEGIE, CETTE ACTION EST DETERMINEE PAR LE DERNIER INDICE ET LES ACTIONS PRECEDENTES



    def agir(self,game,nombre_de_tours_passes_depuis_le_dernier_indice,nombre_de_joueurs,nombre_de_cartes,Valeur_joueurs,Somme_valeur,les_cartes_des_autres):

        if self.actions[nombre_de_tours_passes_depuis_le_dernier_indice] <= nombre_de_cartes and self.actions_depuis_le_dernier_indice[0]==0: ##Si la dernière signification_Somme_valeur indiquait de jouer une carte, qu'aucune carte n'a été jouée depuis que l'indice a été donné, jouer la carte
            self.actions_depuis_le_dernier_indice[0] += 1
            return('p%d'%self.actions[nombre_de_tours_passes_depuis_le_dernier_indice])
            

        elif self.actions[nombre_de_tours_passes_depuis_le_dernier_indice] <= nombre_de_cartes and self.actions_depuis_le_dernier_indice[0]==1 and game.red_coins<2 : #Si la dernière signification_Somme_valeur indiquait de jouer une carte, qu'une carte a été jouée depuis que l'indice a été donné et que les joueurs ont commis moins de deux erreurs, jouez la carte recommandée
            self.actions_depuis_le_dernier_indice[0]+=1
            return('p%d'%self.actions[nombre_de_tours_passes_depuis_le_dernier_indice])
            

        elif game.blue_coins > 0 : #S'il reste des jetons bleus, on donne l'indice determine à la premiere etape

            self.actions_depuis_le_dernier_indice=[0,0,Somme_valeur] 
            
            signification_Somme_valeur = self.recommandation_dictionnary[Somme_valeur]

            cible_de_clue=les_cartes_des_autres[signification_Somme_valeur[1]*nombre_de_cartes] 

            #On donne un indice au joueur considere, seul le type de l'indice importe dans cette strategie. 

            #L'indice et lui même est inutile, seul le fait qu'il soit un color hint ou un rank hint compte.

            if signification_Somme_valeur[0]=='rank':

                for j in range(nombre_de_joueurs-1):
                    dernier_indice = self.actions_depuis_le_dernier_indice[2] # Ceci est la Somme_valeur correspondant au dernier indice qui a ete calcule par clue
                    joueurs_vises_par_l_indice = [i for i in range(nombre_de_joueurs-1) if i != j] # Cette indice ne concerne pas le joueur qui va le donner
                    for i in joueurs_vises_par_l_indice: 
                        dernier_indice -= Valeur_joueurs[i] # On selectionne les joueurs concernees par le dernier indice et on met à jour leur Valeur, c'est ce que leur indique quoi faire
                    dernier_indice %= (2*nombre_de_cartes)# On fait attention au valeurs negatives
                    dernier_indice += 1
                    self.actions[j] = dernier_indice # On met a jour l'action du joueur

                return ('c{}{}'.format(cible_de_clue.number,self.list_players[signification_Somme_valeur[1]][0]))
            if signification_Somme_valeur[0]=='suit':

                for j in range(nombre_de_joueurs-1):
                    dernier_indice = self.actions_depuis_le_dernier_indice[2] # Ceci est la Somme_valeur correspondant au dernier indice qui a ete calcule par clue
                    joueurs_vises_par_l_indice = [i for i in range(nombre_de_joueurs-1) if i != j] # Cette indice ne concerne pas le joueur qui l'a donne
                    for i in joueurs_vises_par_l_indice: 
                        dernier_indice -= Valeur_joueurs[i] # On selectionne les joueurs concernees par le dernier indice et on met à jour leur Valeur, c'est ce que leur indique quoi faire
                    dernier_indice %= (2*nombre_de_cartes) # On fait attention au valeurs negatives
                    dernier_indice += 1
                    self.actions[j] = dernier_indice # On met a jour l'action du joueur

                return ('c{}{}'.format(str(cible_de_clue.color)[0],self.list_players[signification_Somme_valeur[1]][0])) #Le 
            
        elif self.actions[nombre_de_tours_passes_depuis_le_dernier_indice] > nombre_de_cartes : #Si on lui a recommande de jeter une carte, le joueur le fait 
            self.actions_depuis_le_dernier_indice[1]+=1
            return('d%d'%(self.actions[nombre_de_tours_passes_depuis_le_dernier_indice]-nombre_de_cartes))
            

        else : # Si aucune action n'était possible, on discard la carte de gauche par defaut
            self.actions_depuis_le_dernier_indice[1]+=1
            return('d1')


#FONCTION AGIR_END : ELLE DONNE L'ACTION QUE LE JOUEUR DOIT EFFECTUER POUR RESPECTER LA STRATEGIE, CETTE ACTION EST DETERMINEE PAR LE DERNIER INDICE ET LES ACTIONS PRECEDENTES

# C'est avec cette fonction qu'on gere l'ajout de carte pour combler les mains ayant moins de 3 cartes, l'algorithme reste quasiment le meme

    def agir_end(self,game,nombre_de_tours_passes_depuis_le_dernier_indice,nombre_de_joueurs,nombre_de_cartes,Valeur_joueurs,Somme_valeur,les_cartes_des_autres):
        
        tampon = hanabi.deck.Card(hanabi.deck.Color.Blue,-1) # Carte permettant de combler le manque de carte dans une main

        if self.actions[nombre_de_tours_passes_depuis_le_dernier_indice] <= nombre_de_cartes and self.actions_depuis_le_dernier_indice[0]==0: 
                self.actions_depuis_le_dernier_indice[0] += 1
                game.current_hand.cards.append(tampon) # Comme le nombre de carte est fixe dans l'algorithme on utilise un "tampon" pour eviter d'avoir a calculer le nombre de carte dans une main a chaque fois
                #C'est plus efficace au niveau des calculs
                return('p%d'%self.actions[nombre_de_tours_passes_depuis_le_dernier_indice])
                

        elif self.actions[nombre_de_tours_passes_depuis_le_dernier_indice] <= nombre_de_cartes and self.actions_depuis_le_dernier_indice[0]==1 :#and :game.red_coins<2:
            self.actions_depuis_le_dernier_indice[0]+=1
            game.current_hand.cards.append(tampon) # tampon
            return('p%d'%self.actions[nombre_de_tours_passes_depuis_le_dernier_indice])
            
        
        elif game.blue_coins > 0 : 
            self.actions_depuis_le_dernier_indice=[0,0,Somme_valeur]
            signification_Somme_valeur = self.recommandation_dictionnary[Somme_valeur]

            card_to_hint=les_cartes_des_autres[signification_Somme_valeur[1]*nombre_de_cartes] 
            if signification_Somme_valeur[0]=='rank':

                for j in range(nombre_de_joueurs-1):
                    dernier_indice = self.actions_depuis_le_dernier_indice[2]
                    joueur_vises_par_l_indice = [i for i in range(nombre_de_joueurs-1) if i != j]
                    for i in joueur_vises_par_l_indice: 
                        dernier_indice -= Valeur_joueurs[i]
                    dernier_indice %= (2*nombre_de_cartes)
                    dernier_indice += 1
                    self.actions[j] = dernier_indice

                return ('c{}{}'.format(card_to_hint.number,self.list_players[signification_Somme_valeur[1]][0]))
            if signification_Somme_valeur[0]=='suit':

                for j in range(nombre_de_joueurs-1):
                    dernier_indice = self.actions_depuis_le_dernier_indice[2]
                    joueur_vises_par_l_indice = [i for i in range(nombre_de_joueurs-1) if i != j]
                    for i in joueur_vises_par_l_indice: 
                        dernier_indice -= Valeur_joueurs[i]
                    dernier_indice %= (2*nombre_de_cartes)
                    dernier_indice += 1
                    self.actions[j] = dernier_indice

                return ('c{}{}'.format(str(card_to_hint.color)[0],self.list_players[signification_Somme_valeur[1]][0]))
            
        elif self.actions[nombre_de_tours_passes_depuis_le_dernier_indice] > nombre_de_cartes : 
            self.actions_depuis_le_dernier_indice[1]+=1
            game.current_hand.cards.append(tampon) 
            return('d%d'%(self.actions[nombre_de_tours_passes_depuis_le_dernier_indice]-nombre_de_cartes))
            
        
        else : 
            self.actions_depuis_le_dernier_indice[1]+=1
            game.current_hand.cards.append(tampon) 
            return('d1')


#La Fonction PLAY fait jouer l'IA, on alterne simplement les deux etapes de l'algorithme indice/action ==> indice/action ==> etc.

    def play(self):
        game = self.game

        self.list_players = self.list_players[1:]+[self.list_players[0]] # On change les noms des joueurs à chaque tour de jeu
        
        #Il faudra attribuer à chaque main parcourue un nombre entre 0 et 7 pour trouver l'indice a donner


        les_cartes_des_autres = [card for card in self.other_players_cards] #carte des autres joueurs vus par le joueur dont c'est au tour de jouer

        nombre_de_joueurs = len(game.players) # nombre de joueurs

        nombre_de_cartes = game.deck.cards_by_player[nombre_de_joueurs] # nombre de carte par joueurs en fonction du nombre de joueurs total


        if len(game.deck.cards) != 0: # LA PIOCHE EST ENCORE POSSIBLE
        
                  
            #DETERMINATION DE L'INDICE

            #Somme_valeur est la somme des couleurs (ou chapeau) des autres joueurs, elle permet de savoir quel indice donne
            
            #Pour trouver Somme_valeur on doit evaluer les mains de chaque joueurs, on se sert de les_cartes_des_autres qui contient dans l'ordre les cartes des autres joueurs dans l'ordre

            Somme_valeur=0
            Valeur_joueurs = [0] * (nombre_de_joueurs-1)
            Somme_valeur=self.clue(game,Somme_valeur,Valeur_joueurs,les_cartes_des_autres,nombre_de_joueurs,nombre_de_cartes)
            
            # DETERMINATION DE L'ACTION A EFFECTUER

            nombre_de_tours_passes_depuis_le_dernier_indice = self.actions_depuis_le_dernier_indice[0]+self.actions_depuis_le_dernier_indice[1] # Ce calcul est necessaire pour determiner certaines actions
            return(self.agir(game,nombre_de_tours_passes_depuis_le_dernier_indice,nombre_de_joueurs,nombre_de_cartes,Valeur_joueurs,Somme_valeur,les_cartes_des_autres))

        # PLUS DE CARTE DANS LA PIOCHE

        else :

            #DETERMINATION DE L'INDICE

            Somme_valeur=0
            Valeur_joueurs = [0] * (nombre_de_joueurs-1)
            Somme_valeur = self.clue_end(game,Somme_valeur,Valeur_joueurs,les_cartes_des_autres,nombre_de_joueurs,nombre_de_cartes)

            # DETERMINATION DE L'ACTION A EFFECTUER

            nombre_de_tours_passes_depuis_le_dernier_indice = self.actions_depuis_le_dernier_indice[0]+self.actions_depuis_le_dernier_indice[1]# Ce calcul est necessaire pour determiner certaines actions
            return(self.agir_end(game,nombre_de_tours_passes_depuis_le_dernier_indice,nombre_de_joueurs,nombre_de_cartes,Valeur_joueurs,Somme_valeur,les_cartes_des_autres))