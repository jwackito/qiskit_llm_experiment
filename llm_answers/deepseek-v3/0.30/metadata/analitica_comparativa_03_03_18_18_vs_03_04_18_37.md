comparativa entre tabla v030 Deepseek v3, solicitudes "eco" (sin cambiar nada):
tabla 18:16 y tabla 18:37 del 03/04/2025

Tabla 1 --> 12 filas
	4 deprecaciones, 3 actualizaciones, 2 remociones y 3 nuevas características

Tabla 2 --> 13 filas
	5 deprecaciones, 6 actualizaciones y 2 remociones (no tiene nuevas características categorizadas)
	
ambas con problema de homogeneidad en flujo y referencias


coincidencias:
- qobj en run()
- snapshots en favor de save()
- errores no locales en NoiseModel
- método GPU
* parameter_binds en run() -> catalogado diferente dificultad
* PulseSimulator acepta circuito de entrada
* puertas basicas de NoiseModel (descripto diferente, para tabla 2 es una deprecación de u3)
- backend_options
- system_model en PulseSimulator
+ executors ejecucion paralela  (nueva caracteristica para t1 y actualizacion para t2)
+ soporte para PauliGates de n-qubits (t1 lo plantea como nueva caracteristica mientras que t2 como actualizacion)
+ mps_log_data (+ para t1 y * para t2)

diferencias:
	* añadido de SXdgGate y CUGate como compuertas base