Qiskit 0.44 release notes
Version history
This is the final release in which
qiskit
was a “meta-package”, which contained several different “elements”. What is called “Qiskit Terra” within this (and earlier) release notes is principally what is now just called “Qiskit”.
This table tracks the meta-package versions and the version of each legacy Qiskit element installed:
Qiskit Metapackage Version
qiskit-terra
qiskit-aer
qiskit-ignis
qiskit-ibmq-provider
qiskit-aqua
Release Date
0.44.1
0.25.1
2023-08-17
0.44.0
0.25.0
2023-07-27
0.43.3
0.24.2
0.12.2
0.20.2
2023-07-19
0.43.2
0.24.1
0.12.1
0.20.2
2023-06-28
0.43.1
0.24.1
0.12.0
0.20.2
2023-06-02
0.43.0
0.24.0
0.12.0
0.20.2
2023-05-04
0.42.1
0.23.3
0.12.0
0.20.2
2023-03-21
0.42.0
0.23.2
0.12.0
0.20.2
2023-03-10
0.41.1
0.23.2
0.11.2
0.20.1
2023-02-23
0.41.0
0.23.1
0.11.2
0.20.0
2023-01-31
0.40.0
0.23.0
0.11.2
0.19.2
2023-01-26
0.39.5
0.22.4
0.11.2
0.19.2
2023-01-17
0.39.4
0.22.3
0.11.2
0.19.2
2022-12-08
0.39.3
0.22.3
0.11.1
0.19.2
2022-11-25
0.39.2
0.22.2
0.11.1
0.19.2
2022-11-03
0.39.1
0.22.1
0.11.1
0.19.2
2022-11-02
0.39.0
0.22.0
0.11.0
0.19.2
2022-10-13
0.38.0
0.21.2
0.11.0
0.19.2
2022-09-14
0.37.2
0.21.2
0.10.4
0.19.2
2022-08-23
0.37.1
0.21.1
0.10.4
0.19.2
2022-07-28
0.37.0
0.21.0
0.10.4
0.19.2
2022-06-30
0.36.2
0.20.2
0.10.4
0.7.1
0.19.1
2022-05-18
0.36.1
0.20.1
0.10.4
0.7.0
0.19.1
2022-04-21
0.36.0
0.20.0
0.10.4
0.7.0
0.19.0
2022-04-06
0.35.0
0.20.0
0.10.3
0.7.0
0.18.3
2022-03-31
0.34.2
0.19.2
0.10.3
0.7.0
0.18.3
2022-02-09
0.34.1
0.19.1
0.10.2
0.7.0
0.18.3
2022-01-05
0.34.0
0.19.1
0.10.1
0.7.0
0.18.3
2021-12-20
0.33.1
0.19.1
0.9.1
0.7.0
0.18.2
2021-12-10
0.33.0
0.19.0
0.9.1
0.7.0
0.18.1
2021-12-06
0.32.1
0.18.3
0.9.1
0.6.0
0.18.1
0.9.5
2021-11-22
0.32.0
0.18.3
0.9.1
0.6.0
0.18.0
0.9.5
2021-11-10
0.31.0
0.18.3
0.9.1
0.6.0
0.17.0
0.9.5
2021-10-12
0.30.1
0.18.3
0.9.0
0.6.0
0.16.0
0.9.5
2021-09-29
0.30.0
0.18.2
0.9.0
0.6.0
0.16.0
0.9.5
2021-09-16
0.29.1
0.18.2
0.8.2
0.6.0
0.16.0
0.9.5
2021-09-10
0.29.0
0.18.1
0.8.2
0.6.0
0.16.0
0.9.4
2021-08-02
0.28.0
0.18.0
0.8.2
0.6.0
0.15.0
0.9.4
2021-07-13
0.27.0
0.17.4
0.8.2
0.6.0
0.14.0
0.9.2
2021-06-15
0.26.2
0.17.4
0.8.2
0.6.0
0.13.1
0.9.1
2021-05-19
0.26.1
0.17.4
0.8.2
0.6.0
0.13.1
0.9.1
2021-05-18
0.26.0
0.17.3
0.8.2
0.6.0
0.13.1
0.9.1
2021-05-11
0.25.4
0.17.2
0.8.2
0.6.0
0.12.3
0.9.1
2021-05-05
0.25.3
0.17.1
0.8.2
0.6.0
0.12.3
0.9.1
2021-04-29
0.25.2
0.17.1
0.8.1
0.6.0
0.12.3
0.9.1
2021-04-21
0.25.1
0.17.1
0.8.1
0.6.0
0.12.2
0.9.1
2021-04-15
0.25.0
0.17.0
0.8.0
0.6.0
0.12.2
0.9.0
2021-04-02
0.24.1
0.16.4
0.7.6
0.5.2
0.12.2
0.8.2
2021-03-24
0.24.0
0.16.4
0.7.6
0.5.2
0.12.1
0.8.2
2021-03-04
0.23.6
0.16.4
0.7.5
0.5.2
0.11.1
0.8.2
2021-02-18
0.23.5
0.16.4
0.7.4
0.5.2
0.11.1
0.8.2
2021-02-08
0.23.4
0.16.3
0.7.3
0.5.1
0.11.1
0.8.1
2021-01-28
0.23.3
0.16.2
0.7.3
0.5.1
0.11.1
0.8.1
2021-01-26
0.23.2
0.16.1
0.7.2
0.5.1
0.11.1
0.8.1
2020-12-15
0.23.1
0.16.1
0.7.1
0.5.1
0.11.1
0.8.1
2020-11-12
0.23.0
0.16.0
0.7.0
0.5.0
0.11.0
0.8.0
2020-10-16
0.22.0
0.15.2
0.6.1
0.4.0
0.10.0
0.7.5
2020-10-05
0.21.0
0.15.2
0.6.1
0.4.0
0.9.0
0.7.5
2020-09-16
0.20.1
0.15.2
0.6.1
0.4.0
0.8.0
0.7.5
2020-09-08
0.20.0
0.15.1
0.6.1
0.4.0
0.8.0
0.7.5
2020-08-10
0.19.6
0.14.2
0.5.2
0.3.3
0.7.2
0.7.3
2020-06-25
0.19.5
0.14.2
0.5.2
0.3.2
0.7.2
0.7.3
2020-06-19
0.19.4
0.14.2
0.5.2
0.3.0
0.7.2
0.7.2
2020-06-16
0.19.3
0.14.1
0.5.2
0.3.0
0.7.2
0.7.1
2020-06-02
0.19.2
0.14.1
0.5.1
0.3.0
0.7.1
0.7.1
2020-05-14
0.19.1
0.14.1
0.5.1
0.3.0
0.7.0
0.7.0
2020-05-01
0.19.0
0.14.0
0.5.1
0.3.0
0.7.0
0.7.0
2020-04-30
0.18.3
0.13.0
0.5.1
0.3.0
0.6.1
0.6.6
2020-04-24
0.18.2
0.13.0
0.5.0
0.3.0
0.6.1
0.6.6
2020-04-23
0.18.1
0.13.0
0.5.0
0.3.0
0.6.0
0.6.6
2020-04-20
0.18.0
0.13.0
0.5.0
0.3.0
0.6.0
0.6.5
2020-04-09
0.17.0
0.12.0
0.4.1
0.2.0
0.6.0
0.6.5
2020-04-01
0.16.2
0.12.0
0.4.1
0.2.0
0.5.0
0.6.5
2020-03-20
0.16.1
0.12.0
0.4.1
0.2.0
0.5.0
0.6.4
2020-03-05
0.16.0
0.12.0
0.4.0
0.2.0
0.5.0
0.6.4
2020-02-27
0.15.0
0.12.0
0.4.0
0.2.0
0.4.6
0.6.4
2020-02-06
0.14.1
0.11.1
0.3.4
0.2.0
0.4.5
0.6.2
2020-01-07
0.14.0
0.11.0
0.3.4
0.2.0
0.4.4
0.6.1
2019-12-10
0.13.0
0.10.0
0.3.2
0.2.0
0.3.3
0.6.1
2019-10-17
0.12.2
0.9.1
0.3.0
0.2.0
0.3.3
0.6.0
2019-10-11
0.12.1
0.9.0
0.3.0
0.2.0
0.3.3
0.6.0
2019-09-30
0.12.0
0.9.0
0.3.0
0.2.0
0.3.2
0.6.0
2019-08-22
0.11.2
0.8.2
0.2.3
0.1.1
0.3.2
0.5.5
2019-08-20
0.11.1
0.8.2
0.2.3
0.1.1
0.3.1
0.5.3
2019-07-24
0.11.0
0.8.2
0.2.3
0.1.1
0.3.0
0.5.2
2019-07-15
0.10.5
0.8.2
0.2.1
0.1.1
0.2.2
0.5.2
2019-06-27
0.10.4
0.8.2
0.2.1
0.1.1
0.2.2
0.5.1
2019-06-17
0.10.3
0.8.1
0.2.1
0.1.1
0.2.2
0.5.1
2019-05-29
0.10.2
0.8.0
0.2.1
0.1.1
0.2.2
0.5.1
2019-05-24
0.10.1
0.8.0
0.2.0
0.1.1
0.2.2
0.5.0
2019-05-07
0.10.0
0.8.0
0.2.0
0.1.1
0.2.1
0.5.0
2019-05-06
0.9.0
0.8.0
0.2.0
0.1.1
0.1.1
0.5.0
2019-05-02
0.8.1
0.7.2
0.1.1
0.1.0
2019-05-01
0.8.0
0.7.1
0.1.1
0.1.0
2019-03-05
0.7.3
>=0.7,<0.8
>=0.1,<0.2
2019-02-19
0.7.2
>=0.7,<0.8
>=0.1,<0.2
2019-01-22
0.7.1
>=0.7,<0.8
>=0.1,<0.2
2019-01-17
0.7.0
>=0.7,<0.8
>=0.1,<0.2
2018-12-14
Note
For the
0.7.0
,
0.7.1
, and
0.7.2
meta-package releases the meta-package versioning strategy was not formalized yet.
0.44.1
Terra 0.25.1
Prelude
Qiskit Terra 0.25.1 is a bugfix release, addressing some issues identified since the 0.25.1 release.
Bug Fixes
Fixed a bug in QPY serialization (
qiskit.qpy
) where multiple controlled custom gates in a circuit could result in an invalid QPY file that could not be parsed. Fixed
#9746
.
Fixed
#9363
. by labeling the non-registerless synthesis in the order that Tweedledum returns. For example, compare this example before and after the fix:
from
qiskit
.
circuit
import
QuantumCircuit
from
qiskit
.
circuit
.
classicalfunction
import
BooleanExpression
boolean_exp
=
BooleanExpression
.
from_dimacs_file
(
"simple_v3_c2.cnf"
)
circuit
=
QuantumCircuit
(boolean_exp.num_qubits)
circuit
.
append
(boolean_exp,
range
(boolean_exp.num_qubits))
circuit
.
draw
(
"text"
)
from
qiskit
.
circuit
.
classicalfunction
import
classical_function
from
qiskit
.
circuit
.
classicalfunction
.
types
import
Int1
@classical_function
def
grover_oracle
(
a
:
Int1
,
b
:
Int1
,
c
:
Int1)
->
Int1:
return
(a
and
b
and
not
c)
quantum_circuit
=
grover_oracle
.
synth
(registerless
=
False
)
print
(quantum_circuit.
draw
())
Which would print
Before             After
c
:
──■──           a
:
──■──
│                  │
b
:
──■──           b
:
──■──
│                  │
a
:
──o──           c
:
──o──
┌─┴─┐              ┌─┴─┐
return
:
┤ X ├
return
:
┤ X ├
└───┘              └───┘
Fixed
plot_state_paulivec()
, which previously damped the state coefficients by a factor of
2
n
2^n
2
n
, where
n
n
n
is the number of qubits. Now the bar graph correctly displays the coefficients as
T
r
(
σ
ρ
)
\mathrm{Tr}(\sigma\rho)
Tr
(
σ
ρ
)
, where
ρ
\rho
ρ
is the state to be plotted and
σ
\sigma
σ
iterates over all possible tensor products of single-qubit Paulis.
Angles in the OpenQASM 2 exporter (
QuantumCircuit.qasm()
) will now always include a decimal point, for example in the case of
1.e-5
. This is required by a strict interpretation of the floating-point-literal specification in OpenQASM 2. Qiskit’s OpenQASM 2 parser (
qasm2.load()
and
loads()
) is more permissive by default, and will allow
1e-5
without the decimal point unless in
strict
mode.
The setter for
SparsePauliOp.paulis
will now correctly reject attempts to set the attribute with incorrectly shaped data, rather than silently allowing an invalid object to be created. See
#10384
.
Fixed a performance regression in the
SabreLayout
and
SabreSwap
transpiler passes. Fixed
#10650
0.44.0
This release officially marks the end of support for the Qiskit IBMQ Provider package and the removal of Qiskit Aer from the Qiskit metapackage. After this release the metapackage only contains Qiskit Terra, so this is the final release we will refer to the Qiskit metapackage and Qiskit Terra as separate things. Starting in the next release Qiskit 0.45.0 the Qiskit package will just be what was previously Qiskit Terra and there will no longer be a separation between them.
If you’re still using the
qiskit-ibmq-provider
package it has now been retired and is no longer supported. You should follow the links to the migration guides in the README for the package on how to switch over to the new replacement packages
qiskit-ibm-provider
,
qiskit-ibm-runtime
, and
qiskit-ibm-experiment
:
https://github.com/Qiskit/qiskit-ibmq-provider#migration-guides
The Qiskit Aer project is still active and maintained moving forward it is just no longer included as part of the
qiskit
package. To continue using
qiskit-aer
you will need to explicitly install
qiskit-aer
and import the package from
qiskit_aer
.
As this is the final release of the Qiskit metapackage the following setuptools extras used to install optional dependencies will no longer work in the next release Qiskit 0.45.0:
nature
machine-learning
finance
optimization
experiments
If you’re using the extras to install any packages you should migrate to using the packages directly instead of the extra. For example if you were using
pip install qiskit[experiments]
previously you should switch to
pip install qiskit qiskit-experiments
to install both packages. Similarly the
all
extra (what gets installed via
pip install "qiskit[all]"
) will no longer include these packages in Qiskit 0.45.0.
Terra 0.25.0
Prelude
The Qiskit Terra 0.25.0 release highlights are:
Control-flow operations are now supported through the transpiler at all optimization levels, including levels 2 and 3 (e.g. calling
transpile()
or
generate_preset_pass_manager()
with keyword argument
optimization_level
specified as 2 or 3 is now supported).
The fields
IfElseOp.condition
,
WhileLoopOp.condition
and
SwitchCaseOp.target
can now be instances of the new runtime classical-expression type
expr.Expr
. This is distinct from
ParameterExpression
because it is evaluated
at runtime
for backends that support such operations.
These new expressions have significantly more power than the old two-tuple form of supplying classical conditions. For example, one can now represent equality constraints between two different classical registers, or the logic “or” of two classical bits. These two examples would look like:
from
qiskit
.
circuit
import
QuantumCircuit
,
ClassicalRegister
,
QuantumRegister
from
qiskit
.
circuit
.
classical
import
expr
qr
=
QuantumRegister
(
4
)
cr1
=
ClassicalRegister
(
2
)
cr2
=
ClassicalRegister
(
2
)
qc
=
QuantumCircuit
(qr, cr1, cr2)
qc
.
h
(
0
)
qc
.
cx
(
0
,
1
)
qc
.
h
(
2
)
qc
.
cx
(
2
,
3
)
qc
.
measure
([
0
,
1
,
2
,
3
], [
0
,
1
,
2
,
3
])
# If the two registers are equal to each other.
with
qc
.
if_test
(expr.
equal
(cr1, cr2)):
qc
.
x
(
0
)
# While either of two bits are set.
with
qc
.
while_loop
(expr.
logic_or
(cr1[
0
], cr1[
1
])):
qc
.
reset
(
0
)
qc
.
reset
(
1
)
qc
.
measure
([
0
,
1
], cr1)
For more examples, see the documentation for
qiskit.circuit.classical
.
This feature is new for both Qiskit and the available quantum hardware that Qiskit works with. As the features are still being developed there are likely to be places where there are unexpected edge cases that will need some time to be worked out. If you encounter any issue around classical expression support or usage please open an issue with Qiskit or your hardware vendor.
In this initial release, Qiskit has added the operations:
bit_not()
logic_not()
bit_and()
bit_or()
bit_xor()
logic_and()
logic_or()
equal()
not_equal()
less()
less_equal()
greater()
greater_equal()
These can act on Python integer and Boolean literals, or on
ClassicalRegister
and
Clbit
instances.
All these classical expressions are fully supported through the Qiskit transpiler stack, through QPY serialisation (
qiskit.qpy
) and for export to OpenQASM 3 (
qiskit.qasm3
). Import from OpenQASM 3 is currently managed by
a separate package
(which is re-exposed via
qiskit.qasm3
), which we hope will be extended to match the new features in Qiskit.
The
qiskit.algorithms
module has been deprecated and will be removed in a future release. It has been superseded by a new standalone library
qiskit-algorithms
which can be found on PyPi or on Github here:
https://github.com/qiskit-community/qiskit-algorithms
The
qiskit.algorithms
module will continue to work as before and bug fixes will be made to it until its future removal, but active development of new features has moved to the new package. If you’re relying on
qiskit.algorithms
you should update your Python requirements to also include
qiskit-algorithms
and update the imports from
qiskit.algorithms
to
qiskit_algorithms
. Please note that this new package does not include already deprecated algorithms code, including
opflow
and
QuantumInstance
-based algorithms. If you have not yet migrated from
QuantumInstance
-based to primitives-based algorithms, you should follow the migration guidelines in
https://qisk.it/algo_migration
. The decision to migrate the
algorithms
module to a separate package was made to clarify the purpose Qiskit and make a distinction between the tools and libraries built on top of it.
Qiskit Terra 0.25 has dropped support for Python 3.7 following deprecation warnings started in Qiskit Terra 0.23. This is consistent with Python 3.7’s end-of-life on the 27th of June, 2023. To continue using Qiskit, you must upgrade to a more recent version of Python.
New Features
The following features have been added in this release.
Transpiler Features
Added two new options to
BlockCollector
.
The first new option
split_layers
allows collected blocks to be split into sub-blocks over disjoint qubit subsets, i.e. into depth-1 sub-blocks.
The second new option
collect_from_back
allows blocks to be greedily collected starting from the outputs of the circuit. This is important in combination with ALAP-scheduling passes where we may prefer to put gates in the later rather than earlier blocks.
Added new options
split_layers
and
collect_from_back
to
CollectLinearFunctions
and
CollectCliffords
transpiler passes.
When
split_layers
is True, the collected blocks are split into into sub-blocks over disjoint qubit subsets, i.e. into depth-1 sub-blocks. Consider the following example:
from
qiskit
.
circuit
import
QuantumCircuit
from
qiskit
.
transpiler
.
passes
import
CollectLinearFunctions
circuit
=
QuantumCircuit
(
5
)
circuit
.
cx
(
0
,
2
)
circuit
.
cx
(
1
,
4
)
circuit
.
cx
(
2
,
0
)
circuit
.
cx
(
0
,
3
)
circuit
.
swap
(
3
,
2
)
circuit
.
swap
(
4
,
1
)
# Collect all linear gates, without splitting into layers
qct
=
CollectLinearFunctions
(split_blocks
=
False
, min_block_size
=
1
, split_layers
=
False
)(circuit)
assert
qct
.
count_ops
()
[
"linear_function"
]
==
1
# Collect all linear gates, with splitting into layers
qct
=
CollectLinearFunctions
(split_blocks
=
False
, min_block_size
=
1
, split_layers
=
True
)(circuit)
assert
qct
.
count_ops
()
[
"linear_function"
]
==
4
The original circuit is linear. When collecting linear gates without splitting into layers, we should end up with a single linear function. However, when collecting linear gates and splitting into layers, we should end up with 4 linear functions.
When
collect_from_back
is True, the blocks are greedily collected from the outputs towards the inputs of the circuit. Consider the following example:
from
qiskit
.
circuit
import
QuantumCircuit
from
qiskit
.
transpiler
.
passes
import
CollectLinearFunctions
circuit
=
QuantumCircuit
(
3
)
circuit
.
cx
(
1
,
2
)
circuit
.
cx
(
1
,
0
)
circuit
.
h
(
2
)
circuit
.
swap
(
1
,
2
)
# This combines the CX(1, 2) and CX(1, 0) gates into a single linear function
qct
=
CollectLinearFunctions
(collect_from_back
=
False
)(circuit)
# This combines the CX(1, 0) and SWAP(1, 2) gates into a single linear function
qct
=
CollectLinearFunctions
(collect_from_back
=
True
)(circuit)
The original circuit contains a Hadamard gate, so that the CX(1, 0) gate can be combined either with CX(1, 2) or with SWAP(1, 2), but not with both. When
collect_from_back
is False, the linear blocks are greedily collected from the start of the circuit, and thus CX(1, 0) is combined with CX(1, 2). When
collect_from_back
is True, the linear blocks are greedily collected from the end of the circuit, and thus CX(1, 0) is combined with SWAP(1, 2).
Added
DAGCircuit.classical_predecessors()
and
DAGCircuit.classical_successors()
, an alternative to selecting classical wires that doesn’t require accessing the inner graph of a DAG node directly. The following example illustrates the new functionality:
from
qiskit
import
QuantumCircuit
,
QuantumRegister
,
ClassicalRegister
from
qiskit
.
converters
import
circuit_to_dag
from
qiskit
.
circuit
.
library
import
RZGate
q
=
QuantumRegister
(
3
,
'q'
)
c
=
ClassicalRegister
(
3
,
'c'
)
circ
=
QuantumCircuit
(q, c)
circ
.
h
(q[
0
])
circ
.
cx
(q[
0
], q[
1
])
circ
.
measure
(q[
0
], c[
0
])
circ
.
rz
(
0.5
, q[
1
]).
c_if
(c,
2
)
circ
.
measure
(q[
1
], c[
0
])
dag
=
circuit_to_dag
(circ)
rz_node
=
dag
.
op_nodes
(RZGate)
[
0
]
# Contains the "measure" on clbit 0, and the "wire start" nodes for clbits 1 and 2.
classical_predecessors
=
list
(dag.
classical_predecessors
(rz_node))
# Contains the "measure" on clbit 0, and the "wire end" nodes for clbits 1 and 2.
classical_successors
=
list
(dag.
classical_successors
(rz_node))
Enabled support for
ControlFlowOp
operations in the
CommutativeCancellation
pass. Previously, the blocks in control flow operations were skipped by this pass.
Enabled support for
ControlFlowOp
operations in the
ConsolidateBlocks
pass.
Added
DAGCircuit.quantum_causal_cone()
to obtain the causal cone of a qubit in a
DAGCircuit
. The following example shows its correct usage:
from
qiskit
import
QuantumCircuit
,
QuantumRegister
,
ClassicalRegister
from
qiskit
.
circuit
.
library
import
CXGate
,
CZGate
from
qiskit
.
dagcircuit
import
DAGCircuit
# Build a DAGCircuit
dag
=
DAGCircuit
()
qreg
=
QuantumRegister
(
5
)
creg
=
ClassicalRegister
(
5
)
dag
.
add_qreg
(qreg)
dag
.
add_creg
(creg)
dag
.
apply_operation_back
(
CXGate
(), qreg[[
1
,
2
]], [])
dag
.
apply_operation_back
(
CXGate
(), qreg[[
0
,
3
]], [])
dag
.
apply_operation_back
(
CZGate
(), qreg[[
1
,
4
]], [])
dag
.
apply_operation_back
(
CZGate
(), qreg[[
2
,
4
]], [])
dag
.
apply_operation_back
(
CXGate
(), qreg[[
3
,
4
]], [])
# Get the causal cone of qubit at index 0
result
=
dag
.
quantum_causal_cone
(qreg[
0
])
A new method
find_bit()
has been added to the
DAGCircuit
class, which returns the bit locations of the given
Qubit
or
Clbit
as a tuple of the positional index of the bit within the circuit and a list of tuples which locate the bit in the circuit’s registers.
The transpiler’s built-in
EquivalenceLibrary
(
qiskit.circuit.equivalence_library.SessionEquivalenceLibrary
) has been taught the circular Pauli relations
X
=
i
Y
Z
X = iYZ
X
=
iY
Z
,
Y
=
i
Z
X
Y = iZX
Y
=
i
ZX
and
Z
=
i
X
Y
Z = iXY
Z
=
i
X
Y
. This should make transpiling to constrained, and potentially incomplete, basis sets more reliable. See
#10293
for more detail.
Control-flow operations are now supported through the transpiler at all optimization levels, including levels 2 and 3 (e.g. calling
transpile()
or
generate_preset_pass_manager()
with keyword argument
optimization_level=3
).
DAGCircuit.substitute_node()
gained a
propagate_condition
keyword argument that is analogous to the same argument in
substitute_node_with_dag()
. Setting this to
False
opts out of the legacy behaviour of copying a condition on the
node
onto the new
op
that is replacing it.
This option is ignored for general control-flow operations, which will never propagate their condition, nor accept a condition from another node.
Introduced a new method,
DAGCircuit.separable_circuits()
, which returns a list of
DAGCircuit
objects, one for each set of connected qubits which have no gates connecting them to another set.
Each
DAGCircuit
instance returned by this method will contain the same number of clbits as
self
. This method will not return
DAGCircuit
instances consisting solely of clbits.
Added the attribute
Target.concurrent_measurements
which represents a hardware constraint of qubits measured concurrently. This constraint is provided in a nested list form, in which each element represents a qubit group to be measured together. In an example below:
[[
0
,
1
]
,
[
2
,
3
,
4
]]
qubits 0 and 1, and 2, 3 and 4 are measured together on the device. This constraint doesn’t block measuring an individual qubit, but you may need to consider the alignment of measure operations for these qubits when working with the
Qiskit Pulse scheduler
and when authoring new transpiler passes that are timing-aware (i.e. passes that perform scheduling).
The transpiler pass
SetLayout
can now be constructed with a list of integers that represent the physical qubits on which the quantum circuit will be mapped on. That is, the first qubit in the circuit will be allocated to the physical qubit in position zero of the list, and so on.
The transpiler’s built-in
EquivalenceLibrary
has been taught more Pauli-rotation equivalences between the one-qubit
R
X
R_X
R
X
​
,
R
Y
R_Y
R
Y
​
and
R
Z
R_Z
R
Z
​
gates, and between the two-qubit
R
X
X
R_{XX}
R
XX
​
,
R
Y
Y
R_{YY}
R
YY
​
and
R
Z
Z
R_{ZZ}
R
ZZ
​
gates. This should make simple basis translations more reliable, especially circuits that use
Y
Y
Y
rotations. See
#7332
.
Control-flow operations are now supported by the Sabre family of transpiler passes, namely layout pass
SabreLayout
and routing pass
SabreSwap
. Function
transpile()
keyword arguments
layout_method
and
routing_method
now accept the option
"sabre"
for circuits with control flow, which was previously unsupported.
Circuits Features
The fields
IfElseOp.condition
,
WhileLoopOp.condition
and
SwitchCaseOp.target
can now be instances of the new runtime classical-expression type
expr.Expr
. This is distinct from
ParameterExpression
because it is evaluated
at runtime
for backends that support such operations.
These new expressions have significantly more power than the old two-tuple form of supplying classical conditions. For example, one can now represent equality constraints between two different classical registers, or the logic “or” of two classical bits. These two examples would look like:
from
qiskit
.
circuit
import
QuantumCircuit
,
ClassicalRegister
,
QuantumRegister
from
qiskit
.
circuit
.
classical
import
expr
qr
=
QuantumRegister
(
4
)
cr1
=
ClassicalRegister
(
2
)
cr2
=
ClassicalRegister
(
2
)
qc
=
QuantumCircuit
(qr, cr1, cr2)
qc
.
h
(
0
)
qc
.
cx
(
0
,
1
)
qc
.
h
(
2
)
qc
.
cx
(
2
,
3
)
qc
.
measure
([
0
,
1
,
2
,
3
], [
0
,
1
,
2
,
3
])
# If the two registers are equal to each other.
with
qc
.
if_test
(expr.
equal
(cr1, cr2)):
qc
.
x
(
0
)
# While either of two bits are set.
with
qc
.
while_loop
(expr.
logic_or
(cr1[
0
], cr1[
1
])):
qc
.
reset
(
0
)
qc
.
reset
(
1
)
qc
.
measure
([
0
,
1
], cr1)
For more examples, see the documentation for
qiskit.circuit.classical
.
This feature is new for both Qiskit and the available quantum hardware that Qiskit works with. As the features are still being developed there are likely to be places where there are unexpected edge cases that will need some time to be worked out. If you encounter any issue around classical expression support or usage please open an issue with Qiskit or your hardware vendor.
In this initial release, Qiskit has added the operations:
bit_not()
logic_not()
bit_and()
bit_or()
bit_xor()
logic_and()
logic_or()
equal()
not_equal()
less()
less_equal()
greater()
greater_equal()
These can act on Python integer and Boolean literals, or on
ClassicalRegister
and
Clbit
instances.
All these classical expressions are fully supported through the Qiskit transpiler stack, through QPY serialisation (
qiskit.qpy
) and for export to OpenQASM 3 (
qiskit.qasm3
). Import from OpenQASM 3 is currently managed by
a separate package
(which is re-exposed via
qiskit.qasm3
), which we hope will be extended to match the new features in Qiskit.
Tooling for working with the new representations of classical runtime expressions has been added. A general
ExprVisitor
is provided for consumers of these expressions to subclass. Two utilities based on this structure,
iter_vars()
and
structurally_equivalent()
, are also provided, which respectively produce an iterator through the
Var
nodes and check whether two
Expr
instances are structurally the same, up to some mapping of the
Var
nodes contained.
Added function
lift_legacy_condition()
which can be used to convert old-style conditions into new-style
Expr
nodes. Note that these expression nodes are not permitted in old-style
Instruction.condition
fields, which are due to be replaced by more advanced classical handling such as
IfElseOp
.
Added support for taking absolute values of
ParameterExpression
s. For example, the following is now possible:
from
qiskit
.
circuit
import
QuantumCircuit
,
Parameter
x
=
Parameter
(
"x"
)
circuit
=
QuantumCircuit
(
1
)
circuit
.
rx
(
abs
(x),
0
)
bound
=
circuit
.
bind_parameters
({x:
-
1
})
The performance of
QuantumCircuit.assign_parameters()
and
bind_parameters()
has significantly increased for large circuits with structures typical of applications uses. This includes most circuits based on the
NLocal
structure, such as
EfficientSU2
. See
#10282
for more detail.
The method
QuantumCircuit.assign_parameters()
has gained two new keywords arguments:
flat_input
and
strict
. These are advanced options that can be used to speed up the method when passing the parameter bindings as a dictionary;
flat_input=True
is a guarantee that the dictionary keys contain only
Parameter
instances (not
ParameterVector
s), and
strict=False
allows the dictionary to contain parameters that are not present in the circuit. Using these two options can reduce the overhead of input normalisation in this function.
Added a new keyword argument
flatten
to the constructor for the following classes:
EfficientSU2
ExcitationPreserving
NLocal
RealAmplitudes
TwoLocal
EvolvedOperatorAnsatz
QAOAAnsatz
If this argument is set to
True
the
QuantumCircuit
subclass generated will not wrap the implementation into
Gate
or
Instruction
objects. While this isn’t optimal for visualization it typically results in much better runtime performance, especially with
QuantumCircuit.bind_parameters()
and
QuantumCircuit.assign_parameters()
which can see a substatial runtime improvement with a flattened output compared to the nested wrapped default output.
Added support for constructing
LinearFunction
s from more general quantum circuits, that may contain:
Barriers (of type
Barrier
) and delays (
Delay
), which are simply ignored
Permutations (of type
PermutationGate
)
Other linear functions
Cliffords (of type
Clifford
), when the Clifford represents a linear function (and a
CircuitError
exception is raised if not)
Nested quantum circuits of this form
Added
LinearFunction.__eq__()
method. Two objects of type
LinearFunction
are considered equal when their representations as binary invertible matrices are equal.
Added
LinearFunction.extend_with_identity()
method, which allows to extend a linear function over
k
qubits to a linear function over
n >= k
qubits, specifying the new positions of the original qubits and padding with identities on the remaining qubits.
Added two methods for pretty-printing
LinearFunction
objects:
LinearFunction.mat_str()
, which returns the string representation of the linear function viewed as a matrix with 0/1 entries, and
LinearFunction.function_str()
, which returns the string representation of the linear function viewed as a linear transformation.
The instructions
StatePreparation
and
Initialize
, and their associated circuit methods
QuantumCircuit.prepare_state()
and
initialize()
, gained a keyword argument
normalize
, which can be set to
True
to automatically normalize an array target. By default this is
False
, which retains the current behaviour of raising an exception when given non-normalized input.
Algorithms Features
Added the option to pass a callback to the
UMDA
optimizer, which allows keeping track of the number of function evaluations, the current parameters, and the best achieved function value.
OpenQASM Features
The OpenQASM 3 exporters (
qasm3.dump()
,
dumps()
and
Exporter
) have a new
allow_aliasing
argument, which will eventually replace the
alias_classical_registers
argument. This controls whether aliasing is permitted for either classical bits or qubits, rather than the option only being available for classical bits.
Quantum Information Features
Added a new function
negativity()
that calculates the entanglement measure of negativity of a quantum state. Example usage of the above function is given below:
from
qiskit
.
quantum_info
.
states
.
densitymatrix
import
DensityMatrix
from
qiskit
.
quantum_info
.
states
.
statevector
import
Statevector
from
qiskit
.
quantum_info
import
negativity
import
numpy
as
np
# Constructing a two-qubit bell state vector
state
=
np
.
array
([
0
,
1
/
np.
sqrt
(
2
),
-
1
/
np.
sqrt
(
2
),
0
])
# Calculating negativity of statevector
negv
=
negativity
(
Statevector
(state), [
1
])
# Creating the Density Matrix (DM)
rho
=
DensityMatrix
.
from_label
(
"10+"
)
# Calculating negativity of DM
negv2
=
negativity
(rho, [
0
,
1
])
Added the function
schmidt_decomposition()
. This function works with the
Statevector
and
DensityMatrix
classes for bipartite pure states.
Adds support for multiplication of
SparsePauliOp
objects with
Parameter
objects by using the * operator, for example:
from
qiskit
.
circuit
import
Parameter
from
qiskit
.
quantum_info
import
SparsePauliOp
param
=
Parameter
(
"a"
)
op
=
SparsePauliOp
(
"X"
)
param
*
op
Pulse Features
The
SymbolicPulse
library was extended. The new pulse functions in the library are:
GaussianDeriv()
Sech()
SechDeriv()
Square()
The new functions return a
ScalableSymbolicPulse
instance, and match the functionality of the corresponding functions in the discrete pulse library, with the exception of
Square()
for which a phase of
2
π
2\pi
2
π
shifts by a full cycle (contrary to the discrete
square()
where such a shift was induced by a
π
\pi
π
phase).
The method
filter()
is activated in the
ScheduleBlock
class. This method enables users to retain only
Instruction
objects which pass through all the provided filters. As builtin filter conditions, pulse
Channel
subclass instance and
Instruction
subclass type can be specified. User-defined callbacks taking
Instruction
instance can be added to the filters, too.
The method
exclude()
is activated in the
ScheduleBlock
class. This method enables users to retain only
Instruction
objects which do not pass at least one of all the provided filters. As builtin filter conditions, pulse
Channel
subclass instance and
Instruction
subclass type can be specified. User-defined callbacks taking
Instruction
instance can be added to the filters, too. This method is the complement of
filter()
, so the following condition is always satisfied:
block.filter(*filters) + block.exclude(*filters) == block
in terms of instructions included, where
block
is a
ScheduleBlock
instance.
Added a new function
gaussian_square_echo()
to the pulse library. The returned pulse is composed of three
GaussianSquare
pulses. The first two are echo pulses with duration half of the total duration and implement rotary tones. The third pulse is a cancellation tone that lasts the full duration of the pulse and implements correcting single qubit rotations.
QPY supports the
Discriminator
and
Kernel
objects. This feature enables users to serialize and deserialize the
Acquire
instructions with these objects using QPY.
Synthesis Features
Added a new synthesis function
synth_cx_cz_depth_line_my()
which produces the circuit form of a CX circuit followed by a CZ circuit for linear nearest neighbor (LNN) connectivity in 2-qubit depth of at most 5n, using CX and phase gates (S, Sdg or Z). The synthesis algorithm is based on the paper of Maslov and Yang,
arXiv:2210.16195
.
The algorithm accepts a binary invertible matrix
mat_x
representing the CX-circuit, a binary symmetric matrix
mat_z
representing the CZ-circuit, and returns a quantum circuit with 2-qubit depth of at most 5n computing the composition of the CX and CZ circuits. The following example illustrates the new functionality:
import
numpy
as
np
from
qiskit
.
synthesis
.
linear_phase
import
synth_cx_cz_depth_line_my
mat_x
=
np
.
array
([[
0
,
1
], [
1
,
1
]])
mat_z
=
np
.
array
([[
0
,
1
], [
1
,
0
]])
qc
=
synth_cx_cz_depth_line_my
(mat_x, mat_z)
This function is now used by default in the Clifford synthesis algorithm
synth_clifford_depth_lnn()
that optimizes 2-qubit depth for LNN connectivity, improving the 2-qubit depth from 9n+4 to 7n+2. The clifford synthesis algorithm can be used as follows:
from
qiskit
.
quantum_info
import
random_clifford
from
qiskit
.
synthesis
import
synth_clifford_depth_lnn
cliff
=
random_clifford
(
3
)
qc
=
synth_clifford_depth_lnn
(cliff)
The above synthesis can be further improved as described in the paper by Maslov and Yang, using local optimization between 2-qubit layers. This improvement is left for follow-up work.
Visualization Features
QuantumCircuit.draw()
and function
circuit_drawer()
when using option
output='mpl'
now support drawing the nested circuit blocks of
ControlFlowOp
operations, including
if
,
else
,
while
,
for
, and
switch/case
. Circuit blocks are wrapped with boxes to delineate the circuits.
Some restrictions when using
wire_order
in the circuit drawers have been relaxed. Now,
wire_order
can list just qubits and, in that case, it can be used with
cregbundle=True
, since it will not affect the classical bits.
from
qiskit
import
QuantumCircuit
,
QuantumRegister
,
ClassicalRegister
qr
=
QuantumRegister
(
4
,
"q"
)
cr
=
ClassicalRegister
(
4
,
"c"
)
cr2
=
ClassicalRegister
(
2
,
"ca"
)
circuit
=
QuantumCircuit
(qr, cr, cr2)
circuit
.
h
(
0
)
circuit
.
h
(
3
)
circuit
.
x
(
1
)
circuit
.
x
(
3
).
c_if
(cr,
10
)
circuit
.
draw
(
'text'
, wire_order
=
[
2
,
3
,
0
,
1
], cregbundle
=
True
)
q_2
:
────────────
┌───┐ ┌───┐
q_3
:
┤ H ├─┤ X ├─
├───┤ └─╥─┘
q_0
:
┤ H ├───╫───
├───┤   ║
q_1
:
┤ X ├───╫───
└───┘┌──╨──┐
c
:
4
/
═════╡
0x
a
╞
└─────┘
ca
:
2
/
════════════
Misc. Features
A new lazy import tester,
HAS_PYGMENTS
, is available for testing for the presence of
the Pygments syntax highlighting library
.
The magic
%qiskit_version_table
from
qiskit.tools.jupyter
now includes all imported modules with
qiskit
in their name.
Upgrade Notes
Qiskit Terra 0.25 has dropped support for Python 3.7 following deprecation warnings started in Qiskit Terra 0.23. This is consistent with Python 3.7’s end-of-life on the 27th of June, 2023. To continue using Qiskit, you must upgrade to a more recent version of Python.
Qiskit Terra 0.25 now requires versison 0.13.0 of
rustworkx
.
By default Qiskit builds its compiled extensions using the
Python Stable ABI
with support back to the oldest version of Python supported by Qiskit (currently 3.8). This means that moving forward there will be a single precompiled wheel that is shipped on release that works with all of Qiskit’s supported Python versions. There isn’t any expected runtime performance difference using the limited API so it is enabled by default for all builds now. Previously, the compiled extensions were built using the version specific API and would only work with a single Python version. This change was made to reduce the number of package files we need to build and publish in each release. When building Qiskit from source, there should be no changes necessary to the build process except that the default tags in the output filenames will be different to reflect the use of the limited API.
Transpiler Upgrade Notes
Support for passing in lists of argument values to the
transpile()
function is removed. This functionality was deprecated as part of the 0.23.0 release. You are still able to pass in a list of
QuantumCircuit
objects for the first positional argument. What has been removed is list broadcasting of the other arguments to each circuit in that input list. Removing this functionality was necessary to greatly reduce the overhead for parallel execution for transpiling multiple circuits at once. If you’re using this functionality currently you can call
transpile()
multiple times instead. For example if you were previously doing something like:
from
qiskit
.
transpiler
import
CouplingMap
from
qiskit
import
QuantumCircuit
from
qiskit
import
transpile
qc
=
QuantumCircuit
(
2
)
qc
.
h
(
0
)
qc
.
cx
(
0
,
1
)
qc
.
measure_all
()
cmaps
=
[CouplingMap
.
from_heavy_hex
(d)
for
d
in
range
(
3
,
15
,
2
)
]
results
=
transpile
([qc]
*
6
, coupling_map
=
cmaps)
instead you should now run something like:
from
qiskit
.
transpiler
import
CouplingMap
from
qiskit
import
QuantumCircuit
from
qiskit
import
transpile
qc
=
QuantumCircuit
(
2
)
qc
.
h
(
0
)
qc
.
cx
(
0
,
1
)
qc
.
measure_all
()
cmaps
=
[CouplingMap
.
from_heavy_hex
(d)
for
d
in
range
(
3
,
15
,
2
)
]
results
=
[
transpile
(qc, coupling_map
=
cm)
for
cm
in
cmap]
You can also leverage
parallel_map()
or
multiprocessing
from the Python standard library if you want to run this in parallel.
The Sabre family of transpiler passes (namely
SabreLayout
and
SabreSwap
) are now used by default for all circuits when invoking the transpiler at optimization level 1 (e.g. calling
transpile()
or
generate_preset_pass_manager()
with keyword argument
optimization_level=1
). Previously, circuits with control flow operations used
DenseLayout
and
StochasticSwap
with this profile.
Circuits Upgrade Notes
The OpenQASM 2 constructor methods on
QuantumCircuit
(
from_qasm_str()
and
from_qasm_file()
) have been switched to use the Rust-based parser added in Qiskit Terra 0.24. This should result in significantly faster parsing times (10 times or more is not uncommon) and massively reduced intermediate memory usage.
The
QuantumCircuit
methods are kept with the same interface for continuity; the preferred way to access the OpenQASM 2 importer is to use
qasm2.load()
and
qasm2.loads()
, which offer an expanded interface to control the parsing and construction.
The deprecated
circuit_cregs
argument to the constructor for the
InstructionSet
class has been removed. It was deprecated in the 0.19.0 release. If you were using this argument and manually constructing an
InstructionSet
object (which should be quite uncommon as it’s mostly used internally) you should pass a callable to the
resource_requester
keyword argument instead. For example:
from
qiskit
.
circuit
import
Clbit
,
ClassicalRegister
,
InstructionSet
from
qiskit
.
circuit
.
exceptions
import
CircuitError
def
my_requester
(
bits
,
registers
):
bits_set
=
set
(bits)
bits_flat
=
tuple
(bits)
registers_set
=
set
(registers)
def
requester
(
specifier
):
if
isinstance
(specifer, Clbit)
and
specifier
in
bits_set
:
return
specifier
if
isinstance
(specifer, ClassicalRegster)
and
specifier
in
register_set
:
return
specifier
if
isinstance
(specifier,
int
)
and
0
<=
specifier
<
len
(bits_flat):
return
bits_flat
[
specifier
]
raise
CircuitError
(
f
"Unknown resource:
{
specifier
}
"
)
return
requester
my_bits
=
[
Clbit
()
for
_
in
[
None
]
*
5
]
my_registers
=
[
ClassicalRegister
(n)
for
n
in
range
(
3
)
]
InstructionSet
(resource_requester
=
my_requester
(my_bits, my_registers))
OpenQASM Upgrade Notes
The OpenQASM 2 constructor methods on
QuantumCircuit
(
from_qasm_str()
and
from_qasm_file()
) have been switched to use the Rust-based parser added in Qiskit Terra 0.24. This should result in significantly faster parsing times (10 times or more is not uncommon) and massively reduced intermediate memory usage.
The
QuantumCircuit
methods are kept with the same interface for continuity; the preferred way to access the OpenQASM 2 importer is to use
qasm2.load()
and
qasm2.loads()
, which offer an expanded interface to control the parsing and construction.
The OpenQASM 3 exporters (
qasm3.dump()
,
dumps()
and
Exporter
) will now use fewer “register alias” definitions in its output. The circuit described will not change, but it will now preferentially export in terms of direct
bit
,
qubit
and
qubit[n]
types rather than producing a
_loose_bits
register and aliasing more registers off this. This is done to minimise the number of advanced OpenQASM 3 features in use, and to avoid introducing unnecessary array structure into programmes that do not require it.
Quantum Information Upgrade Notes
Clifford.from_circuit()
will no longer attempt to resolve instructions whose
definition
fields are mutually recursive with some other object. Such recursive definitions are already a violation of the strictly hierarchical ordering that the
definition
field requires, and code should not rely on this being possible at all. If you want to define equivalences that are permitted to have (mutual) cycles, use an
EquivalenceLibrary
.
Visualization Upgrade Notes
In the internal
~qiskit.visualization.circuit.matplotlib.MatplotlibDrawer
object, the arguments
layout
,
global_phase
,
qregs
and
cregs
have been removed. They were originally deprecated in Qiskit Terra 0.20. These objects are simply inferred from the given
circuit
now.
This is an internal worker class of the visualization routines. It is unlikely you will need to change any of your code.
Misc. Upgrade Notes
The
qiskit.util
import location has been removed, as it had been deprecated since Qiskit Terra 0.17. Users should use the new import location,
qiskit.utils
.
Deprecation Notes
Extensions of the
qiskit
and
qiskit.providers
namespaces by external packages are now deprecated and the hook points enabling this will be removed in a future release. In the past, the Qiskit project was composed of elements that extended a shared namespace and these hook points enabled doing that. However, it was not intended for these interfaces to ever be used by other packages. Now that the overall Qiskit package is no longer using that packaging model, leaving the possibility for these extensions carry more risk than benefits and is therefore being deprecated for future removal. If you’re maintaining a package that extends the Qiskit namespace (i.e. your users import from
qiskit.x
or
qiskit.providers.y
) you should transition to using a standalone Python namespace for your package. No warning will be raised as part of this because there is no method to inject a warning at the packaging level that would be required to warn external packages of this change.
The dictionary
qiskit.__qiskit_version__
is deprecated, as Qiskit is defined with a single package (
qiskit-terra
). In the future,
qiskit.__version__
will be the single point to query the Qiskit version, as a standard string.
Transpiler Deprecations
The function
get_vf2_call_limit
available via the module
qiskit.transpiler.preset_passmanagers.common
has been deprecated. This will likely affect very few users since this function was neither explicitly exported nor documented. Its functionality has been replaced and extended by a function in the same module.
Circuits Deprecations
The method
qasm()
and all overriding methods of subclasses of :class:~qiskit.circuit.Instruction are deprecated. There is no replacement for generating an OpenQASM2 string for an isolated instruction as typically a single instruction object has insufficient context to completely generate a valid OpenQASM2 string. If you’re relying on this method currently you’ll have to instead rely on the OpenQASM2 exporter:
QuantumCircuit.qasm()
to generate the OpenQASM2 for an entire circuit object.
Algorithms Deprecations
The
qiskit.algorithms
module has been deprecated and will be removed in a future release. It has been superseded by a new standalone library
qiskit-algorithms
which can be found on PyPi or on Github here:
https://github.com/qiskit-community/qiskit-algorithms
The
qiskit.algorithms
module will continue to work as before and bug fixes will be made to it until its future removal, but active development of new features has moved to the new package. If you’re relying on
qiskit.algorithms
you should update your Python requirements to also include
qiskit-algorithms
and update the imports from
qiskit.algorithms
to
qiskit_algorithms
. Please note that this new package does not include already deprecated algorithms code, including
opflow
and
QuantumInstance
-based algorithms. If you have not yet migrated from
QuantumInstance
-based to primitives-based algorithms, you should follow the migration guidelines in
https://qisk.it/algo_migration
. The decision to migrate the
algorithms
module to a separate package was made to clarify the purpose Qiskit and make a distinction between the tools and libraries built on top of it.
Pulse Deprecations
Initializing a
ScalableSymbolicPulse
with complex value for
amp
. This change also affects the following library pulses:
Gaussian
GaussianSquare
Drag
Constant
Initializing
amp
for these with a complex value is now deprecated as well.
Instead, use two floats when specifying the
amp
and
angle
parameters, where
amp
represents the magnitude of the complex amplitude, and angle represents the angle of the complex amplitude. i.e. the complex amplitude is given by
amp
×
exp
⁡
(
i
×
angle
)
\texttt{amp} \times \exp(i \times \texttt{angle})
amp
×
exp
(
i
×
angle
)
.
The
Call
instruction has been deprecated and will be removed in a future release. Instead, use function
call()
from module
qiskit.pulse.builder
within an active building context.
Misc. Deprecations
The Jupyter magic
%circuit_library_info
and the objects in
qiskit.tools.jupyter.library
it calls in turn:
circuit_data_table
properties_widget
qasm_widget
circuit_digram_widget
circuit_library_widget
are deprecated and will be removed in a future release. These objects were only intended for use in the documentation build. They are no longer used there, so are no longer supported or maintained.
Known Issues
Circuits containing classical expressions made with the
expr
module are not yet supported by the circuit visualizers.
Bug Fixes
Fixed a bug in
Channel
where index validation was done incorrectly and only raised an error when the index was both non-integer and negative, instead of either.
Fixed an issue with the
transpile()
function and all the preset pass managers generated via
generate_preset_pass_manager()
where the output
QuantumCircuit
object’s
layout
attribute would have an invalid
TranspileLayout.final_layout
attribute. This would occur in scenarios when the
VF2PostLayout
pass would run and find an alternative initial layout that has lower reported error rates. When altering the initial layout the
final_layout
attribute was never updated to reflect this change. This has been corrected so that the
final_layout
is always correctly reflecting the output permutation caused by the routing stage. Fixed
#10457
The OpenQASM 2 parser (
qasm2.load()
and
loads()
) running in
strict
mode will now correctly emit an error if a
barrier
statement has no arguments. When running in the (default) more permissive mode, an argument-less
barrier
statement will continue to cause a barrier on all qubits currently in scope (the qubits a gate definition affects, or all the qubits defined by a program, if the statement is in a gate body or in the global scope, respectively).
The OpenQASM 2 exporter (
QuantumCircuit.qasm()
) will now no longer attempt to output
barrier
statements that act on no qubits. Such a barrier statement has no effect in Qiskit either, but is invalid OpenQASM 2.
Qiskit can represent custom instructions that act on zero qubits, or on a non-zero number of classical bits. These cannot be exported to OpenQASM 2, but previously
QuantumCircuit.qasm()
would try, and output invalid OpenQASM 2. Instead, a
QASM2ExportError
will now correctly be raised. See
#7351
and
#10435
.
Fixed an issue with using
Target
s without coupling maps with the
FullAncillaAllocation
transpiler pass. In this case,
FullAncillaAllocation
will now add ancilla qubits so that the number of qubits in the
DAGCircuit
matches that of
Target.num_qubits
.
DAGCircuit.substitute_node()
will no longer silently overwrite an existing condition on the given replacement
op
. If
propagate_condition
is set to
True
(the default), a
DAGCircuitError
will be raised instead.
A parametrised circuit that contains a custom gate whose definition has a parametrised global phase can now successfully bind the parameter in the inner global phase. See
#10283
for more detail.
Construction of a
Statevector
from a
QuantumCircuit
containing zero-qubit operations will no longer raise an error. These operations impart a global phase on the resulting statevector.
The control-flow builder interface will now correctly include
ClassicalRegister
resources from nested switch statements in their containing circuit scopes. See
#10398
.
Fixed an issue in
QuantumCircuit.decompose()
where passing a circuit name to the function that matched a composite gate name would not decompose the gate if it had a label assigned to it as well. Fixed
#9136
Fixed an issue with
qiskit.visualization.plot_histogram()
where the relative legend did not show up when the given dataset had a zero value in the first position. See
#10158
for more details.
Fixed a failure with method
Target.update_from_instruction_schedule_map()
triggered by the given
inst_map
containing a
Schedule
with unassigned durations.
When the parameter
conditional=True
is specified in
random_circuit()
, conditional operations in the resulting circuit will now be preceded by a full mid-circuit measurment. Fixes
#9016
Improved the type annotations on the
QuantumCircuit.assign_parameters()
method to reflect the change in return type depending on the
inplace
argument.
The OpenQASM 2 circuit-constructor methods (
QuantumCircuit.from_qasm_str()
and
from_qasm_file()
) will no longer error when encountering a
gate
definition that contains
U
or
CX
instructions. See
#5536
.
Reduced overhead of the
ConsolidateBlocks
pass by performing matrix operations on all two-qubit blocks instead of creating an instance of
QuantumCircuit
and passing it to an
Operator
. The speedup will only be applicable when consolidating two-qubit blocks. Anything higher than that will still be handled by the
Operator
class. Check
#8779
for details.
The OpenQASM 3 exporter (
qiskit.qasm3
) will no longer output invalid OpenQASM 3 for non-unitary
Instruction
instances, but will instead raise a
QASM3ExporterError
explaining that these are not yet supported. This feature is slated for a later release of Qiskit, when there are more classical-processing facilities throughout the library.
Fixes issue
#10185
.
Fixed an issue with function
state_to_latex()
. Previously, it produced invalid LaTeX with unintended coefficient rounding, which resulted in errors when calling
state_drawer()
. Fixed
#9297
.