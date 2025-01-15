# Gestión de Base de Datos

## Descripción General

**Nombre del Proyecto**: Gestión de Base de Datos CTR

**Descripción**: Esta aplicación permite gestionar una base de datos para la empresa CTR. Dentro de esta se puede manejar información sobre empresas, ubicaciones, pontones, dispositivos y sus históricos de movimientos. La interfaz gráfica está construida con Tkinter y se conecta a una base de datos PostgreSQL.

## Requisitos

- Python 3.x
- PostgreSQL
- Bibliotecas de Python:
  - `tkinter`
  - `psycopg2`
  - `ctypes`
  - `logging`
  - `tkcalendar`
  - 

## Configuración inicial

Antes de abrir la aplicación, es necesario realizar una configuración previa para conectarse correctamente a la base de datos. Siga los siguientes pasos:

**- Abrir el archivo de configuración:**

Localice el archivo llamado config.txt dentro del repositorio.

Ábralo con cualquier editor de texto de su preferencia (por ejemplo, Notepad, Visual Studio Code, etc.).

**- Configurar los datos de la base de datos:**

En el archivo config.txt, ingrese los datos correspondientes a la base de datos que desea utilizar.

Estos datos incluyen información como el host, el puerto, el nombre de la base de datos, el usuario y la contraseña.

**- Guardar y cerrar el archivo:**

Una vez que haya completado los datos, guarde el archivo y ciérrelo.

**- Ejecutar la aplicación:**

Después de configurar el archivo, podrá iniciar la aplicación normalmente haciendo doble clic en el archivo main.exe.

## Estructura del repositorio

Este repositorio contiene todo lo necesario para ejecutar y modificar la aplicación:

**- Archivo ejecutable:**

El archivo main.exe permite ejecutar la aplicación sin necesidad de configuraciones adicionales.

**- Dependencias:**

Todas las dependencias necesarias para la ejecución están incluidas en este repositorio.

**- Código fuente:**

El código fuente está disponible para que pueda modificar la aplicación según sus necesidades.

## Explicación de la aplicación

Esta aplicación consta de 6 pestañas principales para la gestión de diferentes datos:

**1. Empresas**

Permite gestionar las empresas.

Puede agregar y eliminar empresas desde esta pestaña.

**2. Ubicaciones**

Se gestionan los centros con los siguientes datos:

Nombre del centro.

Grupo de Telegram asociado.

Empresa vinculada.

Puede agregar y eliminar ubicaciones desde esta pestaña.

**3. Pontones**

Contiene información relacionada a los pontones, como:

Código naval.

Ubicación actual.

Puede agregar y eliminar ubicaciones desde esta pestaña.

**4. Dispositivos**

Administra los datos de los dispositivos, incluyendo:

Tipos de dispositivos (NIO, RADAR, ASISTENTE VIRTUAL, CÁMARA).

Pontones a los que están vinculados.

Puede agregar y eliminar dispositivos desde esta pestaña.

**5. Historial de Movimientos**

Almacena los cambios de ubicación de los pontones hacia otros centros, incluyendo la fecha del cambio.

**6. Historial de Dispositivos**

Registra cualquier cambio de dispositivos entre diferentes pontones, almacenando la fecha del movimiento.

Con esta aplicación, podrá gestionar de manera eficiente las empresas, ubicaciones, pontones, dispositivos y sus respectivos historiales. 
