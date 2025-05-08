IBM Quantum Platform is moving and this version will be sunset on July 1. To get started on the new platform, read the migration guide.

Qiskit 0.40 release notes

0.40.0

This release officially deprecates the Qiskit IBMQ provider project as part of the Qiskit metapackage. This means that in a future release, pip install qiskit will no longer automatically include qiskit-ibmq-provider. If you’re currently installing or listing qiskit as a dependency to get qiskit-ibmq-provider, you should update to explicitly include qiskit-ibmq-provider as well. This is being done as the Qiskit project moves towards a model where the qiskit package only contains the common core functionality for building and compiling quantum circuits, programs, and applications. Packages that build on that core or link Qiskit to hardware or simulators will be installable as separate packages.

Terra 0.23.0

Prelude

Qiskit Terra 0.23.0 is a major feature release that includes a multitude of new features and bugfixes. The highlights for this release are:

Support for importing OpenQASM 3 programs and creating QuantumCircuit objects from the input program via two new functions qiskit.qasm3.load() and qiskit.qasm3.loads().

Improvements to the library of synthesis algorithms included in Qiskit. This includes the following new synthesis functions:

Clifford Synthesis

Linear Function Synthesis:

Permutation Synthesis:

SolovayKitaevDecomposition detailed in: https://arxiv.org/abs/quant-ph/0505030

New plugins for HighLevelSynthesis:

New plugin for UnitarySynthesis

Performance improvements to SabreLayout. The pass is now primarily written in Rust which can lead to a runtime improvement, however the bigger improvement is in the quality of the output (on average, fewer SwapGate gates introduced by SabreSwap). For example, running SabreLayout and SabreSwap on Bernstein Vazirani circuits targeting the FakeSherbrooke backend yields the following results:

This release also deprecates support for running with Python 3.7. A DeprecationWarning will now be emitted if you run Qiskit with Python 3.7. Support for Python 3.7 will be removed as part of the 0.25.0 release (currently planned for release in July 2023), at which point you will need Python 3.8 or newer to use Qiskit.

New Features

The pulses in qiskit.pulse.library

can be initialized with new parameter angle, such that two float parameters could be provided: amp and angle. Initialization with complex amp is still supported.

The AdaptVQE class has a new attribute, eigenvalue_history, which is used to track the lowest achieved energy per iteration of the AdaptVQE. For example:

the returned value of calc.history should be roughly [-1.85727503] as there is a single iteration.

The runtime logging when running the AdaptVQE has been improved. When running the class now, DEBUG and INFO level log messages will be emitted as the class runs.

Added a new transpiler pass, CollectAndCollapse, to collect and to consolidate blocks of nodes in a circuit. This pass is designed to be a general base class for combined block collection and consolidation. To be completely general, the work of collecting and collapsing the blocks is done via functions provided during instantiating the pass. For example, the CollectLinearFunctions has been updated to inherit from CollectAndCollapse and collects blocks of CXGate and SwapGate gates, and replaces each block with a LinearFunction. The CollectCliffords which is also now based on CollectAndCollapse, collects blocks of “Clifford” gates and replaces each block with a Clifford.

The interface also supports the option do_commutative_analysis, which allows to exploit commutativity between gates in order to collect larger blocks of nodes. For example, collecting blocks of CX gates in the following circuit:

using do_commutative_analysis enables consolidating the two CX gates, as the first CX gate and the Z gate commute.

Added a new class BlockCollector that implements various collection strategies, and a new class BlockCollapser that implements various collapsing strategies. Currently BlockCollector includes the strategy to greedily collect all gates adhering to a given filter function (for example, collecting all Clifford gates), and BlockCollapser includes the strategy to consolidate all gates in a block to a single object (or example, a block of Clifford gates can be consolidated to a single Clifford).

Added a new CollectCliffords transpiler pass that collects blocks of Clifford gates and consolidates these blocks into qiskit.quantum_info.Clifford objects. This pass inherits from CollectAndCollapse and in particular supports the option do_commutative_analysis. It also supports two additional options split_blocks and min_block_size. See the release notes for CollectAndCollapse and CollectLinearFunctions for additional details.

The CollectLinearFunctions transpiler pass has several new arguments on its constructor:

do_commutative_analysis: enables exploiting commutativity between gates in order to collect larger blocks of nodes.

split_blocks: enables spliting collected blocks into sub-blocks over disjoint subsets of qubits. For example, in the following circuit:

the single block of CX gates over qubits {0, 1, 2, 3} can be split into two disjoint sub-blocks, one over qubits {0, 2} and the other over qubits {1, 3}.

min_block_size: allows to specify the minimum size of the block to be consolidated, blocks with fewer gates will not be modified. For example, in the following circuit:

the two CX gates will be consolidated when min_block_size is 1 or 2, and will remain unchanged when min_block_size is 3 or larger.

Added a depth-efficient synthesis algorithm synth_cnot_depth_line_kms() for linear reversible circuits LinearFunction over the linear nearest-neighbor architecture, following the paper: https://arxiv.org/abs/quant-ph/0701194.

The DAGCircuit.replace_block_with_op() method will now return the new DAGOpNode that is created when the block is replaced. Previously, calling this method would not return anything.

Added a depth-efficient synthesis algorithm synth_permutation_depth_lnn_kms() for Permutation over the linear nearest-neighbor architecture, following the paper: https://arxiv.org/abs/quant-ph/0701194

Added a new class PermutationGate for representing permutation logic as a circuit element. Unlike the existing Permutation circuit library element which had a static definition this new class avoids synthesizing a permutation circuit when it is declared. This delays the actual synthesis to the transpiler. It also allows enables using several different algorithms for synthesizing permutations, which are available as high-level-synthesis permutation plugins.

Another key feature of the PermutationGate is that implements the __array__ interface for efficiently returning a unitary matrix for a permutation.

Added several high-level-synthesis plugins for synthesizing permutations:

For example:

Added new classes for Quantum Fisher Information (QFI) and Quantum Geometric Tensor (QGT) algorithms using primitives, qiskit.algorithms.gradients.QFI and qiskit.algorithms.gradients.LinCombQGT, to the gradients module: qiskit.algorithms.gradients. For example:

Added a new keyword argument, derivative_type, to the constructor for the LinCombEstimatorGradient. This argument takes a DerivativeType enum that enables specifying to compute only the real or imaginary parts of the gradient.

Added a new option circuit_reverse_bits to the user config file. This allows users to set a boolean for their preferred default behavior of the reverse_bits argument of the circuit drawers QuantumCircuit.draw() and circuit_drawer(). For example, adding a section to the user config file in the default location ~/.qiskit/settings.conf with:

will change the default to display the bits in reverse order.

Added a new class Z2Symmetries to qiskit.quantum_info which is used to identify any Z2Z_2Z2​ symmetries from an input SparsePauliOp.

Added a new pulse directive TimeBlockade. This directive behaves almost identically to the delay instruction, but will be removed before execution. This directive is intended to be used internally within the pulse builder and helps ScheduleBlock represent instructions with absolute time intervals. This allows the pulse builder to convert Schedule into ScheduleBlock, rather than wrapping with Call instructions.

Added primitive-enabled algorithms for Variational Quantum Time Evolution that implement the interface for Quantum Time Evolution. The qiskit.algorithms.VarQRTE class is used for real and the qiskit.algorithms.VarQITE class is used for imaginary quantum time evolution according to a variational principle passed.

Each algorithm accepts a variational principle which implements the ImaginaryVariationalPrinciple abstract interface. The following implementations are included:

For example:

Added rules for converting XXPlusYYGate and XXMinusYYGate to other gates to the SessionEquivalenceLibrary. This enables running transpile() targeting a backend or Target that uses these gates.

Added two new fake backends, FakePrague and FakeSherbrooke to the qiskit.providers.fake_provider module. FakePrague provides a backend with a snapshot of the properties from the IBM Prague Egret R1 backend and FakeSherbrooke provides a backend with a snapshot of the properties from the IBM Sherbrooke Eagle R3 backend.

Added a new keyword argument, allow_unknown_parameters, to the ParameterExpression.bind() and ParameterExpression.subs() methods. When set this new argument enables passing a dictionary containing unknown parameters to these methods without causing an error to be raised. Previously, this would always raise an error without any way to disable that behavior.

The BaseEstimator.run() method’s observables argument now accepts a str or sequence of str input type in addition to the other types already accepted. When used the input string format should match the Pauli string representation accepted by the constructor for Pauli objects.

Added a new constructor method QuantumCircuit.from_instructions() that enables creating a QuantumCircuit object from an iterable of instructions. For example:

The Clifford class now takes an optional copy keyword argument in its constructor. If set to False, then a StabilizerTable provided as input will not be copied, but will be used directly. This can have performance benefits, if the data in the table will never be mutated by any other means.

The performance of Clifford.compose() has been greatly improved for all numbers of qubits. For operators of 20 qubits, the speedup is on the order of 100 times.

Added a new synthesis function synth_clifford_layers(), for synthesizing a Clifford into layers. The algorithm is based on S. Bravyi, D. Maslov, Hadamard-free circuits expose the structure of the Clifford group, arxiv:2003.09412. This decomposes the Clifford into 8 layers of gates including two layers of CZ gates, and one layer of CX gates. For example, a 5-qubit Clifford circuit is decomposed into the following layers:

This method will allow to decompose a Clifford in 2-qubit depth 7n+27n+27n+2 for linear nearest neighbor (LNN) connectivity.

The return types for the power() methods on several standard library gate classes have been updated to return more specific gate objects that result in a less lossy and more efficient output. For example, running power() now returns an IGate instance instead of UnitaryGate as was done previously.

The full list of output types that have been improved are:

Gate Class | Output Class frompower()
CPhaseGate | CPhaseGate
CSGate | CPhaseGate
CSdgGate | CPhaseGate
IGate | IGate.
PhaseGate | PhaseGate
RGate | RGate
RXGate | RXGate
RXXGate | RXXGate
RYGate | RYGate
RYYGate | RYYGate
RZGate | RZGate
RZXGate | RZXGate
RZZGate | RZZGate
SdgGate | PhaseGate
SGate | PhaseGate
TdgGate | PhaseGate
TGate | PhaseGate
XXMinusYYGate | XXMinusYYGate
XXPlusYYGate | XXPlusYYGate
ZGate | PhaseGate
iSwapGate | XXPlusYYGate
The EquivalenceLibrary is now represented internally as a PyDiGraph, this underlying graph object can be accesed from the new graph attribute. This attribute is intended for use internally in Qiskit and therefore should always be copied before being modified by the user to prevent possible corruption of the internal equivalence graph.

The Operator.from_circuit() constructor method now will reverse the output permutation caused by the routing/swap mapping stage of the transpiler. By default if a transpiled circuit had Swap gates inserted the output matrix will have that permutation reversed so the returned matrix will be equivalent to the original un-transpiled circuit. If you’d like to disable this default behavior the ignore_set_layout keyword argument can be set to True to do this (in addition to previous behavior of ignoring the initial layout from transpilation). If you’d like to manually set a final layout you can use the new final_layout keyword argument to pass in a Layout object to use for the output permutation.

Added support to the GateDirection transpiler pass to handle the the symmetric RXXGate, RYYGate, and RZZGate gates. The pass will now correctly handle these gates and simply reverse the qargs order in place without any other modifications.

Added support for using the Python exponentiation operator, **, with Gate objects is now supported. It is equivalent to running the Gate.power() method on the object.

For example:

Added new GaussianSquareDrag pulse shape to the qiskit.pulse.library module. This pulse shape is similar to GaussianSquare but uses the Drag shape during its rise and fall. The correction from the DRAG pulse shape can suppress part of the frequency spectrum of the rise and fall of the pulse which can help avoid exciting spectator qubits when they are close in frequency to the drive frequency of the pulse.

Added a new keyword argument, method, to the constructors for the FiniteDiffEstimatorGradient and FiniteDiffSamplerGradient classes. The method argument accepts a string to indicate the computation method to use for the gradient. There are three methods, available "central", "forward", and "backward". The definition of the methods are:

Method | Computation
"central" | f(x+e)−f(x−e)2e\frac{f(x+e)-f(x-e)}{2e}2ef(x+e)−f(x−e)​
"forward" | f(x+e)−f(x)e\frac{f(x+e) - f(x)}{e}ef(x+e)−f(x)​
"backward" | f(x)−f(x−e)e\frac{f(x)-f(x-e)}{e}ef(x)−f(x−e)​
where eee is the offset epsilon.

All gradient classes in qiskit.algorithms.gradients now preserve unparameterized operations instead of attempting to unroll them. This allows to evaluate gradients on custom, opaque gates that individual primitives can handle and keeps a higher level of abstraction for optimized synthesis and compilation after the gradient circuits have been constructed.

Added a TranslateParameterizedGates pass to map only parameterized gates in a circuit to a specified basis, but leave unparameterized gates untouched. The pass first attempts unrolling and finally translates if a parameterized gate cannot be further unrolled.

The CollectCliffords transpiler pass has been expanded to collect and combine blocks of “clifford gates” into Clifford objects, where “clifford gates” may now also include objects of type LinearFunction, Clifford, and PauliGate. For example:

All the gates will be collected and combined into a single Clifford. Thus the final circuit consists of a single Clifford object.

CouplingMap is now implicitly iterable, with the iteration being identical to iterating through the output of CouplingMap.get_edges(). In other words,

will now function as expected, as will other iterations. This is purely a syntactic convenience.

Added a new function synth_cnot_count_full_pmh() which is used to synthesize linear reversible circuits for all-to-all architectures using the Patel, Markov and Hayes method. This function is identical to the available qiskit.transpiler.synthesis.cnot_synth() function but has a more descriptive name and is more logically placed in the package tree. This new function supersedes the legacy function which will likely be deprecated in a future release.

InstructionScheduleMap has been updated to store backend calibration data in the format of PulseQobj JSON and invokes conversion when the data is accessed for the first time, i.e. lazy conversion. This internal logic update drastically improves the performance of loading backend especially with many calibration entries.

New module qiskit.pulse.calibration_entries has been added. This contains several wrapper classes for different pulse schedule representations.

These classes implement the get_schedule() and get_signature() methods that returns pulse schedule and parameter names to assign, respectively. These classes are internally managed by the InstructionScheduleMap or backend Target, and thus they will not appear in a typical user programs.

Introduced a new subclass ScalableSymbolicPulse, as a subclass of SymbolicPulse. The new subclass behaves the same as SymbolicPulse, except that it assumes that the envelope of the pulse includes a complex amplitude pre-factor of the form amp∗ei×angle\text{amp} * e^{i \times \text{angle}}amp∗ei×angle. This envelope shape matches many common pulses, including all of the pulses in the Qiskit Pulse library (which were also converted to amp, angle representation in this release).

The new subclass removes the non-unique nature of the amp, angle representation, and correctly compares pulses according to their complex amplitude.

Added a new keyword argument, dtype, to the PauliSumOp.from_list() method. When specified this argument can be used to specify the dtype of the numpy array allocated for the SparsePauliOp used internally by the constructed PauliSumOp.

Support for importing OpenQASM 3 programs into Qiskit has been added. This can most easily be accessed using the functions qasm3.loads() and qasm3.load(), to load a program directly from a string and indirectly from a filename, respectively. For example, one can now do:

This will load the program into a QuantumCircuit instance in the variable circuit.

Not all OpenQASM 3 features are supported at first, because Qiskit does not yet have a way to represent advanced classical data processing. The capabilities of the importer will increase along with the capabilities of the rest of Qiskit. The initial feature set of the importer is approximately the same set of features that would be output by the exporter (qasm3.dump() and qasm3.dumps()).

Note that Qiskit’s support of OpenQASM 3 is not meant to provide a totally lossless representation of QuantumCircuits. For that, consider using qiskit.qpy.

The primitives-based gradient classes defined by the BaseEstimatorGradient and BaseSamplerGradient abstract classes have been updated to simplify extending the base interface. There are three new internal overridable methods, _preprocess(), _postprocess(), and _run_unique(). _preprocess() enables a subclass to customize the input gradient circuits and parameters, _postprocess enables to customize the output result, and _run_unique enables calculating the gradient of a circuit with unique parameters.

The SabreLayout transpiler pass has greatly improved performance as it has been re-written in Rust. As part of this rewrite the pass has been transformed from an analysis pass to a transformation pass that will run both layout and routing. This was done to not only improve the runtime performance but also improve the quality of the results. The previous functionality of the pass as an analysis pass can be retained by manually setting the routing_pass argument or using the new skip_routing argument.

The SabreLayout transpiler pass has a new constructor argument layout_trials. This argument is used to control how many random number generator seeds will be attempted to run SabreLayout with. When set the SABRE layout algorithm is run layout_trials number of times and the best quality output (measured in the lowest number of swap gates added) is selected. These seed trials are executed in parallel using multithreading to minimize the potential performance overhead of running layout multiple times. By default if this is not specified the SabreLayout pass will default to using the number of physical CPUs are available on the local system.

Added two new classes SciPyRealEvolver and SciPyImaginaryEvolver that implement integration methods for time evolution of a quantum state. The value and standard deviation of observables as well as the times they are evaluated at can be queried as TimeEvolutionResult.observables and TimeEvolutionResult.times. For example:

Added the SolovayKitaev transpiler pass to run the Solovay-Kitaev algorithm for approximating single-qubit unitaries using a discrete gate set. In combination with the basis translator, this allows to convert any unitary circuit to a universal discrete gate set, which could be implemented fault-tolerantly.

The decomposition can also be used with the unitary synthesis plugin, as the “sk” method on the UnitarySynthesis transpiler pass:

Random-circuit generation with qiskit.circuit.random.random_circuit() is now significantly faster for large circuits.

Random-circuit generation with qiskit.circuit.random.random_circuit() will now output all “standard” gates in Qiskit’s circuit library (qiskit.circuit.library). This includes two 4-qubit gates C3SXGate and RC3XGate, and the allowed values of max_operands have been expanded accordingly.

The Optimize1qGatesDecomposition transpiler pass has a new keyword argument, target, on its constructor. This argument can be used to specify a Target object that represnts the compilation target. If used it superscedes the basis argument to determine if an instruction in the circuit is present on the target backend.

The UnrollCustomDefinitions transpiler pass has a new keyword argument, target, on its constructor. This argument can be used to specify a Target object that represnts the compilation target. If used it superscedes the basis_gates argument to determine if an instruction in the circuit is present on the target backend.

Added the ReverseEstimatorGradient class for a classical, fast evaluation of expectation value gradients based on backpropagation or reverse-mode gradients. This class uses statevectors and thus provides exact gradients but scales exponentially in system size. It is designed for fast reference calculation of smaller system sizes. It can for example be used as:

Added a new keyword argument, use_dag to the constructor for the OneQubitEulerDecomposer class. When use_dag is set to True the output from the decomposer will be a DAGCircuit object instead of QuantumCircuit object. This is useful for transpiler passes that use OneQubitEulerDecomposer (such as Optimize1qGatesDecomposition) as working directly with a DAGCircuit avoids the overhead of converting between QuantumCircuit and DAGCircuit.

Added the ability for analysis passes to set custom heuristic weights for the VF2Layout and VF2PostLayout transpiler passes. If an analysis pass sets the vf2_avg_error_map key in the property set, its value is used for the error weights instead of the error rates from the backend’s Target (or BackendProperties for BackendV1). The value should be an ErrorMap instance, where each value represents the avg error rate for all 1 or 2 qubit operation on those qubits. If a value is NaN, the corresponding edge is treated as an ideal edge (or qubit for 1q operations). For example, an error map created as:

describes a 2 qubit target, where the avg 1q error rate is 0.0024 on qubit 0 and 0.0032 on qubit 1, the avg 2q error rate for gates that operate on (0, 1) is 0.01, and (1, 0) is not supported by the target. This will be used for scoring if it’s set for the vf2_avg_error_map key in the property set when VF2Layout and VF2PostLayout are run. For example:

That will run VF2Layout with the custom scoring from error_map for a 2 qubit Target that doesn’t contain any error rates.

Upgrade Notes

When initializing any of the pulse classes in qiskit.pulse.library:

providing a complex amp argument with a finite angle will result in PulseError now. For example, instead of calling Gaussian(duration=100,sigma=20,amp=0.5j) one should use Gaussian(duration=100,sigma=20,amp=0.5,angle=np.pi/2) instead now. The pulse envelope which used to be defined as amp * ... is in turn defined as amp * exp(1j * angle) * .... This change was made to better support Qiskit Experiments where the amplitude and angle of pulses are calibrated in separate experiments.

For Python 3.7 singledispatchmethod is now a dependency. This was added to enable leveraging the method dispatch mechanism in the standard library of newer versions of Python. If you’re on Python >= 3.8 there is no extra dependency required.

The previously deprecated MSBasisDecomposer transpiler pass available via the qiskit.transpiler.passes module has been removed. It was originally deprecated as part of the Qiskit Terra 0.16.0 release (10-16-2020). Instead the BasisTranslator transpiler pass should be used instead to translate a circuit into an appropriate basis with a RXXGate

EquivalenceLibrary objects that are initialized with the base attribute will no long have a shared reference with the EquivalenceLibrary passed in. In earlier releases if you mutated base after it was used to create a new EquivalenceLibrary instance both instances would reflect that change. This no longer is the case and updates to base will no longer be reflected in the new EquivalenceLibrary. For example, if you created an equivalence library with:

if you modified original_lib with:

in previous releases new_lib would also include the definition of SXGate after it was added to original_lib, but in this release this no longer will be the case. This change was made because of the change in internal data structure to be a graph, which improved performance of the EquivalenceLibrary class, especially when there are multiple runs of the BasisTranslator transpiler pass.

The initial_state argument for the constructor of the NLocal class along with assigning directly to the NLocal.initial_state atrribute must be a QuantumCircuit now. Support for using other types for this argument and attribute is no longer supported. Support for other types was deprecated as part of the Qiskit Terra 0.18.0 release (July 2021).

The LaTeX array drawers (e.g. array_to_latex, Statevector.draw('latex')) now use the same sympy function as the ket-convention drawer. This means it may render some numbers differently to previous releases, but will provide a more consistent experience. For example, it may identify new factors, or rationalize denominators where it did not previously. The default precision has been changed from 5 to 10.

The QPY version format version emitted by dump() has been increased to version 6. This new format version is incompatible with the previous versions and will result in an error when trying to load it with a deserializer that isn’t able to handle QPY version 6. This change was necessary to support the introduction of ScalableSymbolicPulse which was handled by adding a class_name_size attribute to the header of the dumped SymbolicPulse objects.

The __hash__ method for the SymbolicPulse was removed. This was done to reflect the mutable nature (via parameter assignment) of this class which could result in errors when using SymbolicPulse in situtations where a hashable object was required. This means the builtin hash() method and using SymbolicPulse as keys in dictionaries or set members will no longer work.

The names of Register instances (which includes instances of QuantumRegister and ClassicalRegigster) are no longer constrained to be valid OpenQASM 2 identifiers. This is being done as the restriction is overly strict as Qiskit becomes more decoupled from OpenQASM 2, and even the OpenQASM 3 specification is not so restrictive. If you were relying on registers having valid OpenQASM 2 identifier names, you will need to begin escaping the names. A simplistic version of this could be done, for example, by:

The QuantumCircuit methods u1, u2, u3, and their controlled variants cu1, cu3 and mcu1 have been removed following their deprecation in Qiskit Terra 0.16.0. This was to remove gate names that were usually IBM-specific, in favour of the more general methods p(), u(), cp() and cu(). The gate classes U1Gate, U2Gate and U3Gate are still available for use with QuantumCircuit.append(), so backends can still support bases with these gates explicitly given.

The QuantumCircuit methods combine and extend have been removed following their deprecation in Qiskit Terra 0.17.0. This was done because these functions were simply less powerful versions of QuantumCircuit.compose(), which should be used instead.

The removal of extend also means that the + and += operators are no longer defined for QuantumCircuit. Instead, you can use the & and &= operators respectively, which use QuantumCircuit.compose().

The previously deprecated functions: qiskit.circuit.measure.measure() and qiskit.circuit.reset.reset() have been removed. These functions were deprecated in the Qiskit Terra 0.19.0 release (December, 2021). Instead you should use the QuantumCircuit.measure() and QuantumCircuit.reset() methods of the QuantumCircuit object you wish to append a Measure or Reset operation to.

The previously deprecated ParameterView methods which were inherited from set have been removed from ParameterView, the type returned by QuantumCircuit.parameters. The specific methods which have been removed are:

along with support for the Python operators:

These were deprecated in the Qiskit Terra 0.17.0 release (April, 2021). The ParameterView type is now a general sequence view type and doesn’t support these set operations any longer.

The previously deprecated NetworkX converter methods for the DAGCircuit and DAGDependency classes: DAGCircuit.to_networkx(), DAGCircuit.from_networkx(), and DAGDependency.to_networkx() have been removed. These methods were originally deprecated as part of the Qiskit Terra 0.21.0 release (June, 2022). Qiskit has been using rustworkx as its graph library since the qiskit-terra 0.12.0 release and since then the NetworkX converter function have been a lossy process. They were originally added so that users could leverage NetworkX’s algorithms library to leverage functionality not present in DAGCircuit and/or rustworkx. However, since that time both DAGCircuit and rustworkx has matured and offers more functionality and the DAGCircuit is tightly coupled to rustworkx for its operation and having these converter methods provided limited functionality and therefore have been removed.

tweedledum has been removed as a core requirement of Qiskit Terra. The functionality provided (qiskit.circuit.classicalfunction) is still available, if tweedledum is installed manually, such as by:

This change was made because tweedledum development has slowed to the point of not keeping up with new Python and OS releases, and was blocking some Qiskit users from installing Qiskit.

The lazy optional checkers HAS_MATPLOTLIB, HAS_PIL, HAS_PYLATEX and HAS_PDFTOCAIRO are no longer exposed from qiskit.visualization, having been deprecated in Qiskit Terra 0.21. The canonical location for these (and many other lazy checkers) is qiskit.utils.optionals, and all four objects can be found there.

The previously deprecated gate argument to the constructor of the Decompose transpiler pass, along with its matching attribute Decompose.gate have been removed. The argument and attribute were deprecated as part of the Qiskit Terra 0.19.0 release (December, 2021). Instead the gates_to_decompose argument for the constructor along with the Decompose.gates_to_decompose attribute should be used instead. The gates_to_decompose argument and attribute should function the same, but has a more explicit name and also enables specifying lists of gates instead of only supporting a single gate.

The previously deprecated label argument for the constructor of the MCMT and MCMTVChain classes has been removed. It was deprecated as of the Qiskit Terra 0.19.0 release (Decemeber, 2021). Using the label argument on these classes was undefined behavior as they are subclasses of QuantumCircuit instead of Instruction. This would result in the assigned label generally being ignored. If you need to assign a label to an instance of MCMT or MCMTVChain you should convert them to an Gate instance with to_gate() and then assign the desired label to label attribute. For example:

The retworkx dependency for Qiskit has been removed and replaced by rustworkx library. These are the same packages, but rustworkx is the new name for retworkx which was renamed as part of their combined 0.12.0 release. If you were previously using retworkx 0.12.0 with Qiskit then you already installed rustworkx (retworkx 0.12.0 was just a redirect shim for backwards compatibility). This change was made to migrate to the new package name which will be the only supported package in the future.

The default behavior of the SabreLayout compiler pass has changed. The pass is no longer an AnalysisPass and by default will compute the initital layout, apply it to the circuit, and will also run SabreSwap internally and apply the swap mapping and set the final_layout property set with the permutation caused by swap insertions. This means for users running SabreLayout as part of a custom PassManager will need to adjust the pass manager to account for this (unless they were setting the routing_pass argument for SabreLayout). This change was made in the interest of improving the quality output, the layout and routing quality are highly coupled and SabreLayout will now run multiple parallel seed trials and to calculate which seed provides the best results it needs to perform both the layout and routing together. There are three ways you can adjust the usage in your custom pass manager. The first is to avoid using embedding in your preset pass manager. If you were previously running something like:

to compute the layout and then apply it (which was typically followed by routing) you can adjust the usage to just simply be:

as SabreLayout will apply the layout and you no longer need the embedding stage. Alternatively, you can specify the routing_pass argument which will revert SabreLayout to its previous behavior. For example, if you want to run SabreLayout as it was run in previous releases you can do something like:

which will have SabreLayout run as an analysis pass and just set the layout property set. The final approach is to leverage the skip_routing argument on SabreLayout, when this argument is set to True it will skip applying the found layout and inserting the swap gates from routing. However, doing this has a runtime penalty as SabreLayout will still be computing the routing and just does not use this data. The first two approaches outlined do not have additional overhead associated with them.

The layouts computed by the SabreLayout pass (when run without the routing_pass argument) with a fixed seed value may change from previous releases. This is caused by a new random number generator being used as part of the rewrite of the SabreLayout pass in Rust which significantly improved the performance. If you rely on having consistent output you can run the pass in an earlier version of Qiskit and leverage qiskit.qpy to save the circuit and then load it using the current version. Alternatively you can explicitly set the routing_pass argument to an instance of SabreSwap to mirror the previous behavior of SabreLayout:

which will mirror the behavior of the pass in the previous release. Note, that if you were using the swap_trials argument on SabreLayout in previous releases when adjusting the usage to this form that you will need to set trials argument on the SabreSwap constructor if you want to retain the previous output with a fixed seed.

The exact circuit returned by qiskit.circuit.random.random_circuit for a given seed has changed. This is due to efficiency improvements in the internal random-number generation for the function.

The version requirement for the optional feature package qiskit-toqm, installable via pip install qiskit-terra[toqm], has been upgraded from version 0.0.4 to 0.1.0. To use the toqm routing method with transpile() you must now use qiskit-toqm version 0.1.0 or newer. Older versions are no longer discoverable by the transpiler.

The output QuasiDistribution from the Sampler.run method has been updated to filter out any states with a probability of zero. Now if a valid state is missing from the dictionary output it can be assumed to have a 0 probability. Previously, all possible outcomes for a given number of bits (e.g. for a 3 bit result 000, 001, 010, 011, 100, 101, 110, and 111) even if the probability of a given state was 0. This change was made to reduce the size of the output as for larger number of bits the output size could be quite large. Also, filtering the zero probability results makes the output consistent with other implementations of BaseSampler.

The behavior of the pulse builder when a Schedule is called has been upgraded. Called schedules are internally converted into ScheduleBlock representation and now reference mechanism is always applied rather than appending the schedules wrapped by the Call instruction. Note that the converted block doesn’t necessary recover the original alignment context. This is simply an ASAP aligned sequence of pulse instructions with absolute time intervals. This is an upgrade of internal representation of called pulse programs and thus no API changes. However the Call instruction and Schedule no longer appear in the builder’s pulse program. This change guarantees the generated schedule blocks are always QPY compatible. If you are filtering the output schedule instructions by Call, you can access to the ScheduleBlock.references instead to retrieve the called program.

RZXCalibrationBuilder and RZXCalibrationBuilderNoEcho transpiler pass have been upgraded to generate ScheduleBlock. This change guarantees the transpiled circuits are always QPY compatible. If you are directly using rescale_cr_inst(), method from another program or a pass subclass to rescale cross resonance pulse of the device, now this method is turned into a pulse builder macro, and you need to use this method within the pulse builder context to adopts to new release. The method call injects a play instruction to the context pulse program, instead of returning a Play instruction with the stretched pulse.

Deprecation Notes

Support for running Qiskit with Python 3.7 support has been deprecated and will be removed in the qiskit-terra 0.25.0 release. This means starting in the 0.25.0 release you will need to upgrade the Python version you’re using to Python 3.8 or above.

The class LinearFunctionsSynthesis class is now deprecated and will be removed in a future release. It has been superseded by the more general HighLevelSynthesis class which should be used instead. For example, you can instantiate an instance of HighLevelSynthesis that will behave the same way as LinearFunctionSynthesis with:

Support for passing in lists of argument values to the transpile() function is deprecated and will be removed in the 0.25.0 release. This is being done to facilitate greatly reducing the overhead for parallel execution for transpiling multiple circuits at once. If you’re using this functionality currently you can call transpile() multiple times instead. For example if you were previously doing something like:
You can also leverage parallel_map() or multiprocessing from the Python standard library if you want to run this in parallel.

The legacy version of the pulse drawer present in the qiskit.visualization.pulse has been deprecated and will be removed in a future release. This includes the ScheduleDrawer and :class`WaveformDrawer` classes. This module has been superseded by the qiskit.visualization.pulse_v2 drawer and the typical user API pulse_drawer() and PulseBlock.draw() are already updated internally to use qiskit.visualization.pulse_v2.

The pulse.Instruction.draw() method has been deprecated and will removed in a future release. The need for this method has been superseded by the qiskit.visualization.pulse_v2 drawer which doesn’t require Instrucion objects to have their own draw method. If you need to draw a pulse instruction you should leverage the pulse_drawer() instead.

The import qiskit.circuit.qpy_serialization is deprecated, as QPY has been promoted to the top level. You should import the same objects from qiskit.qpy instead. The old path will be removed in a future of Qiskit Terra.

The qiskit.IBMQ object is deprecated. This alias object lazily redirects attribute access to qiskit.providers.ibmq.IBMQ. As the qiskit-ibmq-provider package has been supersceded by qiskit-ibm-provider package which maintains its own namespace maintaining this alias is no longer relevant with the new package. If you were relying on the qiskit.IBMQ alias you should update your usage to use qiskit.providers.ibmq.IBMQ directly instead (and also consider migrating to qiskit-ibm-provider, see the migration guide for more details).

Several public methods of pulse Qobj converters have been deprecated and in a future release they will no longer be directly callable. The list of methods is:
In InstructionToQobjConverter,
Instead of calling any of these methods directly they will be implicitly selected when a converter instance is directly called. For example:

The qiskit.visualization.state_visualization.num_to_latex_ket() and qiskit.visualization.state_visualization.num_to_latex_terms() functions have been deprecated and will be removed in a future release. These function were primarily used internally by the LaTeX output from Statevector.draw() and DensityMatrix.draw() which no longer are using these function and are leverging sympy for this instead. If you were using these functions you should cosinder using Sympy’s nsimplify() latex() functions.

The method Register.qasm() is deprecated and will be removed in a future release. This method is found on the subclasses QuantumRegister and ClassicalRegister. The deprecation is because the qasm() method promotes a false view of the responsible party for safe conversion to OpenQASM 2; a single object alone does not have the context to provide a safe conversion, such as whether its name clashes after escaping it to produce a valid identifier.

The class-variable regular expression Register.name_format is deprecated and wil be removed in a future release. The names of registers are now permitted to be any valid Python string, so the regular expression has no use any longer.

The functions qiskit.quantum_info.synthesis.decompose_clifford() and qiskit.quantum_info.synthesis.decompose_cnot_dihedral() are deprecated and will be removed in a future release. They are replaced by the two functions qiskit.synthesis.synth_clifford_full() and qiskit.synthesis.synth_cnotdihedral_full() respectively.

