import cv2
import numpy as np
from PIL import Image

def apply_texture_based_on_luminosity(image_path, texture_path, output_path):
    # Charger l'image de base
    base_image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)

    # Charger la texture
    texture = cv2.imread(texture_path)

    # Redimensionner la texture pour qu'elle corresponde à la taille de l'image originale
    texture_resized = cv2.resize(texture, (base_image.shape[1], base_image.shape[0]))

    # Normaliser la luminosité (échelle entre 0 et 1)
    luminosity_mask = gray_image / 255.0

    # Créer une image de sortie
    output = np.zeros_like(base_image, dtype=np.uint8)

    # Mélanger la texture et l'image originale en fonction de la luminosité
    for i in range(3):  # Pour chaque canal (R, G, B)
        output[:, :, i] = (
            base_image[:, :, i] * (1 - luminosity_mask)  # Intensité réduite de l'image originale
            + texture_resized[:, :, i] * luminosity_mask  # Intensité de la texture en fonction de la luminosité
        ).astype(np.uint8)

    # Sauvegarder et afficher le résultat final
    cv2.imwrite(output_path, output)
    Image.open(output_path).show()
    print(f"Image retexturée sauvegardée sous {output_path}")

# Exemple d'utilisation
apply_texture_based_on_luminosity("original.jpg", "texture.png", "texture_picture.jpg")
