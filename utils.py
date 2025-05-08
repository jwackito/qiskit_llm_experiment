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
	rects1 = ax.bar(x, cant_caracteres, ancho, color='deepskyblue', label='# Release Note characters')
	rects2 = ax.bar(x - sesgo, tokens_gemma, sesgo, color='aquamarine', label='# Google-Gemma-3-27b-it-GGUF tokens')
	rects3 = ax.bar(x + sesgo, tokens_qween, sesgo, color='plum', label='# DeepSeek-R1-Distill-Qween-32b-GGUF tokens')

	# Personalización
	ax.set_title('Evolution of character and token counts, in release notes', pad=20)
	ax.set_xlabel('Qiskit Version Number')
	ax.set_ylabel('Count')
	ax.set_xticks(x)
	ax.set_xticklabels(versiones, rotation=45, ha='right')
	ax.set_ylim(0, 70000)
	ax.axhline(y=45000, color='darkorange', linestyle='-', alpha=0.3, label='Limit on the amount of significant documentation')
	ax.legend()

	# Añadir valores
	font_size=6
	padding=3
	ax.bar_label(rects1, padding=padding, fmt='%d', fontsize=font_size, rotation=45)
	ax.bar_label(rects2, padding=padding, fmt='%d', fontsize=font_size, rotation=45)
	ax.bar_label(rects3, padding=padding, fmt='%d', fontsize=font_size, rotation=45)

	plt.tight_layout(); plt.savefig('tokens.pdf', format="pdf", dpi=300)
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
    Eres un **asistente experto en ingeniería de software cuántica, altamente capacitado en el ecosistema qiskit y sus liberaciones de versión**. Tu tarea es analizar y resumir los cambios de la versión {qiskit_vo_3d} de Qiskit, generando una tabla Markdown con información detallada sobre cada escenario de migración.
    La tabla debe contener los siguientes campos:
    | Tipo | Flujo | Resumen | Artefactos | Código Pre-Migración | Código Post-Migración | Dificultad | Impacto | Referencias |
    | :- | :-: | :- | :- | :- | :- | :- | :- | :- |
    - Columnas:
    1. **Tipo**:
        - Categoría: permite categorizar el tipo de cambio en base a su naturaleza
            Ej: Inserción, actualización, deprecación, remoción, cambio estructural, semántico, sintáctico, librería, dependencia, etc)
        - Módulo: identifica el módulo del ecosistema qiskit afectado 
            Ej: `qiskit-aer`, `qiskit-terra`, `qiskit-ibm-runtime`, etc.)
    2. **Flujo**: identifica la versión 'origen' que introdujo el artefacto afectado y la 'destino', con formato:
        - `vO.Ox → vD.D.x` (ej: `v0.44.x → v1.0.x`), último dígito (bug-fixes) no especificado "-.-.x"
        - Restricción: vO.O.x >`0.05.x` y vD.D.x = `{qiskit_vo_2d}.x`, si no se encuentra vO.O.x, utilizar la inmediatamente anterior a `{qiskit_vo_2d}.0`     
    3. **Resumen**: aclara la función principal del cambio, con formato:
        - `Descripción breve` (ej: `Cambio de nombre de clase`, `Cambio de formato de retorno`, `Nueva librería`, etc.)
        - `Descripción detallada` (ej: `Cambio de nombre de clase QuantumCircuit.data a QuantumCircuit.bind_parameters`)
    4. **Artefactos** software/hardware implicados, con formato:
        - `Clase` (ej: `QuantumCircuit`, `Transpiler`, `QuantumResult`, etc.)
    5/6. **Código Pre/Post-Migración**: código Python válido de ejemplo
    7. **Dificultad**, representa la dificultad asociada al escenario de migración, con valores posibles:
        7.1 `Alta`: implica cambios estructurales, complejos y relevantes
        7.2 `Moderada`: implica algunos pocos, sin demasiado trabajo de refactor
        7.3 `Baja`: implica una refactorización sencilla, ej: renombrado de clase, método o parámetro, etc.
        7.4 `Mínima`: sin impacto ni complejidad de migración, usualmente incrementos funcionales; ej: mejora interna,nueva funcionalidad o parámetro
        - Formato: `Alta`/`Moderada`/`Baja`/`Mínima` + (breve justificación) Ej: Alta (requiere la instalación de paquetes)
    8. **Impacto** asociado a la ingeniería de software clasica (SE) o cuántica (QSE), opciones no excluyentes, con valores posibles:
        8.1 `QSE`: el escenario afecta sobre ing. de software cuántica. Ej: compuertas, transpilación, primitivas, topologías, siumladores, etc.
        8.2 `SE`: el escenario afecta sobre ing. de software clásica. Ej: migración de módulos, jerarquía de clases, modularidad, etc.
        Formato: `QSE`/`SE` + (breve justificación) Ej: QSE (afecta operadores cuánticos), SE (mejora de modularidad)
    9. **Referencias** correctas, verificadas y accesibles, con formato:
        - `Release Notes`/`Changelog GitHub`/`Documentation oficial`/`Migration Guides`, si hay más de una, separadas por salto de línea
        - Enunciar todas las referencias halladas, separadas por salto de línea

    Restricciones críticas:
    - Fuente de información primordial a considerar, el usuario la indicará entre triple guión-bajo (`___`)
    - Atomicidad e independencia de escenarios:
        1. Evita escenarios replicados, nunca una fila de la tabla puede coincidir en columnas "Tipo de Cambio", "Resumen" y "Artefactos afectados"
        2. No permitir listados con "<br>+", "•" u otros separadores internos en una celda, excepto en "Referencias"
        4. Si implica múltiples aspectos (ej: deprecación + migración), crear filas separadas
        5. Si afecta un mismo módulo (ej: `QuantumCircuit.data` ≠ `QuantumCircuit.compose`), crear filas separadas
    - Columnas 4,8 y 9 admiten múltiples valores, separados por salto de línea
    - Columna 9. Referencias admite sólo URLs válidas, no texto adicional
    - Exclusiones:
        - Respuesta buscada, una única tabla con sintaxis Markdown válida, no incluir encabezados, wrappers, pies de página, ni texto adicional
        - Valores "N/A" o "N/D" en las columnas "Código Pre/Post-Migración", dejar celdas vacías ("")
        - `Bug Fixes`, errores en versiones menores, escenarios hipotéticos y cambios sin documentacion oficial de respaldo
        - `Prelude`, documentación histórica pre-{qiskit_vo_3d}, cambios en versiones menores, escenarios hipotéticos y cambios sin documentacion oficial de respaldo
    '''
    
    technical_terms = {
        'qiskit_vo_2d': 'qiskit_vo_2d',
        'qiskit_vo_3d': 'qiskit_vo_3d',
        'qiskit': 'qiskit',
        'Markdown': 'Markdown',
        'Release Notes': 'Release Notes',
        'Changelog GitHub': 'GitHub Changelog',
        'Migration Guides': 'Migration Guides',
        'QuantumCircuit.data': 'QuantumCircuit.data',
        'SE/QSE': 'SE/QSE',
        'wrappers': 'wrappers',
        'qiskit-aer': 'qiskit-aer',
        'Bug Fixes': 'Bug Fixes',
        'qiskit-dynamics': 'qiskit-dynamics',
        'qiskit-ibm-runtime': 'qiskit-ibm-runtime',
        'Prelude': 'Prelude',
    }

    params = {
         "qiskit_vo_2d": version_objetivo, "QISKIT_VO_2D": version_objetivo,
         "qiskit_vo_3d": f"{version_objetivo}.0", "QISKIT_VO_3D": f"{version_objetivo}.0",
    }

    prompt_traducido = traducir(base_prompt, idioma, technical_terms, params)

    return prompt_traducido

def obtener_user_prompt(inyectar_qiskit_release_notes, version_objetivo, file_content, idioma="es") -> str:
    
    base_prompt = '''
		Genera una tabla en formato Markdown lo más exhaustiva, abarcativa, descriptiva y completa posible, para cada escenario de migración qiskit:
        - **Fuente Primordial de información**:
			{qrn}
        - **Fuente Secundaria de información**:
            1. Release Notes (`https://docs.quantum.ibm.com/api/qiskit/release-notes/{qiskit_vo_2d}`)
            2. Changelog GitHub (`https://github.com/Qiskit/qiskit/releases/tag/{qiskit_vo_3d}`)
            3. Documentation oficial (`https://docs.quantum.ibm.com/`)
            4. Migration Guides (`https://docs.quantum.ibm.com/migration-guides`)
                    
        **Ejemplo paradigmatico de escenario**: 
        | Nueva librería | 0.44.x → 1.0.x | Introducción de librería: `qiskit-dynamics` en simulaciones | módulo `qiskit-dynamics` |  | `from qiskit_dynamics import Solver` | Alta (requiere instalar la nueva dependencia) | QSE (requiere actualizar entornos) | [Release Notes](https://docs.quantum.ibm.com/api/qiskit/release-notes#1.0.0) \n [Migration Guides](https://docs.quantum.ibm.com/migration-guides/qiskit-1.0) |
   '''
    
    technical_terms = {
        'qiskit': 'qiskit',
        'qiskit_vo_3d': 'qiskit_vo_3d',
        'qiskit_vo_2d': 'qiskit_vo_2d',
        'qrn': 'qrn',
        'Markdown': 'Markdown',
        'Release Notes': 'Release Notes',
        'Changelog GitHub': 'GitHub Changelog',
        'Migration Guides': 'Migration Guides',
        'Transpiler': 'Transpiler',
        'QuantumResult': 'QuantumResult'
    }

    params = {
         "qiskit_vo_2d": version_objetivo, "QISKIT_VO_2D": version_objetivo,
         "qiskit_vo_3d": f"{version_objetivo}.0", "QISKIT_VO_3D": f"{version_objetivo}.0",
         "qrn": f"\n___{file_content}___\n" if inyectar_qiskit_release_notes else f"https://docs.quantum.ibm.com/api/qiskit/release-notes/{version_objetivo}",
         "QRN": f"\n___{file_content}___\n" if inyectar_qiskit_release_notes else f"https://docs.quantum.ibm.com/api/qiskit/release-notes/{version_objetivo}"
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