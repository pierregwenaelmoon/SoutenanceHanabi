import unittest
import hanabi



class ColorTest(unittest.TestCase):
    def test_str(self):
        colors=[(31,"Red"),(32,"Green"),(34,"Blue"),(33,"Yellow"),(37,"White")]
        trouve=True
        for (c,color) in colors:
            a=str(hanabi.deck.Color(c))
            self.assertEqual(a,color)
    def test_valid(self):
        for s in (54,78,46,54,-5,3):
            self.assertRaises(ValueError, hanabi.deck.Color, s)


class CardTest(unittest.TestCase):
    def test_not_equaled_cards(self):
        c1=hanabi.deck.Card('B',4)
        c2=hanabi.deck.Card('R',4)
        self.assertNotEqual(c1,c2)

    def test_equal(self):
        c1=hanabi.deck.Card('R',4)
        string_card="R4"
        self.assertEqual(c1,string_card)

    def test_number(self):
        #self.assertRaises(hanabi.deck.Card('R',7), AssertionError)
        with self.assertRaises(AssertionError):
            hanabi.deck.Card('R',7)

class HandTest(unittest.TestCase):
    # test __special__ functions
    

    # test normal functions
    pass

class DeckTest(unittest.TestCase):
    # test __special__ functions
    

    # test normal functions
class DeckTest(unittest.TestCase):
    def setUp(self):
        pass


    def test_shuffle(self):
        Paquet = hanabi.Deck()
        b=0
        Paquet_aux = hanabi.Deck()
        Paquet_aux.cards = Paquet.cards
        
        for k in range(10): 
            
            # On test si sur 10 mélange le deck est bien différent au moins 2 fois

            Paquet_aux.cards = Paquet.cards
            Paquet.shuffle()
            if Paquet!=Paquet_aux:
                b+=1
        self.assertTrue(b>2)

    def test_draw(self):

        # On teste si la carte piochée est la bonne et si le deck a bien été délesté d'une carte

        Paquet = hanabi.Deck()
        Paquet.shuffle()
        LaCarte = Paquet.cards[0]
        nombre_cartes = len(Paquet.cards)
        LaCarte2 = Paquet.draw()
        self.assertEqual(len(Paquet.cards),nombre_cartes-1)
        self.assertEqual(LaCarte,LaCarte2)


    def test_deal(self):

        #On test si le nombre de carte par main est le bon pour 5, 4 et 3 et si les mains retournées sont de la classe Hand

        Paquet = hanabi.Deck()
        Hands = Paquet.deal(5)
        b = True
        for x in Hands:
            self.assertTrue(isinstance(x,hanabi.deck.Hand))
            if len(x)!=4:
                b = False
        self.assertEqual(b,True)
        
        Paquet = hanabi.Deck()        
        Hands = Paquet.deal(3)
        b = True
        for x in Hands:
            self.assertTrue(isinstance(x,hanabi.deck.Hand))
            if len(x)!=5:
                b = False
        self.assertEqual(b,True)
         
        Paquet = hanabi.Deck() 
        Hands = Paquet.deal(4)
        
        b = True
        for x in Hands:
            self.assertTrue(isinstance(x,hanabi.deck.Hand))
            if len(x)!=4:
                b = False
        self.assertEqual(b,True)


    pass



class GameTest(unittest.TestCase):

    def setUp(self):
        self.unshuffled_game = hanabi.Game()
        self.random_game = hanabi.Game()
        # ... group G here! 
        self.predefined_game = hanabi.Game()
        # ...


    # lines 193, 227
    def test_A1(self):
        pass

    # lines 227, 261
    def test_B1(self):
        pass


    # lines 261, 295


    # lines 295, 329


    # lines 329, 363


    # lines 363, 397


    # lines 397, 431


    pass



if __name__ == '__main__':
    unittest.main()
