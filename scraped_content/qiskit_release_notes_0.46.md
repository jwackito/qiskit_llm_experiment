Qiskit 0.46 release notes
0.46.3
Prelude
Qiskit 0.46.3 is a minor bugfix and backport release for the 0.46 series. It is also the last release of the 0.46 minor version, marking its end-of-life.
Bug Fixes
Fixed a missing decorator in
C3SXGate
that made it fail if
Gate.to_matrix()
was called. The gate matrix is now return as expected.
The
QuantumCircuit.parameters
attribute will now correctly be empty when using
QuantumCircuit.copy_empty_like()
on a parametric circuit. Previously, an internal cache would be copied over without invalidation. Fix
#12617
.
Fix the
SolovayKitaev
transpiler pass when loading basic approximations from an exising
.npy
file. Previously, loading a stored approximation which allowed for further reductions (e.g. due to gate cancellations) could cause a runtime failure. Additionally, the global phase difference of the U(2) gate product and SO(3) representation was lost during a save-reload procedure. Fixes
Qiskit/qiskit#12576
.
The constructor
GenericBackendV2
was allowing to create malformed backends because it accepted basis gates that couldn’t be allocated in the backend size . That is, a backend with a single qubit should not accept a basis with two-qubit gates.
Previously,
DAGCircuit.replace_block_with_op()
allowed to place an
n
-qubit operation onto a block of
m
qubits, leaving the DAG in an invalid state. This behavior has been fixed, and the attempt will raise a
DAGCircuitError
.
Other Notes
This release extends the constraints.txt file with a complete list of pinned version numbers of Qiskit 0.46.3 dependencies. As this release marks the end-of-life of the 0.46 version, this ensures a reproducible installation environment for it going forward based on the version specifications in constraints.txt.
0.46.2
Prelude
Qiskit 0.46.2 is a minor bug-fix and backport release for the 0.46 series.
New Features
This release of Qiskit finalizes support for NumPy 2.0. Qiskit will continue to support both Numpy 1.x and 2.x for the foreseeable future.
Bug Fixes
Fixed an issue with the
circuit_drawer()
or
QuantumCircuit.draw()
when using the
mpl
output option where the program would hang if the circuit being drawn had a ControlFlow operation in it and the
fold
option was set to -1 (meaning no fold). Fixed
#12012
.
The
EvolvedOperatorAnsatz
now correctly handles the case where the operators argument is an empty list. Previously, this would result in an error.
From now on,
EvolvedOperatorAnsatz
will not have any qregs when thera are zero qubits, instead of having a
QuantumRegister
instance with zero qubits. This behavior aligns more consistently with its superclass
QuantumCircuit
.
The method
Instruction.repeat()
now moves a set
condition
to the outer returned
Instruction
and leave the inner gates of its definition unconditional. Previously, the method would leave
ClassicalRegister
instances within the inner definition, which was an invalid state, and would manifest itself as seemingly unrelated bugs later, such as during transpilation or export. Fixed
#11935
.
Fixed a floating-point imprecision when scaling certain pulse units between seconds and nanoseconds. If the pulse was symbolically defined, an unnecessary floating-point error could be introduced by the scaling for certain builds of
symengine
, which could manifest in unexpected results once the symbols were fully bound. See
#12392
.
Fixed a bug in
qiskit.visualization.pulse_v2.interface.draw()
that didn’t draw pulse schedules when the draw function was called with a
BackendV2
argument. Because the V2 backend doesn’t report hardware channel frequencies, the generated drawing will show ‘no freq.’ below each channel label.
The
VF2Layout
pass would raise an exception when provided with a
Target
instance without connectivity constraints. This would be the case with targets from Aer 0.13. The issue is now fixed.
The default
init
plugin was not properly raising a
TranspilerError
when called with an invalid optimization level.
PassManager.run()
will no longer waste time serializing itself when given multiple inputs if it is only going to work in serial.
The OpenQASM 2.0 parser (
qasm2.load()
and
qasm2.loads()
) can now evaluate gate-angle expressions including integer operands that would overflow the system-size integer. These will be evaluated in a double-precision floating-point context, just like the rest of the expression always has been. Beware: an arbitrarily large integer will not necessarily be exactly representable in double-precision floating-point, so there is a chance that however the circuit was generated, it had already lost all numerical precision modulo
2
π
2\pi
2
π
.
0.46.1
Prelude
Qiskit 0.46.1 is a minor bugfix release for the 0.46 series.
Bug Fixes
Fixed an issue with
convert_to_target()
where the converter would incorrectly ignore control flow instructions if they were specified in the
BackendConfiguration.supported_instructions
attribute, which is the typical location that control flow instructions are specified in a
BackendConfiguration
object. Fixed
#11872
.
Calling
EquivalenceLibrary.set_entry()
will now correctly update the internal graph object of the library. Previously, the metadata would be updated, but the graph structure would be unaltered, meaning that users like
BasisTranslator
would still use the old rules. Fixed
#11958
.
BasePassManager.run()
will no longer leak the previous
PropertySet
into new workflows when called more than once. Previously, the same
PropertySet
as before would be used to initialize follow-on runs, which could mean that invalid property information was being given to tasks. The behavior now matches that of Qiskit 0.44. Fixed
#11784
.
Updated properties and configuration information of the
FakeOpenPulse2Q
backend. Missing gate properties were added for some gates defined in the pulse defaults so that the gates defined in the two locations are consistent.
The monitoring tools module
qiskit.tools.monitor
(included in the now deprecated module
qiskit.tools
) has been updated to work as expected. The function
job_monitor()
now works with
Job
instances. The functions
backend_overview()
and
backend_monitor()
should now work as expected.
InstructionDurations.from_backend()
now returns an instance of any subclass of
InstructionDurations
instead of the base class.
0.46.0
Prelude
The 0.46.0 release is the final minor version release for the 0.x series. This release primarily adds new deprecation warnings for API changes coming in the future major version release 1.0.0. It is fully compatible with the Qiskit 0.45.x releases. It is strongly recommended that you upgrade from 0.45.x to 0.46.0 so that you’re able to see the warnings about which interfaces will change with Qiskit 1.0.0.
The 0.46.x release series will continue to be supported and recieve bugfix and security fixes via patch releases for 6 months after this release. For more details on the release schedule and support cycle see:
start/install#qiskit-versioning
which documents the release schedule in more detail.
Note
If your project depends on Qiskit, it may rely on functionality that will no longer be supported in Qiskit 1.0.0. For this reason, we recommend that you proactively cap your supported version to
<1.0
. Qiskit 1.0.0 is scheduled to release approximately two weeks after Qiskit 0.46.0, on 2024-02-15, and might not yet be available when you read this message.
The packaging structure of Qiskit is changing in Qiskit 1.0, and unfortunately the changed requirements cannot be fully communicated to
pip
, especially if
pip install --upgrade
commands are run after the environment has been initially configured. All versions of Qiskit prior to 1.0 (including this one) have an installation conflict with Qiskit 1.0 that
pip
will not resolve.
If
import qiskit
raises an
ImportError
for you, your environment is in an invalid state, and versions of Qiskit 0.45/0.46 and 1.0 are both reachable, which will result in subtly broken code. You will need to create a new virtual environment, and ensure that
only
one of the two versions are installed. In particular, if you are intending to install Qiskit 1.0, you must have no packages that depend on
qiskit-terra
installed; these packages are incompatible with Qiskit 1.0 and must be updated. If you are intending to install Qiskit 0.45 or 0.46, you must ensure that you have nothing attempting to install
qiskit>=1.0
.
If you develop a library based on Qiskit and you still have a dependency on
qiskit-terra
, you should urgently release a new package that depends only on
qiskit
. Since version 0.44, the
qiskit
package contained only the
qiskit-terra
compiler core (the component that is now simply called “Qiskit”), so if your minimum version is
0.44
, you can safely switch a
qiskit-terra>=0.44
dependency to
qiskit>=0.44
with no change in what will be installed. For more detail and recommendations for testing and preparation, see the
section for developers of the migration guide
.
New Features
A new function,
qs_decomposition()
, has been added to
qiskit.synthesis
. This function allows to apply the Quantum Shannon Decomposition of arbitrary unitaries.
A new
qiskit.providers.basic_provider
module has been introduced to replace
qiskit.providers.basicaer
. This module contains provider tools that mirror those of the
BasicAer
provider and offers a single, non-efficient, statevector-based simulator:
BasicSimulator
. This simulator is based on the
BackendV2
interface and is exclusively intended for testing and simple prototyping, for more advanced simulation capabilities, please refer to the
qiskit-aer
package. See the
BasicAer
deprecation note for migration guidelines.
The
Target
interface and transpiler pipeline now support target definitions with
num_qubits=None
. This is to allow the creation of
Target
-based simulators with a flexible number of qubits. A target with
num_qubits=None
will exclusively contain global instructions (with
qargs=None
) and when given to the transpiler, it is expected that the transpiler will not resize the circuit. This change in the
Target
requires future transpiler passes to account for the case where
target.num_qubits is None
.
A new class,
GenericBackendV2
has been added to the
qiskit.providers.fake_provider
module. This class is configurable, and builds a
BackendV2
instance that can run locally (in the spirit of fake backends). Users can configure the number of qubits, basis gates, coupling map, ability to run dynamic circuits (control flow instructions), instruction calibrations and dtm of the backend without having to deal with manual target construction. Qubit and gate properties are generated by randomly sampling from default ranges. The seed for this random generation can be fixed to ensure the reproducibility of the backend output. It’s important to note that this backend only supports gates in the standard library. If you need a more flexible backend, there is always the option to directly instantiate a
Target
object to use for transpilation.
Example usage 1:
from
qiskit
import
QuantumCircuit
,
transpile
from
qiskit
.
providers
.
fake_provider
import
GenericBackendV2
# Create a simple circuit
circuit
=
QuantumCircuit
(
3
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
cx
(
0
,
2
)
circuit
.
measure_all
()
circuit
.
draw
(
'mpl'
)
# Define backend with 3 qubits
backend
=
GenericBackendV2
(num_qubits
=
3
)
# Transpile and run
transpiled_circuit
=
transpile
(circuit, backend)
result
=
backend
.
run
(transpiled_circuit).
result
()
Example usage 2:
from
qiskit
import
QuantumCircuit
,
ClassicalRegister
,
transpile
from
qiskit
.
providers
.
fake_provider
import
GenericBackendV2
# Create a circuit with classical control
creg
=
ClassicalRegister
(
19
)
qc
=
QuantumCircuit
(
25
)
qc
.
add_register
(creg)
qc
.
h
(
0
)
for
i
in
range
(
18
):
qc
.
cx
(
0
, i
+
1
)
for
i
in
range
(
18
):
qc
.
measure
(i, creg[i])
qc
.
ecr
(
20
,
21
).
c_if
(creg,
0
)
# Define backend with custom basis gates
# and control flow instructions
backend
=
GenericBackendV2
(
num_qubits
=
25
,
basis_gates
=
[
"ecr"
,
"id"
,
"rz"
,
"sx"
,
"x"
],
control_flow
=
True
)
#Transpile
transpiled_qc
=
transpile
(qc, backend)
Note
The noise properties generated by these class do not mimic any concrete quantum device, and should not be used to measure concrete backend behaviors. They are “reasonable defaults” that can be used to test general backend-interfacing functionality. For a more accurate simulation of existing devices, you can manually build a noise model from the real backend using the functionality offered in
qiskit-aer
.
Upgrade Notes
The minimum version required for
symengine
was bumped to >=0.11. This enabled removing workarounds from
ParameterExpression.is_real()
to handle a bug in earlier releases of
symengine
.
Deprecation Notes
The
ScheduleBlock.scoped_parameters()
and
ScheduleBlock.search_parameters()
methods have been deprecated. These methods produce
Parameter
objects with names modified to indicate pulse scoping. The original intention of the methods was that these objects would still link to the original unscoped
Parameter
objects. However, the modification of the name breaks the link so that assigning using the scoped version does not work. See
#11654
for more context.
Passing a
QuasiDistribution
,
ProbDistribution
, or a distribution dictionary in for the
data
argument of the
plot_histogram()
visualization function is now deprecated. Support for doing this will be removed in the Qiskit 1.0 release. If you would like to plot a histogram from a
QuasiDistribution
,
ProbDistribution
, or a distribution dictionary you should use the
plot_distribution()
function instead.
The
qiskit-terra
Python package is deprecated and will no longer receive updates starting in Qiskit 1.0.0. If you’re installing
qiskit-terra
by itself this will no longer be updated for Qiskit>=1.0.0. If you’re running qiskit without the
qiskit
package a
FutureWarning
will be emitted on import of
qiskit
to indicate you’re not using the
qiskit
package.
Use of the
qiskit.Aer
object is deprecated and will be removed in Qiskit 1.0. You should instead use the same object from the
qiskit_aer
namespace, which is a drop-in replacement.
Importing from
qiskit.providers.aer
is deprecated and will stop working in Qiskit 1.0. You should instead import from
qiskit_aer
, which is a drop-in replacement.
Running pulse jobs on backends from
qiskit.providers.fake_provider
is deprecated, and all support will be removed in Qiskit 1.0. This is due to Qiskit Aer removing its simulation functionality for such jobs. For low-level Hamiltonian-simulation workloads, consider using a specialised library such as
Qiskit Dynamics
.
The
qiskit.transpiler.synthesis
module is deprecated and will be removed in Qiskit 1.0. The following objects have been moved:
qiskit.transpiler.synthesis.aqc
has been moved to
qiskit.synthesis.unitary.aqc
(except of
qiskit.synthesis.unitary.aqc.AQCSynthesisPlugin
).
qiskit.synthesis.unitary.aqc.AQCSynthesisPlugin
has been moved to
qiskit.transpiler.passes.synthesis.AQCSynthesisPlugin
.
qiskit.transpiler.synthesis.graysynth()
has been moved to
qiskit.synthesis.synth_cnot_phase_aam()
.
qiskit.transpiler.synthesis.cnot_synth()
has been moved to
qiskit.synthesis.synth_cnot_count_full_pmh()
.
The
qiskit.tools.jupyter
module has been deprecated and will be removed in Qiskit 1.0.0. This module is deprecated because the functionality in this module is tied to the legacy
qiskit-ibmq-provider
package which is no longer supported and also only supported
BackendV1
. If you’re using this functionality currently, similar jupyter tools exist in the
qiskit-ibm-provider
package which can be used instead.
The
qiskit.tools.monitor
module has been deprecated and will be removed in Qiskit 1.0.0. This module is deprecated because the functionality in this module is tied to the legacy
qiskit-ibmq-provider
package which is no longer supported and also only supported
BackendV1
.
The
qiskit.tools.visualization
module has been deprecated and will be removed in Qiskit 1.0.0. This module was a legacy redirect from the original location of Qiskit’s visualization module and was moved to
qiskit.visualization
in Qiskit 0.8.0. If you’re still using this path you can just update your imports from
qiskit.tools.visualization
to
qiskit.visualization
.
The
qiskit.tools.events
module and the
progressbar()
utility it exposed has been deprecated and will be removed in the Qiskit 1.0.0 release. This module’s functionality was not widely used and better covered by dedicated packages such as
tqdm
.
The
qiskit.tools
module has been deprecated and will be removed in Qiskit 1.0.0. Except as noted in the release notes above for specific submodules (
qiskit.tools.jupyter
,
qiskit.tools.monitor
,
qiskit.tools.events
and
qiskit.tools.visualization
) the functionality in this module have been migrated to
qiskit.utils
. If you’re using any functionality in this module you can update your imports from
qiskit.tools
to
qiskit.utils
.
The module
qiskit.test
is deprecated. This module contains tooling and helpers for internal Qiskit testing, and most of its functionality had been moved or is not used in Qiskit anymore. In practice, the module was never meant to be used externally. If any of the code in the module is absolutely necessary beyond Qiskit, consider copying that code out into your own test infrastructure.
The
qiskit.quantum_info.synthesis
module is deprecated and will be removed in Qiskit 1.0.0. The following objects have been moved to
qiskit.synthesis
:
OneQubitEulerDecomposer
has been moved to
qiskit.synthesis.one_qubit
TwoQubitBasisDecomposer
has been moved to
qiskit.synthesis.two_qubits
XXDecomposer
has been moved to
qiskit.synthesis.two_qubits
two_qubit_cnot_decompose()
has been moved to
qiskit.synthesis.two_qubits
The class
Quaternion
has been migrated from
qiskit.quantum_info.synthesis
to
qiskit.quantum_info
. This move has not affected the usual import path of the class, but accessing it via the
qiskit.quantum_info.synthesis
is now deprecated.
This function is deprecated and will be removed in Qiskit 1.0.0:
cnot_rxx_decompose()
The legacy OpenQASM 2 parser module previously present in
qiskit.qasm
has been deprecated. It will be removed in the Qiskit 1.0.0 release. The legacy OpenQASM 2 parser has been superseded by the
qiskit.qasm2
module which provides a faster more correct parser for OpenQASM 2.
The
qiskit.converters.ast_to_dag
function has been deprecated and will be removed in the Qiskit 1.0.0 release. It previously was used to convert the abstract syntax tree generated by the legacy OpenQASM 2 parser (in the
qiskit.qasm
module which has been deprecated) and convert that directly to a
DAGCircuit
. As the legacy OpenQASM 2 parser has been deprecated this function will no longer serves a purpose after the legacy parser is removed. If you were previously using this, you can instead parse your OpenQASM 2 files into a
QuantumCircuit
using the
QuantumCircuit.from_qasm_file()
or
QuantumCircuit.from_qasm_str()
constructor methods and then converting that
QuantumCircuit
into a
DAGCircuit
with
circuit_to_dag()
.
The
QuantumCircuit.qasm()
method used to generate a OpenQASM 2 representation of the
QuantumCircuit
object has been deprecated and will be removed in the Qiskit 1.0.0 release. The
qasm2.dump()
or
qasm2.dumps()
functions which provide similar functionality should be used instead. If you were using the
QuantumCircuit.qasm()
method to generate pygments formatted output you should instead look at the standalone
openqasm-pygments
package to provide this functionality (as
qasm2.dump()
and
qasm2.dumps()
do not provide pygments colored output).
The
ParametricPulse
base class and pulses are now deprecated, and will be removed in Qiskit 1.0. This includes:
ParametricPulse
Constant
Drag
Gaussian
GaussianSquare
The class has been superseded by
SymbolicPulse
and the corresponding pulse library.
SymbolicPulse
provides better performance, flexibility and QPY support.
The
NoiseAdaptiveLayout
transpiler pass and the corresponding
"noise_adaptive"
layout stage plugin have been deprecated and will be removed in the 1.0.0 release. This pass has been largely superseded by
VF2Layout
and
VF2PostLayout
which will set a layout based on the reported noise characteristics of a backend.
The
CrosstalkAdaptiveSchedule
transpiler pass has been deprecated and will be removed in the 1.0.0 release. This pass was not usable any longer because its internal operation was dependent on custom properties being set in the
BackendProperties
payload of a
BackendV1
instance. As no backends are setting these fields the pass has been deprecated.
The
qiskit.visualization.qcstyle
module is now deprecated and will be removed in the Qiskit 1.0.0 release. Instead you should use
qiskit.visualization.circuit.qcstyle
as direct replacement.
Injecting circuit gate operations into the pulse builder context is now deprecated. The deprecation affects the following functions:
call_gate()
,
cx()
,
u1()
,
u2()
,
u3()
,
x()
As well as input arguments of type
QuantumCircuit
type in
call()
.
If you still wish to inject backend calibrated schedules, you can use following pattern instead of calling gate commands.
from
qiskit
.
providers
.
fake_provider
import
GenericBackendV2
from
qiskit
import
pulse
backend
=
GenericBackendV2
(num_qubits
=
5
)
sched
=
backend
.
target
[
'x'
]
[(qubit
,
)]
.
calibration
with
pulse
.
build
()
as
only_pulse_scheds
:
pulse
.
call
(sched)
Similarly,
QuantumCircuit
can be injected in the builder context by manually transpiling and scheduling the object.
from
math
import
pi
from
qiskit
.
compiler
import
schedule
,
transpile
qc
=
QuatumCircuit
(
2
)
qc
.
rz
(pi
/
2
,
0
)
qc
.
sx
(
0
)
qc
.
rz
(pi
/
2
,
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
qc_t
=
transpile
(qc, backend)
sched
=
schedule
(qc_t, backend)
with
pulse
.
build
()
as
only_pulse_scheds
:
pulse
.
call
(sched)
In any case we now recommend to write a minimum pulse program with the builder and attach it to
QuantumCircuit
via the
QuantumCircuit.add_calibration()
method as a microcode of a gate instruction, rather than writing the entire program with the pulse model.
The following arguments in
build()
have also been deprecated:
default_transpiler_settings
default_circuit_scheduler_settings
Together with the functions:
active_transpiler_settings()
active_circuit_scheduler_settings()
transpiler_settings()
circuit_scheduler_settings()
The following tools in
qiskit.utils
have been deprecated:
Utils in
qiskit.utils.arithmetic
Utils in
qiskit.utils.circuit_utils
Utils in
qiskit.utils.entangler_map
Utils in
qiskit.utils.name_unnamed_args
These functions were used exclusively in the context of
qiskit.algorithms
and
qiskit.opflow
, and will be removed following the removals of
qiskit.algorithms
and
qiskit.opflow
in Qiskit 1.0.
The
qiskit.providers.fake_provider
module has been migrated to the
qiskit-ibm-runtime
Python package. For this reason, the following elements in the
qiskit.providers.fake_provider
have been deprecated as of Qiskit 0.46 and will be removed in Qiskit 1.0:
qiskit.providers.fake_provider.FakeProvider
qiskit.providers.fake_provider.FakeProviderForBackendV2
qiskit.providers.fake_provider.FakeProviderFactory
qiskit.providers.fake_provider.fake_backends.FakeBackendV2
any fake backend contained in
qiskit.providers.fake_provider.backends
(accessible through the provider)
qiskit.providers.fake_provider.FakeQasmSimulator
qiskit.providers.fake_provider.FakeJob
qiskit.providers.fake_provider.FakeQobj
Migration example to the new fake provider:
# Legacy path
from
qiskit
.
providers
.
fake_provider
import
FakeProvider
,
FakeSherbrooke
backend1
=
FakeProvider
().
get_backend
(
"fake_ourense"
)
backend2
=
FakeSherbrooke
()
# New path
# run "pip install qiskit-ibm-runtime"
from
qiskit_ibm_runtime
.
fake_provider
import
FakeProvider
,
FakeSherbrooke
backend1
=
FakeProvider
().
get_backend
(
"fake_ourense"
)
backend2
=
FakeSherbrooke
()
Additionally, the following fake backends designed for special testing purposes have been superseded by the new
GenericBackendV2
class, and are also deprecated as of Qiskit 0.46:
qiskit.providers.fake_provider.fake_backend_v2.FakeBackendV2
qiskit.providers.fake_provider.fake_backend_v2.FakeBackendV2LegacyQubitProps
qiskit.providers.fake_provider.fake_backend_v2.FakeBackend5QV2
qiskit.providers.fake_provider.fake_backend_v2.FakeBackendSimple
Migration example to the new
GenericBackendV2
class:
# Legacy path
from
qiskit
.
providers
.
fake_provider
import
FakeBackend5QV2
backend
=
FakeBackend5QV2
()
# New path
from
qiskit
.
providers
.
fake_provider
import
GenericBackendV2
backend
=
GenericBackendV2
(num_qubits
=
5
)
# note that this class will generate 5q backend with generic
# properties that serves the same purpose as FakeBackend5QV2
# but will generate different results
The
qiskit.extensions
module is now deprecated. It had been pending deprecation since the Qiskit 0.45 release. Most objects have been moved to
qiskit.circuit.library
, including:
DiagonalGate
,
HamiltonianGateGate
,
Initialize
,
Isometry
,
MCGupDiag
,
UCGate
,
UCPauliRotGate
,
UCRXGate
,
UCRYGate
,
UCRZGate
,
UnitaryGate
.
With the deprecation of the objects, the following circuit methods have also been deprecated:
QuantumCircuit.diagonal
,
QuantumCircuit.hamiltonian
,
QuantumCircuit.isometry
and
QuantumCircuit.iso
,
QuantumCircuit.uc
,
QuantumCircuit.ucrx
,
QuantumCircuit.ucry
,
QuantumCircuit.ucrz
.
Qiskit’s
execute()
function is deprecated. This function served as a high-level wrapper around transpiling a circuit with some transpile options and running it on a backend with some run options. To do the same thing, you can explicitly use the
transpile()
function (with appropriate transpile options) followed by
backend.run()
(with appropriate run options).
For example, instead of running:
from
qiskit
import
execute
job
=
execute
(circuit, backend)
you can run:
from
qiskit
import
transpile
new_circuit
=
transpile
(circuit, backend)
job
=
backend
.
run
(new_circuit)
Alternatively, the
Sampler
primitive is semantically equivalent to the deprecated
execute()
function. The class
BackendSampler
is a generic wrapper for backends that do not support primitives:
from
qiskit
.
primitives
import
BackendSampler
sampler
=
BackendSampler
(backend)
job
=
sampler
.
run
(circuit)
Implicit conversion from a dense
BaseOperator`
to a
SparsePauliOp
in
Estimator
observable arguments is deprecated as of Qiskit 0.46 and will be removed in Qiskit 1.0. You should explicitly convert to a
SparsePauliOp
using
SparsePauliOp.from_operator()
instead.
The discrete pulse library is now deprecated and will be removed in a future release. This includes:
constant()
zero()
square()
sawtooth()
triangle()
cos()
sin()
gaussian()
gaussian_deriv()
sech()
sech_deriv()
gaussian_square()
drag()
Instead, use the corresponding
SymbolicPulse
, with
get_waveform()
. For example, instead of
pulse.gaussian(100,0.5,10)
use
pulse.Gaussian(100,0.5,10).get_waveform()
.
Note that the phase of both
Sawtooth
and
Square
is defined such that a phase of
2
p
i
2\\pi
2
p
i
shifts by a full cycle, contrary to the discrete counterpart. Also note that complex amplitude support is deprecated in the symbolic pulse library - use
float
,
amp
and
angle
instead.
The
ConfigurableFakeBackend
class, which has mainly been used for internal testing, is now deprecated. It will be removed in the Qiskit 1.0.0 release. Instead, you can use the
GenericBackendV2
class to build a similar backend for testing.
Loading library
ScalableSymbolicPulse
objects with complex
amp
parameter from qpy files of version 5 or lower (Qiskit Terra < 0.23.0) is now deprecated. Following the removal in Qiskit 1.0.0, complex
amp
will be automatically converted to float (
amp
,
angle
). The change applies to the pulses:
Constant
Drag
Gaussian
GaussianSquare
The
qiskit.providers.basicaer
module and all of its classes are deprecated from Qiskit 0.46 onwards. Their use should be replaced with the
qiskit.quantum_info
module and the new
qiskit.providers.basic_provider
module.
The migration from using
qiskit.providers.basicaer
to
qiskit.providers.basic_provider
can be performed as follows:
Migrate
from
|
Replace
with
------------------------------------------------------------------------------
:
mod
:
`
.
basicaer`
|
:
mod
:
`
.
basic_provider`
:
class
:
`
.
BasicAerProvider`
|
:
class
:
`
.
BasicProvider`
:
class
:
`
.
BasicAerJob`
|
:
class
:
`
.
BasicProviderJob`
:
class
:
`
.
QasmSimulatorPy`
|
:
class
:
`
.
BasicSimulator`
:
class
:
`
.
UnitarySimulatorPy`
|
use
:
class
:
`
~
.
quantum_info
.
Operator`
:
class
:
`
.
StatevectorSimulatorPy`
|
use
:
class
:
`
~
.
quantum_info
.
Statevector`
A notable difference is that the new provider is no longer exposed through a global instance (like
BasicAer
), so it will not be valid to do
from qiskit import BasicProvider
. Instead, the provider class must be imported from its submodule and instantiated:
from
qiskit
.
providers
.
basic_provider
import
BasicProvider
provider
=
BasicProvider
()
backend
=
provider
.
get_backend
(
"sim_name"
)
The following examples show the migration paths of the three simulators in
basicaer
.
Statevector simulator:
from
qiskit
import
QuantumCircuit
qc
=
QuantumCircuit
(
3
)
qc
.
h
(
0
)
qc
.
h
(
1
)
qc
.
cx
(
1
,
2
)
qc
.
measure_all
()
# Former path
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
"statevector_simulator"
)
statevector
=
backend
.
run
(qc).
result
().
get_statevector
()
# New path
qc
.
remove_final_measurements
()
# no measurements allowed
from
qiskit
.
quantum_info
import
Statevector
statevector
=
Statevector
(qc)
Unitary simulator:
from
qiskit
import
QuantumCircuit
qc
=
QuantumCircuit
(
3
)
qc
.
h
(
0
)
qc
.
h
(
1
)
qc
.
cx
(
1
,
2
)
qc
.
measure_all
()
# Former path
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
"unitary_simulator"
)
result
=
backend
.
run
(qc).
result
()
# New path
qc
.
remove_final_measurements
()
# no measurements allowed
from
qiskit
.
quantum_info
import
Operator
result
=
Operator
(qc).
data
Qasm simulator:
from
qiskit
import
QuantumCircuit
qc
=
QuantumCircuit
(
3
)
qc
.
h
(
0
)
qc
.
h
(
1
)
qc
.
cx
(
1
,
2
)
qc
.
measure_all
()
# Former path
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
"qasm_simulator"
)
result
=
backend
.
run
(qc).
result
()
# New path
from
qiskit
.
providers
.
basic_provider
import
BasicProvider
backend
=
BasicProvider
().
get_backend
(
"basic_simulator"
)
result
=
backend
.
run
(qc).
result
()
# or, directly
from
qiskit
.
providers
.
basic_provider
import
BasicSimulator
backend
=
BasicSimulator
()
result
=
backend
.
run
(qc).
result
()
Using a
PauliList
as an observable that is implicitly converted to a
SparsePauliOp
with coefficients 1 when calling
Estimator.run()
is deprecated. Instead you should explicitly convert the argument using
SparsePauliOp(pauli_list)
first.
Critical Issues
When updating Qiskit from
0.46.x
to
1.0.0
you will not be able to update in place. For example,
pip install -U qiskit
or
pip install --upgrade qiskit
is not supported and likely will
not
work. To upgrade
qiskit
the recommended path is to create a new virtual environment (
venv
) to build a new separate environment for Qiskit>=1.0.0. For example:
python
-
m venv qiskit_1
.
0
source qiskit_1
.
0
/
bin
/
activate
pip install qiskit
>=
1
will create a new virtual environment named
qiskit_1.0
will contain the new version of Qiskit.