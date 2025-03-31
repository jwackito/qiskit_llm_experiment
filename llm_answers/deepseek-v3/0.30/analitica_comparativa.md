## Comparativa analítica de: "taxonomia_manual_v0_30.md" vs "deepseek-chat_v0_30_29_03_2025-19:23":

<br>

| Titulo | Escenarios | Resumen | Flujo | # Ej. origen | # Ej. destino | Info. referencias | Coincidencias | Discrepancias |
| -------| ---------: | ------- | ----- | :----------: | :-----------: | ----------------- | ------------- | ------------- |
| Taxonomia manual | 9 | Foco en módulos, ejemplos faltantes y homogeneidad en flujo de cambiso y referencias | correcto y homogéneo 0.29 --> 0.30 | 0 | 3 | completa y homogénea (qrn)
| Taxonomia DeepSeek-v3 | 10 | Foco en tipo de cambio, flujos homogéneos, ejemplos completos y referencias completas | correcto y homogéneo 0.18.x --> 0.30.0 | 10 | 10 | completa, variada y descriptiva

<br>

| Escenario | Taxonomia Manual | Taxonomia DeepSeek-v3 | QSE/SE | Dificultad | Referencia | Observación | 
| :-------- | :--------------: | :-------------------: | :----: | :--------: | :--------- | :--------- |
| + Primitiva Q-Aer - **Compuertas Backend Simulator añadidas** | X | | | | | 
| + Primitiva Q-Aer vs Cambio en modelo de datos - **Soporte para compuerta Pauli de n qubits** | X | X | **QSE** | **Baja** | qrn0.30 vs Aer 0.9.0 New Features | Mientras que DeepSeek lo plantea como un cambio, la taxonomía manual, como un incremento funcional
| + Semántica Q-Aer vs Cambio en mecanismo de ejecución - **Nuevo parámetro "parameter_binds" en método run() de: AerSimulator, StatevectorSimulaor y UnitarySimulator** | X | X | **QSE** | **Baja** | qrn0.30 vs Aer 0.9.0 Release Notes | | 
| + Q-Aer, estructural y usabilidad - **Gestión de circuitos encapsulada en 'PulseSimulator'** | X | | | | |
| * Primitivas Q-Aer vs Modificación de parámetros - **Cambios de compuertas base por defecto en 'NoiseModel'** | X | X |  **QSE** | **Baja** | qrn0.30 vs Qiskit Aer 0.9 Notes |
| - Q-Aer - **Pasaje del objeto qobj en run() en Simulador Aer** | X | | | | |
| - Q-Aer vs reestructuración de módulos - **Deprecación de instantáneas en qiskit.providers.aer.extensions** | X | X | QSE | Baja vs Moderada| | Taxonomía manual lo cataloga como una deprecación en qiskit.providers.aer.extensions mientras que DeepSeek como una migración desde **qiskit.providers.aer.extensions** hacia **qiskit.providers.aer.library** |
| - Q-Aer vs Deprecacion de funcionalidad - **Adición de ruido no local sobre un circuito** | X | X | QSE vs SE | **Baja** | | Mientras que la taxonomia manual lo considera una deprecación más genérica, DeepSeek focaliza sobre backend_options en AerSimulator.run() en favor de noise_model aislado |
| - Q-Aer - **Parámetro "method" en "StatevectorSimulator" y "UnitarySimulator"** | X | | | | |
| * Cambio estructural **Migración desde "qiskit.providers.ibmq" a "qiskit_ibm_provider"** |  | X | | | |
| - Deprecación de métodos **u3** en favor de **rz y sx** |  | X | | | | Cambio estrechamente relacionado con las nuevas puertas base en 'NoiseModel'
| * Actualización de dependencia **numpy** a v1.2+ |  | X | | | |
| * Actualización de visualización **"plot_error_map" para utilizar sx en lugar de u2** |  | X | | | | Se trata de una actualización interna al método, el ejemplo de código no es relevante
| * Migración de funciones **Movimiento desde "qiskit.compiler.assemble()" a "qiskit.execute()" ** |  | X | | | |

<br>

| # Tipo | valor | Descripcion | Proporcion | 
| :------ | :----: | :-------- | -----: |
| Casos | 14 | Total de casos de la conjunción |
| Concordancias | 5 | Casos hallados por ambos métodos de búsqueda | 36 %
| Discrepancias | 4 | Casos hallados por taxonomía manual y no por la auotmatizada | 26 %
| Discrepancias | 5 | Casos hallados por taxonomía automatizada y no por la manual | 36 %

<br>

Resumen:
- La taxonomía manual no fue eficiente en detallar escenarios de migración que involucren librerías o herramientas externas.
- La taxonomía automatizada fue eficiente en abarcar migraciones internas de dificultad nula.
- La taxonomía automatizada fue más específica en la descripción de la fuente de información.
- La taxonomía automatizada fue más completa y eficiente en la descripción de ejemplos, aunque en ciertos casos (como el de optimizaciones internas) pueden replicarse y no tienen mucho sentido.

