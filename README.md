# Observatorio de Obras Públicas · Pacífico caucano

[![Actualizar dashboard](https://github.com/jerson0915/observatorio-obras-pacifico/actions/workflows/actualizar.yml/badge.svg)](https://github.com/jerson0915/observatorio-obras-pacifico/actions/workflows/actualizar.yml)

**¿Cuánto se invierte en obra pública en Guapi, Timbiquí y López de Micay?**

Dashboard interactivo con todos los contratos de obra que las entidades de los tres municipios de la costa del Cauca (Colombia) publicaron en SECOP I y SECOP II entre 2022 y 2026.

🔗 **Ver el dashboard:** `https://jerson0915.github.io/observatorio-obras-pacifico/`

## Qué muestra

- Inversión total del Pacífico caucano, por municipio y **por habitante** (con la población oficial del DANE).
- Línea de tiempo de la inversión por municipio.
- Mapa satelital con los límites de cada municipio.
- Filtros por municipio, contratista, tipo de obra, año, estado (en ejecución, terminada, plazo vencido) y alertas.
- Alertas automáticas: obras repetidas que podrían ser un contrato partido en varios, valores atípicos y procesos sin contrato.
- Tabla de los 363 contratos con enlace a cada uno en SECOP.

## Hallazgos principales

| Municipio | Inversión 2022–2026 | % del total | Por habitante |
|---|---|---|---|
| López de Micay | $73.718 millones | 62,5 % | $3,76 millones |
| Guapi | $28.112 millones | 23,8 % | $956.000 |
| Timbiquí | $16.124 millones | 13,7 % | $552.000 |
| **Total** | **$117.954 millones** | | **$1,5 millones** |

- En López de Micay se firmaron **57 contratos de limpieza de quebradas en 2022 y 42 en 2023**, cada uno por unos $30 millones y casi todos con los mismos dos contratistas.
- **219 contratos** tienen la fecha de fin vencida y no figuran liquidados en SECOP.
- Un solo contrato, el hospital de López de Micay ($42.374 millones, 2026), explica la mayor parte del salto de inversión de 2026.

## Actualización automática

El dashboard se actualiza **solo, todos los lunes a las 6:00 a. m.** (hora de Colombia). GitHub Actions ejecuta los tres notebooks, guarda los datos nuevos de SECOP en el repositorio y vuelve a publicar la página. La fecha de corte que muestra el dashboard es la de la última actualización.

Para actualizar a mano: pestaña **Actions** → **Actualizar dashboard** → **Run workflow**.

## Cómo está hecho

| Paso | Notebook | Qué hace |
|---|---|---|
| 1 | `01_extraccion.ipynb` | Descarga los contratos de obra de SECOP I y II con la API de datos.gov.co y los une sin duplicados. |
| 2 | `02_limpieza.ipynb` | Corrige el municipio de la obra, une los nombres repetidos de contratistas, clasifica por sector y marca alertas. |
| 3 | `03_dashboard.ipynb` | Calcula la inversión por habitante, descarga límites e imágenes satelitales y genera `docs/index.html`. |

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

El mapa ubica cada contrato en la cabecera de su municipio porque SECOP no publica coordenadas de las obras. La inversión es el valor firmado, no lo pagado. Las alertas son reglas automáticas y no prueban irregularidades: cada caso debe revisarse en SECOP.

---

Proyecto de Jerson Sinisterra.
