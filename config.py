
import requests
import pandas as pd

# URL pública del archivo en Google Drive
file_url1 = 'https://drive.google.com/uc?id=132Qhtbskp0pCiVe4HjRe_Uy2VKUGtEu9'
file_url2 = 'https://drive.google.com/uc?id=1--0LShosGlQ9_Y49Amf-yA1_PhW9uG6K'
# Ruta de destino para guardar el archivo descargado
file_path1 = 'df.csv'
file_path2 = 'resumen.csv'
# Descargar el archivo desde la URL pública
response = requests.get(file_url1)

if response.status_code == 200:
    with open(file_path1, 'wb') as file:
        file.write(response.content)
    print('Archivo descargado exitosamente.')
else:
    print('Error al descargar el archivo.')


response = requests.get(file_url2)

if response.status_code == 200:
    with open(file_path2, 'wb') as file:
        file.write(response.content)
    print('Archivo descargado exitosamente.')
else:
    print('Error al descargar el archivo.')



df_csv = 'df.csv'
df = pd.read_csv(df_csv)

resumen_csv = 'resumen.csv'
resumen = pd.read_csv(resumen_csv)