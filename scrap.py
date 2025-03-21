import os, argparse, requests
from bs4 import BeautifulSoup

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
    parser.add_argument("version", help="Versión de Qiskit para la cual extraer las notas de la versión (por ejemplo, '0.46')")
    
    # Parsear los argumentos
    args = parser.parse_args()
    
    # Construir la URL usando la versión proporcionada
    url_qiskit_release_notes = f"https://docs.quantum.ibm.com/api/qiskit/release-notes/{args.version}"
    
    content = extract_main_content(url_qiskit_release_notes)
    
    if content:
        # print(content)

        # Crear la carpeta "descargas" si no existe
        downloads_dir = os.path.join(os.getcwd(), "scraped_content")
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
        
        # Guardar el contenido en un archivo dentro de la carpeta "descargas"
        file_path = os.path.join(downloads_dir, f"qiskit_release_notes_{args.version}.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"El contenido se ha guardado en: {file_path}")