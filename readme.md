## Información de ejecución del proyecto

Ejemplo de ejecución del comando:

```python
python ./scrap.py --version "0.46" --invoke_openai true --url_openai_server_endpoint "http://dominio.com:puerto/subdominio" --openai_api_key "modelo" --verificacion true
```

## Configuración de variables de entorno

Configurando el archivo de variables de entorno del proyecto (.env), no es necesario enviar ningún parámetro.
Ejemplo de configuración (archivo .env):

```python
	# Indica el endpoint de conexión remota
	URL_OPENAI_SERVER_ENDPOINT="http://prueba.com:80/subdominio"

	# Indica la key de conexión a la api
	OPENAI_API_KEY="api-key"

	# Indica el nombre de modelo LLM a utilizar
	MODEL="LLM_model"

	# Indica el directorio donde se guardan las respuestas de invocaciones remotas
	MODEL_OUTPUT_DIRECTORY="llm_answers"

	# Indica el directorio donde se guardan las recopilaciones de info de qiskit release notes
	SCRAP_DIRECTORY="scraped_content"

	# Indica si al prompt enviado al modelo se le inyecta información recopilada desde Qiskit release notes
	INYECTA_INFO_QRN=True
	
	# Indica si se realizará la invocación remota
	REMOTE_INVOKE=True

	# Indica la versión de qiskit para la generación de la tabla
	DEFAULT_VERSION="0.25"

	# Indica la temperatura del modelo (0 menos grados de libertad)
	TEMPERATURE=0

	# Indica si ejecutar o no una etapa de verificación de la info del release note, con la copiada desde esa url
	EJECUTAR_ETAPA_VERIFICACION=False
```

## Información de tokens y caracteres de las notas de liberación

	- prompt de sistema:
    	- 5650 caracteres aprox.
    	- 1300 tokens aprox.
  
	- prompt de usuario:
    	- 1760 caracteres aprox.
    	- 384 tokens aprox.

  	- A priori, los prompts sin información añadida rondan:
    	- 7410 caracteres aprox.
    	- 1684 tokens aprox.


| Version  |  Tamaño  | Cant. líneas | Cant. líneas no vacías | Cant. lineas dif. | Cant. caracteres (k) |Cant. diferencias | estabilidad de datos | # tokens Gemma | # tokens Qween |
| -------: | :------: | -----------: | ---------------------: | ----------------: | -------------------: | ---------------: | :------------------: | -------------: | -------------: |
| 0.05.x | pequeño | 100 | 65 | 64 | 5.8 | 0 | alta | 1459 | 1349 |
| 0.06.x | pequeño | 114 | 79 | 25 | 6.1 | 0 | alta | 1667 | 1495 |
| 0.07.x | moderado | 183 | 127 | 103 | 15.5 | 0 | alta | 3857 | 3572 |
| 0.08.x | pequeño | 12 | 9 | 3 | .28 | 0 | alta | 99 | 100 |
| 0.09.x | moderado | 156 | 141 | 54 | 13.6 | 0 | alta | 3512 | 3381 |
| 0.10.x | pequeño | 22 | 17 | 1 | .53 | 0 | alta | 177 | 174 |
| 0.20.x | grande | 766 | 537 | 385 | 62.9 |  7 | alta | 17274 | 16145 |
| 0.30.x | pequeño | 122 | 94 | 88 | 9.8 | 0 | alta | 2589 | 2480 |
| 0.40.x | grande | 993 | 720 | 387 | 65.9 | 13 | moderada | 19544 | 18148 |
| 0.46.x | moderado | 468 | 341 | 299 | 31.4 | 1 | alta | 9066 | 8305 |
| 1.0.x | grande | 1020 | 735 | 663 | 67.6 | 1 | alta | 19010 | 17432 |
| 1.1.x | moderado | 797 | 565 | 470 | 58.6 | 8 | alta | 16220 | 14939 |
| 1.2.x | moderado | 513 | 361 | 297 | 39.3 | 9 | alta | 10520 | 9926 |
| 1.3.x | grande | 1019 | 760 | 968 | 63.3 | 24 | moderada | 18032 | 16814 |
| 1.4.x | pequeño | 141 | 104 | 27 | 13.6 | 0 | alta | 3758 | 3544 |

<br><br>
<img 
	src="./imagenes/grafico.png" width="90%"
	alt="Líneas de documentación en notas de liberación según versión Qiskit">


Generación del diagrama: 
```python 
python utils.py diagrama
```

Prueba de tokenizer:
```python 
python utils.py tokenizer
```

## Diagrama de flujo de procesamiento actual
<br>
<img 
	src="./imagenes/diagrama_procesamiento.png" width="70%"
	alt="Líneas de documentación en notas de liberación según versión Qiskit">