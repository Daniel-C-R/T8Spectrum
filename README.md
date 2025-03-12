# T8Spectrum

## Introducción

El objetivo de este proyecto es poner el práctica las habilidades para el desarrollo de una aplicación "real" adquiridas al comienzo de la prácticas en TWave (control de versiones con Git, gestión de proyectos con Poetry, creación de tests, documentación del código, etc).

El ejercicio propuesto consiste en obtener la forma de onda y el espectro de una señal almacenada en un dispositivo T8 (los equipos que desarrolla la empresa) por medio de su API REST. Posteriormente, a partir del *waveform* se calculará su espectro y se comparará con el obtenido de la API para comprobar que los cálculos son correctos.

## Configuración

Para poder ejecutar este código, se requiere disponer de la herramienta Poetry e instalar las dependencias con `poetry install`.

También, es necesario crear un archivo `.env` en el que se guarden el usuario y contraseña del equipo T8. Este archivo nunca debe ser versionado. Se ha incluido una plantilla de cómo debe ser este archivo en `.env.example`. De todas formas se incluye la estructura de este archivo a continuación:

```shell
T8_USER=
T8_PASSWORD=
```

En estos momentos, al comienzo del archivo `t8spectrum/main.py` se definen como constantes los parámetros de las URLs a consular. Estos son la dirección del equipo T8 y su identificador, y la máquina, punto, modo de procesamiento e instante de tiempo a consultar. Para poder lanzar las peticiones a otro equipo T8 sería necesario modificar el código.

## Ejecución

El código se puede ejecuar de dos formas, una de ellas sería ejecutando simplemente `poetry run python t8spectrum/main.py`, o activando el entorno virtual y ejecutando el script:

```shell
poetry env activate
python t8spectrum/main.py
```
