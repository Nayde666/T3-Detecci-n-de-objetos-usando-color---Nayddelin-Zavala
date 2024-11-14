import os

carpeta = "./objetos-coil-100/objeto10"
archivos = os.listdir(carpeta)

archivos_imagen = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.png')]

for i, archivo in enumerate(archivos_imagen):
    extension = archivo.split('.')[-1]
    nuevo_nombre = f"obj10_{i}.{extension}"
    ruta_actual = os.path.join(carpeta, archivo)
    nueva_ruta = os.path.join(carpeta, nuevo_nombre)
    os.rename(ruta_actual, nueva_ruta)

