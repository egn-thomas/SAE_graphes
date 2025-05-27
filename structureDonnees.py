import pandas as pd

df = pd.read_csv("liste_produits.csv", sep=';')
df.columns = df.columns.str.strip()  # Nettoie les noms de colonnes

# Dictionnaire où chaque clé est le nom d'une colonne, et la valeur est la liste des produits
categories = {
    colonne: df[colonne].dropna().tolist()
    for colonne in df.columns
}

# liste_catégories : ["Légumes","Poissons","Viandes","Épicerie","Épicerie sucrée","Petit déjeuner","Fruits","Rayon frais","Crèmerie","Conserves","Apéritifs","Boissons","Articles Maison","Hygiène","Bureau","Animaux"]