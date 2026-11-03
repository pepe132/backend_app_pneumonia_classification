# Sistema inteligente de apoyo clínico para la clasificación de severidad en neumonía pediátrica mediante modelos de Machine Learning y Deep Learning

> Consulta [`docs/seguimiento_backend.md`](docs/seguimiento_backend.md) para ver
> el estado actualizado, los bloques terminados y los siguientes pendientes.

## 1. Descripción general del proyecto

El presente proyecto consiste en el desarrollo de una aplicación web de apoyo clínico orientada a la clasificación de severidad en neumonía pediátrica. El sistema permitirá al especialista registrar pacientes, capturar datos clínicos mediante formularios estructurados y, cuando sea necesario, cargar radiografías de tórax.

A partir de esta información, la aplicación utilizará dos modelos inteligentes previamente entrenados: un modelo de Machine Learning para el análisis de datos clínicos tabulares y un modelo de Deep Learning para la clasificación de imágenes radiográficas. La clasificación final de severidad será generada tomando en cuenta de manera conjunta los resultados del modelo tabular y, cuando exista una radiografía disponible, los resultados del modelo de imagen.

El sistema mostrará una clasificación auxiliar de severidad, probabilidades asociadas y recomendaciones clínicas orientativas relacionadas con procedimientos, medicamentos o protocolos a seguir. La aplicación estará diseñada como una herramienta de apoyo a la toma de decisiones, sin sustituir el criterio médico profesional ni emitir diagnósticos definitivos de manera autónoma.

---

## 2. Objetivo del proyecto

### 2.1 Objetivo general

Desarrollar una aplicación web de apoyo clínico para la clasificación de la severidad de neumonía pediátrica, mediante el análisis integrado de datos clínicos tabulares y radiografías de tórax, utilizando modelos de Machine Learning y Deep Learning, con el fin de proporcionar al especialista una estimación auxiliar del grado de severidad y recomendaciones orientativas sobre procedimientos, medicamentos o protocolos clínicos a seguir.

### 2.2 Objetivos específicos

- Permitir el registro y autenticación de usuarios del sistema.
- Registrar pacientes pediátricos con sus datos generales y clínicos relevantes.
- Capturar datos clínicos mediante formularios estructurados.
- Permitir la carga opcional de radiografías de tórax.
- Clasificar la severidad de neumonía pediátrica en categorías como baja, media o alta.
- Utilizar un modelo de Machine Learning para analizar datos clínicos tabulares.
- Utilizar un modelo de Deep Learning para analizar radiografías de tórax cuando estén disponibles.
- Integrar los resultados del modelo tabular y del modelo de imagen para generar una clasificación final auxiliar de severidad.
- Mostrar recomendaciones clínicas auxiliares según el nivel de severidad detectado.
- Guardar el historial de evaluaciones realizadas a cada paciente.
- Mostrar estadísticas generales sobre pacientes, severidades detectadas, resultados por modelo y tendencias.
- Proporcionar una interfaz clara, segura y fácil de usar para personal médico autorizado.

---

## 3. Alcance del proyecto

### 3.1 Alcance general

La aplicación estará enfocada en apoyar al especialista en la evaluación de pacientes pediátricos con sospecha o diagnóstico de neumonía, permitiendo ingresar datos clínicos, cargar radiografías de tórax y obtener una clasificación auxiliar de severidad mediante modelos inteligentes previamente entrenados.

La clasificación de severidad no dependerá únicamente de un solo modelo, sino que podrá considerar de forma conjunta la información clínica tabular y los hallazgos obtenidos del análisis de imagen, cuando ambos datos estén disponibles. En caso de no contar con radiografía, el sistema podrá generar una clasificación basada en el modelo tabular, indicando claramente que el análisis por imagen no fue incluido.

El sistema servirá como una herramienta auxiliar para la toma de decisiones, mostrando resultados interpretables y recomendaciones orientativas, sin sustituir el criterio médico profesional.

### 3.2 Incluye

La aplicación incluirá:

- Registro e inicio de sesión de usuarios.
- Gestión de pacientes.
- Captura de datos clínicos en formulario.
- Carga opcional de radiografía de tórax.
- Clasificación con modelo tabular.
- Clasificación con modelo de imagen.
- Clasificación final integrada considerando ambos modelos, cuando sea posible.
- Visualización comparativa de resultados por modelo.
- Recomendaciones clínicas auxiliares.
- Historial de evaluaciones por paciente.
- Dashboard con estadísticas.
- Vista de reportes o resultados.
- Administración básica de usuarios.
- Seguridad de acceso mediante autenticación.

### 3.3 Delimitaciones y limitaciones del sistema

El sistema generará clasificaciones auxiliares de severidad y recomendaciones clínicas orientativas con base en los resultados integrados del modelo tabular y del modelo de imagen, cuando exista radiografía disponible. Sin embargo, por su naturaleza de herramienta de apoyo clínico, la aplicación no sustituirá el criterio del especialista ni tendrá como finalidad emitir decisiones médicas autónomas.

El sistema no incluirá:

- Diagnóstico médico definitivo emitido de forma autónoma.
- Sustitución del juicio clínico del especialista.
- Prescripción automática de medicamentos.
- Indicaciones terapéuticas obligatorias o vinculantes.
- Interpretación radiológica completa equivalente a la valoración de un radiólogo.
- Seguimiento en tiempo real del paciente hospitalizado.
- Integración directa con expedientes clínicos hospitalarios.
- Integración con dispositivos médicos.
- Firma electrónica médica.
- Validación clínica multicéntrica dentro del alcance inicial del proyecto.

Las recomendaciones generadas por la aplicación deberán entenderse como sugerencias auxiliares basadas en el nivel de severidad estimado, orientadas a apoyar la toma de decisiones sobre posibles procedimientos, medicamentos o protocolos. La decisión final siempre corresponderá al especialista tratante, considerando la valoración clínica completa del paciente y los lineamientos institucionales aplicables.

---

## 4. Propuesta de módulos de la aplicación

### 4.1 Módulo de autenticación

Permite controlar el acceso al sistema mediante usuarios autorizados.

Funciones principales:

- Registro de usuario.
- Inicio de sesión.
- Cierre de sesión.
- Recuperación de contraseña.
- Manejo de roles.

Roles sugeridos:

- **Administrador:** gestiona usuarios, datos generales y configuración.
- **Especialista/Médico:** registra pacientes, realiza evaluaciones y consulta resultados.
- **Consulta/Lectura:** solo puede visualizar información y reportes.

---

### 4.2 Módulo de pacientes

Permite administrar la información de los pacientes pediátricos.

Funciones principales:

- Registrar paciente.
- Editar datos del paciente.
- Consultar lista de pacientes.
- Buscar paciente por nombre, expediente, edad o fecha.
- Ver historial clínico de evaluaciones.
- Asociar múltiples evaluaciones a un mismo paciente.


### 4.3 Módulo de evaluación clínica

Este módulo permite al especialista ingresar los datos clínicos del paciente en un formulario estructurado. La información capturada será enviada al modelo tabular para generar una primera clasificación de severidad.

Variables clínicas sugeridas:

- Saturación de oxígeno.
- Frecuencia respiratoria.
- Frecuencia cardiaca.
- Tiraje.
- Aleteo nasal.
- Sibilancias.
- Rechazo al alimento.
- Estado neurológico o escala de Glasgow.
- Desnutrición.
- MUAC.
- Antecedentes crónicos.
- Temperatura.
- Signos de dificultad respiratoria.
- Observaciones adicionales.

---

### 4.4 Módulo de carga de radiografía

Permite cargar una imagen radiográfica cuando el especialista lo considere necesario o cuando el caso clínico lo requiera.

Funciones principales:

- Subir imagen en formato JPG, PNG o DICOM en futuras versiones.
- Validar que el archivo sea una imagen válida.
- Asociar la radiografía al paciente.
- Enviar la imagen al modelo de Deep Learning.
- Mostrar la clasificación obtenida por imagen.
- Guardar la imagen o su referencia en el historial del paciente.

Clasificaciones posibles del modelo de imagen:

- Normal.
- Neumonía bacteriana.
- Neumonía viral.
- COVID-19.
- Otra categoría definida durante el entrenamiento del modelo.

---

### 4.5 Módulo de clasificación integrada de severidad

Este módulo representa una de las partes centrales del sistema. Su función es integrar los resultados del modelo tabular y del modelo de imagen para generar una clasificación final auxiliar de severidad.

El sistema podrá mostrar:

- Resultado del modelo tabular.
- Probabilidades por clase del modelo tabular.
- Resultado del modelo de imagen, si se cargó radiografía.
- Probabilidades o nivel de confianza del modelo de imagen.
- Comparación entre ambos modelos.
- Clasificación final sugerida.
- Nivel de confianza de la clasificación final.
- Advertencias si existen datos incompletos.
- Mensaje aclaratorio si no se cargó radiografía.

Ejemplo de salida:

```text
Clasificación del modelo tabular: Severidad alta
Probabilidades:
- Baja: 8%
- Media: 22%
- Alta: 70%

Clasificación del modelo de imagen: Neumonía bacteriana

Resultado final sugerido: Neumonía pediátrica de severidad alta

Nota: El resultado es auxiliar y debe ser interpretado por el especialista tratante.
```

En caso de que no exista radiografía:

```text
Clasificación del modelo tabular: Severidad media

No se incluyó análisis radiográfico debido a que no se cargó una imagen.

Resultado final sugerido: Neumonía pediátrica de severidad media basada en datos clínicos tabulares.
```

---

### 4.6 Módulo de recomendaciones clínicas auxiliares

Este módulo muestra recomendaciones según la severidad detectada. Las recomendaciones deben estar redactadas con precaución, dejando claro que son orientativas y deben ser validadas por el especialista.

#### Severidad baja

- Manejo ambulatorio según criterio médico.
- Vigilancia de signos de alarma.
- Revaloración si existe fiebre persistente, dificultad respiratoria o rechazo al alimento.
- Educación a cuidadores.

#### Severidad media

- Considerar observación hospitalaria.
- Monitorización de signos vitales.
- Evaluar oxigenoterapia si hay saturación disminuida.
- Considerar estudios complementarios.
- Revaloración periódica.

#### Severidad alta

- Priorizar valoración urgente.
- Monitorización continua.
- Oxigenoterapia o soporte ventilatorio según criterio médico.
- Considerar ingreso hospitalario.
- Activar protocolo institucional correspondiente.
- Evaluar referencia a unidad de mayor capacidad si es necesario.

Aviso recomendado:

> El sistema emite recomendaciones auxiliares que deben ser validadas por el especialista tratante. La aplicación no sustituye el juicio clínico ni establece diagnósticos definitivos.

---

### 4.7 Módulo de historial clínico de evaluaciones

Permite consultar evaluaciones previas de cada paciente.

Funciones principales:

- Ver historial por paciente.
- Consultar fecha de cada evaluación.
- Ver datos ingresados.
- Ver resultado del modelo tabular.
- Ver resultado del modelo de imagen.
- Ver clasificación final integrada.
- Ver recomendación generada.
- Comparar evolución entre evaluaciones.
- Exportar reporte en PDF en futuras versiones.

---

### 4.8 Módulo de estadísticas y dashboard

Muestra información general del sistema y permite visualizar indicadores útiles para el análisis de los casos registrados.

Indicadores sugeridos:

- Total de pacientes registrados.
- Total de evaluaciones realizadas.
- Pacientes clasificados con severidad baja, media y alta.
- Porcentaje de casos por severidad.
- Distribución por edad.
- Distribución por sexo.
- Casos con radiografía cargada.
- Resultados más frecuentes del modelo de imagen.
- Tendencias por fecha.
- Comparación entre clasificación tabular e imagen.
- Número de casos donde ambos modelos coincidieron.
- Número de casos donde existió discrepancia entre modelos.

---

### 4.9 Módulo de reportes

Permite generar reportes individuales o generales.

Reportes sugeridos:

- Reporte individual del paciente.
- Reporte de evaluación clínica.
- Reporte de severidad.
- Reporte de resultados por modelo.
- Reporte de clasificación final integrada.
- Reporte de estadísticas generales.
- Exportación a PDF.
- Exportación a Excel en futuras versiones.

---

### 4.10 Módulo de administración

Permite gestionar elementos generales del sistema para usuarios con rol administrador.

Funciones principales:

- Gestionar usuarios.
- Activar o desactivar cuentas.
- Cambiar roles.
- Configurar catálogos clínicos.
- Consultar actividad del sistema.
- Ver bitácora de uso.

---

### 4.11 Módulo de auditoría y trazabilidad

Este módulo es importante debido a que el sistema trabaja con información clínica.

Funciones principales:

- Registrar qué usuario creó una evaluación.
- Registrar fecha y hora de cada análisis.
- Registrar cambios en datos del paciente.
- Guardar resultados emitidos por cada modelo.
- Guardar la clasificación final integrada.
- Mantener trazabilidad de decisiones.
- Registrar errores o fallos en el procesamiento.

---

## 5. Requerimientos funcionales

Los requerimientos funcionales describen qué debe hacer el sistema.

### RF-01. Registro de usuarios

El sistema deberá permitir el registro de usuarios autorizados, solicitando datos como nombre, correo electrónico, contraseña y rol.

### RF-02. Inicio de sesión

El sistema deberá permitir que los usuarios registrados inicien sesión mediante correo electrónico y contraseña.

### RF-03. Gestión de roles

El sistema deberá permitir asignar roles a los usuarios, tales como administrador, especialista o usuario de consulta.

### RF-04. Registro de pacientes

El sistema deberá permitir registrar pacientes pediátricos con datos generales y clínicos básicos.

### RF-05. Consulta de pacientes

El sistema deberá permitir visualizar, buscar y filtrar pacientes registrados.

### RF-06. Edición de pacientes

El sistema deberá permitir modificar la información de un paciente previamente registrado.

### RF-07. Registro de evaluación clínica

El sistema deberá permitir capturar datos clínicos del paciente mediante un formulario estructurado.

### RF-08. Validación de datos clínicos

El sistema deberá validar que los datos requeridos estén completos y se encuentren dentro de rangos permitidos antes de enviarlos al modelo.

### RF-09. Clasificación mediante modelo tabular

El sistema deberá enviar los datos clínicos al modelo de Machine Learning tabular para obtener una clasificación preliminar de severidad.

### RF-10. Carga de radiografía

El sistema deberá permitir cargar una radiografía de tórax asociada al paciente.

### RF-11. Clasificación mediante modelo de imagen

El sistema deberá enviar la radiografía al modelo de Deep Learning para obtener una clasificación relacionada con neumonía.

### RF-12. Visualización de resultados por modelo

El sistema deberá mostrar por separado el resultado del modelo tabular y el resultado del modelo de imagen, cuando la radiografía haya sido cargada.

### RF-13. Clasificación final integrada

El sistema deberá generar una clasificación final auxiliar de severidad considerando los resultados del modelo tabular y del modelo de imagen cuando ambos estén disponibles.

### RF-14. Clasificación sin radiografía

El sistema deberá permitir generar una clasificación basada únicamente en el modelo tabular cuando no se cargue radiografía, indicando claramente que el análisis por imagen no fue incluido.

### RF-15. Visualización de probabilidades

El sistema deberá mostrar las probabilidades o niveles de confianza asociados a cada clase generada por los modelos.

### RF-16. Generación de recomendaciones

El sistema deberá mostrar recomendaciones auxiliares según el grado de severidad obtenido.

### RF-17. Historial de evaluaciones

El sistema deberá guardar cada evaluación realizada y asociarla al paciente correspondiente.

### RF-18. Consulta de historial

El sistema deberá permitir consultar el historial de evaluaciones de un paciente.

### RF-19. Dashboard estadístico

El sistema deberá mostrar estadísticas generales sobre pacientes, evaluaciones y resultados de severidad.

### RF-20. Generación de reportes

El sistema deberá permitir generar reportes de evaluación para consulta o impresión.

### RF-21. Bitácora de actividad

El sistema deberá registrar acciones importantes realizadas por los usuarios, como creación, edición o eliminación de registros.

### RF-22. Cierre de sesión

El sistema deberá permitir al usuario cerrar sesión de forma segura.

### RF-23. Manejo de errores en predicción

El sistema deberá informar al usuario si ocurre un error al procesar los datos clínicos, cargar la imagen o ejecutar alguno de los modelos.

### RF-24. Confirmación antes de guardar evaluación

El sistema deberá permitir revisar la información capturada antes de guardar definitivamente una evaluación clínica.

### RF-25. Consulta de evaluaciones por fecha

El sistema deberá permitir filtrar evaluaciones por rango de fechas, paciente, usuario o nivel de severidad.

---

## 6. Requerimientos no funcionales

Los requerimientos no funcionales describen cómo debe comportarse el sistema.

### RNF-01. Seguridad

El sistema deberá proteger el acceso mediante autenticación segura, manejo de sesiones y contraseñas cifradas.

### RNF-02. Privacidad de datos

El sistema deberá proteger la información clínica de los pacientes, evitando accesos no autorizados.

### RNF-03. Confidencialidad

Los datos de pacientes, evaluaciones y radiografías deberán estar disponibles únicamente para usuarios autorizados.

### RNF-04. Usabilidad

La interfaz deberá ser clara, intuitiva y fácil de usar para personal médico, evitando procesos complejos o innecesarios.

### RNF-05. Rendimiento

El sistema deberá procesar las evaluaciones clínicas en un tiempo razonable, idealmente en pocos segundos.

### RNF-06. Disponibilidad

El sistema deberá estar disponible para su uso durante los horarios definidos por la institución o servicio médico.

### RNF-07. Escalabilidad

La arquitectura deberá permitir agregar nuevos modelos, nuevas variables clínicas o nuevos módulos en futuras versiones.

### RNF-08. Mantenibilidad

El código deberá organizarse por módulos para facilitar correcciones, mejoras y mantenimiento futuro.

### RNF-09. Trazabilidad

El sistema deberá conservar registros de evaluaciones, resultados, usuarios responsables y fechas de procesamiento.

### RNF-10. Integridad de datos

El sistema deberá evitar registros incompletos, duplicados o inconsistentes mediante validaciones.

### RNF-11. Compatibilidad

La aplicación deberá funcionar en navegadores modernos como Chrome, Edge y Firefox.

### RNF-12. Responsividad

La interfaz deberá adaptarse a diferentes tamaños de pantalla, como computadora, tablet o laptop.

### RNF-13. Interpretabilidad

El sistema deberá presentar resultados comprensibles para el especialista, evitando mostrar únicamente salidas técnicas del modelo.

### RNF-14. Limitación clínica

El sistema deberá mostrar un aviso indicando que los resultados son auxiliares y no sustituyen el juicio clínico del médico.

### RNF-15. Almacenamiento seguro

Las imágenes, resultados y datos clínicos deberán almacenarse de manera segura, con control de acceso.

### RNF-16. Control de errores

El sistema deberá manejar errores de carga, predicción, conexión o datos inválidos sin interrumpir completamente la aplicación.

### RNF-17. Tiempo de respuesta

El sistema deberá responder rápidamente a las acciones del usuario, especialmente en consultas, formularios y predicciones.

### RNF-18. Modularidad

El sistema deberá separar frontend, backend, base de datos y servicios de modelos para facilitar futuras mejoras.

### RNF-19. Disponibilidad de resultados históricos

El sistema deberá permitir consultar evaluaciones previas sin alterar los resultados originalmente generados.

### RNF-20. Consistencia del modelo

El sistema deberá utilizar versiones controladas de los modelos para garantizar que las predicciones puedan ser trazables y reproducibles.

### RNF-21. Manejo de imágenes

El sistema deberá optimizar el procesamiento y almacenamiento de imágenes para evitar tiempos de carga excesivos.

### RNF-22. Accesibilidad

La interfaz deberá procurar buenas prácticas de accesibilidad, como textos legibles, contraste adecuado y navegación clara.

---

## 7. Recomendación de arquitectura del sistema


### 7.2 Backend

API encargada de manejar usuarios, pacientes, evaluaciones, seguridad y conexión con los modelos.


```text
FastAPI con Python
```

Esta opción es conveniente porque los modelos de Machine Learning y Deep Learning suelen entrenarse y ejecutarse fácilmente en Python.

### 7.3 Modelos inteligentes

Modelos considerados:

- Modelo tabular: XGBoost, Random Forest, LightGBM o similar.
- Modelo de imagen: CNN, MobileNetV2, EfficientNet o similar.

El backend será responsable de recibir los datos, enviarlos al modelo correspondiente y devolver las predicciones al frontend.

### 7.4 Base de datos

Para guardar usuarios, pacientes, evaluaciones, resultados y trazabilidad.

- SQL Server.


### 7.5 Almacenamiento de imágenes

Para radiografías:

- Carpeta protegida en servidor.
- Bucket en la nube.
- Base de datos solo con la ruta del archivo.

---

## 8. Flujo principal del sistema

```text
1. El especialista inicia sesión.
2. Selecciona o registra un paciente.
3. Llena el formulario clínico.
4. Opcionalmente carga una radiografía de tórax.
5. El sistema envía los datos clínicos al modelo tabular.
6. Si hay imagen, el sistema envía la radiografía al modelo de Deep Learning.
7. El sistema recibe las predicciones de cada modelo.
8. El sistema integra los resultados disponibles.
9. Se muestra la clasificación final auxiliar de severidad.
10. Se muestran probabilidades, nivel de confianza y recomendaciones.
11. Se guarda la evaluación en el historial del paciente.
12. El especialista puede consultar reportes o estadísticas.
```

---

## 9. Módulos mínimos para una primera versión

Para una primera versión funcional y realista, se recomienda implementar:

1. Login.
2. Registro de pacientes.
3. Formulario clínico.
4. Carga opcional de radiografía.
5. Predicción con modelo tabular.
6. Predicción con modelo de imagen.
7. Clasificación final integrada.
8. Recomendaciones clínicas auxiliares.
9. Historial de evaluaciones.
10. Dashboard básico.

Con estos módulos, el sistema ya tendría una estructura completa, defendible y alineada con el objetivo principal del proyecto.

---

## 10. Consideraciones clínicas y éticas

Debido a que el sistema trabaja con información clínica pediátrica, es importante considerar lo siguiente:

- La aplicación debe ser presentada como una herramienta auxiliar.
- El sistema no debe reemplazar el juicio clínico del especialista.
- Las recomendaciones no deben mostrarse como órdenes médicas automáticas.
- Los resultados deben interpretarse dentro del contexto clínico completo del paciente.
- Se debe proteger la privacidad de los datos personales y clínicos.
- Se debe mantener trazabilidad de las evaluaciones realizadas.
- Las predicciones deben indicar el nivel de confianza o probabilidad asociada.
- El sistema debe advertir cuando falten datos importantes para una evaluación completa.

Aviso sugerido dentro de la aplicación:

> Este sistema es una herramienta de apoyo clínico. La clasificación de severidad y las recomendaciones generadas son auxiliares y deben ser interpretadas y validadas por el especialista tratante. La aplicación no sustituye el diagnóstico médico ni el juicio clínico profesional.

---

## 11. Nombre del proyecto

**Sistema inteligente de apoyo clínico para la clasificación de severidad en neumonía pediátrica mediante modelos de Machine Learning y Deep Learning**

---

## 12. Resumen ejecutivo

El proyecto propone una aplicación web inteligente para apoyar al especialista en la clasificación de severidad de neumonía pediátrica. El sistema permitirá registrar pacientes, capturar datos clínicos y cargar radiografías de tórax cuando sea necesario. Mediante el uso de un modelo de Machine Learning para datos tabulares y un modelo de Deep Learning para imágenes radiográficas, la aplicación generará una clasificación final auxiliar de severidad considerando ambos enfoques cuando estén disponibles.

Además, el sistema ofrecerá recomendaciones clínicas orientativas, historial de evaluaciones, estadísticas y reportes. Su propósito principal es fortalecer la toma de decisiones clínicas mediante una herramienta tecnológica interpretable, segura y centrada en el apoyo al especialista, sin reemplazar el criterio médico profesional.
