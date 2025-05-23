Qiskit 0.25 release notes
0.25.4
Terra 0.17.2
Prelude
This is a bugfix release that fixes several issues from the 0.17.1 release. Most importantly this release fixes compatibility for the
QuantumInstance
class when running on backends that are based on the
BackendV1
abstract class. This fixes all the algorithms and applications built on
qiskit.algorithms
or
qiskit.opflow
when running on newer backends.
Bug Fixes
Fixed an issue with the
BasisTranslator
transpiler pass which in some cases would translate gates already in the target basis. This would potentially result in both longer execution time and less optimal results. Fixed
#6085
Fixed an issue in the
SPSA
when the optimizer was initialized with a callback function via the
callback
kwarg would potentially cause an error to be raised.
Fixed an issue in the
qiskit.quantum_info.Statevector.expectation_value()
and
qiskit.quantum_info.DensityMatrix.expectation_value`methods where the ``qargs`()
kwarg was ignored if the operator was a
Pauli
or
SparsePauliOp
operator object. Fixed
#6303
Fixed an issue in the
qiskit.quantum_info.Pauli.evolve()
method which could have resulted in the incorrect Pauli being returned when evolving by a
CZGate
,
CYGate
, or a
SwapGate
gate.
Fixed an issue in the
qiskit.opflow.SparseVectorStateFn.to_dict_fn()
method, which previously had at most one entry for the all zero state due to an index error.
Fixed an issue in the
qiskit.opflow.SparseVectorStateFn.equals()
method so that is properly returning
True
or
False
instead of a sparse vector comparison of the single elements.
Fixes an issue in the
Statevector
and
DensityMatrix
probability methods
qiskit.quantum_info.Statevector.probabilities()
,
qiskit.quantum_info.Statevector.probabilities_dict()
,
qiskit.quantum_info.DensityMatrix.probabilities()
,
qiskit.quantum_info.DensityMatrix.probabilities_dict()
where the returned probabilities could have incorrect ordering for certain values of the
qargs
kwarg. Fixed
#6320
Fixed an issue where the
TaperedPauliSumOp
class did not support the multiplication with
ParameterExpression
object and also did not have a necessary
assign_parameters()
method for working with
ParameterExpression
objects. Fixed
#6127
Fixed compatibility for the
QuantumInstance
class when running on backends that are based on the
BackendV1
abstract class. Fixed
#6280
Aer 0.8.2
No change
Ignis 0.6.0
No change
Aqua 0.9.1
No change
IBM Q Provider 0.12.3
No change
0.25.3
Terra 0.17.1
No change
Aer 0.8.2
Known Issues
The
SaveExpectationValue
and
SaveExpectationValueVariance
have been disabled for the extended_stabilizer method of the
QasmSimulator
and
AerSimulator
due to returning the incorrect value for certain Pauli operator components. Refer to #1227 <
https://github.com/Qiskit/qiskit-aer/issues/1227
> for more information and examples.
Bug Fixes
Fixes performance issue with how the
basis_gates
configuration attribute was set. Previously there were unintended side-effects to the backend class which could cause repeated simulation runtime to incrementally increase. Refer to #1229 <
https://github.com/Qiskit/qiskit-aer/issues/1229
> for more information and examples.
Fixes a bug with the
"multiplexer"
simulator instruction where the order of target and control qubits was reversed to the order in the Qiskit instruction.
Fixes a bug introduced in 0.8.0 where GPU simulations would allocate unneeded host memory in addition to the GPU memory.
Fixes a bug in the
stabilizer
simulator method of the
QasmSimulator
and
AerSimulator
where the expectation value for the
save_expectation_value
and
snapshot_expectation_value
could have the wrong sign for certain
Y
Pauli’s.
Ignis 0.6.0
No change
Aqua 0.9.1
No change
IBM Q Provider 0.12.3
No change
0.25.2
Terra 0.17.1
No change
Aer 0.8.1
No change
Ignis 0.6.0
No change
Aqua 0.9.1
No change
IBM Q Provider 0.12.3
Other Notes
The
qiskit.providers.ibmq.experiment.analysis_result.AnalysisResult
fit
attribute is now optional.
0.25.1
Terra 0.17.1
Prelude
This is a bugfix release that fixes several issues from the 0.17.0 release. Most importantly this release fixes the incorrectly constructed sdist package for the 0.17.0 release which was not actually buildable and was blocking installation on platforms without precompiled binaries available.
Bug Fixes
Fixed an issue where the
global_phase
attribute would not be preserved in the output
QuantumCircuit
object when the
qiskit.circuit.QuantumCircuit.reverse_bits()
method was called. For example:
import
math
from
qiskit
import
QuantumCircuit
qc
=
QuantumCircuit
(
3
,
2
, global_phase
=
math.pi)
qc
.
h
(
0
)
qc
.
s
(
1
)
qc
.
cx
(
0
,
1
)
qc
.
measure
(
0
,
1
)
qc
.
x
(
0
)
qc
.
y
(
1
)
reversed
=
qc
.
reverse_bits
()
print
(
reversed
.global_phase)
will now correctly print
π
\pi
π
.
Fixed an issue where the transpiler pass
Unroller
didn’t preserve global phase in case of nested instructions with one rule in their definition. Fixed
#6134
Fixed an issue where the
parameter
attribute of a
ControlledGate
object built from a
UnitaryGate
was not being set to the unitary matrix of the
UnitaryGate
object. Previously,
control()
was building a
ControlledGate
with the
parameter
attribute set to the controlled version of
UnitaryGate
matrix. This would lead to a modification of the
parameter
of the base
UnitaryGate
object and subsequent calls to
inverse()
was creating the inverse of a double-controlled
UnitaryGate
. Fixed
#5750
Fixed an issue with the preset pass managers
level_0_pass_manager
and
level_1_pass_manager
(which corresponds to
optimization_level
0 and 1 for
transpile()
) where in some cases they would produce circuits not in the requested basis.
Fix a bug where using
SPSA
with automatic calibration of the learning rate and perturbation (i.e.
learning_rate
and
perturbation
are
None
in the initializer), stores the calibration for all future optimizations. Instead, the calibration should be done for each new objective function.
Aer 0.8.1
Bug Fixes
Fixed an issue with use of the
matrix_product_state
method of the
AerSimulator
and
QasmSimulator
simulators when running a noisy simulation with Kraus errors. Previously, the matrix product state simulation method would not propogate changes to neighboring qubits after applying the Kraus matrix. This has been fixed so the output from the simulation is correct. Fixed
#1184
and
#1205
Fixed an issue where the
qiskit.extensions.Initialize
instruction would disable measurement sampling optimization for the
statevector
and
matrix_product_state
simulation methods of the
AerSimulator
and
QasmSimulator
simulators, even when it was the first circuit instruction or applied to all qubits and hence deterministic. Fixed
#1210
Fix an issue with the
SaveStatevector
and
SnapshotStatevector
instructions when used with the
extended_stabilizer
simulation method of the
AerSimulator
and
QasmSimulator
simulators where it would return an unnormalized statevector. Fixed
#1196
The
matrix_product_state
simulation method now has support for it’s previously missing set state instruction,
qiskit.providers.aer.library.SetMatrixProductState
, which enables setting the state of a simulation in a circuit.
Ignis 0.6.0
No change
Aqua 0.9.1
IBM Q Provider 0.12.2
No change
0.25.0
This release officially deprecates the Qiskit Aqua project. Accordingly, in a future release the
qiskit-aqua
package will be removed from the Qiskit metapackage, which means in that future release
pip install qiskit
will no longer include
qiskit-aqua
. The application modules that are provided by qiskit-aqua have been split into several new packages:
qiskit-optimization
,
qiskit-nature
,
qiskit-machine-learning
, and
qiskit-finance
. These packages can be installed by themselves (via the standard pip install command, e.g.
pip install qiskit-nature
) or with the rest of the Qiskit metapackage as optional extras (e.g.
pip install 'qiskit[finance,optimization]'
or
pip install 'qiskit[all]'
The core algorithms and the operator flow now exist as part of qiskit-terra at
qiskit.algorithms
and
qiskit.opflow
. Depending on your existing usage of Aqua you should either use the application packages or the new modules in Qiskit Terra. For more details on how to migrate from Qiskit Aqua, you can refer to the
migration guide
.
Terra 0.17.0
Prelude
The Qiskit Terra 0.17.0 includes many new features and bug fixes. The major new feature for this release is the introduction of the
qiskit.algorithms
and
qiskit.opflow
modules which were migrated and adapted from the
qiskit.aqua
project.
New Features
The
qiskit.pulse.call()
function can now take a
Parameter
object along with a parameterized subroutine. This enables assigning different values to the
Parameter
objects for each subroutine call.
For example,
from
qiskit
.
circuit
import
Parameter
from
qiskit
import
pulse
amp
=
Parameter
(
'amp'
)
with
pulse
.
build
()
as
subroutine
:
pulse
.
play
(pulse.
Gaussian
(
160
, amp,
40
),
DriveChannel
(
0
))
with
pulse
.
build
()
as
main_prog
:
pulse
.
call
(subroutine, amp
=
0.1
)
pulse
.
call
(subroutine, amp
=
0.3
)
The
qiskit.providers.models.QasmBackendConfiguration
has a new field
processor_type
which can optionally be used to provide information about a backend’s processor in the form:
{"family": <str>, "revision": <str>, segment: <str>}
. For example:
{"family": "Canary", "revision": "1.0", segment: "A"}
.
The
qiskit.pulse.Schedule
,
qiskit.pulse.Instruction
, and
qiskit.pulse.Channel
classes now have a
parameter
property which will return any
Parameter
objects used in the object and a
is_parameterized()
method which will return
True
if any parameters are used in the object.
For example:
from
qiskit
.
circuit
import
Parameter
from
qiskit
import
pulse
shift
=
Parameter
(
'alpha'
)
schedule
=
pulse
.
Schedule
()
schedule
+=
pulse
.
SetFrequency
(shift, pulse.
DriveChannel
(
0
))
assert
schedule
.
is_parameterized
()
==
True
print
(schedule.parameters)
Added a
PiecewiseChebyshev
to the
qiskit.circuit.library
for implementing a piecewise Chebyshev approximation of an input function. For a given function
f
(
x
)
f(x)
f
(
x
)
and degree
d
d
d
, this class class implements a piecewise polynomial Chebyshev approximation on
n
n
n
qubits to
f
(
x
)
f(x)
f
(
x
)
on the given intervals. All the polynomials in the approximation are of degree
d
d
d
.
For example:
import
numpy
as
np
from
qiskit
import
QuantumCircuit
from
qiskit
.
circuit
.
library
.
arithmetic
.
piecewise_chebyshev
import
PiecewiseChebyshev
f_x
,
degree
,
breakpoints
,
num_state_qubits
=
lambda
x
: np
.
arcsin
(
1
/
x),
2
,
[
2
,
4
]
,
2
pw_approximation
=
PiecewiseChebyshev
(f_x, degree, breakpoints, num_state_qubits)
pw_approximation
.
_build
()
qc
=
QuantumCircuit
(pw_approximation.num_qubits)
qc
.
h
(
list
(
range
(num_state_qubits)))
qc
.
append
(pw_approximation.
to_instruction
(), qc.qubits)
qc
.
draw
(output
=
'mpl'
)
The
BackendProperties
class now has a
readout_length()
method, which returns the readout length [sec] of the given qubit.
A new class,
ScheduleBlock
, has been added to the
qiskit.pulse
module. This class provides a new representation of a pulse program. This representation is best suited for the pulse builder syntax and is based on relative instruction ordering.
This representation takes
alignment_context
instead of specifying starting time
t0
for each instruction. The start time of instruction is implicitly allocated with the specified transformation and relative position of instructions.
The
ScheduleBlock
allows for lazy instruction scheduling, meaning we can assign arbitrary parameters to the duration of instructions.
For example:
from
qiskit
.
pulse
import
ScheduleBlock
,
DriveChannel
,
Gaussian
from
qiskit
.
pulse
.
instructions
import
Play
,
Call
from
qiskit
.
pulse
.
transforms
import
AlignRight
from
qiskit
.
circuit
import
Parameter
dur
=
Parameter
(
'rabi_duration'
)
block
=
ScheduleBlock
(alignment_context
=
AlignRight
())
block
+=
Play
(
Gaussian
(dur,
0.1
, dur
/
4
),
DriveChannel
(
0
))
block
+=
Call
(measure_sched)
# subroutine defined elsewhere
this code defines an experiment scanning a Gaussian pulse’s duration followed by a measurement
measure_sched
, i.e. a Rabi experiment. You can reuse the
block
object for every scanned duration by assigning a target duration value.
Added a new function
array_to_latex()
to the
qiskit.visualization
module that can be used to represent and visualize vectors and matrices with LaTeX.
from
qiskit
.
visualization
import
array_to_latex
from
numpy
import
sqrt
,
exp
,
pi
mat
=
[[
0
,
exp
(pi
*
.75
j
)
]
,
[
1
/
sqrt
(
8
),
0.875
]]
array_to_latex
(mat)
The
Statevector
and
DensityMatrix
classes now have
draw()
methods which allow objects to be drawn as either text matrices, IPython Latex objects, Latex source, Q-spheres, Bloch spheres and Hinton plots. By default the output type is the equivalent output from
__repr__
but this default can be changed in a user config file by setting the
state_drawer
option. For example:
from
qiskit
.
quantum_info
import
DensityMatrix
dm
=
DensityMatrix
.
from_label
(
'r0'
)
dm
.
draw
(
'latex'
)
from
qiskit
.
quantum_info
import
Statevector
sv
=
Statevector
.
from_label
(
'+r'
)
sv
.
draw
(
'qsphere'
)
Additionally, the
draw()
method is now used for the ipython display of these classes, so if you change the default output type in a user config file then when a
Statevector
or a
DensityMatrix
object are displayed in a jupyter notebook that output type will be used for the object.
Pulse
qiskit.pulse.Instruction
objects and parametric pulse objects (eg
Gaussian
now support using
Parameter
and
ParameterExpression
objects for the
duration
parameter. For example:
from
qiskit
.
circuit
import
Parameter
from
qiskit
.
pulse
import
Gaussian
dur
=
Parameter
(
'x_pulse_duration'
)
double_dur
=
dur
*
2
rx_pulse
=
Gaussian
(dur,
0.1
, dur
/
4
)
double_rx_pulse
=
Gaussian
(double_dir,
0.1
, dur
/
4
)
Note that while we can create an instruction with a parameterized
duration
adding an instruction with unbound parameter
duration
to a schedule is supported only by the newly introduced representation
ScheduleBlock
. See the known issues release notes section for more details.
The
run()
method for the
QasmSimulatorPy
,
StatevectorSimulatorPy
, and
UnitarySimulatorPy
backends now takes a
QuantumCircuit
(or a list of
QuantumCircuit
objects) as its input. The previous
QasmQobj
object is still supported for now, but will be deprecated in a future release.
For an example of how to use this see:
from
qiskit
import
transpile
,
QuantumCircuit
from
qiskit
.
providers
.
basicaer
import
BasicAer
backend
=
BasicAer
.
get_backend
(
'qasm_simulator'
)
circuit
=
QuantumCircuit
(
2
)
circuit
.
h
(
0
)
circuit
.
cx
(
0
,
1
)
circuit
.
measure_all
()
tqc
=
transpile
(circuit, backend)
result
=
backend
.
run
(tqc, shots
=
4096
).
result
()
The
CommutativeCancellation
transpiler pass has a new optional kwarg on the constructor
basis_gates
, which takes the a list of the names of basis gates for the target backend. When specified the pass will only use gates in the
basis_gates
kwarg. Previously, the pass would automatically replace consecutive gates which commute with
ZGate
with the
U1Gate
unconditionally. The
basis_gates
kwarg enables you to specify which z-rotation gates are present in the target basis to avoid this.
The constructors of the
Bit
class and subclasses,
Qubit
,
Clbit
, and
AncillaQubit
, have been updated such that their two parameters,
register
and
index
are now optional. This enables the creation of bit objects that are independent of a register.
A new class,
BooleanExpression
, has been added to the
qiskit.circuit.classicalfunction
module. This class allows for creating an oracle from a Python boolean expression. For example:
from
qiskit
.
circuit
import
BooleanExpression
,
QuantumCircuit
expression
=
BooleanExpression
(
'~x & (y | z)'
)
circuit
=
QuantumCircuit
(
4
)
circuit
.
append
(expression, [
0
,
1
,
2
,
3
])
circuit
.
draw
(
'mpl'
)
circuit
.
decompose
().
draw
(
'mpl'
)
The
BooleanExpression
also includes a method,
from_dimacs_file()
, which allows loading formulas described in the
DIMACS-CNF
format. For example:
from
qiskit
.
circuit
import
BooleanExpression
,
QuantumCircuit
boolean_exp
=
BooleanExpression
.
from_dimacs_file
(
"simple_v3_c2.cnf"
)
circuit
=
QuantumCircuit
(boolean_exp.num_qubits)
circuit
.
append
(boolean_exp,
range
(boolean_exp.num_qubits))
circuit
.
draw
(
'text'
)
┌───────────────────┐
q_0
:
┤
0
├
│                   │
q_1
:
┤
1
├
│  SIMPLE_V3_C2
.
CNF │
q_2
:
┤
2
├
│                   │
q_3
:
┤
3
├
└───────────────────┘
circuit
.
decompose
().
draw
(
'text'
)
q_0
:
──o────o────────────
│    │
q_1
:
──■────o────■───────
│    │    │
q_2
:
──■────┼────o────■──
┌─┴─┐┌─┴─┐┌─┴─┐┌─┴─┐
q_3
:
┤ X ├┤ X ├┤ X ├┤ X ├
└───┘└───┘└───┘└───┘
Added a new class,
PhaseOracle
, has been added to the
qiskit.circuit.library
module. This class enables the construction of phase oracle circuits from Python boolean expressions.
from
qiskit
.
circuit
.
library
.
phase_oracle
import
PhaseOracle
oracle
=
PhaseOracle
(
'x1 & x2 & (not x3)'
)
oracle
.
draw
(
'mpl'
)
These phase oracles can be used as part of a larger algorithm, for example with
qiskit.algorithms.AmplificationProblem
:
from
qiskit
.
algorithms
import
AmplificationProblem
,
Grover
from
qiskit
import
BasicAer
backend
=
BasicAer
.
get_backend
(
'qasm_simulator'
)
problem
=
AmplificationProblem
(oracle, is_good_state
=
oracle.evaluate_bitstring)
grover
=
Grover
(quantum_instance
=
backend)
result
=
grover
.
amplify
(problem)
result
.
top_measurement
The
PhaseOracle
class also includes a
from_dimacs_file()
method which enables constructing a phase oracle from a file describing a formula in the
DIMACS-CNF
format.
from
qiskit
.
circuit
.
library
.
phase_oracle
import
PhaseOracle
oracle
=
PhaseOracle
.
from_dimacs_file
(
"simple_v3_c2.cnf"
)
oracle
.
draw
(
'text'
)
state_0
:
─o───────o──────────────
│ ┌───┐ │ ┌───┐
state_1
:
─■─┤ X ├─■─┤ X ├─■──────
│ └───┘   └───┘ │ ┌───┐
state_2
:
─■───────────────o─┤ Z ├
└───┘
All transpiler passes (ie any instances of
BasePass
) are now directly callable. Calling a pass provides a convenient interface for running the pass on a
QuantumCircuit
object.
For example, running a single transformation pass, such as
BasisTranslator
, can be done with:
from
qiskit
import
QuantumCircuit
from
qiskit
.
transpiler
.
passes
import
BasisTranslator
from
qiskit
.
circuit
.
equivalence_library
import
SessionEquivalenceLibrary
as
sel
circuit
=
QuantumCircuit
(
1
)
circuit
.
h
(
0
)
pass_instance
=
BasisTranslator
(sel, [
'rx'
,
'rz'
,
'cx'
])
result
=
pass_instance
(circuit)
result
.
draw
(output
=
'mpl'
)
When running an analysis pass, a property set (as
dict
or as
PropertySet
) needs to be added as a parameter and it might be modified “in-place”. For example:
from
qiskit
import
QuantumCircuit
from
qiskit
.
transpiler
.
passes
import
Depth
circuit
=
QuantumCircuit
(
1
)
circuit
.
h
(
0
)
property_set
=
{}
pass_instance
=
Depth
()
pass_instance
(circuit, property_set)
print
(property_set)
The
QasmQobjConfig
class now has an optional kwarg for
meas_level
and
meas_return
. These fields can be used to enable generating
QasmQobj
job payloads that support
meas_level=1
(kerneled data) for circuit jobs (previously this was only exposed for
PulseQobj
objects). The
assemble()
function has been updated to set this field for
QasmQobj
objects it generates.
A new
tensor()
method has been added to the
QuantumCircuit
class. This method enables tensoring another circuit with an existing circuit. This method works analogously to
qiskit.quantum_info.Operator.tensor()
and is consistent with the little-endian convention of Qiskit.
For example:
from
qiskit
import
QuantumCircuit
top
=
QuantumCircuit
(
1
)
top
.
x
(
0
)
;
bottom
=
QuantumCircuit
(
2
)
bottom
.
cry
(
0.2
,
0
,
1
)
;
bottom
.
tensor
(top).
draw
(output
=
'mpl'
)
The
qiskit.circuit.QuantumCircuit
class now supports arbitrary free form metadata with the
metadata
attribute. A user (or program built on top of
QuantumCircuit
) can attach metadata to a circuit for use in tracking the circuit. For example:
from
qiskit
.
circuit
import
QuantumCircuit
qc
=
QuantumCircuit
(
2
, user_metadata_field_1
=
'my_metadata'
,
user_metadata_field_2
=
'my_other_value'
)
or:
from
qiskit
.
circuit
import
QuantumCircuit
qc
=
QuantumCircuit
(
2
)
qc
.
metadata
=
{
'user_metadata_field_1'
:
'my_metadata'
,
'user_metadata_field_2'
:
'my_other_value'
}
This metadata will
not
be used for influencing the execution of the circuit but is just used for tracking the circuit for the lifetime of the object. The
metadata
attribute will persist between any circuit transforms including
transpile()
and
assemble()
. The expectation is for providers to associate the metadata in the result it returns, so that users can filter results based on circuit metadata the same way they can currently do with
QuantumCircuit.name
.
Add a new operator class
CNOTDihedral
has been added to the
qiskit.quantum_info
module. This class is used to represent the CNOT-Dihedral group, which is generated by the quantum gates
CXGate
,
TGate
, and
XGate
.
Adds a
&
(
__and__
) binary operator to
BaseOperator
subclasses (eg
qiskit.quantum_info.Operator
) in the
qiskit.quantum_info
module. This is shorthand to call the classes
compose()
method (ie
A & B == A.compose(B)
).
For example:
import
qiskit
.
quantum_info
as
qi
qi
.
Pauli
(
'X'
)
&
qi
.
Pauli
(
'Y'
)
Adds a
&
(
__and__
) binary operator to
qiskit.quantum_info.Statevector
and
qiskit.quantum_info.DensityMatrix
classes. This is shorthand to call the classes
evolve()
method (ie
psi & U == psi.evolve(U)
).
For example:
import
qiskit
.
quantum_info
as
qi
qi
.
Statevector
.
from_label
(
'0'
)
&
qi
.
Pauli
(
'X'
)
A new a new 2-qubit gate,
ECRGate
, the echo cross-resonance (ECR), has been added to the
qiskit.circuit.library
module along with a corresponding method,
ecr()
for the
QuantumCircuit
class. The ECR gate is two
C
R
(
π
4
)
CR(\frac{π}{4})
CR
(
4
π
​
)
pulses with an
XGate
between them for the echo. This gate is locally equivalent to a
CXGate
(can convert to a CNOT with local pre- or post-rotation). It is the native gate on current IBM hardware and compiling to it allows the pre-/post-rotations to be merged into the rest of the circuit.
A new kwarg
approximation_degree
has been added to the
transpile()
function for enabling approximate compilation. Valid values range from 0 to 1, and higher means less approximation. This is a heuristic dial to experiment with circuit approximations. The concrete interpretation of this number is left to each pass, which may use it to perform some approximate version of the pass. Specific examples include the
UnitarySynthesis
pass or the or translators to discrete gate sets. If a pass does not support this option, it implies exact transformation.
Two new transpiler passess,
GateDirection
and
qiskit.transpiler.passes.CheckGateDirection
, were added to the
qiskit.transpiler.passes
module. These new passes are inteded to be more general replacements for
CXDirection
and
CheckCXDirection
(which are both now deprecated, see the deprecation notes for more details) that perform the same function but work with other gates beside just
CXGate
.
When running on Windows, parallel execution with the
parallel_map()
function can now be enabled (it is still disabled by default). To do this you can either set
parallel = True
in a user config file, or set the
QISKIT_PARALLEL
environment variable to
TRUE
(this will also effect
transpile()
and
assemble()
which both use
parallel_map()
internally). It is important to note that when enabling parallelism on Windows there are limitations around how Python launches processes for Windows, see the Known Issues section below for more details on the limitations with parallel execution on Windows.
A new function,
hellinger_distance()
, for computing the Hellinger distance between two counts distributions has been added to the
qiskit.quantum_info
module.
The
decompose_clifford()
function in the
qiskit.quantum_info
module (which gets used internally by the
qiskit.quantum_info.Clifford.to_circuit()
method) has a new kwarg
method
which enables selecting the synthesis method used by either setting it to
'AG'
or
'greedy'
. By default for more than three qubits it is set to
'greedy'
which uses a non-optimal greedy compilation routine for Clifford elements synthesis, by Bravyi et. al., which typically yields better CX cost compared to the previously used Aaronson-Gottesman method (for more than two qubits). You can use the
method
kwarg to revert to the previous default Aaronson-Gottesman method by setting
method='AG'
.
The
Initialize
class in the
qiskit.extensions
module can now be constructed using an integer. The ‘1’ bits of the integer will insert a
Reset
and an
XGate
into the circuit for the corresponding qubit. This will be done using the standard little-endian convention is qiskit, ie the rightmost bit of the integer will set qubit 0. For example, setting the parameter in
Initialize
equal to
5
will set qubits 0 and 2 to value 1.
from
qiskit
.
extensions
import
Initialize
initialize
=
Initialize
(
13
)
initialize
.
definition
.
draw
(
'mpl'
)
The
Initialize
class in the
qiskit.extensions
module now supports constructing directly from a Pauli label (analogous to the
qiskit.quantum_info.Statevector.from_label()
method). The Pauli label refer to basis states of the Pauli eigenstates Z, X, Y. These labels use Qiskit’s standard little-endian notation, for example a label of
'01'
would initialize qubit 0 to
∣
1
⟩
|1\rangle
∣1
⟩
and qubit 1 to
∣
0
⟩
|0\rangle
∣0
⟩
.
from
qiskit
.
extensions
import
Initialize
initialize
=
Initialize
(
"10+-lr"
)
initialize
.
definition
.
draw
(
'mpl'
)
The kwarg,
template_list
, for the constructor of the
qiskit.transpiler.passes.TemplateOptimization
transpiler pass now supports taking in a list of both
QuantumCircuit
and
DAGDependency
objects. Previously, only
QuantumCircuit
were accepted (which were internally converted to
DAGDependency
objects) in the input list.
A new transpiler pass,
qiskit.transpiler.passes.RZXCalibrationBuilder
, capable of generating calibrations and adding them to a quantum circuit has been introduced. This pass takes calibrated
CXGate
objects and creates the calibrations for
qiskit.circuit.library.RZXGate
objects with an arbitrary rotation angle. The schedules are created by stretching and compressing the
GaussianSquare
pulses of the echoed-cross resonance gates.
New template circuits for using
qiskit.circuit.library.RZXGate
are added to the
qiskit.circuit.library
module (eg
rzx_yz
). This enables pairing the
TemplateOptimization
pass with the
qiskit.transpiler.passes.RZXCalibrationBuilder
pass to automatically find and replace gate sequences, such as
CNOT - P(theta) - CNOT
, with more efficent circuits based on
qiskit.circuit.library.RZXGate
with a calibration.
The matplotlib output type for the
circuit_drawer()
and the
draw()
method for the
QuantumCircuit
class now supports configuration files for setting the visualization style. In previous releases, there was basic functionality that allowed users to pass in a
style
kwarg that took in a
dict
to customize the colors and other display features of the
mpl
drawer. This has now been expanded so that these dictionaries can be loaded from JSON files directly without needing to pass a dictionary. This enables users to create new style files and use that style for visualizations by passing the style filename as a string to the
style
kwarg.
To leverage this feature you must set the
circuit_mpl_style_path
option in a user config file. This option should be set to the path you want qiskit to search for style JSON files. If specifying multiple path entries they should be separated by
:
. For example, setting
circuit_mpl_style_path = ~/.qiskit:~/user_styles
in a user config file will look for JSON files in both
~/.qiskit
and
~/user_styles
.
A new kwarg,
format_marginal
has been added to the function
marginal_counts()
which when set to
True
formats the counts output according to the
cregs
in the circuit and missing indices are represented with a
_
. For example:
from
qiskit
import
QuantumCircuit
,
execute
,
BasicAer
,
result
from
qiskit
.
result
.
utils
import
marginal_counts
qc
=
QuantumCircuit
(
5
,
5
)
qc
.
x
(
0
)
qc
.
measure
(
0
,
0
)
result
=
execute
(qc, BasicAer.
get_backend
(
'qasm_simulator'
)).
result
()
print
(
marginal_counts
(result.
get_counts
(), [
0
,
2
,
4
], format_marginal
=
True
))
Improved the performance of
qiskit.quantum_info.Statevector.expectation_value()
and
qiskit.quantum_info.DensityMatrix.expectation_value()
when the argument operator is a
Pauli
or
SparsePauliOp
operator.
The user config file has 2 new configuration options,
num_processes
and
parallel
, which are used to control the default behavior of
parallel_map()
. The
parallel
option is a boolean that is used to dictate whether
parallel_map()
will run in multiple processes or not. If it set to
False
calls to
parallel_map()
will be executed serially, while setting it to
True
will enable parallel execution. The
num_processes
option takes an integer which sets how many CPUs to use when executing in parallel. By default it will use the number of CPU cores on a system.
There are 2 new environment variables,
QISKIT_PARALLEL
and
QISKIT_NUM_PROCS
, that can be used to control the default behavior of
parallel_map()
. The
QISKIT_PARALLEL
option can be set to the
TRUE
(any capitalization) to set the default to run in multiple processes when
parallel_map()
is called. If it is set to any other value
parallel_map()
will be executed serially.
QISKIT_NUM_PROCS
takes an integer (for example
QISKIT_NUM_PROCS=5
) which will be used as the default number of processes to run with. Both of these will take precedence over the equivalent option set in the user config file.
A new method,
gradient()
, has been added to the
ParameterExpression
class. This method is used to evaluate the gradient of a
ParameterExpression
object.
The
__eq__
method (ie what is called when the
==
operator is used) for the
ParameterExpression
now allows for the comparison with a numeric value. Previously, it was only possible to compare two instances of
ParameterExpression
with
==
. For example:
from
qiskit
.
circuit
import
Parameter
x
=
Parameter
(
"x"
)
y
=
x
+
2
y
=
y
.
assign
(x,
-
1
)
assert
y
==
1
The
PauliFeatureMap
class in the
qiskit.circuit.library
module now supports adjusting the rotational factor,
α
\alpha
α
, by either setting using the kwarg
alpha
on the constructor or setting the
alpha
attribute after creation. Previously this value was fixed at
2.0
. Adjusting this attribute allows for better control of decision boundaries and provides additional flexibility handling the input features without needing to explicitly scale them in the data set.
A new
Gate
class,
PauliGate
, has been added the
qiskit.circuit.library
module and corresponding method,
pauli()
, was added to the
QuantumCircuit
class. This new gate class enables applying several individual pauli gates to different qubits at the simultaneously. This is primarily useful for simulators which can use this new gate to more efficiently implement multiple simultaneous Pauli gates.
Improve the
qiskit.quantum_info.Pauli
operator. This class now represents and element from the full N-qubit Pauli group including complex coefficients. It now supports the Operator API methods including
compose()
,
dot()
,
tensor()
etc, where compose and dot are defined with respect to the full Pauli group.
This class also allows conversion to and from the string representation of Pauli’s for convenience.
For example
from
qiskit
.
quantum_info
import
Pauli
P1
=
Pauli
(
'XYZ'
)
P2
=
Pauli
(
'YZX'
)
P1
.
dot
(P2)
Pauli’s can also be directly appended to
QuantumCircuit
objects
from
qiskit
import
QuantumCircuit
from
qiskit
.
quantum_info
import
Pauli
circ
=
QuantumCircuit
(
3
)
circ
.
append
(
Pauli
(
'XYZ'
), [
0
,
1
,
2
])
circ
.
draw
(output
=
'mpl'
)
Additional methods allow computing when two Pauli’s commute (using the
commutes()
method) or anticommute (using the
anticommutes()
method), and computing the Pauli resulting from Clifford conjugation
P
′
=
C
.
P
.
C
†
P^\prime = C.P.C^\dagger
P
′
=
C
.
P
.
C
†
using the
evolve()
method.
See the API documentation of the
Pauli
class for additional information.
A new function,
random_pauli()
, for generating a random element of the N-qubit Pauli group has been added to the
qiskit.quantum_info
module.
A new class,
PiecewisePolynomialPauliRotations
, has been added to the
qiskit.circuit.library
module. This circuit library element is used for mapping a piecewise polynomial function,
f
(
x
)
f(x)
f
(
x
)
, which is defined through breakpoints and coefficients, on qubit amplitudes. The breakpoints
(
x
0
,
.
.
.
,
x
J
)
(x_0, ..., x_J)
(
x
0
​
,
...
,
x
J
​
)
are a subset of
[
0
,
2
n
−
1
]
[0, 2^n-1]
[
0
,
2
n
−
1
]
, where
n
n
n
is the number of state qubits. The corresponding coefficients
[
a
j
,
1
,
.
.
.
,
a
j
,
d
]
[a_{j,1},...,a_{j,d}]
[
a
j
,
1
​
,
...
,
a
j
,
d
​
]
, where
d
d
d
is the highest degree among all polynomials. Then
f
(
x
)
f(x)
f
(
x
)
is defined as:
f
(
x
)
=
{
0
,
x
<
x
0
∑
i
=
0
i
=
d
a
j
,
i
x
i
,
x
j
≤
x
<
x
j
+
1
\begin{split}f(x) = \begin{cases}
    0, x < x_0 \\
    \sum_{i=0}^{i=d}a_{j,i} x^i, x_j \leq x < x_{j+1}
    \end{cases}\end{split}
f
(
x
)
=
{
0
,
x
<
x
0
​
∑
i
=
0
i
=
d
​
a
j
,
i
​
x
i
,
x
j
​
≤
x
<
x
j
+
1
​
​
​
where we implicitly assume
x
J
+
1
=
2
n
x_{J+1} = 2^n
x
J
+
1
​
=
2
n
. And the mapping applied to the amplitudes is given by
F
∣
x
⟩
∣
0
⟩
=
cos
⁡
(
p
j
(
x
)
)
∣
x
⟩
∣
0
⟩
+
sin
⁡
(
p
j
(
x
)
)
∣
x
⟩
∣
1
⟩
F|x\rangle |0\rangle = \cos(p_j(x))|x\rangle |0\rangle + \sin(p_j(x))|x\rangle |1\rangle
F
∣
x
⟩
∣0
⟩
=
cos
(
p
j
​
(
x
))
∣
x
⟩
∣0
⟩
+
sin
(
p
j
​
(
x
))
∣
x
⟩
∣1
⟩
This mapping is based on controlled Pauli Y-rotations and constructed using the
PolynomialPauliRotations
.
A new module
qiskit.algorithms
has been introduced. This module contains functionality equivalent to what has previously been provided by the
qiskit.aqua.algorithms
module (which is now deprecated) and provides the building blocks for constructing quantum algorithms. For details on migrating from
qiskit-aqua
to this new module, please refer to the
migration guide
.
A new module
qiskit.opflow
has been introduced. This module contains functionality equivalent to what has previously been provided by the
qiskit.aqua.operators
module (which is now deprecated) and provides the operators and state functions which are used to build quantum algorithms. For details on migrating from
qiskit-aqua
to this new module, please refer to the
migration guide
.
This is the first release that includes precompiled binary wheels for the for Linux aarch64 systems. If you are running a manylinux2014 compatible aarch64 Linux system there are now precompiled wheels available on PyPI, you are no longer required to build from source to install qiskit-terra.
The
qiskit.quantum_info.process_fidelity()
function is now able to be used with a non-unitary target channel. In this case the returned value is equivalent to the
qiskit.quantum_info.state_fidelity()
of the normalized
qiskit.quantum_info.Choi
matrices for the channels.
Note that the
qiskit.quantum_info.average_gate_fidelity()
and
qiskit.quantum_info.gate_error()
functions still require the target channel to be unitary and will raise an exception if it is not.
Added a new pulse builder function,
qiskit.pulse.macro()
. This enables normal Python functions to be decorated as macros. This enables pulse builder functions to be used within the decorated function. The builder macro can then be called from within a pulse building context, enabling code reuse.
For Example:
from
qiskit
import
pulse
@pulse
.
macro
def
measure
(
qubit
:
int
):
pulse
.
play
(pulse.
GaussianSquare
(
16384
,
256
,
15872
),
pulse.
MeasureChannel
(qubit))
mem_slot
=
pulse
.
MemorySlot
(
0
)
pulse
.
acquire
(
16384
, pulse.
AcquireChannel
(
0
), mem_slot)
return
mem_slot
with
pulse
.
build
(backend
=
backend)
as
sched
:
mem_slot
=
measure
(
0
)
print
(
f
"Qubit measured into
{
mem_slot
}
"
)
sched
.
draw
()
A new class,
PauliTwoDesign
, was added to the
qiskit.circuit.library
which implements a particular form of a 2-design circuit from
https://arxiv.org/pdf/1803.11173.pdf
For instance, this circuit can look like:
from
qiskit
.
circuit
.
library
import
PauliTwoDesign
circuit
=
PauliTwoDesign
(
4
, reps
=
2
, seed
=
5
, insert_barriers
=
True
)
circuit
.
decompose
().
draw
(output
=
'mpl'
)
A new pulse drawer
qiskit.visualization.pulse_v2.draw()
(which is aliased as
qiskit.visualization.pulse_drawer_v2
) is now available. This new pulse drawer supports multiple new features not present in the original pulse drawer (
pulse_drawer()
).
Truncation of long pulse instructions.
Visualization of parametric pulses.
New stylesheets
IQXStandard
,
IQXSimple
,
IQXDebugging
.
Visualization of system info (channel frequency, etc…) by specifying
qiskit.providers.Backend
objects for visualization.
Specifying
axis
objects for plotting to allow further extension of generated plots, i.e., for publication manipulations.
New stylesheets can take callback functions that dynamically modify the apperance of the output image, for example, reassembling a collection of channels, showing details of instructions, updating appearance of pulse envelopes, etc… You can create custom callback functions and feed them into a stylesheet instance to modify the figure appearance without modifying the drawer code. See pulse drawer module docstrings for details.
Note that file saving is now delegated to Matplotlib. To save image files, you need to call
savefig
method with returned
Figure
object.
Adds a
reverse_qargs()
method to the
qiskit.quantum_info.Statevector
and
qiskit.quantum_info.DensityMatrix
classes. This method reverses the order of subsystems in the states and is equivalent to the
qiskit.circuit.QuantumCircuit.reverse_bits()
method for N-qubit states. For example:
from
qiskit
.
circuit
.
library
import
QFT
from
qiskit
.
quantum_info
import
Statevector
circ
=
QFT
(
3
)
state1
=
Statevector
.
from_instruction
(circ)
state2
=
Statevector
.
from_instruction
(circ.
reverse_bits
())
state1
.
reverse_qargs
()
==
state2
Adds a
reverse_qargs()
method to the
qiskit.quantum_info.Operator
class. This method reverses the order of subsystems in the operator and is equivalent to the
qiskit.circuit.QuantumCircuit.reverse_bits()
method for N-qubit operators. For example:
from
qiskit
.
circuit
.
library
import
QFT
from
qiskit
.
quantum_info
import
Operator
circ
=
QFT
(
3
)
op1
=
Operator
(circ)
op2
=
Operator
(circ.
reverse_bits
())
op1
.
reverse_qargs
()
==
op2
The
latex
output method for the
qiskit.visualization.circuit_drawer()
function and the
draw()
method now will use a user defined label on gates in the output visualization. For example:
import
math
from
qiskit
.
circuit
import
QuantumCircuit
qc
=
QuantumCircuit
(
2
)
qc
.
h
(
0
)
qc
.
rx
(math.pi
/
2
,
0
, label
=
'My Special Rotation'
)
qc
.
draw
(output
=
'latex'
)
The
routing_method
kwarg for the
transpile()
function now accepts a new option,
'none'
. When
routing_method='none'
no routing pass will be run as part of the transpilation. If the circuit does not fit coupling map a
TranspilerError
exception will be raised.
A new gate class,
RVGate
, was added to the
qiskit.circuit.library
module along with the corresponding
QuantumCircuit
method
rv()
. The
RVGate
is a general rotation gate, similar to the
UGate
, but instead of specifying Euler angles the three components of a rotation vector are specified where the direction of the vector specifies the rotation axis and the magnitude specifies the rotation angle about the axis in radians. For example:
import
math
import
np
from
qiskit
.
circuit
import
QuantumCircuit
qc
=
QuantumCircuit
(
1
)
theta
=
math
.
pi
/
5
phi
=
math
.
pi
/
3
# RGate axis:
axis
=
np
.
array
([math.
cos
(phi), math.
sin
(phi)])
rotation_vector
=
theta
*
axis
qc
.
rv
(
*
rotation_vector,
0
)
Unbound
Parameter
objects used in a
QuantumCircuit
object will now be sorted by name. This will take effect for the parameters returned by the
parameters
attribute. Additionally, the
qiskit.circuit.QuantumCircuit.bind_parameters()
and
qiskit.circuit.QuantumCircuit.assign_parameters()
methods can now take in a list of a values which will bind/assign them to the parameters in name-sorted order. Previously these methods would only take a dictionary of parameters and values. For example:
from
qiskit
.
circuit
import
QuantumCircuit
,
Parameter
circuit
=
QuantumCircuit
(
1
)
circuit
.
rx
(
Parameter
(
'x'
),
0
)
circuit
.
ry
(
Parameter
(
'y'
),
0
)
print
(circuit.parameters)
bound
=
circuit
.
bind_parameters
([
1
,
2
])
bound
.
draw
(output
=
'mpl'
)
The constructors for the
qiskit.quantum_info.Statevector
and
qiskit.quantum_info.DensityMatrix
classes can now take a
QuantumCircuit
object in to build a
Statevector
and
DensityMatrix
object from that circuit, assuming that the qubits are initialized in
∣
0
⟩
|0\rangle
∣0
⟩
. For example:
from
qiskit
import
QuantumCircuit
from
qiskit
.
quantum_info
import
Statevector
qc
=
QuantumCircuit
(
2
)
qc
.
h
(
0
)
qc
.
cx
(
0
,
1
)
statevector
=
Statevector
(qc)
statevector
.
draw
(output
=
'latex'
)
New fake backend classes are available under
qiskit.test.mock
. These included mocked versions of
ibmq_casablanca
,
ibmq_sydney
,
ibmq_mumbai
,
ibmq_lima
,
ibmq_belem
,
ibmq_quito
. As with the other fake backends, these include snapshots of calibration data (i.e.
backend.defaults()
) and error data (i.e.
backend.properties()
) taken from the real system, and can be used for local testing, compilation and simulation.
Known Issues
Attempting to add an
qiskit.pulse.Instruction
object with a parameterized
duration
(ie the value of
duration
is an unbound
Parameter
or
ParameterExpression
object) to a
qiskit.pulse.Schedule
is not supported. Attempting to do so will result in
UnassignedDurationError
PulseError
being raised. This is a limitation of how the
Instruction
overlap constraints are evaluated currently. This is supported by
ScheduleBlock
, in which the overlap constraints are evaluated just before the execution.
On Windows systems when parallel execution is enabled for
parallel_map()
parallelism may not work when called from a script running outside of a
if __name__ == '__main__':
block. This is due to how Python launches parallel processes on Windows. If a
RuntimeError
or
AttributeError
are raised by scripts that call
parallel_map()
(including using functions that use
parallel_map()
internally like
transpile()
) with Windows and parallelism enabled you can try embedding the script calls inside
if __name__ == '__main__':
to workaround the issue. For example:
from
qiskit
import
QuantumCircuit
,
QiskitError
from
qiskit
import
execute
,
Aer
qc1
=
QuantumCircuit
(
2
,
2
)
qc1
.
h
(
0
)
qc1
.
cx
(
0
,
1
)
qc1
.
measure
([
0
,
1
], [
0
,
1
])
# making another circuit: superpositions
qc2
=
QuantumCircuit
(
2
,
2
)
qc2
.
h
([
0
,
1
])
qc2
.
measure
([
0
,
1
], [
0
,
1
])
execute
([qc1, qc2], Aer.
get_backend
(
'qasm_simulator'
))
should be changed to:
from
qiskit
import
QuantumCircuit
,
QiskitError
from
qiskit
import
execute
,
Aer
def
main
():
qc1
=
QuantumCircuit
(
2
,
2
)
qc1
.
h
(
0
)
qc1
.
cx
(
0
,
1
)
qc1
.
measure
([
0
,
1
], [
0
,
1
])
# making another circuit: superpositions
qc2
=
QuantumCircuit
(
2
,
2
)
qc2
.
h
([
0
,
1
])
qc2
.
measure
([
0
,
1
], [
0
,
1
])
execute
([qc1, qc2], Aer.
get_backend
(
'qasm_simulator'
))
if
__name__
==
'__main__'
:
main
()
if any errors are encountered with parallelism on Windows.
Upgrade Notes
The preset pass managers
level_1_pass_manager
,
level_2_pass_manager
, and
level_3_pass_manager
(which are used for
optimization_level
1, 2, and 3 in the
transpile()
and
execute()
functions) now unconditionally use the
Optimize1qGatesDecomposition
pass for 1 qubit gate optimization. Previously, these pass managers would use the
Optimize1qGates
pass if the basis gates contained
u1
,
u2
, or
u3
. If you want to still use the old
Optimize1qGates
you will need to construct a custom
PassManager
with the pass.
Following transpilation of a parameterized
QuantumCircuit
, the
global_phase
attribute of output circuit may no longer be returned in a simplified form, if the global phase is a
ParameterExpression
.
For example:
qc
=
QuantumCircuit
(
1
)
theta
=
Parameter
(
'theta'
)
qc
.
rz
(theta,
0
)
qc
.
rz
(
-
theta,
0
)
print
(
transpile
(qc, basis_gates
=
[
'p'
]).global_phase)
previously returned
0
, but will now return
-0.5*theta + 0.5*theta
. This change was necessary was to avoid a large runtime performance penalty as simplifying symbolic expressions can be quite slow, especially if there are many
ParameterExpression
objects in a circuit.
The
BasicAerJob
job objects returned from BasicAer backends are now synchronous instances of
JobV1
. This means that calls to the
run()
will block until the simulation finishes executing. If you want to restore the previous async behavior you’ll need to wrap the
run()
with something that will run in a seperate thread or process like
futures.ThreadPoolExecutor
or
futures.ProcessPoolExecutor
.
The
allow_sample_measuring
option for the BasicAer simulator
QasmSimulatorPy
has changed from a default of
False
to
True
. This was done to better reflect the actual default behavior of the simulator, which would use sample measuring if the input circuit supported it (even if it was not enabled). If you are running a circuit that doesn’t support sample measurement (ie it has
Reset
operations or if there are operations after a measurement on a qubit) you should make sure to explicitly set this option to
False
when you call
run()
.
The
CommutativeCancellation
transpiler pass is now aware of the target basis gates, which means it will only use gates in the specified basis. Previously, the pass would unconditionally replace consecutive gates which commute with
ZGate
with the
U1Gate
. However, now that the pass is basis aware and has a kwarg,
basis_gates
, for specifying the target basis there is a potential change in behavior if the kwarg is not set. When the
basis_gates
kwarg is not used and there are no variable z-rotation gates in the circuit then no commutative cancellation will occur.
Register
(which is the parent class for
QuantumRegister
and
ClassicalRegister
and
Bit
(which is the parent class for
Qubit
and
Clbit
) objects are now immutable. In previous releases it was possible to adjust the value of a
size
or
name
attributes of a
Register
object and the
index
or
register
attributes of a
Bit
object after it was initially created. However this would lead to unsound behavior that would corrupt container structure that rely on a hash (such as a dict) since these attributes are treated as immutable properties of a register or bit (see
#4705
for more details). To avoid this unsound behavior this attributes of a
Register
and
Bit
are no longer settable after initial creation. If you were previously adjusting the objects at runtime you will now need to create a new
Register
or
Bit
object with the new values.
The
DAGCircuit.__eq__
method (which is used by the
==
operator), which is used to check structural equality of
DAGCircuit
and
QuantumCircuit
instances, will now include the
global_phase
and
calibrations
attributes in the fields checked for equality. This means that circuits which would have evaluated as equal in prior releases may not anymore if the
global_phase
or
calibrations
differ between the circuits. For example, in previous releases this would return
True
:
import
math
from
qiskit
import
QuantumCircuit
qc1
=
QuantumCircuit
(
1
)
qc1
.
x
(
0
)
qc2
=
QuantumCircuit
(
1
, global_phase
=
math.pi)
qc2
.
x
(
0
)
print
(qc2
==
qc1)
However, now because the
global_phase
attribute of the circuits differ this will now return
False
.
The previously deprecated
qubits()
and
clbits()
methods on the
DAGCircuit
class, which were deprecated in the 0.15.0 Terra release, have been removed. Instead you should use the
qubits
and
clbits
attributes of the
DAGCircuit
class. For example, if you were running:
from
qiskit
.
dagcircuit
import
DAGCircuit
dag
=
DAGCircuit
()
qubits
=
dag
.
qubits
()
That would be replaced by:
from
qiskit
.
dagcircuit
import
DAGCircuit
dag
=
DAGCircuit
()
qubits
=
dag
.
qubits
The
PulseDefaults
returned by the fake pulse backends
qiskit.test.mock.FakeOpenPulse2Q
and
qiskit.test.mock.FakeOpenPulse3Q
have been updated to have more realistic pulse sequence definitions. If you are using these fake backend classes you may need to update your usage because of these changes.
The default synthesis method used by
decompose_clifford()
function in the
quantum_info
module (which gets used internally by the
qiskit.quantum_info.Clifford.to_circuit()
method) for more than 3 qubits now uses a non-optimal greedy compilation routine for Clifford elements synthesis, by Bravyi et. al., which typically yields better CX cost compared to the old default. If you need to revert to the previous Aaronson-Gottesman method this can be done by setting
method='AG'
.
The previously deprecated module
qiskit.visualization.interactive
, which was deprecated in the 0.15.0 release, has now been removed. Instead you should use the matplotlib based visualizations:
Removed Interactive function
Equivalent matplotlib function
iplot_bloch_multivector
qiskit.visualization.plot_bloch_multivector()
iplot_state_city
qiskit.visualization.plot_state_city()
iplot_state_qsphere
qiskit.visualization.plot_state_qsphere()
iplot_state_hinton
qiskit.visualization.plot_state_hinton()
iplot_histogram
qiskit.visualization.plot_histogram()
iplot_state_paulivec
qiskit.visualization.plot_state_paulivec()
The
qiskit.Aer
and
qiskit.IBMQ
top level attributes are now lazy loaded. This means that the objects will now always exist and warnings will no longer be raised on import if
qiskit-aer
or
qiskit-ibmq-provider
are not installed (or can’t be found by Python). If you were checking for the presence of
qiskit-aer
or
qiskit-ibmq-provider
using these module attributes and explicitly comparing to
None
or looking for the absence of the attribute this no longer will work because they are always defined as an object now. In other words running something like:
try
:
from
qiskit
import
Aer
except
ImportError
:
print
(
"Aer not available"
)
or
::
try
:
from
qiskit
import
IBMQ
except
ImportError
:
print
(
"IBMQ not available"
)
will no longer work. Instead to determine if those providers are present you can either explicitly use
qiskit.providers.aer.Aer
and
qiskit.providers.ibmq.IBMQ
:
try
:
from
qiskit
.
providers
.
aer
import
Aer
except
ImportError
:
print
(
"Aer not available"
)
try
:
from
qiskit
.
providers
.
ibmq
import
IBMQ
except
ImportError
:
print
(
"IBMQ not available"
)
or check
bool(qiskit.Aer)
and
bool(qiskit.IBMQ)
instead, for example:
import
qiskit
if
not
qiskit
.
Aer
:
print
(
"Aer not available"
)
if
not
qiskit
.
IBMQ
:
print
(
"IBMQ not available"
)
This change was necessary to avoid potential import cycle issues between the qiskit packages and also to improve the import time when Aer or IBMQ are not being used.
The user config file option
suppress_packaging_warnings
option in the user config file and the
QISKIT_SUPPRESS_PACKAGING_WARNINGS
environment variable no longer has any effect and will be silently ignored. The warnings this option controlled have been removed and will no longer be emitted at import time from the
qiskit
module.
The previously deprecated
condition
kwarg for
qiskit.dagcircuit.DAGNode
constructor has been removed. It was deprecated in the 0.15.0 release. Instead you should now be setting the classical condition on the
Instruction
object passed into the
DAGNode
constructor when creating a new
op
node.
When creating a new
Register
(which is the parent class for
QuantumRegister
and
ClassicalRegister
) or
QuantumCircuit
object with a number of bits (eg
QuantumCircuit(2)
), it is now required that number of bits are specified as an integer or another type which is castable to unambiguous integers(e.g.
2.0
). Non-integer values will now raise an error as the intent in those cases was unclear (you can’t have fractional bits). For more information on why this was changed refer to:
#4855
networkx
is no longer a requirement for qiskit-terra. All the networkx usage inside qiskit-terra has been removed with the exception of 3 methods:
qiskit.dagcircuit.DAGCircuit.to_networkx
qiskit.dagcircuit.DAGCircuit.from_networkx
qiskit.dagcircuit.DAGDependency.to_networkx
If you are using any of these methods you will need to manually install networkx in your environment to continue using them.
By default on macOS with Python >=3.8
parallel_map()
will no longer run in multiple processes. This is a change from previous releases where the default behavior was that
parallel_map()
would launch multiple processes. This change was made because with newer versions of macOS with Python 3.8 and 3.9 multiprocessing is either unreliable or adds significant overhead because of the change in Python 3.8 to launch new processes with
spawn
instead of
fork
. To re-enable parallel execution on macOS with Python >= 3.8 you can use the user config file
parallel
option or set the environment variable
QISKIT_PARALLEL
to
True
.
The previously deprecated kwarg
callback
on the constructor for the
PassManager
class has been removed. This kwarg has been deprecated since the 0.13.0 release (April, 9th 2020). Instead you can pass the
callback
kwarg to the
qiskit.transpiler.PassManager.run()
method directly. For example, if you were using:
from
qiskit
.
circuit
.
random
import
random_circuit
from
qiskit
.
transpiler
import
PassManager
qc
=
random_circuit
(
2
,
2
)
def
callback
(
**
kwargs
)
print
(kwargs[
'pass_'
])
pm
=
PassManager
(callback
=
callback)
pm
.
run
(qc)
this can be replaced with:
from
qiskit
.
circuit
.
random
import
random_circuit
from
qiskit
.
transpiler
import
PassManager
qc
=
random_circuit
(
2
,
2
)
def
callback
(
**
kwargs
)
print
(kwargs[
'pass_'
])
pm
=
PassManager
()
pm
.
run
(qc, callback
=
callback)
It is now no longer possible to instantiate a base channel without a prefix, such as
qiskit.pulse.Channel
or
qiskit.pulse.PulseChannel
. These classes are designed to classify types of different user facing channel classes, such as
qiskit.pulse.DriveChannel
, but do not have a definition as a target resource. If you were previously directly instantiating either
qiskit.pulse.Channel
or
qiskit.pulse.PulseChannel
, this is no longer allowed. Please use the appropriate subclass.
When the
require_cp
and/or
require_tp
kwargs of
qiskit.quantum_info.process_fidelity()
,
qiskit.quantum_info.average_gate_fidelity()
,
qiskit.quantum_info.gate_error()
are
True
, they will now only log a warning rather than the previous behavior of raising a
QiskitError
exception if the input channel is non-CP or non-TP respectively.
The
QFT
class in the
qiskit.circuit.library
module now computes the Fourier transform using a little-endian representation of tensors, i.e. the state
∣
1
⟩
|1\rangle
∣1
⟩
maps to
∣
0
⟩
−
∣
1
⟩
+
∣
2
⟩
−
.
.
|0\rangle - |1\rangle + |2\rangle - ..
∣0
⟩
−
∣1
⟩
+
∣2
⟩
−
..
assuming the computational basis correspond to little-endian bit ordering of the integers.
∣
0
⟩
=
∣
000
⟩
,
∣
1
⟩
=
∣
001
⟩
|0\rangle = |000\rangle, |1\rangle = |001\rangle
∣0
⟩
=
∣000
⟩
,
∣1
⟩
=
∣001
⟩
, etc. This was done to make it more consistent with the rest of Qiskit, which uses a little-endian convention for bit order. If you were depending on the previous bit order you can use the
reverse_bits()
method to revert to the previous behavior. For example:
from
qiskit
.
circuit
.
library
import
QFT
qft
=
QFT
(
5
).
reverse_bits
()
The
qiskit.__qiskit_version__
module attribute was previously a
dict
will now return a custom read-only
Mapping
object that checks the version of qiskit elements at runtime instead of at import time. This was done to speed up the import path of qiskit and eliminate a possible import cycle by only importing the element packages at runtime if the version is needed from the package. This should be fully compatible with the
dict
previously return and for most normal use cases there will be no difference. However, if some applications were relying on either mutating the contents or explicitly type checking it may require updates to adapt to this change.
The
qiskit.execute
module has been renamed to
qiskit.execute_function
. This was necessary to avoid a potentical name conflict between the
execute()
function which is re-exported as
qiskit.execute
.
qiskit.execute
the function in some situations could conflict with
qiskit.execute
the module which would lead to a cryptic error because Python was treating
qiskit.execute
as the module when the intent was to the function or vice versa. The module rename was necessary to avoid this conflict. If you’re importing
qiskit.execute
to get the module (typical usage was
from qiskit.execute import execute
) you will need to update this to use
qiskit.execute_function
instead.
qiskit.execute
will now always resolve to the function.
The
qiskit.compiler.transpile
,
qiskit.compiler.assemble
,
qiskit.compiler.schedule
, and
qiskit.compiler.sequence
modules have been renamed to
qiskit.compiler.transpiler
,
qiskit.compiler.assembler
,
qiskit.compiler.scheduler
, and
qiskit.compiler.sequence
respectively. This was necessary to avoid a potentical name conflict between the modules and the re-exported function paths
qiskit.compiler.transpile()
,
qiskit.compiler.assemble()
,
qiskit.compiler.schedule()
, and
qiskit.compiler.sequence()
. In some situations this name conflict between the module path and re-exported function path would lead to a cryptic error because Python was treating an import as the module when the intent was to use the function or vice versa. The module rename was necessary to avoid this conflict. If you were using the imports to get the modules before (typical usage would be like``from qiskit.compiler.transpile import transpile``) you will need to update this to use the new module paths.
qiskit.compiler.transpile()
,
qiskit.compiler.assemble()
,
qiskit.compiler.schedule()
, and
qiskit.compiler.sequence()
will now always resolve to the functions.
The
qiskit.quantum_info.Quaternion
class was moved from the
qiskit.quantum_info.operator
submodule to the
qiskit.quantum_info.synthesis
submodule to better reflect it’s purpose. No change is required if you were importing it from the root
qiskit.quantum_info
module, but if you were importing from
qiskit.quantum_info.operator
you will need to update your import path.
Removed the
QuantumCircuit.mcmt
method, which has been deprecated since the Qiskit Terra 0.14.0 release in April 2020. Instead of using the method, please use the
MCMT
class instead to construct a multi-control multi-target gate and use the
qiskit.circuit.QuantumCircuit.append()
or
qiskit.circuit.QuantumCircuit.compose()
to add it to a circuit.
For example, you can replace:
circuit
.
mcmt
(
ZGate
(), [
0
,
1
,
2
], [
3
,
4
])
with:
from
qiskit
.
circuit
.
library
import
MCMT
mcmt
=
MCMT
(
ZGate
(),
3
,
2
)
circuit
.
compose
(mcmt,
range
(
5
))
Removed the
QuantumCircuit.diag_gate
method which has been deprecated since the Qiskit Terra 0.14.0 release in April 2020. Instead, use the
diagonal()
method of
QuantumCircuit
.
Removed the
QuantumCircuit.ucy
method which has been deprecated since the Qiskit Terra 0.14.0 release in April 2020. Instead, use the
ucry()
method of
QuantumCircuit
.
The previously deprecated
mirror()
method for
qiskit.circuit.QuantumCircuit
has been removed. It was deprecated in the 0.15.0 release. The
qiskit.circuit.QuantumCircuit.reverse_ops()
method should be used instead since mirroring could be confused with swapping the output qubits of the circuit. The
reverse_ops()
method only reverses the order of gates that are applied instead of mirroring.
The previously deprecated support passing a float (for the
scale
kwarg as the first positional argument to the
qiskit.circuit.QuantumCircuit.draw()
has been removed. It was deprecated in the 0.12.0 release. The first positional argument to the
qiskit.circuit.QuantumCircuit.draw()
method is now the
output
kwarg which does not accept a float. Instead you should be using
scale
as a named kwarg instead of using it positionally.
For example, if you were previously calling
draw
with:
from
qiskit
import
QuantumCircuit
qc
=
QuantumCircuit
(
2
)
qc
.
draw
(
0.75
, output
=
'mpl'
)
this would now need to be:
from
qiskit
import
QuantumCircuit
qc
=
QuantumCircuit
(
2
)
qc
.
draw
(output
=
'mpl'
, scale
=
0.75
)
or:
qc
.
draw
(
'mpl'
, scale
=
0.75
)
Features of Qiskit Pulse (
qiskit.pulse
) which were deprecated in the 0.15.0 release (August, 2020) have been removed. The full set of changes are:
Module
Old
New
qiskit.pulse.library
SamplePulse
Waveform
qiskit.pulse.library
ConstantPulse
Constant
(module rename)
pulse.pulse_lib
Module
qiskit.pulse.library
Class
Old method
New method
ParametricPulse
get_sample_pulse
get_waveform
Instruction
command
N/A. Commands and Instructions have been unified. Use
operands()
to get information about the instruction data.
Acquire
acquires
,
mem_slots
,
reg_slots
acquire()
,
mem_slot()
,
reg_slot()
. (The
Acquire
instruction no longer broadcasts across multiple qubits.)
The dictionary previously held on
DAGCircuit
edges has been removed. Instead, edges now hold the
Bit
instance which had previously been included in the dictionary as its
'wire'
field. Note that the NetworkX graph returned by
to_networkx()
will still have a dictionary for its edge attributes, but the
'name'
field will no longer be populated.
The
parameters
attribute of the
QuantumCircuit
class no longer is returning a
set
. Instead it returns a
ParameterView
object which implements all the methods that
set
offers (albeit deprecated). This was done to support a model that preserves name-sorted parameters. It should be fully compatible with any previous usage of the
set
returned by the
parameters
attribute, except for where explicit type checking of a set was done.
When running
transpile()
on a
QuantumCircuit
with
delay()
instructions, the units will be converted to dt if the value of dt (sample time) is known to
transpile()
, either explicitly via the
dt
kwarg or via the
BackendConfiguration
for a
Backend
object passed in via the
backend
kwarg.
The interpretation of
meas_map
(which is an attribute of a
PulseBackendConfiguration
object or as the corresponding
meas_map
kwarg on the
schedule()
,
assemble()
,
sequence()
, or
execute()
functions) has been updated to better match the true constraints of the hardware. The format of this data is a list of lists, where the items in the inner list are integers specifying qubit labels. For instance:
[[A
,
B
,
C]
,
[D
,
E
,
F
,
G]]
Previously, the
meas_map
constraint was interpreted such that if one qubit was acquired (e.g. A), then all other qubits sharing a subgroup with that qubit (B and C) would have to be acquired at the same time and for the same duration. This constraint has been relaxed. One acquisition does not require more acquisitions. (If A is acquired, B and C do
not
need to be acquired.) Instead, qubits in the same measurement group cannot be acquired in a partially overlapping way – think of the
meas_map
as specifying a shared acquisition resource (If we acquire A from
t=1000
to
t=2000
, we cannot acquire B starting from
1000<t<2000
). For example:
# Good
meas_map
=
[[
0
,
1
]]
# Acquire a subset of [0, 1]
sched
=
pulse
.
Schedule
()
sched
=
sched
.
append
(pulse.
Acquire
(
10
, acq_q0))
# Acquire 0 and 1 together (same start time, same duration)
sched
=
pulse
.
Schedule
()
sched
=
sched
.
append
(pulse.
Acquire
(
10
, acq_q0))
sched
=
sched
.
append
(pulse.
Acquire
(
10
, acq_q1))
# Acquire 0 and 1 disjointly
sched
=
pulse
.
Schedule
()
sched
=
sched
.
append
(pulse.
Acquire
(
10
, acq_q0))
sched
=
sched
.
append
(pulse.
Acquire
(
10
, acq_q1))
<<
10
# Acquisitions overlap, but 0 and 1 aren't in the same measurement
# grouping
meas_map
=
[[
0
]
,
[
1
]]
sched
=
pulse
.
Schedule
()
sched
=
sched
.
append
(pulse.
Acquire
(
10
, acq_q0))
sched
=
sched
.
append
(pulse.
Acquire
(
10
, acq_q1))
<<
1
# Bad: 0 and 1 are in the same grouping, but acquisitions
# partially overlap
meas_map
=
[[
0
,
1
]]
sched
=
pulse
.
Schedule
()
sched
=
sched
.
append
(pulse.
Acquire
(
10
, acq_q0))
sched
=
sched
.
append
(pulse.
Acquire
(
10
, acq_q1))
<<
1
Deprecation Notes
Two new arguments have been added to
qiskit.dagcircuit.DAGNode.semantic_eq()
,
bit_indices1
and
bit_indices2
, which are expected to map the
Bit
instances in each
DAGNode
to their index in
qubits
or
clbits
list of their respective
DAGCircuit
. During the deprecation period, these arguments are optional and when
not
specified the mappings will be automatically constructed based on the
register
and
index
properties of each
Bit
instance. However, in a future release, they will be required arguments and the mapping will need to be supplied by the user.
The
pulse
builder functions:
qiskit.pulse.call_circuit()
qiskit.pulse.call_schedule()
are deprecated and will be removed in a future release. These functions are unified into
qiskit.pulse.call()
which should be used instead.
The
qiskit.pulse.Schedule
method
qiskit.pulse.Schedule.flatten()
method is deprecated and will be removed in a future release. Instead you can use the
qiskit.pulse.transforms.flatten()
function which will perform the same operation.
The
assign_parameters()
for the following classes:
qiskit.pulse.channels.Channel
,
qiskit.pulse.library.Pulse
,
qiskit.pulse.instructions.Instruction
,
and all their subclasses is now deprecated and will be removed in a future release. This functionality has been subsumed
ScheduleBlock
which is the future direction for constructing parameterized pulse programs.
The
parameters
attribute for the following clasess:
Channel
Instruction
.
is deprecated and will be removed in a future release. This functionality has been subsumed
ScheduleBlock
which is the future direction for constructing parameterized pulse programs.
Python 3.6 support has been deprecated and will be removed in a future release. When support is removed you will need to upgrade the Python version you’re using to Python 3.7 or above.
Two
QuantumCircuit
methods
combine()
and
extend()
along with their corresponding Python operators
+
and
+=
are deprecated and will be removed in a future release. Instead the
QuantumCircuit
method
compose()
should be used. The
compose()
method allows more flexibility in composing two circuits that do not have matching registers. It does not, however, automatically add qubits/clbits unlike the deprecated methods. To add a circuit on new qubits/clbits, the
qiskit.circuit.QuantumCircuit.tensor()
method can be used. For example:
from
qiskit
.
circuit
import
QuantumRegister
,
QuantumCircuit
a
=
QuantumRegister
(
2
,
'a'
)
circuit_a
=
QuantumCircuit
(a)
circuit_a
.
cx
(
0
,
1
)
b
=
QuantumRegister
(
2
,
'b'
)
circuit_b
=
QuantumCircuit
(b)
circuit_b
.
cz
(
0
,
1
)
# same as circuit_a + circuit_b (or combine)
added_with_different_regs
=
circuit_b
.
tensor
(circuit_a)
# same as circuit_a + circuit_a (or combine)
added_with_same_regs
=
circuit_a
.
compose
(circuit_a)
# same as circuit_a += circuit_b (or extend)
circuit_a
=
circuit_b
.
tensor
(circuit_a)
# same as circuit_a += circuit_a (or extend)
circuit_a
.
compose
(circuit_a, inplace
=
True
)
Support for passing
Qubit
instances to the
qubits
kwarg of the
qiskit.transpiler.InstructionDurations.get()
method has been deprecated and will be removed in a future release. Instead, you should call the
get()
method with the integer indices of the desired qubits.
Using
@
(
__matmul__
) for invoking the
compose
method of
BaseOperator
subclasses (eg
Operator
) is deprecated and will be removed in a future release. The
qiskit.quantum_info.Operator.compose()
method can be used directly or also invoked using the
&
(
__and__
) operator.
Using
*
(
__mul__
) for calling the
dot()
method of
BaseOperator
subclasses (eg
qiskit.quantum_info.Operator
) is deprecated and will be removed in a future release. Instead you can just call the
dot()
directly.
Using
@
(
__matmul__
) for invoking the
evolve()
method of the
qiskit.quantum_info.Statevector
and
qiskit.quantum_info.DensityMatrix
classes is deprecated and will be removed in a future release.. The
evolve
method can be used directly or also invoked using the
&
(
__and__
) operator.
The
qiskit.pulse.schedule.ParameterizedSchedule
class has been deprecated and will be removed in a future release. Instead you can directly parameterize pulse
Schedule
objects with a
Parameter
object, for example:
from
qiskit
.
circuit
import
Parameter
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
import
ShiftPhase
,
DriveChannel
theta
=
Parameter
(
'theta'
)
target_schedule
=
Schedule
()
target_schedule
.
insert
(
0
,
ShiftPhase
(theta,
DriveChannel
(
0
)), inplace
=
True
)
The
qiskit.pulse.ScheduleComponent
class in the
qiskit.pulse
module has been deprecated and will be removed in a future release. Its usage should be replaced either using a
qiskit.pulse.Schedule
or
qiskit.pulse.Instruction
directly. Additionally, the primary purpose of the
ScheduleComponent
class was as a common base class for both
Schedule
and
Instruction
for any place that was explicitly type checking or documenting accepting a
ScheduleComponent
input should be updated to accept
Instruction
or
Schedule
.
The JSON Schema files and usage for the IBMQ API payloads are deprecated and will be removed in a future release. This includes everything under the
qiskit.schemas
module and the
qiskit.validation
module. This also includes the
validate
kwargs for
qiskit.qobj.QasmQobj.to_dict()
and
qiskit.qobj.QasmQobj.to_dict()
along with the module level fastjsonschema validators in
qiskit.qobj
(which do not raise a deprecation warning). The schema files have been moved to the
Qiskit/ibmq-schemas
repository and those should be treated as the canonical versions of the API schemas. Moving forward only those schemas will recieve updates and will be used as the source of truth for the schemas. If you were relying on the schemas bundled in qiskit-terra you should update to use that repository instead.
The
qiskit.util
module has been deprecated and will be removed in a future release. It has been replaced by
qiskit.utils
which provides the same functionality and will be expanded in the future. Note that no
DeprecationWarning
will be emitted regarding this deprecation since it was not feasible on Python 3.6.
The
CXDirection
transpiler pass in the
qiskit.transpiler.passes
module has been deprecated and will be removed in a future release. Instead the
GateDirection
should be used. It behaves identically to the
CXDirection
except that it now also supports transforming a circuit with
ECRGate
gates in addition to
CXGate
gates.
The
CheckCXDirection
transpiler pass in the
qiskit.transpiler.passes
module has been deprecated and will be removed in a future release. Instead the
CheckGateDirection
pass should be used. It behaves identically to the
CheckCXDirection
except that it now also supports checking the direction of all 2-qubit gates, not just
CXGate
gates.
The
WeightedAdder
method
num_ancilla_qubits()
is deprecated and will be removed in a future release. It has been replaced with the
qiskit.circuit.library.WeightedAdder.num_ancillas
attribute which is consistent with other circuit libraries’ APIs.
The following legacy methods of the
qiskit.quantum_info.Pauli
class have been deprecated. See the method documentation for replacement use in the updated Pauli class.
from_label()
sgn_prod()
to_spmatrix()
kron()
update_z()
update_x()
insert_paulis()
append_paulis()
delete_qubits()
pauli_single()
random()
Using a
list
or
numpy.ndarray
as the
channel
or
target
argument for the
qiskit.quantum_info.process_fidelity()
,
qiskit.quantum_info.average_gate_fidelity()
,
qiskit.quantum_info.gate_error()
, and
qiskit.quantum_info.diamond_norm()
functions has been deprecated and will not be supported in a future release. The inputs should instead be a
Gate
or a
BaseOperator
subclass object (eg.
Operator
,
Choi
, etc.)
Accessing references from
Qubit
and
Clbit
instances to their containing registers via the
register
or
index
properties has been deprecated and will be removed in a future release. Instead,
Register
objects can be queried to find the
Bit
objects they contain.
The current functionality of the
qiskit.visualization.pulse_drawer()
function is deprecated and will be replaced by
qiskit.visualization.pulse_drawer_v2()
(which is not backwards compatible) in a future release.
The use of methods inherited from the
set
type on the output of the
parameters
attribute (which used to be a
set
) of the
QuantumCircuit
class are deprecated and will be removed in a future release. This includes the methods from the
add()
,
difference()
,
difference_update()
,
discard()
,
intersection()
,
intersection_update()
,
issubset()
,
issuperset()
,
symmetric_difference()
,
symmetric_difference_update()
,
union()
,
update()
,
__isub__()
(which is the
-=
operator), and
__ixor__()
(which is the
^=
operator).
The name of the first (and only) positional argument for the
qiskit.circuit.QuantumCircuit.bind_parameters()
method has changed from
value_dict
to
values
. The passing an argument in with the name
values_dict
is deprecated and will be removed in future release. For example, if you were previously calling
bind_parameters()
with a call like:
bind_parameters(values_dict={})
this is deprecated and should be replaced by
bind_parameters(values={})
or even better just pass the argument positionally
bind_parameters({})
.
The name of the first (and only) positional argument for the
qiskit.circuit.QuantumCircuit.assign_parameters()
method has changed from
param_dict
to
parameters
. Passing an argument in with the name
param_dict
is deprecated and will be removed in future release. For example, if you were previously calling
assign_parameters()
with a call like:
assign_parameters(param_dict={})
this is deprecated and should be replaced by
assign_parameters(values={})
or even better just pass the argument positionally
assign_parameters({})
.
Bug Fixes
Fixed an issue where the
execute()
function would raise
QiskitError
exception when a
ParameterVector
object was passed in for the
parameter_bind
kwarg. parameter. For example, it is now possible to call something like:
execute
(circuit, backend, parameter_binds
=
[{pv1: [...], pv2: [...]}])
where
pv1
and
pv2
are
ParameterVector
objects. Fixed
#5467
Fixed an issue with the labels of parametric pulses in the
PulseQobjInstruction
class were not being properly set as they are with sampled pulses. This also means that pulse names that are imported from the
PulseDefaults
returned by a
Backend
, such as
x90
,
x90m
, etc, will properly be set. Fixed
#5363
Fixed an issue where unbound parameters only occurring in the
global_phase
attribute of a
QuantumCircuit
object would not show in the
parameters
attribute and could not be bound. Fixed
#5806
The
calibrations
attribute of
QuantumCircuit
objects are now preserved when the
+=
(ie the
extend()
method) and the
+
(ie the
combine()
method) are used. Fixed
#5930
and
#5908
The
name
setter method of class
Register
(which is the parent class of
QuantumRegister
and
ClassicalRegister
) previously did not check if the assigned string was a valid register name as per the
OpenQASM specification
. This check was previously only performed when the name was specified in the constructor, this has now been fixed so that setting the
name
attribute directly with an invalid value will now also raise an exception. Fixed
#5461
Fixed an issue with the
qiskit.visualization.circuit_drawer()
function and
qiskit.circuit.QuantumCircuit.draw()
method when visualizing a
QuantumCircuit
with a
Gate
that has a classical condition after a
Measure
that used the same
ClassicalRegister
, it was possible for the conditional
Gate
to be displayed to the left of the
Measure
. Fixed
#5387
In the transpiler pass
qiskit.transpiler.passes.CSPLayout
a bias towards lower numbered qubits could be observed. This undesireable bias has been fixed by shuffling the candidates to randomize the results. Furthermore, the usage of the
CSPLayout
pass in the
preset_passmanagers
(for level 2 and 3) has been adjusted to use a configured seed if the
seed_transpiler
kwarg is set when
transpile()
is called. Fixed
#5990
Fixes a bug where the
channels
field for a
PulseBackendConfiguration
object was not being included in the output of the
qiskit.providers.models.PulseBackendConfiguration.to_dict
method. Fixed
#5579
Fixed the
'circular'
entanglement in the
qiskit.circuit.library.NLocal
circuit class for the edge case where the circuit has the same size as the entanglement block (e.g. a two-qubit circuit and CZ entanglement gates). In this case there should only be one entanglement gate, but there was accidentially added a second one in the inverse direction as the first. Fixed
qiskit-community/qiskit-aqua#1452
Fixed the handling of breakpoints in the
PiecewisePolynomialPauliRotations
class in the
qiskit.circuit.library
. Now for
n
intervals,
n+1
breakpoints are allowed. This enables specifying another end interval other than
2
num qubits
2^\text{num qubits}
2
num qubits
. This is important because from the end of the last interval to
2
num qubits
2^\text{num qubits}
2
num qubits
the function is the identity.
Fixed an issue in the
qiskit.circuit.library.Permutation
circuit class where some permutations would not be properly generated. This issue could also effect
qiskit.circuit.library.QuantumVolume
if it were called with classical_permutation=False`. Fixed
#5812
Fixed an issue where generating QASM output with the
qasm()
method for a
QuantumCircuit
object that has a
ControlledGate
with an open control the output would be as if all controls were closed independent of the specified control state. This would result in a different circuit being created from
from_qasm_str()
if parsing the generated QASM.
This was fixed by updating the QASM output from
qasm()
by defining a composite gate which uses
XGate
to implement the open controls. The composite gate is named like
<original_gate_name>_o<ctrl_state>
where
o
stands for open control and
ctrl_state
is the integer value of the control state. Fixed
#5443
Fixed an issue where binding
Parameter
objects in a
QuantumCircuit
with the
parameter_binds
in the
execute
function would cause all the bound
QuantumCircuit
objects would have the same
name
, which meant the result names were also not unique. This fix causes the
bind_parameters()
and
assign_parameters()
to assign a unique circuit name when
inplace=False
as:
<
base name
>-<class
instance no
.
>
[
-<
pid name
>
]
where
<base name>
is the name supplied by the “name” kwarg, otherwise it defaults to “circuit”. The class instance number gets incremented every time an instance of the class is generated.
<pid name>
is appended if called outside the main process. Fixed
#5185
Fixed an issue with the
scheduler()
function where it would raise an exception if an input circuit contained an unbound
QuantumCircuit
object. Fixed
#5304
Fixed an issue in the
qiskit.transpiler.passes.TemplateOptimization
transpiler passes where template circuits that contained unbound
Parameter
objects would crash under some scenarios if the parameters could not be bound during the template matching. Now, if the
Parameter
objects can not be bound templates with unbound
Parameter
are discarded and ignored by the
TemplateOptimization
pass. Fixed
#5533
Fixed an issue with the
qiskit.visualization.timeline_drawer()
function where classical bits were inproperly handled. Fixed
#5361
Fixed an issue in the
qiskit.visualization.circuit_drawer()
function and the
qiskit.circuit.QuantumCircuit.draw()
method where
Delay
instructions in a
QuantumCircuit
object were not being correctly treated as idle time. So when the
idle_wires
kwarg was set to
False
the wires with the
Delay
objects would still be shown. This has been fixed so that the idle wires are removed from the visualization if there are only
Delay
objects on a wire.
Previously, when the option
layout_method
kwarg was provided to the
transpile()
function and the
optimization_level
kwarg was set to >= 2 so that the pass
qiskit.transpiler.passes.CSPLayout
would run, if
CSPLayout
found a solution then the method in
layout_method
was not executed. This has been fixed so that if specified, the
layout_method
is always honored. Fixed
#5409
When the argument
coupling_map=None
(either set explicitly, set implicitly as the default value, or via the
backend
kwarg), the transpiling process was not “embedding” the circuit. That is, even when an
initial_layout
was specified, the virtual qubits were not assigned to physical qubits. This has been fixed so that now, the
qiskit.compiler.transpile()
function honors the
initial_layout
argument by embedding the circuit:
from
qiskit
import
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
, name
=
'qr'
)
circ
=
QuantumCircuit
(qr)
circ
.
h
(qr[
0
])
circ
.
cx
(qr[
0
], qr[
1
])
transpile
(circ, initial_layout
=
[
1
,
0
]).
draw
(output
=
'mpl'
)
If the
initial_layout
refers to more qubits than in the circuit, the transpiling process will extended the circuit with ancillas.
from
qiskit
import
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
, name
=
'qr'
)
circ
=
QuantumCircuit
(qr)
circ
.
h
(qr[
0
])
circ
.
cx
(qr[
0
], qr[
1
])
transpile
(circ, initial_layout
=
[
4
,
2
], coupling_map
=
None
).
draw
()
Fixed
#5345
A new kwarg,
user_cost_dict
has been added to the constructor for the
qiskit.transpiler.passes.TemplateOptimization
transpiler pass. This enables users to provide a custom cost dictionary for the gates to the underlying template matching algorithm. For example:
from
qiskit
.
transpiler
.
passes
import
TemplateOptimization
cost_dict
=
{
'id'
:
0
,
'x'
:
1
,
'y'
:
1
,
'z'
:
1
,
'h'
:
1
,
't'
:
1
}
pass
=
TemplateOptimization
(user_cost_dict
=
cost_dict)
An issue when passing the
Counts
object returned by
get_counts()
to
marginal_counts()
would produce an improperly formatted
Counts
object with certain inputs has been fixed. Fixes
#5424
Improved the allocation of helper qubits in
PolynomialPauliRotations
and
PiecewiseLinearPauliRotations
which makes the implementation of these circuit more efficient. Fixed
#5320
and
#5322
Fix the usage of the allocated helper qubits in the
MCXGate
in the
WeightedAdder
class. These were previously allocated but not used prior to this fix. Fixed
#5321
In a number of cases, the
latex
output method for the
qiskit.visualization.circuit_drawer()
function and the
draw()
method did not display the gate name correctly, and in other cases, did not include gate parameters where they should be. Now the gate names will be displayed the same way as they are displayed with the
mpl
output method, and parameters will display for all the gates that have them. In addition, some of the gates did not display in the correct form, and these have been fixed. Fixes
#5605
,
#4938
, and
#3765
Fixed an issue where, if the
qiskit.circuit.Instruction.to_instruction()
method was used on a subcircuit which contained classical registers and that
Instruction
object was then added to a
QuantumCircuit
object, then the output from the
qiskit.visualization.circuit_drawer()
function and the
qiskit.circuit.QuantumCircuit.draw()
method would in some instances display the subcircuit to the left of a measure when it should have been displayed to the right. Fixed
#5947
Fixed an issue with
Delay
objects in a
QuantumCircuit
where
qiskit.compiler.transpile()
would not be convert the units of the
Delay
to the units of the
Backend
, if the
backend
kwarg is set on
transpile()
. This could result in the wrong behavior because of a unit mismatch, for example running:
from
qiskit
import
transpile
,
execute
from
qiskit
.
circuit
import
QuantumCircuit
qc
=
QuantumCircuit
(
1
)
qc
.
delay
(
100
, [
0
], unit
=
'us'
)
qc
=
transpile
(qc, backend)
job
=
execute
(qc, backend)
would previously have resulted in the backend delay for 100 timesteps (each of duration dt) rather than expected (100e-6 / dt) timesteps. This has been corrected so the
qiskit.compiler.transpile()
function properly converts the units.
Other Notes
The snapshots of all the fake/mock backends in
qiskit.test.mock
have been updated to reflect recent device changes. This includes a change in the
basis_gates
attribute for the
BackendConfiguration
to
['cx', 'rz', 'sx', 'x', 'id']
, the addition of a
readout_length
property to the qubit properties in the
BackendProperties
, and updating the
PulseDefaults
so that all the mock backends support parametric pulse based
InstructionScheduleMap
instances.
Aer 0.8.0
Prelude
The 0.8 release includes several new features and bug fixes. The highlights for this release are: the introduction of a unified
AerSimulator
backend for running circuit simulations using any of the supported simulation methods; a simulator instruction library (
qiskit.providers.aer.library
) which includes custom instructions for saving various kinds of simulator data; MPI support for running large simulations on a distributed computing environment.
New Features
Python 3.9 support has been added in this release. You can now run Qiskit Aer using Python 3.9 without building from source.
Add the CMake flag
DISABLE_CONAN
(default=``OFF``)s. When installing from source, setting this to
ON
allows bypassing the Conan package manager to find libraries that are already installed on your system. This is also available as an environment variable
DISABLE_CONAN
, which takes precedence over the CMake flag. This is not the official procedure to build AER. Thus, the user is responsible of providing all needed libraries and corresponding files to make them findable to CMake.
This release includes support for building qiskit-aer with MPI support to run large simulations on a distributed computing environment. See the
contributing guide
for instructions on building and running in an MPI environment.
It is now possible to build qiskit-aer with CUDA enabled in Windows. See the
contributing guide
for instructions on building from source with GPU support.
When building the qiskit-aer Python extension from source several build dependencies need to be pre-installed to enable C++ compilation. As a user convenience when building the extension any of these build dependencies which were missing would be automatically installed using
pip
prior to the normal
setuptools
installation steps, however it was previously was not possible to avoid this automatic installation. To solve this issue a new environment variable
DISABLE_DEPENDENCY_INSTALL
has been added. If it is set to
1
or
ON
when building the python extension from source this will disable the automatic installation of these missing build dependencies.
Adds support for optimized N-qubit Pauli gate (
qiskit.circuit.library.PauliGate
) to the
StatevectorSimulator
,
UnitarySimulator
, and the statevector and density matrix methods of the
QasmSimulator
and
AerSimulator
.
The
run()
method for the
AerSimulator
,
QasmSimulator
,
StatevectorSimulator
, and
UnitarySimulator
backends now takes a
QuantumCircuit
(or a list of
QuantumCircuit
objects) as it’s input. The previous
QasmQobj
object is still supported for now, but will be deprecated in a future release.
For an example of how to use this see:
from
qiskit
import
transpile
,
QuantumCircuit
from
qiskit
.
providers
.
aer
import
Aer
backend
=
Aer
.
get_backend
(
'aer_simulator'
)
circuit
=
QuantumCircuit
(
2
)
qc
.
h
(
0
)
qc
.
cx
(
0
,
1
)
qc
.
measure_all
()
tqc
=
transpile
(circuit, backend)
result
=
backend
.
run
(tqc, shots
=
4096
).
result
()
The
run()
method for the
PulseSimulator
backend now takes a
Schedule
(or a list of
Schedule
objects) as it’s input. The previous
PulseQobj
object is still supported for now, but will be deprecated in a future release.
Adds the new
AerSimulator
simulator backend supporting the following simulation methods
automatic
statevector
stabilizer
density_matrix
matrix_product_state
unitary
superop
The default automatic method will automatically choose a simulation method separately for each run circuit based on the circuit instructions and noise model (if any). Initializing a simulator with a specific method can be done using the method option.
GPU simulation for the statevector, density matrix and unitary methods can be enabled by setting the
device='GPU'
backend option.
Note that the
unitary
and
superop
methods do not support measurement as they simulate the unitary matrix or superoperator matrix of the run circuit so one of the new
save_unitary()
,
save_superop()
, or
save_state()
instructions must be used to save the simulator state to the returned results. Similarly state of the other simulations methods can be saved using the appropriate instructions. See the
qiskit.providers.aer.library
API documents for more details.
Note that the
AerSimulator
simulator superceds the
QasmSimulator
,
StatevectorSimulator
, and
UnitarySimulator
backends which will be deprecated in a future release.
Updates the
AerProvider
class to include multiple
AerSimulator
backends preconfigured for all available simulation methods and simulation devices. The new backends can be accessed through the provider interface using the names
"aer_simulator"
"aer_simulator_statevector"
"aer_simulator_stabilizer"
"aer_simulator_density_matrix"
"aer_simulator_matrix_product_state"
"aer_simulator_extended_stabilizer"
"aer_simulator_unitary"
"aer_simulator_superop"
Additional if Aer was installed with GPU support on a compatible system the following GPU backends will also be available
"aer_simulator_statevector_gpu"
"aer_simulator_density_matrix_gpu"
"aer_simulator_unitary_gpu"
For example:
from
qiskit
import
Aer
# Get the GPU statevector simulator backend
backend
=
Aer
.
get_backend
(
'aer_simulator_statevector_gpu'
)
Added a new
norm estimation
method for performing measurements when using the
"extended_stabilizer"
simulation method. This norm estimation method can be used by passing the following options to the
AerSimulator
and
QasmSimulator
backends
simulator
=
QasmSimulator
(
method
=
'extended_stabilizer'
,
extended_stabilizer_sampling_method
=
'norm_estimation'
)
The norm estimation method is slower than the alternative
metropolis
or
resampled_metropolis
options, but gives better performance on circuits with sparse output distributions. See the documentation of the
QasmSimulator
for more information.
Adds instructions for saving the state of the simulator in various formats. These instructions are
qiskit.providers.aer.library.SaveDensityMatrix
qiskit.providers.aer.library.SaveMatrixProductState
qiskit.providers.aer.library.SaveStabilizer
qiskit.providers.aer.library.SaveState
qiskit.providers.aer.library.SaveStatevector
qiskit.providers.aer.library.SaveStatevectorDict
qiskit.providers.aer.library.SaveUnitary
These instructions can be appended to a quantum circuit by using the
save_density_matrix
,
save_matrix_product_state
,
save_stabilizer
,
save_state
,
save_statevector
,
save_statevector_dict
,
save_unitary
circuit methods which are added to
QuantumCircuit
when importing Aer.
See the
qiskit.providers.aer.library
API documentation for details on method compatibility for each instruction.
Note that the snapshot instructions
SnapshotStatevector
,
SnapshotDensityMatrix
,
SnapshotStabilizer
are still supported but will be deprecated in a future release.
Adds
qiskit.providers.aer.library.SaveExpectationValue
and
qiskit.providers.aer.library.SaveExpectationValueVariance
quantum circuit instructions for saving the expectation value
⟨
H
⟩
=
T
r
[
H
ρ
]
\langle H\rangle = Tr[H\rho]
⟨
H
⟩
=
T
r
[
H
ρ
]
, or expectation value and variance
V
a
r
(
H
)
=
⟨
H
2
⟩
−
⟨
H
⟩
2
Var(H) = \langle H^2\rangle - \langle H\rangle^2
Va
r
(
H
)
=
⟨
H
2
⟩
−
⟨
H
⟩
2
, of a Hermitian operator
H
H
H
for the simulator state
ρ
\rho
ρ
. These instruction can be appended to a quantum circuit by using the
save_expectation_value
and
save_expectation_value_variance
circuit methods which is added to
QuantumCircuit
when importing Aer.
Note that the snapshot instruction
SnapshotExpectationValue
, is still supported but will be deprecated in a future release.
Adds
qiskit.providers.aer.library.SaveProbabilities
and
qiskit.providers.aer.library.SaveProbabilitiesDict
quantum circuit instruction for saving all measurement outcome probabilities for Z-basis measurements of the simualtor state. These instruction can be appended to a quantum circuit by using the
save_probabilities
and
save_probabilities_dict
circuit methods which is added to
QuantumCircuit
when importing Aer.
Note that the snapshot instruction
SnapshotProbabilities
, is still supported but will be deprecated in a future release.
Adds
qiskit.providers.aer.library.SaveAmplitudes
and
qiskit.providers.aer.library.SaveAmplitudesSquared
circuit instructions for saving select complex statevector amplitudes, or select probabilities (amplitudes squared) for supported simulation methods. These instructions can be appended to a quantum circuit by using the
save_amplitudes
and
save_amplitudes_squared
circuit methods which is added to
QuantumCircuit
when importing Aer.
Adds instructions for setting the state of the simulators. These instructions must be defined on the full number of qubits in the circuit. They can be applied at any point in a circuit and will override the simulator state with the one specified. Added instructions are
qiskit.providers.aer.library.SetDensityMatrix
qiskit.providers.aer.library.SetStabilizer
qiskit.providers.aer.library.SetStatevector
qiskit.providers.aer.library.SetUnitary
These instruction can be appended to a quantum circuit by using the
set_density_matrix
,
set_stabilizer
,
set_statevector
,
set_unitary
circuit methods which are added to
QuantumCircuit
when importing Aer.
See the
qiskit.providers.aer.library
API documentation for details on method compatibility for each instruction.
Added support for diagonal gates to the
"matrix_product_state"
simulation method.
Added support for the
initialize
instruction to the
"matrix_product_state"
simulation method.
Known Issues
There is a known issue where the simulation of certain circuits with a Kraus noise model using the
"matrix_product_state"
simulation method can cause the simulator to crash. Refer to
#306
for more information.
Upgrade Notes
The minimum version of
Conan
has been increased to 1.31.2. This was necessary to fix a compatibility issue with newer versions of the
urllib3
(which is a dependency of Conan). It also adds native support for AppleClang 12 which is useful for users with new Apple computers.
pybind11
minimum version required is 2.6 instead of 2.4. This is needed in order to support CUDA enabled compilation in Windows.
Cython has been removed as a build dependency.
Removed x90 gate decomposition from noise models that was deprecated in qiskit-aer 0.7. This decomposition is now done by using regular noise model basis gates and the qiskit transpiler.
The following options for the
"extended_stabilizer"
simulation method have changed.
extended_stabilizer_measure_sampling
: This option has been replaced by the options
extended_stabilizer_sampling_method
, which controls how we simulate qubit measurement.
extended_stabilizer_mixing_time
: This option has been renamed as
extended_stabilizer_metropolis_mixing_time
to clarify it only applies to the
metropolis
and
resampled_metropolis
sampling methods.
extended_stabilizer_norm_estimation_samples
: This option has been renamed to
extended_stabilizer_norm_estimation_default_samples
.
One additional option,
extended_stabilizer_norm_estimation_repetitions
has been added, whih controls part of the behaviour of the norm estimation sampling method.
Deprecation Notes
Python 3.6 support has been deprecated and will be removed in a future release. When support is removed you will need to upgrade the Python version you’re using to Python 3.7 or above.
Bug Fixes
Fixes bug with
AerProvider
where options set on the returned backends using
set_options()
were stored in the provider and would persist for subsequent calls to
get_backend()
for the same named backend. Now every call to and
backends()
returns a new instance of the simulator backend that can be configured.
Fixes bug in the error message returned when a circuit contains unsupported simulator instructions. Previously some supported instructions were also being listed in the error message along with the unsupported instructions.
Fixes issue with setting
QasmSimulator
basis gates when using
"method"
and
"noise_model"
options together, and when using them with a simulator constructed using
from_backend()
. Now the listed basis gates will be the intersection of gates supported by the backend configuration, simulation method, and noise model basis gates. If the intersection of the noise model basis gates and simulator basis gates is empty a warning will be logged.
Fix bug where the
"sx"`
gate
SXGate
was not listed as a supported gate in the C++ code, in
StateOpSet
of
matrix_product_state.hp
.
Fix bug where
"csx"
,
"cu2"
,
"cu3"
were incorrectly listed as supported basis gates for the
"density_matrix"
method of the
QasmSimulator
.
Fix bug where parameters were passed incorrectly between functions in
matrix_product_state_internal.cpp
, causing wrong simulation, as well as reaching invalid states, which in turn caused an infinite loop.
Fixes a bug that resulted in
c_if
not working when the width of the conditional register was greater than 64. See
#1077
.
Fixes a bug
#1153
) where noise on conditional gates was always being applied regardless of whether the conditional gate was actually applied based on the classical register value. Now noise on a conditional gate will only be applied in the case where the conditional gate is applied.
Fixes a bug with nested OpenMP flag was being set to true when it shouldn’t be.
Fixes a bug when applying truncation in the matrix product state method of the QasmSimulator.
Fixed issue
#1126
: bug in reporting measurement of a single qubit. The bug occured when copying the measured value to the output data structure.
In MPS, apply_kraus was operating directly on the input bits in the parameter qubits, instead of on the internal qubits. In the MPS algorithm, the qubits are constantly moving around so all operations should be applied to the internal qubits.
When invoking MPS::sample_measure, we need to first sort the qubits to the default ordering because this is the assumption in qasm_controller.This is done by invoking the method move_all_qubits_to_sorted_ordering. It was correct in sample_measure_using_apply_measure, but missing in sample_measure_using_probabilities.
Fixes bug with the
from_backend()
method of the
QasmSimulator
that would set the
local
attribute of the configuration to the backend value rather than always being set to
True
.
Fixes bug in
from_backend()
and
from_backend()
where
basis_gates
was set incorrectly for IBMQ devices with basis gate set
['id', 'rz', 'sx', 'x', 'cx']
. Now the noise model will always have the same basis gates as the backend basis gates regardless of whether those instructions have errors in the noise model or not.
Fixes an issue where the Extended “extended_stabilizer” simulation method would give incorrect results on quantum circuits with sparse output distributions. Refer to
#306
for more information and examples.
Ignis 0.6.0
New Features
The
qiskit.ignis.mitigation.expval_meas_mitigator_circuits()
function has been improved so that the number of circuits generated by the function used for calibration by the CTMP method are reduced from
O
(
n
)
O(n)
O
(
n
)
to
O
(
log
⁡
n
)
O(\log{n})
O
(
lo
g
n
)
(where
n
n
n
is the number of qubits).
Upgrade Notes
The
qiskit.ignis.verification.randomized_benchmarking_seq()
function is now using the upgraded CNOTDihedral class,
qiskit.ignis.verification.CNOTDihedral
, which enables performing CNOT-Dihedral Randomized Benchmarking on more than two qubits.
The python package
retworkx
is now a requirement for installing qiskit-ignis. It replaces the previous usage of
networkx
(which is no longer a requirement) to get better performance.
The
scikit-learn
dependency is no longer required and is now an optional requirement. If you’re using the IQ measurement discriminators (
IQDiscriminationFitter
,
LinearIQDiscriminationFitter
,
QuadraticIQDiscriminationFitter
, or
SklearnIQDiscriminator
) you will now need to manually install scikit-learn, either by running
pip install scikit-learn
or when you’re also installing qiskit-ignis with
pip install qiskit-ignis[iq]
.
Bug Fixes
Fixed an issue in the expectation value method
expectation_value()
, for the error mitigation classes
TensoredExpvalMeasMitigator
and
CTMPExpvalMeasMitigator
if the
qubits
kwarg was not specified it would incorrectly use the total number of qubits of the mitigator, rather than the number of classical bits in the count dictionary leading to greatly reduced performance. Fixed
#561
Fix the
"auto"
method of the
TomographyFitter
,
StateTomographyFitter
, and
ProcessTomographyFitter
to only use
"cvx"
if CVXPY is installed
and
a third-party SDP solver other than SCS is available. This is because the SCS solver has lower accuracy than other solver methods and often returns a density matrix or Choi-matrix that is not completely-positive and fails validation when used with the
qiskit.quantum_info.state_fidelity()
or
qiskit.quantum_info.process_fidelity()
functions.
Aqua 0.9.0
This release officially deprecates the Qiskit Aqua project, in the future (no sooner than 3 months from this release) the Aqua project will have it’s final release and be archived. All the functionality that qiskit-aqua provides has been migrated to either new packages or to other qiskit packages. The application modules that are provided by qiskit-aqua have been split into several new packages:
qiskit-optimization
,
qiskit-nature
,
qiskit-machine-learning
, and
qiskit-finance
. These packages can be installed by themselves (via the standard pip install command, ie
pip install qiskit-nature
) or with the rest of the Qiskit metapackage as optional extras (ie,
pip install 'qiskit[finance,optimization]'
or
pip install 'qiskit[all]'
. The core building blocks for algorithms and the operator flow now exist as part of qiskit-terra at
qiskit.algorithms
and
qiskit.opflow
. Depending on your existing usage of Aqua you should either use the application packages or the new modules in Qiskit Terra.
For more details on how to migrate from using Qiskit Aqua, you can refer to the
migration guide
.
IBM Q Provider 0.12.2
No change