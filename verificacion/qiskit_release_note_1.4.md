Qiskit SDK 1.4 release notes
1.4.2
Prelude
Qiskit 1.4.2 is a patch release that fixes bugs found in the 1.4 release series.

New Features
Added a new flag trust_payload, to the qpy.load() function. This is used to force the function to load a payload that is potentially insecure. If the payload contains ScheduleBlock objects (either standalone or as part of QuantumCircuit.calibrations) and the symbolic encoding in the QPY file is set to sympy then the payload is potentially insecure and loading it could allow for arbitrary code execution. Since this flag is for controlling the deserialization of ScheduleBlock instances which do not exist in Qiskit >= 2.0.0 this flag will only exist in Qiskit 1.4.x and will not exist in Qiskit >=2.0.0.
Upgrade Notes
By default, qpy.load will now raise a QpyError when called with a QPY payload that contains a ScheduleBlock object (either standalone or as part of QuantumCircuit.calibrations) which is using sympy for encoding symbolic expressions. This is because the payload is potentially vulnerable and should only be loaded if you trust the contents. If you are certain that the payload is not malicious, you can set the new trust_payload argument of qpy.load to True, and this will enable loading the payload.
Security Issues
Fixed a security vulnerability in qpy.load() when loading payloads that use sympy to serialize ParameterExpression objects and other symbolic expressions. This potentially includes any QPY payload using QPY version < 10, and optionally 10, 11, and 12 depending on the symbolic encoding used in the serialization step (qpy.dump()).
Bug Fixes
Fixed a bug in the basis approximation generation for SolovayKitaev. Previously, generating discrete basis approximations using generate_basis_approximations for a basis containing "sx" or "sxdg" gates would fail. This has now been fixed.
1.4.1
Prelude
Qiskit 1.4.1 is a small patch release, fixing some bugs found in the 1.4 extended support series.

Bug Fixes
Circuits compiled using a preset passmanager constructed by generate_preset_pass_manager() will now correctly retain their name attribute, as they do with transpile().

Fixed an issue with QPY 13 when serializing or deserializing a ParameterExpression object that was defined by calling ParameterExpression.subs() to substitute a Parameter with a ParameterExpression. For example:


from qiskit.circuit import Parameter
 
a = Parameter("A")
b = Parameter("B")
expr = a + b
c = Parameter("C")
new_expr = c ** 3.14
final_expr.subs({b: new_expr})
In previous releases if you went to serialize a QuantumCircuit that contained an expression like this with qpy.dump() it would have raised an AttributeError with an error message ‘ParameterExpression’ object has no attribute ‘name’ when using QPY 13 (the default). This has been fixed so that the exception is no longer raised and you can serialize and deserialize a payload containing these nested ParameterExpression objects. See #13879.

1.4.0
Prelude
The Qiskit v1.4 release is the final minor version release for the v1.x series. This release contains minimal features, and primarily adds new deprecation warnings for API changes coming in the future major version release v2.0. It is fully compatible with the Qiskit v1.3.x releases. It is strongly recommended that you upgrade from v1.3.x to v1.4 so that you’re able to see the warnings about which interfaces will change with Qiskit v2.0. The v1.4.x release series will continue to be supported and receive bugfixes for 6 months and security fixes for 1 year after this release. The fixes will take place via patch releases. For more details on the release schedule and support cycle see: open-source/qiskit-sdk-version-strategy which documents the release schedule in more detail.

Circuits Features
Added a new method, QuantumCircuit.estimate_duration(), to compute the estimated duration of a scheduled circuit output from the transpiler. This should be used if you need an estimate of the full circuit duration instead of the deprecated QuantumCircuit.duration attribute.
Circuits Deprecations
Subclassing Register or Bit, or any subclass of them (for example, QuantumRegister or Qubit) is deprecated as of Qiskit v1.4. Subclassing these types was never explicitly supported by Qiskit, and its meaning was never defined. In Qiskit v2.0, the subclassing may become impossible due to technical limitations, and will certainly not be stored in a circuit. This is due to the move of the data model to the Rust space to improve performance.

The dag optional parameter in the constructor of DAGNode subclasses (namely DAGOpNode), which has been unused and ignored since Qiskit v1.2, is now deprecated as of Qiskit v1.4 and will be removed in Qiskit v2.0.

The Multiple-Control-Multiple-Target (MCMT) class in MCMT is now deprecated and replaced by MCMTGate, which is a proper Gate subclass. Using a gate instead of a circuit allows the compiler to reason about the object at a higher level of abstraction and unlocks the use of multiple synthesis plugins.

The qiskit.circuit.classicalfunction module, and with it the ClassicalFunction class and its related classical_function() and BooleanExpression utilities, have been deprecated as of Qiskit v1.4 and will be removed in Qiskit v2.0.

This change is performed to avoid a dependency on the external library tweedledum, which is no longer compatible with all of Qiskit’s supported platforms and Python versions. For a similar functionality please use the PhaseOracle which is going to have an implementation that doesn’t use tweedledum, and the BitFlipOracle which will be added in Qiskit v2.0.

Until BitFlipOracle is added, a phase-flip oracle can be converted to a bit-flip oracle by conditioning it on the result qubit, and applying Hadamard gates before and after the application of the oracle, as in the following example (where the oracle is on qr_x and the result is on qr_y):


from qiskit import QuantumRegister, QuantumCircuit
from qiskit.circuit.library.phase_oracle import PhaseOracle
 
bool_expr = "(x0 & x1 | ~x2) & x4"
qr_x = QuantumRegister(4, "x")
qr_y = QuantumRegister(1, "y")
 
bit_flip_oracle = QuantumCircuit(qr_x, qr_y)
phase_flip_oracle = PhaseOracle(bool_expr)
controlled_phase_flip_oracle = phase_flip_oracle.control(1)
bit_flip_oracle.h(qr_y)
bit_flip_oracle.compose(controlled_phase_flip_oracle, qubits=[*qr_y, *qr_x], inplace=True)
bit_flip_oracle.h(qr_y)
 
print(bit_flip_oracle)
Which results in


          ┌───────────────┐     
x_0: ─────┤0              ├─────
          │               │     
x_1: ─────┤1              ├─────
          │  Phase Oracle │     
x_2: ─────┤2              ├─────
          │               │     
x_3: ─────┤3              ├─────
     ┌───┐└───────┬───────┘┌───┐
  y: ┤ H ├────────■────────┤ H ├
     └───┘                 └───┘
Primitives Deprecations
Providing inputs of type BackendV1 to the backend argument of BackendSamplerV2 and BackendEstimatorV2 is deprecated as of Qiskit 1.4 and will be removed in Qiskit 2.0. Use an instance of BackendV2 instead.
Providers Deprecations
The BackendV2Converter class and convert_to_target() functions have been deprecated in Qiskit v1.4 following the deprecation of BackendV1. The convert_to_target() function is used to build a Target instance from a series of objects from the deprecated BackendV1 workflow: BackendConfiguration, BackendProperties and PulseDefaults. BackendV2Converter is used for converting BackendV1 to BackendV2, and cannot be maintained once BackendV1 is removed.

The BasicSimulator.run_experiment() method has been deprecated and will be removed in Qiskit v2.0. The method takes a QasmQobjExperiment as input argument, which has been deprecated together with the Qobj class and other related functionality. You can call BasicSimulator.run() with a QuantumCircuit input instead.

The error types BackendPropertyError and BackendConfigurationError have been deprecated in Qiskit 1.4 and will be removed in Qiskit 2.0. These errors are only used when retrieving items from the deprecated BackendProperties and BackendConfiguration objects.

The classes GateProperties, BackendStatus, and qiskit.providers.models.JobStatus, which are part of the legacy BackendV1 workflow, are now deprecated. These should have been deprecated in Qiskit 1.2 together with the related elements in qiskit.providers.models.

Synthesis Deprecations
The signature of the argument atomic_evolution in the constructor of the classes LieTrotter, ProductFormula, and SuzukiTrotter was modified in Qiskit v1.2 to improve the visualization of the output circuit. The older signature has now been deprecated in favor of the new alternative. From Qiskit v2.0, only the new alternative will be valid.

To migrate, please modify the callable from Callable[[Pauli | SparsePauliOp, float], QuantumCircuit] to Callable[[QuantumCircuit, Pauli | SparsePauliOp, float], None].

Transpiler Deprecations
The DAGOpNode.sort_key, DAGOutNode.sort_key, and DAGInNode.sort_key attributes have been deprecated and will be removed in the Qiskit v2.0 release. These attributes were originally used as a lexicographical key for topological sorting nodes in a DAGCircuit. However, the key is no longer used for this as the sorting is done internally in Rust code now. If you’re using this attribute, you can recreate the key from the other attributes of a node. For example, you can use a function like:


def get_sort_key(node: DAGNode):
    if isinstance(node, (DAGInNode, DAGOutNode)):
        return str(node.wire)
    return ",".join(
        f"{dag.find_bit(q).index:04d}" for q in itertools.chain(node.qargs, node.cargs)
    )
which will generate a string like the sort key does.

The following uses of the BackendProperties object in the transpilation pipeline have been deprecated as of Qiskit v1.4 and will be removed in Qiskit v2.0:

backend_prop input argument in DenseLayout
properties input argument in VF2Layout
properties and coupling_map input arguments in VF2PostLayout. Note that coupling_map was only used in the presence of properties.
backend_props input argument in UnitarySynthesis
backend_properties input argument in PassManagerConfig
backend_properties in Target.from_configuration()
backend_properties in generate_routing_passmanager()
backend_properties in generate_translation_passmanager()
The BackendProperties class has been deprecated since Qiskit v1.2, together with other elements from the BackendV1 workflow, and will be removed in Qiskit v2.0. The alternative path for communicating hardware information to the transpilation argument is the Target class, which can be set using the target input argument. Specific instruction properties such as gate errors or durations can be added to a Target upon construction through the Target.add_instruction() method.

In the case of generate_routing_passmanager() and generate_translation_passmanager(), the backend_properties argument is optional and is superseded when the required target argument is populated. Usage of the argument can safely be removed in 1.x as long as you were passing in a target, which was the recommended use.

The Pulse deprecation in Qiskit v1.3, included calibration builder passes such as RXCalibrationBuilder. The NormalizeRXAngle pass is a requirement of RXCalibrationBuilder; hence, it is being deprecated in Qiskit v1.4. The rzx_templates() function in the calibration module is also being deprecated as it is not used in our codebase.

Visualization Deprecations
The parameters show_idle and show_barrier in the timeline drawers are deprecated as of Qiskit v1.4. The alternatives are, respectively, the idle_wires and plot_barriers parameters, introduced in Qiskit v1.1, which are fully equivalent. The legacy parameter names will be removed in Qiskit v2.0.

In Qiskit v1.4, the timeline drawer timeline_drawer() function will issue a deprecation warning if a target is not specified to get the duration of instructions. From Qiskit v2.0 on, target will be required and timeline_drawer() will fail if it is not specified.

Providing inputs of type BackendV1 to the backend argument of plot_gate_map(), plot_circuit_layout(), and plot_error_map() are deprecated as of Qiskit 1.4 and will be removed in Qiskit 2.0. Use an instance of BackendV2 instead.

Misc. Deprecations
The use of positional arguments in the constructor of Result is deprecated as of Qiskit 1.4, and will be disabled in Qiskit 2.0. Please set all arguments using kwarg syntax, i.e: Result(backend_name="name", ....). In addition to this, the qobj_id argument is deprecated and will no longer be used in Qiskit 2.0. It will, however, still be possible to set qobj_id as a generic kwarg, which will land in the metadata field with the other generic kwargs.
Bug Fixes
Fixed an issue in Target.has_calibration() and Target.get_calibration() where passing a parameterized Gate didn’t work as expected. Refer to qiskit/#11657 and qiskit/#11658 for more information.
Other Notes
Passing property_set as an arbitrary keyword argument to the run() method of a subclass of BasePassManager will change behavior in Qiskit v2.0. It is currently forwarded to the internal representation converting functions of the pass manager, as is any arbitrary keyword argument to that method. Starting from Qiskit v2.0, the option will instead be used to set the seed of the PropertySet for the pipeline run, and the argument will not be passed to the conversion functions.

This note only concerns implementers of subclasses of BasePassManager who have chosen their _passmanager_frontend and _passmanager_backend implementations to accept a keyword argument called property_set.