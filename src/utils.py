import math
import os

import matplotlib.pyplot as plt
import numpy as np
import openpyxl
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
    result = numerator / denominator
    return result

def calculate_pearson(utilisateur_a_noter,liste_u_notes):
    result = []
    for utilisateur in liste_u_notes:
        u1, u2 = comparer(utilisateur_a_noter, utilisateur)
        pearson = pearson_similarity(u1, u2)
        result.append((utilisateur,pearson))
    return result

def prediction(utilisateur_a_noter, item, liste_u_notes):
    numerator = 0
    denominator = 0
    all_pearson = calculate_pearson(utilisateur_a_noter,liste_u_notes)
    for utilisateur,pearson in all_pearson:
        numerator += (note(utilisateur, item) - moyenne(utilisateur)) * pearson
        denominator += pearson
    if denominator == 0:
        return -1
    return math.trunc(numerator / denominator + moyenne(utilisateur_a_noter))


def prediction3_square(utilisateur_a_noter, item, liste_u_notes):
    numerator = 0
    denominator = 0
    all_pearson = calculate_pearson(utilisateur_a_noter,liste_u_notes)

    for utilisateur,pearson in all_pearson:
        numerator += (
            note(utilisateur, item) -  moyenne(utilisateur)
        ) * pearson**2
        denominator += pearson**2
    if denominator == 0:
        return -1       
    return math.trunc((numerator / denominator) + moyenne(utilisateur_a_noter))


def prediction3(utilisateur_a_noter, item, liste_u_notes):
    numerator = 0
    denominator = 0
    all_pearson = calculate_pearson(utilisateur_a_noter,liste_u_notes)
    for utilisateur,pearson in all_pearson:
        numerator += (note(utilisateur, item)) * pearson
        denominator += pearson
    if denominator == 0:
        return -1
    return round(numerator / denominator)


def prediction_cosine(utilisateur_a_noter, item, liste_u_notes):
    numerator = 0
    denominator = 0
    for utilisateur in liste_u_notes:
        u1, u2 = comparer(utilisateur_a_noter, utilisateur)
        cosine = cosine_similarity(u1, u2)
        numerator += (note(utilisateur, item) - moyenne(utilisateur)) * cosine
        denominator += cosine
    if denominator == 0:
        return -1
    return math.trunc(numerator / denominator + moyenne(utilisateur_a_noter))


def prediction_limited_user(utilisateur_a_noter, item, liste_u_notes, nb_user):
    numerator = 0
    denominator = 0
    all_pearson = calculate_pearson(utilisateur_a_noter,liste_u_notes)

    all_pearson.sort(key=lambda x: x[1], reverse=True)
    all_pearson = all_pearson[:nb_user]

    for user, pearson in all_pearson:
        numerator += (note(user, item)) * pearson**2
        denominator += pearson**2
    if denominator == 0:
        return -1
    return round(numerator / denominator)

def prediction_limited_user2(utilisateur_a_noter, item, liste_u_notes, nb_user):
    numerator = 0
    denominator = 0
    all_pearson = calculate_pearson(utilisateur_a_noter,liste_u_notes)

    all_pearson.sort(key=lambda x: x[1], reverse=True)
    all_pearson = all_pearson[:nb_user]

    for user, pearson in all_pearson:
        numerator += (note(user, item)) * pearson
        denominator += pearson
    if denominator == 0:
        return -1
    return round(numerator / denominator)

def data_reader(file_path) -> pd.DataFrame:
    return pd.read_excel(file_path, header=None)


def get_liste_utilisateur(data, item):
    resultat = []
    for i, _ in data.iterrows():
        user = get_user_data(data, i)
        if user[item] != -1:
            resultat.append(user)

    return resultat

def get_liste_item(data, user):
    resultat = []
    for i, _ in data.iterrows():
        item = get_item_data(data, i)
        if item[user] != -1:
            resultat.append(item)

    return resultat


def moyenne(utilisateur):
    return np.mean(filtrer(utilisateur))


def note(utilisateur, item):
    return utilisateur[item]


def get_user_data(data, user_id):
    return list(map(int, data.loc[user_id].values[0].split()))

def get_item_data(data, item_id):
    items_data = []
    for user in range(len(data)):
        user_data = get_user_data(data,user)
        items_data.append(user_data[item_id])


    return items_data

def filtrer(utilisateur):
    return list(filter(lambda x: (x > -1), utilisateur))


def comparer(u1, u2):
    result_u1 = []
    result_u2 = []
    for indice, item in enumerate(u1):
        if u2[indice] != -1 and item != -1:
            result_u1.append(item)
            result_u2.append(u2[indice])
    return result_u1, result_u2


def cosine_similarity(u1, u2):
    u1 = np.array(u1)
    u2 = np.array(u2)

    dot_product = np.dot(u1, u2)
    norm_u1 = np.linalg.norm(u1)
    norm_u2 = np.linalg.norm(u2)

    if norm_u1 == 0 or norm_u2 == 0:
        return 0

    return dot_product / (norm_u1 * norm_u2)


def qualite_prediction(data_complet, data_rempli):
    resultat = 0
    for i in range(len(data_complet)):
        u_complet = get_user_data(data_complet, i)
        u_rempli = get_user_data(data_rempli, i)
        liste = zip(u_complet, u_rempli)
        for j in liste:
            resultat += j[1] - j[0]
    return resultat


def remplir_total_pearson(data_vide):
    wb = openpyxl.Workbook()
    ws = wb.active

    for i in range(1):
        u = get_user_data(data_vide, i)
        print(u)
        lst = list(range(10))
        row = ""
        for j, item in enumerate(u):
            if j > 10:
                break
            if item == -1:
                liste = get_liste_utilisateur(data_vide, j)
                predicted_value = prediction(u, j, liste)
                print(j, predicted_value)
                row += f"{predicted_value} "
            else:
                row += f"{item} "

            ws.cell(row=i + 1, column=1, value=row)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_dir, "..", "tests/dataset")
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
    save_path = os.path.join(dataset_dir, "data_remplie.xlsx")
    wb.save(save_path)


def efficacite(nb_user):
    dirname = os.path.split(os.path.abspath(__file__))[0]
    data_incomplet = data_reader(f"{dirname}/../dataset/toy_incomplet.xlsx")
    data_reel = data_reader(f"{dirname}/../dataset/toy_complet.xlsx")

    predicted_faux = []
    for i in range(1, 20):
        utilisateur = get_user_data(data_incomplet, i)
        utilisateur_reel = get_user_data(data_reel, i)
        taille = len(utilisateur)
        for j, item in enumerate(utilisateur):
            if j > taille:
                break

            if item == -1:
                liste = get_liste_utilisateur(data_incomplet, j)
                predicted_value = prediction_limited_user(utilisateur, j, liste, nb_user)
                predicted_faux.append(predicted_value - utilisateur_reel[j])
        res_abs = sum([abs(i) for i in predicted_faux]) / taille
    
    return res_abs,nb_user
        
            #all_biais.append(res_biais)
            #all_abs.append(res_abs)

    #plt.plot(nb_user, all_abs, label="abs", color="red")
    #plt.plot(nb_user, all_biais, label="biais", color="blue")
    #plt.show()

def efficacite2(nb_user):
    dirname = os.path.split(os.path.abspath(__file__))[0]
    data_incomplet = data_reader(f"{dirname}/../dataset/toy_incomplet.xlsx")
    data_reel = data_reader(f"{dirname}/../dataset/toy_complet.xlsx")
    predicted_faux = []
    for i in range(1, 20):
        utilisateur = get_user_data(data_incomplet, i)
        utilisateur_reel = get_user_data(data_reel, i)
        taille = len(utilisateur)
        for j, item in enumerate(utilisateur):
            if j > taille:
                break

            if item == -1:
                liste = get_liste_utilisateur(data_incomplet, j)
                predicted_value = prediction_limited_user2(utilisateur, j, liste, nb)
                predicted_faux.append(predicted_value - utilisateur_reel[j])
        res_abs = sum([abs(i) for i in predicted_faux]) / taille
    return res_abs,nb_user
        


def efficacite_simple_item(data_incomplet, data_reel):
    predicted_faux = []
    for i in range(1, 2):
        item = get_item_data(data_incomplet, i)
        item_reel = get_item_data(data_reel, i)
        taille = len(item)
        for j, user in enumerate(item):
            if j > taille:
                break

            if user == -1:
                liste = get_liste_item(data_incomplet, j)
                predicted_value = prediction3_square(item, j, liste)
                predicted_faux.append(predicted_value - item_reel[j])
        res_biais = sum(predicted_faux) / taille
        res_abs = sum([abs(i) for i in predicted_faux]) / taille
        print(res_abs, ": res abs")
        print(res_biais, ": res biais")


def efficacite_simple(data_incomplet, data_reel):
    predicted_faux = []
    for i in range(1,5):
        utilisateur = get_user_data(data_incomplet, i)
        utilisateur_reel = get_user_data(data_reel, i)
        taille = len(utilisateur)
        for j, item in enumerate(utilisateur):
            if j > taille:
                break

            if item == -1:
                liste = get_liste_utilisateur(data_incomplet, j)
                predicted_value = prediction3(utilisateur, j, liste)
                predicted_faux.append(predicted_value - utilisateur_reel[j])        
        res_biais = sum(predicted_faux) / taille
        res_abs = sum([abs(i) for i in predicted_faux]) / taille
        print(res_abs, ": res abs")
        print(res_biais, ": res biais")
