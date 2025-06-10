class magasin:
    def __init__(self, nom, path_plan_magasin, liste_produits, nb_colonnes, nb_lignes):
        self.nom = nom
        self.path_plan_magasin = path_plan_magasin
        self.liste_produits = liste_produits
        self.nb_colonnes = nb_colonnes
        self.nb_lignes = nb_lignes
        
        self.largeur_image = None
        self.hauteur_image = None
        self.taille_cellule = None
        self.nombre_cases_hauteur = None
        
        coord_to_cell = {}
        self.cases_passage = set()
        self.cases_rayon = set()
        self.coord_produits = {}
        
        self.plan_pixmap = None
        self.cell_size = None
        
        
    def initialiser_plan(self, pixmap):
        self.largeur_image = pixmap.width()
        self.hauteur_image = pixmap.height()
        self.taille_cellule = self.largeur_image // self.nombre_cases_largeur
        self.nombre_cases_hauteur = self.hauteur_image // self.taille_cellule