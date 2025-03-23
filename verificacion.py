import difflib

def verificar_cantidad_caracteres(scrapted_content, cantidad_caracteres):

	print(f"Conteo de caracteres --> ", end="")

	cant_caracteres_recopilados = len(scrapted_content)
	resultado = cant_caracteres_recopilados == cantidad_caracteres
	print(
		f"cantidad de caracteres recopilados coincide con la documentación ({cantidad_caracteres})" if resultado 
		else f"cantidad de caracteres recopilados {cant_caracteres_recopilados} DIFIERE con los copiados desde la documentación {cantidad_caracteres} (diferencia = {abs(cant_caracteres_recopilados - cantidad_caracteres)})"
	)
	return resultado

def comparar_cadenas(cadena1, cadena2):

    # Desactiva autojunk para detectar TODAS las diferencias
	differ = difflib.SequenceMatcher(None, cadena1, cadena2, autojunk=False)
	diferencias = []

	for opcode in differ.get_opcodes():
		tipo = opcode[0]
		inicio1, fin1 = opcode[1], opcode[2]
		inicio2, fin2 = opcode[3], opcode[4]

		if tipo != 'equal':
			seg1 = cadena1[inicio1:fin1]
			seg2 = cadena2[inicio2:fin2]
			diferencias.append({
				"tipo": tipo,
				"str1_pos": (inicio1, fin1),
				"str2_pos": (inicio2, fin2),
				"str1_segmento": seg1,
				"str2_segmento": seg2
			})

	return diferencias

def verificar_contenido(contenido_remoto, contenido_local):

	print(f"Comprobación de contenido --> ", end="")

	diferencias = comparar_cadenas(contenido_remoto, contenido_local)

	if not diferencias:
		print("cadenas idénticas")
	else:
		print("diferencias encontradas:")
		for diff in diferencias:
			print(f"- En {diff['str1_pos']}: '{diff['str1_segmento']}' <--> en {diff['str2_pos']}: '{diff['str2_segmento']}'")

def verificar_documentacion(scrapted_content, version):

	print("\nEjecutando verificaciones ... ")

	file_path = f"verificacion/qiskit_release_note_{version}.md"
	try:
		# Abre el archivo en modo lectura y carga su contenido
		with open(file_path, "r", encoding="utf-8") as archivo:
			contenido_md = archivo.read()

		verificar_cantidad_caracteres(scrapted_content, len(contenido_md))

		verificar_contenido(scrapted_content, contenido_md)

	except FileNotFoundError:
		print(f"Error: El archivo '{file_path}' no existe.")
	except Exception as e:
		print(f"Error al leer el archivo: {str(e)}")
	