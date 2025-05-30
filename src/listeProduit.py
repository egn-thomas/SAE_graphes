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