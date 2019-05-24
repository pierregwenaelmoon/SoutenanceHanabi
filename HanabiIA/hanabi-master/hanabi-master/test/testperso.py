import unittest
import hanabi
import hanabi.ai as my_ai



class EndGameTest(unittest.TestCase):
	#We will check if the game ends when it has to end :
	# We have 2 different cases : 
	# 		- 3 red coins
	#		- Deck vide
	
	def testfin(self):

		game = hanabi.Game(5) 
		ai = my_ai.HatGuessIA(game)
		game.ai = ai
		game.quiet = True
		game.run()

		verif = False #Si la variable reste à False c'est que le jeu s'arrete sans raison valable.

		if game.red_coins==3 or len(game.deck)==0:
			verif = True

		self.assertEqual(verif,True)
			


if __name__ == '__main__':
    unittest.main()
