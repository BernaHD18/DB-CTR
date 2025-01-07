import customtkinter as ctk
from data_manager import DataManager

class App(ctk.CTk):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.title("Gestión de Dispositivos")
        self.geometry("600x400")

        # Crear botones para las opciones
        self.label = ctk.CTkLabel(self, text="Menú Principal", font=("Arial", 20))
        self.label.pack(pady=20)

        self.insert_button = ctk.CTkButton(self, text="Insertar Datos", command=self.open_insert_menu)
        self.insert_button.pack(pady=10)

        self.consult_button = ctk.CTkButton(self, text="Consultar Datos", command=self.open_consult_menu)
        self.consult_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(self, text="Salir", command=self.quit)
        self.exit_button.pack(pady=10)

    def open_insert_menu(self):
        InsertMenu(self, self.data_manager)

    def open_consult_menu(self):
        ConsultMenu(self, self.data_manager)

class InsertMenu(ctk.CTkToplevel):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.title("Menú de Inserción")
        self.geometry("500x300")
        ctk.CTkLabel(self, text="Menú de Inserción de Datos").pack(pady=20)

class ConsultMenu(ctk.CTkToplevel):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.title("Menú de Consultas")
        self.geometry("500x300")
        ctk.CTkLabel(self, text="Menú de Consultas").pack(pady=20)

if __name__ == "__main__":
    # Aquí se conecta el DataManager
    from db_connection import DatabaseConnection
    db = DatabaseConnection("DB-CTR", "postgres", "CTR", "localhost", "5432")
    db.connect()
    data_manager = DataManager(db)

    app = App(data_manager)
    app.mainloop()
    db.close()
