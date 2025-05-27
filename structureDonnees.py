import json

with open('liste.json', 'r', encoding='utf-8') as liste:
    produits = json.load(liste)

legumes: list = produits["Légumes"]             # Toutes les catégories sont classées ici, l'administrateur peut ajouter des éléments à cette liste
poisson: list = produits["Poissons"]
viande: list = produits["Viandes"]
epicerie: list = produits["Épicerie"]
epicerieSucree: list = produits["Épicerie sucrée"]
petitDejeuner: list = produits["Petit déjeuner"]
fruits: list = produits["Fruits"]
rayonFrais: list = produits["Rayon frais"]
cremerie: list = produits["Crèmerie"]
conserves: list = produits["Conserves"]
aperitifs: list = produits["Apéritifs"]
boissons: list = produits["Boissons"]
articleMaison: list = produits["Articles maison"]
hygiene: list = produits["Hygiène"]
bureau: list = produits["Bureau"]
animaux: list = produits["Animaux"]