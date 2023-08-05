pydatajson
==========

[![Coverage Status](https://coveralls.io/repos/github/datosgobar/pydatajson/badge.svg?branch=master)](https://coveralls.io/github/datosgobar/pydatajson?branch=master)
[![Build Status](https://travis-ci.org/datosgobar/pydatajson.svg?branch=master)](https://travis-ci.org/datosgobar/pydatajson)
[![PyPI](https://badge.fury.io/py/pydatajson.svg)](http://badge.fury.io/py/pydatajson)
[![Stories in Ready](https://badge.waffle.io/datosgobar/pydatajson.png?label=ready&title=Ready)](https://waffle.io/datosgobar/pydatajson)
[![Documentation Status](http://readthedocs.org/projects/pydatajson/badge/?version=stable)](http://pydatajson.readthedocs.io/es/stable/?badge=stable)

Paquete en python con herramientas para manipular y validar metadatos de catálogos de datos.

* Versión python: 2 y 3
* Licencia: MIT license
* Documentación: [https://pydatajson.readthedocs.io/es/stable](https://pydatajson.readthedocs.io/es/stable)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

## Indice

- [Instalación](#instalaci%C3%B3n)
- [Uso](#uso)
  - [Setup](#setup)
  - [Posibles validaciones de catálogos](#posibles-validaciones-de-cat%C3%A1logos)
  - [Ubicación del catálogo a validar](#ubicaci%C3%B3n-del-cat%C3%A1logo-a-validar)
  - [Ejemplos](#ejemplos)
    - [Archivo data.json local](#archivo-datajson-local)
    - [Archivo data.json remoto](#archivo-datajson-remoto)
    - [Diccionario (data.json deserializado)](#diccionario-datajson-deserializado)
- [Tests](#tests)
- [Créditos](#cr%C3%A9ditos)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Este README cubre los casos de uso más comunes para la librería, junto con ejemplos de código, pero sin mayores explicaciones. Para una versión más detallada de los comportamientos, revise la [documentación oficial](http://pydatajson.readthedocs.io) o el [Manual de Uso](docs/MANUAL.md) de la librería.

## Instalación

* **Producción:** Desde cualquier parte

```bash
$ pip install pydatajson
```

* **Desarrollo:** Clonar este repositorio, y desde su raíz, ejecutar:
```bash
$ pip install -e .
```

A partir de la versión 0.2.x (Febrero 2017), la funcionalidad del paquete se mantendrá fundamentalmente estable hasta futuro aviso. De todas maneras, si piensa utilizar esta librería en producción, le sugerimos fijar la versión que emplea en un archivo `requirements.txt`.

## Usos

La librería cuenta con funciones para cuatro objetivos principales:
- **validación de metadatos de catálogos** y los _datasets_,
- **generación de reportes** sobre el contenido y la validez de los metadatos de catálogos y _datasets_,
- **transformación de archivos de metadatos** al formato estándar (JSON), y
- **generación de indicadores de monitoreo de catálogos** y sus _datasets_.

A continuación se proveen ejemplos de cada uno de estas acciones. Si desea analizar un flujo de trabajo más completo, refiérase a los Jupyter Notebook de [`samples/`](samples/)

### Setup

`DataJson` utiliza un esquema default que cumple con el perfil de metadatos recomendado en la [Guía para el uso y la publicación de metadatos (v0.1)](https://github.com/datosgobar/paquete-apertura-datos/raw/master/docs/Gu%C3%ADa%20para%20el%20uso%20y%20la%20publicaci%C3%B3n%20de%20metadatos%20(v0.1).pdf) del [Paquete de Apertura de Datos](https://github.com/datosgobar/paquete-apertura-datos).

```python
from pydatajson import DataJson

dj = DataJson()
```

Si se desea utilizar un esquema alternativo, por favor, consulte la sección "Uso > Setup" del [manual oficial](docs/MANUAL.md), o la documentación oficial.

### Validación de metadatos de catálogos

- Si se desea un **resultado sencillo (V o F)** sobre la validez de la estructura del catálogo, se utilizará **`is_valid_catalog(catalog)`**.
- Si se desea un **mensaje de error detallado**, se utilizará **`validate_catalog(catalog)`**.

Por conveniencia, la carpeta [`tests/samples/`](tests/samples/) contiene varios ejemplos de `data.json` bien y mal formados con distintos tipos de errores.

#### Archivo data.json local

```python
from pydatajson import DataJson

dj = DataJson()
catalog = "tests/samples/full_data.json"
validation_result = dj.is_valid_catalog(catalog)
validation_report = dj.validate_catalog(catalog)

print validation_result
True

print validation_report
{
    "status": "OK",
    "error": {
        "catalog": {
            "status": "OK",
            "errors": [],
            "title": "Datos Argentina"
        },
        "dataset": [
            {
                "status": "OK",
                "errors": [],
                "title": "Sistema de contrataciones electrónicas"
            }
        ]
    }
}
```

#### Otros formatos

`pydatajson` puede interpretar catálogos tanto en formato JSON como en formato XLSX (siempre y cuando se hayan creado utilizando la [plantilla](samples/plantilla_data.xlsx), estén estos almacenados localmente o remotamente a través de URLs de descarga directa. También es capaz de interpretar diccionarios de Python con metadatos de catálogos.

```python
from pydatajson import DataJson

dj = DataJson()
catalogs = [
    "tests/samples/full_data.json", # archivo JSON local
    "http://181.209.63.71/data.json", # archivo JSON remoto
    "tests/samples/catalogo_justicia.xlsx", # archivo XLSX local
    "https://raw.githubusercontent.com/datosgobar/pydatajson/master/tests/samples/catalogo_justicia.xlsx", # archivo XLSX remoto
    {
        "title": "Catálogo del Portal Nacional",
	"description" "Datasets abiertos para el ciudadano."
        "dataset": [...],
	(...)
    } # diccionario de Python
]

for catalog in catalogs:
    validation_result = dj.is_valid_catalog(catalog)
    validation_report = dj.validate_catalog(catalog)
```

### Generación de reportes y configuraciones del Harvester

Si ya se sabe que se desean cosechar todos los _datasets_ [válidos] de uno o varios catálogos, se pueden utilizar directamente el método `generate_harvester_config()`, proveyendo `harvest='all'` o `harvest='valid'` respectivamente. Si se desea revisar manualmente la lista de _datasets_ contenidos, se puede invocar primero `generate_datasets_report()`, editar el reporte generado y luego proveérselo a `generate_harvester_config()`, junto con la opción `harvest='report'`.

#### Crear un archivo de configuración eligiendo manualmente los datasets a federar

```python
catalogs = ["tests/samples/full_data.json", "http://181.209.63.71/data.json"]
report_path = "path/to/report.xlsx"
dj.generate_datasets_report(
    catalogs=catalogs,
    harvest='none', # El reporte tendrá `harvest==0` para todos los datasets
    export_path=report_path
)

# A continuación, se debe editar el archivo de Excel 'path/to/report.xlsx',
# cambiando a '1' el campo 'harvest' en los datasets que se quieran cosechar.

config_path = 'path/to/config.csv'
dj.generate_harvester_config(
    harvest='report',
    report=report_path,
    export_path=config_path
)
```
El archivo `config_path` puede ser provisto a Harvester para federar los _datasets_ elegidos al editar el reporte intermedio `report_path`.

Por omisión, en la salida de `generate_harvester_config` la frecuencia de actualización deseada para cada _dataset_ será "R/P1D", para intentar cosecharlos diariamente. De preferir otra frecuencia (siempre y cuando sea válida según ISO 8601), se la puede especificar a través del parámetro opcional `frequency`. Si especifica expĺicitamente `frequency=None`, se conservarán las frecuencias de actualización indicadas en el campo `accrualPeriodicity` de cada _dataset_.

#### Crear un archivo de configuración que incluya únicamente los datasets con metadata válida

Conservando las variables anteriores:

```python
dj.generate_harvester_config(
    catalogs=catalogs,
    harvest='valid'
    export_path='path/to/config.csv'
)
```

### Transformación de un archivo de metados XLSX al estándar JSON

```python
from pydatajson.readers import read_catalog
from pydatajson.writers import write_json
from pydatajson import DataJson

dj = DataJson()
catalogo_xlsx = "tests/samples/catalogo_justicia.xlsx"

catalogo = read_catalog(catalogo_xlsx)
write_json(obj=catalogo, path="tests/temp/catalogo_justicia.json")
```

### Generación de indicadores de monitoreo de catálogos

`pydatajson` puede calcular indicadores sobre uno o más catálogos. Estos indicadores recopilan información de interés sobre los _datasets_ de cada uno, tales como:
- el estado de validez de los catálogos;
- el número de días desde su última actualización;
- el formato de sus distribuciones;
- frecuencia de actualización de los _datasets_;
- estado de federación de los _datasets_, comparándolo con el catálogo central

La función usada es `generate_catalogs_indicators`, que acepta los catálogos como parámetros. Devuelve dos valores:
- una lista con tantos valores como catálogos, con cada elemento siendo un diccionario con los indicadores del catálogo respectivo;
- un diccionario con los indicadores de la red entera (una suma de los individuales)

```python
catalogs = ["tests/samples/full_data.json", "http://181.209.63.71/data.json"]
indicators, network_indicators = dj.generate_catalogs_indicators(catalogs)

# Opcionalmente podemos pasar como segundo argumento un catálogo central,
# para poder calcular indicadores sobre la federación de los datasets en 'catalogs'

central_catalog = "http://datos.gob.ar/data.json"
indicators, network_indicators = dj.generate_catalogs_indicators(catalogs, central_catalog)
```

## Tests

Los tests se corren con `nose`. Desde la raíz del repositorio:

**Configuración inicial:**

```bash
$ pip install -r requirements_dev.txt
$ mkdir tests/temp
```

**Correr la suite de tests:**

```bash
$ nosetests
```

## Recursos de interés

* [Estándar ISO 8601 - Wikipedia](https://es.wikipedia.org/wiki/ISO_8601)
* [JSON SChema - Sitio oficial del estándar](http://json-schema.org/)
* [Documentación completa de `pydatajson` - Read the Docs](http://pydatajson.readthedocs.io)
* [Guía para el uso y la publicación de metafatos](https://docs.google.com/document/d/1Z7XhpzOinvITN_9wqUbOYpceDzic3KTOHLtHcGCPAwo/edit)

## Créditos

El validador de archivos `data.json` desarrollado es mayormente un envoltorio (*wrapper*) alrededor de la librería [`jsonschema`](https://github.com/Julian/jsonschema), que implementa el vocabulario definido por [JSONSchema.org](http://json-schema.org/) para anotar y validar archivos JSON.


Versiones
=======

0.3.21 (2017-12-22)
-------------------

* Agrega soporte para Python 3.6

0.3.20 (2017-11-16)
-------------------

* Agrego método `get_theme()` para devolver un tema de la taxonomía específica del catálogo según su `id` o `label`.

0.3.19 (2017-10-31)
-------------------

* Agrego métodos de búsqueda de series de tiempo en un catálogo (`get_time_series()`) y un parámetro `only_time_series=True or False` para filtrar datasets y distribuciones en sus métodos de búsqueda (`get_datasets(only_time_series=True)` devuelve sólo aquellos datasets que tengan alguna serie de tiempo).

0.3.18 (2017-10-19)
-------------------

* Agrego posibilidad de pasar un logger desde afuera a la función de lectura de catálogos en Excel.

0.3.15 (2017-10-09)
-------------------

* Agrega filtro por series de tiempo en `get_datasets()` y `get_distributions()`. Tienen un parámetro `only_time_series` que devuelve sólo aquellos que tengan o sean distribuciones con series de tiempo.

0.3.12 (2017-09-21)
-------------------

* Agrega función para escribir un catálogo en Excel.
* Agrega funciones para remover datasets o distribuciones de un catálogo.

0.3.11 (2017-09-13)
-------------------

* Incorpora parámetro para excluir campos de metadatos en la devolución de la búsqueda de datasets y distribuciones.

0.3.10 (2017-09-11)
-------------------

* Agregar referencia interna a los ids de las entidades padre de otras (distribuciones y fields.)

0.3.9 (2017-09-05)
-------------------

* Flexibiliza lectura de extras en ckan to datajson.
* Flexibiliza longitud mínima de campos para recomendar su federación o no.
* Agrega método para devolver los metadatos a nivel de catálogo.
* Resuelve la escritura de objetos python como texto en excel.

0.3.8 (2017-08-25)
-------------------

* Agrega stop words a `helpers.title_to_name()`

0.3.4 (2017-08-21)
-------------------

* Agrega método para buscar la localización de un `field` en un catálogo.

0.3.3 (2017-08-20)
-------------------

* Agrega método para convertir el título de un dataset o distribución en un nombre normalizado para la creación de URLs.

0.3.2 (2017-08-16)
-------------------

* Amplía reporte de federación en markdown.

0.3.0 (2017-08-14)
-------------------

* Agrega métodos para navegar un catálogo desde el objeto DataJson.

0.2.27 (2017-08-11)
-------------------

* Agrega validacion de que el campo `superTheme` sólo contenga ids en mayúsculas o minúsculas de alguno de los 13 temas de la taxonomía temática de datos.gob.ar.
* Agrega validación limitando a 60 caracteres los nombres de los campos `field_title`.
* Mejoras al reporte de asistencia a la federación.

0.2.26 (2017-08-04)
-------------------

* Agrega validación de que no haya ids repetidos en la lista de temas de `themeTaxonomy`.
* Agrega traducción de ckan del campo extra `Cobertura temporal` a `temporal`.

0.2.24 (2017-08-03)
-------------------
* Mejoras en los reportes de errores y análisis de datasets para federación
* Métodos `DataJson.validate_catalog()` y `DataJson.generate_datasets_report()` tienen nuevas opciones para mejorar los reportes, especialmente en excel.

0.2.23 (2017-08-02)
-------------------

* Bug fixes

0.2.22 (2017-08-02)
-------------------

* Agrega estilo y formato al reporte de datasets
* Agrega nuevos campos al reporte de datasets
* Agrega un campo identificador del catálogo en el archivo de configuración de federación

0.2.21 (2017-08-02)
-------------------

* Tolera el caso de intentar escribir un reporte de datasets sobre un catálogo que no tiene datasets. Loggea un warning en lugar de levantar una excepción.

0.2.20 (2017-08-01)
-------------------

* Elimina la verificación de SSL en las requests de ckan_reader.

0.2.19 (2017-08-01)
-------------------

* Elimina la verificación de SSL en las requests.

0.2.18 (2017-07-25)
-------------------

* Mejora la validación del campo `temporal`
* Agrega formas de reporte de errores para el método `DataJson.validate_catalog()`:
    - Devuelve sólo errores con  `only_errors=True`
    - Devuelve una lista de errores lista para ser convertida en tabla con `fmt="list"`

0.2.17 (2017-07-18)
-------------------

* Agrega un método para convertir un intervalo repetido (Ej.: R/P1Y) en su representación en prosa ("Anualmente").
* Agrego método que estima los datasets federados que fueron borrados de un catálogo específico. Se consideran datasets federados y borrados de un catálogo específico aquellos cuyo publisher.name existe dentro de algún otro dataset todavía presente en el catálogo específico.

0.2.16 (2017-07-13)
-------------------

* Bug fix: convierte a unicode antes de escribir un objeto a JSON.

0.2.15 (2017-07-11)
-------------------

* Modifica la definición de dataset actualizado usando el campo "modified" del perfil de metadatos. Si este campo no está presente en la metadata de un dataset, se lo considera desactualizado.

0.2.14 (2017-07-10)
-------------------

* Modifica la definición de dataset usada para comparar limitándola a la comparación por "title" y "publisher_name".

0.2.13 (2017-06-22)
-------------------

* Agrega método para verificar si un dataset individual está actualizado

0.2.12 (2017-06-22)
-------------------

* Se modifica el template de CATALOG README
* Se agrega el indicador "datasets_no_federados" a generate_catalogs_indicators

0.2.11 (2017-05-23)
-------------------

* Se agrega en `core` el método `DataJson.generate_catalogs_indicators`, que genera indicadores de monitoreo de catálogos, recopilando información sobre, entre otras cosas, su validez, actualidad y formato de sus contenidos.

0.2.10 (2017-05-11)
-------------------

* Correción ortográfica del listado de frecuencias de actualización admisibles (`pydatajson/schemas/accrualPeriodicity.json`).

0.2.9 (2017-05-04)
------------------

* Hotfixes para que `pydatajson` sea deployable en nuevos entornos donde el `setup.py` estaba fallando.

0.2.5 (2017-02-16)
------------------

* Se agrega una nueva función a `readers`, `read_ckan_catalog`, que traduce los metadatos que disponibiliza la Action API v3 de CKAN al estándar `data.json`. Esta función _no_ está integrada a `read_catalog`.

* Se modifican todos los esquemas de validación, de modo que los campos opcionales de cualquier tipo y nivel acepten strings vacías.

0.2.0 (2017-01-31)
------------------

* Se reestructura la librería en 4 módulos: `core`, `readers`, `writers` y `helpers`. Toda la funcionalidad se mantiene intacta, pero algunas funciones muy utilizadas cambian de módulo. En particular, `pydatajson.pydatajson.read_catalog` es ahora `pydatajson.readers.read_catalog`, y `pydatajson.xlsx_to_json.write_json_catalog` es ahora `pydatajson.writers.write_json_catalog` (o `pydatajson.writers.write_json`).

* Se agrega el parámetro `frequency` a `pydatajson.DataJson.generate_harvester_config`, que controla la frecuencia de cosecha que se pretende de los datasets a incluir en el archivo de configuración. Por omisión, se usa `'R/P1D'` (diariamente) para todos los datasets.

* Se agrega la carpeta `samples/`, con dos rutinas de transformación y reporte sobre catálogos de metadatos en formato XLSX.

0.1.7 (2017-01-10)
------------------

* Se agrega el módulo `xlsx_to_json`, con dos métodos para lectura de archivos locales o remotos, sean JSON genéricos (`xlsx_to_json.read_json()`) o metadatos de catálogos en formato XLSX (`read_local_xlsx_catalog()`).
* Se agrega el método `pydatajson.read_catalog()` que interpreta todos las representaciones externas o internas de catálogos conocidas, y devuelve un diccionario con sus metadatos.

0.1.6 (2017-01-04)
------------------

* Se incorpora el método `DataJson.generate_harvestable_catalogs()`, que filtra los datasets no deseados de un conjunto de catálogos.
* Se agrega el parámetro `harvest` a los métodos `DataJson.generate_harvestable_catalogs()`, `DataJson.generate_datasets_report()` y `DataJson.generate_harvester_config()`, para controlar el criterio de elección de los datasets a cosechar.
* Se agrega el parámetro `export_path` a los métodos `DataJson.generate_harvestable_catalogs()`, `DataJson.generate_datasets_report()` y `DataJson.generate_harvester_config()`, para controlar la exportación de sus resultados.

0.1.4 (2016-12-23)
------------------

* Se incorpora el método `DataJson.generate_datasets_report()`, que reporta sobre los datasets y la calidad de calidad de metadatos de un conjunto de catálogos.
* Se incorpora el método `DataJson.generate_harvester_config()`, que crea archivos de configuración para el Harvester a partir de los reportes de `generate_datasets_report()`.

0.1.3 (2016-12-19)
------------------

* Al resultado de `DataJson.validate_catalog()` se le incorpora una lista (`"errors"`) con información de los errores encontrados durante la validación en cada nivel de jerarquía ("catalog" y cada elemento de "dataset")

0.1.2 (2016-12-14)
------------------

* Se incorpora validación de tipo y formato de campo
* Los métodos `DataJson.is_valid_catalog()` y `DataJson.validate_catalog()` ahora aceptan un `dict` además de un `path/to/data.json` o una url a un data.json.

0.1.0 (2016-12-01)
------------------

Primera versión para uso productivo del paquete.

* La instalación via `pip install` debería reconocer correctamente la ubicación de los validadores por default.
* El manejo de data.json's ubicados remotamente se hace en función del resultado de `urlparse.urlparse`
* El formato de respuesta de `validate_catalog` se adecúa a la última especificación (ver [`samples/validate_catalog_returns.json`](samples/validate_catalog_returns.json).

0.0.13 (2016-11-25)
-------------------

* Intentar que la instalación del paquete sepa donde están instalados los schemas por default

0.0.12 (2016-11-25)
-------------------

* Primera versión propuesta para v0.1.0


