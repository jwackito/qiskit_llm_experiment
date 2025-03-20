# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="localhost:puerto/v1", api_key="lm-studio")

completion = client.chat.completions.create(
  model="lmstudio-community/gemma-3-27b-it-GGUF",
  messages=[
    {"role": "system", "content": 
'''Genera una respuesta en forma de tabla con formato Markdown que incluya las siguientes 8 columnas y criterios para escenarios de migración en IBM-Qiskit:

Columna 1: Categoría: Tipo de cambio (Ej: Estructura, Lenguaje, Implicancia, Módulo implicado, Tipo de cambio, relación con QSE).

Columna 2: Flujo de origen y destino de versión indicando las versiones involucradas (Formato: X.X.X → Y.Y.Y).

Columna 3: Resumen del escenario, con una descripción concisa (1 línea).

Columna 4: Ejemplo de código en versión de origen, fragmento Python previo al cambio.

Columna 5: Ejemplo de código en versión de destino, fragmento Python posterior al cambio.

Columna 6: Grado de dificultad asociada al nivel de esfuerzo requerido de migración (Nula/Baja/Moderada/Alta).

Columna 7: Grado de afectación SE/QSE, en relación con Ingeniería de Software Clásica (SE) o Cuántica (QSE).

Columna 8: Referencia: Enlace oficial o hiperlink a una fuente autoritativa de documentación.'''
     },
    {"role": "user", "content": 
'''
Documentación de qiskit
'''
     }
  ],
  temperature=0.7,
)

print(completion.choices[0].message.content)
