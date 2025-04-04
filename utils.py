import sys, os, json
import matplotlib.pyplot as plt
import numpy as np
from deep_translator import GoogleTranslator

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

def obtener_system_prompt(version_objetivo, idioma="es") -> str:

    base_prompt = '''
    Eres un asistente experto en ingeniería de software cuántica, altamente capacitado en el ecosistema qiskit y sus liberaciones de versión. 
    Genere una tabla Markdown con 9 columnas:
    | Tipo de Cambio | Flujo de Cambio | Resumen | Artefactos afectados | Código Pre-Migración | Código Post-Migración | Dificultad | Impacto SE/QSE | Referencias |
    | :- | :-: | :- | :- | :- | :- | :-: | :-: | :- |
    - Columnas:
    1. Tipo de Cambio (inserción, actualización, deprecación, cambio de estructura de módulos, nueva librería, etc)
    2. Flujo de Cambio: versiones qiskit, origen y destino, la versión de origen es la última versión estable anterior a la versión destino, ej: `0.44.x → 1.0.0` (dígito menos significativo: `.x`)
    3. Resumen del cambio, con formato: `Tipo de Cambio` + `Descripción breve`
    4. Artefactos software/hardware implicados, con formato:
        - `Clase` (ej: `QuantumCircuit`, `Transpiler`, `QuantumResult`, etc.)
    5/6. Código de ejemplo pre/post migración
    7. Dificultad, representa la dificultad asociada al escenario de migración, con valores posibles:
    7.1 `Alta`: implica cambios estructurales, complejos y relevantes
    7.2 `Moderada`: implica algunos pocos, sin demasiado trabajo de refactor
    7.3 `Baja`: implica una refactorización sencilla, ej: renombrado de clase, método o parámetro, etc.
    7.4 `Mínima`: sin impacto ni complejidad de migración, usualmente incrementos funcionales; ej: mejora interna,nueva funcionalidad o parámetro
    8. Impacto asociado a la ingeniería de software clasica (SE) o cuántica (QSE), con valores posibles:
    8.1 `QSE`: afecta a la ing. de software cuántica, ej: compuertas, transpilación, primitivas, topologías, siumladores, etc.
    8.2 `SE`: afecta a la ing. de software clásica, ej: migración de módulos, jerarquía de clases, modularización de componentes, etc. 
    - Estas opciones no son exclusivas, es decir, un mismo escenario puede agrupar ambas
    9. Enlaces oficiales validados
    Restricciones críticas:
    - Fuente de información primordial a considerar, el usuario la indicará entre triple guión-bajo (___)
    - No admitas escenarios replicados, nunca una fila de la tabla puede coincidir en columnas "Tipo de Cambio", "Resumen" y "Artefactos afectados"
    - Formato:
    - **Respuesta esperada, una única tabla con sintaxis Markdown válida**
    - Columna 5/6, sólo con **código python válido**
    - Columna 2. "Flujo de Cambio"
    - `o.o.x → d.d.x` (dígito menos significativo: `.x`)
    - versión de origen ≥ 0.05.x y versión destino ≤ {qiskit_vo}.0
    - Columna 7. "Dificultad", con formato: `Alta`/`Moderada`/`Baja`/`Mínima` + breve descripción justificativa entre paréntesis Ej: Alta (requiere la instalación de paquetes)
    - Columna 8. "Referencias", con formato: **`Release Notes`/`Changelog GitHub`/`Documentation oficial`/`Migration Guides`**, si hay más de una, separadas por salto de línea
    - Descripción abarcativa, exhaustiva y completa de todos los scenarios descriptos atómicamente, 1 cambio por fila incluso si:
    - Afecta un mismo módulo (ej: `QuantumCircuit.data` ≠ `QuantumCircuit.compose`)
    - Coincide el "Tipo de Cambio": no permitir listados con "<br>+", "•" u otros separadores internos en una celda
    - Si un cambio implica múltiples aspectos (ej: deprecación + migración), crear filas separadas
    - Celdas opcionales, utiliza ejemplos validados pero si no encuentra mantenlas vacías:
    - Columna 5. "Código Pre-Migración", columna vacía o con código python válido
    - Columna 6. "Código Post-Migración", columna vacía o con código python válido
    - Columna 9. "Referencias", enlaces a Release Notes, Changelog GitHub, Documentation oficial o Migration Guides
    - Hipervínculos correctos y accesibles
    - Utilizar exclusivamente **enlaces a fuentes oficiales** en este orden:
        1. Release Notes (`https://docs.quantum.ibm.com/api/qiskit/release-notes`)
        2. Changelog GitHub (`https://github.com/Qiskit/qiskit/releases/tag/{qiskit_vo}.0`)
        3. Documentation oficial (`https://docs.quantum.ibm.com/`)
        4. Migration Guides (`https://docs.quantum.ibm.com/migration-guides`)
    - No usar documentación histórica pre-{qiskit_vo}.0, ni secciones: "Prelude" o "Bug Fixes"
    - Intenta enunciar todas las referencias halladas específicamente, no te limites a una sola, si existen varias, enuncialas
    - Exclusiones:
    - Bug Fixes, errores en versiones menores, escenarios hipotéticos y cambios sin documentacion oficial de respaldo
    - Texto contenido por fuera de la tabla solicitada, sin wrappers adicionales
    - **Ejemplo paradigmático**: | Nueva librería | 0.44.x → 1.0.0 | Introducción de librería: `qiskit-dynamics` en simulaciones | módulo `qiskit-dynamics` |  | `from qiskit_dynamics import Solver` | Alta (nueva dependencia) | QSE (requiere actualizar entornos) | [Release Notes](https://docs.quantum.ibm.com/api/qiskit/release-notes#1.0.0) [Migration Guides](https://docs.quantum.ibm.com/migration-guides/qiskit-1.0) |'''
    
    technical_terms = {
        'qiskit': 'qiskit',
        'Markdown': 'Markdown',
        'Release Notes': 'Release Notes',
        'Changelog GitHub': 'GitHub Changelog',
        'Migration Guides': 'Migration Guides',
        'QuantumCircuit.data': 'QuantumCircuit.data',
        'SE/QSE': 'SE/QSE',
        'qiskit-aer': 'qiskit-aer'
    }

    params = {
         "qiskit_vo": version_objetivo
    }

    prompt_traducido = traducir(base_prompt, idioma, technical_terms, params)
    #print(f"Prompt de sistema: \n {prompt_traducido}")
    return prompt_traducido

def obtener_user_prompt(inyectar_qiskit_release_notes, version_objetivo, file_content, idioma="es") -> str:
    
    base_prompt = '''
		Genera una tabla Markdown lo más exhaustiva, abarcativa y completa posible, para cada escenario de migración Qiskit para la versión destino: {qiskit_vo}.0:
        - Fuente Primordial de información:
			Qiskit Release Notes versión {qiskit_vo}.0: {qrn}
		Directivas de análisis: 
			1. Escenarios (filas de la tabla):
				- Modificaciones sobre la API (clases y métodos fundamentales, parámetros y estructura)
				- Reestructuraciones de módulos (qiskit.* → qiskit_*) y migración de funcionalidades
				- Cambios en defaults/formatos de retorno (ej: dict → clase)
				- Migración a paquetes externos y nuevas librerías (ej: requiere pip install)
				- Nuevas funcionalidades, actualizaciones y deprecaciones en versión {qiskit_vo}.0
			2. Artefactos Afectados:  
				- Clases: `QuantumCircuit`, `Transpiler` 
				- Métodos: `QuantumCircuit.bind_parameters()`  
				- Paquetes: `qiskit-terra` → `qiskit`  
				- Dependencias: `numpy ≥ 1.21`
			3. Tipo de Cambio:: 
				- **API**: Métodos, clases, parámetros
				- **Módulos**: Reestructuración `qiskit.*` → `qiskit_*` 
				- **Formatos**: `dict` → `QuantumResult`
				- **Dependencias**: Nueva librería (`qiskit-dynamics`) 
			4. Criterios de Inclusión:  
				- Filas independientes por tipo de cambio (ej: inserción ≠ actualización ≠ deprecación ≠ reestructuración)
				- Migraciones documentadas pero sin ejemplos de código origen o destino
   '''
    
    technical_terms = {
        'qiskit': 'qiskit',
        'Markdown': 'qiskit-terra',
        'Release Notes': 'Release Notes',
        'Changelog GitHub': 'GitHub Changelog',
        'Migration Guides': 'Migration Guides',
        'Transpiler': 'Transpiler'
    }

    params = {
         "qiskit_vo": version_objetivo,
         "qrn": f"\n\n___{file_content}___\n\n" if inyectar_qiskit_release_notes else f"https://docs.quantum.ibm.com/api/qiskit/release-notes/{version_objetivo}"
    }
    
    prompt_traducido = traducir(base_prompt, idioma, technical_terms, params)
    #print(f"Prompt de usuario: \n {prompt_traducido}")
    return prompt_traducido

def traducir(contenido: str, idioma: str = "es", terminos_tecnicos: dict = {}, params: dict = {}):

    if idioma != "es":
        # Traducir contenido principal
        translated = GoogleTranslator(source='auto', target=idioma).translate(contenido)
        final_prompt = translated
        
        # Reemplazar términos técnicos
        for term, replacement in terminos_tecnicos.items():
            term_traducido = GoogleTranslator(source='es', target=idioma).translate(term)
            final_prompt = final_prompt.replace(term_traducido, replacement)
    else:
        final_prompt = contenido
    
    return final_prompt.format(**params) if params else final_prompt

def apto_md(contenido):
    return contenido.replace("```markdown", "", 1).rstrip("```").strip()

def guardar_metadata_completion(completion, path, filename, params):

    path_metadata = os.path.join(path, "metadata")
    file_metadata_path = os.path.join(path_metadata, filename + ".json")

    if not os.path.exists(path_metadata):
        os.makedirs(path_metadata, exist_ok=True)

    with open(file_metadata_path, 'w', encoding='utf-8') as f:
        # Asumiendo que 'completion' es un objeto de OpenAI u similar
        completion_dict = completion.to_dict()

        # Añado la info de la solicitud
        completion_dict["temperature"] = params['temperature']
        #completion_dict["top_p"] = params['top_p']
        completion_dict["max_tokens"] = params['max_tokens']
        #completion_dict["frequency_penality"] = params['frequency_penality']
        #completion_dict["presence_penality"] = params['presence_penality']
        completion_dict["n"] = params['n']
        completion_dict["stream"] = params['stream']
        completion_dict["seed"] = params['seed']

        json.dump(completion_dict, f, indent=2, ensure_ascii=False)
        print(f"\n[OK] Archivo de metadata de solicitud 'completion' creado exitosamente en: {obtener_ultimas_dos_secciones(file_metadata_path)}")

def obtener_parametrizacion():

	return {
		"model": os.getenv("MODEL", "gpt-4"),
		"temperature": float(os.getenv("TEMPERATURE", 0.5)),
		"top_p": float(os.getenv("TOP_P", 1.0)),
		"max_tokens": int(os.getenv("MAX_TOKENS", 1000)),
		"frequency_penalty": float(os.getenv("FREQUENCY_PENALTY", 0.0)),
		"presence_penalty": float(os.getenv("PRESENCE_PENALTY", 0.0)),
		"stop": json.loads(os.getenv("STOP", "[]")),
		"n": int(os.getenv("N", 1)),
		"stream": os.getenv("STREAM", "false").lower() == "true",
		"seed": int(os.getenv("SEED", 42)),
		"reasoning_effort": float(os.getenv("REASONING_EFFORT", 1.0))
	}

def guardar_respuesta(completion, llm_answers_dir, file_name):

	file_answer_path = os.path.join(llm_answers_dir, file_name + ".md")
	path_acortado = obtener_ultimas_dos_secciones(file_answer_path)

	with open(file_answer_path, 'w', encoding='utf-8') as f:
		# Asumiendo que 'completion' es un objeto de OpenAI u similar
		contenido = completion.choices[0].message.content
		if contenido:
			f.write(apto_md(contenido))
			print(f"\n[OK] Archivo guardado en: {path_acortado}")
		else:
			print("\n[ERROR] El contenido está vacío o no existe")
                  
	return path_acortado


if __name__ == "__main__":
    
    if len(sys.argv) > 1 and sys.argv[1] == "tokenizer":
        probar_tokenizer()
        
    if len(sys.argv) > 1 and sys.argv[1] == "diagrama":
        generar_diagrama()