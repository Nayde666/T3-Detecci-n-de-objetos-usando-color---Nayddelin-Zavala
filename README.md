# Detección de Objetos por Color en COIL-100

Este proyecto implementa un programa en Python y OpenCV para detectar objetos de la base de datos COIL-100 utilizando histogramas de color. La detección se realiza mediante la comparación de histogramas entre imágenes de entrenamiento y de prueba, y se valida la precisión de los resultados obtenidos.

## Estructura de la Carpeta de Imágenes

Para que el programa funcione correctamente, es necesario contar con una carpeta que contenga subcarpetas divididas por objetos, donde cada subcarpeta tiene 72 imágenes correspondientes a distintas vistas de cada objeto.

La estructura de la carpeta debe verse de la siguiente manera:

<img width="72" alt="image" src="https://github.com/user-attachments/assets/c298f899-9803-49cb-ae8c-e5b61234818e">
<img width="516" alt="image" src="https://github.com/user-attachments/assets/a36ae30b-972b-48c7-8a81-265346dd44cd">



## Renombrado de Imágenes

Si las imágenes no están numeradas como `obj1_0`, `obj1_1`, etc., el programa puede renombrarlas automáticamente para cumplir con el formato adecuado.

## Requisitos

Para ejecutar este proyecto, necesitarás instalar las siguientes bibliotecas:

- `opencv-python`
- `scikit-learn`
