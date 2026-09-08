# Contexto general del proyecto

## Nombre del proyecto

**Sistema inteligente de apoyo clínico para la clasificación de severidad en neumonía pediátrica mediante modelos de Machine Learning y Deep Learning**

## Descripción general

El proyecto consiste en una aplicación web clínica orientada a apoyar al especialista en la clasificación de severidad de neumonía pediátrica. La aplicación permitirá registrar pacientes, capturar datos clínicos mediante formularios estructurados y, cuando el especialista lo considere necesario, cargar una radiografía de tórax.

La clasificación final de severidad se generará de forma integrada a partir de dos fuentes principales:

1. **Modelo de Machine Learning tabular**, encargado de analizar variables clínicas del paciente.
2. **Modelo de Deep Learning de imágenes**, encargado de analizar radiografías de tórax cuando estén disponibles.

El sistema mostrará una clasificación auxiliar de severidad, probabilidades asociadas y recomendaciones clínicas orientativas. La aplicación no sustituye el criterio médico ni emite diagnósticos definitivos.

## Objetivo general

Desarrollar una aplicación web de apoyo clínico para la clasificación de severidad en neumonía pediátrica mediante la integración de datos clínicos tabulares y radiografías de tórax, utilizando modelos de Machine Learning y Deep Learning, con el propósito de proporcionar al especialista una herramienta auxiliar para la toma de decisiones clínicas.

## Objetivos específicos

- Permitir el registro e inicio de sesión de usuarios.
- Gestionar usuarios con roles diferenciados.
- Registrar y consultar pacientes pediátricos.
- Capturar datos clínicos relevantes mediante formularios estructurados.
- Permitir la carga opcional de radiografías de tórax.
- Ejecutar predicción con modelo tabular.
- Ejecutar predicción con modelo de imagen cuando exista radiografía.
- Integrar los resultados de ambos modelos para obtener una clasificación final auxiliar.
- Mostrar recomendaciones clínicas orientativas según la severidad.
- Guardar el historial de evaluaciones de cada paciente.
- Consultar estadísticas generales del sistema.
- Generar reportes de evaluaciones.

## Delimitaciones y limitaciones

El sistema:

- No realiza diagnóstico médico definitivo.
- No sustituye el juicio clínico del especialista.
- No prescribe medicamentos de forma automática.
- No reemplaza protocolos institucionales.
- No realiza interpretación radiológica completa.
- No garantiza validez clínica multicéntrica sin validación posterior.
- No integra inicialmente dispositivos médicos externos.
- No integra inicialmente expedientes clínicos hospitalarios.

Las recomendaciones emitidas por el sistema son únicamente auxiliares, orientativas y deben ser validadas por el especialista responsable.

## Roles del sistema

### Administrador

Puede gestionar usuarios, roles básicos, catálogos, configuración y consultar estadísticas generales.

### Especialista/Médico

Puede registrar pacientes, capturar evaluaciones clínicas, cargar radiografías, ejecutar clasificaciones y consultar resultados.

### Consulta/Lectura

Puede visualizar información, pacientes, evaluaciones, reportes y estadísticas, pero no debe crear, modificar ni eliminar registros clínicos.

## Módulos principales

1. Autenticación y seguridad.
2. Gestión de usuarios y roles.
3. Gestión de pacientes.
4. Evaluaciones clínicas tabulares.
5. Carga y análisis de radiografías.
6. Clasificación integrada de severidad.
7. Recomendaciones clínicas auxiliares.
8. Historial de evaluaciones.
9. Dashboard y estadísticas.
10. Reportes.
11. Auditoría y trazabilidad.

## Flujo principal del sistema

1. El usuario inicia sesión.
2. El sistema valida su identidad y rol.
3. El especialista registra o selecciona un paciente.
4. El especialista captura datos clínicos.
5. Opcionalmente carga una radiografía.
6. El sistema ejecuta el modelo tabular.
7. Si existe radiografía, ejecuta el modelo de imagen.
8. El sistema integra los resultados.
9. Se muestra la severidad final sugerida.
10. Se muestran recomendaciones clínicas auxiliares.
11. Se guarda la evaluación en el historial del paciente.
12. La información queda disponible para reportes y estadísticas.
