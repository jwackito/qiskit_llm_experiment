import os, argparse, requests
from bs4 import BeautifulSoup
from peticion_openai import invoke_openai
from verificacion import verificar_documentacion

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
    
    # Extraer texto manteniendo saltos de línea básicos
    text = cleaned_soup.get_text(separator='\n', strip=True)
    
    # Eliminar líneas vacías múltiples y espacios excesivos
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned_text = '\n'.join(lines)
    
    # Eliminar saltos de línea innecesarios dentro de párrafos
    cleaned_text = ' '.join(cleaned_text.split())  # Elimina espacios múltiples
    cleaned_text = cleaned_text.replace(' .', '.')  # Corrige espacios antes de puntos
    cleaned_text = cleaned_text.replace(' ,', ',')  # Corrige espacios antes de comas
    
    return cleaned_text

if __name__ == "__main__":

    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description="Extracción de documentación oficial Qiskit")
    parser.add_argument("--version", type=str, help="Versión de Qiskit para la cual extraer las notas de la versión", default="1.0")
    parser.add_argument("--usa_qiskit_release_notes", type=bool, help="Flag que indica la utilización de Qiskit release notes como fuente de información", default=False)
    parser.add_argument("--scrapped_path", type=str, help="Directorio donde se almacenan las notas de la versión", default="scraped_content")
    parser.add_argument("--url_openai_server_endpoint", type=str, help="Directorio donde se almacenan las notas de la versión", default="http:prueba.com/openai")
    parser.add_argument("--openai_api_key", type=str, help="Directorio donde se almacenan las notas de la versión", default="1234567890")
    parser.add_argument("--model_answers_path", type=str, help="Directorio donde se almacenan las respuestas del modelo", default="llm_answers")
    parser.add_argument("--invoke_openai", type=bool, help="Flag que indica si invocar a la api de openai", default=False)
    parser.add_argument("--verificacion", type=bool, help="Flag que indica si ejecutar las verificaciones de contenidos obtenidos", default=False)
    # Parsear los argumentos
    args = parser.parse_args()
    
    # Construir la URL usando la versión proporcionada
    url_qiskit_release_notes = f"https://docs.quantum.ibm.com/api/qiskit/release-notes/{args.version}"
    parser.set_defaults(scraped_content_path="scraped_content")
    
    content = extract_main_content(url_qiskit_release_notes)
    
    if content:

        # Crear la carpeta "scrapped_content" si no existe
        downloads_dir = os.path.join(os.getcwd(), args.scrapped_path)
        if not os.path.exists(downloads_dir):
            print(f"Creando el directorio ... {downloads_dir}", "green")
            os.makedirs(downloads_dir)
        
        # Guardar el contenido en un archivo dentro de la carpeta "scrapped_content"
        file_path = os.path.join(downloads_dir, f"qiskit_release_notes_{args.version}.md")
        print(f"Sobreescribiendo el contenido de {file_path} ..." if os.path.exists(file_path) else f"Guardando el contenido en {file_path} ...")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Contenido obtenido desde {url_qiskit_release_notes} guardado en: {file_path}")

        if args.invoke_openai:
            openai_response = invoke_openai(
                args.version, 
                url_qiskit_release_notes, 
                args.url_openai_server_endpoint, 
                args.openai_api_key, 
                args.usa_qiskit_release_notes, 
                args.model_answers_path
            )

        if args.verificacion:           
            verificar_documentacion(content, args.version)