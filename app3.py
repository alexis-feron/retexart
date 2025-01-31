import cv2
import numpy as np
from PIL import Image

# Charger l'image
image = cv2.imread('original.jpg')

# Convertir l'image en LAB pour une segmentation plus facile basée sur les couleurs
lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

# Appliquer K-Means Clustering pour segmenter l'image en plusieurs zones de couleur
Z = lab_image.reshape((-1, 3))
Z = np.float32(Z)

# Paramètres de k-means
K = 15  # Nombre de zones à détecter (ajuster selon l'image)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
_, labels, centers = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# Remettre les couleurs segmentées dans l'image
segmented_image = centers[labels.flatten()].reshape(image.shape).astype(np.uint8)

# Créer une nouvelle image pour afficher les couleurs moyennes
image_with_mean_colors = np.zeros_like(image)

# Calculer et appliquer la couleur moyenne à chaque zone
for i in range(K):
    # Créer un masque pour chaque zone
    mask = (labels == i).reshape(image.shape[:2])
    
    # Calculer la couleur moyenne de la zone
    mean_color = centers[i].astype(np.uint8)
    
    # Appliquer cette couleur moyenne à toute la zone
    image_with_mean_colors[mask] = mean_color

# Sauvegarde et affichage de l'image avec les couleurs moyennes
output_path = 'output_with_mean_colors.jpg'
cv2.imwrite(output_path, image_with_mean_colors)
Image.open(output_path).show()
