Qiskit 0.12 release notes
0.12.0
Terra 0.9
Prelude
The 0.9 release includes many new features and many bug fixes. The biggest changes for this release are new debugging capabilities for PassManagers. This includes a function to visualize a PassManager, the ability to add a callback function to a PassManager, and logging of passes run in the PassManager. Additionally, this release standardizes the way that you can set an initial layout for your circuit. So now you can leverage
initial_layout
the kwarg parameter on
qiskit.compiler.transpile()
and
qiskit.execute()
and the qubits in the circuit will get laid out on the desire qubits on the device. Visualization of circuits will now also show this clearly when visualizing a circuit that has been transpiled with a layout.
New Features
A
DAGCircuit
object (i.e. the graph representation of a QuantumCircuit where operation dependencies are explicit) can now be visualized with the
.draw()
method. This is in line with Qiskit’s philosophy of easy visualization. Other objects which support a
.draw()
method are
QuantumCircuit
,
PassManager
, and
Schedule
.
Added a new visualization function
qiskit.visualization.plot_error_map()
to plot the error map for a given backend. It takes in a backend object from the qiskit-ibmq-provider and will plot the current error map for that device.
Both
qiskit.QuantumCircuit.draw()
and
qiskit.visualization.circuit_drawer()
now support annotating the qubits in the visualization with layout information. If the
QuantumCircuit
object being drawn includes layout metadata (which is normally only set on the circuit output from
transpile()
calls) then by default that layout will be shown on the diagram. This is done for all circuit drawer backends. For example:
from
qiskit
import
ClassicalRegister
,
QuantumCircuit
,
QuantumRegister
from
qiskit
.
compiler
import
transpile
qr
=
QuantumRegister
(
2
,
'userqr'
)
cr
=
ClassicalRegister
(
2
,
'c0'
)
qc
=
QuantumCircuit
(qr, cr)
qc
.
h
(qr[
0
])
qc
.
cx
(qr[
0
], qr[
1
])
qc
.
y
(qr[
0
])
qc
.
x
(qr[
1
])
qc
.
measure
(qr, cr)
# Melbourne coupling map
coupling_map
=
[[
1
,
0
]
,
[
1
,
2
]
,
[
2
,
3
]
,
[
4
,
3
]
,
[
4
,
10
]
,
[
5
,
4
]
,
[
5
,
6
]
,
[
5
,
9
]
,
[
6
,
8
]
,
[
7
,
8
]
,
[
9
,
8
]
,
[
9
,
10
]
,
[
11
,
3
]
,
[
11
,
10
]
,
[
11
,
12
]
,
[
12
,
2
]
,
[
13
,
1
]
,
[
13
,
12
]]
qc_result
=
transpile
(qc, basis_gates
=
[
'u1'
,
'u2'
,
'u3'
,
'cx'
,
'id'
],
coupling_map
=
coupling_map, optimization_level
=
0
)
qc
.
draw
(output
=
'text'
)
will yield a diagram like:
┌──────────┐┌──────────┐┌───┐┌──────────┐┌──────────────────┐┌─┐
(userqr0) q0
|
0
>
┤
U2
(
0
,pi)
├┤
U2
(
0
,pi)
├┤ X ├┤
U2
(
0
,pi)
├┤
U3
(pi,pi
/
2
,pi
/
2
)
├┤M├───
├──────────┤└──────────┘└─┬─┘├──────────┤└─┬─────────────┬──┘└╥┘┌─┐
(userqr1) q1
|
0
>
┤
U2
(
0
,pi)
├──────────────■──┤
U2
(
0
,pi)
├──┤
U3
(pi,
0
,pi)
├────╫─┤M├
└──────────┘                 └──────────┘  └─────────────┘    ║ └╥┘
(ancilla0) q2
|
0
>
──────────────────────────────────────────────────────────────╫──╫─
║  ║
(ancilla1) q3
|
0
>
──────────────────────────────────────────────────────────────╫──╫─
║  ║
(ancilla2) q4
|
0
>
──────────────────────────────────────────────────────────────╫──╫─
║  ║
(ancilla3) q5
|
0
>
──────────────────────────────────────────────────────────────╫──╫─
║  ║
(ancilla4) q6
|
0
>
──────────────────────────────────────────────────────────────╫──╫─
║  ║
(ancilla5) q7
|
0
>
──────────────────────────────────────────────────────────────╫──╫─
║  ║
(ancilla6) q8
|
0
>
──────────────────────────────────────────────────────────────╫──╫─
║  ║
(ancilla7) q9
|
0
>
──────────────────────────────────────────────────────────────╫──╫─
║  ║
(ancilla8) q10
|
0
>
──────────────────────────────────────────────────────────────╫──╫─
║  ║
(ancilla9) q11
|
0
>
──────────────────────────────────────────────────────────────╫──╫─
║  ║
(ancilla10) q12
|
0
>
──────────────────────────────────────────────────────────────╫──╫─
║  ║
(ancilla11) q13
|
0
>
──────────────────────────────────────────────────────────────╫──╫─
║  ║
c0_0
:
0
══════════════════════════════════════════════════════════════╩══╬═
║
c0_1
:
0
═════════════════════════════════════════════════════════════════╩═
If you do not want the layout to be shown on transpiled circuits (or any other circuits with a layout set) there is a new boolean kwarg for both functions,
with_layout
(which defaults
True
), which when set
False
will disable the layout annotation in the output circuits.
A new analysis pass
CountOpsLongest
was added to retrieve the number of operations on the longest path of the DAGCircuit. When used it will add a
count_ops_longest_path
key to the property set dictionary. You can add it to your a passmanager with something like:
from
qiskit
.
transpiler
.
passes
import
CountOpsLongestPath
from
qiskit
.
transpiler
.
passes
import
CxCancellation
from
qiskit
.
transpiler
import
PassManager
pm
=
PassManager
()
pm
.
append
(
CountOpsLongestPath
())
and then access the longest path via the property set value with something like:
pm
.
append
(
CxCancellation
(),
condition
=lambda
property_set
: property_set[
'count_ops_longest_path'
]
<
5
)
which will set a condition on that pass based on the longest path.
Two new functions,
sech()
and
sech_deriv()
were added to the pulse library module
qiskit.pulse.pulse_lib
for creating an unnormalized hyperbolic secant
SamplePulse
object and an unnormalized hyperbolic secant derviative
SamplePulse
object respectively.
A new kwarg option
vertical_compression
was added to the
QuantumCircuit.draw()
method and the
qiskit.visualization.circuit_drawer()
function. This option only works with the
text
backend. This option can be set to either
high
,
medium
(the default), or
low
to adjust how much vertical space is used by the output visualization.
A new kwarg boolean option
idle_wires
was added to the
QuantumCircuit.draw()
method and the
qiskit.visualization.circuit_drawer()
function. It works for all drawer backends. When
idle_wires
is set False in a drawer call the drawer will not draw any bits that do not have any circuit elements in the output quantum circuit visualization.
A new PassManager visualizer function
qiskit.visualization.pass_mamanger_drawer()
was added. This function takes in a PassManager object and will generate a flow control diagram of all the passes run in the PassManager.
When creating a PassManager you can now specify a callback function that if specified will be run after each pass is executed. This function gets passed a set of kwargs on each call with the state of the pass manager after each pass execution. Currently these kwargs are:
pass_
(
Pass
): the pass being run
dag
(
DAGCircuit
): the dag output of the pass
time
(
float
): the time to execute the pass
property_set
(
PropertySet
): the property set
count
(
int
): the index for the pass execution
However, it’s worth noting that while these arguments are set for the 0.9 release they expose the internals of the pass manager and are subject to change in future release.
For example you can use this to create a callback function that will visualize the circuit output after each pass is executed:
from
qiskit
.
transpiler
import
PassManager
def
my_callback
(
**
kwargs
):
print
(kwargs[
'dag'
])
pm
=
PassManager
(callback
=
my_callback)
Additionally you can specify the callback function when using
qiskit.compiler.transpile()
:
from
qiskit
.
compiler
import
transpile
def
my_callback
(
**
kwargs
):
print
(kwargs[
'pass'
])
transpile
(circ, callback
=
my_callback)
A new method
filter()
was added to the
qiskit.pulse.Schedule
class. This enables filtering the instructions in a schedule. For example, filtering by instruction type:
from
qiskit
.
pulse
import
Schedule
from
qiskit
.
pulse
.
commands
import
Acquire
from
qiskit
.
pulse
.
commands
import
AcquireInstruction
from
qiskit
.
pulse
.
commands
import
FrameChange
sched
=
Schedule
(name
=
'MyExperiment'
)
sched
.
insert
(
0
,
FrameChange
(phase
=-
1.57
)(device))
sched
.
insert
(
60
,
Acquire
(
5
))
acquire_sched
=
sched
.
filter
(instruction_types
=
[AcquireInstruction])
Additional decomposition methods for several types of gates. These methods will use different decomposition techniques to break down a gate into a sequence of CNOTs and single qubit gates. The following methods are added:
Method
Description
QuantumCircuit.iso()
Add an arbitrary isometry from m to n qubits to a circuit. This allows for attaching arbitrary unitaries on n qubits (m=n) or to prepare any state of n qubits (m=0)
QuantumCircuit.diag_gate()
Add a diagonal gate to the circuit
QuantumCircuit.squ()
Decompose an arbitrary 2x2 unitary into three rotation gates and add to a circuit
QuantumCircuit.ucg()
Attach an uniformly controlled gate (also called a multiplexed gate) to a circuit
QuantumCircuit.ucx()
Attach a uniformly controlled (also called multiplexed) Rx rotation gate to a circuit
QuantumCircuit.ucy()
Attach a uniformly controlled (also called multiplexed) Ry rotation gate to a circuit
QuantumCircuit.ucz()
Attach a uniformly controlled (also called multiplexed) Rz rotation gate to a circuit
Addition of Gray-Synth and Patel–Markov–Hayes algorithms for synthesis of CNOT-Phase and CNOT-only linear circuits. These functions allow the synthesis of circuits that consist of only CNOT gates given a linear function or a circuit that consists of only CNOT and phase gates given a matrix description.
A new function
random_circuit
was added to the
qiskit.circuit.random
module. This function will generate a random circuit of a specified size by randomly selecting different gates and adding them to the circuit. For example, you can use this to generate a 5-qubit circuit with a depth of 10 using:
from
qiskit
.
circuit
.
random
import
random_circuit
circ
=
random_circuit
(
5
,
10
)
A new kwarg
output_names
was added to the
qiskit.compiler.transpile()
function. This kwarg takes in a string or a list of strings and uses those as the value of the circuit name for the output circuits that get returned by the
transpile()
call. For example:
from
qiskit
.
compiler
import
transpile
my_circs
=
[circ_a
,
circ_b]
tcirc_a
,
tcirc_b
=
transpile
(my_circs,
output_names
=
[
'Circuit A'
,
'Circuit B'
])
the
name
attribute on tcirc_a and tcirc_b will be
'Circuit A'
and
'Circuit B'
respectively.
A new method
equiv()
was added to the
qiskit.quantum_info.Operator
and
qiskit.quantum_info.Statevector
classes. These methods are used to check whether a second
Operator
object or
Statevector
is equivalent up to global phase.
The user config file has several new options:
The
circuit_drawer
field now accepts an auto value. When set as the value for the
circuit_drawer
field the default drawer backend will be mpl if it is available, otherwise the text backend will be used.
A new field
circuit_mpl_style
can be used to set the default style used by the matplotlib circuit drawer. Valid values for this field are
bw
and
default
to set the default to a black and white or the default color style respectively.
A new field
transpile_optimization_level
can be used to set the default transpiler optimization level to use for calls to
qiskit.compiler.transpile()
. The value can be set to either 0, 1, 2, or 3.
Introduced a new pulse command
Delay
which may be inserted into a pulse
Schedule
. This command accepts a
duration
and may be added to any
Channel
. Other commands may not be scheduled on a channel during a delay.
The delay can be added just like any other pulse command. For example:
from
qiskit
import
pulse
drive_channel
=
pulse
.
DriveChannel
(
0
)
delay
=
pulse
.
Delay
(
20
)
sched
=
pulse
.
Schedule
()
sched
+=
delay
(drive_channel)
Upgrade Notes
The previously deprecated
qiskit._util
module has been removed.
qiskit.util
should be used instead.
The
QuantumCircuit.count_ops()
method now returns an
OrderedDict
object instead of a
dict
. This should be compatible for most use cases since
OrderedDict
is a
dict
subclass. However type checks and other class checks might need to be updated.
The
DAGCircuit.width()
method now returns the total number quantum bits and classical bits. Before it would only return the number of quantum bits. If you require just the number of quantum bits you can use
DAGCircuit.num_qubits()
instead.
The function
DAGCircuit.num_cbits()
has been removed. Instead you can use
DAGCircuit.num_clbits()
.
Individual quantum bits and classical bits are no longer represented as
(register, index)
tuples. They are now instances of Qubit and Clbit classes. If you’re dealing with individual bits make sure that you update any usage or type checks to look for these new classes instead of tuples.
The preset passmanager classes
qiskit.transpiler.preset_passmanagers.default_pass_manager
and
qiskit.transpiler.preset_passmanagers.default_pass_manager_simulator
(which were the previous default pass managers for
qiskit.compiler.transpile()
calls) have been removed. If you were manually using this pass managers switch to the new default,
qiskit.transpile.preset_passmanagers.level1_pass_manager
.
The
LegacySwap
pass has been removed. If you were using it in a custom pass manager, it’s usage can be replaced by the
StochasticSwap
pass, which is a faster more stable version. All the preset passmanagers have been updated to use
StochasticSwap
pass instead of the
LegacySwap
.
The following deprecated
qiskit.dagcircuit.DAGCircuit
methods have been removed:
DAGCircuit.get_qubits()
- Use
DAGCircuit.qubits()
instead
DAGCircuit.get_bits()
- Use
DAGCircuit.clbits()
instead
DAGCircuit.qasm()
- Use a combination of
qiskit.converters.dag_to_circuit()
and
QuantumCircuit.qasm()
. For example:
from
qiskit
.
dagcircuit
import
DAGCircuit
from
qiskit
.
converters
import
dag_to_circuit
my_dag
=
DAGCircuit
()
qasm
=
dag_to_circuit
(my_dag).
qasm
()
DAGCircuit.get_op_nodes()
- Use
DAGCircuit.op_nodes()
instead. Note that the return type is a list of
DAGNode
objects for
op_nodes()
instead of the list of tuples previously returned by
get_op_nodes()
.
DAGCircuit.get_gate_nodes()
- Use
DAGCircuit.gate_nodes()
instead. Note that the return type is a list of
DAGNode
objects for
gate_nodes()
instead of the list of tuples previously returned by
get_gate_nodes()
.
DAGCircuit.get_named_nodes()
- Use
DAGCircuit.named_nodes()
instead. Note that the return type is a list of
DAGNode
objects for
named_nodes()
instead of the list of node_ids previously returned by
get_named_nodes()
.
DAGCircuit.get_2q_nodes()
- Use
DAGCircuit.twoQ_gates()
instead. Note that the return type is a list of
DAGNode
objects for
twoQ_gates()
instead of the list of data_dicts previously returned by
get_2q_nodes()
.
DAGCircuit.get_3q_or_more_nodes()
- Use
DAGCircuit.threeQ_or_more_gates()
instead. Note that the return type is a list of
DAGNode
objects for
threeQ_or_more_gates()
instead of the list of tuples previously returned by
get_3q_or_more_nodes()
.
The following
qiskit.dagcircuit.DAGCircuit
methods had deprecated support for accepting a
node_id
as a parameter. This has been removed and now only
DAGNode
objects are accepted as input:
successors()
predecessors()
ancestors()
descendants()
bfs_successors()
quantum_successors()
remove_op_node()
remove_ancestors_of()
remove_descendants_of()
remove_nonancestors_of()
remove_nondescendants_of()
substitute_node_with_dag()
The
qiskit.dagcircuit.DAGCircuit
method
rename_register()
has been removed. This was unused by all the qiskit code. If you were relying on it externally you’ll have to re-implement is an external function.
The
qiskit.dagcircuit.DAGCircuit
property
multi_graph
has been removed. Direct access to the underlying
networkx
multi_graph
object isn’t supported anymore. The API provided by the
DAGCircuit
class should be used instead.
The deprecated exception class
qiskit.qiskiterror.QiskitError
has been removed. Instead you should use
qiskit.exceptions.QiskitError
.
The boolean kwargs,
ignore_requires
and
ignore_preserves
from the
qiskit.transpiler.PassManager
constructor have been removed. These are no longer valid options.
The module
qiskit.tools.logging
has been removed. This module was not used by anything and added nothing over the interfaces that Python’s standard library
logging
module provides. If you want to set a custom formatter for logging use the standard library
logging
module instead.
The
CompositeGate
class has been removed. Instead you should directly create a instruction object from a circuit and append that to your circuit. For example, you can run something like:
custom_gate_circ
=
qiskit
.
QuantumCircuit
(
2
)
custom_gate_circ
.
x
(
1
)
custom_gate_circ
.
h
(
0
)
custom_gate_circ
.
cx
(
0
,
1
)
custom_gate
=
custom_gate_circ
.
to_instruction
()
The previously deprecated kwargs,
seed
and
config
for
qiskit.compiler.assemble()
have been removed use
seed_simulator
and
run_config
respectively instead.
The previously deprecated converters
qiskit.converters.qobj_to_circuits()
and
qiskit.converters.circuits_to_qobj()
have been removed. Use
qiskit.assembler.disassemble()
and
qiskit.compiler.assemble()
respectively instead.
The previously deprecated kwarg
seed_mapper
for
qiskit.compiler.transpile()
has been removed. Instead you should use
seed_transpiler
The previously deprecated kwargs
seed
,
seed_mapper
,
config
, and
circuits
for the
qiskit.execute()
function have been removed. Use
seed_simulator
,
seed_transpiler
,
run_config
, and
experiments
arguments respectively instead.
The previously deprecated
qiskit.tools.qcvv
module has been removed use qiskit-ignis instead.
The previously deprecated functions
qiskit.transpiler.transpile()
and
qiskit.transpiler.transpile_dag()
have been removed. Instead you should use
qiskit.compiler.transpile
. If you were using
transpile_dag()
this can be replaced by running:
circ
=
qiskit
.
converters
.
dag_to_circuit
(dag)
out_circ
=
qiskit
.
compiler
.
transpile
(circ)
qiskit
.
converters
.
circuit_to_dag
(out_circ)
The previously deprecated function
qiskit.compile()
has been removed instead you should use
qiskit.compiler.transpile()
and
qiskit.compiler.assemble()
.
The jupyter cell magic
%%qiskit_progress_bar
from
qiskit.tools.jupyter
has been changed to a line magic. This was done to better reflect how the magic is used and how it works. If you were using the
%%qiskit_progress_bar
cell magic in an existing notebook, you will have to update this to be a line magic by changing it to be
%qiskit_progress_bar
instead. Everything else should behave identically.
The deprecated function
qiskit.tools.qi.qi.random_unitary_matrix()
has been removed. You should use the
qiskit.quantum_info.random.random_unitary()
function instead.
The deprecated function
qiskit.tools.qi.qi.random_density_matrix()
has been removed. You should use the
qiskit.quantum_info.random.random_density_matrix()
function instead.
The deprecated function
qiskit.tools.qi.qi.purity()
has been removed. You should the
qiskit.quantum_info.purity()
function instead.
The deprecated
QuantumCircuit._attach()
method has been removed. You should use
QuantumCircuit.append()
instead.
The
qiskit.qasm.Qasm
method
get_filename()
has been removed. You can use the
return_filename()
method instead.
The deprecated
qiskit.mapper
module has been removed. The list of functions and classes with their alternatives are:
qiskit.mapper.CouplingMap
:
qiskit.transpiler.CouplingMap
should be used instead.
qiskit.mapper.Layout
:
qiskit.transpiler.Layout
should be used instead
qiskit.mapper.compiling.euler_angles_1q()
:
qiskit.quantum_info.synthesis.euler_angles_1q()
should be used instead
qiskit.mapper.compiling.two_qubit_kak()
:
qiskit.quantum_info.synthesis.two_qubit_cnot_decompose()
should be used instead.
The deprecated exception classes
qiskit.mapper.exceptions.CouplingError
and
qiskit.mapper.exceptions.LayoutError
don’t have an alternative since they serve no purpose without a
qiskit.mapper
module.
The
qiskit.pulse.samplers
module has been moved to
qiskit.pulse.pulse_lib.samplers
. You will need to update imports of
qiskit.pulse.samplers
to
qiskit.pulse.pulse_lib.samplers
.
seaborn
is now a dependency for the function
qiskit.visualization.plot_state_qsphere()
. It is needed to generate proper angular color maps for the visualization. The
qiskit-terra[visualization]
extras install target has been updated to install
seaborn>=0.9.0
If you are using visualizations and specifically the
plot_state_qsphere()
function you can use that to install
seaborn
or just manually run
pip install seaborn>=0.9.0
The previously deprecated functions
qiksit.visualization.plot_state
and
qiskit.visualization.iplot_state
have been removed. Instead you should use the specific function for each plot type. You can refer to the following tables to map the deprecated functions to their equivalent new ones:
Qiskit Terra 0.6
Qiskit Terra 0.7+
plot_state(rho)
plot_state_city(rho)
plot_state(rho, method=’city’)
plot_state_city(rho)
plot_state(rho, method=’paulivec’)
plot_state_paulivec(rho)
plot_state(rho, method=’qsphere’)
plot_state_qsphere(rho)
plot_state(rho, method=’bloch’)
plot_bloch_multivector(rho)
plot_state(rho, method=’hinton’)
plot_state_hinton(rho)
The
pylatexenc
and
pillow
dependencies for the
latex
and
latex_source
circuit drawer backends are no longer listed as requirements. If you are going to use the latex circuit drawers ensure you have both packages installed or use the setuptools extras to install it along with qiskit-terra:
pip install qiskit
-
terra
[
visualization
]
The root of the
qiskit
namespace will now emit a warning on import if either
qiskit.IBMQ
or
qiskit.Aer
could not be setup. This will occur whenever anything in the
qiskit
namespace is imported. These warnings were added to make it clear for users up front if they’re running qiskit and the qiskit-aer and qiskit-ibmq-provider packages could not be found. It’s not always clear if the packages are missing or python packaging/pip installed an element incorrectly until you go to use them and get an empty
ImportError
. These warnings should make it clear up front if there these commonly used aliases are missing.
However, for users that choose not to use either qiskit-aer or qiskit-ibmq-provider this might cause additional noise. For these users these warnings are easily suppressable using Python’s standard library
warnings
. Users can suppress the warnings by putting these two lines before any imports from qiskit:
import
warnings
warnings
.
filterwarnings
(
'ignore'
, category
=
RuntimeWarning
,
module
=
'qiskit'
)
This will suppress the warnings emitted by not having qiskit-aer or qiskit-ibmq-provider installed, but still preserve any other warnings emitted by qiskit or any other package.
Deprecation Notes
The
U
and
CX
gates have been deprecated. If you’re using these gates in your code you should update them to use
u3
and
cx
instead. For example, if you’re using the circuit gate functions
circuit.u_base()
and
circuit.cx_base()
you should update these to be
circuit.u3()
and
circuit.cx()
respectively.
The
u0
gate has been deprecated in favor of using multiple
iden
gates and it will be removed in the future. If you’re using the
u0
gate in your circuit you should update your calls to use
iden
. For example, f you were using
circuit.u0(2)
in your circuit before that should be updated to be:
circuit
.
iden
()
circuit
.
iden
()
instead.
The
qiskit.pulse.DeviceSpecification
class is deprecated now. Instead you should use
qiskit.pulse.PulseChannelSpec
.
Accessing a
qiskit.circuit.Qubit
,
qiskit.circuit.Clbit
, or
qiskit.circuit.Bit
class by index is deprecated (for compatibility with the
(register, index)
tuples that these classes replaced). Instead you should use the
register
and
index
attributes.
Passing in a bit to the
qiskit.QuantumCircuit
method
append
as a tuple
(register, index)
is deprecated. Instead bit objects should be used directly.
Accessing the elements of a
qiskit.transpiler.Layout
object with a tuple
(register, index)
is deprecated. Instead a bit object should be used directly.
The
qiskit.transpiler.Layout
constructor method
qiskit.transpiler.Layout.from_tuplelist()
is deprecated. Instead the constructor
qiskit.transpiler.Layout.from_qubit_list()
should be used.
The module
qiskit.pulse.ops
has been deprecated. All the functions it provided:
union
flatten
shift
insert
append
have equivalent methods available directly on the
qiskit.pulse.Schedule
and
qiskit.pulse.Instruction
classes. Those methods should be used instead.
The
qiskit.qasm.Qasm
method
get_tokens()
is deprecated. Instead you should use the
generate_tokens()
method.
The
qiskit.qasm.qasmparser.QasmParser
method
get_tokens()
is deprecated. Instead you should use the
read_tokens()
method.
The
as_dict()
method for the Qobj class has been deprecated and will be removed in the future. You should replace calls to it with
to_dict()
instead.
Bug Fixes
The definition of the
CU3Gate
has been changed to be equivalent to the canonical definition of a controlled
U3Gate
.
The handling of layout in the pass manager has been standardized. This fixes several reported issues with handling layout. The
initial_layout
kwarg parameter on
qiskit.compiler.transpile()
and
qiskit.execute()
will now lay out your qubits from the circuit onto the desired qubits on the device when transpiling circuits.
Support for n-qubit unitaries was added to the BasicAer simulator and
unitary
(arbitrary unitary gates) was added to the set of basis gates for the simulators
The
qiskit.visualization.plost_state_qsphere()
has been updated to fix several issues with it. Now output Q Sphere visualization will be correctly generated and the following aspects have been updated:
All complementary basis states are antipodal
Phase is indicated by color of line and marker on sphere’s surface
Probability is indicated by translucency of line and volume of marker on
sphere’s surface
Other Notes
The default PassManager for
qiskit.compiler.transpile()
and
qiskit.execute()
has been changed to optimization level 1 pass manager defined at
qiskit.transpile.preset_passmanagers.level1_pass_manager
.
All the circuit drawer backends now will express gate parameters in a circuit as common fractions of pi in the output visualization. If the value of a parameter can be expressed as a fraction of pi that will be used instead of the numeric equivalent.
When using
qiskit.assembler.assemble_schedules()
if you do not provide the number of memory_slots to use the number will be inferred based on the number of acquisitions in the input schedules.
The deprecation warning on the
qiskit.dagcircuit.DAGCircuit
property
node_counter
has been removed. The behavior change being warned about was put into effect when the warning was added, so warning that it had changed served no purpose.
Calls to
PassManager.run()
now will emit python logging messages at the INFO level for each pass execution. These messages will include the Pass name and the total execution time of the pass. Python’s standard logging was used because it allows Qiskit-Terra’s logging to integrate in a standard way with other applications and libraries. All logging for the transpiler occurs under the
qiskit.transpiler
namespace, as used by
logging.getLogger('qiskit.transpiler
). For example, to turn on DEBUG level logging for the transpiler you can run:
import
logging
logging
.
basicConfig
()
logging
.
getLogger
(
'qiskit.transpiler'
).
setLevel
(logging.DEBUG)
which will set the log level for the transpiler to DEBUG and configure those messages to be printed to stderr.
Aer 0.3
There’s a new high-performance Density Matrix Simulator that can be used in conjunction with our noise models, to better simulate real world scenarios.
We have added a Matrix Product State (MPS) simulator. MPS allows for efficient simulation of several classes of quantum circuits, even under presence of strong correlations and highly entangled states. For cases amenable to MPS, circuits with several hundred qubits and more can be exactly simulated, e.g., for the purpose of obtaining expectation values of observables.
Snapshots can be performed in all of our simulators.
Now we can measure sampling circuits with read-out errors too, not only ideal circuits.
We have increased some circuit optimizations with noise presence.
A better 2-qubit error approximations have been included.
Included some tools for making certain noisy simulations easier to craft and faster to simulate.
Increased performance with simulations that require less floating point numerical precision.
Ignis 0.2
New Features
Logging Module
Purity RB
Interleaved RB
Repetition Code for Verification
Seed values can now be arbitrarily added to RB (not just in order)
Support for adding multiple results to measurement mitigation
RB Fitters now support providing guess values
Bug Fixes
Fixed a bug in RB fit error
Fixed a bug in the characterization fitter when selecting a qubit index to fit
Other Notes
Measurement mitigation now operates in parallel when applied to multiple results
Guess values for RB fitters are improved
Aqua 0.6
Added
Relative-Phase Toffoli gates
rccx
(with 2 controls) and
rcccx
(with 3 controls).
Variational form
RYCRX
A new
'basic-no-ancilla'
mode to
mct
.
Multi-controlled rotation gates
mcrx
,
mcry
, and
mcrz
as a general
u3
gate is not supported by graycode implementation
Chemistry: ROHF open-shell support
Supported for all drivers: Gaussian16, PyQuante, PySCF and PSI4
HartreeFock initial state, UCCSD variational form and two qubit reduction for parity mapping now support different alpha and beta particle numbers for open shell support
Chemistry: UHF open-shell support
Supported for all drivers: Gaussian16, PyQuante, PySCF and PSI4
QMolecule extended to include integrals, coefficients etc for separate beta
Chemistry: QMolecule extended with integrals in atomic orbital basis to facilitate common access to these for experimentation
Supported for all drivers: Gaussian16, PyQuante, PySCF and PSI4
Chemistry: Additional PyQuante and PySCF driver configuration
Convergence tolerance and max convergence iteration controls.
For PySCF initial guess choice
Chemistry: Processing output added to debug log from PyQuante and PySCF computations (Gaussian16 and PSI4 outputs were already added to debug log)
Chemistry: Merged qiskit-chemistry into qiskit-aqua
Add
MatrixOperator
,
WeightedPauliOperator
and
TPBGroupedPauliOperator
class.
Add
evolution_instruction
function to get registerless instruction of time evolution.
Add
op_converter
module to unify the place in charge of converting different types of operators.
Add
Z2Symmetries
class to encapsulate the Z2 symmetries info and has helper methods for tapering an Operator.
Amplitude Estimation: added maximum likelihood postprocessing and confidence interval computation.
Maximum Likelihood Amplitude Estimation (MLAE): Implemented new algorithm for amplitude estimation based on maximum likelihood estimation, which reduces number of required qubits and circuit depth.
Added (piecewise) linearly and polynomially controlled Pauli-rotation circuits.
Add
q_equation_of_motion
to study excited state of a molecule, and add two algorithms to prepare the reference state.
Changed
Improve
mct
’s
'basic'
mode by using relative-phase Toffoli gates to build intermediate results.
Adapt to Qiskit Terra’s newly introduced
Qubit
class.
Prevent
QPE/IQPE
from modifying input
Operator
objects.
The PyEDA dependency was removed; corresponding oracles’ underlying logic operations are now handled by SymPy.
Refactor the
Operator
class, each representation has its own class
MatrixOperator
,
WeightedPauliOperator
and
TPBGroupedPauliOperator
.
The
power
in
evolution_instruction
was applied on the theta on the CRZ gate directly, the new version repeats the circuits to implement power.
CircuitCache is OFF by default, and it can be set via environment variable now
QISKIT_AQUA_CIRCUIT_CACHE
.
Bug Fixes
A bug where
TruthTableOracle
would build incorrect circuits for truth tables with only a single
1
value.
A bug caused by
PyEDA
’s indeterminism.
A bug with
QPE/IQPE
’s translation and stretch computation.
Chemistry: Bravyi-Kitaev mapping fixed when num qubits was not a power of 2
Setup
initial_layout
in
QuantumInstance
via a list.
Removed
General multi-controlled rotation gate
mcu3
is removed and replaced by multi-controlled rotation gates
mcrx
,
mcry
, and
mcrz
Deprecated
The
Operator
class is deprecated, in favor of using
MatrixOperator
,
WeightedPauliOperator
and
TPBGroupedPauliOperator
.
IBM Q Provider 0.3
No change