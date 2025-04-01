import os
from openai import OpenAI
from datetime import datetime
from utils import *

def invoke_openai(version_objetivo, url_objetivo, url_openai_server_endpoint, openai_api_key, 
                  usar_qiskit_release_notes, model_answers_path, model, temperature, project_id):

    print(f'''\n[INFO] Invocación al modelo {model} ...{f"\nFlag 'usar_qiskit_release_notes' ON --> inyectando info de Qiskit release notes ({obtener_ultimas_dos_secciones(url_objetivo)}) en el prompt de usuario" if usar_qiskit_release_notes else "[INFO] Flag 'usar_qiskit_release_notes' OFF --> utilizando sólo urls en prompts"}''')

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
        "OpenAI-Project": {project_id}
    }

    # Ruta al archivo generado por el script previo
    downloads_dir = os.path.join(os.getcwd(), "scraped_content")
    file_path = os.path.join(downloads_dir, f"qiskit_release_notes_{version_objetivo}.md")

    # Verificar si el archivo existe
    if not os.path.exists(file_path):
        print(f"Error: El archivo {file_path} no existe. Ejecuta primero el script de scraping para generar el archivo.")
        exit(1)

    # Leer el contenido del archivo
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    # Generación de prompts
    system_content = obtener_system_prompt(url_objetivo, version_objetivo)
    user_content = obtener_user_prompt(usar_qiskit_release_notes, version_objetivo, file_content, url_objetivo)

    messages = [
        {
            "role": "system",
            "content": system_content
        },
        {
            "role": "user",
            "content": user_content
        }
    ]

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
        "messages": messages,       # Prompts del sistema y del usuario
        "temperature": 0.0,         # Máxima fidelidad al formato
        "top_p": 0.05,              # Enfoque ultra-estricto en sintaxis MD
        "max_tokens": 3000,         # Capacidad para tablas complejas
        "frequency_penalty": 1.5,   # Eliminar repetición de headers
        "presence_penalty": 0.7,  
        "stop": ["\n\n", "##", "<!--", "<!--END-->", "## Notas", "**Nota**"],   # Prevenir markdown adicional
        "system_prompt_ratio": 0.75,  # Priorizar plantilla MD
        "format_constraints": {
            "markdown_table": {
            "columns": 8,
            "required_headers": ["Tipo de Cambio", "Flujo de Cambio", "Resumen", "Código Pre-Migración", "Código Post-Migración", "Dificultad", "Impacto SE/QSE", "Referencias"],
            "alignment": "left"
            }
        }
    }

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

    try:
        
        client = OpenAI(
            base_url=url_openai_server_endpoint, 
            api_key=openai_api_key
        )

        completion = client.chat.completions.create(
            model=payload['model'], 
            messages=payload['messages'], 
            temperature=payload['temperature'],
            #top_p=payload['top_p'],
            max_tokens=payload['max_tokens'],
            #presence_penalty=payload['presence_penalty'],
            #frequency_penalty=payload['frequency_penalty'],
            #n=payload['n'],
            stream=payload['stream'],
            #system_prompt_ratio=payload['system_prompt_ratio'],
            #stop=payload['stop']
        )
        
        #print(completion.choices[0].message.content)

        # Crear la carpeta "llm_answers" si no existe
        llm_answers_dir = os.path.normpath(os.path.join(os.getcwd(), model_answers_path + f"/{version_objetivo}"))
        if not os.path.exists(llm_answers_dir):
            os.makedirs(llm_answers_dir, exist_ok=True)

        # Guardar el contenido en un archivo dentro de la carpeta configurada (default = "/llm_answers")
        fecha_hora = datetime.now().strftime("%d_%m_%Y-%H_%M")
        modelo_base = (
            payload['model'].split('/', 1)[1] 
            if '/' in payload['model'] 
            else payload['model']
        )

        file_name = f"{modelo_base}_v{version_objetivo.replace('.', '_')}_{fecha_hora}"

        guardar_metadata_completion(completion, llm_answers_dir, file_name, payload)

        # Guarda el contenido de la respuesta
        file_answer_path = os.path.join(llm_answers_dir, file_name + ".md")
        path_acortado = obtener_ultimas_dos_secciones(file_answer_path)

        with open(file_answer_path, 'w', encoding='utf-8') as f:
            # Asumiendo que 'completion' es un objeto de OpenAI u similar
            contenido = completion.choices[0].message.content
            if contenido:
                f.write(apto_md(contenido))
                print(f"\n[OK] Archivo creado exitosamente en: {path_acortado}")
            else:
                print("\n[ERROR] El contenido está vacío o no existe")

        if completion.choices[0].message.content:            
            print(f"\n[OK] Respuesta desde OpenAI obtenida. Almacenada en: {path_acortado}\n")
        else:
            print("\n[ERROR] No se pudo obtener una respuesta del modelo de OpenAI.\n")

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        print("\nPosibles soluciones:")
        print("1. Verifica que el servidor está corriendo y accesible")
        print("2. Confirma que la URL incluye el puerto y ruta correctos")
        print("3. Asegúrate que el modelo está cargado en el servidor remoto")
        print("4. Comprueba que la API key es correcta")