import os
from openai import OpenAI
from datetime import datetime

def invoke_openai(version_objetivo, url_objetivo, url_openai_server_endpoint, openai_api_key, usar_qiskit_release_notes, model_answers_path):

    print(f"Invocación de OpenAI con el contenido de la versión {version_objetivo} --> url: {url_objetivo} ...")

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer lm-studio"
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

    system_content = f'''
    Obten una respuesta con formato tabular que incluya las siguientes 8 dimensiones (columnas de la tabla) relacionados con los escenarios de migración y refactoring en Qiskit:

    Columna 1: Categoría: Tipo de cambio (Ej: Cambio de afectación estructural, lenguaje, implica librería externa, inserción / modificación / deprecación / remoción, afectación de módulo, función, clase, método, grado de relación con ing. de software clásica (SE) o ing. de software cuántica (QSE), etc). Dato obligatorio.
    Columna 2: Flujo de cambio, indicando las versiones involucradas de origen y destino, no es necesario indicar versiones bug-fixes sino solo "x" para ese último dígito (Formato: X.X.x → Y.Y.x). Dato obligatorio.
    Columna 3: Resumen del escenario, con una descripción breve y concisa resumiendo los principales artefactos que sufrieron cambios (1 línea).  Dato obligatorio.
    Columna 4: Ejemplo de código en versión de origen, fragmento Python previo al cambio. Dato opcional.
    Columna 5: Ejemplo de código en versión de destino, fragmento Python posterior al cambio.  Dato opcional.
    Columna 6: Grado de dificultad asociada al nivel de esfuerzo requerido de migración (Nula/Baja/Moderada/Alta).  Dato obligatorio.
    Columna 7: Grado de afectación SE/QSE, en relación con Ingeniería de Software Clásica (SE) o Cuántica (QSE), entre paréntesis indicar una muy breve descripción justificando esa clasificación.  Dato obligatorio.
    Columna 8: Referencia: Enlace oficial o hiperlink a una fuente autoritativa de documentación, aclarando  a continuación del enlace, si la fuente de referencia es "principal" o "secundaria" según las restricciones indicadas debajo; por ej: "<link_fuente> (fuente principal)" o bien ""<link_fuente> (fuente secundaria)"". Dato opcional.

    Restricciones:
    Respuesta en formato tabular expresada con el lenguaje de marcado "Markdown" con formato Markdown. Evita saltos de línea innecesarios en una misma fila de tabla.
    Evitar texto externo a la tabla mísma, explicaciones extras o aclaraciones, sólo limítate a entregar una tabla resultante.
    Los códigos python de ejemplos deben ser correctos, extraídos de fuentes especificadas, en caso de no encontrar, no indicar ninguno.
    Usar como referencias, hipervínculos validados y oficiales.
    No consolidar escenarios y cambios, priorizar la abarcabildiad y extensión de escenarios.
    Verificar la visualización correcta en formato Markdown.
    Si para alguna celda opcional, no se dispone de información supervisada, indicarla como vacía, es decir, con valor: "".
    Evitar escenarios hipotéticos o no documentados, pero se exhaustivo enunciando los documentados.
    Utiliza exclusivamente la siguiente lista de fuentes (principales y secundarias) de Qiskit, sigue este ordenamiento para su revisión exhaustiva:
    Fuentes principales:
    Qiskit SDK realce notes (Enlace: {url_objetivo})
    Qiskit Changelog (Enlace: https://github.com/qiskit/qiskit/releases)
    Fuentes secundarias:
    Qiskit Leatest updates (Enlace: https://docs.quantum.ibm.com/guides/latest-updates)
    Qiskit Migration guides (Enlace: https://docs.quantum.ibm.com/migration-guides)
    Para la detección, examina en orden el listado de fuentes indicado previamente (4 fuentes bibliográficas) generando una nueva fila de la tabla.
    '''

    user_content = f'''
    Describe con el mayor grado de detalle posible, cada uno de los escenarios de migración y refactoring en Qiskit, exclusivamente para la versión: {version_objetivo}. 
    Indaga la mayor cantidad de información disponible para que la tabla sea lo más completa posible.
    {"A continuación, se proporciona el contenido de las notas de la versión {version_objetivo}: {file_content}" if usar_qiskit_release_notes else ""}
    '''

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

    payload = {
        "model": "lmstudio-community/gemma-3-27b-it-GGUF",
        "messages": messages,
        "temperature": 1
    }

    try:
        client = OpenAI(
            base_url=url_openai_server_endpoint, 
            api_key=openai_api_key
        )
        completion = client.chat.completions.create(
            model=payload['model'], 
            messages=payload['messages'], 
            temperature=payload['temperature']
        )
        
        # Crear la carpeta "llm_answers" si no existe
        llm_answers_dir = os.path.join(os.getcwd(), model_answers_path)
        if not os.path.exists(llm_answers_dir):
            os.makedirs(llm_answers_dir)
        
        # Guardar el contenido en un archivo dentro de la carpeta "llm_answers"
        fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_answer_path = os.path.join(llm_answers_dir, f"respuesta_{payload['model'].split("/")[1]}_v{version_objetivo}_{fecha_hora}.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(completion.choices[0].message.content)
        
        print(f"El contenido de respuesta del modelo se ha guardado en: {file_answer_path}")

    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nPosibles soluciones:")
        print("1. Verifica que el servidor está corriendo y accesible")
        print("2. Confirma que la URL incluye el puerto y ruta correctos")
        print("3. Asegúrate que el modelo está cargado en el servidor remoto")
        print("4. Comprueba que la API key es correcta")