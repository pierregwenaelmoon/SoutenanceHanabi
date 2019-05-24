"""
Artificial Intelligence to play Hanabi.
"""
import hanabi
import itertools

class AI:
    """
    AI base class: some basic functions, game analysis.
    """
    def __init__(self, game):
        self.game = game

    @property
    def other_hands(self):
        "The list of other players' hands."
        return self.game.hands[1:]

    @property
    def other_players_cards(self):
        "All of other players's cards, concatenated in a single list."
        #return sum([x.cards for x in self.other_hands], [])
        return list(itertools.chain.from_iterable([hand.cards for hand in self.other_hands]))

        
class Cheater(AI):
    """
    This player can see his own cards!

    Algorithm:
      * if 1-or-more card is playable: play the lowest one, then newest one
      * if blue_coin<8 and an unnecessary card present: discard it.
      * if blue_coin>0: give a clue on precious card (so a human can play with a Cheater)
      * if blue_coin<8: discard the largest one, except if it's the last of its kind or in chop position in his opponent.
    """

    def play(self):
        "Return the best cheater action."
        game = self.game
        playable = [ (i+1, card.number) for (i,card) in
                     enumerate(game.current_hand.cards)
                     if game.piles[card.color]+1 == card.number ]

        if playable:
            # sort by ascending number, then newest
            playable.sort(key=lambda p: (p[1], -p[0]))
            print ('Cheater would play:', "p%d"%playable[0][0], end=' ')
            if (len(playable)>1):
                print('but could also pick:', playable[1:])
            else: print()

            return "p%d"%playable[0][0]


        discardable = [ i+1 for (i,card) in
                        enumerate(game.current_hand.cards)
                        if ( (card.number <= game.piles[card.color])
                             or (game.current_hand.cards.count(card)>1)
                        ) ]
        # discard already played cards, doubles in my hand
        # fixme: discard doubles, if I see it in partner's hand
        # fixme: il me manque les cartes sup d'une pile morte

        if discardable and (game.blue_coins<8):
            print ('Cheater would discard:', "d%d"%discardable[0], discardable)
            return "d%d"%discardable[0]

        ## 2nd type of discard: I have a card, and my partner too
        
        discardable2 = [ i+1 for (i,card) in enumerate(game.current_hand.cards)
                         if card in self.other_players_cards
                       ]
        if discardable2 and (game.blue_coins<8):
            print ('Cheater would discard2:', "d%d"%discardable2[0], discardable2)
            return "d%d"%discardable2[0]


        ## Look at precious cards in other hand, to clue them
        precious = [ card for card in
                     self.other_players_cards
                     if (1+game.discard_pile.cards.count(card))
                         == game.deck.card_count[card.number]
                   ]
        if precious:
            clue = False
            # this loop is such that we prefer to clue an card close to chop
            # would be nice to clue an unclued first, instead of a already clued
            for p in precious:
                #print (p, p.number_clue, p.color_clue)
                if p.number_clue is False:
                    clue = "c%d"%p.number
                    break
                if p.color_clue is False:
                    clue = "c%s"%p.color
                    clue = clue[:2]   # quick fix, with 3+ players, can't clue cRed anymore, only cR
                    break
                # this one was tricky:
                # don't want to give twice the same clue
            if clue:
                print ('Cheater would clue a precious:',
                       clue, precious)
                if game.blue_coins>0:
                    return clue
                print ("... but there's no blue coin left!")


        # if reach here, can't play, can't discard safely, no card to clue-save
        # Let's give a random clue, to see if partner can unblock me
        if game.blue_coins >0:
            print ('Cheater would clue randomly: cW')
            return 'cw'

        # If reach here, can't play, can't discard safely
        # No blue-coin left.
        # Must discard a card. Let's choose a non-precious one (preferably a 4)
        mynotprecious = [ (card.number,i+1) for (i,card) in
                          enumerate(game.current_hand.cards)
                          if not (
                                  (1+game.discard_pile.cards.count(card))
                                  == game.deck.card_count[card.number])
                     ]
        mynotprecious.sort(key=lambda p: (-p[0], p[1]))
        if mynotprecious:
            act = 'd%d'%mynotprecious[0][1]
            print('Cheater is trapped and must discard:', act, mynotprecious)
            return act

        # Oh boy, not even a safe discard, this is gonna hurt!
        # it's a loss. Discard the biggest
        myprecious = [ (card.number,i+1) for (i,card) in enumerate(game.current_hand.cards) ]
        myprecious.sort(key=lambda p: (-p[0], p[1]))
        act = 'd%d'%myprecious[0][1]
        print('Cheater is doomed and must discard:', act, myprecious)
        return actgexit



# Mon IA #

"""
Artificial Intelligence to play Hanabi.
"""




class HatGuessIA(AI):
    """
    Cette intelligence artificielle repose sur l'algorithme du choix de chapeau. L'idée est simple, la mise en pratique
    compliquée. L'intelligence artificielle va donner un indice à un joueur et grace à cet indice elle indiquera en fait 
    à tous les joueurs quoi faire.

    Se référer au fichier joint pour comprendre l'algorithme ainsi que la manière dont il a été mis en place.

    """
    def SearchPlayableCards(self,game) : 
        #game = self.game
        #PlayableCardsTmp = [ (i+1, card.number) for (i,card) in
                     #enumerate(game.current_hand.cards)
                     #if game.piles[card.color]+1 == card.number ]
        red = hanabi.deck.Card(hanabi.deck.Color.Red,2)
        blue = hanabi.deck.Card(hanabi.deck.Color.Blue,2)
        yellow = hanabi.deck.Card(hanabi.deck.Color.Yellow,2)
        green = hanabi.deck.Card(hanabi.deck.Color.Green,2)
        white = hanabi.deck.Card(hanabi.deck.Color.White,2)
        piles = game.piles
        echantillon = [red.color,blue.color,green.color,yellow.color,white.color]
        PlayableCardsTmp =[]
        for c in echantillon:
            if piles[c]<5:
                carte_jouable = hanabi.deck.Card(c,piles[c]+1)
                PlayableCardsTmp.append(carte_jouable)
        return(PlayableCardsTmp)

    def SearchFive(self,game) :
        # Dans chaque main : on cherche les 5 tant qu'on a pas trouvé et qu'on a pas parcouru. On regarde si la
        # carte est dans game.PlayableCards
        FiveHandsTmp=[None,None,None,None,None]
        Mains = game.hands
        for loop in range (len(Mains)):
            MainTmp = Mains[loop]
            CartesTmp = MainTmp.cards
            for i in range (len(CartesTmp)):
                if CartesTmp[i].number == 5 :
                    if CartesTmp[i] in game.PlayableCards :
                        FiveHandsTmp[loop] = [ i , CartesTmp[i].color ]
                        break
        return(FiveHandsTmp)

    def SearchSmallestPlayable(self,game) : 
        #Fonction qui cherche la plus petite carte jouable dans chaque main#
        SmallestPlayableTmp = [None,None,None,None,None]
        Mains = game.hands
        for loop in range (len((Mains))):
            MainTmp = Mains[loop]
            CartesTmp = MainTmp.cards
            SmallestCarteTmp = None  # Plus petite carte de la main oscultée. #
            PosSmallestTmp = None
            for i in range (len(CartesTmp)) : 
                if CartesTmp[i] in game.PlayableCards :
                    if (SmallestCarteTmp == None) :
                        SmallestCarteTmp = CartesTmp[i]
                        PosSmallestTmp = i
                    elif ( CartesTmp[i].number < SmallestCarteTmp.number ):
                        SmallestCarteTmp = CartesTmp[i]
                        PosSmallestTmp = i
            if SmallestCarteTmp != None :
                SmallestPlayableTmp[loop] = [SmallestCarteTmp , PosSmallestTmp]
        return(SmallestPlayableTmp)

    def CalculScoreTot(self,game):
        #Calcul du score total vu par chaque main :
        NbJoueurs = 5
        ScoreTotTmp=[None,None,None,None,None]
        for loop in range (NbJoueurs) :
            ScoreTotTmp[loop] = sum(game.ScoreHands) - (game.ScoreHands[loop])
        return(ScoreTotTmp)

    def AjoutIndice(self,game):
        #Determination du type d'indice, du donneur et du receveur.
        ScoreVu = game.ScoreTotMod8[0] 
        TypeHint = None
        if 0<=ScoreVu<=3 :
            TypeHint = 'Rank' 
        elif 4<=ScoreVu<=7 :
            TypeHint = 'Suit'

        #Trouver le nom du donneur#
        Donneur = game.players[game.current_player]
        InitialeDonneur = Donneur[0]
        #On joue avec des joueurs qui commence par la lettre A,B,C, D et E donc on en déduit 
        #qui est le receveur en trouvant la lettre initiale du donneur.
        ListeLettre = ['A','B','C','D','E']
        PosDonneurLet = ListeLettre.index(InitialeDonneur)

        #On regarde qui ça concerne : joueur 1 à ma gauche, joueur 2 ...

        Concerne = None
        if 0<=ScoreVu<=3 :
            Concerne = ScoreVu
        elif 4<=ScoreVu<=7 :
            Concerne = ScoreVu%4
        InitialeReceveur = ListeLettre[(Concerne + PosDonneurLet)%5]
        #On déduit le nom du receveur : #

        Receveurs = {"A":'Benji',"B":'Clara',"C":'Dante',"D":'Elric',"E":'Alice',}
        Receveur = Receveurs[InitialeReceveur]
        (game.Indices).append( [ Donneur , Receveur , TypeHint ] )
        return([Donneur , Receveur , TypeHint])

    
    def DonnerIndice(self,gamee):
        #Fonction qui calcule le score de chaque main pour déterminer le type d'indice.
        game = gamee
        NbJoueurs = 5
        for loop in range(NbJoueurs):
            MainOscultee=game.hands[loop]
            game.PlayableCards = self.SearchPlayableCards(game)
            game.FiveHands = self.SearchFive(game)

            if game.FiveHands[loop]!=None:
                PositionDuFive= game.FiveHands[loop][0]
                game.ScoreHands[loop] = PositionDuFive

            else : 
            #Si on arrive là c'est qu'on a pas trouvé de 5 jouable #
                #On cherche la plus petite carte jouable : on met tout à jour pour toutes les mains.
                game.SmallestPlayable  = self.SearchSmallestPlayable(game)
                if game.SmallestPlayable[loop]!=None:
                    game.ScoreHands[loop] = game.SmallestPlayable[loop][1]

                else :
                    #Si on arrive là c'est qu'on a pas de cartes jouables dans la main. O
                    # On cherche alors une carte à discard en regardant si les cartes de la main
                    # ne sont pas déjà posées sur la table 
                    DiscardTmp = None
                    piles = game.piles
                    IndxDiscardTmp = None
                    for j in range(len(MainOscultee.cards)):
                        #Color_ref = MainOscultee.cards[j].color
                        if MainOscultee.cards[j].number <= piles[MainOscultee.cards[j].color]:
                            DiscardTmp = MainOscultee.cards[j]
                            IndxDiscardTmp = j  #Position dans la main de la carte à discard.
                            break
                    if DiscardTmp != None :
                        game.ScoreHands[loop] = IndxDiscardTmp+4  #On discard donc ça correspond aux chiffres de 4 à 7#

                    else : 
                        #Si on arrive là c'est qu'on va devoir discard une carte non indispensable à la réussite du jeu. On discard celle avec le plus haut rang#
                        DiscardNonIndisp = None
                        IndxDiscardNonIndisp = None
                        MaxCarteNon = -1
                        pioche = (game.deck).cards
                        for j in range(len(MainOscultee.cards)) : 
                            if MainOscultee.cards[j] in pioche and MainOscultee.cards[j].number > MaxCarteNon :
                                DiscardNonIndisp = MainOscultee.cards[j]
                                IndxDiscardNonIndisp = j
                                MaxCarteNon = MainOscultee.cards[j].number
                        if DiscardNonIndisp != None :
                            game.ScoreHands[loop] = IndxDiscardNonIndisp+4
                        else :
                            #Si on arrive là c'est qu'on doit discard la première carte
                            game.ScoreHands[loop] = 4
                # On a maintenant le score de toutes les mains # 
        # on va calculer le score vu par la main i : ième position dans la liste ScoreTot
        game.ScoreTot = self.CalculScoreTot(game)
        # On calcule ScoreTot modulo 8 # 
        game.ScoreTotMod8 = [i%8 for i in game.ScoreTot]
        #On détermine quel indice donner et à qui le donner.
        IndiceTogive = self.AjoutIndice(game) #Fonction qui ajoute à game.Indices l'indice déterminé.
        DonneurTmp = IndiceTogive[0]
        ReceveurTmp = IndiceTogive[1]
        TypeHintTmp = IndiceTogive[2]
        FirstLetterRecev = ReceveurTmp[0]
        FirstLetterDonn = DonneurTmp[0]

        #On donne un indice au hasard qui correspond au type trouvé. Si c'est Suit : R. Si c'est rank : 2.
        if TypeHintTmp == 'Suit':
            HintTmp = 'R'
            
        elif TypeHintTmp == 'Rank':
            HintTmp = '2'

        #On remet à 0 la variable MoveSinceLast
        game.PlaySinceLast = 0
        #On remplit le dictionnaire des scores 
        #On détermine d'abord qui on est puis on remplit dans l'ordre : 
        PosDonneurs = {"A":0,"B":1,"C":2,"D":3,"E":4}
        PosDonneurDico = PosDonneurs[DonneurTmp[0]]
       
        noms = ['Alice','Benji','Clara','Dante','Elric']
        for loop in range(5) :
            NomTmp = noms[(loop + PosDonneurDico)%5]
            game.ScoreDicoHands[NomTmp] = game.ScoreHands[loop]
        #On donne l'indice :
        res = 'c'+HintTmp+FirstLetterRecev
        return(res)

    def play(self):
        game=self.game
        #Si il s'agit du premier joueur on donne un indice : on regarde la taille de game.moves#
        if len(game.move)==0:  #C'est que c'est le 1er joueur qui va jouer#
            TmpIndice = self.DonnerIndice(game)
            (game.move).append(["c",2])
            game.PlaySinceLast = 0
            return(TmpIndice)
        else : 
            Actuel = game.players[game.current_player]
            MyGuessedScore = game.ScoreDicoHands[Actuel]

            if MyGuessedScore <=3 and MyGuessedScore>=0 :
                WhatIGuessed = 'play'

            elif MyGuessedScore <=7 and MyGuessedScore>=4 :
                WhatIGuessed = 'discard'
            
            if WhatIGuessed == 'play' and game.PlaySinceLast==0:
                NbPlay = game.PlaySinceLast
                if NbPlay == 0 :
                         #On joue la carte qu'on a deviné. 
                        PlaceCarteToPlay = MyGuessedScore + 1
                        (game.move).append(["p",PlaceCarteToPlay])
                        game.PlaySinceLast = game.PlaySinceLast + 1
                        return("p"+str(PlaceCarteToPlay))

            elif WhatIGuessed == 'play' and game.PlaySinceLast==1 and (game.red_coins<2):
                #On va compter le nombre de fois que des cartes ont été jouées depuis le dernier indice donné.
                NbPlay = game.PlaySinceLast

                if (NbPlay == 1) :
                    #On vérifie qu'il y a bien moins de 2 erreurs qui ont été commises.
                    #if game.red_coins <=2 :
                    PlaceCarteToPlay = MyGuessedScore + 1   #L'indice de la première carte est 1.
                    (game.move).append(["p",PlaceCarteToPlay])
                    game.PlaySinceLast = game.PlaySinceLast + 1
                    return("p"+str(PlaceCarteToPlay))

            elif game.blue_coins > 0:  #On donne un indice#
                IndiceTmpp = self.DonnerIndice(game)
                (game.move).append(["c",2])
                game.PlaySinceLast = 0
                return(IndiceTmpp)

            else : 
                #On discard la carte que l'on a deviné#
                if WhatIGuessed == "discard" :
                    PlaceCarteToDiscard = MyGuessedScore - 4 + 1
                    (game.move).append(["d",PlaceCarteToDiscard])
                    return("d"+str(PlaceCarteToDiscard))
                else :
                    #On discard la carte à la plus petite position#
                    (game.move).append(["d",1])
                    return("d"+"1")