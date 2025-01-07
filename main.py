from db_connection import DatabaseConnection
from data_manager import DataManager
from menu import MainMenu

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
    data_manager = DataManager(db)
    menu = MainMenu(data_manager)
    menu.show_menu()
finally:
    db.close()