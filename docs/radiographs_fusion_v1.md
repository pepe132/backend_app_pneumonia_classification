# Radiografías y fusión de resultados v1

## Responsabilidad de cada modelo

- El modelo tabular clasifica severidad: `Bajo`, `Medio` o `Alto`.
- La CNN clasifica la radiografía: `covid_19`, `normal`,
  `pneumonia_bacterial` o `pneumonia_viral`.
- La CNN no fue entrenada para clasificar severidad.

Por esta razón, la severidad final v1 permanece basada en el modelo tabular.
La radiografía agrega evidencia diagnóstica, concordancia y una explicación.

## Reglas de fusión

| Resultado de imagen | Soporte radiográfico | Concordancia | Efecto en severidad |
| --- | --- | --- | --- |
| Sin radiografía | `not_available` | `not_applicable` | Sin cambio |
| Confianza menor a 0.60 | `indeterminate` | `indeterminate` | Sin cambio |
| Neumonía bacteriana o viral | `supports_pneumonia` | `concordant` | Sin cambio |
| Normal | `does_not_support_pneumonia` | `discordant` | Sin cambio |
| COVID-19 | `review_required` | `indeterminate` | Sin cambio |

Una radiografía normal no descarta por sí sola el cuadro clínico y nunca reduce
automáticamente la severidad.

## Endpoints

- `POST /evaluations/{evaluation_id}/radiograph`: carga JPG/PNG, ejecuta la CNN
  y actualiza el resultado integrado.
- `GET /evaluations/{evaluation_id}/radiograph`: consulta el análisis de imagen.
- `GET /evaluations/{evaluation_id}`: consulta severidad tabular y resultado
  integrado persistido.

## Campos preparados para recomendaciones

`recommendation_code` usa uno de estos valores:

- `severity_bajo`
- `severity_medio`
- `severity_alto`

El futuro módulo de recomendaciones podrá resolver ese código a contenido
versionado sin modificar el contrato de evaluación ni las reglas de fusión.
