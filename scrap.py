import os, argparse, requests
from bs4 import BeautifulSoup
from peticion_openai import invoke_openai
from verificacion import verificar_documentacion
from dotenv import load_dotenv

def clean_content(soup):

    # Eliminar elementos con clases comunes de barras laterales/pies de página
    unwanted_classes = ['header', 'footer', 'sidebar', 'aside', 'nav', 'navbar', 'side-dock', 'announcement', 'script', 'style', 'svg']
    for element in soup.find_all(class_=unwanted_classes):
        element.decompose()    

        # Eliminar elementos con el atributo data-testid="page-toc"
    for element in soup.find_all(attrs={"data-testid": "page-feedback"}):
        element.decompose()  

    # Eliminar elementos vacíos
    for element in soup.find_all():
        if len(element.get_text(strip=True)) == 0:
            element.decompose()

    return soup

def extract_main_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la URL: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Intentar encontrar el contenido principal usando selectores comunes
    main_selectors = [
        'main',  # Elemento HTML5 main
        '.main-content',  # Clase común para contenido principal
        '.md-content',  # Usado en documentación MkDocs
        'article',  # Elemento HTML5 article
        '.content'  # Clase genérica para contenido
    ]
    
    main_content = None
    for selector in main_selectors:
        main_content = soup.select_one(selector)
        if main_content:
            break
            
    if not main_content:
        return "No se pudo encontrar el contenido principal en la página."

    # Limpiar el contenido
    cleaned_soup = clean_content(main_content)
    
    # Comento las líneas de limpieza para que no se modifique el código python

    # Extraer texto manteniendo saltos de línea básicos
    text = cleaned_soup.get_text(separator='\n', strip=True)
    
    # Eliminar líneas vacías múltiples y espacios excesivos
    #lines = [line.strip() for line in text.splitlines() if line.strip()]
    #cleaned_text = '\n'.join(lines)
    
    # Eliminar saltos de línea innecesarios dentro de párrafos
    #cleaned_text = ' '.join(cleaned_text.split())  # Elimina espacios múltiples
    #cleaned_text = cleaned_text.replace(' .', '.')  # Corrige espacios antes de puntos
    #cleaned_text = cleaned_text.replace(' ,', ',')  # Corrige espacios antes de comas
    
    return text

def bool_conv(valor):
    return valor.strip().lower() == "true"

if __name__ == "__main__":

    # Carga las variables del archivo .env
    load_dotenv()

    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description="Extracción de documentación oficial Qiskit")
    parser.add_argument("--version", type=str, help="Versión de Qiskit para la cual extraer las notas de la versión", default=os.getenv("DEFAULT_VERSION"))
    parser.add_argument("--inyecta_info_qrn", type=bool, help="Flag que indica la utilización de Qiskit release notes como fuente de información", default=bool_conv(os.getenv("INYECTA_INFO_QRN", False)))
    parser.add_argument("--scrapped_path", type=str, help="Directorio donde se almacenan las notas de la versión", default=os.getenv("SCRAP_DIRECTORY"))
    parser.add_argument("--url_openai_server_endpoint", type=str, help="Directorio donde se almacenan las notas de la versión", default=os.getenv("URL_OPENAI_SERVER_ENDPOINT"))
    parser.add_argument("--openai_api_key", type=str, help="Directorio donde se almacenan las notas de la versión", default=os.getenv("OPENAI_API_KEY"))
    parser.add_argument("--model_answers_path", type=str, help="Directorio donde se almacenan las respuestas del modelo", default="llm_answers")
    parser.add_argument("--invoke_openai", type=bool, help="Flag que indica si invocar a la api de openai", default=bool_conv(os.getenv("REMOTE_INVOKE", False)))
    parser.add_argument("--model", type=str, help="Modelo de OpenAI a ejecutar", default=os.getenv("MODEL"))
    parser.add_argument("--temperature", type=int, help="Temperatura del modelo", default=os.getenv("TEMPERATURE"))
    parser.add_argument("--verificacion", type=bool, help="Flag que indica si ejecutar las verificaciones de contenidos obtenidos", default=bool_conv(os.getenv("EJECUTAR_ETAPA_VERIFICACION", False)))

    args = parser.parse_args()

    # Construir la URL usando la versión proporcionada
    url_qiskit_release_notes = f"https://docs.quantum.ibm.com/api/qiskit/release-notes/{args.version}"
    
    content = extract_main_content(url_qiskit_release_notes)
    
    if content:

        # Crear la carpeta "scrapped_content" si no existe
        downloads_dir = os.path.join(os.getcwd(), args.scrapped_path)
        if not os.path.exists(downloads_dir):
            print(f"Creando el directorio ... {downloads_dir}")
            os.makedirs(downloads_dir)
        
        # Guardar el contenido en un archivo dentro de la carpeta "scrapped_content"
        file_path = os.path.join(downloads_dir, f"qiskit_release_notes_{args.version}.md")
        print(f"Sobreescribiendo el contenido de {file_path} ..." if os.path.exists(file_path) else f"Guardando el contenido en {file_path} ...")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Contenido obtenido desde {url_qiskit_release_notes} guardado en: {file_path}")

        if args.invoke_openai:
            openai_response = invoke_openai(
                version_objetivo = args.version, 
                url_objetivo = url_qiskit_release_notes, 
                url_openai_server_endpoint = args.url_openai_server_endpoint, 
                openai_api_key = args.openai_api_key, 
                usar_qiskit_release_notes = args.inyecta_info_qrn, 
                model_answers_path = args.model_answers_path, 
                model = args.model,
                temperature = args.temperature
            )

        if args.verificacion:           
            verificar_documentacion(content, args.version)