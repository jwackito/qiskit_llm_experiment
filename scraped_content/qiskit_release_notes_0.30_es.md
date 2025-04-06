Qiskit 0.30 notas de la versión

0.30.0
Terra 0.18.2
Sin cambios
Aer 0.9.0
Preludio
La versión 0.9 incluye nuevas opciones de backend para la exeucción paralela de un gran número de circuitos en un cluster HPC usando un Dask distribuido, junto con otras mejoras generales de rendimiento y corrección de errores.
Nuevas características
Añadido soporte para set_matrix_product_state.
Añadidas las librerías qiskit SXdgGate y CUGate a las puertas base soportadas para los backends del simulador Aer. Tenga en cuenta que la puerta CUGate sólo se admite de forma nativa para los métodos statevector y unitary. Para otros métodos de simulación se debe transpilar a las puertas de base soportadas para ese método.
Añade soporte para N-qubit puerta de Pauli ( qiskit.circuit.library.generalized_gates.PauliGate) a todos los métodos de simulación de la AerSimulator y QasmSimulator.
Añade la capacidad de establecer un ejecutor personalizado y configurar la división del trabajo para ejecutar múltiples circuitos en paralelo en un clustor HPC. Se puede establecer un ejecutor personalizado utilizando la opción executor, y la división de trabajos se configura utilizando la opción max_job_size.
Por ejemplo configurando un backend y ejecutando usando
```python
backend = AerSimulator(max_job_size=1, executor=custom_executor)
job = backend.run(circuits)
```
dividirá la sección en varios trabajos, cada uno de los cuales contendrá un único circuito. Si la división de trabajos está activada, el método run devolverá un objeto AerJobSet que contiene todas las clases AerJob individuales. Después de que todos los trabajos individuales terminan de ejecutarse, los resultados del trabajo se combinan automáticamente en un único objeto Result que es devuelto por job.result().
Entre los ejecutores compatibles se incluyen los del módulo concurrent.futures de Python (p. ej., ThreadPoolExecutor, ProcessPoolExecutor) y los ejecutores Dask distributed Client si está instalada la biblioteca dask opcional. El uso de un ejecutor Dask permite configurar la ejecución en paralelo de múltiples circuitos en clusters HPC.
Añade la capacidad de grabar datos de registro para el método de simulación matrix_product_state en los metadatos de resultados del experimento estableciendo la opción de backend mps_log_data=True. Los datos guardados incluyen las dimensiones de enlace y el valor descartado (la suma de los cuadrados de los coeficientes de Schmidt que se descartaron por aproximación) después de cada instrucción de circuito relevante.
```python
from qiskit.circuit import QuantumCircuit, Parameter
from qiskit.providers.aer import AerSimulator
shots = 1000
backend = AerSimulator()
circuit = QuantumCircuit(2)
theta = Parameter('theta')
circuit.rx(theta, 0)
circuit.cx(0, 1)
circuit.measure_all()
parameter_binds = [{theta: [0, 3.14, 6.28]}]
backend.run(circuit, shots=shots, parameter_binds=parameter_binds).result()
```
ejecutará el circuito de entrada 3 veces con los valores 0, 3,14 y 6,28 para theta. Cuando se ejecuta con múltiples parámetros, la longitud de las listas de valores debe ser la misma. Cuando se ejecuta con múltiples circuitos, la longitud de parameter_binds debe coincidir con el número de circuitos de entrada (puede utilizar un dict vacío, {}, si no hay binds para un circuito).
El PulseSimulator puede ahora aceptar objetos QuantumCircuit en la función run(). Anteriormente, sólo aceptaba objetos Schedule como entrada a run(). Cuando se pasa un circuito o una lista de circuitos al simulador, éste llamará a schedule() para convertir los circuitos en un programa antes de ejecutar el circuito. Por ejemplo
```python
from qiskit.circuit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.test.mock import FakeVigo
from qiskit.providers.aer.backends import PulseSimulator
backend = PulseSimulator.from_backend(FakeVigo())
circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure_all()
transpiled_circuit = transpile(circuit, backend)
backend.run(circuit)
```
Problemas conocidos
Se han desactivado SaveExpectationValue y SaveExpectationValueVariance para el método extended_stabilizer de QasmSimulator y AerSimulator debido a que devuelven un valor incorrecto para determinados componentes del operador Pauli. Consulte #1227 &lt;https://github.com/Qiskit/qiskit-aer/issues/1227&gt; para obtener más información y ejemplos.
Notas de actualización
La base predeterminada para la clase NoiseModel se ha cambiado de ["id", "u3", "cx"] a ["id", "rz", "sx", "cx"] debido a la desaprobación del método de circuito u3 en qiskit-terra y al cambio de las puertas de base del backend qiskit-ibmq-provider. Para utilizar las antiguas puertas base puedes inicializar un modelo de ruido con puertas base personalizadas como NoiseModel(basis_gates=[«id», “u3”, «cx»]).
Se ha eliminado el kwarg backend_options del methnod de ejecución de los backends Aer que quedó obsoleto en qiskit-aer 0.7. Ahora todas las opciones de ejecución deben pasarse como kwargs separados.
Eliminado pasar system_model como arg posicional para el método run del PulseSimulator.
Notas de desaprobación
Pasar un qobj ensamblado directamente al método run() de los backends del simulador Aer ha sido desaprobado en favor de pasar circuitos transpilados directamente como backend.run(circuits, **run_options).
Todas las instrucciones snapshot en qiskit.providers.aer.extensions han quedado obsoletas. Para reemplazarlas utiliza las instrucciones save del módulo qiskit.providers.aer.library.
La adición de errores cuánticos no locales a un NoiseModel ha quedado obsoleta debido a incoherencias en la forma en que este ruido se aplica al circuito optimizado. El ruido no local debe añadirse manualmente a un circuito programado en Qiskit utilizando un pase personalizado del transpilador antes de ejecutarlo en el simulador.
Se ha dejado de utilizar la opción de método de StatevectorSimulator y UnitarySimulator para ejecutar una simulación de GPU. Para ejecutar una simulación GPU en un sistema compatible, utilice en su lugar la opción device=“GPU”.
Otras notas
Mejora el rendimiento del algoritmo de muestreo de medidas para el método de simulación matrix_product_state. El nuevo comportamiento por defecto es muestrear siempre utilizando el método mejorado mps_apply_measure. El método de muestreo mps_probabilities puede seguir utilizándose estableciendo el valor de la opción personalizada mps_sample_measure_algorithm="mps_probabilities".
Ignis 0.6.0
Sin cambios
Aqua 0.9.5
Sin cambios
IBM Q Provider 0.16.0
Sin cambios