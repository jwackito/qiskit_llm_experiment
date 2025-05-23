Qiskit 1.0 release notes
1.0.2
Prelude
Qiskit 1.0.2 is a minor bugfix release for the 1.0 series.

Bug Fixes
Fixed an issue with convert_to_target() where the converter would incorrectly ignore control flow instructions if they were specified in the BackendConfiguration.supported_instructions attribute, which is the typical location that control flow instructions are specified in a BackendConfiguration object. Fixed #11872.

Calling EquivalenceLibrary.set_entry() will now correctly update the internal graph object of the library. Previously, the metadata would be updated, but the graph structure would be unaltered, meaning that users like BasisTranslator would still use the old rules. Fixed #11958.

The EvolvedOperatorAnsatz now correctly handles the case where the operators argument is an empty list. Previously, this would result in an error.

Fixed a consistency issue with EvolvedOperatorAnsatz instances with zero qubits. Previously, such instances would contain a single QuantumRegister in qregs with zero qubits, but now no registers are created. This behavior aligns more consistently with its superclass QuantumCircuit.

Fixed a crash in convert_to_target() which would occur when qubit properties (either T1, T2 or frequency) were missing. The missing property values in QubitProperties are now filled with None.

Fixed a performance issue in the qpy.load() function when deserializing QPY payloads with large numbers of qubits or clbits in a circuit.

Fixed a bug where EstimatorPub.coerce() and SamplerPub.coerce() improperly handled a parameter of type BindingsArray. Previously a ValueError exception was falsely raised.

The preset pass managers used by transpile() will no longer fail on circuits with control flow when no hardware target or basis-gate set is specified. They will now treat such abstract targets as permitting all control-flow operations. Fixed #11906.

Fixed coerce() so that it returns a 0-d array when the input is a single, unnested observable. Previously, it erroneously upgraded to a single dimension, with shape (1,).

Parameter was updated so that instances that compare equal always have the same hash. Previously, only the Parameter.uuid was compared, so Parameter instances with different names could compare equal if they had been constructed using a common value for the uuid parameter (which is usually not passed explicitly).

Fixed bug in QuantumCircuit.draw() that was causing custom style dictionaries for the Matplotlib drawer to be modified upon execution.

1.0.1
Prelude
Qiskit 1.0.1 is a patch release fixing a small number of bugs identified in the Qiskit 1.0.0 release.

Bug Fixes
Fixed a bug in the conversion of custom pulse instructions to the legacy qiskit.qobj format. The bug was introduced in Qiskit 1.0.0 and caused conversion of instructions with custom pulse shapes to raise an error. After the fix, the conversion is carried out correctly, and the custom pulse is converted to a pulse.Waveform as it should. Fixed #11828.

Fixed an issue in the InverseCancellation transpiler pass where in some cases it would incorrectly cancel a self-inverse parameterized gate even if the parameter value didn’t match. Fixed #11815.

BasePassManager.run() will no longer leak the previous PropertySet into new workflows when called more than once. Previously, the same PropertySet as before would be used to initialize follow-on runs, which could mean that invalid property information was being given to tasks. The behavior now matches that of Qiskit 0.44. Fixed #11784.

A bug has been fixed in convert_durations_to_dt() where the function assumed its inputs were all in seconds, rather than reading the actual unit. This could lead to wrong orders of magnitude in the reported circuit durations.

1.0.0
Prelude
We are very pleased to release Qiskit 1.0.0. This release is the culmination of 7 years of development to mature Qiskit into a stable, high- performance SDK for quantum computing, and is the start of a new era for the Qiskit project and community. Besides general performance and stability improvements, the most significant changes with the 1.0.0 release relate to the stability policy, release cycles, and versioning. Qiskit is now formally using semantic versioning, and this means that, for the entire lifecycle of the 1.x release series, the project is committed to maintaining backwards compatibility in its public documented APIs. We’re also now starting to offer bugfix support for major versions, so that you continue to have a supported branch for 6 months after the release of the next major version. This starts now with the 1.x and 0.x major series: the 0.46.x release will continue to be supported, with periodic patch releases that contain bug fixes, for 6 months after the release of 1.0. That is, 0.46.x will be supported until 2024-08. You can see the full details of the new policy here:

start/install#qiskit-versioning

Also of key importance in this release is the change in packaging. Since the Qiskit 0.7 release in 2018-12, when Qiskit introduced its elements model, the qiskit package you would install has been a meta-package (or package of packages) that installs the combined elements comprising Qiskit. As announced in previous releases (for more details see the 0.44.0, 0.45.3, and 0.46.0 release notes, along with this blog post) with the 1.0 release we’re completing a transition to have a single qiskit package exposing only the core SDK (what was previously qiskit-terra). This means that for releases >= 1.0.0, we have stopped using the qiskit-terra package and will only be publishing qiskit. As this change in packaging structure is not fully supported by the Python package installer pip, it is not possible to just use pip install -U qiskit to upgrade from qiskit 0.46.0 to 1.0.0. It is strongly recommended that to upgrade to Qiskit 1.0.0 you create a separate virtual environment to isolate the installation. There is a detailed migration guide that explains the packaging changes and how to install Qiskit 1.0.0 in different scenarios which can be found here:

https://qisk.it/1-0-packaging-migration

As with all of our major releases, Qiskit 1.0.0 also has a plethora of new features, the highlights for this release are:

The QuantumCircuit class’s internal data structure has been rewritten in Rust to greatly improve the memory efficiency of the QuantumCircuit objects by caching the arguments of the instructions.
A new version of the primitives interface definition in qiskit.primitives with the BaseSamplerV2 and BaseEstimatorV2 abstract classes. This new version of the interface adds support for performing vectorized calls to the primitive so that sweeps over parameter value sets and observables can be efficiently specified.
A new experimental native OpenQASM 3 parser qiskit.qasm3.loads_experimental() and qiskit.qasm3.load_experimental(). This new parser is still under development and still has several limitations and is still experimental. However, for where it is usable, the new parser is significantly faster and has better diagnostic error message that allows to debug where an OpenQASM 3 program is invalid. This new parser is written in Rust and based on a newly developed Rust library for parsing OpenQASM3 which can be found here: https://github.com/Qiskit/openqasm3_parser
Finally, the Qiskit 1.0.0 release was an opportunity to clean up some technical debt accumulated over the past 7 years of development. You’ll notice that the Qiskit 1.0.0 release is virtually free of DeprecationWarnings being emitted, and, at the same time, the upgrade section of the 1.0.0 release notes is longer than usual. These are direct consequences of the technical debt cleanup. To help with the migration from 0.46.x to 1.0.0, besides the release notes, we have also published a dedicated migration guide which can be found here:

Qiskit 1.0 feature changes

This guide is meant to complement the release notes and have a targeted advice for how to migrate the API changes after the removal of the deprecated functionality from the 0.46.0 release.

Circuits Features
Added a new argument, annotated, to the methods QuantumCircuit.inverse(), circuit.Instruction.inverse() and .inverse() methods of Instruction subclasses (such as SwapGate or SGate) to optionally return an AnnotatedOperation. The default value of annotated is False and corresponds to the pre-existing behavior of the method. Furthermore, for standard gates with an explicitly defined inverse method, the argument annotated has no effect, for example, both:


SwapGate().inverse(annotated=False)
SwapGate().inverse(annotated=True)
return a SwapGate, and both:


SGate().inverse(annotated=False)
SGate().inverse(annotated=True)
return an SdgGate. The difference manifests for custom instructions without an explicitly defined inverse. With annotated=False, the method returns a fresh instruction with the recursively inverted definition, just as before. While annotated=True returns an AnnotatedOperation that represents the instruction modified with the InverseModifier.

Added a commutation library to the CommutationChecker. This library stores all the commutation relations of unparameterizable standard gates into a dictionary that allows for efficient lookup at runtime. This speeds up the execution of the CommutationChecker class and, by extension, the CommutationAnalysis transpiler pass, as instead of computing whether two unparameterizable standard gates commute it just has to look it up from the library.

Additionally, the CommutationChecker was refactored and now has an upper limit set on the number of cached commutation relations that are not in the commutation library. This addressed: #8020 and #7101

QuantumCircuit.assign_parameters() now accepts string keys in the mapping form of input. These names are used to look up the corresponding Parameter instance using get_parameter(). This lets you do:


from qiskit.circuit import QuantumCircuit, Parameter
 
a = Parameter("a")
qc = QuantumCircuit(1)
qc.rx(a, 0)
 
qc.assign_parameters({"a": 1}) == qc.assign_parameters({a: 1})
QuantumCircuit has two new methods, get_parameter() and has_parameter(), which respectively retrieve a Parameter instance used in the circuit by name, and return a boolean of whether a parameter with a matching name (or the exact instance given) are used in the circuit.

A uuid property was added to the qiskit.circuit.Parameter class. In advanced use cases, this property can be used for creating qiskit.circuit.Parameter instances that compare equal to each other.

Added a new method, ParameterExpression.numeric(), which converts a fully bound parameter expression into the most restrictive built-in Python numeric type that accurately describes the result of the symbolic evaluation. For example, a symbolic integer will become an int, while a symbolic real number will become a float and a complex number will become a complex. This method includes several workarounds for peculiarities of the evaluation contexts of symengine, which can sometimes lead to spurious results when calling complex or float on an expression directly.

Primitives Features
Version 2 of the primitives is introduced via a new base class for both the sampler and the estimator, along with new types for their inputs and outputs. The emphasis of this new version is on performing vectorized calls to the primitive run() methods, so that sweeps over parameter value sets and observables can be efficiently specified. See StatevectorSampler and StatevectorEstimator for reference implementations of the V2 primitives.

Moreover, the estimator has gained a precision argument in the run() method that specifies the targeted precision of the expectation value estimates. Analogously, the sampler has moved shots out of the options and into the arguments of the run() method. The sampler has also been changed to return the outputs (e.g. bitstrings) from every shot, rather than providing a Counts-like return, and also to store data from separate ClassicalRegisters . This enables derived classes to implement sampler support for circuits with classical control flow.

The primitive V2 base classes are:

BaseSamplerV2
BaseEstimatorV2
The new types which are used for inputs and outputs are:

SamplerPubLike: primitive unified bloc (PUB) of sampler inputs; a union type of allowed inputs to a sampler
EstimatorPubLike: Primitive unified bloc (PUB) of estimator inputs; a union type of allowed inputs to an estimator
PubResult: the data and metadata resulting from a single PUB’s execution
DataBin: A namespace to hold data from a single PUB’s execution
BitArray: an array-valued collection of bit values in a dense format
PrimitiveResult: an iterable of PubResults along with metadata
The reference implementation StatevectorEstimator of BaseEstimatorV2 was added. As seen in the example below, this estimator (and all V2 estimators) supports providing arrays of observables and/or arrays of parameter value sets that are attached to particular circuits.

Each tuple of (circuit, observables, <optional> parameter values, <optional> precision), called an estimator primitive unified bloc (PUB), produces its own array-based result. The run() method can be given many pubs at once.


from qiskit.circuit import Parameter, QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import Pauli, SparsePauliOp
 
import matplotlib.pyplot as plt
import numpy as np
 
# Define a circuit with two parameters.
circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)
circuit.ry(Parameter("a"), 0)
circuit.rz(Parameter("b"), 0)
circuit.cx(0, 1)
circuit.h(0)
 
# Define a sweep over parameter values, where the second axis is over
# the two parameters in the circuit.
params = np.vstack([
    np.linspace(-np.pi, np.pi, 100),
    np.linspace(-4 * np.pi, 4 * np.pi, 100)
]).T
 
# Define three observables. Many formats are supported here including
# classes such as qiskit.quantum_info.SparsePauliOp. The inner length-1
# lists cause this array of observables to have shape (3, 1), rather
# than shape (3,) if they were omitted.
observables = [
    [SparsePauliOp(["XX", "IY"], [0.5, 0.5])],
    [Pauli("XX")],
    [Pauli("IY")]
]
 
# Instantiate a new statevector simulation based estimator object.
estimator = StatevectorEstimator()
 
# Estimate the expectation value for all 300 combinations of
# observables and parameter values, where the pub result will have
# shape (3, 100). This shape is due to our array of parameter
# bindings having shape (100,), combined with our array of observables
# having shape (3, 1)
pub = (circuit, observables, params)
job = estimator.run([pub])
 
# Extract the result for the 0th pub (this example only has one pub).
result = job.result()[0]
 
# Error-bar information is also available, but the error is 0
# for this StatevectorEstimator.
result.data.stds
 
# Pull out the array-based expectation value estimate data from the
# result and plot a trace for each observable.
for idx, pauli in enumerate(observables):
    plt.plot(result.data.evs[idx], label=pauli)
plt.legend()
The reference implementation StatevectorSampler of BaseSamplerV2 was added. As seen in the example below, this sampler (and all V2 samplers) supports providing arrays of parameter value sets to bind against a single circuit.

Each tuple of (circuit, <optional> parameter values, <optional> shots), called a sampler primitive unified bloc (PUB), produces its own array-based result. The run() method can be given many pubs at once.


from qiskit.circuit import (
    Parameter, QuantumCircuit, ClassicalRegister, QuantumRegister
)
from qiskit.primitives import StatevectorSampler
 
import matplotlib.pyplot as plt
import numpy as np
 
# Define our circuit registers, including classical registers
# called 'alpha' and 'beta'.
qreg = QuantumRegister(3)
alpha = ClassicalRegister(2, "alpha")
beta = ClassicalRegister(1, "beta")
 
# Define a quantum circuit with two parameters.
circuit = QuantumCircuit(qreg, alpha, beta)
circuit.h(0)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.ry(Parameter("a"), 0)
circuit.rz(Parameter("b"), 0)
circuit.cx(1, 2)
circuit.cx(0, 1)
circuit.h(0)
circuit.measure([0, 1], alpha)
circuit.measure([2], beta)
 
# Define a sweep over parameter values, where the second axis is over.
# the two parameters in the circuit.
params = np.vstack([
    np.linspace(-np.pi, np.pi, 100),
    np.linspace(-4 * np.pi, 4 * np.pi, 100)
]).T
 
# Instantiate a new statevector simulation based sampler object.
sampler = StatevectorSampler()
 
# Start a job that will return shots for all 100 parameter value sets.
pub = (circuit, params)
job = sampler.run([pub], shots=256)
 
# Extract the result for the 0th pub (this example only has one pub).
result = job.result()[0]
 
# There is one BitArray object for each ClassicalRegister in the
# circuit. Here, we can see that the BitArray for alpha contains data
# for all 100 sweep points, and that it is indeed storing data for 2
# bits over 256 shots.
assert result.data.alpha.shape == (100,)
assert result.data.alpha.num_bits == 2
assert result.data.alpha.num_shots == 256
 
# We can work directly with a binary array in performant applications.
raw = result.data.alpha.array
 
# For small registers where it is anticipated to have many counts
# associated with the same bitstrings, we can turn the data from,
# for example, the 22nd sweep index into a dictionary of counts.
counts = result.data.alpha.get_counts(22)
 
# Or, convert into a list of bitstrings that preserve shot order.
bitstrings = result.data.alpha.get_bitstrings(22)
print(bitstrings)
Providers Features
Added a new class, GenericBackendV2, to the qiskit.providers.fake_provider module. This class is configurable, and builds a BackendV2 backend instance that can be run locally (in the spirit of fake backends). Users can configure the number of qubits, basis gates, coupling map, ability to run dynamic circuits (control flow instructions), instruction calibrations and measurement timestep of the backend without having to deal with manual target construction. Qubit and gate properties (duration, error) are generated by randomly sampling from default ranges. The seed for this random generation can be fixed to ensure the reproducibility of the backend output. It’s important to note that this backend only supports gates in the standard library. If you need a more flexible backend, there is always the option to directly instantiate a Target object to use for transpilation.

Example usage 1:


from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import GenericBackendV2
 
# Create a simple circuit
circuit = QuantumCircuit(3)
circuit.h(0)
circuit.cx(0,1)
circuit.cx(0,2)
circuit.measure_all()
circuit.draw('mpl')
 
# Define backend with 3 qubits
backend = GenericBackendV2(num_qubits=3)
 
# Transpile and run
transpiled_circuit = transpile(circuit, backend)
result = backend.run(transpiled_circuit).result()
Example usage 2:


from qiskit import QuantumCircuit, ClassicalRegister, transpile
from qiskit.providers.fake_provider import GenericBackendV2
 
# Create a circuit with classical control
creg = ClassicalRegister(19)
qc = QuantumCircuit(25)
qc.add_register(creg)
qc.h(0)
for i in range(18):
    qc.cx(0, i + 1)
for i in range(18):
    qc.measure(i, creg[i])
with qc.if_test((creg, 0)):
    qc.ecr(20, 21)
 
# Define backend with custom basis gates and control flow instructions
backend = GenericBackendV2(
    num_qubits=25,
    basis_gates=["ecr", "id", "rz", "sx", "x"],
    control_flow=True,
  )
 
#Transpile
transpiled_qc = transpile(qc, backend)
Note
The noise properties generated by these class do not mimic any concrete quantum device, and should not be used to measure any concrete behaviors. They are “reasonable defaults” that can be used to test backend-interfacing functionality not tied specific noise values of real quantum systems. For a more accurate simulation of existing devices, you can manually build a noise model from the real backend using the functionality offered in qiskit_aer.

The qiskit.providers.fake_provider module now includes a series of generic fake backends following the BackendV1 interface. They have been introduced as an alternative to the snapshot-based fake backends exposed in the deprecated FakeProvider (FakeVigo, FakeTokyo, etc). The list of new fake backends includes:

Backends without pulse capabilities:

Fake5QV1
Fake20QV1
Backends with pulse capabilities:

Fake7QPulseV1
Fake27QPulseV1
Fake127QPulseV1
They can be imported following the pattern: from qiskit.providers.fake_provider import Fake5QV1. More details on the backend properties can be found on each backend’s API documentation.

OpenQASM Features
The qiskit.qasm3 package now contains a built-in, Rust-based parser for reading OpenQASM 3 programs into QuantumCircuits, found at qiskit.qasm3.load_experimental() and loads_experimental(). These are typically several times faster than the existing, pure Python load() and loads() functions, which additionally require qiskit-qasm3-import to be installed.

For example, we can create a 20,000-instruction entangling QuantumCircuit:


import numpy as np
import qiskit.qasm3
from qiskit.circuit.library import RealAmplitudes
 
qc = RealAmplitudes(100, reps=100, flatten=True)
qc = qc.assign_parameters(np.random.rand(qc.num_parameters))
oq3 = qiskit.qasm3.dumps(qc)
The old qasm3.loads() took about 7.3s to load the resulting OpenQASM 3 program, whereas qasm3.loads_experimental() took under 300ms on a consumer Macbook Pro (i7, 2020)–a speedup of 25x!

The supported feature set of the experimental parser is very limited in this preview version, but this will expand as both the Qiskit side and the native Rust-based parser improve.

One of our main goals with this new parser, alongside the huge speed improvements, is to provide top-quality error diagnostics. As with other parts of the parser, these are a work in progress, but you’ll start to see much higher quality error messages displayed when parsing invalid OpenQASM 3 programs with the experimental parser.

The OpenQASM 3 exporter (see dump() and dumps() functions in qiskit.qasm3) now supports the stabilized syntax of the switch statement in OpenQASM 3 by default. The pre-certification syntax of the switch statement is still available by using the ExperimentalFeatures.SWITCH_CASE_V1 flag in the experimental argument of the exporter. There is no feature flag required for the stabilized syntax, but if you are interfacing with other tooling that is not yet updated, you may need to pass the experimental flag.

The syntax of the stabilized form is slightly different with regards to terminating break statements (no longer required nor permitted), and multiple cases are now combined into a single case line, rather than using C-style fall-through. For more detail, see the OpenQASM 3 documentation on the switch-case construct.

QPY Features
Added a new warning class, QPYLoadingDeprecatedFeatureWarning, to the QPY module. This class allows for deprecation warnings to surface even if the deprecated feature is accessed at a variable point in the call stack, as is the case for many QPY loading functions that are called recursively.

Added a new flag, version, to the qpy.dump() function. This allows qpy.dump() to optionally take an integer value for the QPY Format version to emit. This is useful if you need to generate a QPY file that will be loaded by an older version of Qiskit. However, the supported versions to emit are limited, only versions between the latest QPY version (which is the default), and the compatibility QPY version which is Version 10 (which was introduced in Qiskit 0.45.0) can be used. The compatibility version will remain fixed for the entire 1.x.y major version release series. This does not change the backwards compatibility guarantees of the QPY format when calling qpy.load(), it just enables users to emit an older version of QPY to maintain compatibility and interoperability between the 0.x and 1.x release series.

Quantum Information Features
Added a qiskit.quantum_info.StabilizerState.from_stabilizer_list() method that generates a stabilizer state from a list of stabilizers:


from qiskit.quantum_info import StabilizerState
 
stabilizer_list = ["ZXX", "-XYX", "+ZYY"]
stab = StabilizerState.from_stabilizer_list(stabilizer_list)
SparsePauliOp.from_operator() now uses an implementation of the “tensorized Pauli decomposition algorithm” presented in Hatznko, Binkowski and Gupta (2023). The method is now several orders of magnitude faster; for example, it is possible to decompose a random 10-qubit operator in around 250ms on a consumer Macbook Pro (Intel i7, 2020).

Synthesis Features
Added a qiskit.synthesis.synth_circuit_from_stabilizers() function that returns a circuit that outputs the state stabilized by a series of given stabilizers.

The AQC unitary synthesis plugin method now uses a faster objective function evaluation by default, which results in substantial improvement in synthesis time.

Add a new synthesis method synth_qft_line() of a QFT circuit for linear nearest-neighbor connectivity, which significantly reduces the number of SWAPs for large numbers of qubits compared to SABRE.

The class TwoQubitWeylDecomposition has been added to the public API in qiskit.synthesis. This class allows to apply the Weyl decomposition of two-qubit unitaries. If you were previously importing this while it was a non-public class in the now-removed qiskit.quantum_info.synthesis module, you should update your import paths.

Transpiler Features
Added a new exception class: InvalidLayoutError. This is a TranspilerError subclass which is raised when a user provided layout is invalid (mismatched size, duplicate qubits, etc).

Added a new keyword argument, num_processes, to transpile() and the PassManager.run() method. This allows for overriding both QISKIT_NUM_PROCS and the num_processes field in user configuration files on a per-transpile basis. For example:


from qiskit import transpile, QuantumCircuit
 
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()
 
transpile([qc]*10, basis_gates=['u', 'cz'], num_processes=2)
will run the transpile over the 10 input circuits using only 2 processes and will override the system default, environment variable, or user configuration file for that transpile() call.

Added a new transpiler pass, OptimizeAnnotated, that optimizes annotated operations on a quantum circuit.

Consider the following example:


from qiskit.circuit import QuantumCircuit
from qiskit.circuit.annotated_operation import (
    AnnotatedOperation,
    InverseModifier,
    ControlModifier,
)
from qiskit.circuit.library import CXGate, SwapGate
from qiskit.transpiler.passes import OptimizeAnnotated
 
# Create a quantum circuit with multiple annotated gates
gate1 = AnnotatedOperation(
    SwapGate(),
    [InverseModifier(), ControlModifier(2), InverseModifier(), ControlModifier(1)],
)
gate2 = AnnotatedOperation(
    SwapGate(),
    [InverseModifier(), InverseModifier()]
)
gate3 = AnnotatedOperation(
    AnnotatedOperation(CXGate(), ControlModifier(2)),
    ControlModifier(1)
)
qc = QuantumCircuit(6)
qc.append(gate1, [3, 2, 4, 0, 5])
qc.append(gate2, [1, 5])
qc.append(gate3, [5, 4, 3, 2, 1])
 
# Optimize the circuit using OptimizeAnnotated transpiler pass
qc_optimized = OptimizeAnnotated()(qc)
 
# This is how the optimized circuit should look like
gate1_expected = AnnotatedOperation(SwapGate(), ControlModifier(3))
gate2_expected = SwapGate()
gate3_expected = AnnotatedOperation(CXGate(), ControlModifier(3))
qc_expected = QuantumCircuit(6)
qc_expected.append(gate1_expected, [3, 2, 4, 0, 5])
qc_expected.append(gate2_expected, [1, 5])
qc_expected.append(gate3_expected, [5, 4, 3, 2, 1])
 
assert qc_optimized == qc_expected
In the case of gate1, the modifiers of the annotated swap gate are brought into the canonical form: the two InverseModifiers cancel out, and the two ControlModifiers are combined. In the case of gate2, all the modifiers get removed and the annotated operation is replaced by its base operation. In the case of gate3, multiple layers of annotations are combined into one.

The constructor of the OptimizeAnnotated pass accepts optional arguments target, equivalence_library, basis_gates and recurse. When recurse is True (the default value) and when either target or basis_gates are specified, the pass recursively descends into the gate’s definition circuits, with the exception of gates that are already supported by the target or that belong to the equivalence library. On the other hand, when neither target nor basis_gates are specified, or when recurse is set to False, the pass synthesizes only the “top-level” annotated operations, i.e. does not recursively descend into the definition circuits. This behavior is consistent with that of the HighLevelSynthesis transpiler pass, which needs to be called in order to “unroll” the annotated operations into 1-qubit and 2-qubits gates.

Added a new HighLevelSynthesisPlugin for PermutationGate objects based on Qiskit’s token swapper algorithm. To use this plugin, specify token_swapper when defining high-level-synthesis config.

This synthesis plugin is able to run before or after the layout is set. When synthesis succeeds, the plugin outputs a quantum circuit consisting only of swap gates. When synthesis does not succeed, the plugin outputs None.

The following code illustrates how the new plugin can be run:


from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import PermutationGate
from qiskit.transpiler import PassManager, CouplingMap
from qiskit.transpiler.passes.synthesis.high_level_synthesis import HighLevelSynthesis, HLSConfig
 
# This creates a circuit with a permutation gate.
qc = QuantumCircuit(8)
perm_gate = PermutationGate([0, 1, 4, 3, 2])
qc.append(perm_gate, [3, 4, 5, 6, 7])
 
# This defines the coupling map.
coupling_map = CouplingMap.from_ring(8)
 
# This high-level-synthesis config specifies that we want to use
# the "token_swapper" plugin for synthesizing permutation gates,
# with the option to use 10 trials.
synthesis_config = HLSConfig(permutation=[("token_swapper", {"trials": 10})])
 
# This creates the pass manager that runs high-level-synthesis on our circuit.
# The option use_qubit_indices=True indicates that synthesis is run after the layout is set,
# and hence should preserve the specified coupling map.
pm = PassManager(
    HighLevelSynthesis(
        synthesis_config, coupling_map=coupling_map, target=None, use_qubit_indices=True
    )
)
 
qc_transpiled = pm.run(qc)
Added two new arguments, matrix_based and max_qubits, to the constructor of the CommutativeInverseCancellation transpiler pass. When matrix_based is True, the pass uses matrix representations to check whether two operations are the inverse of each other. This makes the checks more powerful, and in addition allows for cancelling pairs of operations that are inverse up to a phase, while updating the global phase of the circuit accordingly. This generally leads to more reductions at the expense of increased runtime. The argument max_qubits limits the number of qubits in matrix-based commutativity and inverse checks. For example:


import numpy as np
from qiskit.circuit import QuantumCircuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import CommutativeInverseCancellation
 
circuit = QuantumCircuit(1)
circuit.rz(np.pi / 4, 0)
circuit.p(-np.pi / 4, 0)
 
passmanager = PassManager(CommutativeInverseCancellation(matrix_based=True))
new_circuit = passmanager.run(circuit)
The pass is able to cancel the RZ and P gates, while adjusting the circuit’s global phase to 
15
π
8
8
15π
​
 .

Added a new function, high_level_synthesis_plugin_names(), that can be used to get the list of installed high level synthesis plugins for a given operation name.

Visualization Features
The text and mpl outputs for the QuantumCircuit.draw() and circuit_drawer() circuit drawer functions will now display detailed information for operations of AnnotatedOperation. If the AnnotatedOperation.modifiers contains a ControlModifier, the operation will be displayed the same way as controlled gates. If the InverseModifier or PowerModifier is used, these will be indicated with the base operation name. For example:


from qiskit.circuit import (
    AnnotatedOperation,
    ControlModifier,
    PowerModifier,
    InverseModifier,
    QuantumCircuit
)
from qiskit.circuit.library import SGate
 
annotated_op = AnnotatedOperation(SGate(), [PowerModifier(3.4), ControlModifier(3), InverseModifier()])
qc = QuantumCircuit(4)
qc.append(annotated_op, range(4))
qc.draw("mpl")
_images/release_notes-1.png
Misc. Features
Added a new warning base class, QiskitWarning. While Qiskit will continue to use built-in Python warnings (such as DeprecationWarning) when those are most appropriate, for cases that are more specific to Qiskit, the warnings will be subclasses of QiskitWarning.

The optional-functionality testers (qiskit.utils.optionals) will now distinguish an optional dependency that was completely not found (a normal situation) with one that was found, but triggered errors during its import. In the latter case, they will now issue an OptionalDependencyImportWarning telling you what happened, since it might indicate a failed installation or an incompatible version.

Upgrade Notes
Qiskit 1.0 now requires version 0.14.0 of rustworkx. The minimum version requirement was raised to support the new token_swapper PermutationGate synthesis plugin for HighLevelSynthesisPlugin.

The minimum supported Rust version for building Qiskit from source is now 1.70. This has been raised from the previous minimum supported Rust version of 1.64 in the Qiskit 0.45.x and 0.46.0 release series.

The dependency on psutil has been removed. The psutil library was previously only used for detecting the number of physical CPUs and total system memory, however this information provided does not add sufficient value to justify the additional dependencies and overhead so it has been removed. This does mean that the default number of processes used by parallel_map() and functions that internally can use parallel_map() such as transpile() and PassManager.run() may use more or less parallel processes than in previous releases. If you’d like to adjust the number of processes used you can use the new num_processes argument to those functions, or the QISKIT_NUM_PROCS environment variable or num_processes field in a user configuration file (see the local configuration guide for more details) if you need to adjust the number of processes that Qiskit potentially uses.

The scoped_parameters and search_parameters methods have been removed from the ScheduleBlock class. These methods returned Parameter objects that partially linked to the parameters in the ScheduleBlock instance but assigning values using these objects did not work correctly. Users should use ScheduleBlock.parameters instead and iterate through ScheduleBlock.references and compare to the Schedule.parameters attributes of the subreferences when needing to distinguish which subroutine a parameter is used in. See #11654 for more information.

Removed logic for injecting QuantumCircuit and Gate operations into the pulse context (such as in pulse.builder.call()), which was legacy behavior deprecated in Qiskit 0.46. Pulse schedules should be built up as a full schedule context; circuits and gates are a higher level of abstraction.

This includes the removal of the related functions:

pulse.builder.call_gate
pulse.builder.cx
pulse.builder.u1
pulse.builder.u2
pulse.builder.u3
pulse.builder.x
pulse.builder.active_transpiler_settings
pulse.builder.active_circuit_scheduler_settings
pulse.builder.transpiler_settings
pulse.builder.circuit_scheduler_settings
The default_transpiler_settings and default_circuit_scheduler_settings arguments to pulse.builder.build() are similarly removed.


from qiskit import transpile, schedule, QuantumCircuit, pulse
from qiskit.providers.fake_provider import Fake7QPulseV1
 
backend = Fake7QPulseV1()
 
# Create a schedule from a hardware-based circuit.
qc = QuantumCircuit(2)
qc.cx(0, 1)
qc = transpile(qc, backend)
sched = schedule(qc, backend)
 
# These pulse schedules can still be called in builder contexts.
with pulse.build(backend) as qc_sched:
  pulse.call(sched)
 
# Schedules for certain operations can also be directly retrieved
# from BackendV1 instances:
sched = backend.defaults().instruction_schedule_map.get('x', (0,))
 
# ... and from BackendV2 instances:
sched = backend.target['x'][(0,)].calibration
The minimum version required for symengine was bumped to >=0.11.

Circuits Upgrade Notes
Removed the Instruction.qasm method, which was deprecated in Qiskit 0.45.0. Use qiskit.qasm2.dump() with a complete QuantumCircuit instead.

The properties Bit.register and Bit.index are removed. They were deprecated in Qiskit 0.25 (released in 2021-04). The qubits and bits now live only in the context of a QuantumCircuit. The alternative to the properties is to use QuantumCircuit.find_bit() to find all the containing registers within a circuit and the index of the bit within the circuit.

The method QuantumCircuit.bind_parameters has been removed, following its deprecation in Qiskit 0.45. You can use QuantumCircuit.assign_parameters() as a drop-in replacement with all its defaults, and it also exposes additional features over the old method.

Importing Int1, Int2, BooleanFunction, classical_function() from qiskit.circuit is now disabled. Instead, import the objects from the qiskit.circuit.classicalfunction submodule, which requires the tweedledum package.

The header and extension_lib data-only attributes from QuantumCircuit are removed following their deprecation in Qiskit 0.45. These were internal details of the OpenQASM 2 exporter which are no longer used.

Removed the qiskit.extensions module, which has been pending deprecation since the 0.45 release and has been fully deprecated in the 0.46 release. The following operations from this module are available in qiskit.circuit.library:

DiagonalGate,
HamiltonianGateGate,
Initialize,
Isometry,
MCGupDiag,
UCGate,
UCPauliRotGate,
UCRXGate,
UCRYGate,
UCRZGate,
UnitaryGate.
The following objects have been removed:

SingleQubitUnitary (instead use library.UnitaryGate),
Snapshot (superseded by Aer’s save instructions),
ExtensionError,
along with the following circuit methods:

QuantumCircuit.snapshot,
QuantumCircuit.squ,
QuantumCircuit.diagonal,
QuantumCircuit.hamiltonian,
QuantumCircuit.isometry and QuantumCircuit.iso,
QuantumCircuit.uc,
QuantumCircuit.ucrx,
QuantumCircuit.ucry,
QuantumCircuit.ucrz.
These operations can still be performed by appending the appropriate instruction to a quantum circuit.

Removed deprecated, duplicated QuantumCircuit methods. These include:

QuantumCircuit.cnot, instead use QuantumCircuit.cx(),
QuantumCircuit.toffoli, instead use QuantumCircuit.ccx(),
QuantumCircuit.fredkin, instead use QuantumCircuit.cswap(),
QuantumCircuit.mct, instead use QuantumCircuit.mcx(),
QuantumCircuit.i, instead use QuantumCircuit.id().
You can no longer set QuantumCircuit.metadata to be None, following deprecation in Qiskit 0.43.0. Its type is dict, so to clear it, set it to {}.

The attribute .Register.name_format has been removed following its deprecation in Qiskit 0.40.0. There is no restriction on register names any more, and the regular expression there was simply [a-z][a-zA-Z0-9_]*.

Primitives Upgrade Notes
Added the BasePrimitiveJob class as an abstract job class for primitives and made PrimitiveJob inherit BasePrimitiveJob instead of JobV1.
Providers Upgrade Notes
Changed default value of two arguments (add_delay and filter_faulty) in the convert_to_target() function. This conversion function now adds delay instructions and removes faulty instructions by default.

The BackendProperties and PulseDefaults model objects used by the FakeOpenPulse2Q have been updated to be internally consistent and add missing instructions. If you were relying on the previous model objects as a compilation target you can use the backend with Qiskit 0.46 and export a QuantumCircuit generated with transpile() and serialize it using qpy.dump to access it in this release.

The qiskit.providers.basicaer module, exposed as qiskit.BasicAer, has been removed following it deprecation on the 0.46 release. Its functionality has been replaced by the qiskit.quantum_info module and the new qiskit.providers.basic_provider module.

The migration from using qiskit.providers.basicaer (qiskit.BasicAer) to qiskit.providers.basic_provider can be performed as follows:

Migrate from	Replace with
qiskit.BasicAer	The new provider doesn’t have a global instance, imports should be from qiskit.providers.basic_provider
qiskit.providers.basicaer	basic_provider
BasicAerProvider	BasicProvider
BasicAerJob	BasicProviderJob
QasmSimulatorPy	BasicSimulator
UnitarySimulatorPy	use Operator
StatevectorSimulatorPy	use Statevector
A notable difference is that the new provider is no longer exposed through a global instance (like BasicAer), so it will not be valid to do from qiskit import BasicProvider. Instead, the provider class must be imported from its submodule and instantiated manually:


from qiskit.providers.basic_provider import BasicProvider
 
provider = BasicProvider()
backend = provider.get_backend("basic_simulator")
The following examples show the migration paths of the three simulators in BasicAer.

Statevector simulator:


from qiskit import QuantumCircuit
qc = QuantumCircuit(3)
qc.h(0)
qc.h(1)
qc.cx(1,2)
 
# Former path
from qiskit import BasicAer
backend = BasicAer.get_backend("statevector_simulator")
statevector = backend.run(qc).result().get_statevector()
 
# New path
from qiskit.quantum_info import Statevector
statevector = Statevector(qc)
Unitary simulator:


from qiskit import QuantumCircuit
qc = QuantumCircuit(3)
qc.h(0)
qc.h(1)
qc.cx(1,2)
 
# Former path
from qiskit import BasicAer
backend = BasicAer.get_backend("unitary_simulator")
result = backend.run(qc).result()
 
# New path
from qiskit.quantum_info import Operator
result = Operator(qc).data
Qasm simulator:


from qiskit import QuantumCircuit
qc = QuantumCircuit(3)
qc.h(0)
qc.h(1)
qc.cx(1,2)
qc.measure_all()
 
# Former path
from qiskit import BasicAer
backend = BasicAer.get_backend("qasm_simulator")
result = backend.run(qc).result()
 
# New path
from qiskit.providers.basic_provider import BasicProvider
backend = BasicProvider().get_backend("basic_simulator")
result = backend.run(qc).result()
# or, directly
from qiskit.providers.basic_provider import BasicSimulator
backend = BasicSimulator()
result = backend.run(qc).result()
Removed the ConfigurableFakeBackend class deprecated in Qiskit 0.46.0. Instead, a suitable FakeBackend can be used.

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
Pulse Upgrade Notes
Removed the deprecated class qiskit.pulse.instructions.Call No alternative pulse instruction is provided.

Removed deprecated methods in InstructionToQobjConverter and QobjToInstructionConverter. This includes

InstructionToQobjConverter.convert_acquire()
InstructionToQobjConverter.convert_bundled_acquires()
InstructionToQobjConverter.convert_set_frequency()
InstructionToQobjConverter.convert_shift_frequency()
InstructionToQobjConverter.convert_set_phase()
InstructionToQobjConverter.convert_shift_phase()
InstructionToQobjConverter.convert_delay()
InstructionToQobjConverter.convert_play()
InstructionToQobjConverter.convert_snapshot()
QobjToInstructionConverter.convert_acquire()
QobjToInstructionConverter.convert_set_phase()
QobjToInstructionConverter.convert_shift_phase()
QobjToInstructionConverter.convert_set_frequency()
QobjToInstructionConverter.convert_shift_frequency()
QobjToInstructionConverter.convert_delay()
QobjToInstructionConverter.bind_pulse()
QobjToInstructionConverter.convert_parametric()
QobjToInstructionConverter.convert_snapshot()
These public methods are all replaced with protected ones which are implicitly called from the single entry point, i.e. calling the class as like a function.

The class qiskit.pulse.library.ParametricPulse and all subclasses are removed. These were deprecated since Qiskit 0.39 (with qiskit-terra 0.22), released in 2022-10. Instead, use SymbolicPulse and check its documentation for details.

OpenQASM Upgrade Notes
The qasm() methods of the classes QuantumRegister and ClassicalRegister have been removed. There is no replacement necessary; these were an internal detail of a legacy implementation of the OpenQASM 2 exporter. To export a program to OpenQASM 2, use qasm2.dump() or qasm2.dumps().
QPY Upgrade Notes
The latest format version of QPY is now Version 11 and this is what is emitted by default when running qpy.dump().

The module path qiskit.circuit.qpy_serialization has been removed, following its deprecation in Qiskit 0.40.0. For QPY serialization, use qiskit.qpy, which is the new location.

Quantum Information Upgrade Notes
Removed the deprecated __getitem__/__setitem__ magic methods of Clifford. The methods were deprecated since Qiskit 0.44, released in 2023-07. Instead, index or iterate through the Clifford.tableau attribute.

Removed the qiskit.quantum_info.synthesis module, which has been deprecated since the 0.46 release. The following objects have been moved to qiskit.synthesis:

OneQubitEulerDecomposer has been moved to qiskit.synthesis.one_qubit
TwoQubitBasisDecomposer has been moved to qiskit.synthesis.two_qubits
XXDecomposer has been moved to qiskit.synthesis.two_qubits
two_qubit_cnot_decompose() has been moved to qiskit.synthesis.two_qubits
This function was removed, since it has already been deprecated in the 0.46 release: * cnot_rxx_decompose

These functions were removed, since they have already been deprecated in a previous release: * decompose_clifford (use synth_clifford_full() instead) * decompose_cnotdihedral (use synth_cnotdihedral_full() instead)

The functions process_fidelity(), average_gate_fidelity(), gate_error() and diamond_norm() will no longer attempt to coerce arbitrary inputs to their marked expected types, following the deprecation in Qiskit 0.25.0. Pass inputs of the marked types to each argument directly.

Synthesis Upgrade Notes
The following deprecated functions previously in qiskit.quantum_info have been removed. These functions were marked as deprecated in the Qiskit 0.40.0 release in 2023-01.

decompose_clifford: you should use the qiskit.synthesis.synth_clifford_full() function instead.
decompose_cnotdihedral: you should use the qiskit.synthesis.synth_cnotdihedral_full() function instead.
Transpiler Upgrade Notes
The deprecated method Target.aquire_alignment has been removed. It was marked as deprecated in Qiskit 0.43 (released 2023-05). The method Target.acquire_alignment() should be used instead.

Removed deprecated function qiskit.transpiler.preset_passmanagers.common.get_vf2_call_limit. Instead, use get_vf2_limits().

The implicit use of approximation_degree!=1.0 by default in the generate_preset_pass_manager() function has been disabled. The previous default could cause undue and unexpected approximations, especially in workloads involving Trotterization or similar runs of operations that are close, but decidedly not equal, to the identity.

This change brings the inner pass-manager generation defaults in line with transpile(), which was always the intention. See #8595 for more detail.

Removed the deprecated Unroller class in qiskit.transpiler.passes.basis. This class was deprecated in Qiskit 0.45 and use of it can be replaced by the combination usage of BasisTranslator and UnrollCustomDefinitions.

Note that BasisTranslator and UnrollCustomDefinitions take different arguments than Unroller, as they requires a EquivalenceLibrary object to be passed in.

Where previously Unroller(basis_gates) could be used, you can now use:


from qiskit.circuit.library.standard_gates.equivalence_library import (
    StandardEquivalenceLibrary as std_eqlib,
)
pm = PassManager([
    UnrollCustomDefinitions(std_eqlib, basis_gates)
    BasisTranslator(std_eqlib, basis_gates),
])
translated = pm.run(circuit)
The deprecated NoiseAdaptiveLayout transpiler pass has been removed. It was marked as deprecated in Qiskit 0.46.0. This pass has been largely superseded by VF2Layout and VF2PostLayout which will set a layout based on the reported noise characteristics of a backend. Along with the pass, the layout_method plugin "noise_adaptive" has been removed.

The deprecated CrosstalkAdaptiveSchedule transpiler pass has been removed. It was marked as deprecated in Qiskit 0.46.0. This pass was not usable any longer because its internal operation was dependent on custom properties being set in the BackendProperties payload of a BackendV1 instance. As no backends are setting these fields, the pass was removed. If you depend on the pass for a custom workflow you can use the version in Qiskit 0.46.x.

Removed the qiskit.transpiler.synthesis module, which has been deprecated since the 0.46 release. The following objects have been moved:

qiskit.transpiler.synthesis.aqc has been moved to qiskit.synthesis.unitary.aqc (except of qiskit.synthesis.unitary.aqc.AQCSynthesisPlugin).
qiskit.synthesis.unitary.aqc.AQCSynthesisPlugin has been moved to qiskit.transpiler.passes.synthesis.AQCSynthesisPlugin.
qiskit.transpiler.synthesis.graysynth() has been moved to qiskit.synthesis.synth_cnot_phase_aam().
qiskit.transpiler.synthesis.cnot_synth() has been moved to qiskit.synthesis.synth_cnot_count_full_pmh().
The target keyword alias when calling TwoQubitBasisDecomposer instances as functions has been removed following its deprecation in Qiskit 0.40.0. You should pass the argument positionally as the first argument, or use the new name unitary.

The specialized transpiler pass LinearFunctionsSynthesis has been removed following its deprecation in Qiskit 0.40.0. Since its deprecation it just has been a very thin wrapper around HighLevelSynthesis, which you should use instead.

The import path qiskit.transpiler.passes.scheduling.calibration_creators is removed. The transpiler passes it housed, RZXCalibrationBuilder and RZXCalibrationBuilderNoEcho can be imported directly from qiskit.transpiler.passes.

The import path qiskit.transpiler.passes.scheduling.rzx_templates is removed. You should import rzx_templates() from qiskit.transpiler.passes directly.

A pattern for the pass piepline construction was upgraded. The syntactic sugar shown below for instantiation of flow controller was removed.


from qiskit.transpiler import PassManager
 
pm = PassManager()
pm.append(my_pass, condition=condition_callable, do_while=do_while_callable)
Instead of using this keyword argument pattern, you should explicitly instantiate the flow controller.


from qiskit.passmanager import ConditionalController, DoWhileController
from qiskit.transpiler import PassManager
 
pm = PassManager()
pm.append(
  ConditionalController(
    DoWhileController(my_pass, do_while=do_while_callable),
    condition=condition_callable,
  )
)
Note that you can manage the pecking order of controllers when you want to nest them, which was not possible with keyword arguments. You can also build the pipeline with the constructor of the pass manager like below because there is no reason to call the append method now.


pm = PassManager(
  ConditionalController(
    DoWhileController(my_pass, do_while=do_while_callable),
    condition=condition_callable,
  )
)
The append method of built-in flow controllers was removed. This includes

ConditionalController.append
DoWhileController.append
FlowControllerLinear.append
The task pipeline in a flow controller is frozen, and it must be passed when the controller instance is created.

Removed the passess methods of PassManager and StagedPassManager that returned a representation of included passes in the form of list of dictionaries. However, this format doesn’t efficiently represent more complicated pass pipeline, which may include conditional branching and nested conditions. Instead of using this representation, please use following pattern


pm = PassManager(...)
pm.to_flow_controller().tasks
This directly returns a linearized base task instances in tuple format.

The max_iteration argument was removed from PassManager.append() and PassManager.replace().

The following legacy classes were removed from the pass manager and transpiler modules following their deprecation in Qiskit 0.46:

qiskit.passmanager.flow_controllers.FlowController
qiskit.transpiler.fencedobjs.FencedObject
qiskit.transpiler.fencedobjs.FencedPropertySet
qiskit.transpiler.fencedobjs.FencedDAGCircuit
qiskit.transpiler.runningpassmanager.RunningPassManager
Visualization Upgrade Notes
The default style for the circuit visualization using Matplotlib has been changed to "iqp", matching the IBM Quantum Platform.

The deprecated module qiskit.visualization.qcstyle has been removed. This module has been marked as deprecated since Qiskit 0.39.0. Instead you should use the qiskit.visualization.circuit.qcstyle.

The deprecated support for passing a QuasiDistribution, ProbDistribution, or a distribution dictionary to the data argument of the plot_histogram() visualization has been removed. This functionality was marked as deprecated in the Qiskit 0.39.0 release (2022-10). Instead if you would like to plot a histogram from a QuasiDistribution, ProbDistribution, or a distribution dictionary you should use the plot_distribution() function instead.

The link_interval_dt key of QiskitTimelineStyle has been removed. You should use the new name link_interval_percent.

Misc. Upgrade Notes
The object qiskit.Aer has been removed following its deprecation in Qiskit 0.46. You can instead use qiskit_aer.Aer, which is a drop-in replacement.

Importing from qiskit.providers.aer will no longer work, following its deprecation in Qiskit 0.46. You should instead import from qiskit_aer, which is a drop-in replacement.

Pulse jobs are no longer supported in fake backends, following the deprecation and removal of the underlying simulation functionality in Aer. For pulse-level simulation, outside the context of circuit objects, consider using a special-purpose library such as Qiskit Dynamics.

Qiskit’s execute() function is removed. This function served as a high-level wrapper around transpiling a circuit with some transpile options and running it on a backend with some run options. To do the same thing, you can explicitly use the transpile() function (with appropriate transpile options) followed by backend.run() (with appropriate run options).

For example, instead of running:


from qiskit import execute
job = execute(circuit, backend)
you can run:


from qiskit import transpile
new_circuit = transpile(circuit, backend)
job = backend.run(new_circuit)
Alternatively, the Sampler primitive is semantically equivalent to the deprecated execute() function. The class BackendSampler is a generic wrapper for backends that do not support primitives:


from qiskit.primitives import BackendSampler
sampler = BackendSampler(backend)
job = sampler.run(circuit)
The deprecated qiskit.IBMQ object has been removed. This alias object was marked as deprecated in the Qiskit 0.40.0 release. This alias object lazily redirected attribute access to qiskit.providers.ibmq.IBMQ. As the qiskit-ibmq-provider package has now been retired and superseded by qiskit-ibm-provider package which maintains its own namespace, maintaining this alias is no longer relevant. If you were relying on the qiskit.IBMQ alias you should migrate your usage to the qiskit-ibm-provider package, see the migration guide for more details.

Removed the deprecated module qiskit.tools.jupyter which previously included Jupyter magics and widgets for interactively visualizing some data from Qiskit. This module was deprecated in Qiskit 0.46.0. Most of this functionality was directly tied to the legacy qiskit-ibmq-provider package and was no longer valid so the module was removed. Similar functionality is available from the qiskit_ibm_provider.jupyter module in the qiskit-ibm-provider package.

Removed the deprecated module qiskit.tools.monitor which previously included tools for tracking JobV1 job instances, primarily from the legacy qiskit-ibm-provider package. This module was marked as deprecated in Qiskit 0.46.0. It is being removed because it was directly tied to the legacy qiskit-ibm-provider package.

Removed the deprecated import path qiskit.test.mock which previously was used to redirect imports for the mock backends to their newer location in the qiskit.providers.fake_provider. This module was marked as deprecated in Qiskit 0.37.0. If you were using this module you should update your imports from qiskit.test.mock to qiskit.providers.fake_provider instead.

The qiskit.test module is no longer a public module. This was never intended to be public, nor used outside of Qiskit’s own test suite. All functionality was specific to Qiskit and no alternative is provided; if you needed similar functionality, you should include it in your own test harnesses.

The deprecated qiskit.tools.visualization module has removed. This module was deprecated in the Qiskit 0.46.0 release. This module was a legacy redirect from the original location of Qiskit’s visualization module and was moved to qiskit.visualization in Qiskit 0.8.0. If you’re still using this path you can just update your imports from qiskit.tools.visualization to qiskit.visualization.

The deprecated qiskit.tools.events module and the corresponding qiskit.tools.progressbar utility it exposed has been removed. It was deprecated in the Qiskit 0.46.0 release. This module’s functionality was not widely used and better covered by dedicated packages such as tqdm.

The qiskit.tools module has been removed. This module was deprecated in Qiskit 0.46.0. All the contents from this module have been removed except for the qiskit.tools.parallel_map function which now can be used from qiskit.utils.parallel_map() instead.

Primitives Deprecations
The methods PrimitiveJob.submit() and PrimitiveJob.wait_for_final_state() have been removed following their deprecation in Qiskit 0.46. These were not intended to be public methods, but were a legacy of an incorrect inheritance structure.
Bug Fixes
Fixed the return of improper measurement schedules when only a subset of qubits was requested. Previously, a measurement schedule for all qubits would be returned.

Fixed an issue in the text circuit drawer when displaying operations that were not circuit.instruction.Instruction class. These operations would cause the drawer to fail. Examples were Clifford and AnnotatedOperation.

Fixed an issue with the SetLayout transpiler pass where an invalid integer list input that contained duplicate entries which would result in an invalid Layout being generated and subsequent transpiler passes would fail with a cryptic error. This is now caught when SetLayout.run() is called an InvalidLayoutError error will be raised indicating there are duplicate entries in the integer list.

QPY (using qpy.dump() and qpy.load()) will now correctly serialize and deserialize quantum circuits with annotated operations (AnnotatedOperation).

Calling copy() or copy_empty_like() on a BlueprintCircuit will now correctly propagate the global_phase to the copy. Previously, the global phase would always be zero after the copy.

QuantumCircuit.compose() will now correctly raise a CircuitError when there are duplicates in the qubits or clbits arguments.

QPY (using qpy.dump() and qpy.load()) will now correctly serialize and deserialize quantum circuits with Clifford operators (Clifford).

Fixed an issue in the mpl circuit drawer where the text would print beyond the end of the box for a SwitchCaseOp if the default case was empty.

The qubit-argument broadcasting of QuantumCircuit.delay() now correctly produces individual Delay instructions for each qubit, as intended. Previously, when given certain iterables (such as sets), it would instead silently produce an invalid circuit that might fail in unusual locations.

Fixed an issue when using transpile() or running a preset pass manager (such as generated by generate_preset_pass_manager()) when targeting a backend that has disjoint connectivity adding extra barriers to the output QuantumCircuit. In some cases several single qubit Barrier directives would be included in the output circuit right before any final measurements in the circuit. This was internal state generated by the internal processing for disjoint connectivity that was incorrectly being added into the output circuit. Fixed #11649

Fixed an error when a user tries to load calibration data of a gate from a Target in a particular situation. This occurs when the backend reports only partial calibration data, for example referencing a waveform pulse in a command definition but not including that waveform pulse in the pulse library. In this situation, the Qiskit pulse object could not be built, resulting in a failure to build the pulse schedule for the calibration. Now when calibration data is incomplete the Target treats it as equivalent to no calibration being reported at all and does not raise an exception.

The Operator.power() method now works with floating-point exponents, matching the documented description.

Fixed an issue with the OptimizeSwapBeforeMeasure pass where it would incorrectly optimize circuits involving swap and measure instructions. For example:


from qiskit import QuantumCircuit
from qiskit.transpiler.passes import OptimizeSwapBeforeMeasure
pass_ = OptimizeSwapBeforeMeasure()
qc = QuantumCircuit(2, 1)
qc.swap(0, 1)
qc.measure(0, 0)
qc.measure(0, 0)
print(qc.draw())
print(pass_(qc).draw())
would previously print:


        ┌─┐┌─┐
q_0: ─X─┤M├┤M├
      │ └╥┘└╥┘
q_1: ─X──╫──╫─
         ║  ║
c: 1/════╩══╩═
         0  0
     ┌─┐
q_0: ┤M├───
     └╥┘┌─┐
q_1: ─╫─┤M├
      ║ └╥┘
c: 1/═╩══╩═
      0  0
and now the second circuit is correctly optimized to:


q_0: ──────
     ┌─┐┌─┐
q_1: ┤M├┤M├
     └╥┘└╥┘
c: 1/═╩══╩═
      0  0
Fixed an issue with the QPY serialization when a QuantumCircuit contained multiple custom instructions instances that have the same name attribute. In QPY format versions before Version 11 the QPY payload did not differentiate between these instances and would only serialize the properties of the first instance in a circuit. This could potentially cause an incorrect deserialization if the other properties of the custom instruction were different but the names were the same. This has been fixed in QPY Version 11 so that each instance of a custom instruction is serialized individually and there will no longer be a potential conflict with overlapping names. Fixes #8941.

Fixed an issue with the qpy.dump() function where, when the use_symengine flag was set to a truthy object that evaluated to True but was not actually the boolean True, the generated QPY payload would be corrupt. For example, if you set use_symengine to HAS_SYMENGINE, this object evaluates to True when cast as a bool, but isn’t actually True.

Fix a bug in the StabilizerState string representation.

A bug where convert_to_target() and BackendV2Converter raised an unexpected error was solved. The bug occurred when the backend to convert included calibrations for a gate that didn’t have a definition in the backend properties. Such gate is now broadcast to all qubits as an ideal error-free instruction, even when calibrations for a finite set of qubits are reported.

Fixed an issue with the circuit_drawer() function and QuantumCircuit.draw() method when loading a matplotlib style via the user configuration file.

InstructionDurations.from_backend() now returns an instance of any subclass of InstructionDurations instead of the base class.

The UnitarySynthesis transpiler pass will now generate an error on initialization when a nonexistent synthesis plugin is specified, rather than waiting until runtime to raise. Fixed #11355.

The OpenQASM 3 exporters qasm3.dump() and dumps() will now correctly output files claiming to be version 3.0 rather than the unqualified 3, since the OpenQASM 3 project has now standardized on versioning.

The parametric form of XXPlusYYGate and XXMinusYYGate returned from get_standard_gate_name_mapping() now correctly includes the 
β
β parameter as well as the initial 
θ
θ rotation.

The TemplateOptimization pass will now return parametric expressions using the native symbolic expression format of ParameterExpression, rather than always using Sympy. For most supported platforms, this means that the expressions will be Symengine objects. Previously, the pass could return mismatched objects, which could lead to later failures in parameter-handling code.