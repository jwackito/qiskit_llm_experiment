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

def obtener_system_prompt(version_objetivo: str, idioma: str = "es") -> str:
    """
    Genera un prompt de sistema detallado para crear tablas de migración de Qiskit en Markdown.
    
    Args:
        version_objetivo: Versión objetivo de Qiskit (ej: "0.30").
        idioma: Idioma del prompt ("es" para español, otro valor para inglés).
    
    Returns:
        String con el prompt formateado.
    """
    # URLs base reutilizables
    URLS = {
        "release_notes": "https://docs.quantum.ibm.com/api/qiskit/release-notes",
        "github_releases": f"https://github.com/Qiskit/qiskit/releases/tag/{version_objetivo}.0",
        "documentation": "https://docs.quantum.ibm.com/",
        "migration_guides": "https://docs.quantum.ibm.com/migration-guides"
    }

    # Estructura bilingüe modular
    PROMPT_STRUCTURE = {
        "es": {
            "header": "Eres un asistente experto en ingeniería de software cuántica, altamente capacitado en el ecosistema Qiskit y sus liberaciones de versión.",
            "table_header": "| Tipo de Cambio | Flujo de Cambio | Resumen | Artefactos afectados | Código Pre-Migración | Código Post-Migración | Dificultad | Impacto SE/QSE | Referencias |",
            "table_alignment": "| :- | :-: | :- | :- | :- | :- | :-: | :-: | :- |",
            "sections": {
                "columns": [
                    "1. **Tipo de Cambio**: (inserción, actualización, deprecación, cambio de estructura de módulos, nueva librería, etc)",
                    "2. **Flujo de Cambio**: Versiones Qiskit de origen y destino",
                    "3. **Resumen**: Descripción concisa del escenario y su propósito",
                    "4. **Artefactos afectados**: (Clases, métodos, parámetros, librerías, dependencias, etc.)",
                    "5/6. **Código**: Ejemplos pre/post migración (sólo Python válido)",
                    "7. **Dificultad**: `Alta`/`Moderada`/`Baja`/`Nula` con justificación",
                    "8. **Impacto**: `SE` (clásico) o `QSE` (cuántico) con justificación",
                    "9. **Referencias**: Enlaces oficiales validados"
                ],
                "restrictions": [
                    "**Fuente primaria**: Indicada por el usuario entre triple comillas (```)",
                    "**Sin escenarios duplicados**: Unique key = (Tipo de Cambio + Resumen + Artefactos)",
                    "**Formato estricto**:",
                    "- Versiones: `**o.o.x** → **d.d.0**` (origen ≥ 0.05.x, destino ≤ {version_objetivo}.0)",
                    "- Dificultad: **Alta** _(requiere instalación de paquetes)_",
                    "- Referencias: `Release Notes`/`Changelog GitHub`/`Documentation oficial`/`Migration Guides`",
                    "**Atomicidad**: 1 cambio por fila incluso si afecta el mismo módulo",
                    "**Exclusiones**: Bug fixes, cambios menores sin documentación oficial"
                ],
                "example": (
                    "| Nueva Librería | **0.45.x** → **1.0.0** | Introducción de `qiskit-dynamics` | "
                    "`qiskit-dynamics`, `requirements.txt` |  | `from qiskit_dynamics import Solver` | "
                    "**Alta** _(nueva dependencia)_ | **QSE** _(actualizar entornos)_ | "
                    f"[Release Notes]({URLS['release_notes']}#1.0.0) [Migration Guides]({URLS['migration_guides']}/qiskit-1.0) |"
                )
            }
        },
        "en": {
            "header": "You are an expert quantum software engineering wizard, highly skilled in the Qiskit ecosystem and its version releases.",
            "table_header": "| Change Type | Change Flow | Summary | Affected Artifacts | Pre-Migration Code | Post-Migration Code | Difficulty | SE/QSE Impact | References |",
            "table_alignment": "| :- | :-: | :- | :- | :- | :- | :-: | :-: | :- |",
            "sections": {
                "columns": [
                    "1. **Type of Change**: (insert, update, deprecation, module structure change, new library, etc)",
                    "2. **Change Flow**: Source and target Qiskit versions",
                    "3. **Summary**: Concise scenario description and purpose",
                    "4. **Affected Artifacts**: (Classes, methods, parameters, libraries, dependencies, etc.)",
                    "5/6. **Code**: Pre/post migration examples (valid Python only)",
                    "7. **Difficulty**: `High`/`Moderate`/`Low`/`None` with justification",
                    "8. **Impact**: `SE` (classical) or `QSE` (quantum) with justification",
                    "9. **References**: Validated official links"
                ],
                "restrictions": [
                    "**Primary source**: Provided by user in triple quotes (```)",
                    "**No duplicates**: Unique key = (Change Type + Summary + Affected Artifacts)",
                    "**Strict format**:",
                    "- Versions: `**o.o.x** → **d.d.0**` (source ≥ 0.05.x, target ≤ {version_objetivo}.0)",
                    "- Difficulty: **High** _(requires package installation)_",
                    "- References: `Release Notes`/`Changelog GitHub`/`Official Documentation`/`Migration Guides`",
                    "**Atomicity**: 1 change per row even if same module affected",
                    "**Exclusions**: Bug fixes, minor changes without official docs"
                ],
                "example": (
                    "| New Library | **0.45.x** → **1.0.0** | Introduction of `qiskit-dynamics` | "
                    "`qiskit-dynamics`, `requirements.txt` |  | `from qiskit_dynamics import Solver` | "
                    "**High** _(new dependency)_ | **QSE** _(environment updates)_ | "
                    f"[Release Notes]({URLS['release_notes']}#1.0.0) [Migration Guides]({URLS['migration_guides']}/qiskit-1.0) |"
                )
            }
        }
    }

    # Selección de idioma
    lang = "es" if idioma.lower() == "es" else "en"
    content = PROMPT_STRUCTURE[lang]
    
    # Construcción del prompt
    prompt_parts = [
        content["header"],
        f"\nGenera una tabla Markdown con 9 columnas sobre migraciones en Qiskit {version_objetivo}.0:" if lang == "es" else f"\nGenerate a Markdown table with 9 columns about Qiskit {version_objetivo}.0 migrations:",
        f"\n{content['table_header']}",
        content["table_alignment"],
        "\n- **Columnas:**" if lang == "es" else "\n- **Columns:**",
        *[f"  {item}" for item in content["sections"]["columns"]],
        "\n**Restricciones críticas:**" if lang == "es" else "\n**Critical restrictions:**",
        *[f"- {item.replace('{version_objetivo}', version_objetivo)}" for item in content["sections"]["restrictions"]],
        "\n**Ejemplo:**" if lang == "es" else "\n**Example:**",
        content["sections"]["example"]
    ]

    return "\n".join(prompt_parts)

def obtener_user_prompt(
            			inyectar_qiskit_release_notes: bool, 
						version_objetivo: str, 
                       	file_content: str = "", 
                       	idioma: str = "es"
) -> str:
    """
    Genera un prompt detallado para crear tablas Markdown de migración de Qiskit.
    
    Args:
        inyectar_qiskit_release_notes: Si True, incluye el contenido del archivo directamente.
        version_objetivo: Versión objetivo de Qiskit (ej: "0.30").
        file_content: Contenido de las release notes (opcional si inyectar_qiskit_release_notes es True).
        idioma: Idioma del prompt ("es" para español, otro valor para inglés).
    
    Returns:
        String con el prompt formateado.
    """
    # Constantes reutilizables
    URL_BASE = "https://docs.quantum.ibm.com/api/qiskit/release-notes"
    url_completa = f"{URL_BASE}/{version_objetivo}.0"
    
    # Plantillas comunes
    fuente_info = (
        f"```{file_content}```" if inyectar_qiskit_release_notes 
        else f"_[{url_completa}]({url_completa})_"
    )
    
    # Estructura común bilingüe
    estructura = {
        "es": {
            "titulo": f"Genera una tabla Markdown exhaustiva para migraciones Qiskit {version_objetivo}.0",
            "fuente": f"**Fuente Primordial**: Qiskit Release Notes {version_objetivo}.0 {fuente_info}",
            "directivas": [
                "**Escenarios** (filas de la tabla):",
                "- Modificaciones sobre la API (clases, métodos, parámetros)",
                "- Reestructuraciones de módulos (qiskit.* → qiskit_*)",
                "- Cambios en defaults/formatos de retorno (ej: dict → clase)",
                "- Migración a paquetes externos (requiere pip install)",
                "- Nuevas funcionalidades y deprecaciones",
                
                "\n**Artefactos Afectados**:",
                "- Clases: `QuantumCircuit`, `Transpiler`",
                "- Métodos: `QuantumCircuit.bind_parameters()`",
                "- Paquetes: `qiskit-terra` → `qiskit`",
                "- Dependencias: `numpy ≥ 1.21`",
                
                "\n**Tipo de Cambio**:",
                "- **API**: Métodos, clases, parámetros",
                "- **Módulos**: Reestructuración de imports",
                "- **Formatos**: `dict` → `QuantumResult`",
                "- **Dependencias**: Nueva librería (`qiskit-dynamics`)",
                
                "\n**Criterios de Inclusión**:",
                "- Filas independientes por tipo de cambio",
                "- Incluir migraciones sin ejemplos de código"
            ]
        },
        "en": {
            "titulo": f"Generate a comprehensive Markdown table for Qiskit {version_objetivo}.0 migrations",
            "fuente": f"**Primary Source**: Qiskit Release Notes {version_objetivo}.0 {fuente_info}",
            "directivas": [
                "**Scenarios** (table rows):",
                "- API modifications (classes, methods, parameters)",
                "- Module restructures (qiskit.* → qiskit_*)",
                "- Defaults/return formats changes (e.g. dict → class)",
                "- Migration to external packages (pip install required)",
                "- New features and deprecations",
                
                "\n**Affected Artifacts**:",
                "- Classes: `QuantumCircuit`, `Transpiler`",
                "- Methods: `QuantumCircuit.bind_parameters()`",
                "- Packages: `qiskit-terra` → `qiskit`",
                "- Dependencies: `numpy ≥ 1.21`",
                
                "\n**Type of Change**:",
                "- **API**: Methods, classes, parameters",
                "- **Modules**: Import restructuring",
                "- **Formats**: `dict` → `QuantumResult`",
                "- **Dependencies**: New library (`qiskit-dynamics`)",
                
                "\n**Inclusion Criteria**:",
                "- Separate rows by change type",
                "- Include migrations without code examples"
            ]
        }
    }
    
    # Selección de idioma
    lang = "es" if idioma.lower() == "es" else "en"
    contenido = estructura[lang]
    
    # Construcción del prompt
    prompt_lines = [
        f"{contenido['titulo']}:",
        f"\n{contenido['fuente']}",
        "\n**Analysis Directives:**" if lang == "en" else "\n**Directivas de análisis:**",
        *contenido['directivas']
    ]
    
    return "\n".join(prompt_lines)

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