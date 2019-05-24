import hanabi
import hanabi.ai
import statistics as stat
import hanabi.ai as new_ai
import time as t
game = hanabi.Game(5) 
ai = new_ai.HatGuessIA(game)
game.ai = ai




def n_tests(game,n):
    t1 = t.time()
    L=[]
    compteur = 0
    compteur_2 = 0
    for i in range(n):
        
        game.reset()
        game=hanabi.Game(5)
        game.quiet=True
        ai = new_ai.HatGuessIA(game)
        game.ai = ai
        game.run()
        L.append(game.score)
        if game.score >=24:
            compteur+=1
        if game.score >=25:
            compteur_2 +=1
    Moyenne = stat.mean(L)
    Variance = stat.variance(L)

    print(L,"\nMoyenne = ",Moyenne," and Variance = ",Variance," Nombre de partie à plus de 24 coups = ",compteur," Nombre de partie à 25 coups = ",compteur_2)
    t2 = t.time()
    print("Temps de Calcul pour ",n," parties = ",t2-t1," secondes")
