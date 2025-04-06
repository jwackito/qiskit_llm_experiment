Notas de la versión de Qiskit 0.5
Terra 0.5
Aspectos destacados
Esta versión trae una serie de mejoras a Qiskit, tanto para la experiencia del usuario y bajo el capó. Por favor, consulte el changelog completo para una descripción detallada de los cambios - los más destacados son: 
nuevos simuladores de vectores de estado y mejoras en las características y el rendimiento de los ya existentes (en particular para el simulador de C ++), junto con una reorganización de la forma de trabajar con backends centrado en la extensibilidad y flexibilidad (utilizando alias y proveedores de backend)
reorganización de las características asíncronas, proporcionando una interfaz más amigable para ejecutar trabajos de forma asíncrona a través de instancias de Trabajo
numerosas mejoras y correcciones en el conjunto de Terra, tanto para comodidad de los usuarios (como permitir registros anónimos) como para mejorar la funcionalidad (como el trazado mejorado de circuitos)
Compatibilidad
Tenga en cuenta que en esta versión se han introducido varios cambios incompatibles con versiones anteriores como resultado del desarrollo en curso. Mientras que algunas de estas características seguirán siendo compatibles durante un período de tiempo antes de ser totalmente obsoletas, se recomienda actualizar sus programas con el fin de prepararse para las nuevas versiones y aprovechar las nuevas funcionalidades.
Cambios en QuantumProgram
Varios métodos de la clase QuantumProgram están en camino de ser obsoletos:
métodos para interactuar con los backends y la API:
La forma recomendada para abrir una conexión a la API de IBM Q y para utilizar los backends es a través de las funciones de nivel superior directamente en lugar de los métodos QuantumProgram. En particular, el método qiskit.register() proporciona el equivalente de la anterior llamada qiskit.QuantumProgram.set_api(). De forma similar, hay un nuevo qiskit.available_backends(), qiskit.get_backend() y funciones relacionadas para consultar directamente los backends disponibles. Por ejemplo, el siguiente fragmento para la versión 0.4:

```python
from qiskit import QuantumProgram
quantum_program = QuantumProgram()
quantum_program.set_api(token, url)
backends = quantum_program.available_backends()
print(quantum_program.get_backend_status('ibmqx4')
```
sería equivalente al siguiente fragmento para la versión 0.5:
```python
from qiskit import register, available_backends, get_backend
register(token, url)
backends = available_backends()
backend = get_backend('ibmqx4')
print(backend.status)
```
para compilar y ejecutar programas:
Las funciones de nivel superior ahora también proporcionan equivalentes para los métodos qiskit.QuantumProgram.compile() y qiskit.QuantumProgram.execute(). Por ejemplo, el siguiente fragmento de la versión 0.4:
```python
quantum_program.execute(circuit, args, ...)
```
sería equivalente al siguiente fragmento para la versión 0.5:
```python
from qiskit import execute
execute(circuit, args, ...)
```
En general, a partir de la versión 0.5 animamos a intentar hacer uso de los objetos y clases individuales directamente en lugar de depender de QuantumProgram. Por ejemplo, un QuantumCircuit puede ser instanciado y construido anexando QuantumRegister, ClassicalRegister, y gates directamente. Por favor, comprueba el ejemplo de actualización en la sección Quickstart, o los ejemplos using_qiskit_core_level_0.py y using_qiskit_core_level_1.py en el repositorio principal.
Cambios en el nombre del backend
Con el fin de proporcionar un marco más extensible para los backends, ha habido algunos cambios de diseño en consecuencia:
nombres de simuladores locales
Se han homogeneizado los nombres de los simuladores locales para que sigan el mismo patrón: PROVIDERNAME_TYPE_simulator_LANGUAGEORPROJECT - por ejemplo, el simulador C++ antes llamado local_qiskit_simulator es ahora local_qasm_simulator_cpp. Una visión general de los simuladores actuales:
Se supone que el simulador QASM es como un experimento. Aplicas un circuito en algunos qubits, y observas los resultados de la medición - y repites durante muchos disparos para obtener un histograma de conteos a través de result.get_counts().
El simulador de vector de estado es para obtener el vector de estado completo (2n amplitudes) después de evolucionar el estado cero a través del circuito, y se puede obtener a través de result.get_statevector().
El simulador unitario es para obtener la matriz unitaria equivalente del circuito, devuelta a través de result.get_unitary().
Además, puede obtener estados intermedios de un simulador aplicando una instrucción snapshot(slot) en varios puntos del circuito. Esto guardará el estado actual del simulador en una ranura determinada, que puede recuperarse posteriormente mediante result.get_snapshot(slot).
Alias de backend:
El SDK proporciona ahora un sistema de «alias» que permite utilizar automáticamente el simulador de mayor rendimiento de un tipo específico, si está disponible en su sistema. Por ejemplo, con el siguiente fragmento de código:
```python
from qiskit import get_backend
backend = get_backend('local_statevector_simulator')
```
el backend será el simulador de vectores de estado C++ si está disponible, recurriendo al simulador de vectores de estado Python si no está presente.
Nombres y parámetros más flexibles
Varias funciones del SDK se han hecho más flexibles y fáciles de usar:
nombres automáticos de circuitos y registros
qiskit.ClassicalRegister, qiskit.QuantumRegister y qiskit.QuantumCircuit ahora pueden ser instanciados sin darles explícitamente un nombre - una nueva función de autonaming les asignará automáticamente un identificador:
```python
q = QuantumRegister(2)
```
Observe también que se ha intercambiado el orden de los parámetros QuantumRegister(size, name).
Métodos que aceptan nombres o instancias
En combinación con los cambios de autonaming, varios métodos como qiskit.Result.get_data() ahora aceptan tanto nombres como instancias para mayor comodidad. Por ejemplo, al recuperar los resultados de un trabajo que tiene un solo circuito como:
```python
qc = QuantumCircuit(..., name='my_circuit')
job = execute(qc, ...)
result = job.result()
```
Las siguientes llamadas son equivalentes:
```python
data = result.get_data('my_circuit')
data = result.get_data(qc)
data = result.get_data()
```