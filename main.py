import ctypes
import logging
import traceback
from db_connection import DatabaseConnection
from data_manager import DataManager
from table_manager import TableManager
from menu import MainMenu
from gui import App

# Configuración de loggin
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)

# Configuración de la conexión
db = DatabaseConnection(
    dbname="DB-CTR",
    user="postgres",
    password="CTR",
    host="localhost",
    port="5432"
)

try:
    db.connect()
    # Creación de tablas
    table_manager = TableManager(db)
    #table_manager.drop_tables()
    #table_manager.create_tables()
    #table_manager.alter_tables()

    # Inicialización de la aplicación
    data_manager = DataManager(db)
    #menu = MainMenu(data_manager)
    #menu.show_menu()

    # Cambiar el icono en la barra de tareas
    myappid = 'mycompany.myproduct.subproduct.version'  # Arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Creación y uso de la interfaz gráfica
    app = App(data_manager)
    app.iconbitmap('icono.ico')
    app.mainloop()

except ValueError as ve:
    logging.error(f"Error de validación: {ve}")
    print(f"Error de validación: {ve}")
except Exception as e:
    logging.error(f"Error en la aplicación: {e}\n{traceback.format_exc()}")
    print(f"Error en la aplicación: {e}\n{traceback.format_exc()}")


finally:
    db.close()
 