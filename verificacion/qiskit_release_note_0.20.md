Qiskit 0.20 release notes
0.20.1
Terra 0.15.2
Bug Fixes
When accessing the definition attribute of a parameterized Gate instance, the generated QuantumCircuit had been generated with an invalid ParameterTable, such that reading from QuantumCircuit.parameters or calling QuantumCircuit.bind_parameters would incorrectly report the unbound parameters. This has been resolved.
SXGate().inverse() had previously returned an ‘sx_dg’ gate with a correct definition but incorrect to_matrix. This has been updated such that SXGate().inverse() returns an SXdgGate() and vice versa.
Instruction.inverse(), when not overridden by a subclass, would in some cases return a Gate instance with an incorrect to_matrix method. The instances of incorrect to_matrix methods have been removed.
For C3XGate with a non-zero angle, inverting the gate via C3XGate.inverse() had previously generated an incorrect inverse gate. This has been corrected.
The MCXGate modes have been updated to return a gate of the same mode when calling .inverse(). This resolves an issue where in some cases, transpiling a circuit containing the inverse of an MCXVChain gate would raise an error.
Previously, when creating a multiply controlled phase gate via PhaseGate.control, an MCU1Gate gate had been returned. This has been had corrected so that an MCPhaseGate is returned.
Previously, attempting to decompose a circuit containing an MCPhaseGate would raise an error due to an inconsistency in the definition of the MCPhaseGate. This has been corrected.
QuantumCircuit.compose and DAGCircuit.compose had, in some cases, incorrectly translated conditional gates if the input circuit contained more than one ClassicalRegister. This has been resolved.
Fixed an issue when creating a qiskit.result.Counts object from an empty data dictionary. Now this will create an empty Counts object. The most_frequent() method is also updated to raise a more descriptive exception when the object is empty. Fixes #5017
Extending circuits with differing registers updated the qregs and cregs properties accordingly, but not the qubits and clbits lists. As these are no longer generated from the registers but are cached lists, this lead to a discrepancy of registers and bits. This has been fixed and the extend method explicitly updates the cached bit lists.
Fix bugs of the concrete implementations of meth:~qiskit.circuit.ControlledGate.inverse method which do not preserve the ctrl_state parameter.
A bug was fixed that caused long pulse schedules to throw a recursion error.
Aer 0.6.1
No change

Ignis 0.4.0
No change

Aqua 0.7.5
No change

IBM Q Provider 0.8.0
No change

0.20.0
Terra 0.15.1
Prelude
The 0.15.0 release includes several new features and bug fixes. Some highlights for this release are:

This release includes the introduction of arbitrary basis translation to the transpiler. This includes support for directly targeting a broader range of device basis sets, e.g. backends implementing RZ, RY, RZ, CZ or iSwap gates.

The QuantumCircuit class now tracks global phase. This means controlling a circuit which has global phase now correctly adds a relative phase, and gate matrix definitions are now exact rather than equal up to a global phase.

New Features
A new DAG class qiskit.dagcircuit.DAGDependency for representing the dependency form of circuit, In this DAG, the nodes are operations (gates, measure, barrier, etc…) and the edges corresponds to non-commutation between two operations.

Four new functions are added to qiskit.converters for converting back and forth to DAGDependency. These functions are:

circuit_to_dagdependency() to convert from a QuantumCircuit object to a DAGDependency object.
dagdependency_to_circuit() to convert from a DAGDependency object to a QuantumCircuit object.
dag_to_dagdependency() to convert from a DAGCircuit object to a DAGDependency object.
dagdependency_to_dag() to convert from a DAGDependency object to a DAGCircuit object.
For example:


from qiskit.converters.dagdependency_to_circuit import dagdependency_to_circuit
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
 
circuit_in = QuantumCircuit(2)
circuit_in.h(qr[0])
circuit_in.h(qr[1])
 
dag_dependency = circuit_to_dagdependency(circuit_in)
circuit_out = dagdepency_to_circuit(dag_dependency)
Two new transpiler passes have been added to qiskit.transpiler.passes The first, UnrollCustomDefinitions, unrolls all instructions in the circuit according to their definition property, stopping when reaching either the specified basis_gates or a set of gates in the provided EquivalenceLibrary. The second, BasisTranslator, uses the set of translations in the provided EquivalenceLibrary to re-write circuit instructions in a specified basis.

A new translation_method keyword argument has been added to transpile() to allow selection of the method to be used for translating circuits to the available device gates. For example, transpile(circ, backend, translation_method='translator'). Valid choices are:

'unroller': to use the Unroller pass
'translator': to use the BasisTranslator pass.
'synthesis': to use the UnitarySynthesis pass.
The default value is 'translator'.

A new class for handling counts result data, qiskit.result.Counts, has been added. This class is a subclass of dict and can be interacted with like any other dictionary. But, it includes helper methods and attributes for dealing with counts results from experiments and also handles post processing and formatting of binary strings at object initialization. A Counts object can be created by passing a dictionary of counts with the keys being either integers, hexadecimal strings of the form '0x4a', binary strings of the form '0b1101', a bit string formatted across register and memory slots (ie '00 10'), or a dit string. For example:


from qiskit.result import Counts
 
counts = Counts({"0x0': 1, '0x1', 3, '0x2': 1020})
A new method for constructing qiskit.dagcircuit.DAGCircuit objects has been added, from_networkx(). This method takes in a networkx MultiDiGraph object (in the format returned by to_networkx()) and will return a new DAGCircuit object. The intent behind this function is to enable transpiler pass authors to leverage networkx’s graph algorithm library if a function is missing from the retworkx API. Although, hopefully in such casses an issue will be opened with retworkx issue tracker (or even better a pull request submitted).

A new kwarg for init_qubits has been added to assemble() and execute(). For backends that support this feature init_qubits can be used to control whether the backend executing the circuits inserts any initialization sequences at the start of each shot. By default this is set to True meaning that all qubits can assumed to be in the ground state at the start of each shot. However, when init_qubits is set to False qubits will be uninitialized at the start of each experiment and between shots. Note, that the backend running the circuits has to support this feature for this flag to have any effect.

A new kwarg rep_delay has been added to qiskit.compiler.assemble(), qiskit.execute.execute(), and the constructor for PulseQobjtConfig.qiskit This new kwarg is used to denotes the time between program executions. It must be chosen from the list of valid values set as the rep_delays from a backend’s PulseBackendConfiguration object which can be accessed as backend.configuration().rep_delays).

The rep_delay kwarg will only work on backends which allow for dynamic repetition time. This will also be indicated in the PulseBackendConfiguration object for a backend as the dynamic_reprate_enabled attribute. If dynamic_reprate_enabled is False then the rep_time value specified for qiskit.compiler.assemble(), qiskit.execute.execute(), or the constructor for PulseQobjtConfig will be used rather than rep_delay. rep_time only allows users to specify the duration of a program, rather than the delay between programs.

The qobj_schema.json JSON Schema file in qiskit.schemas has been updated to include the rep_delay as an optional configuration property for pulse qobjs.

The backend_configuration_schema.json JSON Schema file in mod:qiskit.schemas has been updated to include rep_delay_range and default_rep_delay as optional properties for a pulse backend configuration.

A new attribute, global_phase, which is is used for tracking the global phase has been added to the qiskit.circuit.QuantumCircuit class. For example:


import math
 
from qiskit import QuantumCircuit
 
circ = QuantumCircuit(1, global_phase=math.pi)
circ.u1(0)
The global phase may also be changed or queried with circ.global_phase in the above example. In either case the setting is in radians. If the circuit is converted to an instruction or gate the global phase is represented by two single qubit rotations on the first qubit.

This allows for other methods and functions which consume a QuantumCircuit object to take global phase into account. For example. with the global_phase attribute the to_matrix() method for a gate can now exactly correspond to its decompositions instead of just up to a global phase.

The same attribute has also been added to the DAGCircuit class so that global phase can be tracked when converting between QuantumCircuit and DAGCircuit.

Two new classes, AncillaRegister and AncillaQubit have been added to the qiskit.circuit module. These are subclasses of QuantumRegister and Qubit respectively and enable marking qubits being ancillas. This will allow these qubits to be re-used in larger circuits and algorithms.

A new method, control(), has been added to the QuantumCircuit. This method will return a controlled version of the QuantumCircuit object, with both open and closed controls. This functionality had previously only been accessible via the Gate class.

A new method repeat() has been added to the QuantumCircuit class. It returns a new circuit object containing a specified number of repetitions of the original circuit. For example:


from qiskit.circuit import QuantumCircuit
 
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
repeated_qc = qc.repeat(3)
repeated_qc.decompose().draw(output='mpl')
The parameters are copied by reference, meaning that if you update the parameters in one instance of the circuit all repetitions will be updated.

A new method reverse_bits() has been added to the QuantumCircuit class. This method will reverse the order of bits in a circuit (both quantum and classical bits). This can be used to switch a circuit from little-endian to big-endian and vice-versa.

A new method, combine_into_edge_map(), was added to the qiskit.transpiler.Layout class. This method enables converting converting two Layout objects into a qubit map for composing two circuits.

A new class, ConfigurableFakeBackend, has been added to the qiskit.test.mock.utils module. This new class enables the creation of configurable mock backends for use in testing. For example:


from qiskit.test.mock.utils import ConfigurableFakeBackend
 
backend = ConfigurableFakeBackend("Tashkent",
                                  n_qubits=100,
                                  version="0.0.1",
                                  basis_gates=['u1'],
                                  qubit_t1=99.,
                                  qubit_t2=146.,
                                  qubit_frequency=5.,
                                  qubit_readout_error=0.01,
                                  single_qubit_gates=['u1'])
will create a backend object with 100 qubits and all the other parameters specified in the constructor.

A new method draw() has been added to the qiskit.circuit.EquivalenceLibrary class. This method can be used for drawing the contents of an equivalence library, which can be useful for debugging. For example:


from numpy import pi
 
from qiskit.circuit import EquivalenceLibrary
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.circuit import Parameter
from qiskit.circuit.library import HGate
from qiskit.circuit.library import U2Gate
from qiskit.circuit.library import U3Gate
 
my_equiv_library = EquivalenceLibrary()
 
q = QuantumRegister(1, 'q')
def_h = QuantumCircuit(q)
def_h.append(U2Gate(0, pi), [q[0]], [])
my_equiv_library.add_equivalence(HGate(), def_h)
 
theta = Parameter('theta')
phi = Parameter('phi')
lam = Parameter('lam')
def_u2 = QuantumCircuit(q)
def_u2.append(U3Gate(pi / 2, phi, lam), [q[0]], [])
my_equiv_library.add_equivalence(U2Gate(phi, lam), def_u2)
 
my_equiv_library.draw()
A new Phase instruction, SetPhase, has been added to qiskit.pulse. This instruction sets the phase of the subsequent pulses to the specified phase (in radians. For example:


import numpy as np
 
from qiskit.pulse import DriveChannel
from qiskit.pulse import Schedule
from qiskit.pulse import SetPhase
 
sched = Schedule()
sched += SetPhase(np.pi, DriveChannel(0))
In this example, the phase of the pulses applied to DriveChannel(0) after the SetPhase instruction will be set to 
π
π radians.

A new pulse instruction ShiftFrequency has been added to qiskit.pulse.instructions. This instruction enables shifting the frequency of a channel from its set frequency. For example:


from qiskit.pulse import DriveChannel
from qiskit.pulse import Schedule
from qiskit.pulse import ShiftFrequency
 
sched = Schedule()
sched += ShiftFrequency(-340e6, DriveChannel(0))
In this example all the pulses applied to DriveChannel(0) after the ShiftFrequency command will have the envelope a frequency decremented by 340MHz.

A new method conjugate() has been added to the ParameterExpression class. This enables calling numpy.conj() without raising an error. Since a ParameterExpression object is real, it will return itself. This behaviour is analogous to Python floats/ints.

A new class PhaseEstimation has been added to qiskit.circuit.library. This circuit library class is the circuit used in the original formulation of the phase estimation algorithm in arXiv:quant-ph/9511026. Phase estimation is the task to to estimate the phase 
ϕ
ϕ of an eigenvalue 
e
2
π
i
ϕ
e 
2πiϕ
  of a unitary operator 
U
U, provided with the corresponding eigenstate 
∣
p
s
i
⟩
∣psi⟩. That is

U
∣
ψ
⟩
=
e
2
π
i
ϕ
∣
ψ
⟩
U∣ψ⟩=e 
2πiϕ
 ∣ψ⟩
This estimation (and thereby this circuit) is a central routine to several well-known algorithms, such as Shor’s algorithm or Quantum Amplitude Estimation.

The qiskit.visualization function plot_state_qsphere() has a new kwarg show_state_labels which is used to control whether each blob in the qsphere visualization is labeled. By default this kwarg is set to True and shows the basis states next to each blob by default. This feature can be disabled, reverting to the previous behavior, by setting the show_state_labels kwarg to False.

The qiskit.visualization function plot_state_qsphere() has a new kwarg show_state_phases which is set to False by default. When set to True it displays the phase of each basis state.

The qiskit.visualization function plot_state_qsphere() has a new kwarg use_degrees which is set to False by default. When set to True it displays the phase of each basis state in degrees, along with the phase circle at the bottom right.

A new class, QuadraticForm to the qiskit.circuit.library module for implementing a a quadratic form on binary variables. The circuit library element implements the operation

∣
x
⟩
∣
0
⟩
↦
∣
x
⟩
∣
Q
(
x
)
m
o
d
 
 
2
m
⟩
∣x⟩∣0⟩↦∣x⟩∣Q(x)mod2 
m
 ⟩
for the quadratic form 
Q
Q and 
m
m output qubits. The result is in the 
m
m output qubits is encoded in two’s complement. If 
m
m is not specified, the circuit will choose the minimal number of qubits required to represent the result without applying a modulo operation. The quadratic form is specified using a matrix for the quadratic terms, a vector for the linear terms and a constant offset. If all terms are integers, the circuit implements the quadratic form exactly, otherwise it is only an approximation.

For example:


import numpy as np
 
from qiskit.circuit.library import QuadraticForm
 
A = np.array([[1, 2], [-1, 0]])
b = np.array([3, -3])
c = -2
m = 4
quad_form_circuit = QuadraticForm(m, A, b, c)
Add qiskit.quantum_info.Statevector.expectation_value() and qiskit.quantum_info.DensityMatrix.expectation_value() methods for computing the expectation value of an qiskit.quantum_info.Operator.

For the seed kwarg in the constructor for qiskit.circuit.library.QuantumVolume numpy random Generator objects can now be used. Previously, only integers were a valid input. This is useful when integrating QuantumVolume as part of a larger function with its own random number generation, e.g. generating a sequence of QuantumVolume circuits.

The QuantumCircuit method compose() has a new kwarg front which can be used for prepending the other circuit before the origin circuit instead of appending. For example:


from qiskit.circuit import QuantumCircuit
 
circ1 = QuantumCircuit(2)
circ2 = QuantumCircuit(2)
 
circ2.h(0)
circ1.cx(0, 1)
 
circ1.compose(circ2, front=True).draw(output='mpl')
Two new passes, SabreLayout and SabreSwap for layout and routing have been added to qiskit.transpiler.passes. These new passes are based on the algorithm presented in Li et al., “Tackling the Qubit Mapping Problem for NISQ-Era Quantum Devices”, ASPLOS 2019. They can also be selected when using the transpile() function by setting the layout_method kwarg to 'sabre' and/or the routing_method to 'sabre' to use SabreLayout and SabreSwap respectively.

Added the method replace() to the qiskit.pulse.Schedule class which allows a pulse instruction to be replaced with another. For example:


.. code-block:: python
from qiskit import pulse

d0 = pulse.DriveChannel(0)

sched = pulse.Schedule()

old = pulse.Play(pulse.Constant(100, 1.0), d0) new = pulse.Play(pulse.Constant(100, 0.1), d0)

sched += old

sched = sched.replace(old, new)

assert sched == pulse.Schedule(new)

Added new gate classes to qiskit.circuit.library for the 
X
X
​
 , its adjoint 
X
†
X
​
  
†
 , and controlled 
X
X
​
  gates as SXGate, SXdgGate, and CSXGate. They can also be added to a QuantumCircuit object using the sx(), sxdg(), and csx() respectively.

Add support for Reset instructions to qiskit.quantum_info.Statevector.from_instruction(). Note that this involves RNG sampling in choosing the projection to the zero state in the case where the qubit is in a superposition state. The seed for sampling can be set using the seed() method.

The methods qiskit.circuit.ParameterExpression.subs() and qiskit.circuit.QuantumCircuit.assign_parameters() now accept ParameterExpression as the target value to be substituted.

For example,


from qiskit.circuit import QuantumCircuit, Parameter
 
p = Parameter('p')
source = QuantumCircuit(1)
source.rz(p, 0)
 
x = Parameter('x')
source.assign_parameters({p: x*x})

     ┌──────────┐
q_0: ┤ Rz(x**2) ├
     └──────────┘
The QuantumCircuit() method to_gate() has a new kwarg label which can be used to set a label for for the output Gate object. For example:


from qiskit.circuit import QuantumCircuit
 
circuit_gate = QuantumCircuit(2)
circuit_gate.h(0)
circuit_gate.cx(0, 1)
custom_gate = circuit_gate.to_gate(label='My Special Bell')
new_circ = QuantumCircuit(2)
new_circ.append(custom_gate, [0, 1], [])
new_circ.draw(output='mpl')
Added the UGate, CUGate, PhaseGate, and CPhaseGate with the corresponding QuantumCircuit methods u(), cu(), p(), and cp(). The UGate gate is the generic single qubit rotation gate with 3 Euler angles and the CUGate gate its controlled version. CUGate has 4 parameters to account for a possible global phase of the U gate. The PhaseGate and CPhaseGate gates are the general Phase gate at an arbitrary angle and it’s controlled version.

A new kwarg, cregbundle has been added to the qiskit.visualization.circuit_drawer() function and the QuantumCircuit method draw(). When set to True the cregs will be bundled into a single line in circuit visualizations for the text and mpl drawers. The default value is True. Addresses issue #4290.

For example:


from qiskit import QuantumCircuit
circuit = QuantumCircuit(2)
circuit.measure_all()
circuit.draw(output='mpl', cregbundle=True)
A new kwarg, initial_state has been added to the qiskit.visualization.circuit_drawer() function and the QuantumCircuit method draw(). When set to True the initial state will now be included in circuit visualizations for all drawers. Addresses issue #4293.

For example:


from qiskit import QuantumCircuit
circuit = QuantumCircuit(2)
circuit.measure_all()
circuit.draw(output='mpl', initial_state=True)
Labels will now be displayed when using the ‘mpl’ drawer. There are 2 types of labels - gate labels and control labels. Gate labels will replace the gate name in the display. Control labels will display above or below the controls for a gate. Fixes issues #3766, #4580 Addresses issues #3766 and #4580.

For example:


from qiskit import QuantumCircuit
from qiskit.circuit.library.standard_gates import YGate
circuit = QuantumCircuit(2)
circuit.append(YGate(label='A Y Gate').control(label='Y Control'), [0, 1])
circuit.draw(output='mpl')
Upgrade Notes
Implementations of the multi-controlled X Gate ( MCXGrayCode, MCXRecursive, and MCXVChain) have had their name properties changed to more accurately describe their implementation: mcx_gray, mcx_recursive, and mcx_vchain respectively. Previously, these gates shared the name mcx with MCXGate, which caused these gates to be incorrectly transpiled and simulated.

By default the preset passmanagers in qiskit.transpiler.preset_passmanagers are using UnrollCustomDefinitions and BasisTranslator to handle basis changing instead of the previous default Unroller. This was done because the new passes are more flexible and allow targeting any basis set, however the output may differ. To use the previous default you can set the translation_method kwarg on transpile() to 'unroller'.

The qiskit.converters.circuit_to_gate() and :func`qiskit.converters.circuit_to_instruction` converter functions had previously automatically included the generated gate or instruction in the active SessionEquivalenceLibrary. These converters now accept an optional equivalence_library keyword argument to specify if and where the converted instances should be registered. The default behavior has changed to not register the converted instance.

The default value of the cregbundle kwarg for the qiskit.circuit.QuantumCircuit.draw() method and qiskit.visualization.circuit_drawer() function has been changed to True. This means that by default the classical bits in the circuit diagram will now be bundled by default, for example:


from qiskit.circuit import QuantumCircuit
 
circ = QuantumCircuit(4)
circ.x(0)
circ.h(1)
circ.measure_all()
circ.draw(output='mpl')
If you want to have your circuit drawing retain the previous behavior and show each classical bit in the diagram you can set the cregbundle kwarg to False. For example:


from qiskit.circuit import QuantumCircuit
 
circ = QuantumCircuit(4)
circ.x(0)
circ.h(1)
circ.measure_all()
circ.draw(output='mpl', cregbundle=False)
Schedule plotting with qiskit.pulse.Schedule.draw() and qiskit.visualization.pulse_drawer() will no longer display the event table by default. This can be reenabled by setting the table kwarg to True.

The pass RemoveResetInZeroState was previously included in the preset pass manager level_0_pass_manager() which was used with the optimization_level=0 for transpile() and execute() functions. However, RemoveResetInZeroState is an optimization pass and should not have been included in optimization level 0 and was removed. If you need to run transpile() with RemoveResetInZeroState either use a custom pass manager or optimization_level 1, 2, or 3.

The deprecated kwarg line_length for the qiskit.visualization.circuit_drawer() function and qiskit.circuit.QuantumCircuit.draw() method has been removed. It had been deprecated since the 0.10.0 release. Instead you can use the fold kwarg to adjust the width of the circuit diagram.

The 'mpl' output mode for the qiskit.circuit.QuantumCircuit.draw() method and circuit_drawer() now requires the pylatexenc library to be installed. This was already an optional dependency for visualization, but was only required for the 'latex' output mode before. It is now also required for the matplotlib drawer because it is needed to handle correctly sizing gates with matplotlib’s mathtext labels for gates.

The deprecated get_tokens methods for the qiskit.qasm.Qasm and qiskit.qasm.QasmParser has been removed. These methods have been deprecated since the 0.9.0 release. The qiskit.qasm.Qasm.generate_tokens() and qiskit.qasm.QasmParser.generate_tokens() methods should be used instead.

The deprecated kwarg channels_to_plot for qiskit.pulse.Schedule.draw(), qiskit.pulse.Instruction.draw(), qiskit.visualization.pulse.matplotlib.ScheduleDrawer.draw and pulse_drawer() has been removed. The kwarg has been deprecated since the 0.11.0 release and was replaced by the channels kwarg, which functions identically and should be used instead.

The deprecated circuit_instruction_map attribute of the qiskit.providers.models.PulseDefaults class has been removed. This attribute has been deprecated since the 0.12.0 release and was replaced by the instruction_schedule_map attribute which can be used instead.

The union method of Schedule and Instruction have been deprecated since the 0.12.0 release and have now been removed. Use qiskit.pulse.Schedule.insert() and qiskit.pulse.Instruction.meth() methods instead with the kwarg``time=0``.

The deprecated scaling argument to the draw method of Schedule and Instruction has been replaced with scale since the 0.12.0 release and now has been removed. Use the scale kwarg instead.

The deprecated period argument to qiskit.pulse.library functions have been replaced by freq since the 0.13.0 release and now removed. Use the freq kwarg instead of period.

The qiskit.pulse.commands module containing Commands classes was deprecated in the 0.13.0 release and has now been removed. You will have to upgrade your Pulse code if you were still using commands. For example:

Old	New
Command(args)(channel)	Instruction(args, channel)
```python	
Acquire(duration)(AcquireChannel(0))	
```	```python
Acquire(duration, AcquireChannel(0))	

| ```python
Delay(duration)(channel) 
```             | ```python
Delay(duration, channel) 
```                                          |
| ```python
FrameChange(angle)(DriveChannel(0)) 
```  | ```python
# FrameChange was also renamed ShiftPhase(angle, DriveChannel(0)) 
``` |
| ```python
Gaussian(...)(DriveChannel(0)) 
```       | ```python
# Pulses need to be `Play`d Play(Gaussian(...), DriveChannel(0)) 
```  |
All classes and function in the qiskit.tool.qi module were deprecated in the 0.12.0 release and have now been removed. Instead use the qiskit.quantum_info module and the new methods and classes that it has for working with quantum states and operators.

The qiskit.quantum_info.basis_state and qiskit.quantum_info.projector functions are deprecated as of Qiskit Terra 0.12.0 as are now removed. Use the qiskit.quantum_info.QuantumState and its derivatives qiskit.quantum_info.Statevector and qiskit.quantum_info.DensityMatrix to work with states.

The interactive plotting functions from qiskit.visualization, iplot_bloch_multivector, iplot_state_city, iplot_state_qsphere, iplot_state_hinton, iplot_histogram, iplot_state_paulivec now are just deprecated aliases for the matplotlib based equivalents and are no longer interactive. The hosted static JS code that these functions relied on has been removed and they no longer could work. A normal deprecation wasn’t possible because the site they depended on no longer exists.

The validation components using marshmallow from qiskit.validation have been removed from terra. Since they are no longer used to build any objects in terra.

The marshmallow schema classes in qiskit.result have been removed since they are no longer used by the qiskit.result.Result class.

The output of the to_dict() method for the qiskit.result.Result class is no longer in a format for direct JSON serialization. Depending on the content contained in instances of these classes there may be types that the default JSON encoder doesn’t know how to handle, for example complex numbers or numpy arrays. If you’re JSON serializing the output of the to_dict() method directly you should ensure that your JSON encoder can handle these types.

The option to acquire multiple qubits at once was deprecated in the 0.12.0 release and is now removed. Specifically, the init args mem_slots and reg_slots have been removed from qiskit.pulse.instructions.Acquire, and channel, mem_slot and reg_slot will raise an error if a list is provided as input.

Support for the use of the USE_RETWORKX environment variable which was introduced in the 0.13.0 release to provide an optional fallback to the legacy networkx based qiskit.dagcircuit.DAGCircuit implementation has been removed. This flag was only intended as provide a relief valve for any users that encountered a problem with the new implementation for one release during the transition to retworkx.

The module within qiskit.pulse responsible for schedule->schedule transformations has been renamed from reschedule.py to transforms.py. The previous import path has been deprecated. To upgrade your code:


from qiskit.pulse.rescheduler import <X>
should be replaced by:


from qiskit.pulse.transforms import <X>
In previous releases a PassManager did not allow TransformationPass classes to modify the PropertySet. This restriction has been lifted so a TransformationPass class now has read and write access to both the PropertySet and DAGCircuit during run(). This change was made to more efficiently facilitate TransformationPass classes that have an internal state which may be necessary for later passes in the PassManager. Without this change a second redundant AnalysisPass would have been necessary to recreate the internal state, which could add significant overhead.

Deprecation Notes
The name of the first positional parameter for the qiskit.visualization functions plot_state_hinton(), plot_bloch_multivector(), plot_state_city(), plot_state_paulivec(), and plot_state_qsphere() has been renamed from rho to state. Passing in the value by name to rho is deprecated and will be removed in a future release. Instead you should either pass the argument positionally or use the new parameter name state.

The qiskit.pulse.pulse_lib module has been deprecated and will be removed in a future release. It has been renamed to qiskit.pulse.library which should be used instead.

The qiskit.circuit.QuantumCircuit method mirror() has been deprecated and will be removed in a future release. The method qiskit.circuit.QuantumCircuit.reverse_ops() should be used instead, since mirroring could be confused with swapping the output qubits of the circuit. The reverse_ops() method only reverses the order of gates that are applied instead of mirroring.

The qubits() and clbits() methods of qiskit.dagcircuit.DAGCircuit have been deprecated and will be removed in a future release. They have been replaced with properties of the same name, qiskit.dagcircuit.DAGCircuit.qubits and qiskit.dagcircuit.DAGCircuit.clbits, and are cached so accessing them is much faster.

The get_sample_pulse method for qiskit.pulse.library.ParametricPulse derived classes (for example GaussianSquare) has been deprecated and will be removed in a future release. It has been replaced by the get_waveform method (for example get_waveform()) which should behave identically.

The use of the optional condition argument on qiskit.dagcircuit.DAGNode, qiskit.dagcircuit.DAGCircuit.apply_operation_back(), and qiskit.dagcircuit.DAGCircuit.apply_operation_front() has been deprecated and will be removed in a future release. Instead the control set in qiskit.circuit.Instruction instances being added to a DAGCircuit should be used.

The set_atol and set_rtol class methods of the qiskit.quantum_info.BaseOperator and qiskit.quantum_info.QuantumState classes (and their subclasses such as Operator and qiskit.quantum_info.DensityMatrix) are deprecated and will be removed in a future release. Instead the value for the attributes .atol and .rtol should be set on the class instead. For example:


from qiskit.quantum_info import ScalarOp
 
ScalarOp.atol = 3e-5
op = ScalarOp(2)
The interactive plotting functions from qiskit.visualization, iplot_bloch_multivector, iplot_state_city, iplot_state_qsphere, iplot_state_hinton, iplot_histogram, iplot_state_paulivec have been deprecated and will be removed in a future release. The matplotlib based equivalent functions from qiskit.visualization, plot_bloch_multivector(), plot_state_city(), plot_state_qsphere(), plot_state_hinton(), plot_state_histogram(), and plot_state_paulivec() should be used instead.

The properties acquires, mem_slots, and reg_slots of the qiskit.pulse.instructions.Acquire pulse instruction have been deprecated and will be removed in a future release. They are just duplicates of channel, mem_slot, and reg_slot respectively now that previously deprecated support for using multiple qubits in a single Acquire instruction has been removed.

The SamplePulse class from qiskit.pulse has been renamed to Waveform. SamplePulse is deprecated and will be removed in a future release.

The style dictionary key cregbundle has been deprecated and will be removed in a future release. This has been replaced by the kwarg cregbundle added to the qiskit.visualization.circuit_drawer() function and the QuantumCircuit method draw().

Bug Fixes
The qiskit.circuit.QuantumCircuit method num_nonlocal_gates previously included multi-qubit qiskit.circuit.Instruction objects (for example, Barrier) in its count of non-local gates. This has been corrected so that only non-local Gate objects are counted. Fixes #4500

ControlledGate instances with a set ctrl_state were in some cases not being evaluated as equal, even if the compared gates were equivalent. This has been resolved so that Fixes #4573

When accessing a bit from a qiskit.circuit.QuantumRegister or qiskit.circuit.ClassicalRegister by index when using numpy integer types <https://numpy.org/doc/stable/user/basics.types.html>`__ would previously raise a CircuitError exception. This has been resolved so numpy types can be used in addition to Python’s built-in int type. Fixes #3929.

A bug was fixed where only the first qiskit.pulse.configuration.Kernel or qiskit.pulse.configuration.Discriminator for an qiskit.pulse.Acquire was used when there were multiple Acquires at the same time in a qiskit.pulse.Schedule.

The SI unit use for constructing qiskit.pulse.SetFrequency objects is in Hz, but when a PulseQobjInstruction object is created from a SetFrequency instance it needs to be converted to GHz. This conversion was missing from previous releases and has been fixed.

Previously it was possible to set the number of control qubits to zero in which case the the original, potentially non-controlled, operation would be returned. This could cause an AttributeError to be raised if the caller attempted to access an attribute which only ControlledGate object have. This has been fixed by adding a getter and setter for num_ctrl_qubits to validate that a valid value is being used. Fixes #4576

Open controls were implemented by modifying a Gate objects definition. However, when the gate already exists in the basis set, this definition was not used, which resulted in incorrect circuits being sent to a backend after transpilation. This has been fixed by modifying the Unroller pass to use the definition if it encounters a controlled gate with open controls. Fixes #4437

The insert_barriers keyword argument in the ZZFeatureMap class didn’t actually insert barriers in between the Hadamard layers and evolution layers. This has been fixed so that barriers are now properly inserted.

Fixed issue where some gates with three or more qubits would fail to compile in certain instances. Refer to #4577 <https://github.com/Qiskit/qiskit/issues/4577 for more detail.

The matplotlib ('mpl') output backend for the qiskit.circuit.QuantumCircuit method draw() and the qiskit.visualization.circuit_drawer() function was not properly scaling when the kwarg scale was set. Fonts and line widths did not scale with the rest of the image. This has been fixed and all elements of the circuit diagram now scale properly. For example:


from qiskit import QuantumCircuit
circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)
circuit.draw(output='mpl', scale=0.5)
Fixes #4179.

Fixes issue where initializing or evolving qiskit.quantum_info.Statevector and qiskit.quantum_info.DensityMatrix classes by circuits by circuit containing Barrier instructions would raise an exception. Fixes #4461

Previously when a QuantumCircuit contained a Gate with a classical condition the transpiler would sometimes fail when using optimization_level=3 on transpile() or execute() raising an UnboundLocalError. This has been fixed by updating the ConsolidateBlocks pass to account for the classical condition. Fixes #4672.

In some situations long gate and register names would overflow, or leave excessive empty space around them when using the 'mpl' output backend for the qiskit.circuit.QuantumCircuit.draw() method and qiskit.visualization.circuit_drawer() function. This has been fixed by using correct text widths for a proportional font. Fixes #4611, #4605, #4545, #4497, #4449, and #3641.

When using the style` kwarg on the :meth:`qiskit.circuit.QuantumCircuit.draw` or :func:`qiskit.visualization.circuit_drawer` with the ``'mpl' output backend the dictionary key 'showindex' set to True, the index numbers at the top of the column did not line up properly. This has been fixed.

When using cregbunde=True with the 'mpl' output backend for the qiskit.circuit.QuantumCircuit.draw() method and qiskit.visualization.circuit_drawer() function and measuring onto a second fold, the measure arrow would overwrite the creg count. The count was moved to the left to prevent this. Fixes #4148.

When using the 'mpl' output backend for the qiskit.circuit.QuantumCircuit.draw() method and qiskit.visualization.circuit_drawer() function CSwapGate gates and a controlled RZZGate gates now display with their appropriate symbols instead of in a box.

When using the 'mpl' output backend for the qiskit.circuit.QuantumCircuit.draw() method and qiskit.visualization.circuit_drawer() function controlled gates created using the to_gate() method were not properly spaced and could overlap with other gates in the circuit diagram. This issue has been fixed.

When using the 'mpl' output backend for the qiskit.circuit.QuantumCircuit.draw() method and qiskit.visualization.circuit_drawer() function gates with arrays as parameters, such as HamiltonianGate, no longer display with excessive space around them. Fixes #4352.

When using the 'mpl' output backend for the qiskit.circuit.QuantumCircuit.draw() method and qiskit.visualization.circuit_drawer() function generic gates created by directly instantiating qiskit.circuit.Gate method now display the proper background color for the gate. Fixes #4496.

When using the 'mpl' output backend for the qiskit.circuit.QuantumCircuit.draw() method and qiskit.visualization.circuit_drawer() function an AttributeError that occurred when using Isometry or Initialize has been fixed. Fixes #4439.

When using the 'mpl' output backend for the qiskit.circuit.QuantumCircuit.draw() method and qiskit.visualization.circuit_drawer() function some open-controlled gates did not properly display the open controls. This has been corrected so that open controls are properly displayed as open circles. Fixes #4248.

When using the 'mpl' output backend for the qiskit.circuit.QuantumCircuit.draw() method and qiskit.visualization.circuit_drawer() function setting the fold kwarg to -1 will now properly display the circuit without folding. Fixes #4506.

Parametric pulses from qiskit.pulse.library.discrete now have zero ends of parametric pulses by default. The endpoints are defined such that for a function 
f
(
x
)
f(x) then 
f
(
−
1
)
=
f
(
d
u
r
a
t
i
o
n
+
1
)
=
0
f(−1)=f(duration+1)=0. Fixes #4317

Other Notes
The qiskit.result.Result class which was previously constructed using the marshmallow library has been refactored to not depend on marshmallow anymore. This new implementation should be a seamless transition but some specific behavior that was previously inherited from marshmallow may not work. Please file issues for any incompatibilities found.
Aer 0.6.1
Prelude
This 0.6.0 release includes numerous performance improvements for all simulators in the Aer provider and significant changes to the build system when building from source. The main changes are support for SIMD vectorization, approximation in the matrix product state method via bond-dimension truncation, more efficient Pauli expectation value computation, and greatly improved efficiency in Python conversion of C++ result objects. The build system was upgraded to use the Conan to manage common C++ dependencies when building from source.

New Features
Add density matrix snapshot support to “statevector” and “statevector_gpu” methods of the QasmSimulator.

Allow density matrix snapshots on specific qubits, not just all qubits. This computes the partial trace of the state over the remaining qubits.

Adds Pauli expectation value snapshot support to the “density_matrix” simulation method of the qiskit.providers.aer.QasmSimulator. Add snapshots to circuits using the qiskit.providers.aer.extensions.SnapshotExpectationValue extension.

Greatly improves performance of the Pauli expectation value snapshot algorithm for the “statevector”, “statevector_gpu, “density_matrix”, and “density_matrix_gpu” simulation methods of the qiskit.providers.aer.QasmSimulator.

Enable the gate-fusion circuit optimization from the qiskit.providers.aer.QasmSimulator in both the qiskit.providers.aer.StatevectorSimulator and qiskit.providers.aer.UnitarySimulator backends.

Improve the performance of average snapshot data in simulator results. This effects probability, Pauli expectation value, and density matrix snapshots using the following extensions:

qiskit.providers.aer.extensions.SnapshotExpectationValue
qiskit.providers.aer.extensions.SnapshotProbabilities
qiskit.providers.aer.extensions.SnapshotDensityMatrix
Add move constructor and improve memory usage of the C++ matrix class to minimize copies of matrices when moving output of simulators into results.

Improve performance of unitary simulator.

Add approximation to the “matrix_product_state” simulation method of the QasmSimulator to limit the bond-dimension of the MPS.

There are two modes of approximation. Both discard the smallest Schmidt coefficients following the SVD algorithm. There are two parameters that control the degree of approximation: "matrix_product_state_max_bond_dimension" (int): Sets a limit on the number of Schmidt coefficients retained at the end of the svd algorithm. Coefficients beyond this limit will be discarded. (Default: None, i.e., no limit on the bond dimension). "matrix_product_state_truncation_threshold" (double): Discard the smallest coefficients for which the sum of their squares is smaller than this threshold. (Default: 1e-16).

Improve the performance of measure sampling when using the “matrix_product_state” QasmSimulator simulation method.

Add support for Delay, Phase and SetPhase pulse instructions to the qiskit.providers.aer.PulseSimulator.

Improve the performance of the qiskit.providers.aer.PulseSimulator by caching calls to RHS function

Introduce alternate DE solving methods, specifiable through backend_options in the qiskit.providers.aer.PulseSimulator.

Improve performance of simulator result classes by using move semantics and removing unnecessary copies that were happening when combining results from separate experiments into the final result object.

Greatly improve performance of pybind11 conversion of simulator results by using move semantics where possible, and by moving vector and matrix results to Numpy arrays without copies.

Change the RNG engine for simulators from 32-bit Mersenne twister to 64-bit Mersenne twister engine.

Improves the performance of the “statevector” simulation method of the qiskit.providers.aer.QasmSimulator and qiskit.providers.aer.StatevectorSimulator by using SIMD intrinsics on systems that support the AVX2 instruction set. AVX2 support is automatically detected and enabled at runtime.

Upgrade Notes
Changes the build system to use the Conan package manager. This tool will handle most of the dependencies needed by the C++ source code. Internet connection may be needed for the first build or when dependencies are added or updated, in order to download the required packages if they are not in your Conan local repository.

When building the standalone version of qiskit-aer you must install conan first with:


pip install conan
Changes how transpilation passes are handled in the C++ Controller classes so that each pass must be explicitly called. This allows for greater customization on when each pass should be called, and with what parameters. In particular this enables setting different parameters for the gate fusion optimization pass depending on the QasmController simulation method.

Add gate_length_units kwarg to qiskit.providers.aer.noise.NoiseModel.from_device() for specifying custom gate_lengths in the device noise model function to handle unit conversions for internal code.

Add Controlled-Y (“cy”) gate to the Stabilizer simulator methods supported gateset.

For Aer’s backend the jsonschema validation of input qobj objects from terra is now opt-in instead of being enabled by default. If you want to enable jsonschema validation of qobj set the validate kwarg on the qiskit.providers.aer.QasmSimualtor.run() method for the backend object to True.

Adds an OpSet object to the base simulator State class to allow easier validation of instructions, gates, and snapshots supported by simulators.

Refactor OpSet class. Moved OpSet to separate header file and add contains and difference methods based on std::set::contains and std::algorithm::set_difference. These replace the removed invalid and validate instructions from OpSet, but with the order reversed. It returns a list of other ops not in current opset rather than opset instructions not in the other.

Improves how measurement sampling optimization is checked. The expensive part of this operation is now done once during circuit construction where rather than multiple times during simulation for when checking memory requirements, simulation method, and final execution.

Bug Fixes
Remove “extended_stabilizer” from the automatically selected simulation methods. This is needed as the extended stabilizer method is not exact and may give incorrect results for certain circuits unless the user knows how to optimize its configuration parameters.

The automatic method now only selects from “stabilizer”, “density_matrix”, and “statevector” methods. If a non-Clifford circuit that is too large for the statevector method is executed an exception will be raised suggesting you could try explicitly using the “extended_stabilizer” or “matrix_product_state” methods instead.

Disables gate fusion for the matrix product state simulation method as this was causing issues with incorrect results being returned in some cases.

Fixes a bug causing incorrect channel evaluation in the qiskit.providers.aer.PulseSimulator.

Fixes several minor bugs for Hamiltonian parsing edge cases in the qiskit.providers.aer.pulse.system_models.hamiltonian_model.HamiltonianModel class.

Ignis 0.4.0
Prelude
The main change made in this release is a refactor of the Randomized Benchmarking code to integrate the updated Clifford class qiskit.quantum_info.Clifford from Terra and to improve the CNOT-Dihedral class.

New Features
The qiskit.ignis.verification.randomized_benchmarking.randomized_benchmarking_seq() function was refactored to use the updated Clifford class Clifford, to allow efficient Randomized Benchmarking (RB) on Clifford sequences with more than 2 qubits. In addition, the code of the CNOT-Dihedral class qiskit.ignis.verification.randomized_benchmarking.CNOTDihedral was refactored to make it more efficient, by using numpy arrays, as well not using pre-generated pickle files storing all the 2-qubit group elements. The qiskit.ignis.verification.randomized_benchmarking.randomized_benchmarking_seq() function has a new kwarg rand_seed which can be used to specify a seed for the random number generator used to generate the RB circuits. This can be useful for having a reproducible circuit.
The qiskit.ignis.verification.qv_circuits() function has a new kwarg seed which can be used to specify a seed for the random number generator used to generate the Quantum Volume circuits. This can be useful for having a reproducible circuit.
Upgrade Notes
The qiskit.ignis.verification.randomized_benchmarking.randomized_benchmarking_seq() function is now using the updated Clifford class Clifford and the updated CNOT-Dihedral class qiskit.ignis.verification.randomized_benchmarking.CNOTDihedral to construct its output instead of using pre-generated group tables for the Clifford and CNOT-Dihedral group elements, which were stored in pickle files. This may result in subtle differences from the output from the previous version.
A new requirement scikit-learn has been added to the requirements list. This dependency was added in the 0.3.0 release but wasn’t properly exposed as a dependency in that release. This would lead to an ImportError if the qiskit.ignis.measurement.discriminator.iq_discriminators module was imported. This is now correctly listed as a dependency so that scikit-learn will be installed with qiskit-ignis.
The qiskit.ignis.verification.qv_circuits() function is now using the circuit library class QuantumVolume to construct its output instead of building the circuit from scratch. This may result in subtle differences from the output from the previous version.
Tomography fitters can now also get list of Result objects instead of a single Result as requested in issue #320.
Deprecation Notes
The kwarg interleaved_gates for the qiskit.ignis.verification.randomized_benchmarking.randomized_benchmarking_seq() function has been deprecated and will be removed in a future release. It is superseded by interleaved_elem. The helper functions qiskit.ignis.verification.randomized_benchmarking.BasicUtils, qiskit.ignis.verification.randomized_benchmarking.CliffordUtils and qiskit.ignis.verification.randomized_benchmarking.DihedralUtils were deprecated. These classes are superseded by qiskit.ignis.verification.randomized_benchmarking.RBgroup that handles the group operations needed for RB. The class qiskit.ignis.verification.randomized_benchmarking.Clifford is superseded by Clifford.

The kwargs qr and cr for the qiskit.ignis.verification.qv_circuits() function have been deprecated and will be removed in a future release. These kwargs were documented as being used for specifying a qiskit.circuit.QuantumRegister and qiskit.circuit.ClassicalRegister to use in the generated Quantum Volume circuits instead of creating new ones. However, the parameters were never actually respected and a new Register would always be created regardless of whether they were set or not. This behavior is unchanged and these kwargs still do not have any effect, but are being deprecated prior to removal to avoid a breaking change for users who may have been setting either.

Support for passing in subsets of qubits as a list in the qubit_lists parameter for the qiskit.ignis.verification.qv_circuits() function has been deprecated and will removed in a future release. In the past this was used to specify a layout to run the circuit on a device. In other words if you had a 5 qubit device and wanted to run a 2 qubit QV circuit on qubits 1, 3, and 4 of that device. You would pass in [1, 3, 4] as one of the lists in qubit_lists, which would generate a 5 qubit virtual circuit and have qv applied to qubits 1, 3, and 4 in that virtual circuit. However, this functionality is not necessary and overlaps with the concept of initial_layout in the transpiler and whether a circuit has been embedded with a layout set. Moving forward instead you should just run transpile() or execute() with initial layout set to do this. For example, running the above example would become:


from qiskit import execute
from qiskit.ignis.verification import qv_circuits
 
initial_layout = [1, 3, 4]
qv_circs, _ = qv_circuits([list(range3)])
execute(qv_circuits, initial_layout=initial_layout)
Bug Fixes
Fix a bug of the position of measurement pulses inserted by py:func:qiskit.ignis.characterization.calibrations.pulse_schedules.drag_schedules. Fixes #465
Aqua 0.7.5
New Features
Removed soft dependency on CPLEX in ADMMOptimizer. Now default optimizers used by ADMMOptimizer are MinimumEigenOptimizer for QUBO problems and SlsqpOptimizer as a continuous optimizer. You can still use CplexOptimizer as an optimizer for ADMMOptimizer, but it should be set explicitly.
New Yahoo! finance provider created.
Introduced QuadraticProgramConverter which is an abstract class for converters. Added convert/interpret methods for converters instead of encode/decode. Added to_ising and from_ising to QuadraticProgram class. Moved all parameters from convert to constructor except name. Created setter/getter for converter parameters. Added auto_define_penalty and interpret for``LinearEqualityToPenalty``. Now error messages of converters are more informative.
Added an SLSQP optimizer qiskit.optimization.algorithms.SlsqpOptimizer as a wrapper of the corresponding SciPy optimization method. This is a classical optimizer, does not depend on quantum algorithms and may be used as a replacement for CobylaOptimizer.
Cobyla optimizer has been modified to accommodate a multi start feature introduced in the SLSQP optimizer. By default, the optimizer does not run in the multi start mode.
The SummedOp does a mathematically more correct check for equality, where expressions such as X + X == 2*X and X + Z == Z + X evaluate to True.
Deprecation Notes
GSLS optimizer class deprecated __init__ parameter max_iter in favor of maxiter. SPSA optimizer class deprecated __init__ parameter max_trials in favor of maxiter. optimize_svm function deprecated max_iters parameter in favor of maxiter. ADMMParameters class deprecated __init__ parameter max_iter in favor of maxiter.
The ising convert classes qiskit.optimization.converters.QuadraticProgramToIsing and qiskit.optimization.converters.IsingToQuadraticProgram have been deprecated and will be removed in a future release. Instead the qiskit.optimization.QuadraticProgram methods to_ising() and from_ising() should be used instead.
The pprint_as_string method for qiskit.optimization.QuadraticProgram has been deprecated and will be removed in a future release. Instead you should just run .pprint_as_string() on the output from to_docplex()
The prettyprint method for qiskit.optimization.QuadraticProgram has been deprecated and will be removed in a future release. Instead you should just run .prettyprint() on the output from to_docplex()
Bug Fixes
Changed in python version 3.8: On macOS, the spawn start method is now the default. The fork start method should be considered unsafe as it can lead to crashes in subprocesses. However P_BFGS doesn’t support spawn, so we revert to single process. Refer to #1109 <https://github.com/qiskit-community/qiskit-aqua/issues/1109> for more details.
Binding parameters in the CircuitStateFn did not copy the value of is_measurement and always set is_measurement=False. This has been fixed.
Previously, SummedOp.to_matrix_op built a list MatrixOp’s (with numpy matrices) and then summed them, returning a single MatrixOp. Some algorithms (for example vqe) require summing thousands of matrices, which exhausts memory when building the list of matrices. With this change, no list is constructed. Rather, each operand in the sum is converted to a matrix, added to an accumulator, and discarded.
Changing backends in VQE from statevector to qasm_simulator or real device was causing an error due to CircuitSampler incompatible reuse. VQE was changed to always create a new CircuitSampler and create a new expectation in case not entered by user. Refer to #1153 <https://github.com/qiskit-community/qiskit-aqua/issues/1153> for more details.
Exchange and Wikipedia finance providers were fixed to correctly handle Quandl data. Refer to #775 <https://github.com/qiskit-community/qiskit-aqua/issues/775> for more details. Fixes a divide by 0 error on finance providers mean vector and covariance matrix calculations. Refer to #781 <https://github.com/qiskit-community/qiskit-aqua/issues/781> for more details.
The ListOp.combo_fn property has been lost in several transformations, such as converting to another operator type, traversing, reducing or multiplication. Now this attribute is propagated to the resulting operator.
The evaluation of some operator expressions, such as of SummedOp``s and evaluations with the ``CircuitSampler did not treat coefficients correctly or ignored them completely. E.g. evaluating ~StateFn(0 * (I + Z)) @ Plus did not yield 0 or the normalization of ~StateFn(I) @ ((Plus + Minus) / sqrt(2)) missed a factor of sqrt(2). This has been fixed.
OptimizationResult included some public setters and class variables were Optional. This fix makes all class variables read-only so that mypy and pylint can check types more effectively. MinimumEigenOptimizer.solve generated bitstrings in a result as str. This fix changed the result into List[float] as the other algorithms do. Some public classes related to optimization algorithms were missing in the documentation of qiskit.optimization.algorithms. This fix added all such classes to the docstring. #1131 <https://github.com/qiskit-community/qiskit-aqua/issues/1131> for more details.
OptimizationResult.__init__ did not check whether the sizes of x and variables match or not (they should match). This fix added the check to raise an error if they do not match and fixes bugs detected by the check. This fix also adds missing unit tests related to OptimizationResult.variable_names and OptimizationResult.variables_dict in test_converters. #1167 <https://github.com/qiskit-community/qiskit-aqua/issues/1167> for more details.
Fix parameter binding in the OperatorStateFn, which did not bind parameters of the underlying primitive but just the coefficients.
op.eval(other), where op is of type OperatorBase, sometimes silently returns a nonsensical value when the number of qubits in op and other are not equal. This fix results in correct behavior, which is to throw an error rather than return a value, because the input in this case is invalid.
The construct_circuit method of VQE previously returned the expectation value to be evaluated as type OperatorBase. This functionality has been moved into construct_expectation and construct_circuit returns a list of the circuits that are evaluated to compute the expectation value.
IBM Q Provider 0.8.0
New Features
IBMQBackend now has a new reservations() method that returns reservation information for the backend, with optional filtering. In addition, you can now use provider.backends.my_reservations() to query for your own reservations.
qiskit.providers.ibmq.job.IBMQJob.result() raises an IBMQJobFailureError exception if the job has failed. The exception message now contains the reason the job failed, if the entire job failed for a single reason.
A new attribute client_version was added to IBMQJob and qiskit.result.Result object retrieved via qiskit.providers.ibmq.job.IBMQJob.result(). client_version is a dictionary with the key being the name and the value being the version of the client used to submit the job, such as Qiskit.
The least_busy() function now takes a new, optional parameter reservation_lookahead. If specified or defaulted to, a backend is considered unavailable if it has reservations in the next n minutes, where n is the value of reservation_lookahead. For example, if the default value of 60 is used, then any backends that have reservations in the next 60 minutes are considered unavailable.
ManagedResults now has a new combine_results() method that combines results from all managed jobs and returns a single Result object. This Result object can be used, for example, in qiskit-ignis fitter methods.
Upgrade Notes
Timestamps in the following fields are now in local time instead of UTC:

Backend properties returned by qiskit.providers.ibmq.IBMQBackend.properties().
Backend properties returned by qiskit.providers.ibmq.job.IBMQJob.properties().
estimated_start_time and estimated_complete_time in QueueInfo, returned by qiskit.providers.ibmq.job.IBMQJob.queue_info().
date in Result, returned by qiskit.providers.ibmq.job.IBMQJob.result().
In addition, the datetime parameter for qiskit.providers.ibmq.IBMQBackend.properties() is also expected to be in local time unless it has UTC timezone information.

websockets 8.0 or above is now required if Python 3.7 or above is used. websockets 7.0 will continue to be used for Python 3.6 or below.

On Windows, the event loop policy is set to WindowsSelectorEventLoopPolicy instead of using the default WindowsProactorEventLoopPolicy. This fixes the issue that the qiskit.providers.ibmq.job.IBMQJob.result() method could hang on Windows. Fixes #691

Deprecation Notes
Use of Qconfig.py to save IBM Quantum Experience credentials is deprecated and will be removed in the next release. You should use qiskitrc (the default) instead.
Bug Fixes
Fixes an issue wherein a call to qiskit.providers.ibmq.IBMQBackend.jobs() can hang if the number of jobs being returned is large. Fixes #674
Fixes an issue which would raise a ValueError when building error maps in Jupyter for backends that are offline. Fixes #706
qiskit.providers.ibmq.IBMQBackend.jobs() will now return the correct list of IBMQJob objects when the status kwarg is set to 'RUNNING'.
The package metadata has been updated to properly reflect the dependency on qiskit-terra >= 0.14.0. This dependency was implicitly added as part of the 0.7.0 release but was not reflected in the package requirements so it was previously possible to install qiskit-ibmq-provider with a version of qiskit-terra which was too old. Fixes #677