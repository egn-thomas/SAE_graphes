import csv
import pandas as pd

with open('liste_produits.csv', mode='r', encoding='utf-8') as produits:     # Lit le csv
    df = pd.read_csv("liste_produits.csv")
    df.columns = df.columns.str.strip()
    csv.DictReader(produits, delimiter=';')
    pd.read_csv("data.csv", sep=';')

legumes = df["Légumes"].dropna().tolist()               # Toutes les catégories sont classées ici, l'administrateur peut ajouter des éléments à cette liste
poissons = df["Poissons"].dropna().tolist()
viande = df["Viandes"].dropna().tolist()
epicerie = df["Épicerie"].dropna().tolist()
epicerieSucree = df["Épicerie sucrée"].dropna().tolist()
petitDejeuner = df["Petit déjeuner"].dropna().tolist()
fruits = df["Fruits"].dropna().tolist()
rayonFrais = df["Rayon frais"].dropna().tolist()
cremerie = df["Crèmerie"].dropna().tolist()
conserves = df["Conserves"].dropna().tolist()
apperitifs = df["Apéritifs"].dropna().tolist()
boissons = df["Boissons"].dropna().tolist()
articleMaison = df["Articles Maison"].dropna().tolist()
hygiene = df["Hygiène"].dropna().tolist()
bureau = df["Bureau"].dropna().tolist()
animaux = df["Animaux"].dropna().tolist()

# Ajouter "import structureDonnees" au debut du code Admin