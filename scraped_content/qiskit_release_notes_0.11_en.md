Qiskit 0.11 release notes
0.11.1
We have bumped up Qiskit micro version to 0.11.1 because IBM Q Provider has bumped its micro version as well.
Terra 0.8
No Change
Aer 0.2
No change
Ignis 0.1
No Change
Aqua 0.5
qiskit-aqua
has been updated to
0.5.3
to fix code related to changes in how gates inverses are done.
IBM Q Provider 0.3
The
IBMQProvider
has been updated to version
0.3.1
to fix backward compatibility issues and work with the default 10 job limit in single calls to the IBM Q API v2.
0.11
We have bumped up Qiskit minor version to 0.11 because IBM Q Provider has bumped up its minor version too. On Aer, we have jumped from 0.2.1 to 0.2.3 because there was an issue detected right after releasing 0.2.2 and before Qiskit 0.11 went online.
Terra 0.8
No Change
Aer 0.2
New features
Added support for multi-controlled phase gates
Added optimized anti-diagonal single-qubit gates
Improvements
Introduced a technique called Fusion that increments performance of circuit execution Tuned threading strategy to gain performance in most common scenarios.
Some of the already implemented error models have been polished.
Ignis 0.1
No Change
Aqua 0.5
No Change
IBM Q Provider 0.3
The
IBMQProvider
has been updated in order to default to use the new
IBM Q Experience v2
. Accessing the legacy IBM Q Experience v1 and QConsole will still be supported during the 0.3.x line until its final deprecation one month from the release. It is encouraged to update to the new IBM Q Experience to take advantage of the new functionality and features.
Updating to the new IBM Q Experience v2
If you have credentials for the legacy IBM Q Experience stored on disk, you can make use of the interactive helper:
from
qiskit
import
IBMQ
IBMQ
.
update_account
()
For more complex cases or fine tuning your configuration, the following methods are available:
the
IBMQ.delete_accounts()
can be used for resetting your configuration file.
the
IBMQ.save_account('MY_TOKEN')
method can be used for saving your credentials, following the instructions in the
IBM Q Experience v2
account page.
Updating your programs
When using the new IBM Q Experience v2 through the provider, access to backends is done via individual
provider
instances (as opposed to accessing them directly through the
qiskit.IBMQ
object as in previous versions), which allows for more granular control over the project you are using.
You can get a reference to the
providers
that you have access to using the
IBMQ.providers()
and
IBMQ.get_provider()
methods:
from
qiskit
import
IBMQ
provider
=
IBMQ
.
load_account
()
my_providers
=
IBMQ
.
providers
()
provider_2
=
IBMQ
.
get_provider
(hub
=
'A'
, group
=
'B'
, project
=
'C'
)
For convenience,
IBMQ.load_account()
and
IBMQ.enable_account()
will return a provider for the open access project, which is the default in the new IBM Q Experience v2.
For example, the following program in previous versions:
from
qiskit
import
IBMQ
IBMQ
.
load_accounts
()
backend
=
IBMQ
.
get_backend
(
'ibmqx4'
)
backend_2
=
IBMQ
.
get_backend
(
'ibmq_qasm_simulator'
, hub
=
'HUB2'
)
Would be equivalent to the following program in the current version:
from
qiskit
import
IBMQ
provider
=
IBMQ
.
load_account
()
backend
=
provider
.
get_backend
(
'ibmqx4'
)
provider_2
=
IBMQ
.
get_provider
(hub
=
'HUB2'
)
backend_2
=
provider_2
.
get_backend
(
'ibmq_qasm_simulator'
)
You can find more information and details in the
IBM Q Provider documentation
.