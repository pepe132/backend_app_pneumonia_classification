# Módulos detallados de la aplicación

## 1. Módulo de autenticación

### Función

Gestionar acceso seguro al sistema.

### Entidades

- Users.
- Roles.

### Endpoints

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

### Reglas

- No guardar contraseñas en texto plano.
- Usar JWT.
- Validar usuario activo.
- No permitir creación pública de administradores.

## 2. Módulo de roles

### Función

Controlar permisos de acceso.

### Roles

- Administrador.
- Especialista/Médico.
- Consulta/Lectura.

### Reglas

- Usar `require_roles`.
- No necesariamente requiere CRUD al inicio.
- Puede crecer después a permisos más detallados.

## 3. Módulo de pacientes

### Función

Gestionar pacientes pediátricos.

### Datos sugeridos

- patient_id.
- full_name o identificador.
- age_months (edad en meses cumplidos, de 0 a 72).
- sex.
- weight.
- height.
- guardian_name.
- created_at.
- updated_at.
- active.

### Endpoints

- Crear paciente.
- Listar pacientes.
- Buscar paciente.
- Ver detalle.
- Editar paciente.
- Baja lógica.

## 4. Módulo de evaluaciones

### Función

Registrar datos clínicos para clasificación.

### Datos sugeridos

edad_meses
peso_kg
fr
fc
temperatura_c
spo2
tiraje
aleteo_nasal
quejido_espiratorio
cianosis
apnea
rechazo_comer
vomita_todo
convulsiones
glasgow
desnutricion
antecedentes_cronicos
sibilancias
dias_sintomas
dias_fiebre
dias_tos
dias_dificultad_respiratoria
crepitantes
disminucion_murmullo_vesicular
dolor_toracico

## 5. Módulo de modelo tabular

### Función

Clasificar severidad con variables clínicas.

### Entrada

Datos de evaluación clínica.

### Salida

- severity_class.
- probability_low.
- probability_medium.
- probability_high.

## 6. Módulo de radiografías

### Función

Cargar y asociar imágenes al paciente/evaluación.

### Datos sugeridos

- image_id.
- patient_id.
- evaluation_id.
- file_path.
- original_filename.
- content_type.
- uploaded_by.
- created_at.

## 7. Módulo de modelo de imagen

### Función

Clasificar radiografía mediante Deep Learning.

### Salida sugerida

- image_class.
- probability_normal.
- probability_bacterial.
- probability_viral.
- probability_covid.
- model_version.

## 8. Módulo de integración de resultados

### Función

Combinar modelo tabular e imagen.

### Reglas sugeridas

- Si solo existe tabular, usar clasificación tabular.
- Si existe imagen, mostrar ambos resultados.
- Calcular severidad final según lógica definida.
- Mostrar advertencia cuando falten datos o imagen.
- Guardar resultado final.

## 9. Módulo de recomendaciones

### Función

Generar orientación clínica auxiliar.

### Severidad baja

- Seguimiento según criterio médico.
- Vigilancia de signos de alarma.
- Educación al cuidador.

### Severidad media

- Considerar observación.
- Monitorización de signos vitales.
- Evaluar oxigenoterapia según saturación.
- Revaloración periódica.

### Severidad alta

- Valoración urgente.
- Monitorización continua.
- Considerar soporte ventilatorio.
- Activar protocolos institucionales.
- Considerar referencia si se requiere.

## 10. Módulo de historial

### Función

Consultar evaluaciones previas del paciente.

### Funciones

- Ver evolución.
- Comparar severidades.
- Consultar radiografías.
- Consultar recomendaciones previas.

## 11. Módulo de dashboard

### Función

Mostrar métricas generales.

### Indicadores

- Total pacientes.
- Total evaluaciones.
- Severidad baja/media/alta.
- Casos con radiografía.
- Resultados por fecha.
- Distribución por edad.

## 12. Módulo de reportes

### Función

Generar documentos consultables.

### Reportes

- Reporte de paciente.
- Reporte de evaluación.
- Reporte estadístico.
- Reporte de predicción.

## 13. Módulo de auditoría

### Función

Registrar acciones importantes.

### Eventos

- Login.
- Registro de usuario.
- Creación/edición de paciente.
- Creación de evaluación.
- Predicción ejecutada.
- Radiografía cargada.
- Reporte generado.
