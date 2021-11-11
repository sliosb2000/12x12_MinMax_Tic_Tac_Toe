# -*- coding: utf-8 -*-
"""
Created on Tue May 18 16:43:06 2021

@author: SLIOSBERG Benjamin

This program program was written during an IAvsIA competition, We won the 2nd place of the tournament 
This program was written in french, the variables and functions names are mostly in French, the comments have been translated for a better understanding
A TicTacToe is called a Morpion in French
"""

import random as rd
import numpy as np

IA='X'
Joueur = 'O'
    

def Actions(s):
    L = np.shape(s)[0]
    return ([(i,j) for i in range(L) for j in range(L) if s[i,j]=='.'])
def TerminalTest(s,j):
    t = np.shape(s)[0]
    for i in range(t):
        if VerifFinal([s[i,j] for j in range(t)], j):
            return True
        elif VerifFinal([s[j,i] for j in range(t)], j):
            return True
        elif VerifFinal(list(s.diagonal(i)), j):
            return True
        elif VerifFinal(list(s.diagonal(-i)), j):
            return True
        elif VerifFinal(list(np.fliplr(s).diagonal(i)), j):
            return True
        elif VerifFinal(list(np.fliplr(s).diagonal(-i)), j):
            return True
    return False

def Result(s, a, j):
    s[a[0], a[1]] = j
    return s

def VerifFinal(a,j):
    for i in range(len(a) - 3):
        if all(x == j for x in a[i:i + 4]): 
            return True
    return False
def VerifLigne(a,l,j,borne):
    r = 0
    for i in range(1, len(a) - l ):
        if borne :
            if all(x == j for x in a[i:i+l]) and a[i-1] == '.' and a[i+l] == '.':    
                r += 1
        else:       
            if all(x == j for x in a[i:i+l]) and ((a[i-1] == '.' and a[i+l] != '.') or (a[i+l] == '.' and a[i-1] != '.')):        
                r += 1
    return r
def VerifPion(a,j):
    for i in range(1, len(a) - 3):
        if a[i] == a[i+2] == j and a[i-1] == a[i+1] == a[i+3] == '.':
            return 1
    return 0
def temps(fonction):
    import time
    def inner(*param,**param2):
        start = time.time()
        retval = fonction(*param, **param2)
        end = time.time()
        temps = end - start
        print('Time:', float(temps), 's')
        return retval
    return inner

def Utility(s,j,z1,z2,z3,z4):                                       #this utility function takes the values of the next move the IA can do 
    score = 0                                                       #and substracts the value of the next possible moves from the player 
    if TerminalTest(s, j):                                          #=> if the player can finish during the next turn, the IA will prioritize blocking the player (if the IA can't finish next turn)
        return 10000
    for i in range(np.shape(s)[0]):
        l = s[i,:]
        c = s[:,i]
        d1 = s.diagonal(i)
        d2 = np.fliplr(s).diagonal(i)
        d1bis = s.diagonal(-i)
        d2bis = np.fliplr(s).diagonal(-i)
        score += VerifLigne(l, 2, j, True)*z1         
        score += VerifLigne(l, 3, j, False)*z2
        score += VerifLigne(l, 3, j, True)*z3
        score += VerifPion(l, j)*z4 
        score += VerifLigne(c, 2, j, True)*z1         
        score += VerifLigne(c, 3, j, False)*z2
        score += VerifLigne(c, 3, j, True)*z3
        score += VerifPion(c, j)*z4
        score += VerifLigne(d1, 2, j, True)*z1        
        score += VerifLigne(d1, 3, j, False)*z2
        score += VerifLigne(d1, 3, j, True)*z3   
        score += VerifPion(d1, j)*z4         
        score += VerifLigne(d2, 2, j, True)*z1          
        score += VerifLigne(d2, 3, j, False)*z2
        score += VerifLigne(d2, 3, j, True)*z3      
        score += VerifPion(d2, j)*z4

        if i != 0:
            score += VerifLigne(d1bis, 2, j, True)*z1          
            score += VerifLigne(d1bis, 3, j, False)*z2
            score += VerifLigne(d1bis, 3, j, True)*z3
            score += VerifPion(d1bis, j)*z4
            score += VerifLigne(d2bis, 2, j, True)*z1         
            score += VerifLigne(d2bis, 3, j, False)*z2
            score += VerifLigne(d2bis, 3, j, True)*z3
            score += VerifPion(d2bis, j)*z4 

    return score

def ActionsPerdantes(s, joueur):
    actions = []
    for i in range(12):
        for j in range(12):
            if s[i, j] == '.':
                s[i, j] = joueur
                if Utility(s) == -2 or Utility(s) == 0:
                    actions.append((i, j))
                s[i, j] = '.'
    return actions


def Grille(s, act = None):                                                     #printing the Game Grid
    print()
    print('   1  2  3  4  5  6  7  8  9  10 11 12')
    for i in range(12):
        if i < 9: print(i+1, end = '  ')
        else :print(i+1, end = ' ')

        for j in range(12):
            print(s[i, j], end = '  ')
        print()
    print('\n\n')

def MinMax(s,depth,maximum = True,alpha = float('-inf'), beta = float('inf')): #The minmax algorithm uses the utility function to chose a next bet move for the IA. 
    if depth == 0 or TerminalTest(s,Joueur) or TerminalTest(s,IA):
        return(Utility(s,IA,2,5,10,3)-Utility(s,Joueur,4.5,12.5,25,6))         #the parameters are  set arbitrarely with the IA's parameters lower than the Player since the player plays after the IA
    if maximum:                                                                #this enables to favorise blocking the player's next move instead of finding the next bestmove to have a Winning combination
        bestvalue=float('-inf')
        for i in Actions(s):                                                   #The MinMax algorithm works by alternating recursively by minimising a turn then maximising the next one.
            s[i[0],i[1]]='X'                                                   #in this case, maximising the IA's possible movements and minimising the players possible movements. 
            value = MinMax(s,depth-1,False,alpha,beta)
            s[i[0],i[1]]='.'
            bestvalue = max(bestvalue,value)            
            if bestvalue>=beta:
                return value
            alpha = max(alpha,bestvalue) 
            return value
    else:
        worsevalue=float('inf')
        for i in Actions(s):
            s[i[0]][i[1]]='O'
            value= MinMax(s,depth-1,True,alpha,beta)
            s[i[0],i[1]]='.'
            worsevalue=min(worsevalue,value)            
            if worsevalue<=alpha:
                return worsevalue
            beta=min(beta,worsevalue)
            return worsevalue                          
@temps

def DetectionZone(matrice):
    x1, y1 = 1000, 1000
    x2, y2 = -1000, -1000

    for i in range(np.shape(matrice)[0]):
        for j in range(np.shape(matrice)[0]):
            if matrice[i,j] != '.':
                if x1 > i:
                    x1 = i
                if x2 < i:
                    x2 = i
                if y1 > j:
                    y1 = j
                if y2 < j:
                    y2 = j
    return [x1 - 3,x2 + 3,y1 - 3,y2 + 3]
def JeuReduit(matrice):
    [x1,x2,y1,y2] = DetectionZone(matrice)
    taille = np.shape(matrice)[0]

    if x1 < 0:
        x1 = 0 
    if y1 < 0 :
        y1 = 0
    if x2 > taille - 1:
        x2 = taille - 1
    if y2 > taille - 1:
        y2 = taille - 1 
    while((x2 - x1 + 1) - (y2 - y1 + 1)) != 0:
        x = x2 - x1 + 1
        y = y2 - y1 + 1
        if x > y:
            if y2 + 1 > 11:
                if y1 -1 < 0 :
                    break
                else :
                    y1 -= 1
            else:
                y2 += 1         
        if x < y:
            if x2 +1 > 11:
                if x1 -1 < 0 :
                    break
                else :
                    x1 -= 1
            else:
                x2 += 1 
    taille = (x2 - x1 + 1)
    matriceA = np.full((taille,taille), fill_value ='.')
    for i in range(taille):
        for j in range(taille):
            matriceA[i,j] = matrice[i+x1,j+y1]
    return matriceA, [x1,y1]

def BestMove(s,x1,y1):                              #The Best_Move function introduces the minMax algorithm for the IA to place the most interesting move.
    max = -1000
    bestmove = None
    coup_autorise = Actions(s)

    for i in coup_autorise:
        s[i[0],i[1]] = 'X'
        val = MinMax(s, False, 0, -100, 100)
        if val > max:
            bestmove = i
            max = val
        s[i[0],i[1]] = '.'
    return bestmove

def PlacementJoueur(s):
    ok = False
    while ok == False:
        c = int(input('Play!\n\nColumn Cell:'))
        l = int(input('Row Cell:'))
        r = (l-1, c-1)
        if (r in Actions(s)): 
            s[r[0],r[1]]="O"
            ok = True                    
        else :
            print('\nAlready Taken!', end = ' ')
def PlacementIA(s):                                     #introduction function to the Best_Move function

    sTemp,[x1,y1] = JeuReduit(s)
    bMove = BestMove(sTemp,x1,y1)
    s[bMove[0]+x1,bMove[1]+y1] = 'X'
  
@temps    
def Morpion():                                          #this function is the function defining the game
    import random
    jeu = np.zeros((12, 12))
    jeu = np.where(jeu == 0, '.', jeu)
    j = int(input('Would you like to play First or Second? (0 for First and 1 for Second):'))
    while (j!=0 and j!=1):
        j = int(input('Would you like to play First or Second? (0 for First and 1 for Second):'))    
    tour =1
    while (TerminalTest(jeu,Joueur) == False) and (TerminalTest(jeu,IA)==False):
        print('Turn N°', tour)
        Grille(jeu)
        if ((tour==1)and(j==1)and(len(Actions(jeu))==144)):
            jeu[random.randint(6,7),random.randint(6,7)]= 'X'
        else :
            PlacementJoueur(jeu)
            if TerminalTest(jeu,Joueur):
                break
            if (len(Actions(jeu))==143) :
                if (5,5) in Actions(jeu):
                    jeu[5,5] = 'X'
                else:
                    jeu[6,6] = 'X'
            else :
                PlacementIA(jeu) 
        tour+=1
    Grille(jeu)    
def Conversion(tour):
    if tour ==0:
        return 'O'
    elif tour ==1:
        return 'X'

if __name__ == '__main__': 
   Morpion()
