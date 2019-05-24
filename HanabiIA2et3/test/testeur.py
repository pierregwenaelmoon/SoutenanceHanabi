import hanabi
import hanabi.ai
import statistics as stat
import hanabi.un_ai2 as new_ai
import time as t
game = hanabi.Game(5) 
ai = new_ai.Recommander(game)
game.ai = ai
import matplotlib.pyplot as plt



def n_tests(game,n):
    t1 = t.time()
    L=[]
    compteur = 0
    compteur_2 = 0
    for i in range(n):
        
        game.reset()
        game=hanabi.Game(5)
        game.quiet=True
        ai = new_ai.Recommander(game)
        game.ai = ai
        game.run()
        L.append(game.score)
        if game.score >=21:
            compteur+=1
        if game.score >=25:
            compteur_2 +=1
    Moyenne = stat.mean(L)
    Variance = stat.variance(L)

    print(L,"\nMoyenne = ",Moyenne," and Variance = ",Variance," Nombre de partie à plus de 24 coups = ",compteur," Nombre de partie à 25 coups = ",compteur_2)
    t2 = t.time()
    print("Temps de Calcul pour ",n," parties = ",t2-t1," secondes")
    plt.hist(L,rwidth=0.4,edgecolor='black',align='left',bins=[i for i in range(15,27)],normed=1)
    V=str(Variance)
    m=str(Moyenne)
    plt.title("Résultats pour "+str(n)+" parties avec stratégie risquée \n\n"+"V = "+V + " et m = "+m+ "\n"+str(compteur_2/n)+str('%')+" de parties à 25 coups"+ "\n"+str(compteur/n)+str('%')+" de parties à plus de 21 coups" )

    plt.show()
