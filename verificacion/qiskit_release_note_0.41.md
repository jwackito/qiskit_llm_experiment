Qiskit 0.41 release notes
0.41.1
Terra 0.23.2
Prelude
The Qiskit Terra 0.23.2 patch release fixes further bugs identified in the 0.23 series.

Bug Fixes
Add the following Clifford gates, that already exist in the circuit library, to the Clifford class: SXGate, SXdgGate, CYGate, DCXGate, iSwapGate and ECRGate.

Add a decomposition of an ECRGate into Clifford gates (up to a global phase) to the standard equivalence library.

Fixed an issue with the BackendV2Converter class when wrapping a BackendV1-based simulator. It would error if either the online_date field in the BackendConfiguration for the simulator was not present or if the simulator backend supported ideal implementations of gates that involve more than 1 qubit. Fixed #9562.

Fixed an incorrect return value of the method BackendV2Converter.meas_map() that had returned the backend dt instead.

Fixed missing return values from the methods BackendV2Converter.drive_channel(), measure_channel(), acquire_channel() and control_channel().

The deprecated Qubit and Clbit properties register and index will now be correctly round-tripped by QPY (qiskit.qpy) in all valid usages of QuantumRegister and ClassicalRegister. In earlier releases in the Terra 0.23 series, this information would be lost. In versions before 0.23.0, this information was partially reconstructed but could be incorrect or produce invalid circuits for certain register configurations.

The correct way to retrieve the index of a bit within a circuit, and any registers in that circuit the bit is contained within is to call QuantumCircuit.find_bit(). This method will return the correct information in all versions of Terra since its addition in version 0.19.

Fixed an issue with the InstructionScheduleMap.has_custom_gate() method, where it would always return True when the InstructionScheduleMap object was created by Target. Fixed #9595.

Fixed a bug in the NumPy-based eigensolvers (NumPyMinimumEigensolver / NumPyEigensolver) and in the SciPy-based time evolvers (SciPyRealEvolver / SciPyImaginaryEvolver), where operators that support conversion to sparse matrices, such as SparsePauliOp, were converted to dense matrices anyways.

Fixed a bug in generate_basic_approximations() where the inverse of the SdgGate was not correctly recognized as SGate. Fixed #9585.

Fixed a bug in the VQD algorithm where the energy evaluation function could not process batches of parameters, making it incompatible with optimizers with max_evals_grouped>1. Fixed #9500.

Fixed bug in QNSPSA which raised a type error when the computed fidelities happened to be of type int but the perturbation was of type float.

Aer 0.11.2
No change

IBM Q Provider 0.20.1
Since qiskit-ibmq-provider is now deprecated, the dependencies have been bumped and fixed to the latest working versions. There was an issue with the latest version of the requests-ntlm package which caused some end to end tests to fail.

0.41.0
Terra 0.23.1
Prelude
Qiskit Terra 0.23.1 is a small patch release to fix bugs identified in Qiskit Terra 0.23.0

Bug Fixes
An edge case of pickle InstructionScheduleMap with non-picklable iterable arguments is now fixed. Previously, using an unpickleable iterable as the arguments parameter to InstructionScheduleMap.add() (such as dict_keys) could cause parallel calls to transpile() to fail. These arguments will now correctly be normalized internally to list.

Fixed a performance bug in ReverseEstimatorGradient where the calculation did a large amount of unnecessary copies if the gradient was only calculated for a subset of parameters, or in a circuit with many unparameterized gates.

Fixed a bad deprecation of Register.name_format which had made the class attribute available only from instances and not the class. When trying to send dynamic-circuits jobs to hardware backends, this would frequently cause the error:


AttributeError: 'property' object has no attribute 'match'
Fixed #9493.

Aer 0.11.2
No change

IBM Q Provider 0.20.0
Prelude
This release of the qiskit-ibmq-provider package marks the package as deprecated and will be retired and archived in the future. The functionality in qiskit-ibmq-provider has been supersceded by 3 packages qiskit-ibm-provider, qiskit-ibm-runtime, and qiskit-ibm-experiment which offer different subsets of functionality that qiskit-ibmq-provider contained. You can refer to the table here:

https://github.com/Qiskit/qiskit-ibmq-provider#migration-guides

for links to the migration guides for moving from qiskit-ibmq-provider to its replacmeent packages.

Deprecation Notes
As of version 0.20.0, qiskit-ibmq-provider has been deprecated with its support ending and eventual archival being no sooner than 3 months from that date. The function provided by qiskit-ibmq-provider is not going away rather it has being split out to separate repositories. Please see https://github.com/Qiskit/qiskit-ibmq-provider#migration-guides.
Bug Fixes
In the upcoming terra release there will be a release candidate tagged prior to the final release. However changing the version string for the package is blocked on the qiskit-ibmq-provider right now because it is trying to parse the version and is assuming there will be no prelease suffix on the version string (see #8200 for the details). PR #1135 fixes this version parsing to use the regex from the pypa/packaging project which handles all the PEP440 package versioning include pre-release suffixes. This will enable terra to release an 0.21.0rc1 tag without breaking the qiskit-ibmq-provider.

PR #1129 updates least_busy() method to no longer support BaseBackend as a valid input or output type since it has been long deprecated in qiskit-terra and has recently been removed.

threading.currentThread and notifyAll were deprecated in Python 3.10 (October 2021) and will be removed in Python 3.12 (October 2023). PR #1133 replaces them with threading.current_thread, notify_all added in Python 2.6 (October 2008).

Calls to run a quantum circuit with dynamic=True now raise an error that asks the user to install the new qiskit-ibm-provider.

