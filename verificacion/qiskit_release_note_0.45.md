Qiskit 0.45 release notes
This page contains the release notes for Qiskit 0.45, the first release after the legacy “elements” structure was completely removed. For all release notes, including those stretching back through the old “meta-package” structure of Qiskit, see Release notes. For a table of meta-package versions, see the Qiskit 0.44 release notes.

0.45.3
Prelude
Qiskit 0.45.3 is a point release with no code changes other than to raise an ImportError if it detects it has been installed in an invalid environment with Qiskit >=1.0.

Please read our migration guide about the new packaging for help on errors, preparing for Qiskit 1.0, and more detailed background information.

Note
Qiskit 1.0 is due to release approximately two weeks after Qiskit 0.45.3, on the 15th of February 2024, and might not yet be available when you read this message. This change is being made proactively.

The packaging structure of Qiskit is changing in Qiskit 1.0, and unfortunately the changed requirements cannot be fully communicated to pip, especially if pip install --upgrade commands are run after the environment has been initially configured. All versions of Qiskit prior to 1.0 (including this one) have an installation conflict with Qiskit 1.0 that pip will not resolve.

If import qiskit raises an ImportError for you, your environment is in an invalid state, and versions of Qiskit 0.45/0.46 and 1.0 are both reachable, which will result in subtly broken code. You will need to create a new virtual environment, and ensure that only one of the two versions are installed. In particular, if you are intending to install Qiskit 1.0, you must have no packages that depend on qiskit-terra installed; these packages are incompatible with Qiskit 1.0 and must be updated. If you are intending to install Qiskit 0.45 or 0.46, you must ensure that you have nothing attempting to install qiskit>=1.0.

If you develop a library based on Qiskit and you still have a dependency on qiskit-terra, you should urgently release a new package that depends only on qiskit. Since version 0.44, the qiskit package contained only the qiskit-terra compiler core (the component that is now simply called “Qiskit”), so if your minimum version is 0.44, you can safely switch a qiskit-terra>=0.44 dependency to qiskit>=0.44 with no change in what will be installed. For more detail and recommendations for testing and preparation, see the section for developers of the migration guide.

0.45.2
Prelude
Qiskit 0.45.2 is a small patch release, fixing several bugs found in the 0.45 release series.

Bug Fixes
Calling copy() or copy_empty_like() on a BlueprintCircuit will now correctly propagate the global_phase to the copy. Previously, the global phase would always be zero after the copy.

QPY (using qpy.dump() and qpy.load()) will now correctly serialize and deserialize quantum circuits with Clifford operators (Clifford).

Fixed an issue in the mpl circuit drawer where the text would print beyond the end of the box for a SwitchCaseOp if the default case was empty.

The qubit-argument broadcasting of QuantumCircuit.delay() now correctly produces individual Delay instructions for each qubit, as intended. Previously, when given certain iterables (such as sets), it would instead silently produce an invalid circuit that might fail in unusual locations.

Fixed a bug that results in an error when a user tries to load .calibration data of a gate in Target in a particular situation. This occurs when the backend reports only partial calibration data, for example referencing a waveform pulse in a command definition but not including that waveform pulse in the pulse library. In this situation, the Qiskit pulse object cannot be built, resulting in a failure to build the pulse schedule for the calibration. Now when calibration data is incomplete the Target treats it as equivalent to no calibration being reported at all and does not raise an exception.

Fixed an issue with the Optimize1qGatesDecomposition transpiler pass where it would potentially resynthesize a single ideal (meaning the error rate is 0.0) gate which was present in the Target. This is now fixed so the pass Optimize1qGatesDecomposition will defer to the circuit’s gate if the error rate (which includes number of gates) are the same. Fixed #10568

Fixed an issue with the OptimizeSwapBeforeMeasure pass where it would incorrectly optimize circuits involving swap and measure instructions. This commit fixes the bug by changing DAGCircuit.successors() to DAGCircuit.descendants(). Also, added a couple of extra tests to ensure that the bug is fixed. For example:


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
and now the second ciruit is correctly optimized to:


q_0: ──────
     ┌─┐┌─┐
q_1: ┤M├┤M├
     └╥┘└╥┘
c: 1/═╩══╩═
      0  0
Fix a bug in the StabilizerState string representation.

0.45.1
Prelude
Qiskit Terra 0.45.1 is a small patch release, fixing several bugs found in the 0.45 release series. It is also the first release to have official support for Python 3.12. The 0.45.1 release supports Python 3.8, 3.9, 3.10, 3.11, and 3.12.

New Features
Added support for using Qiskit with Python 3.12. As of this release Qiskit supports running with Python versions 3.8, 3.9, 3.10, 3.11, and 3.12.
Bug Fixes
QuantumCircuit.barrier() will now generate correct output when given a set as one of its inputs. Previously, it would append an invalid operation onto the circuit, though in practice this usually would not cause observable problems. Fixed #11208

The property Instruction.condition_bits will now correctly handle runtime classical expressions (qiskit.circuit.classical).

Fixed the hash() of Qiskit Pulse Channel objects (such as DriveChannel) in cases where the channel was transferred from one Python process to another that used a different hash seed.

Conditioned custom gates imported from OpenQASM 2 will now correctly retain their conditions when pickled and deep-copied. Previously, any conditional custom gate (defined by a gate statement in an OpenQASM 2 file) would lose its condition when copied or pickled.

Fixed QPY deserialization of the StatePreparation and Initialize circuit instructions with string and integer parameters (as opposed to an explicit statevector, which was already working). Fixed #11158.

Fixed a bug in SabreLayout where it would fail to add the register information to the Layout object used for TranspileLayout.initial_layout. This affected circuit visualization with QuantumCircuit.draw() and circuit_drawer() after transpilation which would show a virtual qubit label of the form Qubit[QuantumRegister(6, 'q', 0)] rather than the expected virtual qubit label using the register name (e.g. q0). Fixed #11038

Fixed an issue with qpy.dump() which would cause the function to potentially ignore the value of use_symengine when serializing a ScheduleBlock object. This would result in an invalid QPY payload being generated as it would report it was using symengine for symbolic expressions but actually contain sympy serialized data.

Fixed a bug which caused UnitaryOverlap to error upon initialization if given an input circuit containing a barrier.

0.45.0
Prelude
Qiskit 0.45.0 is the last feature release before 1.0. It prepares the ground for the API changes we are planning for our first major version release, including many removals of previously deprecated functionality as well as a series of new deprecations.

Note
If your project depends on Qiskit, it may rely on functionality that will no longer be supported in Qiskit 1.0. For this reason, we recommend that you proactively cap your supported version to <1.0.

Some feature highlights of Qiskit 0.45.0 are:

Starting in this release, all unparametrized gates in the Qiskit standard circuit library are now singletons. By default, these gates share a single instance in memory, so once a gate of a specific type, let’s say XGate, is instantiated, any subsequent instances of XGate will be a reference to the first one. This results in a reduced memory usage and construction overhead when using multiple gates of the same type in a circuit. To realize this feature, new base classes have been introduced: SingletonInstruction and SingletonGate. See feature notes for more details.
We have added a new generic pass manager interface that can be found in the new qiskit.passmanager module. This is a generalization of the pass manager that was used to build the Qiskit transpiler, and it introduces a generic framework to enable users to create new pass managers that use different intermediate representations (IRs). The module includes a generic pass manager base class, flow controllers, and the necessary infrastructure to manage the execution of pass manager tasks. The new interface was used to rebuild the existing pass manager in the qiskit.transpiler module, cleaning up technical debt in the code, and improving usability and performance. See feature and upgrade notes for more details.
0.45.0 allows users to better interact with the layout permutations performed by the transpiler. The data contained in the TranspileLayout class is now more accessible through a series of new methods and attributes. And a new SparsePauliOp.apply_layout() method allows to apply a specific layout permutation to a SparsePauliOp observable that was built for an input circuit to the transpiler. See feature notes for more details.
Finally, we have introduced annotated operations with the new AnnotatedOperation class, which allows to formulate complex circuit instructions as a base instruction with a set of modifiers. For example, instead of a specific operation type that implements the controlled inverse of a RXGate, we can now use an annotated RXGate with inverse and control attributes. See feature notes for more details.
Circuits Features
Added a new class AnnotatedOperation that is a subclass of Operation and represents some “base operation” modified by a list of “modifiers”. The base operation is of type Operation and the currently supported modifiers are of types InverseModifier, ControlModifier and PowerModifier. The modifiers are applied in the order they appear in the list.

As an example:


gate = AnnotatedOperation(
  base_op=SGate(),
  modifiers=[
      InverseModifier(),
      ControlModifier(1),
      InverseModifier(),
      PowerModifier(2),
  ],
)
is logically equivalent to gate = SGate().inverse().control(1).inverse().power(2), or to:


gate = AnnotatedOperation(
  AnnotatedOperation(SGate(), [InverseModifier(), ControlModifier(1)]),
  [InverseModifier(), PowerModifier(2)],
)
However, this equivalence is only logical, the internal representations are very different.

For convenience, a single modifier can be also passed directly, thus AnnotatedGate(SGate(), [ControlModifier(1)]) is equivalent to AnnotatedGate(SGate(), ControlModifier(1)).

A distinguishing feature of an annotated operation is that circuit definition is not constructed when the operation is declared, and instead happens only during transpilation, specifically during the HighLevelSynthesis transpiler pass.

An annotated operation can be also viewed as a “higher-level” or a “more abstract” object that can be added onto a quantum circuit. This enables writing transpiler optimization passes that make use of this higher-level representation, for instance removing a gate that is immediately followed by its inverse (note that this reduction might not be possible if both the gate and its inverse are first synthesized into simpler gates).

In a sense, an annotated operation can be viewed as an extension of ControlledGate, which also allows adding control to the base operation. In the future we are planning to replace ControlledGate by AnnotatedOperation. Similar to controlled gates, the transpiler synthesizes annotated operations before layout/routing takes place.

As of now, the annotated operations can appear only in the top-level of a quantum circuit, that is they cannot appear inside of the recursively-defined definition circuit. We are planning to remove this limitation later.

Added a new option max_num_qubits to qiskit.circuit.CommutationChecker.commute() that specifies the maximum number of qubits to consider for the more expensive matrix multiplication-based commutativity check. This avoids trying to internally allocate arrays of size 
2
N
×
2
N
2 
N
 ×2 
N
 . Simpler versions of commutativity check (for instance, two quantum operations commute when they are over disjoint sets of qubits) continue to work without this limit.

Added a new argument, check_input, to the constructor for the UnitaryGate class. This flag is used to disable the default initialization checks that input object represents a unitary matrix. This can be used to speed up the creation of UnitaryGate objects if you know the input is already a unitary matrix. This new option should only be used in these cases because if it’s set to False and the input is not unitary this will result in an invalid UnitaryGate object.

A new method Parameter.assign() has been added. This method primarily serves as a fast path to improve the performance of QuantumCircuit.assign_parameters() for the common case of circuits that predominantly contain “expressions” that are actually just single parameters to be assigned later.

The performance of QuantumCircuit.assign_parameters() when assigning a single parameter of a circuit that involves many parameters has been improved.

Introduced two new classes, SingletonInstruction and SingletonGate, which are subclasses of Instruction and Gate respectively, that use a single instance for all objects of that type. The intent behind this class is to minimize the memory and construction overhead of using multiple gates in a circuit with the tradeoff of having global shared state. For this reason this class is only applicable to gates that do not have any unique and/or mutable state stored in an instance. For example, the best example of this is XGate doesn’t contain any state and could leverage SingletonGate (and does starting in this release), while RXGate stores an angle parameter in an instance and thus can not use SingletonGate because a single shared global instance can not represent the parameter values.

The other potential issue to be aware of when using singleton classes is that the Instruction data model supports some mutable state. Specifically, the label, duration, unit, and condition attributes are all accessible and mutable in the Instruction and its direct subclasses. However, this is incompatible with having a shared object via SingletonInstruction. For instances of SingletonInstruction, setting these attributes directly is not allowed and it will raise an exception. If they are needed for a particular instance, you must ensure you have a mutable instance using Instruction.to_mutable() (or use Instruction.c_if() for condition). label, duration and unit can also be given as keyword arguments during class construction.

The following standard library gates are now instances of SingletonGate:

DCXGate
ECRGate
HGate
IGate
iSwapGate
SGate
SdgGate
SwapGate
SXGate
SXdgGate
TGate
TdgGate
XGate
RCCXGate
RC3XGate
YGate
ZGate
This means that if these classes are instantiated as (e.g.) XGate() using all the constructor defaults, they will all share a single global instance. This results in a large reduction in the memory overhead for > 1 object of these types and significantly faster object construction time.

Introduced a new class SingletonControlledGate which is a subclass of ControlledGate that uses a single instance for all objects of that type. The intent behind this class is to minimize the memory and construction overhead of using multiple gates in a circuit with the tradeoff of having a global shared state. For this reason, this class is only applicable to gates that do not have any unique and/or mutable state stored in an instance. For example, a CXGate doesn’t contain any state and thus can leverage SingletonControlledGate (and does starting in this release). In contrast, CRXGate stores an angle parameter as part of its instance data and thus can not use SingletonControlledGate.

The other potential issue to be aware of when using SingletonControlledGate is that the original data model of ControlledGate supports mutation. Specifically, the label, duration, unit, condition, and ctrl_state attributes are all accessible and mutable in the ControlledGate, but mutation of these attributes on SingletonControlledGate subclasses is not allowed, and will raise an exception. These attributes can be customized but only at creation time (i.e. via the constructor). In that case, the newly constructed gate will be a separate instance with the custom state instead of the globally shared instance. You can also use the SingletonControlledGate.to_mutable() method to get a mutable copy of a gate object and then mutate the attributes like you would on any other Instruction object.

The following standard library gates are now instances of SingletonControlledGate:

CHGate
CSGate
CSdgGate
CSwapGate
CSXGate
CXGate
CCXGate
C3SXGate
C3XGate
C4XGate
CYGate
CZGate
This means that unless a label, condition, duration, unit, or ctrl_state are set on the instance at creation time they will all share a single global instance whenever a new gate object is created. This results in a large reduction in the memory overhead for > 1 object of these types.

Added a new method Instruction.to_mutable() and attribute Instruction.mutable which is used to get a mutable copy and check whether an Instruction object is mutable. With the introduction of SingletonGate these methods can be used to have a unified interface to deal with the mutablitiy of instruction objects.

Added an attribute Instruction.base_class, which gets the “base” type of an instruction. Many instructions will satisfy type(obj) == obj.base_class, however the singleton instances of SingletonInstruction and SingletonGate are subclasses of their base type. You can use the new base_class attribute to find the base class of these. See the attribute documentation for considerations on when other subclasses may modify their base_class, and what this means for execution.

Added the UnitaryOverlap circuit to the Qiskit circuit library. It can be used to compute the fidelity of states generated by unitaries by looking at the probability of the output distribution in the all-zeros state or, equivalently, by computing the expectation value of the projector onto the all-zeros state. This is useful in applications such as machine learning, and computing excited states in quantum chemistry, to name a few.

Pulse Features
Enabled circuit-to-pulse scheduling using BackendV2.


# import a fake backend which is a sub-class of BackendV2
from qiskit.providers.fake_provider import FakePerth
from qiskit.compiler.scheduler import schedule
from qiskit.circuit import QuantumCircuit
 
qc = QuantumCircuit(1, 1)
qc.x(0)
qc.measure(0,0)
sched = schedule(circuits=qc, backend=FakePerth())
Since BackendV2 was not supported by the schedule() function, this caused the schedule() method to error out when the backend argument was supplied with an instance of BackendV2. Refer to #10837 for more information.

OpenQASM Features
The OpenQASM 2 module qiskit.qasm2 has gained the export functions dump() and dumps(). These are used in a very similar manner to the previous QuantumCircuit.qasm():


from qiskit import qasm2, QuantumCircuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
print(qasm2.dumps(qc))
The new functions stem from the same code as QuantumCircuit.qasm(), which will slowly be phased out and replaced with the new paths, to provide a more coherent interface when compared to the OpenQASM 3 (qiskit.qasm3) and QPY (qiskit.qpy) modules. This is particularly important since the method name qasm() gave no indication of the OpenQASM version, and since it was originally added, Qiskit has gained several serialisation modules that could easily become confused.

QPY Features
QPY now supports the use of symengine-native serialization and deserialization for objects of type ParameterExpression as well as symbolic expressions in Pulse schedule blocks. This is a faster serialization alternative, but not supported in all platforms. Please check that your target platform is supported by the symengine library before setting this option, as it will be required by qpy to deserialize the payload.

The feature can be enabled through the use_symengine parameter in qpy.dump():


from qiskit.circuit import QuantumCircuit, Parameter
from qiskit import qpy
 
theta = Parameter("theta")
phi = Parameter("phi")
sum_param = theta + phi
 
qc = QuantumCircuit(1)
qc.rz(sum_param, 0)
qc.measure_all()
 
with open('bell.qpy', 'wb') as fd:
    qpy.dump(qc, fd, use_symengine=True)
 
with open('bell.qpy', 'rb') as fd:
    new_qc = qpy.load(fd)[0]
Quantum Information Features
Added Clifford.from_linear_function() and Clifford.from_permutation() methods that create a Clifford object from LinearFunction and from PermutationGate respectively. As a consequence, a Clifford can now be constructed directly from a LinearFunction, a PermutationGate, or a quantum circuit containing such gates.

The Operator class now has a draw() method allowing it to be displayed as a text matrix, IPython LaTeX object or LaTeX source. The default draw type still is the ASCII __repr__ of the operator.

Added a new method, apply_layout(), to the SparsePauliOp class. This method is used to apply a TranspileLayout layout from the transpiler to a SparsePauliOp observable that was built for an input circuit to the transpiler. This enables working with BaseEstimator implementations and local transpilation more easily. For example:


from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import BackendEstimator
from qiskit.compiler import transpile
from qiskit.providers.fake_provider import FakeNairobiV2
 
psi = RealAmplitudes(num_qubits=2, reps=2)
H1 = SparsePauliOp.from_list([("II", 1), ("IZ", 2), ("XI", 3)])
backend = FakeNairobiV2()
estimator = BackendEstimator(backend=backend, skip_transpilation=True)
 
thetas = [0, 1, 1, 2, 3, 5]
transpiled_psi = transpile(psi, backend, optimization_level=3)
permuted_op = H1.apply_layout(transpiled_psi.layout)
res = estimator.run(transpiled_psi, permuted_op, thetas)
where an input circuit is transpiled locally before it’s passed to run. Transpilation expands the original circuit from 2 to 7 qubits (the size of backend) and permutes its layout, which is then applied to H1 using apply_layout() to reflect the transformations performed by transpile().

Transpiler Features
The HighLevelSynthesis class is extended to synthesize circuits with objects of type AnnotatedOperation.

A new qiskit.passmanager module has been added to the Qiskit library. This module implements a generic pass manager and flow controllers, and provides infrastructure to manage execution of pass manager tasks. The module provides base classes for passes (GenericPass) and flow controllers (BaseController), as well as a new interface class, passmanager.Task, to manage the execution of the pass manager (see the Task.execute() method). These new classes follow the composite pattern, as flow controllers are collections of passes, and a controller can be recursively nested into the task pipeline. It must also be noted the base classes are not not aware of the input and output object types, and they must be subclassed for a particular program type to optimize. This unified design reduces the complexity of the conventional pass manager, and no longer requires the use of classes such as the RunningPassManager to handle the execution logic dispatch and task structure renormalization. The qiskit.transpiler module has been reorganized to rebuild the existing pass managers based off of the generic pass manager. See upgrade notes for more details.

Added a new analysis SabrePreLayout pass that creates a starting layout for SabreLayout, writing the layout into the property set value sabre_starting_layouts.

The pass works by augmenting the coupling map with more and more “extra” edges until VF2Layout succeeds to find a perfect graph isomorphism. More precisely, the augmented coupling map contains edges between nodes that are within a given distance d in the original coupling map, and the value of d is increased until an isomorphism is found. The pass also optionally minimizes the number of extra edges involved in the layout until a local minimum is found. This involves removing extra edges and calling VF2Layout to check if an isomorphism still exists.

Here is an example of calling the SabrePreLayout before SabreLayout:


import math
from qiskit.transpiler import CouplingMap, PassManager
from qiskit.circuit.library import EfficientSU2
from qiskit.transpiler.passes import SabrePreLayout, SabreLayout
 
qc = EfficientSU2(16, entanglement='circular', reps=6, flatten=True)
qc.assign_parameters([math.pi / 2] * len(qc.parameters), inplace=True)
qc.measure_all()
 
coupling_map = CouplingMap.from_heavy_hex(7)
 
pm = PassManager(
    [
        SabrePreLayout(coupling_map=coupling_map),
        SabreLayout(coupling_map),
    ]
)
 
pm.run(qc)
Added the arguments coupling_map, target and use_qubit_indices to HighLevelSynthesis transpiler pass. The argument target specifies the target backend, allowing the synthesis plugins called within the pass to access all target-specific information, such as the coupling map and the supported gate set. The argument coupling_map only specifies the coupling map, and is only used when target is not specified. The argument use_qubit_indices indicates whether the high-level-synthesis pass is running before or after the layout is set, that is, whether the qubit indices of higher-level-objects correspond to qubit indices on the target backend.

Added the arguments coupling_map, target and qubits to HighLevelSynthesisPlugin. The positional argument target specifies the target backend, allowing the plugin to access all target-specific information, such as the coupling map, the supported gate set, and so on. The positional argument coupling_map only specifies the coupling map, and is only used when target is not specified. The positional argument qubits specifies the list of qubits over which the higher-level-object is defined, in case the synthesis is done on the physical circuit. The value of None indicates that the layout has not yet been chosen.

This enables a cleaner separation of synthesis plugins options into general interface options for plugins (that is, coupling_map, target, and qubits) and into plugin-specific options (a free form configuration dictionary specified via options). It is worthwhile to note that this change is backward-compatible, if the options coupling_map, etc. are not explicitly added to the plugin’s run() method, they will appear as part of options.

The DAGCircuit methods apply_operation_back() and apply_operation_front() have gained a check keyword argument that can be set False to skip validation that the inputs uphold the DAGCircuit data-structure invariants. This is useful as a performance optimisation when the DAG is being built from known-good data, such as during transpiler passes.

The method CouplingMap.reduce() now accepts an additional argument check_if_connected, defaulted to True. This corresponds to the previous behavior, checking whether the reduced coupling map remains connected and raising a CouplingError if not so. When set to False, the check is skipped, allowing disconnected reduced coupling maps.

The constructor for HighLevelSynthesis transpiler pass now accepts additional arguments equivalence_library, basis_gates, and min_qubits. The pass can now unroll custom definitions similarly to UnrollCustomDefinitions, and as such completely subsumes the functionality of the latter pass. In particular, HighLevelSynthesis is now recursive, fixing an oversight in the initial implementation. Thus, when either target or basis_gates are specified, HighLevelSynthesis recursively synthesizes all high-level objects, annotated operations and custom gates in the circuit, leaving only gates that are supported by the target or belong to the equivalence library. This allows to use HighLevelSynthesis as a drop-in replacement for UnrollCustomDefinitions. On the other hand, when neither target nor basis_gates are specified, the pass synthesizes only the “top-level” high-level objects and annotated operations, i.e. does not recursively descent into the custom gates definition field. This is backward-compatible both with UnrollCustomDefinitions (which would not do anything) and with the older behavior of the high level synthesis pass, which allows to use it as an intermediate transform, only synthesizing high-level objects as specified by HLSConfig.

Significantly improved the performance of the MergeAdjacentBarriers transpiler pass, which used to rebuild the complete DAG to merge the barriers.

Added a new keyword argument, min_qubits, to the constructor of the BasisTranslator transpiler pass. When set to a non-zero value this is used to set a minimum number of qubits to filter operations to translate in the circuit. For example, if min_qubits=3 is set the BasisTranslator instance will only translate gates in the circuit that operate on 3 or more qubits.

Added a new keyword argument, min_qubits, to the constructor of the UnrollCustomDefinitions transpiler pass. When set to a non-zero value this is used to set a minimum number of qubits to filter operations to translate in the circuit. For example, if min_qubits=3 is set the UnrollCustomDefinitions instance will only translate gates in the circuit that operate on 3 or more qubits.

Added support to the SabreLayout pass to add trials with specified starting layouts. The SabreLayout transpiler pass typically runs multiple layout trials that all start with fully random layouts which then use a routing pass to permute that layout instead of inserting swaps to find a layout which will result in fewer swap gates. This new feature enables running an AnalysisPass prior to SabreLayout which sets the "sabre_starting_layout" field in the property set to provide the SabreLayout with additional starting layouts to use in its internal trials. For example, if you wanted to run DenseLayout as the starting point for one trial in SabreLayout you would do something like:


from qiskit.providers.fake_provider import FakeSherbrooke
from qiskit.transpiler import AnalysisPass, PassManager
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.transpiler.passes import DenseLayout
 
class SabreDenseLayoutTrial(AnalysisPass):
 
  def __init__(self, target):
      self.dense_pass = DenseLayout(target=target)
      super().__init__()
 
  def run(self, dag):
      self.dense_pass.run(dag)
      self.property_set["sabre_starting_layouts"] = [self.dense_pass.property_set["layout"]]
 
backend = FakeSherbrooke()
opt_level_1 = generate_preset_pass_manager(1, backend)
pre_layout = PassManager([SabreDenseLayoutTrial(backend.target)])
opt_level_1.pre_layout = pre_layout
Then when the opt_level_1 StagedPassManager is run with a circuit the output of the DenseLayout pass will be used for one of the SabreLayout trials in addition to the 5 fully random trials that run by default in optimization level 1.

Two new transpiler passes are added to generate single-pulse RX gate calibrations on the fly. These single-pulse RX calibrations will reduce the gate time in half, as described in P.Gokhale et al, Optimized Quantum Compilation for Near-Term Algorithms with OpenPulse (2020), arXiv:2004.11205.

To reduce the amount of RX calibration data that needs to be generated, NormalizeRXAngle performs three optimizations: wrapping the RXGate rotation angles to [0, pi], replacing RX(pi/2) and RX(pi) with SXGate and XGate, and quantizing the rotation angles. This pass is required to be run before RXCalibrationBuilder, which generates RX calibrations on the fly.

The optimizations performed by NormalizeRXAngle reduce the amount of calibration data and enable us to take advantage of the more accurate, hardware-calibrated pulses. The calibrations generated by RXCalibrationBuilder are bootstrapped from the SXGate calibration, which should be already present in the target. The amplitude is linearly scaled to achieve the desired arbitrary rotation angle.

Such single-pulse calibrations reduces the RXGate time in half, compared to the conventional sequence that consists of two SXGate pulses. There could be an improvement in fidelity due to this reduction in gate time.

Added new methods to TranspileLayout, initial_index_layout() and routing_permutation(), which are used to generate a list view of the TranspileLayout.initial_layout and TranspileLayout.final_layout attributes respectively. For example, if the final_layout attribute was:


Layout({
  qr[0]: 2,
  qr[1]: 3,
  qr[2]: 0,
  qr[3]: 1,
})
then routing_permutation() will return:


[2, 3, 0, 1]
Added a new method to TranspileLayout, initial_virtual_layout(), which is equivalent to the TranspileLayout.initial_layout attribute but gives the option to filter ancilla qubits that were added to the circuit. By default the TranspileLayout.initial_layout will typically include any ancillas added by the transpiler.

Added a new methods, final_index_layout() and final_virtual_layout() to the TranspileLayout class. These methods are used to return a final layout (the mapping of input circuit qubits to the final position in the output). This is distinct from the final_layout attribute which is the permutation caused by routing as a Layout object. The final_index_layout() method returns a list to show the output position for each qubit in the input circuit to the transpiler. For example, with an original circuit:


qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)
and the output from the transpiler was:


tqc = QuantumCircuit(3)
tqc.h(2)
tqc.cx(2, 1)
tqc.swap(0, 1)
tqc.cx(2, 1)
then the output from final_index_layout() would return a list of:


[2, 0, 1]
The final_virtual_layout() returns this as a Layout object, so the return from the above example would be:


Layout({
  qc.qubits[0]: 2,
  qc.qubits[1]: 0,
  qc.qubits[2]: 1,
})
Visualization Features
Added the ability to display conditions as expressions from Expr in the QuantumCircuit.draw() method and the circuit_drawer() function when visualizing circuits that have ControlFlowOp instructions.

Added the "iqp" and "iqp-dark" color styles for the matplotlib circuit drawer, which are based on the IBM Quantum Platform color scheme.

In TextDrawer, operations built from ControlFlowOp, including if, else, while, for, and switch/case, whether directly instantiated or built using methods in QuantumCircuit, will now fully display the circuits defined in the ControlFlowOps with brackets to delineate the circuits.

When defining a custom stylesheet for the pulse timeline drawer qiskit.visualization.timeline_drawer(), “generator” functions that have the object attribute accepts_program set to True will receive an extra keyword argument program containing the full scheduled QuantumCircuit being drawn.

The visualizations from the plot_gate_map(), plot_coupling_map(). plot_error_map(), and plot_circuit_layout() functions have been significantly improved for rendering layouts of backends with large numbers of qubits. This was accomplished by leveraging graphviz through rustworkx’s graphviz_draw() function to perform a more sophisticated algorithmic graph layout that scales for large numbers of qubits.

_images/release_notes-1.png
Misc. Features
Added support for expressing the sign of a ParameterExpression. Instead of assigning a concrete value and using numpy.sign or other library functions, the user can use the instance of the ParameterExpression class to calculate the sign and can work with the sign before the expression is fully assigned.

It can be used as follows:


from qiskit.circuit import Parameter
 
b = Parameter("phi")
sign_value = b.sign()
print("sign of an unassigned Parameter is: ", sign_value)
print("Sign of a Parameter assigned to -3 is: ", sign_value.assign(b,-3))
Refer to #10360 for more details.

Parameter now has an advanced-usage keyword argument uuid in its constructor, which can be used to make the Parameter compare equal to another of the same name. This should not typically be used by users, and is most useful for custom serialisation and deserialisation.

Circuits Upgrade Notes
The ControlledGate.definition of the output from the Gate.control() method may be different as compared to previous releases. The internal generation of the Gate.control() method is no longer using the now deprecated Unroller transpiler pass to generate its definition and this can potentially cause a different definition to be generated. The output ControlledGate object’s definition will be unitary equivalent to what was generated before. But if you require the exact definition from calling Gate.control() you can use an earlier release and save the circuit with qpy.dump() and then load it with a newer release.

The property num_ancilla_qubits from the class PolynomialPauliRotations has been removed, as deprecated in Qiskit 0.23.0. Instead, use the property PolynomialPauliRotations.num_ancillas.

The following standard library gates:

DCXGate
ECRGate
HGate
IGate
iSwapGate
SGate
SdgGate
SwapGate
SXGate
SXdgGate
TGate
TdgGate
XGate
RCCXGate
RC3XGate
YGate
ZGate
CHGate
CSGate
CSdgGate
CSwapGate
CSXGate
CXGate
CCXGate
C3SXGate
C3XGate
C4XGate
CYGate
CZGate
are no longer able to set label, condition, duration, or unit (and ctrl_state for ControlledGate subclasses) after instantiating an object anymore. You can still set condition through the use c_if(). You can use to_mutable() to get a mutable copy of the instruction and then use the setter on that copy instead of the original object. label, duration and unit can be given as keyword arguments to these gates at construction time, and a mutable instance will be returned automatically. This change was necessary as part of converting these classes to be SingletonGate and SingletonControlledGate types which greatly reduces the memory footprint of repeated instances of these gates.

For anything that interacts with Gate, Operation, or Instruction objects or works with these as part of a QuantumCircuit or DAGCircuit classes, it is important to note that the use of shared references for instances is much more common now. Previously, it was possible to reuse and share an instance of a circuit operation, but it wasn’t very commonly used and a copy would generate a unique instance. This has changed starting in this release because of SingletonInstruction and SingletonGate being made available (and a large number of standard library gates now built off of them). If your usage of these objects is assuming unique instances for every circuit operation, this becomes a potential issue, as now a shared state will be reused between operations of the same type (that will persist through copy and deep copies). You can rely on the Instruction.mutable attribute to check the mutability of an object or use Instruction.to_mutable() to get a mutable copy of any instruction.

More Instruction instances (those that return singletons) no longer strictly satisfy (for example):


type(XGate()) is XGate
The returned object will, however, still be a standard subclass so isinstance() (the correct way to do type checking) will continue to work correctly. Several instructions already had this property (e.g. MCXGate), but it is now more common as many more standard gates will do this.

If you require the “base” type of a gate for some reason, omitting the synthetic singleton subclasses, which cannot be instantiated, see Instruction.base_class.

The definition of UnitaryGate for single qubit unitaries is now in terms of UGate instead of the legacy U3Gate class.

Providers Upgrade Notes
The QasmSimulatorPy python-based simulator included in qiskit.providers.basicaer now includes 'h' (HGate), 'p' (PhaseGate), and 'u' (UGate) in its basis gate set.

The argument channel in the method PulseBackendConfiguration.control() is removed. It was deprecated in Qiskit 0.33 (with Terra 0.19), released on Dec 2021. Instead use the qubits argument.

Replaced the argument qobj[Qobj] in QasmSimulatorPy.run() with run_input[QuantumCircuit or list]

Here is an example to migrate your code:


# Importing necessary Qiskit libraries
from qiskit import transpile, QuantumCircuit
from qiskit.aer import QasmSimulator
 
# Defining the Quantum Circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()
 
# Transpile the circuit to optimize for the target simulator
simulator = QasmSimulator()
transpiled_circuit = transpile(qc, simulator)
# Run the simulation
job = simulator.run(transpiled_circuit, shots=1024)
# Get the simulation result
result = job.result()
All these were deprecated since 0.22 (released on October 13, 2022) and now they are removed.

Pulse Upgrade Notes
The functions qiskit.scheduler.utils.format_meas_map(), qiskit.scheduler.utils.measure(), and qiskit.scheduler.utils.measure_all() had been moved to qiskit.pulse.utils.format_meas_map(), qiskit.pulse.macros.measure(), and qiskit.pulse.macros.measure_all() respectively. The previous location was deprecated in Qiskit 0.20.0 (Terra 0.15.0, released on 2020-08-10) and it is no longer supported.

The methods to_dict in the classes pulse.transforms.AlignmentKind, pulse.transforms.AlignEquispaced, and pulse.transforms.AlignFunc are removed. They were deprecatedin Qiskit 0.37 (with Terra 0.21), released on June 2022.

QPY Upgrade Notes
The use of the keyword circuits for the first positional argument in the function qiskit.qpy.dump() is removed as its usage was deprecated in Qiskit 0.37 (with Terra 0.21), released on June 2022. Instead, use the keyword programs can be used instead (or just pass the argument in positionally), which behaves identically.
Quantum Information Upgrade Notes
The method qiskit.quantum_info.pauli_basis() does not accept the pauli_list argument any more. It was deprecated in Qiskit 0.39 (with Terra 0.22), released on Oct 2022.

The function random_stabilizer_table in the qiskit.quantum_info.random module is removed. It was deprecated in Qiskit 0.39 (with Terra 0.22), released on Oct 2022. Instead, use qiskit.quantum_info.random.random_pauli_list().

The classes qiskit.quantum_info.PauliTable and qiskit.quantum_info.StabilizerTable are removed. The function random_pauli_table() is also removed. They were deprecated in Qiskit 0.43 (with Terra 0.24), released in May 2023. Instead, you should use PauliList and random_pauli_list().

The arguments z and x to the initializer of to Pauli were removed, as deprecated in Qiskit Terra 0.17 (released on April, 2021). A pair of x and z should be passed positionally as a single tuple instead (Pauli((z, x))).

The argument label to the initializer of Pauli was removed, as deprecated in Qiskit Terra 0.17 (released on April, 2021). Pass the label positionally instead, such as Pauli("XYZ").

Importing from qiskit.quantum_info.operators.pauli is not allowed anymore, as it was deprecated in Qiskit Terra 0.21 (released on June, 2022). Import directly from qiskit.quantum_info instead.

Synthesis Upgrade Notes
The parameter order in synthesis.SuzukiTrotter constructor raises an exception instead of deprecation warning when set in an odd number. Suzuki product formulae are symmetric and therefore only defined for even orders.
Transpiler Upgrade Notes
As a consequence of the pass manager refactoring efforts, existing flow controllers: FlowControllerLinear, ConditionalController, and DoWhileController are now subclasses of the BaseController. Note that these controllers have dropped the implementation of the __iter__() method. They are now only iterable in the context of a flow-controller execution, which threads the compilation state through after each inner task is executed.

The functionalitly of the RunningPassManager class has been superseded by the new pass manager framework (BasePassManager and BaseController). The running pass manager is now a stateless flow controller (essentially, an alias of FlowControllerLinear), as the pass manager is responsible for the construction of task pipeline, while the controller is responsible for the execution of associated tasks. Subclassing the RunningPassManager is no longer recommended, and this class will be completely replaced with the flow controller in future releases.

A new class, WorkflowStatus, has been introduced to track the status of the pass manager workflow. This portable object is created when the pass manager is run, and handed over to the underlying tasks. Such status was previously managed by the RunningPassManager with instance variables.

The transpiler-specific transpiler.PassManager (used in transpile()) is now a subclass of passmanager.BasePassManager. However, this class hierarchy change doesn’t introduce any breaking change to the public-facing API.

Exceptions raised during pass-manager execution now inherit from the newly introduced PassManagerError. A generic failure of the pass-manager machinery will raise PassManagerError for general pass managers, but the transpiler-specific transpile.PassManager will currently wrap this in its specific TranspilerError for backwards compatibility. This wrapping will be removed in the future.

The use of FencedObject in the pass manager framework has been removed. This wrapper class cannot protect mutable object attributes from modification, and this should not be an issue for properly implemented code. Analysis passes should not modify an input IR, controllers should not update the property set, and so forth. It’s the pass manager developer’s responsibility to ensure that the pass is not modifying object attributes,

The plugin name default is reserved for the plugin stages init, layout, optimization, and scheduling. These stages previously did not reserve this plugin name, but the default name is now used to represent Qiskit’s built-in default method for these stages. If you were using these names for plugins on these stages these will conflict with Qiskit’s usage and you should rename your plugin.

Disabled the use of the RemoveResetInZeroState class in the preset passmanagers. Previously, when transpile() or generate_preset_pass_manager() was run with optimization_level at level 1, 2, or 3, it would run RemoveResetInZeroState. However, this pass prohibited the notion of arbitrary initial states unless explicitly set to zeros with resets. If you need to run the pass as part of your compilation pipeline, you can run something like:


pm = generate_preset_pass_manager(1, backend)
pm.init.append(RemoveResetInZeroState())
pm.run(circuit)
to retain this functionality for your circuit compilation.

The deprecated transpiler routing pass, BIPMapping has been removed. It was marked as deprecated in the Qiskit 0.43.0 release. It has been replaced by an external plugin package: qiskit-bip-mapper. Details for this new package can be found at the package’s github repository:

https://github.com/qiskit-community/qiskit-bip-mapper

The pass was made into a separate plugin package for two reasons: first, the dependency on CPLEX makes it harder to use, and secondly, the plugin package integrates more cleanly with transpile(). The optional extra bip-mapper to install cplex and docplex to support this pass has been removed as nothing in Qiskit optionally requires it anymore.

The argument qubits in the method InstructionDurations.get(), does not accept Qubit (or a list of them) any more. This functionality was deprecated in Qiskit 0.33 (with Terra 0.19), released on Dec 2021. Instead, use an integer for the qubit indices.

Removed the argument qubit_channel_mapping in RZXCalibrationBuilder, which was deprecated in Qiskit 0.39 (released on Oct 2022, with qiskit-terra 0.22)

In transpiler.CouplingMap method subgraph is removed as deprecated in 0.20. reduce() can be used in place of method subgraph.

Visualization Upgrade Notes
Removed support for using the keyword rho for the first positional argument in plot_state_hinton(), plot_bloch_multivector(), plot_state_city(), plot_state_paulivec(), and plot_state_qsphere(). The use of rho has been replaced by state, which can be used instead. Removed qiskit.scheduler.utils as all contained functions were moved to qiskit.pulse.macros and qiskit.pulse.utils. All these were deprecated since 0.15 (released on August 06, 2020) and now they are removed.

The class constructor arguments qregs, cregs, layout and global_phase for visualization.QCircuitImage are removed, as they were deprecated in 0.20.

The visualization functions: plot_gate_map(), plot_coupling_map(). plot_error_map(), and plot_circuit_layout() now depend on graphviz being installed to function. This change was necessary to enable visualizing backends with larger numbers of qubits. This additional external requirement is in addition to the existing optional dependencies these functions previously required. You find details on how to install graphviz here: https://graphviz.org/download/

Misc. Upgrade Notes
The QuasiDistribution values might include floating-point errors. QuasiDistribution.__repr__ rounds using numpy.round() and the parameter ndigits can be manipulated with the class attribute __ndigits__. The default is 15.

The class qiskit.qobj.Qobj is removed. It was deprecated in Qiskit 0.33 (with Terra 0.19), released on Dec 2021. Instead, use qiskit.qobj.QasmQobj or qiskit.qobj.PulseQobj.

The decorator qiskit.utils.deprecation.deprecate_function() has been deprecated since Qiskit 0.39.0 (released on October 2022, with qiskit-terra 0.22.0) and now is been removed. Use qiskit.utils.deprecate_func() instead.

The function execute() does not accept the arguments qobj_id and qobj_header any more. Their use was deprecated in Qiskit 0.37 (with Terra 0.21), released on June 2022.

The transpilation pass qiskit.transpiler.passes.CXDirection is removed. Its use was deprecated in Qiskit 0.37 (with Terra 0.21), released on June 2022. Instead, use the more generic GateDirection pass.

The transpilation pass qiskit.transpiler.passes.CheckCXDirection is removed. Its use was deprecated in Qiskit 0.37 (with Terra 0.21), released on June 2022. Instead, use the more generic CheckGateDirection pass.

Building Qiskit from source now requires a Rust compiler compatible with language version 1.64. This has been increased from the previous minimum supported Rust version of 1.61 for building earlier versions of Qiskit.

Algorithms Deprecations
The algorithm utils in qiskit.utils.validation and qiskit.utils.algorithm_globals are now deprecated and will be removed in no less than 3 months from the release date. These utils were introduced with the qiskit.algorithms module to support legacy and primitive-based algorithm workflows. Now that qiskit.algorithms is deprecated and the primitive-based algorithms codebase has been migrated to a standalone library, these utils are no longer used in the context of Qiskit. If your application allows it, we recommend that you migrate your code to use qiskit_algorithms, where you will be able to import the relevant utilities in algorithm_globals and validation from qiskit_algorithms.utils. Please note that legacy functionality has not been migrated to the new package.
Circuits Deprecations
Passing None as the qargs or cargs arguments to DAGCircuit.apply_operation_back() or apply_operation_front() is deprecated and will be removed in Qiskit 1.0. This has been explicitly against the typing documentation for some time, but silently accepted by Qiskit. Instead, simply pass () rather than None.

The method QuantumCircuit.bind_parameters() is now deprecated and will be removed from the codebase in no less than 3 months from the release date. Its functionality overlapped highly with QuantumCircuit.assign_parameters(), and can be totally replaced by it. Please use QuantumCircuit.assign_parameters() instead.

Deprecate duplicate gate methods on QuantumCircuit. The rule applied is that the method names reflect that gate names, e.g. the CXGate is added via QuantumCircuit.cx() and not QuantumCircuit.cnot(). The deprecations are:

QuantumCircuit.cnot() in favor of QuantumCircuit.cx()
QuantumCircuit.toffoli() in favor of QuantumCircuit.ccx()
QuantumCircuit.fredkin() in favor of QuantumCircuit.cswap()
QuantumCircuit.mct() in favor of QuantumCircuit.mcx()
QuantumCircuit.i() in favor of QuantumCircuit.id()
Note that QuantumCircuit.i() is the only exception to the rule above, but since QuantumCircuit.id() more intuively represents the identity and is used more, we chose it over its counterpart.

To streamline the structure of Qiskit’s gates and operations, the qiskit.extensions module is pending deprecation and will be deprecated in a future release. The following objects have been moved to qiskit.circuit.library

DiagonalGate,
HamiltonianGate,
Initialize,
Isometry,
MCGupDiag,
UCGate,
UCPauliRotGate,
UCRXGate,
UCRYGate,
UCRZGate,
UnitaryGate.
These instructions have already been deprecated in this release,

SingleQubitUnitary, instead use library.UnitaryGate,
Snapshot, which has been superseded by Qiskit Aer’s save instructions,
along with their circuit methods

QuantumCircuit.snapshot(),
QuantumCircuit.squ().
In addition, the following circuit methods are pending deprecation

QuantumCircuit.diagonal(),
QuantumCircuit.hamiltonian(),
QuantumCircuit.isometry() and QuantumCircuit.iso(),
QuantumCircuit.uc(),
QuantumCircuit.ucrx(),
QuantumCircuit.ucry(),
QuantumCircuit.ucrz().
Since the entire module is pending deprecation, so is ExtensionError.

The little-used QuantumCircuit class data attributes header and extension_lib are deprecated and scheduled for removal. These respectively held strings of the OpenQASM 2.0 version header statement and qelib1.inc include statement. No alternative will be provided; these were mostly intended as internal details.

Transpiler Deprecations
The flow controller factory method FlowController.controller_factory() is deprecated along with FlowController.add_flow_controller() and FlowController.remove_flow_controller(). In the future, task construction with keyword arguments in the BasePassManager.append() method will also be deprecated. Controllers must be explicitly instantiated and appended to the pass manager. For example, the previously used conventional syntax


pm.append([task1, task2], condition=lambda x: x["value1"] > 10)
must be replaced with


controller = ConditionalController([task1, task2], condition=lambda x: x["value1"] > 10)
pm.append(controller)
The latter allows more precise control on the order of controllers especially when multiple keyword arguments are specified together, and allows for the construction of general flow controllers that may have more than one pipeline or do not take a single simple conditional function in their constructors.

The FlowControllerLinear.append(), DoWhileController.append(), and ConditionalController.append() methods are all deprecated immediately. The construction of the pass manager task pipeline is now the role of BasePassManager, and individual flow controllers do not need to this method. For a flow controller, all the passes should be specificed in one go directly to the constructor.

The general attribute and variable name passes is replaced with tasks all over the qiskit.passmanager module. Note that a task must indicate a union of pass and controller, and the singular form pass conflicts with the Python keyword. In this sense, the use of tasks is much preferable.

The Unroller transpiler pass has been deprecated and will be removed in a future release. The Unroller has been superseded by the BasisTranslator which provides a similar set of functionality but offers it in a more general manner so that you’re able to translate a circuit to any universal basis set. The Unroller class only works in situations where the circuit’s gate definitions are recursively defined in terms of the target basis; for Qiskit’s standard library gates this means UGate and CXGate. If you are using the Unroller pass it can be replaced by using a custom pass manager of the form:


from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import UnrollCustomDefinitions, BasisTranslator
from qiskit.circuit.equivalence_library import SessionEquivalenceLibrary as sel
 
pm = PassManager(
    [
        UnrollCustomDefinitions(sel, basis_gates=basis_gates),
        BasisTranslator(sel, target_basis=basis_gates),
    ]
)
pm.run(circuit)
The use of the value "unroller" for the translation_method keyword argument on the transpile() and generate_preset_pass_manager() has been deprecated. This translation stage plugin will be removed from Qiskit in a future release as it has been superseded by the default "translator" method which will work similarly to the "unroller" plugin but support a broader set of target backends.

Visualization Deprecations
The default matplotlib drawer setting now issues a FutureWarning, as the default style is changing to the "iqp" style (previously known as "iqx"). The old default is available as the "clifford" style. To silence the warning, you can explicitly set the desired style, e.g.:


from qiskit import QuantumCircuit
 
circuit = QuantumCircuit(2)
circuit.x(0)
circuit.h(0)
circuit.cp(0.5, 0, 1)
 
circuit.draw("mpl", style="clifford")  # or style="iqp"
Passing a circuit to qiskit.visualization.timeline_drawer() that does not have scheduled node start-time information is deprecated. Only circuits that have gone through one of the scheduling analysis passes (for example ALAPScheduleAnalysis or ASAPScheduleAnalysis) can be visualised. If you have used one of the old-style scheduling passes (for example ALAPSchedule or ASAPSchedule), you can propagate the scheduling information by running:


from qiskit import transpile
from qiskit.transpiler import InstructionDurations
 
scheduled = transpile(
  my_old_style_circuit,
  optimization_level=0,
  scheduling_method="alap",
  instruction_durations=InstructionDurations(),
)
This behaviour was previously intended to be deprecated in Qiskit 0.37, but due to a bug in the warning, it was not displayed to users until now. The behaviour will be removed in Qiskit 1.0.

Bug Fixes
The maximum number of qubits to consider for matrix multiplication-based commutativity check in CommutationChecker is now limited to 3 by default. Fixed #10488

The GateDirection transpiler pass will now use discrete-basis translations rather than relying on a continuous RYGate, which should help make some discrete-basis-set targets slightly more reliable. In general, transpile() only has partial support for basis sets that do not contain a continuously-parametrised operation, and so it may not always succeed in these situations, and will almost certainly not produce optimal results.

Fixed CommutationAnalysis to group gates on a wire into sets, with each set only containing gates that pairwise commute. This prevents CommutationCancellation from performing unsound optimizations. See #8020

CUGate will now behave correctly during calls to QuantumCircuit.assign_parameters(). Previously, it would cause various odd errors, often some time after the initial circuit assignment. See #7326, #7410, #9627, #10002, and #10131.

The control-flow builder interface (the context-manager forms of QuantumCircuit.if_test(), while_loop(), for_loop() and switch()) will now correctly track a separate global-phase advancement within that block. You can add a global-phase advancement to an inner block by assigning to QuantumCircuit.global_phase within a builder scope:


from math import pi
from qiskit import QuantumCircuit
 
qc = QuantumCircuit(3, 3)
qc.global_phase = pi / 2  # Set the outer circuit's global phase.
 
with qc.if_test((qc.clbits[0], False)) as else_:
  # The global phase advancement in a control-flow block begins at 0,
  # because it represents how much the phase will be advanced by an
  # execution of the block.  The defined phase of the outer scope is not
  # affected by this set.
  qc.global_phase = pi
with else_:
  # Similarly, the `else` block may induce a different global-phase
  # advancement to the `if`, so it can also be set separately.
  qc.global_phase = 1.5 * pi
 
# The phase advancement caused directly by the outer scope is independent
# of the phase advancement conditionally caused by each control-flow path.
assert qc.global_phase == pi / 2
The meaning of QuantumCircuit.global_phase is taken to be the global-phase advancement that is inherent to a single execution of the block. It is still a global phase advancement, in that if the block is entered, the phase of all qubits in the entire program will be advanced.

Fix the coloring of the "iqx" and "iqx-dark" matplotlib color schemes, which previously drew the RZGate, RZZGate, (multi-)controlled PhaseGates and iSwapGate in the wrong color.

The hash of a Parameter is now equal to the hashes of any ParameterExpression that it compares equal to. Previously the hashes were different, which would cause spurious additional entries in hashmaps when Parameter and ParameterExpression values were mixed in the same map as it violated Python’s data model.

Fixed a bug in QPY serialization (qiskit.qpy) where controlled unitary gates in a circuit could result would fail to deserialize. Fixed #10802.

Fixes the implementation of random_statevector() so that it samples from the uniform distribution.

The pass NoiseAdaptiveLayout now takes CouplingMap as an optional argument. This is used by the plugin to control on inconsistency between configuration() and properties(), like in the case of FakeMelbourne. Fixed #7677.

The methods QuantumCircuit.copy() and copy_empty_like() will now raise an error if the name argument is incorrectly typed, instead of generating an invalid circuit.

The "decay" heuristic of SabreSwap and SabreLayout now tracks the depth correctly on physical qubits rather than mistakenly tracking the “depth” of swaps on virtual qubits.

Fixed an oversight in the ECRGate that prevented setting an ECRGate.label attribute at object construction time. All other Gate classes and subclasses enable setting a label keyword argument in the constructor.

Fixed an oversight in the Gate (and standard-library subclasses) constructor where the duration and unit attributes could not be set as keyword arguments during construction. The parent class Instruction supported setting this but Gate was previously not exposing this interface correctly.

Added support to allow SparsePauliOp default initialization passing an empty iterable to the static methods from_list() and from_sparse_list(). Fixed #10159.

The use of the (deprecated) Optimizer class on AQC did not have a non-deprecated alternative path, which should have been introduced in Qiskit 0.44. It now accepts a callable that implements the Minimizer protocol, as explicitly stated in the deprecation warning. The callable can look like the following example:


from scipy.optimize import minimize
from qiskit.transpiler.synthesis.aqc.aqc import AQC
 
optimizer = partial(minimize, args=(), method="L-BFGS-B", options={"maxiter": 200})
aqc = AQC(optimizer=optimizer)
Fixed an issue with the Barrier class. When adding a Barrier instance to a QuantumCircuit with the QuantumCircuit.append() method previously there was no validation that the size of the barrier matched the qargs specified.

The BlockCollapser transpiler pass will now correctly handle circuits that contain more than one condition on the same classical register.

BlueprintCircuit subclasses will now behave correctly when the semi-public method QuantumCircuit._append() is used with the blueprint in an unbuilt state, i.e. the circuit will be built before attempting the append.

Adjusted zoom, fontsize, and margins in plot_state_city() to fit the plot better for more figure sizes. Corrected the Z-ordering behavior of bars and the zero-amplitude plane, and corrected display of negative real value bars.

Other Notes
This version of Qiskit is explicitly pinned to the Numpy 1.x series, because it includes compiled extensions that are not yet compiled against the as-yet-unreleased Numpy 2.x series. We will release a new version of Qiskit with Numpy 2.x support as soon as feasible.

We cannot prevent your package manager from resolving to older versions of Qiskit (which do not have the same pin but are still likely to be incompatible) if you forcibly try to install Qiskit alongside Numpy 2, before we have released a compatible version.

Modified the behavior of the VF2Layout and VF2PostLayout transpiler passes, which would previously run their internal scoring using multithreading if the input circuits were sufficiently large. The multithreading usage has now been removed from the passes, as it was shown to cause a performance regression instead of an improvement like originally intended.

