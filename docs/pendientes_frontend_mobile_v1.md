# Pendientes del frontend móvil v1

Fecha de creación: 2026-08-11.

## Objetivo

Desarrollar una aplicación móvil para apoyar el registro de pacientes
pediátricos, evaluaciones clínicas, análisis de radiografías y consulta del
resultado combinado del backend.

El frontend puede comenzar aunque el backend todavía no esté cerrado. Los
contratos actuales se tratarán como provisionales y la lógica clínica seguirá
perteneciendo al backend.

El corte actualizado de módulos, endpoints, pruebas y pendientes del servidor
se encuentra en `docs/seguimiento_implementacion.md`. El detalle de trabajo aún
pendiente se mantiene en `docs/pendientes_backend_v1.md`.

## Stack propuesto

- React Native con Expo y TypeScript.
- Expo Router para navegación.
- TanStack Query para consultas, mutaciones y caché.
- React Hook Form y Zod para formularios.
- Expo SecureStore para almacenar el token.
- Expo ImagePicker para seleccionar radiografías.
- Cliente HTTP centralizado mediante `fetch` o Axios.
- Jest y React Native Testing Library para pruebas.

## Ubicación recomendada

Crear el frontend como proyecto hermano, no dentro de `backend/app`:

```text
todo/
├── backend_app_pneumonia/
└── mobile_app_pneumonia/
```

## Alcance de la primera versión

Flujo principal:

```text
Inicio de sesión
  -> Lista de pacientes
  -> Registro o selección de paciente
  -> Evaluación clínica
  -> Resultado del modelo clínico
  -> Carga de radiografía
  -> Resultado radiográfico y combinado
```

No se implementarán reglas clínicas directamente en el dispositivo. La app
mostrará el resultado y la recomendación que entregue el backend.

## Fase M0 - Contrato y preparación

- [ ] Inventariar los endpoints disponibles del backend.
- [ ] Documentar cuerpos de solicitud, respuestas y códigos HTTP.
- [ ] Clasificar contratos como estables, provisionales o pendientes.
- [ ] Definir los valores permitidos para roles y severidades.
- [ ] Definir el formato común de errores que consumirá la app.
- [ ] Crear `.env.example` móvil con `EXPO_PUBLIC_API_URL`.
- [ ] Confirmar pruebas desde teléfono físico y emulador Android.
- [ ] Configurar FastAPI en la red local sin exponer SQL Server.

## Fase M1 - Base del proyecto

- [ ] Crear el proyecto Expo con TypeScript.
- [ ] Configurar ESLint, Prettier y alias de importación.
- [ ] Crear navegación pública y navegación autenticada.
- [ ] Crear cliente HTTP centralizado.
- [ ] Incorporar TanStack Query.
- [ ] Incorporar React Hook Form y Zod.
- [ ] Definir tema visual, colores, tipografía y componentes básicos.
- [ ] Crear estados reutilizables de carga, vacío y error.
- [ ] Configurar pruebas unitarias y de componentes.

Estructura inicial:

```text
src/
├── api/
├── components/
├── features/
│   ├── auth/
│   ├── patients/
│   ├── evaluations/
│   ├── radiographs/
│   └── decisions/
├── navigation/
├── screens/
├── storage/
└── types/
```

## Fase M2 - Autenticación y sesión

- [ ] Crear pantalla de inicio de sesión.
- [ ] Validar campos y mostrar errores del backend.
- [ ] Guardar el token mediante SecureStore.
- [ ] Restaurar la sesión al abrir la aplicación.
- [ ] Consultar y conservar la información del usuario actual.
- [ ] Cerrar sesión y eliminar credenciales locales.
- [ ] Manejar token vencido y respuestas `401`.
- [ ] Restringir pantallas y acciones según el rol.
- [ ] Probar que el token nunca se muestre en logs.

## Fase M3 - Pacientes

- [ ] Mostrar listado de pacientes activos.
- [ ] Implementar búsqueda por nombre.
- [ ] Crear pantalla de detalle del paciente.
- [ ] Crear formulario de registro.
- [ ] Crear formulario de edición.
- [ ] Validar edad de 0 a 72 meses.
- [ ] Validar sexo, peso, talla y campos obligatorios.
- [ ] Implementar desactivación con confirmación.
- [ ] Restringir acciones según permisos del backend.
- [ ] Manejar listas vacías, carga y errores de conexión.

## Fase M4 - Evaluación clínica

- [ ] Crear formulario con los campos clínicos actuales.
- [ ] Agrupar signos vitales, síntomas, antecedentes y exploración.
- [ ] Usar controles adecuados para valores booleanos y numéricos.
- [ ] Validar rangos antes de enviar sin duplicar reglas médicas.
- [ ] Confirmar al usuario antes de registrar la evaluación.
- [ ] Mostrar la severidad y probabilidades del modelo tabular.
- [ ] Mostrar claramente que el resultado es apoyo y no diagnóstico autónomo.
- [ ] Consultar el historial de evaluaciones del paciente.
- [ ] Evitar envíos duplicados por doble toque o mala conexión.

## Fase M5 - Radiografías

- [ ] Seleccionar una imagen desde el dispositivo.
- [ ] Evaluar posteriormente captura mediante cámara si resulta clínicamente útil.
- [ ] Validar tipo y tamaño antes de cargar.
- [ ] Mostrar vista previa y permitir reemplazar la imagen.
- [ ] Mostrar progreso de carga.
- [ ] Enviar la radiografía como `multipart/form-data`.
- [ ] Manejar una radiografía por evaluación según el contrato actual.
- [ ] Mostrar clase, confianza y probabilidades del modelo CNN.
- [ ] Manejar imagen inválida, modelo no disponible y error de red.
- [ ] Evitar conservar imágenes clínicas innecesarias en caché o galería.

## Fase M6 - Resultado combinado y recomendación

- [ ] Mostrar el resultado clínico y radiográfico por separado.
- [ ] Mostrar severidad final, concordancia y fundamento de fusión.
- [ ] Mostrar el código y texto de recomendación devuelto por el backend.
- [ ] Resaltar signos de alarma de forma accesible y no ambigua.
- [ ] Diseñar el estado de discordancia entre ambos modelos.
- [ ] Mostrar la versión de reglas/modelos cuando el backend la entregue.
- [ ] Mostrar aviso de apoyo a la decisión clínica.
- [ ] Probar escenarios bajo, medio, alto, indeterminado y discordante.

Bloqueado parcialmente hasta validar la matriz clínica y completar la Fase 6
del backend.

## Fase M7 - Experiencia sin conexión y resiliencia

- [ ] Definir con el equipo clínico qué información puede consultarse offline.
- [ ] Detectar ausencia de conexión y mostrar un estado claro.
- [ ] No presentar como enviado un registro que el servidor no confirmó.
- [ ] Definir si habrá cola local de formularios pendientes.
- [ ] Cifrar cualquier dato clínico almacenado localmente.
- [ ] Implementar reintentos sólo para operaciones seguras.
- [ ] Prevenir duplicados mediante identificadores o idempotencia del backend.

Esta fase necesita una decisión explícita de seguridad antes de almacenar datos
de pacientes en el dispositivo.

## Fase M8 - Seguridad y privacidad

- [ ] Usar HTTPS fuera del entorno local.
- [ ] No conectar la aplicación directamente a SQL Server.
- [ ] No guardar contraseñas ni tokens en almacenamiento plano.
- [ ] Ocultar datos sensibles en logs y herramientas de analítica.
- [ ] Definir bloqueo por inactividad o autenticación biométrica si aplica.
- [ ] Revisar permisos de cámara, galería y almacenamiento.
- [ ] Evitar capturas de pantalla en vistas sensibles si el contexto lo exige.
- [ ] Definir aviso de privacidad, consentimiento y retención de datos.
- [ ] Revisar requisitos legales e institucionales antes de uso real.

## Fase M9 - Accesibilidad y usabilidad clínica

- [ ] Diseñar para operación rápida con una mano cuando sea posible.
- [ ] Usar textos legibles, contraste suficiente y áreas táctiles amplias.
- [ ] No depender únicamente del color para comunicar severidad.
- [ ] Añadir etiquetas para lectores de pantalla.
- [ ] Mantener unidades visibles: meses, kg, cm, °C, rpm, lpm y porcentaje.
- [ ] Reducir captura repetida de información.
- [ ] Validar el flujo mediante pruebas con personal clínico.

## Fase M10 - Pruebas y distribución

- [ ] Pruebas unitarias de validadores y transformaciones.
- [ ] Pruebas de componentes para formularios y resultados.
- [ ] Pruebas de integración contra una base exclusiva de pruebas.
- [ ] Pruebas de permisos por rol.
- [ ] Pruebas con red lenta, desconexión y token vencido.
- [ ] Pruebas en diferentes tamaños y versiones de Android.
- [ ] Configurar builds de desarrollo y preview con EAS Build.
- [ ] Separar URLs de desarrollo, pruebas y producción.
- [ ] Preparar icono, splash screen, nombre y versión de la aplicación.
- [ ] Preparar publicación sólo después de validación clínica y de seguridad.

## Dependencias actuales del backend

Se puede desarrollar desde ahora:

- Autenticación y sesión.
- Navegación por rol.
- Pacientes.
- Evaluaciones clínicas y resultado tabular.
- Carga y resultado de radiografía.
- Presentación básica de la fusión.

Debe mantenerse provisional:

- Recomendaciones y mensajes clínicos.
- Reglas de signos de alarma.
- Manejo clínico de discordancias.
- Campos nuevos que solicite la especialista.
- Dashboard, reportes y administración avanzada de usuarios.

## Decisiones pendientes

- [ ] Confirmar que la primera plataforma objetivo será Android.
- [ ] Definir si se probará inicialmente con teléfono físico, emulador o ambos.
- [ ] Elegir biblioteca visual o componentes propios.
- [ ] Definir identidad visual provisional.
- [ ] Decidir si la cámara se permitirá o sólo la selección de archivos.
- [ ] Decidir política de sesión y bloqueo por inactividad.
- [ ] Definir requisitos offline y almacenamiento local.
- [ ] Definir si los usuarios podrán cambiar de servidor de pruebas.

## Criterio de terminado de cada pantalla

Una pantalla se considera terminada cuando:

- Consume el contrato vigente del backend.
- Tiene estados de carga, vacío, éxito y error.
- Valida entradas y evita envíos duplicados.
- Respeta los permisos del usuario.
- No expone información sensible en logs.
- Tiene pruebas proporcionales a su riesgo.
- Funciona en al menos un dispositivo Android objetivo.
- Está registrada como estable o provisional.

## Orden recomendado para comenzar

1. Documentar los contratos actuales del backend.
2. Crear `mobile_app_pneumonia` con Expo y TypeScript.
3. Implementar cliente HTTP, sesión y navegación.
4. Construir login.
5. Construir listado, alta y detalle de pacientes.
6. Construir evaluación clínica.
7. Incorporar radiografías y resultado combinado.
8. Integrar las recomendaciones cuando sean validadas.
