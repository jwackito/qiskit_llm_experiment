import os
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
    return f'''
        Obten una respuesta con formato tabular que incluya las siguientes 8 dimensiones (columnas de la tabla) relacionados con los escenarios de migración y refactoring en Qiskit:

        Columna 1: Categoría: Tipo de cambio (Ej: Cambio de afectación estructural, lenguaje, implica librería externa, inserción / modificación / deprecación / remoción, afectación de módulo, función, clase, método, grado de relación con ing. de software clásica (SE) o ing. de software cuántica (QSE), etc).
        Columna 2: Flujo de cambio, indicando las versiones involucradas de origen y destino, no es necesario indicar versiones bug-fixes sino solo "x" para ese último dígito (Formato: d.d.x → d.d.x).
        Columna 3: Resumen del escenario, con una descripción breve y concisa resumiendo los principales artefactos que sufrieron cambios (1 línea).
        Columna 4: Ejemplo de código en versión de origen, fragmento Python previo al cambio.
        Columna 5: Ejemplo de código en versión de destino, fragmento Python posterior al cambio.
        Columna 6: Grado de dificultad asociada al nivel de esfuerzo requerido de migración (Nula/Baja/Moderada/Alta).
        Columna 7: Grado de afectación SE/QSE, en relación con Ingeniería de Software Clásica (SE) o Cuántica (QSE), entre paréntesis indicar una muy breve descripción justificando esa clasificación.
        Columna 8: Referencia, enlace a una fuente autoritativa de documentación, aclarando a continuación del enlace, si la fuente de referencia es "principal" o "secundaria" según las restricciones indicadas en las restricciones; por ej: "<link_fuente> (principal)" o bien "<link_fuente> (secundaria)".

        Requisitos adicionales para la generación de la tabla:
            1. Analiza exhaustivamente cambios en todos estos componentes de Qiskit y obtenerlos todos: 
            QuantumCircuit, Transpiler, Primitives, Providers (IBMQ/Aer), Qiskit Terra/Aer/Ignis/Experiments, Operadores, PassManagers, Visualización.

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

            3. Para cada versión objetivo indicada, en este caso: {version_objetivo}, examina todas las transiciones relevantes desde:
                - 0.05.x → 0.06.x → ... → {version_objetivo}
                - Entre versiones con cambios de API documentados

            4. Prioriza la creación de filas distintas para:
                - Cambios en diferentes sub-módulos (ej: qiskit.circuit vs qiskit.transpiler)
                - Tipos de operación distintos (inserción vs actualización vs deprecación vs remoción vs reubicación)
                - Niveles de abstracción diferentes (clases base vs implementaciones específicas)
                - Componentes afectados (librerias externas, involucra pip, backend, breaking-changes)
                - Incluye casos paradigmáticos como: migraciones de transpilador, cambios de parámetros, reestructuracion de módulos, etc.
            
        Restricciones:
            - Respuesta en formato tabular expresada con el lenguaje de marcado "Markdown" con formato Markdown. Evita saltos de línea innecesarios en una misma fila de tabla.
            - Evitar texto externo a la tabla mísma, explicaciones extras o aclaraciones, sólo limítate a entregar una tabla resultante.
            - Los códigos python de ejemplos deben ser correctos, extraídos de fuentes especificadas, en caso de no encontrar, no indicar ninguno.
            - Usar como referencias, hipervínculos validados y oficiales.
            - No consolidar escenarios y cambios, priorizar la abarcabildiad y extensión de escenarios.
            - Verificar la visualización correcta en formato Markdown.
            - Si para alguna celda opcional, no se dispone de información supervisada, indicarla como vacía, es decir, con valor: "".
            - Evitar escenarios hipotéticos o no documentados, pero se exhaustivo enunciando los documentados.
            - Utiliza exclusivamente la siguiente lista de fuentes (principales y secundarias), sigue este ordenamiento para su revisión exhaustiva:
                - Qiskit SDK realce notes (Enlace: {url_objetivo}) (principal)
                - Qiskit Changelog (Enlace: "https://github.com/qiskit/qiskit/releases") (principal)
                - Qiskit Leatest updates (Enlace: "https://docs.quantum.ibm.com/guides/latest-updates") (secundaria)
                - Qiskit Migration guides (Enlace: "https://docs.quantum.ibm.com/migration-guides") (secundaria)
    '''

def obtener_user_prompt(usar_qiskit_release_notes, version_objetivo, file_content):
    return f'''
        Describe exhaustivamente los escenarios de migración/refactoring en Qiskit {version_objetivo} considerando:

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
            - Deprecaciones con removal en {version_objetivo}
            - Cambios de API en métodos fundamentales
            - Reestructuraciones de módulos (qiskit.providers.ibmq → qiskit_ibm_provider)
            - Modificaciones en parámetros obligatorios/opcionales
            - Cambios en valores por defecto
            - Alteraciones en formatos de retorno (dict → clase específica)
            - Migración de funcionalidades a paquetes externos (qiskit-*)

        3. Directivas de análisis:
            - Examinar minuciosamente las release notes adjuntas
            - Cruzar información con changelogs oficiales
            - Priorizar cambios que afecten >2 componentes
            - Generar filas independientes por tipo de cambio aunque afecten mismo módulo
            - Incluir casos aunque no existan ejemplos de código disponibles
            - Considerar cambios en dependencias (numpy >= 1.2x, etc)

        {"4. Contenido de referencia para análisis específico de versión {version_objetivo}: {file_content}" if usar_qiskit_release_notes else ""} 
    '''

def invoke_openai(version_objetivo, url_objetivo, url_openai_server_endpoint, openai_api_key, usar_qiskit_release_notes, model_answers_path, model, temperature):

    print(f"\n\nInvocación de OpenAI utilizando el contenido de la versión {version_objetivo} --> url: {url_objetivo} ...")

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
        "temperature": temperature
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
        
        print(completion.choices[0].message.content)

        # Crear la carpeta "llm_answers" si no existe
        llm_answers_dir = os.path.normpath(os.path.join(os.getcwd(), model_answers_path))
        if not os.path.exists(llm_answers_dir):
            os.makedirs(llm_answers_dir, exist_ok=True)
        
        # Guardar el contenido en un archivo dentro de la carpeta configurada (default = "/llm_answers")
        fecha_hora = datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
        file_name = f"{payload['model'].split("/")[1]}_v{version_objetivo.replace('.', '_')}-{fecha_hora}.md"

        file_answer_path = os.path.join(llm_answers_dir, file_name)
        path_acortado = obtener_ultimas_dos_secciones(file_answer_path)

        with open(file_answer_path, 'w', encoding='utf-8') as f:
            # Asumiendo que 'completion' es un objeto de OpenAI u similar
            contenido = completion.choices[0].message.content
            if contenido:
                f.write(contenido)
                print(f"Archivo creado exitosamente en: {path_acortado}")
            else:
                print("Error: El contenido está vacío o no existe")

        if completion.choices[0].message.content:            
            print(f"\nRespuesta desde OpenAI obtenida. Almacenada en: {path_acortado}")
        else:
            print("\nNo se pudo obtener una respuesta del modelo de OpenAI.")

    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nPosibles soluciones:")
        print("1. Verifica que el servidor está corriendo y accesible")
        print("2. Confirma que la URL incluye el puerto y ruta correctos")
        print("3. Asegúrate que el modelo está cargado en el servidor remoto")
        print("4. Comprueba que la API key es correcta")