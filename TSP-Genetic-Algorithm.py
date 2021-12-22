import numpy as np
import matplotlib.pyplot as plt
from random import randint

def populacao():
    populacao = np.zeros((12,5))
    for i in range(12):
        populacao[i] = np.random.choice(5, 5, replace=False)
    populacao = populacao.astype(int)
    return populacao

def fitness(populacao):
    cg = np.array([325,420,230,143,189])
    cidades = np.array([[0,325,230,143,189],[335,0,588,563,609],[270,588,0,373,413],[285,563,373,0,213],[474,609,413,213,0]])
    fit = np.zeros((12,1))
    for i in range(12):
        soma = 0
        for j in range(5):
            if(j==0 or j==4):
                soma +=cg[populacao[i][j]]
            if(j!=0):
                soma += cidades[populacao[i][j-1],populacao[i][j]]
        fit[i] = soma        
        fit[i] = 1/fit[i]
    return fit

def proba(fit):
    p=fit
    som = 0
    for i in range(12):
        som += fit[i] 
    for i in range(12):
        p[i] = fit[i]/som  
    return p

def wheel(p):
    roulette = p
    for i in range(12):
        if (i!=0):
            roulette[i] += roulette[i-1]
    return roulette

def mutation(p):
    for i in range(12):
        t = np.random.random_sample()
        #print(t)
        if(t<=0.1):
            a = randint(0,4)
            b = randint(0,4)
            while(a==b):
                b = randint(0,4)
            temp = p[i]
            x = temp[a]
            temp[a] = temp[b]
            temp[b] = x 
            p[i] = temp
    return p


def crossover(p):
    a = randint(1,2)
    b = randint(2,3)
    p_temp = np.zeros((12,5))
    filho1 = np.array([0,0,0,0,0])
    filho2 = np.array([0,0,0,0,0])
    
    while(a==b):
        b = 3

    for i in range(6):
        p_temp[i] = p[i]
        p_temp[i+6] = p[i+6]
        p_temp = p_temp.astype(int)

        t = np.random.random_sample()
        if(t>=0.6):
            filho1 = p_temp[i]
            filho2 = p_temp[i+6]
            for j in range(a):
                filho1[j] = -1
                filho2[j] = -1
                for k in range(b+1,5):
                    filho1[k] = -1
                    filho2[k] = -1
            j = b+1
            m = j
            n = j
            while((m!=a)and(n!=a)):
                temp = p[i]
                temp2 = p[i+6]
                for l in range(a,b+1):                    
                    if(temp[j]==filho2[l]):
                        break
                    if(l==b):
                        filho2[m] = temp[j]
                        m = (m+1)%5
                for l in range(a,b+1):
                    if(temp2[j]==filho1[l]):
                        break
                    if(l==b):
                        filho1[n] = temp2[j]
                        n = (n+1)%5
                j = (j+1)%5
            p_temp[i] = filho2
            p_temp[i+6] = filho1
        else:
            p_temp[i] = p[i]
            p_temp[i+6] = p[i+6]
    return p_temp
                 
def repeat(wh,x):
    for i in range(500):
        p = x
        for j in range(12):
            r = np.random.random_sample()
            k = 0
            for k in range(12):
                if(r<=wh[[k]]):
                    p[j] = x[k]
                    break
        temp_p = crossover(p)
        p_temp = mutation(temp_p)
        
        fit = fitness(p_temp)
        prob = proba(fit)
        wh = wheel(prob)

    print(p_temp)


if __name__ == "__main__":
    x = populacao()
    fit = fitness(x)
    prob = proba(fit)
    wh = wheel(prob)
    repeat(wh,x)