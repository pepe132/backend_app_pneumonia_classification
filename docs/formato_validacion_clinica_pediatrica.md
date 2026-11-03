# Formato de validación clínica pediátrica

## 1. Objetivo

Validar la matriz de reglas clínicas auxiliares de la aplicación para apoyar la
clasificación de severidad en neumonía pediátrica. La herramienta no sustituye
el diagnóstico, tratamiento ni juicio clínico del médico tratante.

Cada revisor debe completar este formato de manera independiente. Las
respuestas se consolidarán posteriormente en una versión aprobada de la matriz.

Documentos revisados:

- `docs/matriz_reglas_clinicas_v1.md`
- `docs/backlog_pruebas_backend.md`, escenarios DE-01 a DE-10

## 2. Datos del revisor

| Campo | Respuesta |
|---|---|
| Nombre completo | |
| Especialidad y subespecialidad | |
| Institución / servicio | |
| Años de experiencia | |
| Cédula o registro profesional (opcional) | |
| Fecha de revisión | |
| Versión revisada | `v1` |

## 3. Criterio de respuesta

Para cada regla seleccionar una opción:

- **Aprobar:** la regla y el resultado son clínicamente aceptables.
- **Aprobar con cambios:** la idea es válida, pero requiere modificar condición,
  umbral, prioridad o texto.
- **Rechazar:** la regla no debe utilizarse en la versión revisada.
- **No puedo evaluar:** requiere información adicional o no corresponde a su
  experiencia.

## 4. Revisión de reglas clínicas

| ID | Regla / condición | Decisión | Cambio o comentario | Fuente / justificación |
|---|---|---|---|---|
| ALARM-001 | SpO₂ < 90% | | | |
| ALARM-002 | Cianosis | | | |
| ALARM-003 | Apnea | | | |
| ALARM-004 | Convulsiones | | | |
| ALARM-005 | Rechazo o incapacidad para alimentarse | | | |
| ALARM-006 | Vomita todo | | | |
| ALARM-007 | Alteración del estado de conciencia / Glasgow | | | |
| ALARM-008 | Dificultad respiratoria severa | | | |
| RESP-001 | Frecuencia respiratoria elevada por edad + tiraje | | | |
| RESP-002 | Quejido espiratorio | | | |
| RESP-003 | Aleteo nasal | | | |
| RESP-004 | Retracción xifoidea | | | |
| SEV-LOW | Severidad tabular baja | | | |
| SEV-MEDIUM | Severidad tabular media | | | |
| SEV-HIGH | Severidad tabular alta | | | |
| XRAY-001 | CNN no disponible | | | |
| XRAY-002 | Confianza radiográfica inferior al umbral | | | |
| XRAY-003 | Radiografía normal | | | |
| XRAY-004 | Neumonía bacteriana o viral | | | |
| XRAY-005 | COVID-19 radiográfico | | | |

## 5. Umbrales respiratorios por edad

Indicar si el umbral es adecuado, requiere cambio o no debe utilizarse.

| Grupo de edad | Umbral propuesto | Decisión | Umbral sugerido / comentario |
|---|---:|---|---|
| Menor de 2 meses | FR ≥ 60 | | |
| 2–11 meses | FR ≥ 50 | | |
| 12–59 meses | FR ≥ 40 | | |
| 60–72 meses | FR ≥ 30 | | |

## 6. Datos clínicos faltantes o ambiguos

| Elemento | ¿Debe agregarse o modificarse? | Propuesta |
|---|---|---|
| Incapacidad para beber o lactar | | |
| Rechazo parcial del alimento | | |
| Glasgow / estado de conciencia | | |
| Estridor en reposo | | |
| Cabeceo respiratorio | | |
| Intensidad del tiraje | | |
| Hidratación y perfusión | | |
| Otro | | |

## 7. Niveles y textos de recomendación

| Código | Texto propuesto | ¿Es adecuado? | Texto sugerido |
|---|---|---|---|
| CARE-FOLLOWUP | Seguimiento y educación sobre signos de alarma | | |
| CARE-REASSESS | Valoración médica y reevaluación según evolución | | |
| CARE-PRIORITY | Valoración médica prioritaria y vigilancia estrecha | | |
| CARE-URGENT | Valoración médica urgente y considerar referencia | | |

Confirmar también:

- [ ] No incluye diagnósticos definitivos.
- [ ] No indica medicamentos, dosis ni duración de tratamientos.
- [ ] No indica hospitalización de forma autónoma.
- [ ] Incluye una nota clara de apoyo a la decisión clínica.

## 8. Precedencia y discordancia

| Pregunta | Respuesta / comentario |
|---|---|
| ¿Una alarma urgente debe prevalecer sobre cualquier severidad tabular? | |
| ¿La severidad tabular alta debe conservarse aunque la radiografía sea normal? | |
| ¿Una radiografía de baja confianza debe modificar la recomendación? | |
| ¿Qué debe mostrarse cuando clínica y radiografía son discordantes? | |
| ¿Qué datos faltantes deben impedir una recomendación normal? | |

## 9. Casos clínicos controlados

Para cada caso indicar la recomendación esperada y las reglas que deberían
activarse. Si la respuesta actual no es adecuada, explicar el cambio.

| Caso | Resultado esperado | Reglas esperadas | ¿Adecuado? | Comentario |
|---|---|---|---|---|
| DE-01: severidad baja sin alarmas | | | | |
| DE-02: severidad media | | | | |
| DE-03: severidad alta | | | | |
| DE-04: SpO₂ < 90% | | | | |
| DE-05: cianosis, apnea o convulsiones | | | | |
| DE-06: Glasgow bajo / alteración de conciencia | | | | |
| DE-07: FR elevada + tiraje | | | | |
| DE-08: radiografía normal con clínica relevante | | | | |
| DE-09: nota de seguridad | | | | |
| DE-10: integración al cargar radiografía | | | | |

## 10. Dictamen del revisor

Seleccionar una opción:

- [ ] Apruebo la matriz sin cambios.
- [ ] Apruebo la matriz con los cambios indicados en este formato.
- [ ] No apruebo la matriz; requiere una nueva revisión.
- [ ] No puedo emitir un dictamen completo con la información disponible.

Observaciones generales:

______________________________________________________________________________

______________________________________________________________________________

Nombre y firma: ____________________________________

Fecha: ____________________

## 11. Uso interno del equipo del proyecto

| Campo | Resultado |
|---|---|
| Revisor identificado | |
| Fecha de recepción | |
| Dictamen consolidado | |
| Cambios aplicados a la matriz | |
| Nueva versión de la matriz | |
| Fecha de aprobación | |
| Responsable técnico | |

No implementar ni presentar las recomendaciones como funcionalidad clínica
aprobada hasta registrar el dictamen y la versión correspondiente de la matriz.
