import cv2
import numpy as np

def analyser_image():
    chemin_image = input("Entrez le chemin de votre image : ")
    
    try:
        image = cv2.imread(chemin_image)
        if image is None:
            print("Erreur : Impossible de charger l'image. Vérifiez le chemin.")
            return

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hauteur, largeur = image_rgb.shape[:2]
        
        print(f"Image chargée : {largeur}x{hauteur} pixels")
        
        nb_colonnes = int(input("Nombre de colonnes : "))
        nb_lignes = int(input("Nombre de lignes : "))
        seuil_blanc = float(input("Pourcentage de blanc pour considérer une case comme blanche (0-100) : "))
        
        largeur_case = largeur // nb_colonnes
        hauteur_case = hauteur // nb_lignes
        
        print(f"Taille de chaque case : {largeur_case}x{hauteur_case} pixels")
        
        cases_colorees = []

        for ligne in range(nb_lignes):
            for colonne in range(nb_colonnes):
                x_debut = colonne * largeur_case
                y_debut = ligne * hauteur_case
                x_fin = min(x_debut + largeur_case, largeur)
                y_fin = min(y_debut + hauteur_case, hauteur)
                
                case = image_rgb[y_debut:y_fin, x_debut:x_fin]

                pourcentage_blanc = calculer_pourcentage_blanc(case)

                if pourcentage_blanc < seuil_blanc:
                    cases_colorees.append((colonne, ligne))
                    print(f"Case colorée trouvée : ({colonne},{ligne}) - {pourcentage_blanc:.1f}% de blanc")
                else:
                    print(f"Case blanche skippée : ({colonne},{ligne}) - {pourcentage_blanc:.1f}% de blanc")

        print(f"\n=== RÉSULTATS ===")
        print(f"Nombre total de cases : {nb_colonnes * nb_lignes}")
        print(f"Nombre de cases colorées : {len(cases_colorees)}")
        print(f"Nombre de cases blanches (skippées) : {nb_colonnes * nb_lignes - len(cases_colorees)}")
        
        print(f"\nCoordonnées des cases colorées :")
        for coord in cases_colorees:
            print(f"  {coord}")
        
        return cases_colorees
        
    except Exception as e:
        print(f"Erreur : {e}")
        return None

def calculer_pourcentage_blanc(case):
    """
    Calcule le pourcentage de pixels blancs dans une case
    Un pixel est considéré comme blanc si ses valeurs RGB sont toutes > 240
    """
    seuil_pixel_blanc = 240
    
    pixels_blancs = np.sum(np.all(case >= seuil_pixel_blanc, axis=2))
    pixels_totaux = case.shape[0] * case.shape[1]
    
    if pixels_totaux == 0:
        return 0
    
    pourcentage = (pixels_blancs / pixels_totaux) * 100
    return pourcentage

if __name__ == "__main__":
    resultat = analyser_image()
    
    if resultat:
        print("\nAnalyse terminée avec succès !")
    else:
        print("\nErreur lors de l'analyse.")