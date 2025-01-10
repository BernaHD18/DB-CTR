from db_connection import DatabaseConnection
from data_manager import DataManager
from table_manager import TableManager
from menu import MainMenu
#from gui import App

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
    menu = MainMenu(data_manager)
    menu.show_menu()

    # Creación y uso de la interfaz gráfica
    #app = App(data_manager)
    #app.mainloop()
finally:
    db.close()

