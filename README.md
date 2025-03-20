# T8Spectrum

## Introducción

El objetivo de este proyecto es poner el práctica las habilidades para el desarrollo de una aplicación "real" adquiridas al comienzo de la prácticas en TWave (control de versiones con Git, gestión de proyectos con Poetry, creación de tests, documentación del código, etc).

La finalidad de esta aplicación es servir como cliente para obtener datos de la API REST de los dispositivos T8 que desarrolla la empresa. Concretamente, obtienen datos relativos a las formas de onda y espectros de las señales almacenadas en este.

## Configuración y ejecución

Para poder ejecutar este código, se requiere disponer de la herramienta Poetry e instalar las dependencias con `poetry install`.

Respecto a la ejecución de la aplicación, primero es necesario especificar en las variables de entorno del shell actual el host, ID, usuario y contraseña del dispositivo T8 al que se dese conectar. A continuación se muestra un ejemplo de los comandos a ejecutar para asignar dichas variables de entorno:

```shell
# Estos datos son sólo de ejemplo
export HOST="lzfs45.mirror.twave.io"
export ID="lzfs45"
export T8_USER="user"
export T8_PASSWORD="password"
```

A continuación, la aplicación se puede ejecutar de dos formas. La primera de ellas es activando el entorno virtual que crea poetry, que podrá disponible el comando `t8-client`. La otra forma es simplemente ejecutando `poetry run t8-client` sin necesidad de activas ningún entorno.

Para ver los subcomandos disponibles en la aplicación y una guía rápida de cómo utilizarlos se puede ejecutar `t8-client --help` o `poetry run t8-client --help` dependiendo de la opción que sa haya elegido.

## Otros

La primera tarea de este proyecto era implementar una aplicación que obtuviese una forma de onda desde la API, calculase su espectro y lo comparase con el espectro que se obtiene también desde la API del T8. Ese programa que se hizo en un principio ha sido movido a la carpeta `scripts` con el nombre `spectra_comparison.py`. Puede ser ejecutado con el comando `spectra-comparison` (o `poetry run spectra-comparison`). Eso sí, hay que tener en cuenta que los parámetros de las URLs a lanzar las peticiones están fijados en el código, por lo que sería necesario cambiarlos primero. También, el usuario y contraseña del T8 deben ser pasados por teclado.