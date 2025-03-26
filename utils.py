import sys
import matplotlib.pyplot as plt
import numpy as np

def generar_diagrama():

	# Datos
	versiones = ["0.05.x", "0.06.x", "0.07.x", "0.08.x", "0.09.x", "0.10.x",
				"0.20.x", "0.30.x", "0.40.x", "0.46.x", "1.0.x", "1.1.x",
				"1.2.x", "1.3.x", "1.4.x"]

	cant_caracteres = [5800, 6100, 15500, 280, 13600, 530, 62900, 9800, 65900, 31400, 67600, 58600, 39300, 63300, 13600]
	tokens_gemma = [1459, 1667, 3857, 99, 3512, 177, 17274, 2589, 19544, 9066, 19010, 16220, 10520, 18032, 3758]
	tokens_qween = [1349, 1495, 3572, 100, 3381, 174, 16145, 2480, 18148, 8305, 17432, 14939, 9926, 16814, 3544]

	x = np.arange(len(versiones))
	ancho = 0.5

	fig, ax = plt.subplots(figsize=(14, 7))

	# Crear barras
	rects1 = ax.bar(x, cant_caracteres, ancho, color='deepskyblue', label='Caracteres en nota de liberación Qiskit')
	rects2 = ax.bar(x - ancho/2, tokens_gemma, ancho/2, color='aquamarine', label='Tokens gemma-3-27b-it')
	rects3 = ax.bar(x + ancho/2, tokens_qween, ancho/2, color='plum', label='Tokens qween-r1-32b')

	# Personalización
	ax.set_title('Evolución de cantidad de líneas de notas de liberación y tokens', pad=20)
	ax.set_xlabel('Número de versión Qiskit')
	ax.set_ylabel('Cantidad')
	ax.set_xticks(x)
	ax.set_xticklabels(versiones, rotation=45, ha='right')
	ax.set_ylim(0, 70000)
	ax.legend()

	# Añadir valores
	ax.bar_label(rects1, padding=3, fmt='%d', fontsize=8)
	ax.bar_label(rects2, padding=3, fmt='%d', fontsize=8)
	ax.bar_label(rects3, padding=3, fmt='%d', fontsize=8)

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

if __name__ == "__main__":
    
    if len(sys.argv) > 1 and sys.argv[1] == "tokenizer":
        probar_tokenizer()
        
    if len(sys.argv) > 1 and sys.argv[1] == "diagrama":
        generar_diagrama()