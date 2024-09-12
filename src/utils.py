import numpy as np
import pandas as pd


def pearson_similarity(u1, u2):
    if len(u1) != len(u2):
        raise ValueError("Les deux listes doivent avoir la même longueur")
    u1 = np.array(u1)
    u2 = np.array(u2)
    mean_u1 = np.mean(u1)
    mean_u2 = np.mean(u2)
    numerator = np.sum((u1 - mean_u1) * (u2 - mean_u2))
    denominator = np.sqrt(
        np.sum((u1 - mean_u1) ** 2) * np.sum((u2 - mean_u2) ** 2)
    )
    if denominator == 0:
        return 0
    return numerator / denominator


def prediction(data,utilisateur_a_noter, item, liste_u_notes):
    numerator = moyenne(data,utilisateur_a_noter)
    denominator = 0
    for utilisateur in liste_u_notes:
        pearson=pearson_similarity(comparer(utilisateur_a_noter, utilisateur))
        numerator += note(data,utilisateur, item) - moyenne(data,utilisateur) * pearson
        denominator += pearson
    if denominator == 0:
        return -1
    return numerator / denominator


def data_reader(file_path) -> pd.DataFrame:
    return pd.read_excel(file_path, header=None)


def get_liste_utilisateur(data, item):
    resultat = []
    for utilisateur in data:
        if utilisateur[item] != -1:
            resultat.append(utilisateur)


def moyenne(data, utilisateur):
    return np.mean(filtrer(get_user_data(data, utilisateur)))


def note(data, utilisateur, item):
    return get_user_data(data, utilisateur)[item]


def get_user_data(data, user_id):
    return list(map(int, data.loc[user_id].values[0].split()))


def filtrer(utilisateur):
    return list(filter(lambda x: (x > -1), utilisateur))

def comparer(u1,u2):
    result_u1=[]
    result_u2=[]
    for indice,item in enumerate(u1):
        if u2[indice]!=-1 and item!=-1:
            result_u1.append(item)
            result_u2.append(u2[indice])
    return(result_u1,result_u2)

def cosine_similarity(u1, u2):
    u1 = np.array(u1)
    u2 = np.array(u2)
    dot_product = np.dot(u1, u2)
    norm_u1 = np.linalg.norm(u1)
    norm_u2 = np.linalg.norm(u2)
    if norm_u1 == 0 or norm_u2 == 0:
        return 0
    return dot_product / (norm_u1 * norm_u2)


