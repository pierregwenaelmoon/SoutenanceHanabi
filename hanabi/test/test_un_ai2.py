import unittest
import hanabi.ai
import hanabi
import hanabi.un_ai2 as new_ai
import itertools


from hanabi.ai import AI 

class Test_un_ai2(unittest.TestCase):
    def setUp(self):
        pass
        

#On teste clue et agir sur un exemple pour lequel on a pris soin de faire le calcul de l'indice et l'action mentalement

    def test_clue_and_agir(self):
        game = hanabi.Game(5)

        ai = new_ai.Recommander(game)
        
        carte=hanabi.deck.Card(hanabi.deck.Color.Red,1)  # des cartes pour tester
        carte2=hanabi.deck.Card(hanabi.deck.Color.Red,2)
        carte3=hanabi.deck.Card(hanabi.deck.Color.Red,3)
        carte4=hanabi.deck.Card(hanabi.deck.Color.Red,4)
        carte5=hanabi.deck.Card(hanabi.deck.Color.Red,5)

        cartes=[carte,carte2,carte3,carte4,carte5]
        for k in range(0,5):
            for i in range(0,4):
                game.hands[k].cards[i]=cartes[k]
        
        game.hands[4].cards[2]=carte2
        game.hands[3].cards[3]=carte

        print(game.hands)
        print(game.deck)
        game.print_piles()
        ai.list_players = ai.list_players[1:]+[ai.list_players[0]]
        Valeur_joueurs = [0]*4
        Somme_valeur = 0
        print(game.current_player_name)

        self.assertEqual(ai.clue(game,Somme_valeur,Valeur_joueurs,[card for card in ai.other_players_cards],5,4),7)
        self.assertEqual(ai.agir(game,0,5,4,Valeur_joueurs,Somme_valeur,[card for card in ai.other_players_cards]),'c2B')
        

if __name__ == '__main__':
    unittest.main()
    


