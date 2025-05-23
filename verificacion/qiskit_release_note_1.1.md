Qiskit SDK 1.1 release notes
1.1.2
Prelude
Qiskit 1.1.2 is a minor bugfix release for the 1.1 series.

Bug Fixes
Fixed a bug in BitArray.from_counts() and BitArray.from_samples(). Previously these would raise an error if given data containing only zeros, and no value for the optional argument num_bits. Now they produce a BitArray with BitArray.num_bits set to 1.

Fixed a missing decorator in C3SXGate that made it fail if Gate.to_matrix() was called. The gate matrix is now return as expected.

Added missing Clifford gates to the CollectCliffords transpiler pass. In particular, we have added the gates ECRGate, DCXGate, iSWAPGate, SXGate and SXdgGate to this transpiler pass.

The QuantumCircuit.parameters attribute will now correctly be empty when using QuantumCircuit.copy_empty_like() on a parametric circuit. Previously, an internal cache would be copied over without invalidation. Fix #12617.

Fix the SolovayKitaev transpiler pass when loading basic approximations from an existing .npy file. Previously, loading a stored approximation which allowed for further reductions (e.g. due to gate cancellations) could cause a runtime failure. Additionally, the global phase difference of the U(2) gate product and SO(3) representation was lost during a save-reload procedure. Fixes Qiskit/qiskit#12576.

Fixed an issue with dag_drawer() and DAGCircuit.draw() when attempting to visualize a DAGCircuit instance that contained Var wires. The visualizer would raise an exception trying to do this which has been fixed so the expected visualization will be generated.

The constructor GenericBackendV2 previously allowed malformed backends to be constructed because it accepted basis gates that couldn’t be allocated given the backend size. For example, a backend with a single qubit could previously accept a basis with two-qubit gates.

The OpenQASM 2 parser (qiskit.qasm2) can now handle conditionals with integers that do not fit within a 64-bit integer. Fixed #12773.

Previously, DAGCircuit.replace_block_with_op() allowed an n-qubit operation to be placed onto a block of m qubits, leaving the DAG in an invalid state. This behavior has been fixed, and any attempt to do this will now raise a DAGCircuitError as expected.

1.1.1
Prelude
Qiskit 1.1.1 is a minor bugfix release for the 1.1 series.

Bug Fixes
Fix a bug in Isometry due to an unnecessary assertion, that led to an error in UnitaryGate.control() when UnitaryGate had more that two qubits.

QuantumCircuit.depth() will now correctly handle operations that do not have operands, such as GlobalPhaseGate.

QuantumCircuit.depth() will now count the variables and clbits used in real-time expressions as part of the depth calculation.

Fixed a bug in qiskit.visualization.pulse_v2.interface.draw() that didn’t draw pulse schedules when the draw function was called with a BackendV2 argument. Because the V2 backend doesn’t report hardware channel frequencies, the generated drawing will show ‘no freq.’ below each channel label.

The VF2Layout pass would raise an exception when provided with a Target instance without connectivity constraints. This would be the case with targets from Aer 0.13. The issue is now fixed.

ParameterExpression was updated so that fully bound instances that compare equal to instances of Python’s built-in numeric types (like float and int) also have hash values that match those of the other instances. This change ensures that these types can be used interchangeably as dictionary keys. See #12488.

Custom gates (those stemming from a gate statement) in imported OpenQASM 2 programs will now have a Gate.to_matrix() implementation. Previously they would have no matrix definition, meaning that roundtrips through OpenQASM 2 could needlessly lose the ability to derive the gate matrix. Note, though, that the matrix is calculated by recursively finding the matrices of the inner gate definitions, as Operator does, which might be less performant than before the round-trip.

Target.has_calibration() has been updated so that it does not raise an exception for an instruction that has been added to the target with None for its instruction properties. Fixes #12525.

1.1.0
Prelude
The Qiskit 1.1.0 release is a minor feature release that includes a myriad of new feature and bugfixes. The highlights for this release are:

Support for typed classical variables has been added to Qiskit’s QuantumCircuit. These classical variables can be specified as inputs or as scoped variables in a QuantumCircuit where they e.g. store the output of qubit measurements or target control-flow operations. Support for e.g. setting gate parameters or output variables will be added in the future.

The default two qubit synthesis methods that are used internally by the transpiler in the UnitarySynthesis pass have been re-implemented in Rust. This yields significant runtime speedups when decomposing two qubit unitary matrices. As a consequence, the runtime of transpilation with optimization level 3 was significantly improved where running UnitarySynthesis incurred a large runtime overhead historically. This release also starts running UnitarySynthesis as part of the optimization stage in optimization level 2 because of these runtime performance improvements.

Additionally, the numeric methods used in Isometry have been moved to Rust, enabling large runtime speed-ups in particular for controlled unitary gate synthesis. The decomposition for multi-controlled :class:.XGate` and PhaseGate has been improved resulting in a reduction in the number of gates used in the synthesis by more than two orders of magnitude.

A number of new transpiler passes have been introduced to Qiskit that yield significant runtime speedups while also decreasing the size of the transpiled quantum circuits in many cases. Specifically, ElidePermutations and StarPreRouting have been demonstrated to have a significant impact on the routing output quality and runtime and RemoveFinalReset can improve quantum circuits that include resets.

The default pass managers have been improved by extending them with the newly introduced transpiler passes. In particular, the optimization level 2 preset pass manager from generate_preset_pass_manager and used internally by transpile() has been refactored to have a better tradeoff between runtime and optimization effort in order to serve as a default pass manager in future releases. While this release doesn’t change the default to use level 2 it is typically a better choice than using level 1 or 3.

New generic primitive V2 implementations were added, BackendEstimatorV2 and BackendSamplerV2, to compliment the existing full statevector based implementations.

Changes to platform support: Python 3.8 is deprecated starting with Qiskit 1.1.0 and will no longer be supported in 1.3.0, and arm64 macOS has been promoted to tier 1 support.

Circuits Features
The methods QuantumCircuit.power(), Gate.power(), as well as the similar methods on subclasses of subclasses of Gate (such as of SGate) all have an additional have a new argument annotated which is used to return an AnnotatedOperation object when applying a power to a gate or circuit. The default value of False corresponds to the existing behavior. Furthermore, for standard gates with an explicitly defined power method, the argument annotated has no effect. For example, both SGate().power(1.5, annotated=False) and SGate().power(1.5, annotated=True) return a PhaseGate. A difference in the value of annotated manifests for gates without an explicitly defined power method. The value of False returns a UnitaryGate, just as before, while the value of True returns an AnnotatedOperation that represents the instruction modified with the “power modifier”.

Added a new ctrl_state argument to QuantumCircuit.mcp() and MCPhaseGate.

The QuantumCircuit.mcp() method and MCPhaseGate class have been updated to include a ctrl_state parameter. This enhancement allows users to specify the control state of the multi-controlled phase gate. The parameter can accept either an integer value or a bitstring and defaults to controlling the ‘1’ state if not provided.


from qiskit import QuantumCircuit
 
qc = QuantumCircuit(4)
qc.mcp(0.2,[0,1,2],3,ctrl_state=2)
Added a new ctrl_state argument to QuantumCircuit.mcx().

The QuantumCircuit.mcx() method in the quantum circuit library has been enhanced to include a ctrl_state parameter, allowing users to specify the control state of the multi-controlled X gate. This parameter can accept either a decimal value or a bitstring and defaults to controlling the ‘1’ state if not provided.


from qiskit import QuantumCircuit
 
qc = QuantumCircuit(3, 3)
qc.mcx([0, 1], 2, ctrl_state="00")
A QuantumCircuit can now contain typed classical variables:


from qiskit.circuit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.circuit.classical import expr, types
 
qr = QuantumRegister(2, "q")
cr = ClassicalRegister(2, "c")
qc = QuantumCircuit(qr, cr)
# Add two input variables to the circuit with different types.
a = qc.add_input("a", types.Bool())
mask = qc.add_input("mask", types.Uint(2))
 
# Test whether the input variable was true at runtime.
with qc.if_test(a) as else_:
    qc.x(0)
with else_:
    qc.h(0)
 
qc.cx(0, 1)
qc.measure(qr, cr)
 
# Add a typed variable manually, initialized to the same value as the classical register.
b = qc.add_var("b", expr.lift(cr))
 
qc.reset([0, 1])
qc.h(0)
qc.cx(0, 1)
qc.measure(qr, cr)
 
# Store some calculated value into the `b` variable.
qc.store(b, expr.bit_and(b, cr))
# Test whether we had equality, up to a mask.
with qc.if_test(expr.equal(expr.bit_and(b, mask), mask)):
    qc.x(0)
These variables can be specified either as inputs to the circuit, or as scoped variables. The circuit object does not yet have support for representing typed classical-variable outputs, but this will be added later when hardware and the result interfaces are in more of a position to support it. Circuits that represent a block of an inner scope may also capture variables from outer scopes.

A variable is a Var node, which can now contain an arbitrary type, and represents a unique memory location within its live range when added to a circuit. These can be constructed in a circuit using QuantumCircuit.add_var() and QuantumCircuit.add_input(), or at a lower level using Var.new().

Variables can be manually stored to, using the Store instruction and its corresponding circuit method QuantumCircuit.store(). This includes writing to Clbit and ClassicalRegister instances wrapped in Var nodes.

Variables can be used wherever classical expressions (see qiskit.circuit.classical.expr) are valid. Currently this is the target expressions of control-flow operations, though we plan to expand this to gate parameters in the future, as the type and expression system are expanded.

See Real-time classical computation for more discussion of these variables, and the associated data model.

These are supported throughout the transpiler, through QPY serialization (qiskit.qpy), OpenQASM 3 export (qiskit.qasm3), and have initial support through the circuit visualizers (see QuantumCircuit.draw()).

Note
The new classical variables and storage will take some time to become supported on hardware and simulator backends. They are not supported in the primitives interfaces (qiskit.primitives), but will likely inform those interfaces as they evolve.

The classical realtime-expressions module qiskit.circuit.classical can now represent indexing and bitshifting of unsigned integers and bitlikes (e.g. ClassicalRegister). For example, it is now possible to compare one register with the bitshift of another:


from qiskit.circuit import QuantumCircuit, ClassicalRegister
from qiskit.circuit.classical import expr
 
cr1 = ClassicalRegister(4, "cr1")
cr2 = ClassicalRegister(4, "cr2")
qc = QuantumCircuit(cr1, cr2)
with qc.if_test(expr.equal(cr1, expr.shift_left(cr2, 2))):
    pass
Qiskit can also represent a condition that dynamically indexes into a register:


with qc.if_test(expr.index(cr1, cr2)):
    pass
The construction performance of NLocal and its derived circuit-library subclasses (e.g. EfficientSU2 and RealAmplitudes) has significantly improved, when the rotation and/or entanglement subblocks are simple applications of a single Qiskit standard-library gate. Since these circuits are constructed lazily, you might not see the improvement immediately on instantiation of the class, but instead on first access to its internal structure. Performance improvements are on the order of ten times faster.

QuantumCircuit.append() now has a copy keyword argument, which defaults to True. When an instruction with runtime parameters (ParameterExpressions) is appended to a circuit, by default, the circuit has always created a copy of the instruction so that if QuantumCircuit.assign_parameters() attempts to mutate the instruction in place, it does not affect other references to the same instruction. Now, setting copy=False allows you to override this, so you can avoid the copy penalty if you know your instructions will not be used in other locations.

QuantumCircuit.compose() now has a copy keyword argument, which defaults to True. By default, compose() copies all instructions, so that mutations from one circuit do not affect any other. If copy=False, then instructions from the other circuit will become directly owned by the new circuit, which may involve mutating them in place. The other circuit must not be used afterwards, in this case.

Construction time for QuantumVolume circuits has been significantly improved, on the order of 10x or a bit more. The internal SU4 gates will now also use more bits of randomness during their generation, leading to more representative volume circuits, especially at large widths and depths.

QuantumVolume now has a flatten keyword argument. This defaults to False, where the constructed circuit contains a single instruction that in turn contains the actual volume structure. If set True, the circuit will directly have the volumetric SU4 matrices.

UnitaryGate now accepts an optional num_qubits argument. The only effect of this is to skip the inference of the qubit count, which can be helpful for performance when many gates are being constructed.

QuantumCircuit has several new methods to work with and inspect manual Var variables.

See Working with real-time typed classical data for more in-depth discussion on all of these.

The new methods are:

add_var()
add_input()
add_capture()
add_uninitialized_var()
get_var()
has_var()
iter_vars()
iter_declared_vars()
iter_captured_vars()
iter_input_vars()
store()
In addition, there are several new dynamic attributes on QuantumCircuit surrounding these variables:

num_vars
num_input_vars
num_captured_vars
num_declared_vars
ControlFlowOp and its subclasses now have a iter_captured_vars() method, which will return an iterator over the unique variables captured in any of its immediate blocks.

DAGCircuit has several new methods to work with and inspect manual Var variables. These are largely equivalent to their QuantumCircuit counterparts, except that the DAGCircuit ones are optimized for programmatic access with already defined objects, while the QuantumCircuit methods are more focussed on interactive human use.

The new methods are:

add_input_var()
add_captured_var()
add_declared_var()
has_var()
iter_vars()
iter_declared_vars()
iter_captured_vars()
iter_input_vars()
There are also new public attributes:

num_vars
num_input_vars
num_captured_vars
num_declared_vars
DAGCircuit.wires will now also contain any Var manual variables in the circuit as well, as these are also classical data flow.

A new method, Var.new(), is added to manually construct a real-time classical variable that owns its memory.

QuantumCircuit.compose() has two need keyword arguments, var_remap and inline_captures to better support real-time classical variables.

var_remap can be used to rewrite Var nodes in the circuit argument as its instructions are inlined onto the base circuit. This can be used to avoid naming conflicts.

inline_captures can be set to True (defaults to False) to link all Var nodes tracked as “captures” in the argument circuit with the same Var nodes in the base circuit, without attempting to redeclare the variables. This can be used, in combination with QuantumCircuit.copy_empty_like()’s vars_mode="captures" handling, to build up a circuit layer by layer, containing variables.

DAGCircuit.compose() has a new keyword argument, inline_captures, which can be set to True to inline “captured” Var nodes on the argument circuit onto the base circuit without redeclaring them. In conjunction with the vars_mode="captures" option to several DAGCircuit methods, this can be used to combine DAGs that operate on the same variables.

QuantumCircuit.copy_empty_like() and DAGCircuit.copy_empty_like() have a new keyword argument, vars_mode which controls how any memory-owning Var nodes are tracked in the output. By default ("alike"), the variables are declared in the same input/captured/local mode as the source. This can be set to "captures" to convert all variables to captures (useful with compose()) or "drop" to remove them.

A new vars_mode keyword argument has been added to the DAGCircuit methods:

separable_circuits()
layers()
serial_layers()
which has the same meaning as it does for copy_empty_like().

All of the “standard gates” in the circuit library (qiskit.circuit.library) can now be specified by string name for the entangling operations in TwoLocal circuits, such as RealAmplitudes and EfficientSU2.

Primitives Features
The implementation BackendEstimatorV2 of BaseEstimatorV2 was added. This estimator supports BackendV1 and BackendV2.


import numpy as np
from qiskit import transpile
from qiskit.circuit.library import IQP
from qiskit.primitives import BackendEstimatorV2
from qiskit.providers.fake_provider import Fake7QPulseV1
from qiskit.quantum_info import SparsePauliOp, random_hermitian
 
backend = Fake7QPulseV1()
estimator = BackendEstimatorV2(backend=backend)
n_qubits = 5
mat = np.real(random_hermitian(n_qubits, seed=1234))
circuit = IQP(mat)
observable = SparsePauliOp("Z" * n_qubits)
isa_circuit = transpile(circuit, backend=backend, optimization_level=1)
isa_observable = observable.apply_layout(isa_circuit.layout)
job = estimator.run([(isa_circuit, isa_observable)], precision=0.01)
result = job.result()
print(f"> Expectation value: {result[0].data.evs}")
print(f"> Standard error: {result[0].data.stds}")
print(f"> Metadata: {result[0].metadata}")
The implementation BackendSamplerV2 of BaseSamplerV2 was added. This sampler supports BackendV1 and BackendV2 that allow memory option to compute bitstrings.


import numpy as np
from qiskit import transpile
from qiskit.circuit.library import IQP
from qiskit.primitives import BackendSamplerV2
from qiskit.providers.fake_provider import Fake7QPulseV1
from qiskit.quantum_info import random_hermitian
 
backend = Fake7QPulseV1()
sampler = BackendSamplerV2(backend=backend)
n_qubits = 5
mat = np.real(random_hermitian(n_qubits, seed=1234))
circuit = IQP(mat)
circuit.measure_all()
isa_circuit = transpile(circuit, backend=backend, optimization_level=1)
job = sampler.run([isa_circuit], shots=100)
result = job.result()
print(f"> bitstrings: {result[0].data.meas.get_bitstrings()}")
print(f"> counts: {result[0].data.meas.get_counts()}")
print(f"> Metadata: {result[0].metadata}")
Added methods to join multiple BitArray objects along various axes.

concatenate(): join arrays along an existing axis of the arrays.
concatenate_bits(): join arrays along the bit axis.
concatenate_shots(): join arrays along the shots axis.

ba = BitArray.from_samples(['00', '11'])
print(ba)
# BitArray(<shape=(), num_shots=2, num_bits=2>)
 
# reshape the bit array because `concatenate` requires an axis.
ba_ = ba.reshape(1, 2)
print(ba_)
# BitArray(<shape=(1,), num_shots=2, num_bits=2>)
 
ba2 = BitArray.concatenate([ba_, ba_])
print(ba2.get_bitstrings())
# ['00', '11', '00', '11']
 
# `concatenate_bits` and `concatenates_shots` do not require any axis.
 
ba3 = BitArray.concatenate_bits([ba, ba])
print(ba3.get_bitstrings())
# ['0000', '1111']
 
ba4 = BitArray.concatenate_shots([ba, ba])
print(ba4.get_bitstrings())
# ['00', '11', '00', '11']
Added methods to generate a subset of BitArray object by slicing along various axes.

__getitem__(): slice the array along an existing axis of the array.
slice_bits(): slice the array along the bit axis.
slice_shots(): slice the array along the shot axis.

ba = BitArray.from_samples(['0000', '0001', '0010', '0011'], 4)
print(ba)
# BitArray(<shape=(), num_shots=4, num_bits=4>)
print(ba.get_bitstrings())
# ['0000', '0001', '0010', '0011']
 
ba2 = ba.reshape(2, 2)
print(ba2)
# BitArray(<shape=(2,), num_shots=2, num_bits=2>)
print(ba2[0].get_bitstrings())
# ['0000', '0001']
print(ba2[1].get_bitstrings())
# ['0010', '0011']
 
ba3 = ba.slice_bits([0, 2])
print(ba3.get_bitstrings())
# ['00', '01', '00', '01']
 
ba4 = ba.slice_shots([0, 2])
print(ba3.get_bitstrings())
# ['0000', '0010']
Added a method transpose() to transpose a BitArray.


ba = BitArray.from_samples(['00', '11']).reshape(2, 1, 1)
print(ba)
# BitArray(<shape=(2, 1), num_shots=1, num_bits=2>)
print(ba.transpose())
# BitArray(<shape=(1, 2), num_shots=1, num_bits=2>)
Added a method expectation_values() to compute expectation values of diagonal operators.


ba = BitArray.from_samples(['01', '11'])
print(ba.expectation_values(["IZ", "ZI", "01"]))
# [-1.   0.   0.5]
DataBin now satisfies the Shaped protocol. This means that every DataBin instance now has the additional attributes

shape (tuple[int, …]): the leading shape of every entry in the instance
ndim (int): the length of shape
size (int): the product of the entries of shape
The shape can be passed to the constructor.

Added mapping-like features to DataBin, i.e., __getitem__, __contains__, __iter__, keys(), values(), and items().


from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
 
circuit = QuantumCircuit(1)
circuit.h(0)
circuit.measure_all()
 
sampler = StatevectorSampler()
result = sampler.run([circuit]).result()
databin = result[0].data
for creg, arr in databin.items():
    print(creg, arr)
for creg in databin:
    print(creg, databin[creg])
The subclass SamplerPubResult of PubResult was added, which BaseSamplerV2 implementations can return. The main feature added in this new subclass is join_data(), which joins together (a subset of) the contents of data into a single object. This enables the following patterns:


job_result =  sampler.run([pub1, pub2, pub3], shots=123).result()
 
# assuming all returned data entries are BitArrays
counts1 = job_result[0].join_data().get_counts()
bistrings2 = job_result[1].join_data().get_bitstrings()
array3 = job_result[2].join_data().array
Providers Features
The BasicSimulator python-based simulator included in basic_provider now supports running all the standard gates up to 3 qubits defined in qiskit.circuit.library.
Pulse Features
It is now possible to assign parameters to pulse Schedule and ScheduleBlock objects by specifying the parameter name as a string. The parameter name can be used to assign values to all parameters within the Schedule or ScheduleBlock that have the same name. Moreover, the parameter name of a ParameterVector can be used to assign all values of the vector simultaneously (the list of values should therefore match the length of the vector).

The assign_parameters methods of Schedule and ScheduleBlock now support assigning a ParameterVector to a list of parameter values simultaneously in addition to assigning individual Parameter instances to individual values.

OpenQASM Features
The OpenQASM 3 exporter supports manual-storage Var nodes on circuits.
QPY Features
QPY (qiskit.qpy) format version 12 has been added, which includes support for memory-owning Var variables. See Version 12 for more detail on the format changes.
Quantum Information Features
Added a new apply_layout() method that is equivalent to apply_layout(). This method is used to apply a TranspileLayout layout from the transpiler to a Pauli observable that was built for an input circuit. This enables working with BaseEstimator / BaseEstimatorV2 implementations and local transpilation when the input is of type Pauli. For example:


from qiskit.circuit.library import RealAmplitudes
from qiskit.primitives import BackendEstimatorV2
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.quantum_info import Pauli
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
 
psi = RealAmplitudes(num_qubits=2, reps=2)
H1 = Pauli("XI")
backend = GenericBackendV2(num_qubits=7)
estimator = BackendEstimatorV2(backend=backend)
thetas = [0, 1, 1, 2, 3, 5]
pm = generate_preset_pass_manager(optimization_level=3, backend=backend)
transpiled_psi = pm.run(psi)
permuted_op = H1.apply_layout(transpiled_psi.layout)
res = estimator.run([(transpiled_psi, permuted_op, thetas)]).result()
where an input circuit is transpiled locally before it’s passed to run(). Transpilation expands the original circuit from 2 to 7 qubits (the size of backend) and permutes its layout, which is then applied to H1 using apply_layout() to reflect the transformations performed by pm.run().

Adds the PauliList.noncommutation_graph() and SparsePauliOp.noncommutation_graph() methods, exposing the construction of non-commutation graphs, recasting the measurement operator grouping problem into a graph coloring problem. This permits users to work with these graphs directly, for example to explore coloring algorithms other than the one used by SparsePauliOp.group_commuting().

The performance of SparsePauliOp.to_matrix() has been greatly improved for both dense and sparse forms. By default, both will now take advantage of threaded parallelism available on your system, subject to the RAYON_NUM_THREADS environment variable. You can temporarily force serial execution using the new force_serial Boolean argument to to_matrix().

Synthesis Features
The KMSSynthesisLinearFunction plugin for synthesizing LinearFunction objects now accepts two additional options use_inverted and use_transposed. These option modify the matrix on which the underlying synthesis algorithm runs by possibly inverting and/or transposing it, and then suitably adjust the synthesized circuit. By varying these options, we generally get different synthesized circuits, and in cases may obtain better results than for their default values.

The PMHSynthesisLinearFunction plugin for synthesizing LinearFunction objects now accepts several additional options. The option section_size is passed to the underlying synthesis method. The options use_inverted and use_transposed modify the matrix on which the underlying synthesis algorithm runs by possibly inverting and/or transposing it, and then suitably adjust the synthesized circuit. By varying these options, we generally get different synthesized circuits, and in cases may obtain better results than for their default values.

Added a new argument, use_dag, to the TwoQubitBasisDecomposer.__call__() and XXDecomposer.__call__() methods. This argument is used to control whether a DAGCircuit is returned when calling a TwoQubitBasisDecomposer or XXDecomposer instance instead of the default QuantumCircuit. For example:


from qiskit.circuit.library import CXGate
from qiskit.quantum_info import random_unitary
from qiskit.synthesis import TwoQubitBasisDecomposer
 
decomposer = TwoQubitBasisDecomposer(CXGate(), euler_basis="PSX")
decomposer(random_unitary(4), use_dag=True)
will return a DAGCircuit when calling the TwoQubitBasisDecomposer instance decomposer.

LieTrotter.synthesize() now uses QuantumCircuit.repeat() to generate additional repetitions of a Trotter step after the first Trotter step. This reduces the number of QuantumCircuit.compose() calls by a factor of reps and significantly reduces the runtime for larger operators.

Add a new synthesis method synth_permutation_reverse_lnn_kms() of reverse permutations for linear nearest-neighbor architectures using Kutin, Moulton, Smithline method. This algorithm synthesizes the reverse permutation on 
n
n qubits over a linear nearest-neighbor architecture using CX gates with depth 
2
∗
n
+
2
2∗n+2.

The TwoQubitBasisDecomposer class has been rewritten in Rust which greatly improves the runtime performance.

The TwoQubitWeylDecomposition synthesis class has been rewritten in Rust for better performance.

Transpiler Features
Extended the commutation analysis performed by CommutationChecker to also work with abstract circuits, i.e. each operation in the input quantum circuit is now checked for its matrix representation before proceeding to the analysis step. Previously, the commutation analysis was only performed on physical circuits. In addition, each operation is now checked for its ability to be cached in the session commutation library. For example, this now enables computing whether AnnotatedOperation commute. This enables transpiler passes that rely on CommutationChecker internally, such as CommutativeCancellation, to run during earlier stages of a default transpilation pipeline (prior to basis translation).

The transpiler pass ElidePermutations runs by default in the init stage for optimization levels 2 and 3. Intuitively, removing SwapGates and PermutationGates in a virtual circuit is almost always beneficial, as it makes the circuit shorter and easier to route. As OptimizeSwapBeforeMeasure is a special case of ElidePermutations, it has been replaced by the ElidePermuations pass as part of the init stage in optimization level 3 pass managers.

Added a new optimization transpiler pass, ElidePermutations, which is designed to run prior to the Layout Stage and will optimize away any SwapGates and PermutationGates in a circuit by permuting virtual qubits. For example, taking a circuit with SwapGates:

_images/release_notes-1.png
will remove the swaps when the pass is run:


from qiskit.transpiler.passes import ElidePermutations
from qiskit.circuit import QuantumCircuit
 
qc = QuantumCircuit(3)
qc.h(0)
qc.swap(0, 1)
qc.swap(2, 0)
qc.cx(1, 0)
qc.measure_all()
 
ElidePermutations()(qc).draw("mpl")
_images/release_notes-2.png
The pass also sets the virtual_permutation_layout property set, storing the permutation of the virtual qubits at the end of the circuit that was optimized away.

The HLSConfig now has two additional optional arguments. The argument plugin_selection can be set either to "sequential" or to "all". If set to “sequential” (default), for every higher-level-object the HighLevelSynthesis pass will consider the specified methods sequentially, in the order they appear in the list, stopping at the first method that is able to synthesize the object. If set to “all”, all the specified methods will be considered, and the best synthesized circuit, according to plugin_evaluation_fn will be chosen. The argument plugin_evaluation_fn is an optional callable that evaluates the quality of the synthesized quantum circuit; a smaller value means a better circuit. When set to None, the quality of the circuit is its size (i.e. the number of gates that it contains).

The following example illustrates the new functionality:


from qiskit import QuantumCircuit
from qiskit.circuit.library import LinearFunction
from qiskit.synthesis.linear import random_invertible_binary_matrix
from qiskit.transpiler.passes import HighLevelSynthesis, HLSConfig
 
# Create a circuit with a linear function
mat = random_invertible_binary_matrix(7, seed=37)
qc = QuantumCircuit(7)
qc.append(LinearFunction(mat), [0, 1, 2, 3, 4, 5, 6])
 
# Run different methods with different parameters,
# choosing the best result in terms of depth.
hls_config = HLSConfig(
    linear_function=[
        ("pmh", {}),
        ("pmh", {"use_inverted": True}),
        ("pmh", {"use_transposed": True}),
        ("pmh", {"use_inverted": True, "use_transposed": True}),
        ("pmh", {"section_size": 1}),
        ("pmh", {"section_size": 3}),
        ("kms", {}),
        ("kms", {"use_inverted": True}),
    ],
    plugin_selection="all",
    plugin_evaluation_fn=lambda circuit: circuit.depth(),
)
 
# synthesize
qct = HighLevelSynthesis(hls_config=hls_config)(qc)
In the example, we run multiple synthesis methods with different parameters, choosing the best circuit in terms of depth. Note that optimizing circuit.size() instead would pick a different circuit.

Added the CommutativeCancellation pass to the init stage of the preset pass managers for optimization levels 2 and 3. This enables the preset pass managers to cancel additional logical operations at the beginning of the compilation pipeline.

The following analysis passes now accept constraints encoded in a Target thanks to a new target input argument:

InstructionDurationCheck
ConstrainedReschedule
ValidatePulseGates
The target constraints will have priority over user-provided constraints, for coherence with the rest of the transpiler pipeline.

Added a new method Layout.inverse() which is used for taking the inverse of a Layout object. Added a new method Layout.compose() which is used for composing two Layout objects together. Added a new method Layout.to_permutation() which is used for creating a permutation corresponding to a Layout object.

Added a new reduction to the OptimizeAnnotated transpiler pass. This reduction looks for annotated operations (objects of type AnnotatedOperation that consist of a base operation 
B
B and a list 
M
M of control, inverse and power modifiers) with the following properties:

the base operation 
B
B needs to be synthesized (i.e. it’s not already supported by the target or belongs to the equivalence library)
the definition circuit for 
B
B can be expressed as 
P
P – 
Q
Q – 
R
R with 
R
=
P
−
1
R=P 
−1
 
In this case the modifiers can be moved to the 
Q
Q-part only. As a specific example, controlled QFT-based adders have the form control - [QFT -- U -- IQFT], which can be simplified to QFT -- control-[U] -- IQFT. By removing the controls over QFT and IQFT parts of the circuit, one obtains significantly fewer gates in the transpiled circuit.

Added two new methods to the DAGCircuit class: qiskit.dagcircuit.DAGCircuit.op_successors() returns an iterator to DAGOpNode successors of a node, and qiskit.dagcircuit.DAGCircuit.op_successors() returns an iterator to DAGOpNode predecessors of a node.

Added a new transpiler pass, RemoveFinalReset, which will remove any Reset operation which is the final instruction on a qubit wire. For example, taking a circuit with final Resets:

_images/release_notes-3.png
will remove the final resets when the pass is run:


from qiskit.transpiler.passes import RemoveFinalReset
from qiskit.circuit import QuantumCircuit
 
qc = QuantumCircuit(3, 1)
qc.reset(0)
qc.h(range(3))
qc.cx(1, 0)
qc.measure(0, 0)
qc.reset(range(3))
RemoveFinalReset()(qc).draw("mpl")
_images/release_notes-4.png
Added a new transpiler pass StarPreRouting which is designed to identify star connectivity subcircuits and then replace them with an optimal linear routing. This is useful for certain circuits that are composed of this circuit connectivity such as Bernstein-Vazirani and QFT. For example:

_images/release_notes-5.png

from qiskit.circuit import QuantumCircuit
from qiskit.transpiler.passes import StarPreRouting
 
qc = QuantumCircuit(5)
qc.h(0)
qc.cx(0, range(1, 5))
StarPreRouting()(qc).draw("mpl")
_images/release_notes-6.png
Alternatively, an existing preset pass manager can be extended by:


from qiskit import QuantumCircuit
from qiskit.transpiler import CouplingMap
from qiskit.transpiler.passes import StarPreRouting
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
 
cm = CouplingMap.from_line(5)
qc = QuantumCircuit(5)
qc.h(0)
qc.cx(0, range(1, 5))
pm = generate_preset_pass_manager(2, coupling_map=cm)
pm.init += StarPreRouting()
result = pm.run(qc)
result.draw("mpl")
_images/release_notes-7.png
Visualization Features
The text and Matplotlib circuit drawers (QuantumCircuit.draw()) have minimal support for displaying expressions involving manual real-time variables. The Store operation and the variable initializations are not yet supported; for large-scale dynamic circuits, we recommend using the OpenQASM 3 export capabilities (qasm3.dumps()) to get a textual representation of a circuit.
Misc. Features
This release of Qiskit finalizes support for NumPy 2.0. Qiskit will continue to support both NumPy 1.x and 2.x for the foreseeable future.
Upgrade Notes
Removes the hard-coding of style options for plot_histogram(). This allows Matplotlib style files to be faithfully applied to the figures. Users looking to go beyond the defaults set by Matplotlib can make their own style files, or pass a Matplotlib Axes object to plot_histogram and post-apply any customizations.

The transpile() function has been upgraded to internally convert backend inputs of type BackendV1 to BackendV2, which allows the transpilation pipeline to now access the backend constraints through a Target. This change does not require any user action.

Circuits Upgrade Notes
The random-number usage of QuantumVolume has changed, so you will get a different circuit for a fixed seed between older versions of Qiskit and this version. The random-unitary generation now uses more bits of entropy, so large circuits will be less biased.

The internal UnitaryGate instances in the definition of a QuantumVolume circuit will no longer have a label field set. Previously this was set to the string su4_<seed> where <seed> was a three-digit number denoting the seed of an internal Numpy pRNG instance for that gate. Doing this was a serious performance problem, and the seed ought not to have been useful; if you need to retrieve the matrix from the gate, simply use the Gate.to_matrix() method.

Primitives Upgrade Notes
The function make_data_bin() no longer creates and returns a DataBin subclass. It instead always returns the DataBin class. However, it continues to exist for backwards compatibility, though will eventually be deprecated. All users should migrate to construct DataBin instances directly, instead of instantiating subclasses as output by make_data_bin().
Providers Upgrade Notes
Implementations of BackendV2 (and BackendV1) may desire to update their run() methods to eagerly reject inputs containing typed classical variables (see qiskit.circuit.classical) and the Store instruction, if they do not have support for them. The new Store instruction is treated by the transpiler as an always-available “directive” (like Barrier); if your backends do not support this won’t be caught by the transpiler.

See Real-time variables for more information.

QPY Upgrade Notes
The value of qiskit.qpy.QPY_VERSION is now 12. QPY_COMPATIBILITY_VERSION is unchanged at 10.
Synthesis Upgrade Notes
The TwoQubitWeylDecomposition no longer will self-specialize into a subclass on creation. This was an internal detail of the TwoQubitWeylDecomposition previously, and was not a documented public behavior as all the subclasses behaved the same and were only used for internal dispatch. However, as it was discoverable behavior this release note is to document that this will no longer occur and all instances of TwoQubitWeylDecomposition will be of the same type. There is no change in behavior for public methods of the class.
Transpiler Upgrade Notes
The preset StagedPassManager returned for optimization level 2 by generate_preset_pass_manager() and level_2_pass_manager() have been reworked to provide a better balance between runtime and optimization. This means the output circuits will change compared to earlier releases. If you need an exact pass manager from level 2 in earlier releases you can either build it manually or use it from an earlier release and save the circuits with qpy to load with a newer release.
Misc. Upgrade Notes
The minimum supported version of Windows is now Windows 10. In previous releases we did not explicitly list a minimum supported version of Windows and implicitly Windows 7, 8, and 8.1 may have worked (but were never tested). But due to Rust 1.78 dropping support for older versions of Windows Qiskit’s published binaries on PyPI will not support older versions of Windows starting with this release. If you’re using an older version of Windows you can likely still build Qiskit from source using an older Rust compiler (Qiskit’s minimum supported Rust version for building from source is currently 1.70) but older versions of Windows are not a supported platform and are untested.
Deprecation Notes
Support for running Qiskit with Python 3.8 has been deprecated and will be removed in the Qiskit 1.3.0 release. The 1.3.0 is the first release after Python 3.8 goes end of life and is no longer supported. [1] This means that starting in the 1.3.0 release you will need to upgrade the Python version you’re using to Python 3.9 or above.

[1] https://devguide.python.org/versions/

Providers Deprecations
The abstract base classes Provider and ProviderV1 are now deprecated and will be removed in Qiskit 2.0.0. The abstraction offered by these interface definitions were not providing a substantial value; it solely encapsulated the attributes name, backends, and a get_backend(). A _provider_, as a concept, will continue existing as a collection of backends. If you’re implementing a provider currently you can adjust your code by simply removing ProviderV1 as the parent class of your implementation. As part of this you probably would want to add an implementation of get_backend for backwards compatibility. For example:


def get_backend(self, name=None, **kwargs):
  backends = self.backends(name, **kwargs)
  if len(backends) > 1:
      raise QiskitBackendNotFoundError("More than one backend matches the criteria")
  if not backends:
      raise QiskitBackendNotFoundError("No backend matches the criteria")
  return backends[0]
Synthesis Deprecations
The TwoQubitWeylDecomposition.specialize() method is now deprecated and will be removed in the Qiskit 2.0.0 release. This method never had a public purpose and was unsafe for an end user to call as it would mutate the calculated decomposition in the object and produce invalid fields in the object. It was only used internally to construct a new TwoQubitWeylDecomposition object. Despite this it was still a documented part of the public API for the class and is now being deprecated without any potential replacement. This release it always will raise a NotImplementedError when called because the specialization subclassing has been removed as part of the Rust rewrite of the class.
Transpiler Deprecations
The pass qiskit.transpiler.passes.CXCancellation was deprecated in favor of InverseCancellation, which is more generic. CXCancellation is fully semantically equivalent to InverseCancellation([CXGate()]).

The transpilation pass qiskit.transpiler.passes.ALAPSchedule is now deprecated. It was pending for deprecation since Qiskit 0.37 (with Terra 0.21), released on June 2022. The pass is replaced by ALAPScheduleAnalysis, which is an analysis pass.

The transpilation pass qiskit.transpiler.passes.ASAPSchedule is now deprecated. It was pending for deprecation since Qiskit 0.37 (with Terra 0.21), released on June 2022. It has been superseded by ASAPScheduleAnalysis and the new scheduling workflow.

The transpilation pass qiskit.transpiler.passes.DynamicalDecoupling is now deprecated. It was pending for deprecation since Qiskit 0.37 (with Terra 0.21), released on June 2022. Instead, use PadDynamicalDecoupling, which performs the same function but requires scheduling and alignment analysis passes to run prior to it.

The transpilation pass qiskit.transpiler.passes.AlignMeasures is now deprecated. It was pending for deprecation since Qiskit 0.37 (with Terra 0.21), released on June 2022. Instead, use ConstrainedReschedule, which performs the same function and also supports aligning to additional timing constraints.

Visualization Deprecations
The parameters show_idle and show_barrier in the timeline drawers had been replaced by idle_wires and plot_barriers respectively to match the circuit drawer parameters. Their previous names are now deprecated and will be removed in the next major release. The new parameters are fully equivalent.
Bug Fixes
Fixed an issue with the qpy.dump() function where, when the use_symengine flag was set to a truthy object that evaluated to True but was not actually the boolean True, the generated QPY payload would be corrupt. For example, if you set use_symengine to HAS_SYMENGINE, this object evaluates to True when cast as a bool, but isn’t actually True.

Fixed an issue with the circuit_drawer() function and QuantumCircuit.draw() method when loading a matplotlib style via the user configuration file.

Fixed an issue where the ConstrainedReschedule transpiler pass would previously error if the circuit contained a Reset instruction. This has been corrected so that the pass no longer errors, however an actual hardware may behave differently from what Qiskit scheduler assumes especially for mid-circuit measurements and resets. Qiskit scheduler raises RuntimeWarning if it encounters circuit containing either. Fixed #10354

Fixed an issue with the CommutationChecker class where it would error if a gate’s name attribute was UTF8 encoded. Previously only gate names with ascii encoding would work. Fixed #12501

Fixed an issue with the SparsePauliOp.apply_layout() and Pauli.apply_layout() methods when an invalid array with duplicate or negative indices were passed in for the layout argument. Previously this wouldn’t result in an error and the transformation performed would not be valid. These methods will now raise a QiskitError if duplicate indices or negative indices are provided as part of a layout.

Fixed a performance issue in the BackendSamplerV2 and BackendEstimatorV2. Fixed #12290

Fixed an issue with the convert_to_target() where the converter would incorrectly ignore control flow instructions if they were specified in the BackendConfiguration.supported_instructions attribute which is the typical location that control flow instructions are specified in a BackendConfiguration object. Fixed #11872.

Fixed an issue with the circuit_drawer() or QuantumCircuit.draw() when using the mpl output option where the program would hang if the circuit being drawn had a ControlFlow operation in it and the fold option was set to -1 (meaning no fold). Fixed #12012.

Fixed a bug in the conversion of custom pulse instructions to the legacy qiskit.qobj format. The bug was introduced in Qiskit 1.0.0 and caused conversion of instructions with custom pulse shapes to raise an error. After the fix, the conversion is carried out correctly, and the custom pulse is converted to Waveform as it should. Fixed #11828.

A bug in transpile() has been fixed where custom instruction_durations, dt and backend_properties constraints would be ignored when provided at the same time as a backend of type BackendV2. The behavior after the fix is now independent of whether the provided backend is of type BackendV1 or type BackendV2. Similarly, custom timing_constraints are now overridden by target inputs but take precedence over BackendV1 and BackendV2 inputs.

Calling EquivalenceLibrary.set_entry() will now correctly update the internal graph object of the library. Previously, the metadata would be updated, but the graph structure would be unaltered, meaning that users like BasisTranslator would still use the old rules. Fixed #11958.

The EvolvedOperatorAnsatz now correctly handles the case where the operators argument is an empty list. Previously, this would result in an error.

From now on, EvolvedOperatorAnsatz will not have any qregs when thera are zero qubits, instead of having a QuantumRegister instance with zero qubits. This behavior aligns more consistently with its superclass QuantumCircuit.

The method Instruction.repeat() now moves a set condition to the outer returned Instruction and leave the inner gates of its definition unconditional. Previously, the method would leave ClassicalRegister instances within the inner definition, which was an invalid state, and would manifest itself as seemingly unrelated bugs later, such as during transpilation or export. Fixed #11935.

Fixed an issue in the InverseCancellation transpiler pass where in some cases it would incorrectly cancel a self-inverse parameterized gate even if the parameter value didn’t match. Fixed #11815

Improve the decomposition of the gates MCXGate and MCPhaseGate without using ancilla qubits, so that the number of CXGate will grow quadratically in the number of qubits and not exponentially.

A bug that crashes the convert_to_target() function when qubit properties (either T1, T2 or frequency) are missing was fixed. The missing property values in QubitProperties are filled with None.

BasePassManager.run() will no longer leak the previous PropertySet into new workflows when called more than once. Previously, the same PropertySet as before would be used to initialize follow-on runs, which could mean that invalid property information was being given to tasks. The behavior now matches that of Qiskit 0.44. Fixed #11784.

Pauli.evolve() now correctly handles quantum circuits containing ECR gates. Formerly they were not recognized as Clifford gates, and an error was raised.

Fixed a bug in Pauli.evolve() where evolving by a circuit with a name matching certain Clifford gates (‘cx’, ‘cz’, etc) would evolve the Pauli according to the name of the circuit, not by the contents of the circuit. This bug occurred only with the non-default option frame='s'.

Fixed a performance issue in the qpy.load() function when deserializing QPY payloads with large numbers of qubits or clbits in a circuit.

Fixed a bug in the handling of default_alignment argument of build(). Inputs of type AlignmentKind are now correctly processed as default alignments.

Fixed a bug in qiskit.pulse.utils.format_parameter_value() function that unintentionally converts large enough integer numbers into float values or causes unexpected rounding. See #11971 for details.

Fix an issue in the QDrift class where the coefficients of the Hamiltonian were previously force to be positive by taking the absolute value of each coefficient. This has been corrected so that the negative coeffients’ signs are added back.

A bug has been fixed in convert_durations_to_dt() where the function would blindly apply a conversion from seconds to dt on circuit durations, independently of the original units of the attribute. This could lead to wrong orders of magnitude in the reported circuit durations.

Fixed SparsePauliOp.apply_layout() to work correctly with zero-qubit operators. For example, if you previously created a 0 qubit and applied a layout like:


op = SparsePauliOp("")
op.apply_layout(None, 3)
this would have previously raised an error. Now this will correctly return an operator of the form: SparsePauliOp(['III'], coeffs=[1.+0.j])

Fixed an oversight in the Commuting2qGateRouter transpiler pass where the qreg permutations were not added to the pass property set, so they would have to be tracked manually by the user. Now it’s possible to access the permutation through the output circuit’s layout property and plug the pass into any transpilation pipeline without loss of information.

Fixed a floating-point imprecision when scaling certain pulse units between seconds and nanoseconds. If the pulse was symbolically defined, an unnecessary floating-point error could be introduced by the scaling for certain builds of symengine, which could manifest in unexpected results once the symbols were fully bound. Fixed #12392.

The preset pass managers of transpile() will no longer fail on circuits with control flow, if no hardware target or basis-gate set is specified. They will now treat such abstract targets as permitting all control-flow operations. Fixed #11906.

The method qiskit.instruction.Instruction.soft_compare() is meant to compare whether two gates match in their name, number of qubits, number of clbits, and the number of parameters. However, there was a typo where it would not check the number of qubits and number of clbits for a match. This resolves the apparent typo.

The default init plugin was not properly raising a TranspilerError when called with an invalid optimization level.

Fixed an issue with the Operator.from_circuit() constructor method where it would incorrectly interpret the final layout permutation resulting in an invalid Operator being constructed. Previously, the final layout was processed without regards for the initial layout, i.e. the initialization was incorrect for all quantum circuits that have a non-trivial initial layout.

Fixed a performance issue in PassManager.run() when it is running over multiple circuits in parallel. It will no longer spend time serializing the PassManager (which is a requirement for parallel execution) when given multiple inputs if it is only going to process the inputs serially.

Parameter was updated so that instances that compare equal always have the same hash. Previously, only the Parameter.uuid was compared, so Parameter instances with different names could compare equal if they had been constructed using a common value for the uuid parameter (which is usually not passed explicitly).

Fixed a bug in plot_coupling_map() that caused the edges of the coupling map to be colored incorrectly. Fixed #12369.

The OpenQASM 2.0 parser (qasm2.load() and qasm2.loads()) can now evaluate gate-angle expressions including integer operands that would overflow the system-size integer. These will be evaluated in a double-precision floating-point context, just like the rest of the expression always has been. However, an arbitrarily large integer will not necessarily be exactly representable in double-precision floating-point, so there is a chance that however the circuit was generated, it had already lost all numerical precision modulo 
2
π
2π.

Parameter instances used as stand-ins for input variables in OpenQASM 3 programs will now have their names escaped to avoid collisions with built-in gates during the export to OpenQASM 3. Previously there could be a naming clash, and the exporter would generate invalid OpenQASM 3.

Fixed bug in QuantumCircuit.draw() that was causing custom style dictionaries for the Matplotlib drawer to be modified upon execution.

QuantumCircuit.append() with copy=True (its default) will now correctly copy instructions parametrized by ParameterExpression instances, and not just by Parameter instances.

The internal handling of custom circuit calibrations and InstructionDurations has been offloaded from the transpile() function to the individual transpiler passes: DynamicalDecoupling, DynamicalDecoupling. Before, instruction durations from circuit calibrations would not be taken into account unless they were manually incorporated into instruction_durations input argument, but the passes that need it now analyze the circuit and pick the most relevant duration value according to the following priority order: target > custom input > circuit calibrations.

Fixed a bug in transpile() where the num_processes argument would only be used if dt or instruction_durations were provided.

Other Notes
Support for the arm64 macOS platform has been promoted from Tier 3 to Tier 1. Previously the platform was at Tier 3 because there was no available CI environment for testing Qiskit on the platform. Now that Github has made an arm64 macOS environment available to open source projects [1] we’re testing the platform along with the other Tier 1 supported platforms.

[1]

https://github.blog/changelog/2024-01-30-github-actions-introducing-the-new-m1-macos-runner-available-to-open-source/

1.0.0rc1
Providers Upgrade Notes
The deprecated qiskit.providers.fake_provider module has been migrated to the qiskit-ibm-runtime Python package. For this reason, the following elements in the qiskit.providers.fake_provider have been removed following their deprecation in Qiskit 0.46:

qiskit.providers.fake_provider.FakeProvider
qiskit.providers.fake_provider.FakeProviderForBackendV2
qiskit.providers.fake_provider.FakeProviderFactory
qiskit.providers.fake_provider.fake_backends.FakeBackendV2
any fake backend contained in qiskit.providers.fake_provider.backends (accessible through the provider)
qiskit.providers.fake_provider.FakeQasmSimulator
qiskit.providers.fake_provider.FakeJob
qiskit.providers.fake_provider.FakeQobj
To use the new fake provider module, you can run pip install qiskit-ibm-runtime and replace the qiskit import path (qiskit.providers.fake_provider) with the new import path (qiskit_ibm_runtime.fake_provider). Migration example:


# Legacy path
from qiskit.providers.fake_provider import FakeProvider, FakeSherbrooke
backend1 = FakeProvider().get_backend("fake_ourense")
backend2 = FakeSherbrooke()
 
# New path
# run "pip install qiskit-ibm-runtime"
from qiskit_ibm_runtime.fake_provider import FakeProvider, FakeSherbrooke
backend1 = FakeProvider().get_backend("fake_ourense")
backend2 = FakeSherbrooke()
Additionally, the following fake backends designed for special testing purposes have been superseded by the new GenericBackendV2 class, and are also removed following their deprecation in Qiskit 0.46:

qiskit.providers.fake_provider.fake_backend_v2.FakeBackendV2
`qiskit.providers.fake_provider.fake_backend_v2.FakeBackendV2LegacyQubitProps
qiskit.providers.fake_provider.fake_backend_v2.FakeBackend5QV2
qiskit.providers.fake_provider.fake_backend_v2.FakeBackendSimple
Migration example to the new GenericBackendV2 class:


# Legacy path
from qiskit.providers.fake_provider import FakeBackend5QV2
backend = FakeBackend5QV2()
 
# New path
from qiskit.providers.fake_provider import GenericBackendV2
backend = GenericBackendV2(num_qubits=5)
# note that this class will generate 5q backend with generic
# properties that serves the same purpose as FakeBackend5QV2
# but will generate different results
