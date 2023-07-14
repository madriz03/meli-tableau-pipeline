# Meli API to Tableau Hyper

Este proyecto utiliza la API de Mercado Libre (Meli) para consultar información de productos basado en un término de búsqueda y crea un archivo Hyper de Tableau para su posterior análisis y visualización.

## Requisitos

- Python 3.7 o superior
- Paquetes de Python (se pueden instalar con `pip`):
  - requests
  - tableauhyperapi

## Instalación

1. Clona o descarga este repositorio en tu máquina local.
2. Asegúrate de tener Python 3.7 o superior instalado en tu sistema.
3. Instala los paquetes de Python requeridos ejecutando el siguiente comando en tu terminal: pip freeze > requirements.txt


## Uso

1. Abre el archivo `main.py` en tu editor de código.
2. Ejecuta el archivo `main.py` en tu terminal:


3. Se te solicitará ingresar el término de búsqueda. Introduce el término de búsqueda y presiona Enter.
4. El programa consultará la API de Meli, obtendrá los datos de los productos y creará un archivo Hyper con la estructura de tabla especificada y los datos recuperados.
5. El archivo Hyper resultante se guardará en la ruta del proyecto.

## Estructura del proyecto

- `main.py`: Contiene el código principal del programa, incluyendo la consulta a la API, creación del archivo Hyper y carga de datos en la tabla.
- `validations.py`: Contiene funciones para validar la entrada del usuario.
- `settings.py`: Contiene configuraciones y variables globales del proyecto.
- `test.py`: Archivo de pruebas con casos de prueba utilizando pytest.
- `requeriments.txt`: Archivo que contiene las dependencias del proyecto.
- `public_data_meli.hyper`: Archivo Hyper resultante.

## Contribución

Si deseas contribuir a este proyecto, siéntete libre de enviar pull requests o abrir issues para discutir nuevas características, mejoras o soluciones a problemas existentes.

## Autor

Javier Madriz

