Qiskit 0.30 release notes
0.30.1
Terra 0.18.3
Prelude
This bugfix release fixes a few minor issues in 0.18, including a performance regression in assemble when dealing with executing QuantumCircuit objects on pulse-enabled backends.

Bug Fixes
Fixed #7004 where AttributeError was raised when executing ScheduleBlock on a pulse backend. These blocks are now correctly treated as pulse jobs, like Schedule.
Fixed an issue causing an error when binding a complex parameter value to an operator’s coefficient. Casts to float in PrimitiveOp were generalized to casts to complex if necessary, but will remain float if there is no imaginary component. Fixes #6976.
Update the 1-qubit gate errors in plot_error_map to use the sx gate instead of the u2 gate, consistent with IBMQ backends.
Aer 0.9.0
No change

Ignis 0.6.0
No change

Aqua 0.9.5
No change

IBM Q Provider 0.16.0
No change

0.30.0
Terra 0.18.2
No change

Aer 0.9.0
Prelude
The 0.9 release includes new backend options for parallel exeuction of large numbers of circuits on a HPC cluster using a Dask distributed, along with other general performance improvements and bug fixes.

New Features
Added support for set_matrix_product_state.

Add qiskit library SXdgGate and CUGate to the supported basis gates for the Aer simulator backends. Note that the CUGate gate is only natively supported for the statevector and unitary methods. For other simulation methods it must be transpiled to the supported basis gates for that method.

Adds support for N-qubit Pauli gate ( qiskit.circuit.library.generalized_gates.PauliGate) to all simulation methods of the AerSimulator and QasmSimulator.

Adds the ability to set a custom executor and configure job splitting for executing multiple circuits in parallel on a HPC clustor. A custom executor can be set using the executor option, and job splitting is configured by using the max_job_size option.

For example configuring a backend and executing using


backend = AerSimulator(max_job_size=1, executor=custom_executor)
job = backend.run(circuits)
will split the exection into multiple jobs each containing a single circuit. If job splitting is enabled the run method will return a AerJobSet object containing all the individual AerJob classes. After all individual jobs finish running the job results are automatically combined into a single Result object that is returned by job.result().

Supported executors include those in the Python concurrent.futures module (eg. ThreadPoolExecutor, ProcessPoolExecutor), and Dask distributed Client executors if the optional dask library is installed. Using a Dask executor allows configuring parallel execution of multiple circuits on HPC clusters.

Adds ability to record logging data for the matrix_product_state simulation method to the experiment result metadata by setting the backend option mps_log_data=True. The saved data includes the bond dimensions and the discarded value (the sum of the squares of the Schmidt coeffients that were discarded by approximation) after every relevant circuit instruction.

The run() method for the AerSimulator, QasmSimulator, StatevectorSimulator, and UnitarySimulator has a new kwarg, parameter_binds which is used to provide a list of values to use for any unbound parameters in the inbound circuit. For example:


from qiskit.circuit import QuantumCircuit, Parameter
from qiskit.providers.aer import AerSimulator
 
shots = 1000
backend = AerSimulator()
circuit = QuantumCircuit(2)
theta = Parameter('theta')
circuit.rx(theta, 0)
circuit.cx(0, 1)
circuit.measure_all()
parameter_binds = [{theta: [0, 3.14, 6.28]}]
backend.run(circuit, shots=shots, parameter_binds=parameter_binds).result()
will run the input circuit 3 times with the values 0, 3.14, and 6.28 for theta. When running with multiple parameters the length of the value lists must all be the same. When running with multiple circuits, the length of parameter_binds must match the number of input circuits (you can use an empty dict, {}, if there are no binds for a circuit).

The PulseSimulator can now take QuantumCircuit objects on the run(). Previously, it only would except Schedule objects as input to run(). When a circuit or list of circuits is passed to the simulator it will call schedule() to convert the circuits to a schedule before executing the circuit. For example:


from qiskit.circuit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.test.mock import FakeVigo
from qiskit.providers.aer.backends import PulseSimulator
 
backend = PulseSimulator.from_backend(FakeVigo())
 
circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure_all()
 
transpiled_circuit = transpile(circuit, backend)
backend.run(circuit)
Known Issues
The SaveExpectationValue and SaveExpectationValueVariance have been disabled for the extended_stabilizer method of the QasmSimulator and AerSimulator due to returning the incorrect value for certain Pauli operator components. Refer to #1227 <https://github.com/Qiskit/qiskit-aer/issues/1227> for more information and examples.
Upgrade Notes
The default basis for the NoiseModel class has been changed from ["id", "u3", "cx"] to ["id", "rz", "sx", "cx"] due to the deprecation of the u3 circuit method in qiskit-terra and change of qiskit-ibmq-provider backend basis gates. To use the old basis gates you can initialize a noise model with custom basis gates as NoiseModel(basis_gates=["id", "u3", "cx"]).
Removed the backend_options kwarg from the run methnod of Aer backends that was deprecated in qiskit-aer 0.7. All run options must now be passed as separate kwargs.
Removed passing system_model as a positional arg for the run method of the PulseSimulator.
Deprecation Notes
Passing an assembled qobj directly to the run() method of the Aer simulator backends has been deprecated in favor of passing transpiled circuits directly as backend.run(circuits, **run_options).
All snapshot instructions in qiskit.providers.aer.extensions have been deprecated. For replacement use the save instructions from the qiskit.providers.aer.library module.
Adding non-local quantum errors to a NoiseModel has been deprecated due to inconsistencies in how this noise is applied to the optimized circuit. Non-local noise should be manually added to a scheduled circuit in Qiskit using a custom transpiler pass before being run on the simulator.
Use of the method option of the StatevectorSimulator, and UnitarySimulator to run a GPU simulation has been deprecated. To run a GPU simulation on a compatible system use the option device='GPU' instead.
Bug Fixes
Fixes performance issue with how the basis_gates configuration attribute was set. Previously there were unintended side-effects to the backend class which could cause repeated simulation runtime to incrementally increase. Refer to #1229 <https://github.com/Qiskit/qiskit-aer/issues/1229> for more information and examples.
Fixed bug in MPS::apply_kraus. After applying the kraus matrix to the relevant qubits, we should propagate the changes to the neighboring qubits.
Fixes a bug where qiskit-terra assumes that qubits in a multiplexer gate are first the targets and then the controls of the gate while qiskit-aer assumes the opposite order.
Fixes a bug introduced in 0.8.0 where GPU simulations would allocate unneeded host memory in addition to the GPU memory.
Fixes bug where the initialize instruction would disable measurement sampling optimization for the statevector and matrix product state simulation methods even when it was the first circuit instruction or applied to all qubits and hence deterministic.
Fix issue #1196 by using the inner products with the computational basis states to calculate the norm rather than the norm estimation algorithm.
Fixes a bug in the stabilizer simulator method of the QasmSimulator and AerSimulator where the expectation value for the save_expectation_value and snapshot_expectation_value could have the wrong sign for certain Y Pauli’s.
Fixes bug where the if the required memory is smaller than the system memory the multi-chunk simulation method was enabled and simulation was still started. This case will now throw an insufficient memory exception.
Fixes issue where setting the shots option for a backend with set_options(shots=k) was always running the default number of shots (1024) rather than the specified value.
Fixes a bug in how the AerSimulator handled the option value for max_parallel_experiments=1. Previously this was treated the same as max_parallel_experiments=0.
Fixes bug in the extended_stabilizer simulation method where it incorrectly treated qelay gate and multi-qubit Pauli instructions as unsupported.
Fixes typo in the AerSimulator and QasmSimulator options for the extended_stabilizer_norm_estimation_repetitions option.
Fixes bug with applying the unitary gate in using the matrix_product_state simulation method which did not correctly support permutations in the ordering of the qubits on which the gate is applied.
Fixes an issue where gate fusion could still be enabled for the matrix_product_state simulation method even though it is not supported. Now fusion is always disabled for this method.
Fixed bug in the matrix_product_state simulation method in computing the normalization following truncation of the Schmidt coefficients after performing the SVD.
Other Notes
Improves the performance of the measurement sampling algorithm for the matrix_product_state simulation method. The new default behaviour is to always sample using the improved mps_apply_measure method. The mps_probabilities sampling method be still used by setting the custom option value mps_sample_measure_algorithm="mps_probabilities".
Ignis 0.6.0
No change

Aqua 0.9.5
No change

IBM Q Provider 0.16.0
No change