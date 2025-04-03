import os
from openai import OpenAI
from datetime import datetime
from utils import *
from dotenv import load_dotenv

def invoke_openai(
    version_objetivo, url_objetivo, url_openai_server_endpoint, openai_api_key, usar_qiskit_release_notes, model_answers_path, project_id, idioma):

    print(f'''\n[INFO] Invocación al modelo {os.getenv("MODEL")} ...{f"\nFlag 'usar_qiskit_release_notes' ON --> inyectando info de Qiskit release notes ({obtener_ultimas_dos_secciones(url_objetivo)}) en el prompt de usuario" if usar_qiskit_release_notes else "[INFO] Flag 'usar_qiskit_release_notes' OFF --> utilizando sólo urls en prompts"}''')

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
        "OpenAI-Project": project_id
    }

    # Ruta al archivo generado por el script previo
    downloads_dir = os.path.join(os.getcwd(), "scraped_content")
    file_path = os.path.join(downloads_dir, f"qiskit_release_notes_{version_objetivo}_{idioma}.md")

    # Verificar si el archivo existe
    if not os.path.exists(file_path):
        print(f"Error: El archivo {file_path} no existe. Ejecuta primero el script de scraping para generar el archivo.")
        exit(1)

    # Leer el contenido del archivo
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": obtener_system_prompt(version_objetivo, idioma)
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": obtener_user_prompt(usar_qiskit_release_notes, version_objetivo, file_content, idioma)
                }
            ]
        }
    ]

    try:
        
        client = OpenAI(
            base_url=url_openai_server_endpoint, 
            api_key=openai_api_key
        )

        extra_params = obtener_parametrizacion()

        completion = client.chat.completions.create(
            model=extra_params['model'], 
            messages=messages, 
            temperature=extra_params['temperature'],
            #top_p=extra_params['top_p'],
            max_tokens=extra_params['max_tokens'],
            #frequency_penalty=extra_params['frequency_penalty'],
            #presence_penalty=extra_params['presence_penalty'],            
            #response_format=extra_params['response_format'],
            #system_prompt_ratio=extra_params['system_prompt_ratio'],
            #stop=extra_params['stop'],
            #n=extra_params['n'],
            stream=extra_params['stream'],
            seed=extra_params['seed'],
            #reasoning_effort=extra_params['reasoning_effort'],
        )
        
        #print(completion.choices[0].message.content)

        # Crear la carpeta "llm_answers" si no existe
        llm_answers_dir = os.path.normpath(os.path.join(os.getcwd(), model_answers_path + f"/{version_objetivo}"))
        if not os.path.exists(llm_answers_dir):
            os.makedirs(llm_answers_dir, exist_ok=True)

        # Armado del nombre de archivo de respuesta
        fecha_hora = datetime.now().strftime("%d_%m_%Y-%H_%M")
        modelo_base = (
            extra_params['model'].split('/', 1)[1] if '/' in extra_params['model'] else extra_params['model']
        )
        file_name = f"{modelo_base}_v{version_objetivo.replace('.', '_')}_{fecha_hora}"

        guardar_metadata_completion(completion, llm_answers_dir, file_name, params=extra_params)

        path = guardar_respuesta(completion, llm_answers_dir, file_name)

        if completion.choices[0].message.content:            
            print(f"\n[OK] Respuesta desde OpenAI obtenida. Almacenada en: {path}\n")
        else:
            print("\n[ERROR] No se pudo obtener una respuesta del modelo de OpenAI.\n")

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        print("\nPosibles soluciones:")
        print("1. Verifica que el servidor está corriendo y accesible")
        print("2. Confirma que la URL incluye el puerto y ruta correctos")
        print("3. Asegúrate que el modelo está cargado en el servidor remoto")
        print("4. Comprueba que la API key es correcta")