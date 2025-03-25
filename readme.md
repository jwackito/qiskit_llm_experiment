Ejemplo de ejecución del comando:

```python
python ./scrap.py --version "0.46" --invoke_openai true --url_openai_server_endpoint "http://dominio.com:puerto/subdominio" --openai_api_key "modelo" --verificacion true
```

| Version  |  Tamaño  | Cant. líneas | Cant. líneas no vacías | Cant. lineas dif. | Cant. caracteres (k) |Cant. diferencias | estabilidad de datos | # tokens |
| -------: | :------: | -----------: | ---------------------: | ----------------: | -------------------: | ---------------: | :------------------: | -------: |
| 0.05.x | pequeño | 100 | 65 | 64 | 5.8 | 0 | alta |  |
| 0.06.x | pequeño | 114 | 79 | 25 | 6 | 0 | alta |  |
| 0.07.x | moderado | 183 | 127 | 103 | 15.4 | 0 | alta |  |
| 0.08.x | pequeño | 12 | 9 | 3 | .2 | 0 | alta |  |
| 0.09.x | moderado | 156 | 141 | 54 | 13.7 | 0 | alta |  |
| 0.10.x | pequeño | 22 | 17 | 1 | .5 | 0 | alta |  |
| 0.20.x | grande | 766 | 537 | 385 | 62 |  7 | alta |  |
| 0.30.x | pequeño | 122 | 94 | 88 | 9.8 | 0 | alta |  |
| 0.40.x | grande | 993 | 720 | 387 | 65.5 | 13 | moderada |  |
| 0.46.x | moderado | 468 | 341 | 299 | 30.5 | 1 | alta |
| 1.0.x | grande | 1020 | 735 | 663 | 67.5 | 1 | alta |  |
| 1.1.x | moderado | 797 | 565 | 470 | 57.5 | 8 | alta |  |
| 1.2.x | moderado | 513 | 361 | 297 | 39.3 | 9 | alta |  |
| 1.3.x | grande | 1019 | 760 | 968 | 62.7 | 24 | moderada |  |
| 1.4.x | pequeño | 141 | 104 | 27 | 13.6 | 0 | alta |  |


![Líneas de documentación en notas de liberación](/imagenes/grafico_version_cant_lineas.png)