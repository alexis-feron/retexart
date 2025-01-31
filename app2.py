import cv2
import numpy as np

# Charger l'image
image = cv2.imread('original.jpg')

# Convertir l'image en espace colorimétrique HSV (pour faciliter la détection des couleurs)
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Dictionnaire contenant les plages de couleurs
colors = {
    "red": [(0, 120, 70), (10, 255, 255)], 
    "red2": [(170, 120, 70), (180, 255, 255)],
    "green": [(40, 50, 50), (80, 255, 255)],
    "blue": [(100, 50, 50), (140, 255, 255)],
    "yellow": [(20, 100, 100), (40, 255, 255)],
    "orange": [(10, 100, 100), (20, 255, 255)],
    "cyan": [(80, 100, 100), (100, 255, 255)],
    "purple": [(140, 100, 100), (160, 255, 255)],
}

# Dictionnaire contenant les couleurs BGR pour dessiner
color_bgr = {
    "red": (0, 0, 255),
    "red2": (0, 0, 255),  # Ajoute cette ligne pour la couleur rouge (2e plage)
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "yellow": (0, 255, 255),
    "orange": (0, 165, 255),
    "cyan": (255, 255, 0),
    "purple": (255, 0, 255),
}

# Créer une image de base (vide) pour dessiner les contours remplis
image_filled = np.zeros_like(image)

# Itérer sur les couleurs et appliquer le traitement
for color_name, (lower, upper) in colors.items():
    # Créer un masque pour chaque couleur
    mask = cv2.inRange(hsv_image, np.array(lower), np.array(upper))
    
    # Trouver les contours de chaque zone colorée
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Colorier l'intérieur des contours avec la couleur appropriée
    cv2.drawContours(image_filled, contours, -1, color_bgr[color_name], thickness=cv2.FILLED)

# Afficher l'image résultante avec les zones de couleurs remplies
cv2.imshow("Zones de couleur remplies", image_filled)
cv2.waitKey(0)
cv2.destroyAllWindows()

# import cv2
# import numpy as np
# from sklearn.cluster import KMeans

# # Charger l'image
# image = cv2.imread('original.jpg')

# # Convertir l'image en espace colorimétrique HSV
# hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# # Convertir l'image en un format de données pour KMeans (reshape en une liste de pixels)
# pixels = hsv_image.reshape(-1, 3)

# # Appliquer KMeans pour extraire les couleurs dominantes (par exemple, 8 clusters)
# kmeans = KMeans(n_clusters=8, random_state=0)
# kmeans.fit(pixels)

# # Obtenir les centres des clusters (les couleurs dominantes)
# dominant_colors = kmeans.cluster_centers_

# # Créer un dictionnaire pour les couleurs dominantes avec des plages approximatives
# colors_dict = {}
# color_bgr = {}

# for i, color in enumerate(dominant_colors):
#     hue = int(color[0])
#     lower = [hue - 10, 50, 50]  # Plage inférieure approximative
#     upper = [hue + 10, 255, 255]  # Plage supérieure approximative
#     colors_dict[f"color_{i}"] = [lower, upper]

#     # Convertir la couleur dominante de HSV à BGR pour l'affichage
#     bgr_color = tuple(map(int, cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_HSV2BGR)[0][0]))
#     color_bgr[f"color_{i}"] = bgr_color

# # Créer une image de base (vide) pour dessiner les contours remplis
# image_filled = np.zeros_like(image)

# # Itérer sur les couleurs dominantes et appliquer le traitement
# for color_name, (lower, upper) in colors_dict.items():
#     # Créer un masque pour chaque couleur dominante
#     mask = cv2.inRange(hsv_image, np.array(lower), np.array(upper))
    
#     # Trouver les contours de chaque zone colorée
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
#     # Colorier l'intérieur des contours avec la couleur appropriée
#     cv2.drawContours(image_filled, contours, -1, color_bgr[color_name], thickness=cv2.FILLED)

# # Afficher l'image résultante avec les zones de couleurs remplies
# cv2.imshow("Zones de couleur remplies", image_filled)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
