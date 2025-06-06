import csv
class csvLoader :
    def __init__(self, file_path, delimiter=';'):
        """le delimiter est mis car le fichier csv separe les produit par des ';' et non des ',' """
        self.file_path = file_path
        self.delimiter=delimiter
    
    
    def extract_all(self):
        """on extrait l'ensemble du fichier dans une liste de liste"""
        with open(self.file_path, newline='', encoding='utf-8') as csvfile:
            reader=csv.reader(csvfile, delimiter=self.delimiter)
            return [row for row in reader]
#lecture du fichier CSV

if __name__ == "__main__":
    csv_loader=csvLoader('../liste_produits.csv')
    liste_produits= csv_loader.extract_all()
    csv_loader=csvLoader('../Magasin.csv')
    liste_produits_magasin=csv_loader.extract_all()

    print(liste_produits)
    print(liste_produits_magasin)
