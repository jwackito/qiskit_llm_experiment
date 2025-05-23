Qiskit 0.14 release notes
0.14.0
Terra 0.11.0
Prelude
The 0.11.0 release includes several new features and bug fixes. The biggest change for this release is the addition of the pulse scheduler. This allows users to define their quantum program as a
QuantumCircuit
and then map it to the underlying pulse instructions that will control the quantum hardware to implement the circuit.
New Features
Added 5 new commands to easily retrieve user-specific data from
BackendProperties
:
gate_property
,
gate_error
,
gate_length
,
qubit_property
,
t1
,
t2
,
readout_error
and
frequency
. They return the specific values of backend properties. For example:
from
qiskit
.
test
.
mock
import
FakeOurense
backend
=
FakeOurense
()
properties
=
backend
.
properties
()
gate_property
=
properties
.
gate_property
(
'u1'
)
gate_error
=
properties
.
gate_error
(
'u1'
,
0
)
gate_length
=
properties
.
gate_length
(
'u1'
,
0
)
qubit_0_property
=
properties
.
qubit_property
(
0
)
t1_time_0
=
properties
.
t1
(
0
)
t2_time_0
=
properties
.
t2
(
0
)
readout_error_0
=
properties
.
readout_error
(
0
)
frequency_0
=
properties
.
frequency
(
0
)
Added method
Instruction.is_parameterized()
to check if an instruction object is parameterized. This method returns
True
if and only if instruction has a
ParameterExpression
or
Parameter
object for one of its params.
Added a new analysis pass
Layout2qDistance
. This pass allows to “score” a layout selection, once
property_set['layout']
is set. The score will be the sum of distances for each two-qubit gate in the circuit, when they are not directly connected. This scoring does not consider direction in the coupling map. The lower the number, the better the layout selection is.
For example, consider a linear coupling map
[0]--[2]--[1]
and the following circuit:
qr
=
QuantumRegister
(
2
,
'qr'
)
circuit
=
QuantumCircuit
(qr)
circuit
.
cx
(qr[
0
], qr[
1
])
If the layout is
{qr[0]:0, qr[1]:1}
,
Layout2qDistance
will set
property_set['layout_score'] = 1
. If the layout is
{qr[0]:0, qr[1]:2}
, then the result is
property_set['layout_score'] = 0
. The lower the score, the better.
Added
qiskit.QuantumCircuit.cnot
as an alias for the
cx
method of
QuantumCircuit
. The names
cnot
and
cx
are often used interchangeably now the cx method can be called with either name.
Added
qiskit.QuantumCircuit.toffoli
as an alias for the
ccx
method of
QuantumCircuit
. The names
toffoli
and
ccx
are often used interchangeably now the ccx method can be called with either name.
Added
qiskit.QuantumCircuit.fredkin
as an alias for the
cswap
method of
QuantumCircuit
. The names
fredkin
and
cswap
are often used interchangeably now the cswap method can be called with either name.
The
latex
output mode for
qiskit.visualization.circuit_drawer()
and the
qiskit.circuit.QuantumCircuit.draw()
method now has a mode to passthrough raw latex from gate labels and parameters. The syntax for doing this mirrors matplotlib’s
mathtext mode
syntax. Any portion of a label string between a pair of ‘$’ characters will be treated as raw latex and passed directly into the generated output latex. This can be leveraged to add more advanced formatting to circuit diagrams generated with the latex drawer.
Prior to this release all gate labels were run through a utf8 -> latex conversion to make sure that the output latex would compile the string as expected. This is still what happens for all portions of a label outside the ‘$’ pair. Also if you want to use a dollar sign in your label make sure you escape it in the label string (ie
'\$'
).
You can mix and match this passthrough with the utf8 -> latex conversion to create the exact label you want, for example:
from
qiskit
import
circuit
circ
=
circuit
.
QuantumCircuit
(
2
)
circ
.
h
([
0
,
1
])
circ
.
append
(circuit.
Gate
(name
=
'α_gate'
, num_qubits
=
1
, params
=
[
0
]), [
0
])
circ
.
append
(circuit.
Gate
(name
=
'α_gate$_2$'
, num_qubits
=
1
, params
=
[
0
]), [
1
])
circ
.
append
(circuit.
Gate
(name
=
'\$α\$_gate'
, num_qubits
=
1
, params
=
[
0
]), [
1
])
circ
.
draw
(output
=
'latex'
)
will now render the first custom gate’s label as
α_gate
, the second will be
α_gate
with a 2 subscript, and the last custom gate’s label will be
$α$_gate
.
Add
ControlledGate
class for representing controlled gates. Controlled gate instances are created with the
control(n)
method of
Gate
objects where
n
represents the number of controls. The control qubits come before the controlled qubits in the new gate. For example:
from
qiskit
import
QuantumCircuit
from
qiskit
.
extensions
import
HGate
hgate
=
HGate
()
circ
=
QuantumCircuit
(
4
)
circ
.
append
(hgate.
control
(
3
), [
0
,
1
,
2
,
3
])
print
(circ)
generates:
q_0
:
|
0
>
──■──
│
q_1
:
|
0
>
──■──
│
q_2
:
|
0
>
──■──
┌─┴─┐
q_3
:
|
0
>
┤ H ├
└───┘
Allowed values of
meas_level
parameters and fields can now be a member from the IntEnum class
qiskit.qobj.utils.MeasLevel
. This can be used when calling
execute
(or anywhere else
meas_level
is specified) with a pulse experiment. For example:
from
qiskit
import
QuantumCircuit
,
transpile
,
schedule
,
execute
from
qiskit
.
test
.
mock
import
FakeOpenPulse2Q
from
qiskit
.
qobj
.
utils
import
MeasLevel
,
MeasReturnType
backend
=
FakeOpenPulse2Q
()
qc
=
QuantumCircuit
(
2
,
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
qc_transpiled
=
transpile
(qc, backend)
sched
=
schedule
(qc_transpiled, backend)
execute
(sched, backend, meas_level
=
MeasLevel.CLASSIFIED)
In this above example,
meas_level=MeasLevel.CLASSIFIED
and
meas_level=2
can be used interchangably now.
A new layout selector based on constraint solving is included. CSPLayout models the problem of finding a layout as a constraint problem and uses recursive backtracking to solve it.
cmap16
=
CouplingMap
(
FakeRueschlikon
().
configuration
().coupling_map)
qr
=
QuantumRegister
(
5
,
'q'
)
circuit
=
QuantumCircuit
(qr)
circuit
.
cx
(qr[
0
], qr[
1
])
circuit
.
cx
(qr[
0
], qr[
2
])
circuit
.
cx
(qr[
0
], qr[
3
])
pm
=
PassManager
(
CSPLayout
(cmap16))
circuit_after
=
pm
.
run
(circuit)
print
(pm.property_set[
'layout'
])
Layout
({
1
:
Qubit
(
QuantumRegister
(
5
,
'q'
),
1
),
2
:
Qubit
(
QuantumRegister
(
5
,
'q'
),
0
),
3
:
Qubit
(
QuantumRegister
(
5
,
'q'
),
3
),
4
:
Qubit
(
QuantumRegister
(
5
,
'q'
),
4
),
15
:
Qubit
(
QuantumRegister
(
5
,
'q'
),
2
)
})
The parameter
CSPLayout(...,strict_direction=True)
is more restrictive but it will guarantee there is no need of running
CXDirection
after.
pm
=
PassManager
(
CSPLayout
(cmap16, strict_direction
=
True
))
circuit_after
=
pm
.
run
(circuit)
print
(pm.property_set[
'layout'
])
Layout
({
8
:
Qubit
(
QuantumRegister
(
5
,
'q'
),
4
),
11
:
Qubit
(
QuantumRegister
(
5
,
'q'
),
3
),
5
:
Qubit
(
QuantumRegister
(
5
,
'q'
),
1
),
6
:
Qubit
(
QuantumRegister
(
5
,
'q'
),
0
),
7
:
Qubit
(
QuantumRegister
(
5
,
'q'
),
2
)
})
If the constraint system is not solvable, the layout property is not set.
circuit
.
cx
(qr[
0
], qr[
4
])
pm
=
PassManager
(
CSPLayout
(cmap16))
circuit_after
=
pm
.
run
(circuit)
print
(pm.property_set[
'layout'
])
None
PulseBackendConfiguration (accessed normally as backend.configuration()) has been extended with useful methods to explore its data and the functionality that exists in PulseChannelSpec. PulseChannelSpec will be deprecated in the future. For example:
backend
=
provider
.
get_backend
(backend_name)
config
=
backend
.
configuration
()
q0_drive
=
config
.
drive
(
0
)
# or, DriveChannel(0)
q0_meas
=
config
.
measure
(
0
)
# MeasureChannel(0)
q0_acquire
=
config
.
acquire
(
0
)
# AcquireChannel(0)
config
.
hamiltonian
# Returns a dictionary with hamiltonian info
config
.
sample_rate
()
# New method which returns 1 / dt
PulseDefaults
(accessed normally as
backend.defaults()
) has an attribute,
circuit_instruction_map
which has the methods of CmdDef. The new circuit_instruction_map is an
InstructionScheduleMap
object with three new functions beyond what CmdDef had:
qubit_instructions(qubits) returns the operations defined for the qubits
assert_has(instruction, qubits) raises an error if the op isn’t defined
remove(instruction, qubits) like pop, but doesn’t require parameters
There are some differences from the CmdDef:
__init__
takes no arguments
cmds
and
cmd_qubits
are deprecated and replaced with
instructions
and
qubits_with_instruction
Example:
backend
=
provider
.
get_backend
(backend_name)
inst_map
=
backend
.
defaults
().
circuit_instruction_map
qubit
=
inst_map
.
qubits_with_instruction
(
'u3'
)
[
0
]
x_gate
=
inst_map
.
get
(
'u3'
, qubit, P0
=
np.pi, P1
=
0
, P2
=
np.pi)
pulse_schedule
=
x_gate
(
DriveChannel
(qubit))
A new kwarg parameter,
show_framechange_channels
to optionally disable displaying channels with only framechange instructions in pulse visualizations was added to the
qiskit.visualization.pulse_drawer()
function and
qiskit.pulse.Schedule.draw()
method. When this new kwarg is set to
False
the output pulse schedule visualization will not include any channels that only include frame changes.
For example:
from
qiskit
.
pulse
import
*
from
qiskit
.
pulse
import
library
as
pulse_lib
gp0
=
pulse_lib
.
gaussian
(duration
=
20
, amp
=
1.0
, sigma
=
1.0
)
sched
=
Schedule
()
channel_a
=
DriveChannel
(
0
)
channel_b
=
DriveChannel
(
1
)
sched
+=
Play
(gp0, channel_a)
sched
=
sched
.
insert
(
60
,
ShiftPhase
(
-
1.57
, channel_a))
sched
=
sched
.
insert
(
30
,
ShiftPhase
(
-
1.50
, channel_b))
sched
=
sched
.
insert
(
70
,
ShiftPhase
(
1.50
, channel_b))
sched
.
draw
(show_framechange_channels
=
False
)
A new utility function
qiskit.result.marginal_counts()
is added which allows marginalization of the counts over some indices of interest. This is useful when more qubits are measured than needed, and one wishes to get the observation counts for some subset of them only.
When
passmanager.run(...)
is invoked with more than one circuit, the transpilation of these circuits will run in parallel.
PassManagers can now be sliced to create a new PassManager containing a subset of passes using the square bracket operator. This allow running or drawing a portion of the PassManager for easier testing and visualization. For example let’s try to draw the first 3 passes of a PassManager pm, or run just the second pass on our circuit:
pm
[
0
:
4
].
draw
()
circuit2
=
pm
[
1
].
run
(circuit)
Also now, PassManagers can be created by adding two PassManagers or by directly adding a pass/list of passes to a PassManager.
pm
=
pm1
[
0
]
+
pm2
[
1
:
3
]
pm
+=
[setLayout
,
unroller]
A basic
scheduler
module has now been added to Qiskit. The scheduler schedules an input transpiled
QuantumCircuit
into a pulse
Schedule
. The scheduler accepts as input a
Schedule
and either a pulse
Backend
, or a
CmdDef
which relates circuit
Instruction
objects on specific qubits to pulse Schedules and a
meas_map
which determines which measurements must occur together.
Scheduling example:
from
qiskit
import
QuantumCircuit
,
transpile
,
schedule
from
qiskit
.
test
.
mock
import
FakeOpenPulse2Q
backend
=
FakeOpenPulse2Q
()
qc
=
QuantumCircuit
(
2
,
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
qc_transpiled
=
transpile
(qc, backend)
schedule
(qc_transpiled, backend)
The scheduler currently supports two scheduling policies, as_late_as_possible (
alap
) and as_soon_as_possible (
asap
), which respectively schedule pulse instructions to occur as late as possible or as soon as possible across qubits in a circuit. The scheduling policy may be selected with the input argument
method
, for example:
schedule
(qc_transpiled, backend, method
=
'alap'
)
It is easy to use a pulse
Schedule
within a
QuantumCircuit
by mapping it to a custom circuit instruction such as a gate which may be used in a
QuantumCircuit
. To do this, first, define the custom gate and then add an entry into the
CmdDef
for the gate, for each qubit that the gate will be applied to. The gate can then be used in the
QuantumCircuit
. At scheduling time the gate will be mapped to the underlying pulse schedule. Using this technique allows easy integration with preexisting qiskit modules such as Ignis.
For example:
from
qiskit
import
pulse
,
circuit
,
schedule
from
qiskit
.
pulse
import
pulse_lib
custom_cmd_def
=
pulse
.
CmdDef
()
# create custom gate
custom_gate
=
circuit
.
Gate
(name
=
'custom_gate'
, num_qubits
=
1
, params
=
[])
# define schedule for custom gate
custom_schedule
=
pulse
.
Schedule
()
custom_schedule
+=
pulse_lib
.
gaussian
(
20
,
1.0
,
10
)(pulse.DriveChannel)
# add schedule to custom gate with same name
custom_cmd_def
.
add
(
'custom_gate'
, (
0
,), custom_schedule)
# use custom gate in a circuit
custom_qc
=
circuit
.
QuantumCircuit
(
1
)
custom_qc
.
append
(custom_gate, qargs
=
[
0
])
# schedule the custom gate
schedule
(custom_qc, cmd_def
=
custom_cmd_def, meas_map
=
[[
0
]])
Known Issues
The feature for transpiling in parallel when
passmanager.run(...)
is invoked with more than one circuit is not supported under Windows. See
#2988
for more details.
Upgrade Notes
The
qiskit.pulse.channels.SystemTopology
class was used as a helper class for
PulseChannelSpec
. It has been removed since with the deprecation of
PulseChannelSpec
and changes to
BackendConfiguration
make it unnecessary.
The previously deprecated representation of qubits and classical bits as tuple, which was deprecated in the 0.9 release, has been removed. The use of
Qubit
and
Clbit
objects is the new way to represent qubits and classical bits.
The previously deprecated representation of the basis set as single string has been removed. A list of strings is the new preferred way.
The method
BaseModel.as_dict
, which was deprecated in the 0.9 release, has been removed in favor of the method
BaseModel.to_dict
.
In PulseDefaults (accessed normally as backend.defaults()),
qubit_freq_est
and
meas_freq_est
are now returned in Hz rather than GHz. This means the new return values are 1e9 * their previous value.
dill
was added as a requirement. This is needed to enable running
passmanager.run()
in parallel for more than one circuit.
The previously deprecated gate
UBase
, which was deprecated in the 0.9 release, has been removed. The gate
U3Gate
should be used instead.
The previously deprecated gate
CXBase
, which was deprecated in the 0.9 release, has been removed. The gate
CnotGate
should be used instead.
The instruction
snapshot
used to implicitly convert the
label
parameter to string. That conversion has been removed and an error is raised if a string is not provided.
The previously deprecated gate
U0Gate
, which was deprecated in the 0.9 release, has been removed. The gate
IdGate
should be used instead to insert delays.
Deprecation Notes
The
qiskit.pulse.CmdDef
class has been deprecated. Instead you should use the
qiskit.pulse.InstructionScheduleMap
. The
InstructionScheduleMap
object for a pulse enabled system can be accessed at
backend.defaults().instruction_schedules
.
PulseChannelSpec
is being deprecated. Use
BackendConfiguration
instead. The backend configuration is accessed normally as
backend.configuration()
. The config has been extended with most of the functionality of PulseChannelSpec, with some modifications as follows, where 0 is an exemplary qubit index:
pulse_spec
.
drives
[
0
]
-> config
.
drive
(
0
)
pulse_spec
.
measures
[
0
]
-> config
.
measure
(
0
)
pulse_spec
.
acquires
[
0
]
-> config
.
acquire
(
0
)
pulse_spec
.
controls
[
0
]
-> config
.
control
(
0
)
Now, if there is an attempt to get a channel for a qubit which does not exist for the device, a
BackendConfigurationError
will be raised with a helpful explanation.
The methods
memoryslots
and
registerslots
of the PulseChannelSpec have not been migrated to the backend configuration. These classical resources are not restrained by the physical configuration of a backend system. Please instantiate them directly:
pulse_spec
.
memoryslots
[
0
]
->
MemorySlot
(
0
)
pulse_spec
.
registerslots
[
0
]
->
RegisterSlot
(
0
)
The
qubits
method is not migrated to backend configuration. The result of
qubits
can be built as such:
[q
for
q
in
range
(backend.
configuration
().n_qubits)
]
Qubit
within
pulse.channels
has been deprecated. They should not be used. It is possible to obtain channel <=> qubit mappings through the BackendConfiguration (or backend.configuration()).
The function
qiskit.visualization.circuit_drawer.qx_color_scheme()
has been deprecated. This function is no longer used internally and doesn’t reflect the current IBM QX style. If you were using this function to generate a style dict locally you must save the output from it and use that dictionary directly.
The Exception
TranspilerAccessError
has been deprecated. An alternative function
TranspilerError
can be used instead to provide the same functionality. This alternative function provides the exact same functionality but with greater generality.
Buffers in Pulse are deprecated. If a nonzero buffer is supplied, a warning will be issued with a reminder to use a Delay instead. Other options would include adding samples to a pulse instruction which are (0.+0.j) or setting the start time of the next pulse to
schedule.duration + buffer
.
Passing in
sympy.Basic
,
sympy.Expr
and
sympy.Matrix
types as instruction parameters are deprecated and will be removed in a future release. You’ll need to convert the input to one of the supported types which are:
int
float
complex
str
np.ndarray
Bug Fixes
The Collect2qBlocks and CommutationAnalysis passes in the transpiler had been unable to process circuits containing Parameterized gates, preventing Parameterized circuits from being transpiled at optimization_level 2 or above. These passes have been corrected to treat Parameterized gates as opaque.
The align_measures function had an issue where Measure stimulus pulses weren’t properly aligned with Acquire pulses, resulting in an error. This has been fixed.
Uses of
numpy.random.seed
have been removed so that calls of qiskit functions do not affect results of future calls to
numpy.random
Fixed race condition occurring in the job monitor when
job.queue_position()
returns
None
.
None
is a valid return from
job.queue_position()
.
Backend support for
memory=True
now checked when that kwarg is passed.
QiskitError
results if not supported.
When transpiling without a coupling map, there were no check in the amount of qubits of the circuit to transpile. Now the transpile process checks that the backend has enough qubits to allocate the circuit.
Other Notes
The
qiskit.result.marginal_counts()
function replaces a similar utility function in qiskit-ignis
qiskit.ignis.verification.tomography.marginal_counts()
, which will be deprecated in a future qiskit-ignis release.
All sympy parameter output type support have been been removed (or deprecated as noted) from qiskit-terra. This includes sympy type parameters in
QuantumCircuit
objects, qasm ast nodes, or
Qobj
objects.
Aer 0.3
No Change
Ignis 0.2
No Change
Aqua 0.6
No Change
IBM Q Provider 0.4
Prelude
The 0.4.0 release is the first release that makes use of all the features of the new IBM Q API. In particular, the
IBMQJob
class has been revamped in order to be able to retrieve more information from IBM Q, and a Job Manager class has been added for allowing a higher-level and more seamless usage of large or complex jobs. If you have not upgraded from the legacy IBM Q Experience or QConsole yet, please ensure to revisit the release notes for IBM Q Provider 0.3 (Qiskit 0.11) for more details on how to make the transition. The legacy accounts will no longer be supported as of this release.
New Features
Job modifications
The
IBMQJob
class has been revised, and now mimics more closely to the contents of a remote job along with new features:
You can now assign a name to a job, by specifying
IBMQBackend.run(..., job_name='...')
when submitting a job. This name can be retrieved via
IBMQJob.name()
and can be used for filtering.
Jobs can now be shared with other users at different levels (global, per hub, group or project) via an optional
job_share_level
parameter when submitting the job.
IBMQJob
instances now have more attributes, reflecting the contents of the remote IBM Q jobs. This implies that new attributes introduced by the IBM Q API will automatically and immediately be available for use (for example,
job.new_api_attribute
). The new attributes will be promoted to methods when they are considered stable (for example,
job.name()
).
.error_message()
returns more information on why a job failed.
.queue_position()
accepts a
refresh
parameter for forcing an update.
.result()
accepts an optional
partial
parameter, for returning partial results, if any, of jobs that failed. Be aware that
Result
methods, such as
get_counts()
will raise an exception if applied on experiments that failed.
Please note that the changes include some low-level modifications of the class. If you were creating the instances manually, note that:
the signature of the constructor has changed to account for the new features.
the
.submit()
method can no longer be called directly, and jobs are expected to be submitted either via the synchronous
IBMQBackend.run()
or via the Job Manager.
Job Manager
A new Job Manager (
IBMQJobManager
) has been introduced, as a higher-level mechanism for handling jobs composed of multiple circuits or pulse schedules. The Job Manager aims to provide a transparent interface, intelligently splitting the input into efficient units of work and taking full advantage of the different components. It will be expanded on upcoming versions, and become the recommended entry point for job submission.
Its
.run()
method receives a list of circuits or pulse schedules, and returns a
ManagedJobSet instance
, which can then be used to track the statuses and results of these jobs. For example:
from
qiskit
.
providers
.
ibmq
.
managed
import
IBMQJobManager
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
import
IBMQ
from
qiskit
.
compiler
import
transpile
provider
=
IBMQ
.
load_account
()
backend
=
provider
.
backends
.
ibmq_ourense
circs
=
[]
for
_
in
range
(
1000000
):
circs
.
append
(
random_circuit
(
2
,
2
))
transpile
(circs, backend
=
backend)
# Farm out the jobs.
jm
=
IBMQJobManager
()
job_set
=
jm
.
run
(circs, backend
=
backend, name
=
'foo'
)
job_set
.
statuses
()
# Gives a list of job statuses
job_set
.
report
()
# Prints detailed job information
results
=
job_set
.
results
()
counts
=
results
.
get_counts
(
5
)
# Returns data for experiment 5
provider.backends modifications
The
provider.backends
member, which was previously a function that returned a list of backends, has been promoted to a service. This implies that it can be used both in the previous way, as a
.backends()
method, and also as a
.backends
attribute with expanded capabilities:
it contains the existing backends from that provider as attributes, which can be used for autocompletion. For example:
my_backend
=
provider
.
get_backend
(
'ibmq_qasm_simulator'
)
is equivalent to:
my_backend
=
provider
.
backends
.
ibmq_qasm_simulator
the
provider.backends.jobs()
and
provider.backends.retrieve_job()
methods can be used for retrieving provider-wide jobs.
Other changes
The
backend.properties()
function now accepts an optional
datetime
parameter. If specified, the function returns the backend properties closest to, but older than, the specified datetime filter.
Some
warnings
have been toned down to
logger.warning
messages.