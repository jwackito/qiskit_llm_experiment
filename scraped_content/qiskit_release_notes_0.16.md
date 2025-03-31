Qiskit 0.16 release notes
0.16.0
Terra 0.12.0
No Change
Aer 0.4.0
No Change
Ignis 0.2.0
No Change
Aqua 0.6.4
No Change
IBM Q Provider 0.5.0
New Features
Some of the visualization and Jupyter tools, including gate/error map and backend information, have been moved from
qiskit-terra
to
qiskit-ibmq-provider
. They are now under the
qiskit.providers.ibmq.jupyter
and
qiskit.providers.ibmq.visualization
. In addition, you can now use
%iqx_dashboard
to get a dashboard that provides both job and backend information.
Changed
JSON schema validation is no longer run by default on Qobj objects passed to
qiskit.providers.ibmq.IBMQBackend.run()
. This significantly speeds up the execution of the run() method. Qobj objects are still validated on the server side, and invalid Qobjs will continue to raise exceptions. To force local validation, set
validate_qobj=True
when you invoke
run()
.