# librerias necesarias
import os
import cv2
import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score

#------------------------------------------------------------------------------
# ruta local de la base de datos COIL-100
ruta_base = './objetos-coil-100'
folders_objetos = [f'objeto{i}' for i in range(1, 11)]
imagenes = {obj_id: [] for obj_id in range(1, 11)}

for obj_id, folder in zip(range(1, 11), folders_objetos):
    folder_path = os.path.join(ruta_base, folder)
    img_files = [os.path.join(folder_path, f'obj{obj_id}_{i}.png') for i in range(72)]
    imagenes[obj_id].extend(img_files)

#------------------------------------------------------------------------------
# dividir en entrenamiento, y test
img_entrenamiento = {}
img_test = {}

for obj_id, img_paths in imagenes.items():
    # seleccionó 16 de entrenamiento y 56 de test, de manera aleatoria
    img_entrenamiento[obj_id], img_test[obj_id] = train_test_split(img_paths, train_size=16/72, test_size=56/72)
#------------------------------------------------------------------------------
# funión para calcular histograma de color para entrenamiento
def calcular_histograma(imagen):
    img = cv2.imread(imagen)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # clcular en el canal H-Hue
    hist_hue = cv2.calcHist([img_hsv], [0], None, [256], [0, 256])
    # calcular historgrama en el canal S-Saturation
    hist_saturation = cv2.calcHist([img_hsv], [1], None, [256], [0, 256])
    # calcular el histograma en el canal V-Value
    hist_value = cv2.calcHist([img_hsv], [2], None, [256], [0, 256])
    
    # normalizar el histograma
    hist_hue /= hist_hue.sum()
    hist_saturation /= hist_saturation.sum()
    hist_value /= hist_value.sum()
    
    return hist_hue, hist_saturation, hist_value
#------------------------------------------------------------------------------
def comparar_histogramas(hist1, hist2):
    # distancia Chi-cuadrado para comparar histogramas
    dist_hue = cv2.compareHist(hist1[0], hist2[0], cv2.HISTCMP_CHISQR)
    dist_saturation = cv2.compareHist(hist1[1], hist2[1], cv2.HISTCMP_CHISQR)
    dist_value = cv2.compareHist(hist1[2], hist2[2], cv2.HISTCMP_CHISQR)
    
    return dist_hue + dist_saturation + dist_value
#------------------------------------------------------------------------------ 
# generar histogramas de entrenamiento para cada objeto
histogramas_entrenamiento = {obj_id: [] for obj_id in range(1, 11)}

for obj_id, img_paths in img_entrenamiento.items():
    for img in img_paths:
        hist = calcular_histograma(img)
        histogramas_entrenamiento[obj_id].append(hist)
#------------------------------------------------------------------------------
# inicializamos la s metriscas requeridas
verdaderos_positivos = 0
falsos_positivos = 0
verdaderos_negativos = 0
falsos_negativos = 0

# deteccion objetos en las imágenes de prueba
for obj_id, img_paths in img_test.items():
    for img in img_paths:
        # calcular histograma de la imagen de prueba
        hist_test = calcular_histograma(img)
        
        # coparar con los histogramas de entrenamiento
        mejor_match = None
        distancia_minima = float('inf')
        
        for entrenado_id, hist_list in histogramas_entrenamiento.items():
            for hist_entrenado in hist_list:
                dist = comparar_histogramas(hist_test, hist_entrenado)
                if dist < distancia_minima:
                    distancia_minima = dist
                    mejor_match = entrenado_id

        if mejor_match == obj_id:
            verdaderos_positivos += 1
        else:
            falsos_positivos += 1
            if mejor_match is not None:
                falsos_negativos += 1

#------------------------------------------------------------------------------ 
#metricas por objeto
for obj_id, img_paths in img_test.items():
    img_paths_muestra = random.sample(img_paths, 3) # 3 imagenes random del msmo objeto
    img_cuarta = random.choice(img_paths) # imagen que se cimparara con otra de otra carpeta

    # Seleccionar una imagen aleatoria de otra carpeta para la comparación negativa
    carpeta_aleatoria = random.choice([i for i in range(1, 11) if i != obj_id])
    img_aleatoria_negativa = random.choice(img_test[carpeta_aleatoria])

    predicciones_positivas = []
    valores_reales_positivas = []

    #comparacion
    print("------------------------------------------------------------------------------")
    print(f"\n---------------------------PRUEBA OBJETO {obj_id}--------------------------")
    print(f"\n--- Comparación de imagenes para el Objeto {obj_id} ---")
    for img in img_paths_muestra:
        hist_test = calcular_histograma(img)
        
        # busqueda del mejor "match" en las imagenes de entrenamiento
        mejor_match = None
        distancia_minima = float('inf')
        
        for entrenado_id, hist_list in histogramas_entrenamiento.items():
            for hist_entrenado in hist_list:
                dist = comparar_histogramas(hist_test, hist_entrenado)
                if dist < distancia_minima:
                    distancia_minima = dist
                    mejor_match = entrenado_id

        predicciones_positivas.append(mejor_match)#guardar en lista
        valores_reales_positivas.append(obj_id)
        
        print(f"Imagen: {img}, Objeto Real: {obj_id}, Objeto Predicho: {mejor_match}")

    # metricas de las imagenes que sean positivas
    accuracy = accuracy_score(valores_reales_positivas, predicciones_positivas)
    precision = precision_score(valores_reales_positivas, predicciones_positivas, average='macro', zero_division=1)
    recall = recall_score(valores_reales_positivas, predicciones_positivas, average='macro', zero_division=1)
    f1 = f1_score(valores_reales_positivas, predicciones_positivas, average='macro', zero_division=1)

    print(f"\n--- Métricas para el Objeto {obj_id} ---")
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F-Score: {f1}")

    # comparar cuarta cuarta imagen con una imagen de otra carpeta (negativa)
    hist_test_cuarta = calcular_histograma(img_cuarta)
    mejor_match_cuarta = None
    distancia_minima_cuarta = float('inf')
    
    for hist_entrenado in histogramas_entrenamiento[carpeta_aleatoria]:
        dist = comparar_histogramas(hist_test_cuarta, hist_entrenado)
        if dist < distancia_minima_cuarta:
            distancia_minima_cuarta = dist
            mejor_match_cuarta = carpeta_aleatoria

    print(f"\n--- Comparación de Imagen Negativa para el Objeto {obj_id} ---")
    print(f"Imagen (misma carpeta): {img_cuarta}, Imagen (otra carpeta): {img_aleatoria_negativa}")
    print(f"Objeto Real: {obj_id}, Objeto Predicho (debería no coincidir): {mejor_match_cuarta}")

    # se clasificó correctamente?
    if mejor_match_cuarta != obj_id:
        print("Clasificación correcta de la comparación negativa (no coincide).")
    else:
        print("Error: La comparación negativa fue clasificada incorrectamente.")
    print("------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------")




















