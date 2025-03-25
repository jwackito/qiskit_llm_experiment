import difflib

def verificar_cantidad_caracteres(scrapted_content, cantidad_caracteres):

	print(f"\nConteo de caracteres --> ", end="")

	cant_caracteres_recopilados = len(scrapted_content)
	resultado = cant_caracteres_recopilados == cantidad_caracteres
	print(
		f"cantidad de caracteres recopilados coincide con la documentación ({cantidad_caracteres})" if resultado 
		else f"cantidad de caracteres recopilados {cant_caracteres_recopilados} DIFIERE con los copiados desde la documentación {cantidad_caracteres} (diferencia = {abs(cant_caracteres_recopilados - cantidad_caracteres)})"
	)
	return resultado

def comparar_cadenas(cadena_remota, cadena_local):

    # Desactiva autojunk para detectar TODAS las diferencias
	differ = difflib.SequenceMatcher(None, cadena_remota, cadena_local, autojunk=False)
	diferencias = []

	for opcode in differ.get_opcodes():
		tipo = opcode[0]
		inicio1, fin1 = opcode[1], opcode[2]
		inicio2, fin2 = opcode[3], opcode[4]

		if tipo != 'equal':
			seg1 = cadena_remota[inicio1:fin1]
			seg2 = cadena_local[inicio2:fin2]

			# Si es una diferencia trivial, que no la considere
			if seg1.strip() == "" or seg2.strip() == "" or seg1.strip() == "\n" or seg2.strip() == "\n": continue

			diferencias.append({
				"tipo": tipo,
				"str1_pos": (inicio1, fin1),
				"str2_pos": (inicio2, fin2),
				"str1_segmento": seg1.replace("\n", "\\n"),
				"str2_segmento": seg2.replace("\n", "\\n")
			})

	return diferencias

def verificar_contenido(contenido_remoto, contenido_local):
	'''
		El contenido remoto es el que se recopiló automáticamente, 
		mientras que el local es producto de una copia manual del usuario sobre la documentación.
	'''

	print(f"\nComprobación de contenido --> ", end="")

	diferencias = comparar_cadenas(contenido_remoto, contenido_local)

	if not diferencias:
		print("cadenas idénticas")
	else:
		print(f"{len(diferencias)} diferencias encontradas:")
		for diff in diferencias:
			print(f"- En {diff['str1_pos']}: '{diff['str1_segmento']}' vs. en {diff['str2_pos']}: '{diff['str2_segmento']}'")

def verificar_documentacion(scrapted_content, version):

	print("\n---------------------   Ejecutando verificaciones   ---------------------")

	file_path = f"verificacion/qiskit_release_note_{version}.md"
	try:
		# Abre el archivo en modo lectura y carga su contenido
		with open(file_path, "r", encoding="utf-8") as archivo:
			contenido_md = archivo.read()

		verificar_cantidad_caracteres(scrapted_content, len(contenido_md))

		verificar_contenido(scrapted_content, contenido_md)

	except FileNotFoundError:
		print(f"Error: No se encontró el archivo {file_path}, necesario para establecer las comparaciones ...")
	except Exception as e:
		print(f"Error al leer el archivo: {str(e)}")
	