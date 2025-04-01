import sys, os, json
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

def obtener_system_prompt(version_objetivo, url_release_notes, url_changelog="https://github.com/qiskit/qiskit/releases/tag/{version}"):
	return f'''
		Genere una tabla Markdown con 8 columnas sobre migraciones en Qiskit:

		| Tipo de Cambio | Flujo de Cambio | Resumen | Código Pre-Migración | Código Post-Migración | Dificultad | Impacto SE/QSE | Referencias |
		|----------------|-------------------------------------|---------|----------------------|-----------------------|------------|----------------|-------------|

		- **Columnas:**  
		1. Tipo de Cambio (inserción, actualización, deprecación, cambio de estructura de módulos, nueva librería, etc.; excluir Bug Fixes)  
		2. Versiones en formato `**o.o.x** → **d.d.x**` (excluir último dígito de versión indicando ".x")
		3. Descripción concisa del escenario y los módulos, clases, objetos, artefactos, librerías o lenguajes implicados
		4/5. Fragmentos de código (solo si existen fuentes verificadas)  
		6. Dificultad (`Alta/Moderada/Baja/Nula`) + justificación breve  
		7. Impacto en SE/QSE + justificación (opciones no excluyentes)
		8. Enlaces oficiales validados  

		**Requisitos:**  
		1. **Componentes:** QuantumCircuit, Transpiler, Primitives, Providers, Terra/Aer/Ignis/Experiments, Operadores, PassManagers, Visualización.  
		2. **Tipos de cambios:** Deprecaciones, herencia, migración de funciones, modificaciones de firmas, reestructuraciones de paquetes, serialización, modelos de datos.  
		3. **Condición crítica en Columna "Flujo de Cambio":** Origen ≥ 0.05.x y destino ≤ {version_objetivo}.0.  
		4. **Priorizar:** 
		- Casos paradigmáticos y cambios disruptivos (api, transpilador, parámetros, métodos, reestructuraciones, migraciones, deprecaciones)  
		

		**Restricciones críticas:**  
		- Solo tabla Markdown válida (sin texto adicional)  
		- Celdas vacías permitidas solo en **columnas de código de ejemplo** (4/5)
		- **Referencias** 
          	- Hipervínculos correctos y accesibles
            - Utilizar exclusivamente **enlaces a fuentes oficiales** en este orden: Release Notes > Changelog > Documentation > Migration Guides  
		- Excluir Bug Fixes, escenarios hipotéticosy cambios sin documentacion oficial de respaldo
        - Celdas vacías permitidas solo en código pre/post
		- Sintaxis Markdown válida (sin wrappers adicionales)
    	- **Ordenamiento de filas**: la tabla final DEBE estar ordenada por:  
  			1. Columna "Dificultad" 6:  "Alta" > "Moderada" > "Baja" > "Nula"  
  			2. Columna "Tipo de Cambio" "Inserción" > "Actualización" > "Deprecación"  
			- Mantener este orden incluso si contradice otros criterios de visualización 
        	- No usar funciones de sorting Markdown (ej: <!-- SORT -->), aplicar orden directamente en generación de los datos
    	- **No incluir ningún texto externo a la tabla**, toda respuesta debe ser contenida en la tabla
		- **Formato celda**: Texto conciso sin saltos de línea. Si un cambio implica múltiples aspectos (ej: deprecación + migración), crear filas separadas. No admitir celdas con valor "N/A", si no hay datos indicar ""
        - **Descripción de scenarios atómicos y extensiva**, 1 cambio por fila incluso si:  
			- Afecta mismo módulo (ej: `QuantumCircuit.data` ≠ `QuantumCircuit.compose`)  
            - Coincide el "tipo de cambio": no permitir listados con "<br>+", "•", u otros separadores internos en una celda  
		**Fuentes Prioritarias**:  
		- Release Notes Oficiales ({url_release_notes})  
		- Changelog de GitHub ({url_changelog})  
		- No usar documentación histórica pre-{version_objetivo}.0
	'''

def obtener_user_prompt(inyectar_qiskit_release_notes, version_objetivo, file_content, url_objetivo_qrn="", 
                        url_changelog_qGitHub="https://github.com/qiskit/qiskit/releases/tag/{version}"):
    return f'''
    Genere una tabla Markdown exhaustiva para cada escenario de migraciones Qiskit para la versión destino: {version_objetivo}.0: 

	**Tipos de Cambio Prioritarios:**  	 
	- Modificaciones sobre la API (clases y métodos fundamentales, parámetros y estructura)
	- Reestructuraciones de módulos (qiskit.* → qiskit_*)
	- Cambios en defaults/formatos de retorno (ej: dict → clase)
	- Migración a paquetes externos y nuevas librerías (ej: requiere pip install)
    - Deprecaciones con remoción en versión {version_objetivo}.0
    - Nuevas funcionalidades y actualizaciones en versión {version_objetivo}.0

	**Directivas de Análisis:**  
	1. **Fuentes Primarias**:  
	- **Release notes Qiskit** (versión {version_objetivo}.0) {f": _{file_content}_" if inyectar_qiskit_release_notes else f"_{url_objetivo_qrn}_"}  
	- **Changelog oficial GitHub** (versión {version_objetivo}.0: _{url_changelog_qGitHub}_)  

	2. **Criterios de Inclusión**:  
	- Filas independientes por tipo de cambio (ej: inserción ≠ actualización ≠ deprecación ≠ reestructuración)  
	- Incluir cambios documentados pero sin ejemplos de código origen o destino
	- Dependencias críticas (numpy ≥ 1.2x, pip, matplotlib, etc)  
    - Lenguajes, librerías, funcionalidades, herramientas externas, etc.
    
    **Ejemplo paradigmático de un escenario** (un ejemplo de fila en la tabla):
	- Reestructuración de paquetes	| 0.05.x → {version_objetivo}.x | qiskit-terra → qiskit (core) |	pip install qiskit-terra |	pip install qiskit | Alta  (involucra instalación de paquetes) | SE/QSE (requiere entorno virtual nuevo) | Qiskit 1.0 Packaging Migration, Qiskit release notes 1.0 y Migration Guide
   '''

def apto_md(contenido):
    return contenido.replace("```markdown", "", 1).rstrip("```").strip()

def guardar_metadata_completion(completion, path, filename, payload):

    path_metadata = os.path.join(path, "metadata")
    file_metadata_path = os.path.join(path_metadata, filename + ".json")

    if not os.path.exists(path_metadata):
        os.makedirs(path_metadata, exist_ok=True)

    with open(file_metadata_path, 'w', encoding='utf-8') as f:
        # Asumiendo que 'completion' es un objeto de OpenAI u similar
        completion_dict = completion.to_dict()

        # Añado la info de la solicitud
        completion_dict["temperature"] = payload['temperature']
        completion_dict["max_tokens"] = payload['max_tokens']
        completion_dict["stream"] = payload['stream']

        json.dump(completion_dict, f, indent=2, ensure_ascii=False)
        print(f"\n[OK] Archivo de metadata de solicitud 'completion' creado exitosamente en: {obtener_ultimas_dos_secciones(file_metadata_path)}")

if __name__ == "__main__":
    
    if len(sys.argv) > 1 and sys.argv[1] == "tokenizer":
        probar_tokenizer()
        
    if len(sys.argv) > 1 and sys.argv[1] == "diagrama":
        generar_diagrama()