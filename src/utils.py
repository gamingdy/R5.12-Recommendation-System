import numpy as np

def pearson_similarity(x, y):

    if len(x) != len(y):
        raise ValueError("Les deux listes doivent avoir la même longueur")
    x = np.array(x)
    y = np.array(y)
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    numerator = np.sum((x - mean_x) * (y - mean_y))
    denominator = np.sqrt(np.sum((x - mean_x) ** 2) * np.sum((y - mean_y) ** 2))

    if denominator == 0:
        return 0
    return numerator / denominator


def prediction(i,j,L):
    numerator=moyenne(i)
    denominator=0
    for u in L:
        numerator += note(u,j)-moyenne(u)*pearson_similarity(i,u)
        denominator+=pearson_similarity(i,u)
    return numerator/denominator

def getListeU(j,L):
    resultat=[]
    for k in L:
        if k[j]!=-1:
            resultat.append(k)

def moyenne(i):
    u=getListeBase(i)
    return(np.mean(u))

def note(i,j):
    u=getListeBase(i)
    return(u[j])