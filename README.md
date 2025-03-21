🇬🇧 This README is also available in [English](#english_readme) below.

# 🇪🇸 T8Spectrum

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

<a name="english_readme"></a>
# 🇬🇧 T8Spectrum

## Introduction

The objective of this project is to put into practice the skills for developing a "real" application acquired at the beginning of the internship at TWave (version control with Git, project management with Poetry, creating tests, code documentation, etc).

The purpose of this application is to serve as a client to obtain data from the REST API of the T8 devices developed by the company. Specifically, it retrieves data related to waveforms and spectra of the signals stored in it.

## Configuration and Execution

To run this code, you need to have the Poetry tool and install the dependencies with `poetry install`.

Regarding the execution of the application, it is first necessary to specify the host, ID, user, and password of the T8 device you want to connect to in the environment variables of the current shell. Below is an example of the commands to set these environment variables:

```shell
# These data are just examples
export HOST="lzfs45.mirror.twave.io"
export ID="lzfs45"
export T8_USER="user"
export T8_PASSWORD="password"
```

Next, the application can be run in two ways. The first is by activating the virtual environment created by Poetry, which will make the `t8-client` command available. The other way is simply by running `poetry run t8-client` without needing to activate any environment.

To see the available subcommands in the application and a quick guide on how to use them, you can run `t8-client --help` or `poetry run t8-client --help` depending on the chosen option.

## Others

The first task of this project was to implement an application that would obtain a waveform from the API, calculate its spectrum, and compare it with the spectrum also obtained from the T8 API. That initial program has been moved to the `scripts` folder with the name `spectra_comparison.py`. It can be run with the command `spectra-comparison` (or `poetry run spectra-comparison`). However, note that the URL parameters for making requests are fixed in the code, so they would need to be changed first. Also, the T8 user and password must be entered via the keyboard.