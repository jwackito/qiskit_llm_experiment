import sys, os
import matplotlib.pyplot as plt
import numpy as np

def generar_diagrama():

	# Datos
	versiones = [
        "0.05.x", "0.06.x", "0.07.x", "0.08.x", "0.09.x", "0.10.x", "0.11.x", "0.12.x", "0.13.x", "0.14.x", "0.15.x", "0.16.x", "0.17.x", "0.18.x", "0.19.x", 
    	"0.20.x", "0.30.x", "0.40.x", "0.41.x", "0.42.x", "0.43.x", "0.44.x", "0.45.x", "0.46.x", 
        "1.0.x", "1.1.x", "1.2.x", "1.3.x", "1.4.x"
    ]

	cant_caracteres = [
        5800, 6100, 15500, 280, 13600, 530, 3400, 32400, 12900, 23300, 25700, 800, 1300, 48900, 25700, 
        62900, 9800, 65900, 6000, 16400, 68600, 50700, 65900, 31400, 
        67600, 58600, 39300, 63300, 13600
    ]
	tokens_gemma = [
        1459, 1667, 3857, 99, 3512, 177, 1032, 9258, 3211, 7068, 8109, 267, 390, 14772, 6302, 
        17274, 2589, 19544, 1664, 4034, 18430, 17691, 17588, 9066, 
        19010, 16220, 10520, 18032, 3758
    ]
	tokens_qween = [
        1349, 1495, 3572, 100, 3381, 174, 937, 8493, 3400, 6304, 7155, 253, 255, 13420, 6628, 
        16145, 2480, 18148, 1596, 3908, 17369, 16687, 16467, 8305, 
        17432, 14939, 9926, 16814, 3544
    ]

	x = np.arange(len(versiones))
	ancho = 0.5
	sesgo = ancho/1.7

	fig, ax = plt.subplots(figsize=(14, 7))

	# Crear barras
	rects1 = ax.bar(x, cant_caracteres, ancho, color='deepskyblue', label='Caracteres en nota de liberación Qiskit')
	rects2 = ax.bar(x - sesgo, tokens_gemma, sesgo, color='aquamarine', label='Tokens gemma-3-27b-it')
	rects3 = ax.bar(x + sesgo, tokens_qween, sesgo, color='plum', label='Tokens qween-r1-32b')

	# Personalización
	ax.set_title('Evolución de cantidad de líneas de notas de liberación y tokens', pad=20)
	ax.set_xlabel('Número de versión Qiskit')
	ax.set_ylabel('Cantidad')
	ax.set_xticks(x)
	ax.set_xticklabels(versiones, rotation=45, ha='right')
	ax.set_ylim(0, 70000)
	ax.axhline(y=45000, color='darkorange', linestyle='-', alpha=0.3, label='Documentación de liberación abundante')
	ax.legend()

	# Añadir valores
	font_size=6
	padding=3
	ax.bar_label(rects1, padding=padding, fmt='%d', fontsize=font_size, rotation=45)
	ax.bar_label(rects2, padding=padding, fmt='%d', fontsize=font_size, rotation=45)
	ax.bar_label(rects3, padding=padding, fmt='%d', fontsize=font_size, rotation=45)

	plt.tight_layout()
	plt.show()

def probar_tokenizer():

	from transformers import AutoTokenizer

	# Cargar el tokenizador de Qwen-R1-32B
	tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-32B")

	# Probar el tokenizador con un ejemplo
	input = "Hola, este es un ejemplo de tokenización en Qwen-R1-32B. hola ¿ como estas bien ?"
	tokens = tokenizer.tokenize(input)
	token_ids = tokenizer.convert_tokens_to_ids(tokens)
      
	print(f"\nSe generaron: {len(token_ids)} tokens\n")
	#print("Tokens:", tokens)
	#print("IDs de Tokens:", token_ids)
      
def obtener_ultimas_dos_secciones(ruta):
    # Normalizar la ruta para asegurar separadores consistentes
    ruta_normalizada = os.path.normpath(ruta)
    
    # Dividir la ruta en sus componentes
    partes = ruta_normalizada.split(os.sep)
    
    # Filtrar elementos vacíos y tomar los últimos dos
    partes_no_vacias = [p for p in partes if p]
    ultimas_dos = partes_no_vacias[-2:] if len(partes_no_vacias) >= 2 else partes_no_vacias
    
    # Reconstruir la subruta con el separador original
    return os.sep.join(ultimas_dos)

if __name__ == "__main__":
    
    if len(sys.argv) > 1 and sys.argv[1] == "tokenizer":
        probar_tokenizer()
        
    if len(sys.argv) > 1 and sys.argv[1] == "diagrama":
        generar_diagrama()