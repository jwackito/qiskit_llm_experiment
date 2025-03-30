import os, json
from openai import OpenAI
from datetime import datetime

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

def obtener_system_prompt(url_objetivo, version_objetivo):
    version = version_objetivo + ".0"
    return f'''
        Obten una respuesta con formato tabular que incluya las siguientes 8 dimensiones (columnas de la tabla) relacionados con los escenarios de migración y refactoring en Qiskit:
        Columna 1: Categoría: Tipo de cambio (Ej: cambio estructural, lenguaje, implica librería externa, inserción / modificación / deprecación / remoción, breve descripción de módulo, función, clase, método, o artefacto implicado. Omite Bug Fixes.
        Columna 2: Flujo de cambio, indicando las versiones involucradas de origen y destino, no es necesario indicar versiones bug-fixes sino solo "x" para ese último dígito (Formato: o.o.x → d.d.x).
        Columna 3: Resumen del escenario, con una descripción breve y concisa resumiendo los principales artefactos que sufrieron cambios (1 línea).
        Columna 4: Ejemplo de código en versión de origen, fragmento Python previo al cambio.
        Columna 5: Ejemplo de código en versión de destino, fragmento Python posterior al cambio.
        Columna 6: Grado de dificultad asociada al nivel de esfuerzo requerido de migración ("Nula" si no afecta al código vs "Baja" si reviste poca dificultad de migración vs "Moderada" si requiere múltiples cambios de adaptación vs "Alta" si es un cambio disruptivo y afecta la API), entre paréntesis indicar una muy breve descripción justificando esa clasificación.
        Columna 7: Grado de afectación sobre "ing. de software clásica" (SE) vs "ing. de software cuántica" (QSE), entre paréntesis indicar una muy breve descripción justificando esa clasificación.
        Columna 8: Referencia, enlaces a una o más fuentes autoritativas de origen de la información, celda requerida.

        Requisitos adicionales para la generación de la tabla:
            1. Revisa exhaustivamente cambios en todos estos componentes Qiskit y recopilalos todos: QuantumCircuit, Transpiler, Primitives, Providers (IBMQ/Aer), Qiskit Terra/Aer/Ignis/Experiments, Operadores, PassManagers, Visualización.                

            2. Considera específicamente estos tipos de cambios:
                - Deprecaciones de clases/métodos entre versiones 
                - Cambios de jerarquía de clases (herencia)
                - Migración de funciones entre módulos
                - Modificaciones en firmas de métodos (args/kwargs)
                - Reestructuraciones de paquetes (qiskit.* → qiskit_*)
                - Cambios en mecanismos de configuración
                - Actualizaciones de dependencias externas (numpy, scipy, etc)
                - Modificaciones en sistemas de serialización
                - Cambios en modelos de datos (QuantumCircuit.data)
                - Transiciones de APIs síncronas a asíncronas

            3. Para cada versión objetivo indicada: {version}, debes enunciar todas las transiciones relevantes:
                - desde la versión base 0.05.0 y superiores, pudiendo incluir cambios como: 0.05.x → {version}, 0.06.x → {version}, etc.
                - Siempre la versión de destino del cambio debe ser mayor o igual que la de origen.

            4. Prioriza la creación de filas distintas para:
                - Cambios en diferentes sub-módulos (ej: qiskit.circuit vs qiskit.transpiler)
                - Tipos de operación distintos (inserción vs actualización vs deprecación vs remoción vs reubicación)
                - Considera la estructura de cambios que utiliza v{url_objetivo}
                - Niveles de abstracción diferentes (clases base vs implementaciones específicas)
                - Componentes afectados (librerias externas, involucra pip, backend, breaking-changes)
                - Incluye casos paradigmáticos como: migraciones de transpilador, cambios de parámetros, reestructuracion de módulos, etc.
            
        Restricciones:
            - Respuesta en formato tabular expresada con el lenguaje de marcado "Markdown" con formato Markdown. Evita saltos de línea innecesarios en una misma fila de tabla.
            - Evitar texto externo a la tabla mísma, explicaciones extras o aclaraciones, sólo limítate a entregar una tabla resultante.
            - Los códigos python de ejemplos deben ser correctos, extraídos de fuentes especificadas, en caso de no encontrar, no indicar ninguno.
            - Usar como referencias, sólo hipervínculos validados y oficiales.
            - En el flujo de cambios (segunda columna) nunca la versión superior debe ser mayor que v{version}, pudiendo admitirse cualquiera en la versión de origen.
            - No consolidar escenarios y cambios, priorizar la abarcabildiad y extensión de escenarios.
            - Verificar la visualización correcta en formato Markdown.
            - Si para alguna celda opcional, no se dispone de información supervisada, indicarla como vacía, es decir, con valor: "".
            - Solo se admiten celdas vacías para los ejemplos de código (4° y 5° columna).
            - Evitar escenarios hipotéticos o no documentados, pero se exhaustivo enunciando los documentados.
            - Utiliza la siguiente lista de fuentes en este ordenamiento para su revisión exhaustiva:
                - Qiskit SDK realce notes ({url_objetivo}) (principal)
                - Qiskit Changelog (https://github.com/qiskit/qiskit/releases/tag/{version}) (principal)
                - Qiskit Documentation tree (https://github.com/Qiskit/documentation/tree/main/docs/api/qiskit/{version_objetivo}) (secundaria)
                - Qiskit Leatest updates (https://docs.quantum.ibm.com/guides/latest-updates) (secundaria)
                - Qiskit Migration guides (https://docs.quantum.ibm.com/migration-guides) (secundaria)
                - Si el cambio tiene un enlace interno, indícalo también como una nueva línea en la columna de referencias, entre paréntesis indicar el tipo de fuente ("principal" vs "secundaria").
            - No generes filas a partir de ninguna migración de corrección de código del tipo: Bug Fixes.
    '''

def obtener_user_prompt(inyectar_qiskit_release_notes, version_objetivo, file_content):
    version = version_objetivo + ".0"
    return f'''
        Describe exhaustivamente todos los escenarios de migración Qiskit en la versión objetivo {version} considerando:

        1. Componentes críticos a inspeccionar:
            - QuantumCircuit y sus métodos (compose, combine, etc)
            - Transpiler (passes, niveles de optimización)
            - Primitivas (Sampler, Estimator)
            - Módulos de proveedores (IBMProvider, Backends)
            - Operadores (Pauli, SparsePauliOp)
            - Sistemas de visualización (circuit_drawer, plot_histogram)
            - Mecanismos de ejecución (Aer simulators, BasicAer)
            - Qiskit-Terra vs Aer vs Experiments

        2. Tipos de cambios a priorizar:
            - Deprecaciones con removal en {version}
            - Cambios de API en métodos fundamentales
            - Reestructuraciones de módulos (qiskit.providers.ibmq → qiskit_ibm_provider)
            - Modificaciones en parámetros obligatorios/opcionales
            - Cambios en valores por defecto
            - Alteraciones en formatos de retorno (dict → clase específica)
            - Migración de funcionalidades a paquetes externos (qiskit-*)
            - Instalaciones o ejecución de pip

        3. Directivas de análisis:
            - Examinar minuciosamente las release notes adjuntas
            - Cruzar información con changelogs oficiales
            - Priorizar cambios que afecten >2 componentes
            - Generar filas independientes por tipo de cambio aunque afecten mismo módulo
            - Incluir casos aunque no existan ejemplos de código disponibles
            - Considerar cambios en dependencias (numpy >= 1.2x, etc)
            {f"- Considera de suma relevancia la siguiente información de versión {version} para analizarla detalladamente: {file_content}" if inyectar_qiskit_release_notes else ""} 
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

def invoke_openai(version_objetivo, url_objetivo, url_openai_server_endpoint, openai_api_key, usar_qiskit_release_notes, model_answers_path, model, temperature):

    print(f'''\n[INFO] Invocación al modelo {model} ...{f"\nFlag 'usar_qiskit_release_notes' ON --> inyectando info de Qiskit rrnn ({url_objetivo})" if usar_qiskit_release_notes else "[INFO] Flag 'usar_qiskit_release_notes' OFF --> utilizando sólo urls en prompts"}''')

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
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
    user_content = obtener_user_prompt(usar_qiskit_release_notes, version_objetivo, file_content)

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
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 2048,
        "stream": False
    }

    try:
        
        client = OpenAI(
            base_url=url_openai_server_endpoint, 
            api_key=openai_api_key
        )

        completion = client.chat.completions.create(
            model=payload['model'], 
            messages=payload['messages'], 
            temperature=payload['temperature'],
            max_tokens=payload['max_tokens'],
            stream=payload['stream']
        )
        
        print(completion.choices[0].message.content)

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