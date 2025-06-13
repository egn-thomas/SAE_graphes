import csv
from collections import defaultdict

class CsvLoader:
    def __init__(self, file_path, delimiter=';'):
        """Le délimiteur est mis car le fichier CSV sépare les produits par des ';' et non des ','"""
        self.file_path = file_path
        self.delimiter = delimiter

    def extract_all(self):
        """Extrait l'ensemble du fichier dans une liste de listes"""
        with open(self.file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            return [row for row in reader]

    @staticmethod
    def charger_table_categories(path="../liste_produits.csv"):
        """
        Charge un fichier CSV où la première ligne contient les catégories
        et les lignes suivantes les produits associés.
        """
        table_categorie = defaultdict(list)
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=';')
            lignes = list(reader)
            categories = lignes[0]
            for ligne in lignes[1:]:
                for i, produit in enumerate(ligne):
                    produit = produit.strip()
                    if produit:
                        table_categorie[categories[i]].append(produit)
        return table_categorie

    @staticmethod
    def extraire_articles_par_categorie(fichier_disposition, fichier_categories):
        """Retourne un tableau de type CSV (1re ligne = catégories, lignes suivantes = produits alignés)"""
        
        # 1. Récupérer les articles présents
        articles_presents = set()
        with open(fichier_disposition, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                nom = row["Nom du produit"].strip()
                if " x" in nom:
                    nom = nom.split(" x")[0].strip()
                articles_presents.add(nom)

        # 2. Charger les catégories
        table_categories = CsvLoader.charger_table_categories(fichier_categories)

        # 3. Filtrer les produits présents
        resultat = defaultdict(list)
        for categorie, produits in table_categories.items():
            for p in produits:
                if p in articles_presents:
                    resultat[categorie].append(p)

        # 4. Convertir en tableau avec entêtes
        categories = list(resultat.keys())
        max_len = max(len(liste) for liste in resultat.values())

        lignes = [categories]
        for i in range(max_len):
            ligne = []
            for cat in categories:
                if i < len(resultat[cat]):
                    ligne.append(resultat[cat][i])
                else:
                    ligne.append("")
            lignes.append(ligne)

        return lignes
