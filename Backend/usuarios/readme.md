# Microservice - Usuarios

Este microservicio corresponden a la gestión de usuarios, el cual permite la creación, actualización y autenticación de usuarios. Además, permite la consulta de información del usuario y el reseteo de la base de datos.

## Índice

1. [Estructura](#estructura)
2. [Ejecución](#ejecución)
3. [Uso](#uso)
4. [Pruebas](#pruebas)
5. [Otras características](#otras-características)
6. [Autor](#autor)

## Estructura

Describe la estructura de archivos de la carpeta, puedes usar una estructura de arbol para ello:

```bash
usuarios/
│
├── src/
│   ├── blueprints/
│   ├── commands/
│   ├── db/
│   ├── errors/
│   ├── models/
│   ├── utils/
│   ├── __init__.py
│   └── main.py
│
├── tests/
│   ├── blueprints/
│   ├── commands/
│   ├── __init__.py
│   └── conftest.py
│
├── scripts/
│
├── .env
├── .env.template
├── .env.test
├── Dockerfile
├── Pipfile
├── Pipfile.lock
├── pytest.ini
├── readme.md
└── requirements.txt
```

- src/: Esta es la carpeta principal que contiene el código fuente del microservicio.

  - blueprints/: Aquí se almacenan los blueprints de Flask, que permiten modularizar la aplicación en componentes o módulos independientes, facilitando la organización y escalabilidad del código.

  - commands/: Contiene scripts o comandos personalizados que se pueden ejecutar desde la línea de comandos, por ejemplo, para tareas de mantenimiento, migraciones de base de datos, etc.

  - db/: Se utiliza para definir y gestionar la base de datos. Aquí podrían estar los archivos de configuración de la base de datos, migraciones, y cualquier otro relacionado con el manejo de los datos.

  - errors/: Esta carpeta gestiona los errores y excepciones personalizados que puede generar la aplicación. Es útil para centralizar la gestión de errores y mejorar el manejo de respuestas de error.

  - models/: Aquí se encuentran las definiciones de los modelos de datos, que representan las tablas de la base de datos en la aplicación. Cada modelo define la estructura y las relaciones de los datos que maneja el microservicio.

  - utils/: Contiene utilidades y funciones auxiliares que son utilizadas en diferentes partes del código. Estos pueden incluir funciones comunes que no pertenecen a un módulo específico.

  - __init__.py: Este archivo indica que el directorio es un paquete de Python. Suele incluir código de inicialización que se ejecuta al importar el paquete.

  - main.py: Es el punto de entrada principal de la aplicación. Aquí se configura e inicia el servidor Flask y se conectan los diferentes componentes del microservicio.

- tests/: Esta carpeta contiene todos los tests que se utilizan para validar el correcto funcionamiento del microservicio.

  - blueprints/: Contiene los tests específicos para los blueprints definidos en src/blueprints/.

  - commands/: Contiene los tests específicos para los comandos definidos en src/commands/.

  - __init__.py: Similar al archivo en src/, indica que la carpeta tests/ es un paquete de Python.

  - conftest.py: Archivo de configuración para pytest que permite definir fixtures y configuraciones comunes para todos los tests.

- scripts/: Contiene scripts que permiten llenar la base de datos con pruebas

- .env: Archivo que contiene variables de entorno para la configuración de la aplicación en un entorno específico (desarrollo, producción, etc.).

- .env.template: Un archivo de plantilla que sirve como ejemplo de las variables de entorno que deben definirse en .env. Este archivo generalmente se distribuye con el código fuente.

- .env.test: Archivo de variables de entorno específico para el entorno de testing.

- Dockerfile: Archivo que define cómo se debe construir la imagen Docker del microservicio. Contiene instrucciones sobre cómo instalar dependencias, copiar archivos y configurar el entorno dentro del contenedor.

- Pipfile: Archivo de configuración para el gestor de paquetes pipenv. Define las dependencias de la aplicación.

- Pipfile.lock: Archivo generado automáticamente por pipenv que asegura que todas las instalaciones de paquetes sean reproducibles, bloqueando las versiones exactas de las dependencias.

- pytest.ini: Archivo de configuración para pytest, que permite definir opciones de configuración para la ejecución de los tests.

- readme.md: Documento donde se proporciona información sobre el proyecto, cómo configurarlo, ejecutarlo, y cualquier otra información relevante para los desarrolladores o usuarios.

- requirements.txt: Archivo tradicional de Python que lista las dependencias del proyecto. Se puede utilizar en lugar de o junto con Pipfile.

## Ejecución

Este proyecto hace uso de pipenv para gestionar las dependencias y el entorno de desarrollo. Para configurar el entorno de desarrollo se debe ejecutar el siguiente comando:

- Activar el entorno virtual

```bash
pipenv shell
```

- Instalar dependencias del proyecto

```bash
pipenv install
```

> Este comando instalará las dependencias del proyecto que se encuentran definidas en el archivo Pipfile

- Ejecutar el proyecto - En modo desarrollo

> Para Windows

```bash
$env:FLASK_APP = "./src/main.py"
flask run --debug -p 3000
```

- Mediante Pipenv

```bash
$env:FLASK_APP = "./src/main.py"
pipenv run flask run --debug -p 3000
```

> Para macOs y Linux

```bash
export FLASK_APP="./src/main.py"
flask run --debug -p 3001
```

> Si quiere conectarse a un cliente de base de datos, la base de datos de este microservicio se encuentra en el puerto 5430 (usando el servicio de docker). Sin embargo para facilidad de desarrollo se recomienda instalar Postgres directamente en la maquina local, corriendo en el puerto por defecto 5432

## Uso

Este proyecto consta se las siguientes Apis

- [POST] /usuarios -> Crear un usuario
- [PATCH] /usuarios/:id -> Actualizar un usuario
- [POST] /usuarios/auth -> Autenticar un usuario (Genera un token)
- [GET] /usuarios/me  -> Consultar Información del usuario - Este servirá para validar el token desde los otros micros
- [GET] /usuarios/ping -> Ping para validar que el microservicio está funcionando correctamente
- [POST] /usuarios/reset -> Resetear el contenido de la base de datos

Esto se hace mediante la ruta o url `http://localhost:3000/`

## Pruebas

Este proyecto hace uso de pytest para la ejecución de pruebas. Para ejecutar las pruebas se debe ejecutar el siguiente comando:

> Recuerde estar ubicado en el directorio de este microservicio `usuarios/`

```bash
pytest
```

Para ejecutar las pruebas con cobertura de por lo menos el  70% se debe ejecutar el siguiente comando:

```bash
pytest --cov=src -v -s --cov-fail-under=70
```

Para Generar informe de cobertura se debe ejecutar el siguiente comando:

```bash
 pytest --cov=src --cov-report=term --cov-report=html --cov-fail-under=70 -v -s
```

## Otras Características (opcional)

### Ejecutar Proyecto desde Compose

Para ejecutar el proyecto desde docker-compose se debe ejecutar el siguiente comando:

- Construir el proyecto

```bash
docker-compose build
```

- Ejecutar solo el microservicio de usuarios - y base de datos

> Solo se ejecuta el microservicio de usuarios, ya que este depende de la base de datos, y por ende se ejecuta también

```bash
docker-compose up -d usuarios
```

> No es necesario especificar las variables de entorno, ya que estas se encuentran en la definición del archivo docker-compose.yml

## Autor

- Nombre: [Oscar Andrés García](https://github.com/oagarcia)
