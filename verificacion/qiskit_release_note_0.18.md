Qiskit 0.18 release notes
0.18.3
Terra 0.13.0
No Change

Aer 0.5.1
Upgrade Notes
Changes how transpilation passes are handled in the C++ Controller classes so that each pass must be explicitly called. This allows for greater customization on when each pass should be called, and with what parameters. In particular this enables setting different parameters for the gate fusion optimization pass depending on the QasmController simulation method.
Add gate_length_units kwarg to qiskit.providers.aer.noise.NoiseModel.from_device() for specifying custom gate_lengths in the device noise model function to handle unit conversions for internal code.
Add Controlled-Y (“cy”) gate to the Stabilizer simulator methods supported gateset.
For Aer’s backend the jsonschema validation of input qobj objects from terra is now opt-in instead of being enabled by default. If you want to enable jsonschema validation of qobj set the validate kwarg on the qiskit.providers.aer.QasmSimualtor.run() method for the backend object to True.
Bug Fixes
Remove “extended_stabilizer” from the automatically selected simulation methods. This is needed as the extended stabilizer method is not exact and may give incorrect results for certain circuits unless the user knows how to optimize its configuration parameters.

The automatic method now only selects from “stabilizer”, “density_matrix”, and “statevector” methods. If a non-Clifford circuit that is too large for the statevector method is executed an exception will be raised suggesting you could try explicitly using the “extended_stabilizer” or “matrix_product_state” methods instead.

Fixes Controller classes so that the ReduceBarrier transpilation pass is applied first. This prevents barrier instructions from preventing truncation of unused qubits if the only instruction defined on them was a barrier.

Disables gate fusion for the matrix product state simulation method as this was causing issues with incorrect results being returned in some cases.

Fix error in gate time unit conversion for device noise model with thermal relaxation errors and gate errors. The error probability the depolarizing error was being calculated with gate time in microseconds, while for thermal relaxation it was being calculated in nanoseconds. This resulted in no depolarizing error being applied as the incorrect units would make the device seem to be coherence limited.

Fix bug in incorrect composition of QuantumErrors when the qubits of composed instructions differ.

Fix issue where the “diagonal” gate is checked to be unitary with too high a tolerance. This was causing diagonals generated from Numpy functions to often fail the test.

Fix remove-barrier circuit optimization pass to be applied before qubit trucation. This fixes an issue where barriers inserted by the Terra transpiler across otherwise inactive qubits would prevent them from being truncated.

Ignis 0.3.0
No Change

Aqua 0.6.6
No Change

IBM Q Provider 0.6.1
No Change

0.18.0
Terra 0.13.0
Prelude
The 0.13.0 release includes many big changes. Some highlights for this release are:

For the transpiler we have switched the graph library used to build the qiskit.dagcircuit.DAGCircuit class which is the underlying data structure behind all operations to be based on retworkx for greatly improved performance. Circuit transpilation speed in the 0.13.0 release should be significanlty faster than in previous releases.

There has been a significant simplification to the style in which Pulse instructions are built. Now, Command s are deprecated and a unified set of Instruction s are supported.

The qiskit.quantum_info module includes several new functions for generating random operators (such as Cliffords and quantum channels) and for computing the diamond norm of quantum channels; upgrades to the Statevector and DensityMatrix classes to support computing measurement probabilities and sampling measurements; and several new classes are based on the symplectic representation of Pauli matrices. These new classes include Clifford operators (Clifford), N-qubit matrices that are sparse in the Pauli basis (SparsePauliOp), lists of Pauli’s (PauliTable), and lists of stabilizers (StabilizerTable).

This release also has vastly improved documentation across Qiskit, including improved documentation for the qiskit.circuit, qiskit.pulse and qiskit.quantum_info modules.

Additionally, the naming of gate objects and QuantumCircuit methods have been updated to be more consistent. This has resulted in several classes and methods being deprecated as things move to a more consistent naming scheme.

For full details on all the changes made in this release see the detailed release notes below.

New Features
Added a new circuit library module qiskit.circuit.library. This will be a place for constructors of commonly used circuits that can be used as building blocks for larger circuits or applications.

The qiskit.providers.BaseJob class has four new methods:

done()
running()
cancelled()
in_final_state()
These methods are used to check wheter a job is in a given job status.

Add ability to specify control conditioned on a qubit being in the ground state. The state of the control qubits is represented by an integer. For example:


from qiskit import QuantumCircuit
from qiskit.extensions.standard import XGate
 
qc = QuantumCircuit(4)
cgate = XGate().control(3, ctrl_state=6)
qc.append(cgate, [0, 1, 2, 3])
Creates a four qubit gate where the fourth qubit gets flipped if the first qubit is in the ground state and the second and third qubits are in the excited state. If ctrl_state is None, the default, control is conditioned on all control qubits being excited.

A new jupyter widget, %circuit_library_info has been added to qiskit.tools.jupyter. This widget is used for visualizing details about circuits built from the circuit library. For example


from qiskit.circuit.library import XOR
import qiskit.tools.jupyter
circuit = XOR(5, seed=42)
%circuit_library_info circuit
A new kwarg option, formatted , has been added to qiskit.circuit.QuantumCircuit.qasm() . When set to True the method will print a syntax highlighted version (using pygments) to stdout and return None (which differs from the normal behavior of returning the QASM code as a string).

A new kwarg option, filename , has been added to qiskit.circuit.QuantumCircuit.qasm(). When set to a path the method will write the QASM code to that file. It will then continue to output as normal.

A new instruction SetFrequency which allows users to change the frequency of the PulseChannel. This is done in the following way:


from qiskit.pulse import Schedule
from qiskit.pulse import SetFrequency
 
sched = pulse.Schedule()
sched += SetFrequency(5.5e9, DriveChannel(0))
In this example, the frequency of all pulses before the SetFrequency command will be the default frequency and all pulses applied to drive channel zero after the SetFrequency command will be at 5.5 GHz. Users of SetFrequency should keep in mind any hardware limitations.

A new method, assign_parameters() has been added to the qiskit.circuit.QuantumCircuit class. This method accepts a parameter dictionary with both floats and Parameters objects in a single dictionary. In other words this new method allows you to bind floats, Parameters or both in a single dictionary.

Also, by using the inplace kwarg it can be specified you can optionally modify the original circuit in place. By default this is set to False and a copy of the original circuit will be returned from the method.

A new method num_nonlocal_gates() has been added to the qiskit.circuit.QuantumCircuit class. This method will return the number of gates in a circuit that involve 2 or or more qubits. These gates are more costly in terms of time and error to implement.

The qiskit.circuit.QuantumCircuit method iso() for adding an Isometry gate to the circuit has a new alias. You can now call qiskit.circuit.QuantumCircuit.isometry() in addition to calling iso.

A description attribute has been added to the CouplingMap class for storing a short description for different coupling maps (e.g. full, grid, line, etc.).

A new method compose() has been added to the DAGCircuit class for composing two circuits via their DAGs.


dag_left.compose(dag_right, edge_map={right_qubit0: self.left_qubit1,
                                  right_qubit1: self.left_qubit4,
                                  right_clbit0: self.left_clbit1,
                                  right_clbit1: self.left_clbit0})

            ┌───┐                    ┌─────┐┌─┐
lqr_1_0: ───┤ H ├───     rqr_0: ──■──┤ Tdg ├┤M├
            ├───┤               ┌─┴─┐└─┬─┬─┘└╥┘
lqr_1_1: ───┤ X ├───     rqr_1: ┤ X ├──┤M├───╫─
         ┌──┴───┴──┐            └───┘  └╥┘   ║
lqr_1_2: ┤ U1(0.1) ├  +  rcr_0: ════════╬════╩═  =
         └─────────┘                    ║
lqr_2_0: ─────■─────     rcr_1: ════════╩══════
            ┌─┴─┐
lqr_2_1: ───┤ X ├───
            └───┘
lcr_0:   ═══════════
 
lcr_1:   ═══════════
 
            ┌───┐
lqr_1_0: ───┤ H ├──────────────────
            ├───┤        ┌─────┐┌─┐
lqr_1_1: ───┤ X ├─────■──┤ Tdg ├┤M├
         ┌──┴───┴──┐  │  └─────┘└╥┘
lqr_1_2: ┤ U1(0.1) ├──┼──────────╫─
         └─────────┘  │          ║
lqr_2_0: ─────■───────┼──────────╫─
            ┌─┴─┐   ┌─┴─┐  ┌─┐   ║
lqr_2_1: ───┤ X ├───┤ X ├──┤M├───╫─
            └───┘   └───┘  └╥┘   ║
lcr_0:   ═══════════════════╩════╬═
                                 ║
lcr_1:   ════════════════════════╩═
The mock backends in qiskit.test.mock now have a functional run() method that will return results similar to the real devices. If qiskit-aer is installed a simulation will be run with a noise model built from the device snapshot in the fake backend. Otherwise, qiskit.providers.basicaer.QasmSimulatorPy will be used to run an ideal simulation. Additionally, if a pulse experiment is passed to run and qiskit-aer is installed the PulseSimulator will be used to simulate the pulse schedules.

The qiskit.result.Result() method get_counts() will now return a list of all the counts available when there are multiple circuits in a job. This works when get_counts() is called with no arguments.

The main consideration for this feature was for drawing all the results from multiple circuits in the same histogram. For example it is now possible to do something like:


from qiskit import execute
from qiskit import QuantumCircuit
from qiskit.providers.basicaer import BasicAer
from qiskit.visualization import plot_histogram
 
sim = BasicAer.get_backend('qasm_simulator')
 
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()
result = execute([qc, qc, qc], sim).result()
 
plot_histogram(result.get_counts())
A new kwarg, initial_state has been added to the qiskit.visualization.circuit_drawer() function and the QuantumCircuit method draw(). When set to True the initial state will be included in circuit visualizations for all backends. For example:


from qiskit import QuantumCircuit
 
circuit = QuantumCircuit(2)
circuit.measure_all()
circuit.draw(output='mpl', initial_state=True)
It is now possible to insert a callable into a qiskit.pulse.InstructionScheduleMap which returns a new qiskit.pulse.Schedule when it is called with parameters. For example:


def test_func(x):
   sched = Schedule()
   sched += pulse_lib.constant(int(x), amp_test)(DriveChannel(0))
   return sched
 
inst_map = InstructionScheduleMap()
inst_map.add('f', (0,), test_func)
output_sched = inst_map.get('f', (0,), 10)
assert output_sched.duration == 10
Two new gate classes, qiskit.extensions.iSwapGate and qiskit.extensions.DCXGate, along with their QuantumCircuit methods iswap() and dcx() have been added to the standard extensions. These gates, which are locally equivalent to each other, can be used to enact particular XY interactions. A brief motivation for these gates can be found in: arxiv.org/abs/quant-ph/0209035

The qiskit.providers.BaseJob class now has a new method wait_for_final_state() that polls for the job status until the job reaches a final state (such as DONE or ERROR). This method also takes an optional callback kwarg which takes a Python callable that will be called during each iteration of the poll loop.

The search_width and search_depth attributes of the qiskit.transpiler.passes.LookaheadSwap pass are now settable when initializing the pass. A larger search space can often lead to more optimized circuits, at the cost of longer run time.

The number of qubits in BackendConfiguration can now be accessed via the property num_qubits. It was previously only accessible via the n_qubits attribute.

Two new methods, angles() and angles_and_phase(), have been added to the qiskit.quantum_info.OneQubitEulerDecomposer class. These methods will return the relevant parameters without validation, and calling the OneQubitEulerDecomposer object will perform the full synthesis with validation.

An RR decomposition basis has been added to the qiskit.quantum_info.OneQubitEulerDecomposer for decomposing an arbitrary 2x2 unitary into a two RGate circuit.

Adds the ability to set qargs to objects which are subclasses of the abstract BaseOperator class. This is done by calling the object op(qargs) (where op is an operator class) and will return a shallow copy of the original object with a qargs property set. When such an object is used with the compose() or dot() methods the internal value for qargs will be used when the qargs method kwarg is not used. This allows for subsystem composition using binary operators, for example:


from qiskit.quantum_info import Operator
 
init = Operator.from_label('III')
x = Operator.from_label('X')
h = Operator.from_label('H')
init @ x([0]) @ h([1])
Adds qiskit.quantum_info.Clifford operator class to the quantum_info module. This operator is an efficient symplectic representation an N-qubit unitary operator from the Clifford group. This class includes a to_circuit() method for compilation into a QuantumCircuit of Clifford gates with a minimal number of CX gates for up to 3-qubits. It also providers general compilation for N > 3 qubits but this method is not optimal in the number of two-qubit gates.

Adds qiskit.quantum_info.SparsePauliOp operator class. This is an efficient representaiton of an N-qubit matrix that is sparse in the Pauli basis and uses a qiskit.quantum_info.PauliTable and vector of complex coefficients for its data structure.

This class supports much of the same functionality of the qiskit.quantum_info.Operator class so SparsePauliOp objects can be tensored, composed, scalar multiplied, added and subtracted.

Numpy arrays or Operator objects can be converted to a SparsePauliOp using the :class:`~qiskit.quantum_info.SparsePauliOp.from_operator method. SparsePauliOp can be convered to a sparse csr_matrix or dense Numpy array using the to_matrix method, or to an Operator object using the to_operator method.

A SparsePauliOp can be iterated over in terms of its PauliTable components and coefficients, its coefficients and Pauli string labels using the label_iter() method, and the (dense or sparse) matrix components using the matrix_iter() method.

Add qiskit.quantum_info.diamond_norm() function for computing the diamond norm (completely-bounded trace-norm) of a quantum channel. This can be used to compute the distance between two quantum channels using diamond_norm(chan1 - chan2).

A new class qiskit.quantum_info.PauliTable has been added. This is an efficient symplectic representation of a list of N-qubit Pauli operators. Some features of this class are:

PauliTable objects may be composed, and tensored which will return a PauliTable object with the combination of the operation ( compose(), dot(), expand(), tensor()) between each element of the first table, with each element of the second table.
Addition of two tables acts as list concatination of the terms in each table (+).
Pauli tables can be sorted by lexicographic (tensor product) order or by Pauli weights (sort()).
Duplicate elements can be counted and deleted (unique()).
The PauliTable may be iterated over in either its native symplectic boolean array representation, as Pauli string labels (label_iter()), or as dense Numpy array or sparse CSR matrices (matrix_iter()).
Checking commutation between elements of the Pauli table and another Pauli (commutes()) or Pauli table (commutes_with_all())
See the qiskit.quantum_info.PauliTable class API documentation for additional details.

Adds qiskit.quantum_info.StabilizerTable class. This is a subclass of the qiskit.quantum_info.PauliTable class which includes a boolean phase vector along with the Pauli table array. This represents a list of Stabilizer operators which are real-Pauli operators with +1 or -1 coefficient. Because the stabilizer matrices are real the "Y" label matrix is defined as [[0, 1], [-1, 0]]. See the API documentation for additional information.

Adds qiskit.quantum_info.pauli_basis() function which returns an N-qubit Pauli basis as a qiskit.quantum_info.PauliTable object. The ordering of this basis can either be by standard lexicographic (tensor product) order, or by the number of non-identity Pauli terms (weight).

Adds qiskit.quantum_info.ScalarOp operator class that represents a scalar multiple of an identity operator. This can be used to initialize an identity on arbitrary dimension subsystems and it will be implicitly converted to other BaseOperator subclasses (such as an qiskit.quantum_info.Operator or qiskit.quantum_info.SuperOp) when it is composed with, or added to, them.

Example: Identity operator


from qiskit.quantum_info import ScalarOp, Operator
 
X = Operator.from_label('X')
Z = Operator.from_label('Z')
 
init = ScalarOp(2 ** 3)  # 3-qubit identity
op = init @ X([0]) @ Z([1]) @ X([2])  # Op XZX
A new method, reshape(), has been added to the qiskit.quantum_innfo.Operator class that returns a shallow copy of an operator subclass with reshaped subsystem input or output dimensions. The combined dimensions of all subsystems must be the same as the original operator or an exception will be raised.

Adds qiskit.quantum_info.random_clifford() for generating a random qiskit.quantum_info.Clifford operator.

Add qiskit.quantum_info.random_quantum_channel() function for generating a random quantum channel with fixed Choi-rank in the Stinespring representation.

Add qiskit.quantum_info.random_hermitian() for generating a random Hermitian Operator.

Add qiskit.quantum_info.random_statevector() for generating a random Statevector.

Adds qiskit.quantum_info.random_pauli_table() for generating a random qiskit.quantum_info.PauliTable.

Adds qiskit.quantum_info.random_stabilizer_table() for generating a random qiskit.quantum_info.StabilizerTable.

Add a num_qubits attribute to qiskit.quantum_info.StateVector and qiskit.quantum_info.DensityMatrix classes. This returns the number of qubits for N-qubit states and returns None for non-qubit states.

Adds to_dict() and to_dict() methods to convert qiskit.quantum_info.Statevector and qiskit.quantum_info.DensityMatrix objects into Bra-Ket notation dictionary.

Example


from qiskit.quantum_info import Statevector
 
state = Statevector.from_label('+0')
print(state.to_dict())

from qiskit.quantum_info import DensityMatrix
 
state = DensityMatrix.from_label('+0')
print(state.to_dict())
Adds probabilities() and probabilities() to qiskit.quantum_info.Statevector and qiskit.quantum_info.DensityMatrix classes which return an array of measurement outcome probabilities in the computational basis for the specified subsystems.

Example


from qiskit.quantum_info import Statevector
 
state = Statevector.from_label('+0')
print(state.probabilities())

from qiskit.quantum_info import DensityMatrix
 
state = DensityMatrix.from_label('+0')
print(state.probabilities())
Adds probabilities_dict() and probabilities_dict() to qiskit.quantum_info.Statevector and qiskit.quantum_info.DensityMatrix classes which return a count-style dictionary array of measurement outcome probabilities in the computational basis for the specified subsystems.


from qiskit.quantum_info import Statevector
 
state = Statevector.from_label('+0')
print(state.probabilities_dict())

from qiskit.quantum_info import DensityMatrix
 
state = DensityMatrix.from_label('+0')
print(state.probabilities_dict())
Add sample_counts() and sample_memory() methods to the Statevector and DensityMatrix classes for sampling measurement outcomes on subsystems.

Example:

Generate a counts dictionary by sampling from a statevector


from qiskit.quantum_info import Statevector
 
psi = Statevector.from_label('+0')
shots = 1024
 
# Sample counts dictionary
counts = psi.sample_counts(shots)
print('Measure both:', counts)
 
# Qubit-0
counts0 = psi.sample_counts(shots, [0])
print('Measure Qubit-0:', counts0)
 
# Qubit-1
counts1 = psi.sample_counts(shots, [1])
print('Measure Qubit-1:', counts1)
Return the array of measurement outcomes for each sample


from qiskit.quantum_info import Statevector
 
psi = Statevector.from_label('-1')
shots = 10
 
# Sample memory
mem = psi.sample_memory(shots)
print('Measure both:', mem)
 
# Qubit-0
mem0 = psi.sample_memory(shots, [0])
print('Measure Qubit-0:', mem0)
 
# Qubit-1
mem1 = psi.sample_memory(shots, [1])
print('Measure Qubit-1:', mem1)
Adds a measure() method to the qiskit.quantum_info.Statevector and qiskit.quantum_info.DensityMatrix quantum state classes. This allows sampling a single measurement outcome from the specified subsystems and collapsing the statevector to the post-measurement computational basis state. For example


from qiskit.quantum_info import Statevector
 
psi = Statevector.from_label('+1')
 
# Measure both qubits
outcome, psi_meas = psi.measure()
print("measure([0, 1]) outcome:", outcome, "Post-measurement state:")
print(psi_meas)
 
# Measure qubit-1 only
outcome, psi_meas = psi.measure([1])
print("measure([1]) outcome:", outcome, "Post-measurement state:")
print(psi_meas)
Adds a reset() method to the qiskit.quantum_info.Statevector and qiskit.quantum_info.DensityMatrix quantum state classes. This allows reseting some or all subsystems to the 
∣
0
⟩
∣0⟩ state. For example


from qiskit.quantum_info import Statevector
 
psi = Statevector.from_label('+1')
 
# Reset both qubits
psi_reset = psi.reset()
print("Post reset state: ")
print(psi_reset)
 
# Reset qubit-1 only
psi_reset = psi.reset([1])
print("Post reset([1]) state: ")
print(psi_reset)
A new visualization function qiskit.visualization.visualize_transition() for visualizing single qubit gate transitions has been added. It takes in a single qubit circuit and returns an animation of qubit state transitions on a Bloch sphere. To use this function you must have installed the dependencies for and configured globally a matplotlib animtion writer. You can refer to the matplotlib documentation for more details on this. However, in the default case simply ensuring that FFmpeg is installed is sufficient to use this function.

It supports circuits with the following gates:

HGate
XGate
YGate
ZGate
RXGate
RYGate
RZGate
SGate
SdgGate
TGate
TdgGate
U1Gate
For example:


from qiskit.visualization import visualize_transition
from qiskit import *
 
qc = QuantumCircuit(1)
qc.h(0)
qc.ry(70,0)
qc.rx(90,0)
qc.rz(120,0)
 
visualize_transition(qc, fpg=20, spg=1, trace=True)
execute() has a new kwarg schedule_circuit. By setting schedule_circuit=True this enables scheduling of the circuit into a Schedule. This allows users building qiskit.circuit.QuantumCircuit objects to make use of custom scheduler methods, such as the as_late_as_possible and as_soon_as_possible methods. For example:


job = execute(qc, backend, schedule_circuit=True,
              scheduling_method="as_late_as_possible")
A new environment variable QISKIT_SUPPRESS_PACKAGING_WARNINGS can be set to Y or y which will suppress the warnings about qiskit-aer and qiskit-ibmq-provider not being installed at import time. This is useful for users who are only running qiskit-terra (or just not qiskit-aer and/or qiskit-ibmq-provider) and the warnings are not an indication of a potential packaging problem. You can set the environment variable to N or n to ensure that warnings are always enabled even if the user config file is set to disable them.

A new user config file option, suppress_packaging_warnings has been added. When set to true in your user config file like:


[default]
suppress_packaging_warnings = true
it will suppress the warnings about qiskit-aer and qiskit-ibmq-provider not being installed at import time. This is useful for users who are only running qiskit-terra (or just not qiskit-aer and/or qiskit-ibmq-provider) and the warnings are not an indication of a potential packaging problem. If the user config file is set to disable the warnings this can be overridden by setting the QISKIT_SUPPRESS_PACKAGING_WARNINGS to N or n

qiskit.compiler.transpile() has two new kwargs, layout_method and routing_method. These allow you to select a particular method for placement and routing of circuits on constrained architectures. For, example:


transpile(circ, backend, layout_method='dense',
          routing_method='lookahead')
will run DenseLayout layout pass and LookaheadSwap routing pass.

There has been a significant simplification to the style in which Pulse instructions are built.

With the previous style, Command s were called with channels to make an Instruction. The usage of both commands and instructions was a point of confusion. This was the previous style:


sched += Delay(5)(DriveChannel(0))
sched += ShiftPhase(np.pi)(DriveChannel(0))
sched += SamplePulse([1.0, ...])(DriveChannel(0))
sched += Acquire(100)(AcquireChannel(0), MemorySlot(0))
or, equivalently (though less used):


sched += DelayInstruction(Delay(5), DriveChannel(0))
sched += ShiftPhaseInstruction(ShiftPhase(np.pi), DriveChannel(0))
sched += PulseInstruction(SamplePulse([1.0, ...]), DriveChannel(0))
sched += AcquireInstruction(Acquire(100), AcquireChannel(0),
                            MemorySlot(0))
Now, rather than build a command and an instruction, each command has been migrated into an instruction:


sched += Delay(5, DriveChannel(0))
sched += ShiftPhase(np.pi, DriveChannel(0))
sched += Play(SamplePulse([1.0, ...]), DriveChannel(0))
sched += SetFrequency(5.5, DriveChannel(0))  # New instruction!
sched += Acquire(100, AcquireChannel(0), MemorySlot(0))
There is now a Play instruction which takes a description of a pulse envelope and a channel. There is a new Pulse class in the pulse_lib from which the pulse envelope description should subclass.

For example:


Play(SamplePulse([0.1]*10), DriveChannel(0))
Play(ConstantPulse(duration=10, amp=0.1), DriveChannel(0))
Upgrade Notes
The qiskit.dagcircuit.DAGNode method pop which was deprecated in the 0.9.0 release has been removed. If you were using this method you can leverage Python’s del statement or delattr() function to perform the same task.

A new optional visualization requirement, pygments , has been added. It is used for providing syntax highlighting of OpenQASM 2.0 code in Jupyter widgets and optionally for the qiskit.circuit.QuantumCircuit.qasm() method. It must be installed (either with pip install pygments or pip install qiskit-terra[visualization]) prior to using the %circuit_library_info widget in qiskit.tools.jupyter or the formatted kwarg on the qasm() method.

The pulse buffer option found in qiskit.pulse.Channel and qiskit.pulse.Schedule was deprecated in Terra 0.11.0 and has now been removed. To add a delay on a channel or in a schedule, specify it explicitly in your Schedule with a Delay:


sched = Schedule()
sched += Delay(5)(DriveChannel(0))
PulseChannelSpec, which was deprecated in Terra 0.11.0, has now been removed. Use BackendConfiguration instead:


config = backend.configuration()
drive_chan_0 = config.drives(0)
acq_chan_0 = config.acquires(0)
or, simply reference the channel directly, such as DriveChannel(index).

An import path was deprecated in Terra 0.10.0 and has now been removed: for PulseChannel, DriveChannel, MeasureChannel, and ControlChannel, use from qiskit.pulse.channels import X in place of from qiskit.pulse.channels.pulse_channels import X.

The pass qiskit.transpiler.passes.CSPLayout (which was introduced in the 0.11.0 release) has been added to the preset pass manager for optimization levels 2 and 3. For level 2, there is a call limit of 1,000 and a timeout of 10 seconds. For level 3, the call limit is 10,000 and the timeout is 1 minute.

Now that the pass is included in the preset pass managers the python-constraint package is not longer an optional dependency and has been added to the requirements list.

The TranspileConfig class which was previously used to set run time configuration for a qiskit.transpiler.PassManager has been removed and replaced by a new class qiskit.transpile.PassManagerConfig. This new class has been structured to include only the information needed to construct a PassManager. The attributes of this class are:

initial_layout
basis_gates
coupling_map
backend_properties
seed_transpiler
The function transpile_circuit in qiskit.transpiler has been removed. To transpile a circuit with a custom PassManager now you should use the run() method of the :class:~qiskit.transpiler.PassManager` object.

The QuantumCircuit method draw() and qiskit.visualization.circuit_drawer() function will no longer include the initial state included in visualizations by default. If you would like to retain the initial state in the output visualization you need to set the initial_state kwarg to True. For example, running:


from qiskit import QuantumCircuit
 
circuit = QuantumCircuit(2)
circuit.measure_all()
circuit.draw(output='text')
This no longer includes the initial state. If you’d like to retain it you can run:


from qiskit import QuantumCircuit
 
circuit = QuantumCircuit(2)
circuit.measure_all()
circuit.draw(output='text', initial_state=True)
qiskit.compiler.transpile() (and qiskit.execute.execute(), which uses transpile internally) will now raise an error when the pass_manager kwarg is set and a value is set for other kwargs that are already set in an instantiated PassManager object. Previously, these conflicting kwargs would just be silently ignored and the values in the PassManager instance would be used. For example:


from qiskit.circuit import QuantumCircuit
from qiskit.transpiler.pass_manager_config import PassManagerConfig
from qiskit.transpiler import preset_passmanagers
from qiskit.compiler import transpile
 
qc = QuantumCircuit(5)
 
config = PassManagerConfig(basis_gates=['u3', 'cx'])
pm = preset_passmanagers.level_0_pass_manager(config)
transpile(qc, optimization_level=3, pass_manager=pm)
will now raise an error while prior to this release the value in pm would just silently be used and the value for the optimization_level kwarg would be ignored. The transpile kwargs this applies to are:

optimization_level
basis_gates
coupling_map
seed_transpiler
backend_properties
initial_layout
layout_method
routing_method
backend
The Operator, Clifford, SparsePauliOp, PauliTable, StabilizerTable, operator classes have an added call method that allows them to assign a qargs to the operator for use with the compose(), dot(), evolve(),``+``, and - operations.

The addition method of the qiskit.quantum_info.Operator, class now accepts a qarg kwarg to allow adding a smaller operator to a larger one assuming identities on the other subsystems (same as for qargs on compose() and dot() methods). This allows subsystem addition using the call method as with composition. This support is added to all BaseOperator subclasses (ScalarOp, Operator, QuantumChannel).

For example:


from qiskit.quantum_info import Operator, ScalarOp
 
ZZ = Operator.from_label('ZZ')
 
# Initialize empty Hamiltonian
n_qubits = 10
ham = ScalarOp(2 ** n_qubits, coeff=0)
 
# Add 2-body nearest neighbour terms
for j in range(n_qubits - 1):
    ham = ham + ZZ([j, j+1])
The BaseOperator class has been updated so that addition, subtraction and scalar multiplication are no longer abstract methods. This means that they are no longer required to be implemented in subclasses if they are not supported. The base class will raise a NotImplementedError when the methods are not defined.

The qiskit.quantum_info.random_density_matrix() function will now return a random DensityMatrix object. In previous releases it returned a numpy array.

The qiskit.quantum_info.Statevector and qiskit.quantum_info.DensityMatrix classes no longer copy the input array if it is already the correct dtype.

fastjsonschema is added as a dependency. This is used for much faster validation of qobj dictionaries against the JSON schema when the to_dict() method is called on qobj objects with the validate keyword argument set to True.

The qobj construction classes in qiskit.qobj will no longer validate against the qobj jsonschema by default. These include the following classes:

qiskit.qobj.QasmQobjInstruction
qiskit.qobj.QobjExperimentHeader
qiskit.qobj.QasmQobjExperimentConfig
qiskit.qobj.QasmQobjExperiment
qiskit.qobj.QasmQobjConfig
qiskit.qobj.QobjHeader
qiskit.qobj.PulseQobjInstruction
qiskit.qobj.PulseQobjExperimentConfig
qiskit.qobj.PulseQobjExperiment
qiskit.qobj.PulseQobjConfig
qiskit.qobj.QobjMeasurementOption
qiskit.qobj.PulseLibraryItem
qiskit.qobj.QasmQobjInstruction
qiskit.qobj.QasmQobjExperimentConfig
qiskit.qobj.QasmQobjExperiment
qiskit.qobj.QasmQobjConfig
qiskit.qobj.QasmQobj
qiskit.qobj.PulseQobj
If you were relying on this validation or would like to validate them against the qobj schema this can be done by setting the validate kwarg to True on to_dict() method from either of the top level Qobj classes QasmQobj or PulseQobj. For example:

which will validate the output dictionary against the Qobj jsonschema.

The output dictionary from qiskit.qobj.QasmQobj.to_dict() and qiskit.qobj.PulseQobj.to_dict() is no longer in a format for direct json serialization as expected by IBMQ’s API. These Qobj objects are the current format we use for passing experiments to providers/backends and while having a dictionary format that could just be passed to the IBMQ API directly was moderately useful for qiskit-ibmq-provider, it made things more difficult for other providers. Especially for providers that wrap local simulators. Moving forward the definitions of what is passed between providers and the IBMQ API request format will be further decoupled (in a backwards compatible manner) which should ease the burden of writing providers and backends.

In practice, the only functional difference between the output of these methods now and previous releases is that complex numbers are represented with the complex type and numpy arrays are not silently converted to list anymore. If you were previously calling json.dumps() directly on the output of to_dict() after this release a custom json encoder will be needed to handle these cases. For example:


import json
 
from qiskit.circuit import ParameterExpression
from qiskit import qobj
 
my_qasm = qobj.QasmQobj(
    qobj_id='12345',
    header=qobj.QobjHeader(),
    config=qobj.QasmQobjConfig(shots=1024, memory_slots=2,
                               max_credits=10),
    experiments=[
        qobj.QasmQobjExperiment(instructions=[
            qobj.QasmQobjInstruction(name='u1', qubits=[1],
                                     params=[0.4]),
            qobj.QasmQobjInstruction(name='u2', qubits=[1],
                                     params=[0.4, 0.2])
        ])
    ]
)
qasm_dict = my_qasm.to_dict()
 
class QobjEncoder(json.JSONEncoder):
    """A json encoder for pulse qobj"""
    def default(self, obj):
        # Convert numpy arrays:
        if hasattr(obj, 'tolist'):
            return obj.tolist()
        # Use Qobj complex json format:
        if isinstance(obj, complex):
            return (obj.real, obj.imag)
        if isinstance(obj, ParameterExpression):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
 
json_str = json.dumps(qasm_dict, cls=QobjEncoder)
will generate a json string in the same exact manner that json.dumps(my_qasm.to_dict()) did in previous releases.

CmdDef has been deprecated since Terra 0.11.0 and has been removed. Please continue to use InstructionScheduleMap instead.

The methods cmds and cmd_qubits in InstructionScheduleMap have been deprecated since Terra 0.11.0 and have been removed. Please use instructions and qubits_with_instruction instead.

PulseDefaults have reported qubit_freq_est and meas_freq_est in Hz rather than GHz since Terra release 0.11.0. A warning which notified of this change has been removed.

The previously deprecated (in the 0.11.0 release) support for passsing in qiskit.circuit.Instruction parameters of types sympy.Basic, sympy.Expr, qiskit.qasm.node.node.Node (QASM AST node) and sympy.Matrix has been removed. The supported types for instruction parameters are:

int
float
complex
str
list
np.ndarray
qiskit.circuit.ParameterExpression
The following properties of BackendConfiguration:

dt
dtm
rep_time
all have units of seconds. Prior to release 0.11.0, dt and dtm had units of nanoseconds. Prior to release 0.12.0, rep_time had units of microseconds. The warnings alerting users of these changes have now been removed from BackendConfiguration.

A new requirement has been added to the requirements list, retworkx. It is an Apache 2.0 licensed graph library that has a similar API to networkx and is being used to significantly speed up the qiskit.dagcircuit.DAGCircuit operations as part of the transpiler. There are binaries published on PyPI for all the platforms supported by Qiskit Terra but if you’re using a platform where there aren’t precompiled binaries published refer to the retworkx documentation for instructions on pip installing from sdist.

If you encounter any issues with the transpiler or DAGCircuit class as part of the transition you can switch back to the previous networkx implementation by setting the environment variable USE_RETWORKX to N. This option will be removed in the 0.14.0 release.

Deprecation Notes
Passing in the data to the constructor for qiskit.dagcircuit.DAGNode as a dictionary arg data_dict is deprecated and will be removed in a future release. Instead you should now pass the fields in as kwargs to the constructor. For example the previous behavior of:


from qiskit.dagcircuit import DAGNode
 
data_dict = {
    'type': 'in',
    'name': 'q_0',
}
node = DAGNode(data_dict)
should now be:


from qiskit.dagcircuit import DAGNode
 
node = DAGNode(type='in', name='q_0')
The naming of gate objects and methods have been updated to be more consistent. The following changes have been made:

The Pauli gates all have one uppercase letter only (I, X, Y, Z)
The parameterized Pauli gates (i.e. rotations) prepend the uppercase letter R (RX, RY, RZ)
A controlled version prepends the uppercase letter C (CX, CRX, CCX)
Gates are named according to their action, not their alternative names (CCX, not Toffoli)
The old names have been deprecated and will be removed in a future release. This is a list of the changes showing the old and new class, name attribute, and methods. If a new column is blank then there is no change for that.

Old Class	New Class	Old Name Attribute	New Name Attribute	Old qiskit.circuit.QuantumCircuit method	New qiskit.circuit.QuantumCircuit method
ToffoliGate	CCXGate	ccx		ccx() and toffoli()	
CrxGate	CRXGate	crx		crx()	
CryGate	CRYGate	cry		cry()	
CrzGate	CRZGate	crz		crz()	
FredkinGate	CSwapGate	cswap		cswap() and fredkin()	
Cu1Gate	CU1Gate	cu1		cu1()	
Cu3Gate	CU3Gate	cu3		cu3()	
CnotGate	CXGate	cx		cx() and cnot()	
CyGate	CYGate	cy		cy()	
CzGate	CZGate	cz		cz()	
DiagGate	DiagonalGate	diag	diagonal	diag_gate	diagonal()
IdGate	IGate	id		iden	i() and id()
Isometry		iso	isometry	iso()	isometry() and iso()
UCG	UCGate	multiplexer		ucg	uc()
UCRot	UCPauliRotGate				
UCX	UCRXGate	ucrotX	ucrx	ucx	ucrx()
UCY	UCRYGate	ucroty	ucry	ucy	ucry()
UCZ	UCRZGate	ucrotz	ucrz	ucz	ucrz()
The kwarg period for the function square(), sawtooth(), and triangle() in qiskit.pulse.pulse_lib is now deprecated and will be removed in a future release. Instead you should now use the freq kwarg to set the frequency.

The DAGCircuit.compose_back() and DAGCircuit.extend_back() methods are deprecated and will be removed in a future release. Instead you should use the qiskit.dagcircuit.DAGCircuit.compose() method, which is a more general and more flexible method that provides the same functionality.

The callback kwarg of the qiskit.transpiler.PassManager class’s constructor has been deprecated and will be removed in a future release. Instead of setting it at the object level during creation it should now be set as a kwarg parameter on the qiskit.transpiler.PassManager.run() method.

The n_qubits and numberofqubits keywords are deprecated throughout Terra and replaced by num_qubits. The old names will be removed in a future release. The objects affected by this change are listed below:

Class	Old Method	New Method
QuantumCircuit	n_qubits	num_qubits()
Pauli	numberofqubits	num_qubits()
Function	Old Argument	New Argument
random_circuit()	n_qubits	num_qubits
MSGate	n_qubit	num_qubits
The function qiskit.quantum_info.synthesis.euler_angles_1q is now deprecated. It has been superseded by the qiskit.quantum_info.OneQubitEulerDecomposer class which provides the same functionality through:


OneQubitEulerDecomposer().angles(mat)
The pass_manager kwarg for the qiskit.compiler.transpile() has been deprecated and will be removed in a future release. Moving forward the preferred way to transpile a circuit with a custom PassManager object is to use the run() method of the PassManager object.

The qiskit.quantum_info.random_state() function has been deprecated and will be removed in a future release. Instead you should use the qiskit.quantum_info.random_statevector() function.

The add, subtract, and multiply methods of the qiskit.quantum_info.Statevector and qiskit.quantum_info.DensityMatrix classes are deprecated and will be removed in a future release. Instead you shoulde use +, -, * binary operators instead.

Deprecates qiskit.quantum_info.Statevector.to_counts(), qiskit.quantum_info.DensityMatrix.to_counts(), and qiskit.quantum_info.counts.state_to_counts(). These functions are superseded by the class methods qiskit.quantum_info.Statevector.probabilities_dict() and qiskit.quantum_info.DensityMatrix.probabilities_dict().

SamplePulse and ParametricPulse s (e.g. Gaussian) now subclass from Pulse and have been moved to the qiskit.pulse.pulse_lib. The previous path via pulse.commands is deprecated and will be removed in a future release.

DelayInstruction has been deprecated and replaced by Delay. This new instruction has been taken over the previous Command Delay. The migration pattern is:


Delay(<duration>)(<channel>) -> Delay(<duration>, <channel>)
DelayInstruction(Delay(<duration>), <channel>)
    -> Delay(<duration>, <channel>)
Until the deprecation period is over, the previous Delay syntax of calling a command on a channel will also be supported:


Delay(<phase>)(<channel>)
The new Delay instruction does not support a command attribute.

FrameChange and FrameChangeInstruction have been deprecated and replaced by ShiftPhase. The changes are:


FrameChange(<phase>)(<channel>) -> ShiftPhase(<phase>, <channel>)
FrameChangeInstruction(FrameChange(<phase>), <channel>)
    -> ShiftPhase(<phase>, <channel>)
Until the deprecation period is over, the previous FrameChange syntax of calling a command on a channel will be supported:


ShiftPhase(<phase>)(<channel>)
The call method of SamplePulse and ParametricPulse s have been deprecated. The migration is as follows:


Pulse(<*args>)(<channel>) -> Play(Pulse(*args), <channel>)
AcquireInstruction has been deprecated and replaced by Acquire. The changes are:


Acquire(<duration>)(<**channels>) -> Acquire(<duration>, <**channels>)
AcquireInstruction(Acquire(<duration>), <**channels>)
    -> Acquire(<duration>, <**channels>)
Until the deprecation period is over, the previous Acquire syntax of calling the command on a channel will be supported:


Acquire(<duration>)(<**channels>)
Bug Fixes
The BarrierBeforeFinalMeasurements transpiler pass, included in the preset transpiler levels when targeting a physical device, previously inserted a barrier across only measured qubits. In some cases, this allowed the transpiler to insert a swap after a measure operation, rendering the circuit invalid for current devices. The pass has been updated so that the inserted barrier will span all qubits on the device. Fixes #3937

When extending a QuantumCircuit instance (extendee) with another circuit (extension), the circuit is taken via reference. If a circuit is extended with itself that leads to an infinite loop as extendee and extension are the same. This bug has been resolved by copying the extension if it is the same object as the extendee. Fixes #3811

Fixes a case in qiskit.result.Result.get_counts(), where the results for an expirement could not be referenced if the experiment was initialized as a Schedule without a name. Fixes #2753

Previously, replacing Parameter objects in a circuit with new Parameter objects prior to decomposing a circuit would result in the substituted values not correctly being substituted into the decomposed gates. This has been resolved such that binding and decomposition may occur in any order.

The matplotlib output backend for the qiskit.visualization.circuit_drawer() function and qiskit.circuit.QuantumCircuit.draw() method drawer has been fixed to render CU1Gate gates correctly. Fixes #3684

A bug in qiskit.circuit.QuantumCircuit.from_qasm_str() and qiskit.circuit.QuantumCircuit.from_qasm_file() when loading QASM with custom gates defined has been fixed. Now, loading this QASM:


OPENQASM 2.0;
include "qelib1.inc";
gate rinv q {sdg q; h q; sdg q; h q; }
qreg q[1];
rinv q[0];
is equivalent to the following circuit:


rinv_q = QuantumRegister(1, name='q')
rinv_gate = QuantumCircuit(rinv_q, name='rinv')
rinv_gate.sdg(rinv_q)
rinv_gate.h(rinv_q)
rinv_gate.sdg(rinv_q)
rinv_gate.h(rinv_q)
rinv = rinv_gate.to_instruction()
qr = QuantumRegister(1, name='q')
expected = QuantumCircuit(qr, name='circuit')
expected.append(rinv, [qr[0]])
Fixes #1566

Allow quantum circuit Instructions to have list parameter values. This is used in Aer for expectation value snapshot parameters for example params = [[1.0, 'I'], [1.0, 'X']]] for 
⟨
I
+
X
⟩
⟨I+X⟩.

Previously, for circuits containing composite gates (those created via qiskit.circuit.QuantumCircuit.to_gate() or qiskit.circuit.QuantumCircuit.to_instruction() or their corresponding converters), attempting to bind the circuit more than once would result in only the first bind value being applied to all circuits when transpiled. This has been resolved so that the values provided for subsequent binds are correctly respected.

Other Notes
The qasm and pulse qobj classes:

QasmQobjInstruction
QobjExperimentHeader
QasmQobjExperimentConfig
QasmQobjExperiment
QasmQobjConfig
QobjHeader
PulseQobjInstruction
PulseQobjExperimentConfig
PulseQobjExperiment
PulseQobjConfig
QobjMeasurementOption
PulseLibraryItem
QasmQobjInstruction
QasmQobjExperimentConfig
QasmQobjExperiment
QasmQobjConfig
QasmQobj
PulseQobj
from qiskit.qobj have all been reimplemented without using the marsmallow library. These new implementations are designed to be drop-in replacement (except for as noted in the upgrade release notes) but specifics inherited from marshmallow may not work. Please file issues for any incompatibilities found.

Aer 0.5.0
Added
Add support for terra diagonal gate
Add support for parameterized qobj
Fixed
Added postfix for linux on Raspberry Pi
Handle numpy array inputs from qobj
Ignis 0.3.0
Added
API documentation
CNOT-Dihedral randomized benchmarking
Accreditation module for output accrediation of noisy devices
Pulse calibrations for single qubits
Pulse Discriminator
Entanglement verification circuits
Gateset tomography for single-qubit gate sets
Adds randomized benchmarking utility functions calculate_1q_epg, calculate_2q_epg functions to calculate 1 and 2-qubit error per gate from error per Clifford
Adds randomized benchmarking utility functions calculate_1q_epc, calculate_2q_epc for calculating 1 and 2-qubit error per Clifford from error per gate
Changed
Support integer labels for qubits in tomography
Support integer labels for measurement error mitigation
Deprecated
Deprecates twoQ_clifford_error function. Use calculate_2q_epc instead.
Python 3.5 support in qiskit-ignis is deprecated. Support will be removed on the upstream python community’s end of life date for the version, which is 09/13/2020.
Aqua 0.6.5
No Change

IBM Q Provider 0.6.0
No Change

