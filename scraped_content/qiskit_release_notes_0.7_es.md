Qiskit 0.7 notas de la versión
0.7
En Qiskit 0.7 introducimos Qiskit Aer y lo combinamos con Qiskit Terra.
Terra 0.7
Nuevas características
Esta versión incluye varias características nuevas y muchas correcciones de errores. Con esta versión las interfaces para diagrama de circuito, histograma, vectores bloch y visualizaciones de estado se declaran estables. Además, esta versión incluye un orden de bits/endiancia definido y estandarizado en todos los aspectos de Qiskit. Todos estos son declarados como interfaces estables en esta versión que no tendrán cambios de ruptura en el futuro, a menos que haya períodos de depreciación apropiados y prolongados advirtiendo de los cambios que se avecinan.
También hay la introducción de las siguientes nuevas características:
Un nuevo modo de salida de dibujo de circuitos en arte ASCII
Una nueva interfaz de dibujo de circuitos a partir de objetos QuantumCircuit que permite llamadas de circuit. draw() o print(circuit) para renderizar un dibujo de circuitos
Un visualizador para dibujar la representación DAG de un circuito
Un nuevo tipo de trazado de estado cuántico para diagramas de Hinton en los trazados de estado locales basados en matplotlib
2 nuevos métodos constructores de la clase QuantumCircuit from_qasm_str() y from_qasm_file() que permiten crear fácilmente un objeto de circuito desde OpenQASM
Una nueva función plot_bloch_multivector() para trazar vectores Bloch desde un vector de estado tensado o una matriz de densidad
Los resultados de las mediciones por disparo están disponibles en los simuladores. Los resultados de las mediciones por disparo están disponibles en simuladores y dispositivos seleccionados. Se puede acceder a ellos estableciendo el kwarg de memoria en True cuando se llama a compile() o execute() y luego se accede utilizando el método get_memory() en el objeto Result.
Un módulo qiskit.quantum_info con objetos Pauli renovados y métodos para trabajar con estados cuánticos
Nuevos pases transpile para análisis y transformación de circuitos: CommutationAnalysis, CommutationTransformation, CXCancellation, Decompose, Unroll, Optimize1QGates, CheckMap, CXDirection, BarrierBeforeFinalMeasurements
Nuevos pases swapper alternativos en el transpilador: BasicSwap, LookaheadSwap, StochasticSwap
Infraestructura de transpilador más avanzada con soporte para pases de análisis, pases de transformación, un property_set global para el gestor de pases y control de repetición hasta el final de los pases.

Consideraciones de compatibilidad
Como parte de la versión 0.7, las siguientes cosas han sido obsoletas y serán eliminadas o cambiadas de forma incompatible en una futura versión. Aunque no es estrictamente necesario, estas son cosas para ajustar antes de la próxima versión para evitar un cambio de ruptura.
plot_circuit(), latex_circuit_drawer(), generate_latex_source(), y matplotlib_circuit_drawer() de qiskit.tools.visualization están obsoletos. En su lugar se debe utilizar la función circuit_drawer() del mismo módulo, hay opciones kwarg para reflejar la funcionalidad de todas las funciones obsoletas.
La salida actual por defecto de circuit_drawer() (usando latex y recurriendo a python) está obsoleta y se cambiará para usar sólo la salida de texto por defecto en futuras versiones.
Las funciones qiskit.wrapper.load_qasm_string() y qiskit.wrapper.load_qasm_file() están obsoletas y en su lugar deben utilizarse los métodos constructores QuantumCircuit.from_qasm_str() y QuantumCircuit.from_qasm_file().
Las claves plot_barriers y reverse_bits en el diccionario style kwarg están obsoletas, en su lugar deben utilizarse los kwargs qiskit.tools.visualization.circuit_drawer() plot_barriers y reverse_bits.
Las funciones plot_state() y iplot_state() han sido depreciadas. En su lugar, se debe llamar a las funciones plot_state_*() y iplot_state_*() para el método de visualización requerido.
El argumento skip_transpiler ha sido depreciado de compile() y execute(). En su lugar, puede utilizar el PassManager directamente, sólo tiene que establecer el pass_manager a un objeto PassManager en blanco con PassManager()
El kwarg de formato de la función transpile_dag() para emitir diferentes formatos de salida está obsoleto, en su lugar debe convertir el objeto DAGCircuit de salida por defecto al formato deseado.
Los desenrolladores han quedado obsoletos, en adelante sólo se soportará el desenrollado de DAG a DAG.
Tenga en cuenta que en esta versión se han realizado algunos cambios incompatibles con versiones anteriores. Las siguientes notas contienen información sobre cómo adaptarse a estos cambios.

Cambios en los objetos Resultado
Como parte de la reescritura del objeto Resultado para que sea más consistente y una interfaz estable de cara al futuro, se han realizado algunos cambios en la forma de acceder a los datos almacenados en el objeto resultado. En primer lugar, el método get_data() ha pasado a llamarse simplemente data(). Este cambio va acompañado de un cambio en el formato de los datos devueltos por la función. Ahora devuelve los datos sin procesar de los backends en lugar de hacer ningún post-procesamiento. Por ejemplo, en versiones anteriores se podía llamar a:
```python
result = execute(circuit, backend).result()
unitary = result.get_data()['unitary']
print(unitary)
```
y que devolvería la matriz unitaria como:
```python
[[1+0j, 0+0.5j], [0-0.5j][-1+0j]]
```
Pero ahora si llamas (con el método renombrado):
```python
result.data()['unitary']
```
devolverá algo como:
```python
[[[1, 0], [0, -0.5]], [[0, -0.5], [-1, 0]]]
```
Para obtener los resultados postprocesados en el mismo formato que antes de la versión 0.7, debe utilizar los métodos get_counts(), get_statevector() y get_unitary() en el objeto result en lugar de get_data()[“counts”], get_data()[“statevector”] y get_data()[“unitary”] respectivamente.
Además, se ha eliminado el soporte para len() y la indexación en un objeto Result. En su lugar, deberá tratar con la salida de los métodos postprocesados en los objetos Resultado.
También se han eliminado los métodos get_snapshot() y get_snapshots() de la clase Result. En su lugar, se puede acceder a las instantáneas utilizando Result.data()[“snapshots”].
Cambios en la visualización
El mayor cambio realizado en la visualización en la versión 0.7 es la eliminación de Matplotlib y otras dependencias de visualización de los requisitos del proyecto. Esto se hizo para simplificar los requisitos y la configuración necesaria para instalar Qiskit. Si planeas usar cualquier visualización (incluyendo todas las magias de jupyter) excepto la salida de texto, latex y latex_source para el cajón del circuito, deberás asegurarte manualmente de que las dependencias de visualización están instaladas. Para ello, puedes aprovechar los requisitos opcionales del paquete Qiskit Terra:
pip install qiskit-terra[visualization]
Aparte de esto, se han realizado cambios en varias de las interfaces como parte de la estabilización que pueden tener un impacto en el código existente. El primero es que ya no se acepta el kwarg de base en la función circuit_drawer(). Si confiaba en circuit_drawer() para ajustar las puertas base utilizadas en el dibujo de un circuito, tendrá que hacerlo antes de llamar a circuit_drawer(). Por ejemplo:
```python
from qiskit.tools import visualization
visualization.circuit_drawer(circuit, basis_gates='x,U,CX')
```
tendrá que ajustarse para ser:
```python
from qiskit import BasicAer
from qiskit import transpiler
from qiskit.tools import visualization
backend = BasicAer.backend('qasm_simulator')
draw_circ = transpiler.transpile(circuit, backend, basis_gates='x,U,CX')
visualization.circuit_drawer(draw_circ)
```
En adelante, la función circuit_drawer() será la única interfaz para el dibujo de circuitos en el módulo de visualización. Antes de la versión 0.7 había otras funciones que utilizaban diferentes salidas o cambiaban la salida para dibujar circuitos. Sin embargo, todas esas otras funciones han quedado obsoletas y esa funcionalidad se ha integrado como opciones en circuit_drawer().
Para las otras funciones de visualización, plot_histogram() y plot_state() también hay algunos cambios que comprobar al actualizar. El primero es que la salida de estas funciones ha cambiado, en versiones anteriores estas mostraban interactivamente la visualización de salida. Sin embargo, esto ha cambiado para devolver un objeto matplotlib.Figure. Esto proporciona mucha más flexibilidad y opciones para interactuar con la visualización antes de guardarla o mostrarla. Esto requerirá un ajuste en la forma en que se consumen estas funciones. Por ejemplo, antes de esta versión cuando se llamaba a:
```python
plot_histogram(counts)
plot_state(rho)
```
abriría nuevas ventanas (dependiendo del backend matplotlib) para mostrar la visualización. Sin embargo, a partir de la versión 0.7 tendrá que llamar a show() en la salida para reflejar este comportamiento. Por ejemplo:
```python
plot_histogram(counts).show()
plot_state(rho).show()
```
o:
```python
hist_fig = plot_histogram(counts)
state_fig = plot_state(rho)
hist_fig.show()
state_fig.show()
```
Tenga en cuenta que esto es sólo para cuando se ejecuta fuera de Jupyter. No se requiere ningún ajuste dentro de un entorno Jupyter porque los cuadernos Jupyter entienden de forma nativa cómo renderizar objetos matplotlib.Figure.
Sin embargo, devolver el objeto Figure proporciona flexibilidad adicional para tratar la salida. Por ejemplo, en lugar de simplemente mostrar la figura, ahora puede guardarla directamente en un archivo utilizando el método savefig(). Por ejemplo:
```python
hist_fig = plot_histogram(counts)
state_fig = plot_state(rho)
hist_fig.savefig('histogram.png')
state_fig.savefig('state_plot.png')
```
El otro aspecto clave que ha cambiado con estas funciones es cuando se ejecuta bajo jupyter. En la versión 0.6 plot_state() y plot_histogram() cuando se ejecutaban bajo jupyter el comportamiento por defecto era utilizar los gráficos Javascript interactivos si la librería Javascript alojada externamente para renderizar la visualización era accesible a través de la red. En caso contrario, se utilizaba la versión matplotlib. Sin embargo, en la versión 0.7 esto ya no es así, y en su lugar se utilizarán funciones separadas para los gráficos interactivos, iplot_state() e iplot_histogram(). plot_state() y plot_histogram() siempre utilizan las versiones de matplotlib.
Además, a partir de esta versión, la función plot_state() queda obsoleta en favor de la llamada a métodos individuales para cada método de trazado de un estado cuántico. Aunque la función plot_state() seguirá funcionando hasta la versión 0.9, emitirá una advertencia cada vez que se utilice:
Qiskit Terra 0.6	Qiskit Terra 0.7+
plot_state(rho)	plot_state_city(rho)
plot_state(rho, method=’city’)	plot_state_city(rho)
plot_state(rho, method=’paulivec’)	plot_state_paulivec(rho)
plot_state(rho, method=’qsphere’)	plot_state_qsphere(rho)
plot_state(rho, method=’bloch’)	plot_bloch_multivector(rho)
plot_state(rho, method=’hinton’)	plot_state_hinton(rho)
Lo mismo ocurre con el equivalente interactivo en JS, iplot_state(). Los nombres de las funciones son los mismos, sólo que con una i antepuesta para cada función. Por ejemplo, iplot_state(rho, method=“paulivec”) es iplot_state_paulivec(rho).
Cambios en los backends
Con las mejoras introducidas en la versión 0.7 hay algunas cosas relacionadas con los backends que hay que tener en cuenta al actualizar. El mayor cambio es la reestructuración de las instancias del proveedor en el espacio de nombres raíz qiskit`. El proveedor Aer no está instalado por defecto y requiere la instalación del paquete qiskit-aer. Este paquete contiene el nuevo simulador de alto rendimiento con todas las funciones. Si lo instalaste mediante pip install qiskit ya lo tendrás instalado. Los simuladores python están ahora disponibles bajo qiskit.BasicAer y los antiguos simuladores C++ están disponibles con qiskit.LegacySimulators. Esto también significa que el fallback implícito a los simuladores basados en python cuando los simuladores C++ no se encuentran ya no existe. Si pides un simulador local basado en C++, y no se puede encontrar, se lanzará una excepción en lugar de utilizar el simulador python.
Además, se han eliminado las funciones de nivel superior register() y available_backends(), anteriormente obsoletas. También se han eliminado los métodos obsoletos backend.parameters() y backend.calibration() en favor de backend.properties(). Puedes consultar la sección de notas de la versión 0.6 Trabajando con backends para más detalles sobre estos cambios.
Las llamadas a backend.jobs() y backend.retrieve_jobs() ya no devuelven resultados de esos trabajos. En su lugar, debes llamar al método result() en los objetos jobs devueltos.
Cambios en el compilador, el transpilador y los desenrolladores
Como parte de un esfuerzo por estabilizar las interfaces del compilador, se han producido varios cambios que deben tenerse en cuenta al utilizar las funciones del compilador. En primer lugar es importante señalar que la función qiskit.transpiler.transpile() ahora toma un objeto QuantumCircuit (o una lista de ellos) y devuelve un objeto QuantumCircuit (o una lista de ellos). El procesamiento DAG se hace internamente ahora.
También puede cambiar fácilmente entre circuitos, DAGs, y Qobj ahora utilizando las funciones en qiskit.converters.
Aer 0.1
Nuevas características
Aer proporciona tres simuladores:
QasmSimulator: simula experimentos y devuelve los resultados de las mediciones
StatevectorSimulator: devuelve el vector de estado final para un circuito cuántico que actúa sobre el estado todo cero
UnitarySimulator: devuelve la matriz unitaria para un circuito cuántico
noise module: contiene funciones avanzadas de modelado de ruido para el QasmSimulator
NoiseModel, QuantumError, ReadoutError classes for simulating a Qiskit quantum circuit in the presence of errors
errors submodule including functions for generating QuantumError objects for the following types of quantum errors: Kraus, unitario mixto, unitario coherente, Pauli, despolarizante, relajación térmica, amortiguación de amplitud, amortiguación de fase, amortiguación combinada de fase y amplitud
device submodule para generar automáticamente un modelo de ruido basado en las BackendProperties de un dispositivo
utils module:
qobj_utils proporciona funciones para modificar directamente un Qobj para insertar instrucciones especiales del simulador aún no soportadas a través de la API de Qiskit Terra.
Aqua 0.4
Nuevas características
APIs programáticas para algoritmos y componentes - cada componente puede ahora ser instanciado e inicializado a través de una única (no vacía) llamada al constructor.
API QuantumInstance para la disociación algoritmo/backend - QuantumInstance encapsula un backend y su configuración
Documentación actualizada y cuadernos Jupyter que ilustran las nuevas API programáticas
Paralelización transparente para optimizadores basados en gradientes
Operación múltiple-NOT controlada (cnx)
Componente algorítmico enchufable RandomDistribution
Implementaciones concretas de RandomDistribution: BernoulliDistribution, LogNormalDistribution, MultivariateDistribution, MultivariateNormalDistribution, MultivariateUniformDistribution, NormalDistribution, UniformDistribution y UnivariateDistribution
Implementaciones concretas de UncertaintyProblem: FixedIncomeExpectedValue, EuropeanCallExpectedValue y EuropeanCallDelta
Algoritmo de estimación de amplitud
Optimización Qiskit: Nuevos modelos Ising para problemas de optimización: cobertura exacta, empaquetamiento de conjuntos, cobertura de vértices, camarilla y partición de grafos
Qiskit AI:
Nuevos mapas de características que amplían la interfaz conectable FeatureMap: PauliExpansion y PauliZExpansion
Mecanismo de serialización/deserialización de modelos de formación
Qiskit Finance:
Estimación de amplitud para una variable aleatoria Bernoulli: ilustración de la estimación de amplitud en un problema de un solo qubit
Carga de múltiples distribuciones aleatorias univariantes y multivariantes
Opción de compra europea: valor esperado y delta (usando distribuciones univariantes)
Valoración de activos de renta fija: valor esperado (usando distribuciones multivariantes)
La cadena Pauli en la clase Operator se alinea con Terra 0.7. Ahora el orden de una cadena pauli de n-qubit es q_{n-1}...q{0} Por lo tanto, los (de)serialier (save_to_dict y load_from_dict) en la clase Operator también se modifican para adoptar los cambios de la clase Pauli.
Consideraciones de compatibilidad
HartreeFock componente de tipo enchufable InitialState movido a Qiskit Chemistry
UCCSD componente de tipo enchufable VariationalForm movido a Qiskit Chemistry