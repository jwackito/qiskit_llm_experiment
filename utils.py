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

def obtener_developer_prompt(version_objetivo, url_release_notes, url_changelog="https://github.com/qiskit/qiskit/releases/tag/{version}"):
	return f'''
		Eres un asistente experto en ingeniería de software cuántica, altamente capacitado en el ecosistema qiskit y sus liberaciones de versión.
        Genere una tabla Markdown con 9 columnas sobre migraciones en Qiskit:

		| Tipo de Cambio | Flujo de Cambio | Resumen | Artefactos afectados | Código Pre-Migración | Código Post-Migración | Dificultad | Impacto SE/QSE | Referencias |
		| :------------- | :-------------- | :------ | :------------------- | :------------------- | :-------------------- | :--------- | :------------- | :---------- |

		- **Columnas:**
		1. Tipo de Cambio (inserción, actualización, deprecación, cambio de estructura de módulos, nueva librería, etc)
		2. Versiones qiskit de origen y de destino
		3. Descripción concisa del escenario y su propósito
        4. Artefactos software o hardware implicados (Clase, Objeto, método, parámetro, librería externa o dependencia, lenguaje, comando, herramientas externas, dependencias, módulos del ecosistema qiskit, etc.) ej: 'qiskit-aer', 'qiskit-ibm-runtime', 'pip', matplotlib, numpy, etc.
		5/6. Código de ejemplo pre/post migración
		7. Dificultad, con valores posibles:
          	- `**Alta**`: implica cambios estructurales, complejos y relevantes
            - `**Moderada**`: implica algunos pocos, sin demasiado trabajo de refactor
            - `**Baja**`: implica modificación simple en el código, ej: renombrado de funciones o parametrizaciones
            - `**Nula**`: sin impacto ni complejidad para migrar de versión, ej: mejora interna
		8. Impacto en SE/QSE + justificación (opciones no excluyentes)
		9. Enlaces oficiales validados

		**Restricciones críticas:**
        - **Fuente de información primordial**, el usuario la indicará entre etiquetas `**<qrn></qrn>**`
		- **Formato**:
          	- **Respuesta esperada, una única tabla con sintaxis Markdown válida**
            - Columna 5/6, sólo con **código python válido**
            - Columna 2. "Flujo de Cambio"
               - `**o.o.x** → **d.d.0**` (dígito menos significativo en versión de origen: _`.x`_ y en destino: _`.0`_)
               - versión de origen ≥ 0.05.x y versión destino ≤ {version_objetivo}.0
            - Columna 7. "Dificultad", con formato: **`Alta`/`Moderada`/`Baja`/`Nula`** _(breve descripción justificativa)_ Ej: **Alta** _(requiere la instalación de paquetes)_
            - Columna 8. "Referencias", con formato: **`Release Notes`/`Changelog GitHub`/`Documentation oficial`/`Migration Guides`**, si hay más de una, separadas por salto de línea
            - **Descripción extensiva y exhaustiva de scenarios atómicos**, 1 cambio por fila incluso si:
				- Afecta un mismo módulo (ej: `QuantumCircuit.data` ≠ `QuantumCircuit.compose`)
            	- Coincide el "Tipo de Cambio": no permitir listados con "<br>+", "•" u otros separadores internos en una celda
               	- Si un cambio implica múltiples aspectos (ej: deprecación + migración), crear filas separadas
		- **Celdas opcionales**:
          	- Columna 5. "Código Pre-Migración"
            - Columna 6. "Código Post-Migración"
		- **Columna 8. "Referencias"**
          	- Hipervínculos correctos y accesibles
            - Utilizar exclusivamente **enlaces a fuentes oficiales** en este orden:
            	1. Release Notes (_`https://docs.quantum.ibm.com/api/qiskit/release-notes`_)
                2. Changelog GitHub (_`https://github.com/Qiskit/qiskit/releases/tag/{version_objetivo}.0`_)
                3. Documentation oficial (_`https://docs.quantum.ibm.com/`_)
                4. Migration Guides (_`https://docs.quantum.ibm.com/migration-guides`_)
            - No usar documentación histórica pre-{version_objetivo}.0, ni secciones: "Prelude" o "Bug Fixes"
		- **Exclusiones**:
          	- Bug Fixes, errores en versiones menores, escenarios hipotéticos y cambios sin documentacion oficial de respaldo
            - Texto contenido por fuera de la tabla solicitada, sin wrappers adicionales
    	- **Ordenamiento**, ordenar filas primero por Columna 7. "Dificultad" (Alta → Moderada → Baja → Nula), luego por Columna 8. "Impacto SE/QSE" (QSE → SE)"
                  
        - Ejemplo de filas en la tabla:
        | Nueva Librería | **0.45.x** → **1.0.0** | Introducción de librería: `qiskit-dynamics` para simulaciones | módulo: `qiskit-dynamics`, 'requirements.txt' |  | `from qiskit_dynamics import Solver` | **Alta** _(nueva dependencia)_ | **QSE** _(requiere actualizar entornos)_ | [Migration Guides](https://docs.quantum.ibm.com/migration-guides/qiskit-1.0) | 
        | Deprecación | **0.19.x** → **1.0.0** | Uso de `qiskit.execute` | método execute() en módulo qiskit | `result = execute(circuit, backend).result()` | `from qiskit import transpile; job = backend.run(transpile(circuit, backend))` | **Moderada** _(nuevo flujo de ejecución)_ | **SE** _(requiere refactorizar workflows)_ | [Release Notes](https://docs.quantum.ibm.com/api/qiskit/release-notes#1.0.0), [Migration Guides](https://docs.quantum.ibm.com/migration-guides/qiskit-1.0) |  
	'''

def obtener_user_prompt(inyectar_qiskit_release_notes, version_objetivo, file_content, url_objetivo_qrn="https://docs.quantum.ibm.com/api/qiskit/release-notes"):
    return f'''
		Genere una tabla Markdown exhaustiva para cada escenario de migración Qiskit para la versión destino: {version_objetivo}.0:

        - **Fuente Primordial de información**:
			**Qiskit Release Notes versión {version_objetivo}.0** {f": **<qrn>**{file_content}**</qrn>**" if inyectar_qiskit_release_notes else f"_{url_objetivo_qrn}_"}

		**Directivas de análisis:** 
			1. **Escenarios** (filas de la tabla):
				- Modificaciones sobre la API (clases y métodos fundamentales, parámetros y estructura)
				- Reestructuraciones de módulos (qiskit.* → qiskit_*) y migración de funcionalidades
				- Cambios en defaults/formatos de retorno (ej: dict → clase)
				- Migración a paquetes externos y nuevas librerías (ej: requiere pip install)
				- Nuevas funcionalidades, actualizaciones y deprecaciones en versión {version_objetivo}.0
			2. **Artefactos Afectados**:  
				- Clases: `QuantumCircuit`, `Transpiler` 
				- Métodos: `QuantumCircuit.bind_parameters()`  
				- Paquetes: `qiskit-terra` → `qiskit`  
				- Dependencias: `numpy ≥ 1.21`
			3. **Tipo de Cambio:**: 
				- **API**: Métodos, clases, parámetros
				- **Módulos**: Reestructuración `qiskit.*` → `qiskit_*` 
				- **Formatos**: `dict` → `QuantumResult`
				- **Dependencias**: Nueva librería (`qiskit-dynamics`) 
			4. **Criterios de Inclusión**:  
				- Filas independientes por tipo de cambio (ej: inserción ≠ actualización ≠ deprecación ≠ reestructuración)
				- Migraciones documentadas pero sin ejemplos de código origen o destino
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

def obtener_parametrizacion(model, messages, temperature):
    
    '''
    # Genérico -> chatGPT
    payload = {
        "model": model,             # Modelo LLM objetivo
        "messages": messages,       # Prompts del sistema y del usuario
        "temperature": temperature, # Máxima precisión para datos estructurados 0.25 DeepSeek
        #"top_p": 0.5,               # Balance entre cobertura y ruido
        "max_tokens": 3000,         # Capacidad para ~20-25 filas
        #"presence_penalty": 0.8,    # Evita redundancias en columnas
        #"frequency_penalty": 0.9,   # ↓ repetición de términos técnicos (ej: "QuantumCircuit")
        #"n": 1,                     # Cantiadad de respuestas resultantes
        "stream": False,            # Modalidad de flujo de datos
        #"stop": ["##", "<!--", "<!--END-->", "## Notas"]  # Delimitadores claros
    }

    '''
    
    # Payload deepseek-v3
    payload = {
        "model": model,             # Modelo LLM objetivo
        "messages":messages,		# Prompts de usuario y sistema
        "temperature": temperature, # Máxima fidelidad al formato
        "top_p": 0.01,              # Evita el sampling estocástico
        "max_tokens": 3000,         # Capacidad para tablas complejas +30 filas
        "frequency_penalty": 1.2,   # Eliminar repetición de headers
        "presence_penalty": 0.9,  	# Incentivar contenido nuevo por fila 
        "stop": ["###", "<!--", "<!--END-->", "## Notas", "**Nota**", "\n#", "```", "### Notas"],   # Prevenir markdown adicional
        "n": 1, 
        "stream": False,
        "seed": 123 
    }
    
    '''
    # Payload deepseek-r1
    payload = {
        "model": model,             # Modelo LLM objetivo
        "messages": messages,       # Prompts del sistema y del usuario
        "temperature": 0.1,         # Maximizar precisión técnica
        "top_p": 0.05,              # Enfoque estricto en fuentes oficiales
        "max_tokens": 3000,         # Tamaño típico de tablas de migración
        "frequency_penalty": 0.7,   # Reducir repetición en múltiples filas
        "presence_penalty": 0.5,    # Garantizar cobertura de componentes requeridos
        "stop": ["\n\n", "##", "<!--", "<!--END-->", "## Notas", "**Nota**"],   # Prevenir markdown adicional
        "system_prompt_ratio": 0.6, # Priorizar estructura técnica
        "stream": False,            # Modalidad de flujo de datos
        "n": 1,                     # Cantiadad de respuestas resultantes
    }
    '''
    return payload

if __name__ == "__main__":
    
    if len(sys.argv) > 1 and sys.argv[1] == "tokenizer":
        probar_tokenizer()
        
    if len(sys.argv) > 1 and sys.argv[1] == "diagrama":
        generar_diagrama()