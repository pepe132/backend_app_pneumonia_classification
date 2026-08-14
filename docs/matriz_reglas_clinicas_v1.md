# Matriz de reglas clínicas auxiliares v1

Estado: borrador para validación médica.

Fecha: 2026-08-09.

## Advertencia

Este documento no constituye una guía médica ni autoriza por sí mismo el uso
clínico de las reglas. Es una especificación técnica preliminar para traducir
recomendaciones publicadas a una capa de apoyo explicable.

Antes de desplegar estas reglas deben revisarlas y aprobarlas profesionales de
pediatría o medicina responsables del proyecto. La aplicación no debe indicar
diagnósticos definitivos, prescribir medicamentos ni sustituir el juicio
clínico.

## Alcance propuesto

- Contexto principal: México.
- Población almacenada por la aplicación: 0 a 72 meses, que corresponde al
  rango de entrenamiento confirmado del modelo tabular.
- Atención: apoyo para valoración inicial, priorización, reevaluación y
  referencia.
- Fuera de alcance en v1: selección de antibiótico, dosis, duración del
  tratamiento y decisión autónoma de hospitalización.
- La severidad tabular y el hallazgo radiográfico deben mostrarse separados de
  la recomendación de atención.

## Fuentes normativas candidatas

| Código | Fuente | Alcance | Uso propuesto |
| --- | --- | --- | --- |
| MX-GPC-2021 | [CENETEC GPC-SS-120-21: neumonía bacteriana adquirida en la comunidad en menores de 18 años](https://www.cenetec-difusion.com/CMGPC/GPC-SS-120-21/ER.pdf) | Menores de 18 años, México | Fuente nacional principal |
| MX-RR-2021 | [Referencia rápida CENETEC GPC-SS-120-21](https://www.cenetec-difusion.com/CMGPC/GPC-SS-120-21/RR.pdf) | Características de enfermedad severa | Criterios de alarma y referencia |
| WHO-PNEU-2024 | [OMS: manejo de neumonía y diarrea en menores de hasta 10 años](https://www.who.int/publications/i/item/9789240103412) | Niños de hasta 10 años; algunas recomendaciones se restringen a 2–59 meses | Complemento internacional actualizado |
| WHO-ETAT | [OMS: triaje, evaluación y tratamiento pediátrico de emergencia](https://www.who.int/publications/i/item/9789241510219) | Paciente pediátrico críticamente enfermo | Hipoxemia y signos de emergencia |

La versión, vigencia y aplicabilidad institucional de estas fuentes debe
confirmarse antes de aprobar la matriz.

## Separación de responsabilidades

| Componente | Pregunta que responde | No debe hacer |
| --- | --- | --- |
| Modelo tabular | ¿Qué severidad estima a partir de los datos clínicos? | Prescribir o diagnosticar de forma definitiva |
| CNN | ¿Qué patrón reconoce en la radiografía? | Clasificar severidad clínica |
| Fusión | ¿La imagen apoya, contradice o no permite concluir sobre el cuadro? | Sumar probabilidades de tareas diferentes |
| Reglas clínicas | ¿Qué nivel de atención auxiliar sugieren los signos y resultados? | Reemplazar la valoración médica |

## Niveles de recomendación propuestos

| Código | Etiqueta | Acción textual permitida |
| --- | --- | --- |
| CARE-FOLLOWUP | Seguimiento | Seguimiento y educación sobre signos de alarma |
| CARE-REASSESS | Reevaluación | Valoración médica y reevaluación según evolución |
| CARE-PRIORITY | Valoración prioritaria | Valoración médica prioritaria y vigilancia estrecha |
| CARE-URGENT | Valoración urgente | Valoración médica urgente y considerar referencia según criterio clínico |

Estos niveles no equivalen automáticamente a tratamiento ambulatorio,
hospitalización, antibiótico u oxígeno.

## Reglas candidatas de seguridad

| ID | Condición computable | Resultado propuesto | Sustento | Estado |
| --- | --- | --- | --- | --- |
| ALARM-001 | `spo2 < 90` | `CARE-URGENT` | CENETEC incluye saturación menor a 90% entre características de NAC severa; OMS ETAT aborda hipoxemia | Respaldada, requiere validación local |
| ALARM-002 | `cianosis = true` | `CARE-URGENT` | Signo de hipoxemia/enfermedad severa en referencias OMS | Respaldada, requiere validación local |
| ALARM-003 | `apnea = true` | `CARE-URGENT` | Signo de compromiso respiratorio crítico | Requiere localizar cita exacta y aprobación médica |
| ALARM-004 | `convulsiones = true` | `CARE-URGENT` | Signo general de peligro OMS | Respaldada |
| ALARM-005 | `rechazo_comer = true` | Al menos `CARE-PRIORITY`; elevar a urgente según definición clínica | CENETEC incluye incapacidad para alimentación oral; OMS incluye incapacidad para beber o lactar | El campo actual no distingue rechazo parcial de incapacidad total |
| ALARM-006 | `vomita_todo = true` | `CARE-URGENT` | Signo general de peligro OMS | Respaldada |
| ALARM-007 | Alteración del estado de conciencia | `CARE-URGENT` | CENETEC: letargo o disminución del estado de conciencia; OMS: letargo/inconsciencia | Falta acordar el umbral de Glasgow; no asumir automáticamente `<14` |
| ALARM-008 | Dificultad respiratoria severa | `CARE-URGENT` | CENETEC: dificultad respiratoria, tiraje y quejido; OMS: distrés respiratorio severo | Falta una definición computable aprobada |

## Reglas respiratorias por edad

La OMS utiliza, para parte de su clasificación en menores de cinco años,
umbrales de respiración rápida dependientes de edad. El código actual usa:

| Edad | Umbral actual de FR elevada | Estado |
| --- | --- | --- |
| Menor de 2 meses | `fr >= 60` | Requiere fuente y protocolo específico para lactante pequeño |
| 2 a 11 meses | `fr >= 50` | Compatible con criterios OMS usados habitualmente |
| 12 a 59 meses | `fr >= 40` | Compatible con criterios OMS usados habitualmente |
| 60 a 72 meses | `fr >= 30` | Requiere validación clínica; no extrapolar automáticamente la regla de menores de cinco años |

Regla candidata actual:

| ID | Condición | Resultado | Estado |
| --- | --- | --- | --- |
| RESP-001 | FR elevada por edad y `tiraje = true` | `CARE-URGENT` | Adaptación conservadora existente; requiere aprobación médica explícita |
| RESP-002 | `quejido_espiratorio = true` | Al menos `CARE-PRIORITY` | CENETEC lo incluye entre características severas; confirmar si siempre debe ser urgente |
| RESP-003 | `aleteo_nasal = true` | Hallazgo relevante; elevar según combinación | OMS 2024 lo considera en evaluación de distrés cuando no hay oximetría; aquí sí existe SpO₂ |
| RESP-004 | `retraccion_xifoidea = true` | Hallazgo relevante; elevar según combinación | Requiere equivalencia clínica validada con tiraje/retracción severa |

## Uso de la severidad tabular

| ID | Condición | Resultado base | Regla de seguridad |
| --- | --- | --- | --- |
| SEV-LOW | `severity_tabular = Bajo` | `CARE-FOLLOWUP` | Cualquier alarma puede elevar la recomendación |
| SEV-MEDIUM | `severity_tabular = Medio` | `CARE-REASSESS` o `CARE-PRIORITY` | Definir con especialista cuál texto corresponde |
| SEV-HIGH | `severity_tabular = Alto` | `CARE-URGENT` | Nunca reducir por resultado radiográfico |

La probabilidad del modelo debe mostrarse, pero no se utilizará como dosis ni
como porcentaje de certeza diagnóstica.

## Uso de la CNN y fusión

| ID | Condición | Efecto permitido |
| --- | --- | --- |
| XRAY-001 | CNN no disponible | Continuar con clínica y declarar imagen no disponible |
| XRAY-002 | Confianza inferior al umbral técnico | Marcar resultado `indeterminate`; no cambiar severidad |
| XRAY-003 | `normal` con confianza suficiente | Registrar que no apoya neumonía; no reducir severidad ni cancelar alarmas |
| XRAY-004 | `pneumonia_bacterial` o `pneumonia_viral` con confianza suficiente | Registrar soporte radiográfico; correlación médica |
| XRAY-005 | `covid_19` con confianza suficiente | Marcar revisión específica; no convertirlo en diagnóstico definitivo |

El umbral CNN actual de 0.60 es una decisión técnica, no una recomendación de
guía clínica. Debe justificarse con validación del modelo, calibración y métricas
por clase antes de producción.

## Precedencia propuesta

1. Si existe una regla `CARE-URGENT`, la recomendación final es urgente.
2. En ausencia de alarma, se utiliza el nivel base de la severidad tabular.
3. La CNN agrega soporte, discordancia o indeterminación, pero no reduce el
   nivel clínico.
4. Si faltan datos críticos, no se genera una recomendación normal; se devuelve
   `insufficient_data`.
5. La respuesta siempre enumera las reglas activadas y su versión.

## Contrato sugerido

```json
{
  "clinical_severity": "Medio",
  "radiographic_finding": "pneumonia_viral",
  "radiographic_support": "indeterminate",
  "care_level": "CARE-URGENT",
  "triggered_rules": [
    "RESP-001"
  ],
  "recommendation_version": "MX-GPC-WHO-draft-1",
  "recommendation_text": "Valoración médica urgente.",
  "safety_note": "Resultado auxiliar que no sustituye el juicio médico."
}
```

## Campos clínicos faltantes o ambiguos

| Elemento de guía | Campo actual | Acción requerida |
| --- | --- | --- |
| Incapacidad para beber o lactar | `rechazo_comer` | Separar rechazo parcial de incapacidad total |
| Letargo o inconsciencia | `glasgow` | Definir equivalencia validada; considerar campo explícito |
| Estridor en reposo | No existe | Evaluar agregarlo |
| Cabeceo respiratorio | No existe | Evaluar agregarlo |
| Tiraje intercostal/severo | `tiraje`, `retraccion_xifoidea` | Definir intensidad y equivalencias |
| Estado de hidratación/perfusión | No existe | Determinar si forma parte del alcance |
| FR para 60 a 72 meses | Existe FR y edad | Seleccionar umbrales pediátricos aprobados |

## Caso ficticio actual

Datos relevantes:

- 36 meses.
- FR 50.
- SpO₂ 91%.
- Tiraje y retracción xifoidea.
- Fiebre, aleteo nasal, rechazo al alimento, sibilancias, crepitantes y
  dificultad respiratoria persistente.
- Severidad tabular `Medio`.
- CNN `pneumonia_viral` con confianza 0.527403, inferior al umbral 0.60.

Resultado técnico actual:

- Severidad final: `Medio`.
- Evidencia radiográfica: `indeterminate`.
- La regla existente FR elevada más tiraje produce recomendación urgente.

Decisión pendiente: un médico debe confirmar que `RESP-001` y el texto urgente
son apropiados para este contexto y grupo etario.

## Checklist de aprobación médica

- [ ] Confirmar población y nivel de atención.
- [ ] Definir reglas clínicas específicas para 0 a 59 días, aunque el modelo
  tabular sí fue entrenado en ese rango.
- [ ] Confirmar definición de cada signo de alarma.
- [ ] Confirmar umbrales de FR para todos los grupos de edad.
- [ ] Confirmar umbral y uso de Glasgow.
- [ ] Diferenciar rechazo alimentario de incapacidad para vía oral.
- [ ] Confirmar los cuatro niveles de atención y sus textos.
- [ ] Confirmar que no se incluyan fármacos ni dosis en v1.
- [ ] Aprobar reglas de precedencia.
- [ ] Aprobar el manejo de discordancia clínica-radiografía.
- [ ] Registrar nombre, rol, fecha y versión del revisor clínico.

## Plan técnico después de la aprobación

1. Convertir cada regla aprobada en una función pequeña con ID estable.
2. Devolver `triggered_rules` y `recommendation_version` en la API.
3. Guardar un snapshot de la recomendación y su versión en cada evaluación.
4. Crear pruebas unitarias por regla y pruebas de combinaciones conflictivas.
5. Mantener las probabilidades de ML y CNN separadas.
6. Bloquear el despliegue clínico si la matriz no tiene aprobación registrada.
