Qiskit 0.17 release notes
0.17.0
Terra 0.12.0
No Change
Aer 0.4.1
No Change
Ignis 0.2.0
No Change
Aqua 0.6.5
No Change
IBM Q Provider 0.6.0
New Features
There are three new exceptions:
VisualizationError
,
VisualizationValueError
, and
VisualizationTypeError
. These are now used in the visualization modules when an exception is raised.
You can now set the logging level and specify a log file using the environment variables
QSIKIT_IBMQ_PROVIDER_LOG_LEVEL
and
QISKIT_IBMQ_PROVIDER_LOG_FILE
, respectively. Note that the name of the logger is
qiskit.providers.ibmq
.
qiskit.providers.ibmq.job.IBMQJob
now has a new method
scheduling_mode()
that returns the scheduling mode the job is in.
IQX-related tutorials that used to be in
qiskit-iqx-tutorials
are now in
qiskit-ibmq-provider
.
Changed
qiskit.providers.ibmq.IBMQBackend.jobs()
now accepts a new boolean parameter
descending
, which can be used to indicate whether the jobs should be returned in descending or ascending order.
qiskit.providers.ibmq.managed.IBMQJobManager
now looks at the job limit and waits for old jobs to finish before submitting new ones if the limit has been reached.
qiskit.providers.ibmq.IBMQBackend.status()
now raises a
qiskit.providers.ibmq.IBMQBackendApiProtocolError
exception if there was an issue with validating the status.