from .utils import prediction4,data_reader,get_user_data,get_liste_utilisateur

incomplete = data_reader("dataset/toy_incomplet.xlsx")
item = 1
u = get_user_data(incomplete, 0)

liste=get_liste_utilisateur(incomplete,item)
pred = prediction4(u,item,liste)