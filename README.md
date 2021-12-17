# Expectedscore Scraper
**python version: 3.9**

Extraer información de [expectedscore.com](https://expectedscore.com/) y guardarla en una hoja de cálculo de Excel.
El programa requiere inicio de sesión para poder visualizar los datos.

## Flujo del programa 

1. Iniciar sesión sesión en la página.
2. Obtener los partidos mediante paginación (12 a la vez).
3. Extraer la informaicón de los partidos (estadisticas de equipo local y visitante).
4. Formatear la información.
5. Guardar la informaicón resultante en una hoja de cálculo de excel. 
6. Solicitar al usuario si desea continuar con los siguientes 12 partidos o detener el programa.

## Prompt

Para el **paso 6** del **flujo del programa**, en la terminal se muestra un mensaje como: 

```bash
continue? _
```

Cualquier texto de entrada (como "sí", "yes", "s", o solamente la tecla *enter*), se considera como *sí* a excepción de la palabra "no" (en caso de ingresar esa palabra, el programa se detendrá).


# Instalación
## Instalar módulos de terceros

Instale los módulos necesarios mediante pip: 

``` bash
$ pip install -r requirements.txt
```

## Programas

Para ejecutar el proyecto, los siguientes programas deben estar instalados

* [Google Chrome](https://www.google.com/intl/es/chrome) última versión

# Ejecutar el programa

Para iniciar el programa, ejecuta el archivo __ main__.py o la carpeta del proyecto con tu interprete de python 3.9 

#  Configuraciones

Todas las configuraciones se encuentran en el archivo config.json

```json
{
    "user": "email@gmail.com",
    "password": "mypass"
}
```

## user

Usuario para la página [expectedscore.com](https://expectedscore.com/)

## password

Contraseña de usuario para la página [expectedscore.com](https://expectedscore.com/)

# Datos de salida

La información del web scraping se deposita en el archivo **output.xlsx**, en la hoja **data**.
Cada vez que se ejecuta el programa, la informaicón del documento se sobreescribe, por lo que, es remondable hacer un respaldo antes de iniciar y ejecutar el programa con la hoja **data** sin filas (unicamente con las nombres de las columnas, pero sin registros)

**Nota:** durante la ejecución del programa (el proceso de web scraping), es importante **NO tener abierto** el archvo de excel, ya que puede provocar un conflicto de escritura.