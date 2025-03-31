Qiskit 0.19 release notes
0.19.6
Terra 0.14.2
No Change

Aer 0.5.2
No Change

Ignis 0.3.3
Upgrade Notes
A new requirement scikit-learn has been added to the requirements list. This dependency was added in the 0.3.0 release but wasn’t properly exposed as a dependency in that release. This would lead to an ImportError if the qiskit.ignis.measurement.discriminator.iq_discriminators module was imported. This is now correctly listed as a dependency so that scikit-learn will be installed with qiskit-ignis.
Bug Fixes
Fixes an issue in qiskit-ignis 0.3.2 which would raise an ImportError when qiskit.ignis.verification.tomography.fitters.process_fitter was imported without cvxpy being installed.
Aqua 0.7.3
No Change

IBM Q Provider 0.7.2
No Change

0.19.5
Terra 0.14.2
No Change

Aer 0.5.2
No Change

Ignis 0.3.2
Bug Fixes
The qiskit.ignis.verification.TomographyFitter.fit() method has improved detection logic for the default fitter. Previously, the cvx fitter method was used whenever cvxpy was installed. However, it was possible to install cvxpy without an SDP solver that would work for the cvx fitter method. This logic has been reworked so that the cvx fitter method is only used if cvxpy is installed and an SDP solver is present that can be used. Otherwise, the lstsq fitter is used.
Fixes an edge case in qiskit.ignis.mitigation.measurement.fitters.MeasurementFitter.apply() for input that has invalid or incorrect state labels that don’t match the calibration circuit. Previously, this would not error and just return an empty result. Instead now this case is correctly caught and a QiskitError exception is raised when using incorrect labels.
Aqua 0.7.3
Upgrade Notes
The cvxpy dependency which is required for the svm classifier has been removed from the requirements list and made an optional dependency. This is because installing cvxpy is not seamless in every environment and often requires a compiler be installed to run. To use the svm classifier now you’ll need to install cvxpy by either running pip install cvxpy<1.1.0 or to install it with aqua running pip install qiskit-aqua[cvx].
Bug Fixes
The compose method of the CircuitOp used QuantumCircuit.combine which has been changed to use QuantumCircuit.compose. Using combine leads to the problem that composing an operator with a CircuitOp based on a named register does not chain the operators but stacks them. E.g. composing Z ^ 2 with a circuit based on a 2-qubit named register yielded a 4-qubit operator instead of a 2-qubit operator.
The MatrixOp.to_instruction method previously returned an operator and not an instruction. This method has been updated to return an Instruction. Note that this only works if the operator primitive is unitary, otherwise an error is raised upon the construction of the instruction.
The __hash__ method of the PauliOp class used the id() method which prevents set comparisons to work as expected since they rely on hash tables and identical objects used to not have identical hashes. Now, the implementation uses a hash of the string representation inline with the implementation in the Pauli class.
IBM Q Provider 0.7.2
No Change

0.19.4
Terra 0.14.2
Upgrade Notes
The circuit_to_gate and circuit_to_instruction converters had previously automatically included the generated gate or instruction in the active SessionEquivalenceLibrary. These converters now accept an optional equivalence_library keyword argument to specify if and where the converted instances should be registered. The default behavior is not to register the converted instance.
Bug Fixes
Implementations of the multi-controlled X Gate (MCXGrayCode, MCXRecursive and MCXVChain) have had their name properties changed to more accurately describe their implementation (mcx_gray, mcx_recursive, and mcx_vchain respectively.) Previously, these gates shared the name mcx` with ``MCXGate, which caused these gates to be incorrectly transpiled and simulated.
ControlledGate instances with a set ctrl_state were in some cases not being evaluated as equal, even if the compared gates were equivalent. This has been resolved.
Fixed the SI unit conversion for qiskit.pulse.SetFrequency. The SetFrequency instruction should be in Hz on the frontend and has to be converted to GHz when SetFrequency is converted to PulseQobjInstruction.
Open controls were implemented by modifying a gate's definition. However, when the gate already exists in the basis, this definition is not used, which yields incorrect circuits sent to a backend. This modifies the unroller to output the definition if it encounters a controlled gate with open controls.
Aer 0.5.2
No Change

Ignis 0.3.0
No Change

Aqua 0.7.2
Prelude
VQE expectation computation with Aer qasm_simulator now defaults to a computation that has the expected shot noise behavior.

Upgrade Notes
cvxpy is now in the requirements list as a dependency for qiskit-aqua. It is used for the quadratic program solver which is used as part of the qiskit.aqua.algorithms.QSVM. Previously cvxopt was an optional dependency that needed to be installed to use this functionality. This is no longer required as cvxpy will be installed with qiskit-aqua.
For state tomography run as part of qiskit.aqua.algorithms.HHL with a QASM backend the tomography fitter function qiskit.ignis.verification.StateTomographyFitter.fit() now gets called explicitly with the method set to lstsq to always use the least-squares fitting. Previously it would opportunistically try to use the cvx fitter if cvxpy were installed. But, the cvx fitter depends on a specifically configured cvxpy installation with an SDP solver installed as part of cvxpy which is not always present in an environment with cvxpy installed.
The VQE expectation computation using qiskit-aer’s qiskit.providers.aer.extensions.SnapshotExpectationValue instruction is not enabled by default anymore. This was changed to be the default in 0.7.0 because it is significantly faster, but it led to unexpected ideal results without shot noise (see #1013 for more details). The default has now changed back to match user expectations. Using the faster expectation computation is now opt-in by setting the new include_custom kwarg to True on the qiskit.aqua.algorithms.VQE constructor.
New Features
A new kwarg include_custom has been added to the constructor for qiskit.aqua.algorithms.VQE and it’s subclasses (mainly qiskit.aqua.algorithms.QAOA). When set to true and the expectation kwarg is set to None (the default) this will enable the use of VQE expectation computation with Aer’s qasm_simulator qiskit.providers.aer.extensions.SnapshotExpectationValue instruction. The special Aer snapshot based computation is much faster but with the ideal output similar to state vector simulator.
IBM Q Provider 0.7.2
No Change

0.19.3
Terra 0.14.1
No Change

Aer 0.5.2
Bug Fixes
Fixed bug with statevector and unitary simulators running a number of (parallel) shots equal to the number of CPU threads instead of only running a single shot.
Fixes the “diagonal” qobj gate instructions being applied incorrectly in the density matrix Qasm Simulator method.
Fixes bug where conditional gates were not being applied correctly on the density matrix simulation method.
Fix bug in CZ gate and Z gate for “density_matrix_gpu” and “density_matrix_thrust” QasmSimulator methods.
Fixes issue where memory requirements of simulation were not being checked on the QasmSimulator when using a non-automatic simulation method.
Fixed a memory leak that effected the GPU simulator methods
Ignis 0.3.0
No Change

Aqua 0.7.1
No Change

IBM Q Provider 0.7.2
Bug Fixes
qiskit.provider.ibmq.IBMQBackend.jobs() will now return the correct list of IBMQJob objects when the status kwarg is set to 'RUNNING'. Fixes #523
The package metadata has been updated to properly reflect the dependency on qiskit-terra >= 0.14.0. This dependency was implicitly added as part of the 0.7.0 release but was not reflected in the package requirements so it was previously possible to install qiskit-ibmq-provider with a version of qiskit-terra which was too old. Fixes #677
0.19.0
Terra 0.14.0
Prelude
The 0.14.0 release includes several new features and bug fixes. The biggest change for this release is the introduction of a quantum circuit library in qiskit.circuit.library, containing some circuit families of interest.

The circuit library gives users access to a rich set of well-studied circuit families, instances of which can be used as benchmarks, as building blocks in building more complex circuits, or as a tool to explore quantum computational advantage over classical. The contents of this library will continue to grow and mature.

The initial release of the circuit library contains:

standard_gates: these are fixed-width gates commonly used as primitive building blocks, consisting of 1, 2, and 3 qubit gates. For example the XGate, RZZGate and CSWAPGate. The old location of these gates under qiskit.extensions.standard is deprecated.
generalized_gates: these are families that can generalize to arbitrarily many qubits, for example a Permutation or GMS (Global Molmer-Sorensen gate).
boolean_logic: circuits that transform basis states according to simple Boolean logic functions, such as ADD or XOR.
arithmetic: a set of circuits for doing classical arithmetic such as WeightedAdder and IntegerComparator.
basis_changes: circuits such as the quantum Fourier transform, QFT, that mathematically apply basis changes.
n_local: patterns to easily create large circuits with rotation and entanglement layers, such as TwoLocal which uses single-qubit rotations and two-qubit entanglements.
data_preparation: circuits that take classical input data and encode it in a quantum state that is difficult to simulate, e.g. PauliFeatureMap or ZZFeatureMap.
Other circuits that have proven interesting in the literature, such as QuantumVolume, GraphState, or IQP.
To allow easier use of these circuits as building blocks, we have introduced a compose() method of qiskit.circuit.QuantumCircuit for composition of circuits either with other circuits (by welding them at the ends and optionally permuting wires) or with other simpler gates:


>>> lhs.compose(rhs, qubits=[3, 2], inplace=True)

            ┌───┐                   ┌─────┐                ┌───┐
lqr_1_0: ───┤ H ├───    rqr_0: ──■──┤ Tdg ├    lqr_1_0: ───┤ H ├───────────────
            ├───┤              ┌─┴─┐└─────┘                ├───┤
lqr_1_1: ───┤ X ├───    rqr_1: ┤ X ├───────    lqr_1_1: ───┤ X ├───────────────
         ┌──┴───┴──┐           └───┘                    ┌──┴───┴──┐┌───┐
lqr_1_2: ┤ U1(0.1) ├  +                     =  lqr_1_2: ┤ U1(0.1) ├┤ X ├───────
         └─────────┘                                    └─────────┘└─┬─┘┌─────┐
lqr_2_0: ─────■─────                           lqr_2_0: ─────■───────■──┤ Tdg ├
            ┌─┴─┐                                          ┌─┴─┐        └─────┘
lqr_2_1: ───┤ X ├───                           lqr_2_1: ───┤ X ├───────────────
            └───┘                                          └───┘
lcr_0: 0 ═══════════                           lcr_0: 0 ═══════════════════════
lcr_1: 0 ═══════════                           lcr_1: 0 ═══════════════════════
With this, Qiskit’s circuits no longer assume an implicit initial state of 
∣
0
⟩
∣0⟩, and will not be drawn with this initial state. The all-zero initial state is still assumed on a backend when a circuit is executed.

New Features
A new method, has_entry(), has been added to the qiskit.circuit.EquivalenceLibrary class to quickly check if a given gate has any known decompositions in the library.

A new class IQP, to construct an instantaneous quantum polynomial circuit, has been added to the circuit library module qiskit.circuit.library.

A new compose() method has been added to qiskit.circuit.QuantumCircuit. It allows composition of two quantum circuits without having to turn one into a gate or instruction. It also allows permutations of qubits/clbits at the point of composition, as well as optional inplace modification. It can also be used in place of append(), as it allows composing instructions and operators onto the circuit as well.

qiskit.circuit.library.Diagonal circuits have been added to the circuit library. These circuits implement diagonal quantum operators (consisting of non-zero elements only on the diagonal). They are more efficiently simulated by the Aer simulator than dense matrices.

Add from_label() method to the qiskit.quantum_info.Clifford class for initializing as the tensor product of single-qubit I, X, Y, Z, H, or S gates.

Schedule transformer qiskit.pulse.reschedule.compress_pulses() performs an optimization pass to reduce the usage of waveform memory in hardware by replacing multiple identical instances of a pulse in a pulse schedule with a single pulse. For example:


from qiskit.pulse import reschedule
 
schedules = []
for _ in range(2):
    schedule = Schedule()
    drive_channel = DriveChannel(0)
    schedule += Play(SamplePulse([0.0, 0.1]), drive_channel)
    schedule += Play(SamplePulse([0.0, 0.1]), drive_channel)
    schedules.append(schedule)
 
compressed_schedules = reschedule.compress_pulses(schedules)
The qiskit.transpiler.Layout has a new method reorder_bits() that is used to reorder a list of virtual qubits based on the layout object.

Two new methods have been added to the qiskit.providers.models.PulseBackendConfiguration for interacting with channels.

get_channel_qubits() to get a list of all qubits operated by the given channel and
get_qubit_channel() to get a list of channels operating on the given qubit.
New qiskit.extensions.HamiltonianGate and qiskit.circuit.QuantumCircuit.hamiltonian() methods are introduced, representing Hamiltonian evolution of the circuit wavefunction by a user-specified Hermitian Operator and evolution time. The evolution time can be a Parameter, allowing the creation of parameterized UCCSD or QAOA-style circuits which compile to UnitaryGate objects if time parameters are provided. The Unitary of a HamiltonianGate with Hamiltonian Operator H and time parameter t is 
e
−
i
H
t
e 
−iHt
 .

The circuit library module qiskit.circuit.library now provides a new boolean logic AND circuit, qiskit.circuit.library.AND, and OR circuit, qiskit.circuit.library.OR, which implement the respective operations on a variable number of provided qubits.

New fake backends are added under qiskit.test.mock. These include mocked versions of ibmq_armonk, ibmq_essex, ibmq_london, ibmq_valencia, ibmq_cambridge, ibmq_paris, ibmq_rome, and ibmq_athens. As with other fake backends, these include snapshots of calibration data (i.e. backend.defaults()) and error data (i.e. backend.properties()) taken from the real system, and can be used for local testing, compilation and simulation.

The last_update_date parameter for BackendProperties can now also be passed in as a datetime object. Previously only a string in ISO8601 format was accepted.

Adds qiskit.quantum_info.Statevector.from_int() and qiskit.quantum_info.DensityMatrix.from_int() methods that allow constructing a computational basis state for specified system dimensions.

The methods on the qiskit.circuit.QuantumCircuit class for adding gates (for example h()) which were previously added dynamically at run time to the class definition have been refactored to be statically defined methods of the class. This means that static analyzer (such as IDEs) can now read these methods.

Upgrade Notes
A new package, python-dateutil, is now required and has been added to the requirements list. It is being used to parse datetime strings received from external providers in BackendProperties objects.

The marshmallow schema classes in qiskit.providers.models have been removed since they are no longer used by the BackendObjects.

The output of the to_dict() method for the classes in qiskit.providers.models is no longer in a format for direct JSON serialization. Depending on the content contained in instances of these class there may be numpy arrays and/or complex numbers in the fields of the dict. If you’re JSON serializing the output of the to_dict methods you should ensure your JSON encoder can handle numpy arrays and complex numbers. This includes:

qiskit.providers.models.BackendConfiguration.to_dict()
qiskit.providers.models.BackendProperties.to_dict()
qiskit.providers.models.BackendStatus.to_dict()
qiskit.providers.models.QasmBackendConfiguration.to_dict()
qiskit.providers.models.PulseBackendConfiguration.to_dict()
qiskit.providers.models.UchannelLO.to_dict()
qiskit.providers.models.GateConfig.to_dict()
qiskit.providers.models.PulseDefaults.to_dict()
qiskit.providers.models.Command.to_dict()
qiskit.providers.models.JobStatus.to_dict()
qiskit.providers.models.Nduv.to_dict()
qiskit.providers.models.Gate.to_dict()
Deprecation Notes
The qiskit.dagcircuit.DAGCircuit.compose() method now takes a list of qubits/clbits that specify the positional order of bits to compose onto. The dictionary-based method of mapping using the edge_map argument is deprecated and will be removed in a future release.

The combine_into_edge_map() method for the qiskit.transpiler.Layout class has been deprecated and will be removed in a future release. Instead, the new method reorder_bits() should be used to reorder a list of virtual qubits according to the layout object.

Passing a qiskit.pulse.ControlChannel object in via the parameter channel for the qiskit.providers.models.PulseBackendConfiguration method control() has been deprecated and will be removed in a future release. The ControlChannel objects are now generated from the backend configuration channels attribute which has the information of all channels and the qubits they operate on. Now, the method control() is expected to take the parameter qubits of the form (control_qubit, target_qubit) and type list or tuple, and returns a list of control channels.

The AND and OR methods of qiskit.circuit.QuantumCircuit are deprecated and will be removed in a future release. Instead you should use the circuit library boolean logic classes qiskit.circuit.library.AND amd qiskit.circuit.library.OR and then append those objects to your class. For example:


from qiskit import QuantumCircuit
from qiskit.circuit.library import AND
 
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
 
qc_and = AND(2)
 
qc.compose(qc_and, inplace=True)
The qiskit.extensions.standard module is deprecated and will be removed in a future release. The gate classes in that module have been moved to qiskit.circuit.library.standard_gates.

Bug Fixes
The qiskit.circuit.QuantumCircuit methods inverse(), mirror() methods, as well as the QuantumCircuit.data setter would generate an invalid circuit when used on a parameterized circuit instance. This has been resolved and these methods should now work with a parameterized circuit. Fixes #4235

Previously when creating a controlled version of a standard qiskit gate if a ctrl_state was specified a generic ControlledGate object would be returned whereas without it a standard qiskit controlled gate would be returned if it was defined. This PR allows standard qiskit controlled gates to understand ctrl_state.

Additionally, this PR fixes what might be considered a bug where setting the ctrl_state of an already controlled gate would assume the specified state applied to the full control width instead of the control qubits being added. For instance,:


circ = QuantumCircuit(2)
circ.h(0)
circ.x(1)
gate = circ.to_gate()
cgate = gate.control(1)
c3gate = cgate.control(2, ctrl_state=0)
would apply ctrl_state to all three control qubits instead of just the two control qubits being added.

Fixed a bug in random_clifford() that stopped it from sampling the full Clifford group. Fixes #4271

The qiskit.circuit.Instruction method qiskit.circuit.Instruction.is_parameterized() method had previously returned True for any Instruction instance which had a qiskit.circuit.Parameter in any element of its params array, even if that Parameter had been fully bound. This has been corrected so that .is_parameterized will return False when the instruction is fully bound.

qiskit.circuit.ParameterExpression.subs() had not correctly detected some cases where substituting parameters would result in a two distinct Parameters objects in an expression with the same name. This has been corrected so a CircuitError will be raised in these cases.

Improve performance of qiskit.quantum_info.Statevector and qiskit.quantum_info.DensityMatrix for low-qubit circuit simulations by optimizing the class __init__ methods. Fixes #4281

The function qiskit.compiler.transpile() now correctly handles when the parameter basis_gates is set to None. This will allow any gate in the output tranpiled circuit, including gates added by the transpilation process. Note that using this parameter may have some unintended consequences during optimization. Some transpiler passes depend on having a basis_gates set. For example, qiskit.transpiler.passes.Optimize1qGates only optimizes the chains of u1, u2, and u3 gates and without basis_gates it is unable to unroll gates that otherwise could be optimized:


from qiskit import *
 
q = QuantumRegister(1, name='q')
circuit = QuantumCircuit(q)
circuit.h(q[0])
circuit.u1(0.1, q[0])
circuit.u2(0.1, 0.2, q[0])
circuit.h(q[0])
circuit.u3(0.1, 0.2, 0.3, q[0])
 
result = transpile(circuit, basis_gates=None, optimization_level=3)
result.draw()

     ┌───┐┌─────────────┐┌───┐┌─────────────────┐
q_0: ┤ H ├┤ U2(0.1,0.3) ├┤ H ├┤ U3(0.1,0.2,0.3) ├
     └───┘└─────────────┘└───┘└─────────────────┘
Fixes #3017

Other Notes
The objects in qiskit.providers.models which were previously constructed using the marshmallow library have been refactored to not depend on marshmallow. This includes:

BackendConfiguration
BackendProperties
BackendStatus
QasmBackendConfiguration
PulseBackendConfiguration
UchannelLO
GateConfig
PulseDefaults
Command
JobStatus
Nduv
Gate
These should be drop-in replacements without any noticeable change but specifics inherited from marshmallow may not work. Please file issues for any incompatibilities found.

Aer 0.5.1
No Change

Ignis 0.3.0
No Change

Aqua 0.7.0
Prelude
The Qiskit Aqua 0.7.0 release introduces a lot of new functionality along with an improved integration with qiskit.circuit.QuantumCircuit objects. The central contributions are the Qiskit’s optimization module, a complete refactor on Operators, using circuits as native input for the algorithms and removal of the declarative JSON API.

Optimization module
The qiskit.optimization` module now offers functionality for modeling and solving quadratic programs. It provides various near-term quantum and conventional algorithms, such as the MinimumEigenOptimizer (covering e.g. VQE or QAOA) or CplexOptimizer, as well as a set of converters to translate between different problem representations, such as QuadraticProgramToQubo. See the changelog for a list of the added features.

Operator flow
The operator logic provided in qiskit.aqua.operators` was completely refactored and is now a full set of tools for constructing physically-intuitive quantum computations. It contains state functions, operators and measurements and internally relies on Terra’s Operator objects. Computing expectation values and evolutions was heavily simplified and objects like the ExpectationFactory produce the suitable, most efficient expectation algorithm based on the Operator input type. See the changelog for a overview of the added functionality.

Native circuits
Algorithms commonly use parameterized circuits as input, for example the VQE, VQC or QSVM. Previously, these inputs had to be of type VariationalForm or FeatureMap which were wrapping the circuit object. Now circuits are natively supported in these algorithms, which means any individually constructed QuantumCircuit can be passed to these algorithms. In combination with the release of the circuit library which offers a wide collection of circuit families, it is now easy to construct elaborate circuits as algorithm input.

Declarative JSON API
The ability of running algorithms using dictionaries as parameters as well as using the Aqua interfaces GUI has been removed.

IBM Q Provider 0.7.0
New Features
A new exception, qiskit.providers.ibmq.IBMQBackendJobLimitError, is now raised if a job could not be submitted because the limit on active jobs has been reached.
qiskit.providers.ibmq.job.IBMQJob and qiskit.providers.ibmq.managed.ManagedJobSet each has two new methods update_name and update_tags. They are used to change the name and tags of a job or a job set, respectively.
qiskit.providers.ibmq.IBMQFactory.save_account() and qiskit.providers.ibmq.IBMQFactory.enable_account() now accept optional parameters hub, group, and project, which allow specifying a default provider to save to disk or use, respectively.
Upgrade Notes
The qiskit.providers.ibmq.job.IBMQJob methods creation_date and time_per_step now return date time information as a datetime object in local time instead of UTC. Similarly, the parameters start_datetime and end_datetime, of qiskit.providers.ibmq.IBMQBackendService.jobs() and qiskit.providers.ibmq.IBMQBackend.jobs() can now be specified in local time.
The qiskit.providers.ibmq.job.QueueInfo.format() method now uses a custom datetime to string formatter, and the package arrow is no longer required and has been removed from the requirements list.
Deprecation Notes
The from_dict() and to_dict() methods of qiskit.providers.ibmq.job.IBMQJob are deprecated and will be removed in the next release.
Bug Fixes
Fixed an issue where nest_asyncio.apply() may raise an exception if there is no asyncio loop due to threading.
On this page

