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

		if game.red_coins==3 or len(game.deck.cards)==0:
			verif = True

		self.assertEqual(verif,True)
			

class TypeOfRes(unittest.TestCase):
	#We will check if the type of the result is what we expect it to be.

	def testType(self):

		game = hanabi.Game(5) 
		ai = my_ai.HatGuessIA(game)
		game.ai = ai
		res = ai.play()
		print()
		print(res)
		print()
		verif = True #Tant que verif est True, le test est valide.

		if res[0]!='p' and res[0]!='c' and res[0]!=p :
			verif = False
		if len(res)>3:
			verif = False
		self.assertEqual(verif,True)






if __name__ == '__main__':
    unittest.main()
