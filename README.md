# Observatorio de Obras Públicas · Pacífico caucano

[![Actualizar dashboard](https://github.com/jerson0915/observatorio-obras-pacifico/actions/workflows/actualizar.yml/badge.svg)](https://github.com/jerson0915/observatorio-obras-pacifico/actions/workflows/actualizar.yml)

**¿Cuánto se invierte en obra pública en Guapi, Timbiquí y López de Micay?**

Dashboard interactivo con todos los contratos de obra que las entidades de los tres municipios de la costa del Cauca (Colombia) publicaron en SECOP I y SECOP II entre 2022 y 2026.

🔗 **Ver el dashboard:** `https://jerson0915.github.io/observatorio-obras-pacifico/`

## Qué muestra

- Inversión total del Pacífico caucano, por municipio y **por habitante** (con la población oficial del DANE).
- Línea de tiempo de la inversión por municipio.
- Mapa satelital con los límites de cada municipio.
- Un resumen de hallazgos arriba, que se reescribe con cada actualización.
- **Obras adjudicadas sin contrato publicado**: procesos que SECOP I marca como adjudicados pero sin contrato, comparados con lo firmado.
- Modalidad de contratación (mínima cuantía, licitación, contratación directa...) y concentración de contratistas.
- Filtros por municipio, contratista, tipo de obra, modalidad, año, estado (en ejecución, terminada, plazo vencido) y alertas.
- Alertas automáticas: obras repetidas que podrían ser un contrato partido en varios, valores atípicos y procesos sin contrato.
- Tabla de los 357 contratos con ficha de cada uno, enlace a SECOP y descarga en CSV. Las tablas completas están en [`docs/datos/`](docs/datos/).

## Hallazgos principales

| Municipio | Inversión 2022–2026 | % del total | Por habitante |
|---|---|---|---|
| López de Micay | $71.912 millones | 61,9 % | $3,67 millones |
| Guapi | $28.104 millones | 24,2 % | $956.000 |
| Timbiquí | $16.124 millones | 13,9 % | $552.000 |
| **Total** | **$116.140 millones** | | **$1,48 millones** |

- **Timbiquí adjudicó 52 obras por $31.177 millones sin publicar nunca el contrato en SECOP**: 1,9 veces lo que sí tiene firmado. Su inversión real probablemente es bastante mayor, y la comparación por habitante con los otros dos municipios está sesgada por eso. López de Micay tiene 47 procesos así ($21.027 millones) y Guapi 11 ($3.510 millones).
- En López de Micay se firmaron **51 obras parecidas de quebradas y ríos en 2022**, cada una por unos $30 millones y todas con los mismos dos contratistas.
- **253 de los 357 contratos (71 %) son de mínima cuantía**, la modalidad con menos competencia, aunque suman solo el 7 % del valor.
- Un solo contrato, el hospital de López de Micay ($42.374 millones, 2026), es el 36 % de todo lo contratado.
- **214 contratos** tienen la fecha de fin vencida y no figuran liquidados en SECOP. Eso no quiere decir que estén abandonados: muchas entidades no registran la liquidación.

## Actualización automática

El dashboard se actualiza **solo, todos los lunes a las 6:00 a. m.** (hora de Colombia). GitHub Actions ejecuta los tres notebooks, guarda los datos nuevos de SECOP en el repositorio y vuelve a publicar la página. La fecha de corte que muestra el dashboard es la de la última actualización.

Antes de guardar, `validar.py` revisa los datos: si el número de contratos cae más de 10 % frente a la versión anterior, si aparecen valores negativos o vacíos, o si una fuente o un municipio queda sin contratos, la ejecución falla, no se publica nada y GitHub avisa por correo.

Para actualizar a mano: pestaña **Actions** → **Actualizar dashboard** → **Run workflow**.

## Cómo está hecho

| Paso | Notebook | Qué hace |
|---|---|---|
| 1 | `01_extraccion.ipynb` | Descarga los contratos de obra de SECOP I y II con la API de datos.gov.co y los une sin duplicados. También trae los procesos adjudicados sin contrato publicado. |
| 2 | `02_limpieza.ipynb` | Quita lo que no es obra (prestaciones de servicios, interventorías; quedan en `datos/excluidos.csv`), corrige el municipio de la obra, une los nombres repetidos de contratistas, clasifica por sector y modalidad y marca alertas. |
| 3 | `03_dashboard.ipynb` | Calcula la inversión por habitante, escribe los hallazgos, descarga los límites y genera `docs/index.html`. |
| — | `validar.py` | Revisa los datos antes de publicarlos. |

**Herramientas:** Python, pandas, DuckDB (SQL), API Socrata de datos.gov.co, Leaflet, HTML, CSS, JavaScript y GitHub Actions.

## Cómo reproducirlo

```bash
pip install -r requirements.txt
```

Ejecuta los tres notebooks en orden. Para analizar otra región, cambia la celda de configuración de `01_extraccion.ipynb`.

## Fuentes

- Contratos: [SECOP II](https://www.datos.gov.co/resource/jbjy-vk9h) y [SECOP I](https://www.datos.gov.co/resource/f789-7hwg), Colombia Compra Eficiente.
- Población: [DANE, proyecciones municipales 2018–2042](https://www.dane.gov.co/index.php/estadisticas-por-tema/demografia-y-poblacion/proyecciones-de-poblacion).
- Límites municipales: © colaboradores de OpenStreetMap.
- Imágenes satelitales: Esri, Maxar, Earthstar Geographics.

## Límites

Estas alcaldías publican casi todo en SECOP I; en SECOP II solo aparecen algunos contratos de las E.S.E. de salud. Los procesos adjudicados sin contrato publicado no se suman a la inversión, porque no se sabe si el contrato se firmó ni por cuánto. El mapa ubica cada contrato en la cabecera de su municipio porque SECOP no publica coordenadas de las obras. La inversión es el valor firmado, no lo pagado. Las alertas son reglas automáticas y no prueban irregularidades: cada caso debe revisarse en SECOP.

---

Proyecto de Jerson Sinisterra.
