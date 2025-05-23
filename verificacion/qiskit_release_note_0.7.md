Qiskit 0.7 release notes
0.7
In Qiskit 0.7 we introduced Qiskit Aer and combined it with Qiskit Terra.

Terra 0.7
New Features
This release includes several new features and many bug fixes. With this release the interfaces for circuit diagram, histogram, bloch vectors, and state visualizations are declared stable. Additionally, this release includes a defined and standardized bit order/endianness throughout all aspects of Qiskit. These are all declared as stable interfaces in this release which won’t have breaking changes made moving forward, unless there is appropriate and lengthy deprecation periods warning of any coming changes.

There is also the introduction of the following new features:

A new ASCII art circuit drawing output mode
A new circuit drawing interface off of QuantumCircuit objects that enables calls of circuit.draw() or print(circuit) to render a drawing of circuits
A visualizer for drawing the DAG representation of a circuit
A new quantum state plot type for hinton diagrams in the local matplotlib based state plots
2 new constructor methods off the QuantumCircuit class from_qasm_str() and from_qasm_file() which let you easily create a circuit object from OpenQASM
A new function plot_bloch_multivector() to plot Bloch vectors from a tensored state vector or density matrix
Per-shot measurement results are available in simulators and select devices. These can be accessed by setting the memory kwarg to True when calling compile() or execute() and then accessed using the get_memory() method on the Result object.
A qiskit.quantum_info module with revamped Pauli objects and methods for working with quantum states
New transpile passes for circuit analysis and transformation: CommutationAnalysis, CommutationTransformation, CXCancellation, Decompose, Unroll, Optimize1QGates, CheckMap, CXDirection, BarrierBeforeFinalMeasurements
New alternative swap mapper passes in the transpiler: BasicSwap, LookaheadSwap, StochasticSwap
More advanced transpiler infrastructure with support for analysis passes, transformation passes, a global property_set for the pass manager, and repeat-until control of passes
Compatibility Considerations
As part of the 0.7 release the following things have been deprecated and will either be removed or changed in a backwards incompatible manner in a future release. While not strictly necessary these are things to adjust for before the next release to avoid a breaking change.

plot_circuit(), latex_circuit_drawer(), generate_latex_source(), and matplotlib_circuit_drawer() from qiskit.tools.visualization are deprecated. Instead the circuit_drawer() function from the same module should be used, there are kwarg options to mirror the functionality of all the deprecated functions.
The current default output of circuit_drawer() (using latex and falling back on python) is deprecated and will be changed to just use the text output by default in future releases.
The qiskit.wrapper.load_qasm_string() and qiskit.wrapper.load_qasm_file() functions are deprecated and the QuantumCircuit.from_qasm_str() and QuantumCircuit.from_qasm_file() constructor methods should be used instead.
The plot_barriers and reverse_bits keys in the style kwarg dictionary are deprecated, instead the qiskit.tools.visualization.circuit_drawer() kwargs plot_barriers and reverse_bits should be used instead.
The functions plot_state() and iplot_state() have been depreciated. Instead the functions plot_state_*() and iplot_state_*() should be called for the visualization method required.
The skip_transpiler argument has been deprecated from compile() and execute(). Instead you can use the PassManager directly, just set the pass_manager to a blank PassManager object with PassManager()
The transpile_dag() function format kwarg for emitting different output formats is deprecated, instead you should convert the default output DAGCircuit object to the desired format.
The unrollers have been deprecated, moving forward only DAG to DAG unrolling will be supported.
Please note that some backwards-incompatible changes have been made during this release. The following notes contain information on how to adapt to these changes.

Changes to Result objects
As part of the rewrite of the Results object to be more consistent and a stable interface moving forward a few changes have been made to how you access the data stored in the result object. First the get_data() method has been renamed to just data(). Accompanying that change is a change in the data format returned by the function. It is now returning the raw data from the backends instead of doing any post-processing. For example, in previous versions you could call:


result = execute(circuit, backend).result()
unitary = result.get_data()['unitary']
print(unitary)
and that would return the unitary matrix like:


[[1+0j, 0+0.5j], [0-0.5j][-1+0j]]
But now if you call (with the renamed method):


result.data()['unitary']
it will return something like:


[[[1, 0], [0, -0.5]], [[0, -0.5], [-1, 0]]]
To get the post processed results in the same format as before the 0.7 release you must use the get_counts(), get_statevector(), and get_unitary() methods on the result object instead of get_data()['counts'], get_data()['statevector'], and get_data()['unitary'] respectively.

Additionally, support for len() and indexing on a Result object has been removed. Instead you should deal with the output from the post processed methods on the Result objects.

Also, the get_snapshot() and get_snapshots() methods from the Result class have been removed. Instead you can access the snapshots using Result.data()['snapshots'].

Changes to Visualization
The largest change made to visualization in the 0.7 release is the removal of Matplotlib and other visualization dependencies from the project requirements. This was done to simplify the requirements and configuration required for installing Qiskit. If you plan to use any visualizations (including all the jupyter magics) except for the text, latex, and latex_source output for the circuit drawer you’ll you must manually ensure that the visualization dependencies are installed. You can leverage the optional requirements to the Qiskit Terra package to do this:


pip install qiskit-terra[visualization]
Aside from this there have been changes made to several of the interfaces as part of the stabilization which may have an impact on existing code. The first is the basis kwarg in the circuit_drawer() function is no longer accepted. If you were relying on the circuit_drawer() to adjust the basis gates used in drawing a circuit diagram you will have to do this priort to calling circuit_drawer(). For example:


from qiskit.tools import visualization
visualization.circuit_drawer(circuit, basis_gates='x,U,CX')
will have to be adjusted to be:


from qiskit import BasicAer
from qiskit import transpiler
from qiskit.tools import visualization
backend = BasicAer.backend('qasm_simulator')
draw_circ = transpiler.transpile(circuit, backend, basis_gates='x,U,CX')
visualization.circuit_drawer(draw_circ)
Moving forward the circuit_drawer() function will be the sole interface for circuit drawing in the visualization module. Prior to the 0.7 release there were several other functions which either used different output backends or changed the output for drawing circuits. However, all those other functions have been deprecated and that functionality has been integrated as options on circuit_drawer().

For the other visualization functions, plot_histogram() and plot_state() there are also a few changes to check when upgrading. First is the output from these functions has changed, in prior releases these would interactively show the output visualization. However that has changed to instead return a matplotlib.Figure object. This provides much more flexibility and options to interact with the visualization prior to saving or showing it. This will require adjustment to how these functions are consumed. For example, prior to this release when calling:


plot_histogram(counts)
plot_state(rho)
would open up new windows (depending on matplotlib backend) to display the visualization. However starting in the 0.7 you’ll have to call show() on the output to mirror this behavior. For example:


plot_histogram(counts).show()
plot_state(rho).show()
or:


hist_fig = plot_histogram(counts)
state_fig = plot_state(rho)
hist_fig.show()
state_fig.show()
Note that this is only for when running outside of Jupyter. No adjustment is required inside a Jupyter environment because Jupyter notebooks natively understand how to render matplotlib.Figure objects.

However, returning the Figure object provides additional flexibility for dealing with the output. For example instead of just showing the figure you can now directly save it to a file by leveraging the savefig() method. For example:


hist_fig = plot_histogram(counts)
state_fig = plot_state(rho)
hist_fig.savefig('histogram.png')
state_fig.savefig('state_plot.png')
The other key aspect which has changed with these functions is when running under jupyter. In the 0.6 release plot_state() and plot_histogram() when running under jupyter the default behavior was to use the interactive Javascript plots if the externally hosted Javascript library for rendering the visualization was reachable over the network. If not it would just use the matplotlib version. However in the 0.7 release this no longer the case, and separate functions for the interactive plots, iplot_state() and iplot_histogram() are to be used instead. plot_state() and plot_histogram() always use the matplotlib versions.

Additionally, starting in this release the plot_state() function is deprecated in favor of calling individual methods for each method of plotting a quantum state. While the plot_state() function will continue to work until the 0.9 release, it will emit a warning each time it is used. The

Qiskit Terra 0.6	Qiskit Terra 0.7+
plot_state(rho)	plot_state_city(rho)
plot_state(rho, method=’city’)	plot_state_city(rho)
plot_state(rho, method=’paulivec’)	plot_state_paulivec(rho)
plot_state(rho, method=’qsphere’)	plot_state_qsphere(rho)
plot_state(rho, method=’bloch’)	plot_bloch_multivector(rho)
plot_state(rho, method=’hinton’)	plot_state_hinton(rho)
The same is true for the interactive JS equivalent, iplot_state(). The function names are all the same, just with a prepended i for each function. For example, iplot_state(rho, method='paulivec') is iplot_state_paulivec(rho).

Changes to Backends
With the improvements made in the 0.7 release there are a few things related to backends to keep in mind when upgrading. The biggest change is the restructuring of the provider instances in the root qiskit` namespace. The Aer provider is not installed by default and requires the installation of the qiskit-aer package. This package contains the new high performance fully featured simulator. If you installed via pip install qiskit you’ll already have this installed. The python simulators are now available under qiskit.BasicAer and the old C++ simulators are available with qiskit.LegacySimulators. This also means that the implicit fallback to python based simulators when the C++ simulators are not found doesn’t exist anymore. If you ask for a local C++ based simulator backend, and it can’t be found an exception will be raised instead of just using the python simulator instead.

Additionally the previously deprecation top level functions register() and available_backends() have been removed. Also, the deprecated backend.parameters() and backend.calibration() methods have been removed in favor of backend.properties(). You can refer to the 0.6 release notes section Working with backends for more details on these changes.

The backend.jobs() and backend.retrieve_jobs() calls no longer return results from those jobs. Instead you must call the result() method on the returned jobs objects.

Changes to the compiler, transpiler, and unrollers
As part of an effort to stabilize the compiler interfaces there have been several changes to be aware of when leveraging the compiler functions. First it is important to note that the qiskit.transpiler.transpile() function now takes a QuantumCircuit object (or a list of them) and returns a QuantumCircuit object (or a list of them). The DAG processing is done internally now.

You can also easily switch between circuits, DAGs, and Qobj now using the functions in qiskit.converters.

Aer 0.1
New Features
Aer provides three simulator backends:

QasmSimulator: simulate experiments and return measurement outcomes
StatevectorSimulator: return the final statevector for a quantum circuit acting on the all zero state
UnitarySimulator: return the unitary matrix for a quantum circuit
noise module: contains advanced noise modeling features for the QasmSimulator

NoiseModel, QuantumError, ReadoutError classes for simulating a Qiskit quantum circuit in the presence of errors
errors submodule including functions for generating QuantumError objects for the following types of quantum errors: Kraus, mixed unitary, coherent unitary, Pauli, depolarizing, thermal relaxation, amplitude damping, phase damping, combined phase and amplitude damping
device submodule for automatically generating a noise model based on the BackendProperties of a device
utils module:

qobj_utils provides functions for directly modifying a Qobj to insert special simulator instructions not yet supported through the Qiskit Terra API.
Aqua 0.4
New Features
Programmatic APIs for algorithms and components – each component can now be instantiated and initialized via a single (non-empty) constructor call

QuantumInstance API for algorithm/backend decoupling – QuantumInstance encapsulates a backend and its settings

Updated documentation and Jupyter Notebooks illustrating the new programmatic APIs

Transparent parallelization for gradient-based optimizers

Multiple-Controlled-NOT (cnx) operation

Pluggable algorithmic component RandomDistribution

Concrete implementations of RandomDistribution: BernoulliDistribution, LogNormalDistribution, MultivariateDistribution, MultivariateNormalDistribution, MultivariateUniformDistribution, NormalDistribution, UniformDistribution, and UnivariateDistribution

Concrete implementations of UncertaintyProblem: FixedIncomeExpectedValue, EuropeanCallExpectedValue, and EuropeanCallDelta

Amplitude Estimation algorithm

Qiskit Optimization: New Ising models for optimization problems exact cover, set packing, vertex cover, clique, and graph partition

Qiskit AI:

New feature maps extending the FeatureMap pluggable interface: PauliExpansion and PauliZExpansion
Training model serialization/deserialization mechanism
Qiskit Finance:

Amplitude estimation for Bernoulli random variable: illustration of amplitude estimation on a single qubit problem
Loading of multiple univariate and multivariate random distributions
European call option: expected value and delta (using univariate distributions)
Fixed income asset pricing: expected value (using multivariate distributions)
The Pauli string in Operator class is aligned with Terra 0.7. Now the order of a n-qubit pauli string is q_{n-1}...q{0} Thus, the (de)serialier (save_to_dict and load_from_dict) in the Operator class are also changed to adopt the changes of Pauli class.

Compatibility Considerations
HartreeFock component of pluggable type InitialState moved to Qiskit Chemistry
UCCSD component of pluggable type VariationalForm moved to Qiskit Chemistry