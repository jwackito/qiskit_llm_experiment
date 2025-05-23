Qiskit 0.9 release notes
0.9
Terra 0.8
Highlights
Introduction of the Pulse module under
qiskit.pulse
, which includes tools for building pulse commands, scheduling them on pulse channels, visualization, and running them on IBM Q devices.
Improved QuantumCircuit and Instruction classes, allowing for the composition of arbitrary sub-circuits into larger circuits, and also for creating parameterized circuits.
A powerful Quantum Info module under
qiskit.quantum_info
, providing tools to work with operators and channels and to use them inside circuits.
New transpiler optimization passes and access to predefined transpiling routines.
New Features
The core
StochasticSwap
routine is implemented in
Cython
.
Added
QuantumChannel
classes for manipulating quantum channels and CPTP maps.
Support for parameterized circuits.
The
PassManager
interface has been improved and new functions added for easier interaction and usage with custom pass managers.
Preset
PassManager
s are now included which offer a predetermined pipeline of transpiler passes.
User configuration files to let local environments override default values for some functions.
New transpiler passes:
EnlargeWithAncilla
,
Unroll2Q
,
NoiseAdaptiveLayout
,
OptimizeSwapBeforeMeasure
,
RemoveDiagonalGatesBeforeMeasure
,
CommutativeCancellation
,
Collect2qBlocks
, and
ConsolidateBlocks
.
Compatibility Considerations
As part of the 0.8 release the following things have been deprecated and will either be removed or changed in a backwards incompatible manner in a future release. While not strictly necessary these are things to adjust for before the 0.9 (unless otherwise noted) release to avoid a breaking change in the future.
The methods prefixed by
_get
in the
DAGCircuit
object are being renamed without that prefix.
Changed elements in
couplinglist
of
CouplingMap
from tuples to lists.
Unroller bases must now be explicit, and violation raises an informative
QiskitError
.
The
qiskit.tools.qcvv
package is deprecated and will be removed in the in the future. You should migrate to using the Qiskit Ignis which replaces this module.
The
qiskit.compile()
function is now deprecated in favor of explicitly using the
qiskit.compiler.transpile()
function to transform a circuit, followed by
qiskit.compiler.assemble()
to make a Qobj out of it. Instead of
compile(...)
, use
assemble(transpile(...), ...)
.
qiskit.converters.qobj_to_circuits()
has been deprecated and will be removed in a future release. Instead
qiskit.assembler.disassemble()
should be used to extract
QuantumCircuit
objects from a compiled Qobj.
The
qiskit.mapper
namespace has been deprecated. The
Layout
and
CouplingMap
classes can be accessed via
qiskit.transpiler
.
A few functions in
qiskit.tools.qi.qi
have been deprecated and moved to
qiskit.quantum_info
.
Please note that some backwards incompatible changes have been made during this release. The following notes contain information on how to adapt to these changes.
IBM Q Provider
The IBM Q provider was previously included in Terra, but it has been split out into a separate package
qiskit-ibmq-provider
. This will need to be installed, either via pypi with
pip install qiskit-ibmq-provider
or from source in order to access
qiskit.IBMQ
or
qiskit.providers.ibmq
. If you install qiskit with
pip install qiskit
, that will automatically install all subpackages of the Qiskit project.
Cython Components
Starting in the 0.8 release the core stochastic swap routine is now implemented in
Cython
. This was done to significantly improve the performance of the swapper, however if you build Terra from source or run on a non-x86 or other platform without prebuilt wheels and install from source distribution you’ll need to make sure that you have Cython installed prior to installing/building Qiskit Terra. This can easily be done with pip/pypi:
pip install Cython
.
Compiler Workflow
The
qiskit.compile()
function has been deprecated and replaced by first calling
qiskit.compiler.transpile()
to run optimization and mapping on a circuit, and then
qiskit.compiler.assemble()
to build a Qobj from that optimized circuit to send to a backend. While this is only a deprecation it will emit a warning if you use the old
qiskit.compile()
call.
transpile(), assemble(), execute() parameters
These functions are heavily overloaded and accept a wide range of inputs. They can handle circuit and pulse inputs. All kwargs except for
backend
for these functions now also accept lists of the previously accepted types. The
initial_layout
kwarg can now be supplied as a both a list and dictionary, e.g. to map a Bell experiment on qubits 13 and 14, you can supply:
initial_layout=[13, 14]
or
initial_layout={qr[0]: 13, qr[1]: 14}
Qobj
The Qobj class has been split into two separate subclasses depending on the use case, either
PulseQobj
or
QasmQobj
for pulse and circuit jobs respectively. If you’re interacting with Qobj directly you may need to adjust your usage accordingly.
The
qiskit.qobj.qobj_to_dict()
is removed. Instead use the
to_dict()
method of a Qobj object.
Visualization
The largest change to the visualization module is it has moved from
qiskit.tools.visualization
to
qiskit.visualization
. This was done to indicate that the visualization module is more than just a tool. However, since this interface was declared stable in the 0.7 release the public interface off of
qiskit.tools.visualization
will continue to work. That may change in a future release, but it will be deprecated prior to removal if that happens.
The previously deprecated functions,
plot_circuit()
,
latex_circuit_drawer()
,
generate_latex_source()
, and
matplotlib_circuit_drawer()
from
qiskit.tools.visualization
have been removed. Instead of these functions, calling
qiskit.visualization.circuit_drawer()
with the appropriate arguments should be used.
The previously deprecated
plot_barriers
and
reverse_bits
keys in the
style
kwarg dictionary are deprecated, instead the
qiskit.visualization.circuit_drawer()
kwargs
plot_barriers
and
reverse_bits
should be used.
The Wigner plotting functions
plot_wigner_function
,
plot_wigner_curve
,
plot_wigner_plaquette
, and
plot_wigner_data
previously in the
qiskit.tools.visualization._state_visualization
module have been removed. They were never exposed through the public stable interface and were not well documented. The code to use this feature can still be accessed through the qiskit-tutorials repository.
Mapper
The public api from
qiskit.mapper
has been moved into
qiskit.transpiler
. While it has only been deprecated in this release, it will be removed in the 0.9 release so updating your usage of
Layout
and
CouplingMap
to import from
qiskit.transpiler
instead of
qiskit.mapper
before that takes place will avoid any surprises in the future.
Aer 0.2
New Features
Added multiplexer gate
qiskit-aer #192
Added
remap_noise_model
function to
noise.utils
qiskit-aer #181
Added
__eq__
method to
NoiseModel
,
QuantumError
,
ReadoutError
qiskit-aer #181
Added support for labelled gates in noise models
qiskit-aer #175
Added optimized
mcx
,
mcy
,
mcz
,
mcu1
,
mcu2
,
mcu3
, gates to
QubitVector
qiskit-aer #124
Added optimized controlled-swap gate to
QubitVector
qiskit-aer #142
Added gate-fusion optimization for
QasmController
, which is enabled by setting
fusion_enable=true
qiskit-aer #136
Added better management of failed simulations
qiskit-aer #167
Added qubits truncate optimization for unused qubits
qiskit-aer #164
Added ability to disable depolarizing error on device noise model
qiskit-aer #131
Added initialize simulator instruction to
statevector_state
qiskit-aer #117
,
qiskit-aer #137
Added coupling maps to simulators
qiskit-aer #93
Added circuit optimization framework
qiskit-aer #83
Added benchmarking
qiskit-aer #71
,
qiskit-aer #177
Added wheels support for Debian-like distributions
qiskit-aer #69
Added autoconfiguration of threads for qasm simulator
qiskit-aer #61
Added Simulation method based on Stabilizer Rank Decompositions
qiskit-aer #51
Added
basis_gates
kwarg to
NoiseModel
init
qiskit-aer #175
.
Added an optional parameter to
NoiseModel.as_dict()
for returning dictionaries that can be serialized using the standard json library directly
qiskit-aer #165
Refactor thread management
qiskit-aer #50
Improve noise transformations
qiskit-aer #162
Improve error reporting
qiskit-aer #160
Improve efficiency of parallelization with
max_memory_mb
a new parameter of
backend_opts
qiskit-aer #61
Improve u1 performance in
statevector
qiskit-aer #123
Bug Fixes
Fixed OpenMP clashing problems on macOS for the Terra add-on
qiskit-aer #46
Compatibility Considerations
Deprecated
"initial_statevector"
backend option for
QasmSimulator
and
StatevectorSimulator
qiskit-aer #185
Renamed
"chop_threshold"
backend option to
"zero_threshold"
and changed default value to 1e-10
qiskit-aer #185
Ignis 0.1
New Features
Quantum volume
Measurement mitigation using tensored calibrations
Simultaneous RB has the option to align Clifford gates across subsets
Measurement correction can produce a new calibration for a subset of qubits
Compatibility Considerations
RB writes to the minimal set of classical registers (it used to be Q[i]->C[i]). This change enables measurement correction with RB. Unless users had external analysis code, this will not change outcomes. RB circuits from 0.1 are not compatible with 0.1.1 fitters.
Aqua 0.5
New Features
Implementation of the HHL algorithm supporting
LinearSystemInput
Pluggable component
Eigenvalues
with variant
EigQPE
Pluggable component
Reciprocal
with variants
LookupRotation
and
LongDivision
Multiple-Controlled U1 and U3 operations
mcu1
and
mcu3
Pluggable component
QFT
derived from component
IQFT
Summarized the transpiled circuits at the DEBUG logging level
QuantumInstance
accepts
basis_gates
and
coupling_map
again.
Support to use
cx
gate for the entanglement in
RY
and
RYRZ
variational form (
cz
is the default choice)
Support to use arbitrary mixer Hamiltonian in QAOA, allowing use of QAOA in constrained optimization problems [arXiv:1709.03489]
Added variational algorithm base class
VQAlgorithm
, implemented by
VQE
and
QSVMVariational
Added
ising/docplex.py
for automatically generating Ising Hamiltonian from optimization models of DOcplex
Added
'basic-dirty-ancilla
’ mode for
mct
Added
mcmt
for Multi-Controlled, Multi-Target gate
Exposed capabilities to generate circuits from logical AND, OR, DNF (disjunctive normal forms), and CNF (conjunctive normal forms) formulae
Added the capability to generate circuits from ESOP (exclusive sum of products) formulae with optional optimization based on Quine-McCluskey and ExactCover
Added
LogicalExpressionOracle
for generating oracle circuits from arbitrary Boolean logic expressions (including DIMACS support) with optional optimization capability
Added
TruthTableOracle
for generating oracle circuits from truth-tables with optional optimization capability
Added
CustomCircuitOracle
for generating oracle from user specified circuits
Added implementation of the Deutsch-Jozsa algorithm
Added implementation of the Bernstein-Vazirani algorithm
Added implementation of the Simon’s algorithm
Added implementation of the Shor’s algorithm
Added optional capability for Grover’s algorithm to take a custom initial state (as opposed to the default uniform superposition)
Added capability to create a
Custom
initial state using existing circuit
Added the ADAM (and AMSGRAD) optimization algorithm
Multivariate distributions added, so uncertainty models now have univariate and multivariate distribution components
Added option to include or skip the swaps operations for qft and iqft circuit constructions
Added classical linear system solver
ExactLSsolver
Added parameters
auto_hermitian
and
auto_resize
to
HHL
algorithm to support non-Hermitian and non
2
n
2^n
2
n
sized matrices by default
Added another feature map,
RawFeatureVector
, that directly maps feature vectors to qubits’ states for classification
SVM_Classical
can now load models trained by
QSVM
Bug Fixes
Fixed
ising/docplex.py
to correctly multiply constant values in constraints
Fixed package setup to correctly identify namespace packages using
setuptools.find_namespace_packages
Compatibility Considerations
QuantumInstance
does not take
memory
anymore.
Moved command line and GUI to separate repo (
qiskit_aqua_uis
)
Removed the
SAT
-specific oracle (now supported by
LogicalExpressionOracle
)
Changed
advanced
mode implementation of
mct
: using simple
h
gates instead of
ch
, and fixing the old recursion step in
_multicx
Components
random_distributions
renamed to
uncertainty_models
Reorganized the constructions of various common gates (
ch
,
cry
,
mcry
,
mct
,
mcu1
,
mcu3
,
mcmt
,
logic_and
, and
logic_or
) and circuits (
PhaseEstimationCircuit
,
BooleanLogicCircuits
,
FourierTransformCircuits
, and
StateVectorCircuits
) under the
circuits
directory
Renamed the algorithm
QSVMVariational
to
VQC
, which stands for Variational Quantum Classifier
Renamed the algorithm
QSVMKernel
to
QSVM
Renamed the class
SVMInput
to
ClassificationInput
Renamed problem type
'svm_classification'
to
'classification'
Changed the type of
entangler_map
used in
FeatureMap
and
VariationalForm
to list of lists
IBM Q Provider 0.1
New Features
This is the first release as a standalone package. If you are installing Terra standalone you’ll also need to install the
qiskit-ibmq-provider
package with
pip install qiskit-ibmq-provider
if you want to use the IBM Q backends.
Support for non-Qobj format jobs has been removed from the provider. You’ll have to convert submissions in an older format to Qobj before you can submit.