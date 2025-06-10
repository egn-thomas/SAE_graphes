class Magasin:
    def __init__(self, nom="", path_plan_magasin="", liste_produits=None, nb_colonnes=35, nb_lignes=52):
        self.nom = nom
        self.path_plan_magasin = path_plan_magasin
        self.liste_produits = liste_produits if liste_produits is not None else []
        self.nb_colonnes = nb_colonnes
        self.nb_lignes = nb_lignes

        self.largeur_image = None
        self.hauteur_image = None
        self.largeur_cellule = None
        self.hauteur_cellule = None

        self.coord_to_cell = {}  # "A1" → Cellule
        self.cases_passage = set()
        self.cases_rayon = set()  # Changement de list() à set()
        self.coord_produits = {}  # Le dictionnaire contiendra des listes de produits

    def initialiser_plan(self, pixmap):
        self.plan_pixmap = pixmap
        self.largeur_image = pixmap.width()
        self.hauteur_image = pixmap.height()

        self.largeur_cellule = self.largeur_image // self.nb_colonnes
        self.hauteur_cellule = self.hauteur_image // self.nb_lignes

        self.coord_to_cell.clear()

        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                coord = f"{chr(65 + j)}{i + 1}"  # Exemple : A1, B2, etc.
                self.coord_to_cell[coord] = None

    # Méthodes pour marquer les zones et gérer les produits :
    def definir_passage(self, coord):
        self.cases_passage.add(coord)
        self.cases_rayon.discard(coord)

    def definir_rayon(self, coord):
        self.cases_rayon.add(coord)
        self.cases_passage.discard(coord)

    def est_passage(self, coord):
        return coord in self.cases_passage

    def est_rayon(self, coord):
        return coord in self.cases_rayon

    def enregistrer_produit(self, coord, produit):
        if coord not in self.coord_produits:
            self.coord_produits[coord] = []
        self.coord_produits[coord].append(produit)

    def produit_a(self, coord):
        if coord in self.coord_produits and self.coord_produits[coord]:
            return ", ".join(self.coord_produits[coord])
        return None

    def affecter_cellule(self, coord, widget):
        self.coord_to_cell[coord] = widget

    def sauvegarder(self, chemin):
        import json
        with open(chemin, "w") as f:
            json.dump({
                "nom": self.nom,
                "image_path": self.path_plan_magasin,
                "nb_colonnes": self.nb_colonnes,
                "nb_lignes": self.nb_lignes,
                "cases_passage": list(self.cases_passage),
                "cases_rayon": list(self.cases_rayon),
                "coord_produits": self.coord_produits,
            }, f, indent=2)

    def charger(self, chemin):
        import json
        with open(chemin, "r") as f:
            data = json.load(f)
            self.nom = data["nom"]
            self.path_plan_magasin = data["image_path"]
            self.nb_colonnes = data["nb_colonnes"]
            self.nb_lignes = data["nb_lignes"]
            self.cases_passage = set(data["cases_passage"])
            self.cases_rayon = set(data["cases_rayon"])
            self.coord_produits = data["coord_produits"]