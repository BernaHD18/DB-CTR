import tkinter as tk
from tkinter import ttk, messagebox
from data_manager import DataManager

class App(tk.Tk):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.title("Gestión de Base de Datos")
        self.geometry("800x600")

        # Cambiar el icono de la ventana
        self.iconbitmap('icono.ico')

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.apply_styles()
        self.create_menu()
        self.create_tab_empresas()
        self.create_tab_ubicaciones()
        self.create_tab_pontones()
        self.create_tab_dispositivos()
        self.create_tab_historico_movimientos()
        self.create_tab_historico_dispositivos()

    def apply_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')  # Puedes cambiar a 'alt', 'default', 'classic', etc.
        style.configure('TButton', font=('Helvetica', 12))
        style.configure('TLabel', font=('Helvetica', 12))
        style.configure('TEntry', font=('Helvetica', 12))

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Salir", command=self.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.show_about)

    def show_about(self):
        messagebox.showinfo("Acerca de", "Gestión de Base de Datos\nVersión 1.0")

    def create_tab_empresas(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Empresas")

        form_frame = ttk.LabelFrame(tab, text="Agregar Empresa")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_empresa_var = tk.StringVar()
        nombre_entry = ttk.Entry(form_frame, textvariable=self.nombre_empresa_var)
        nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        add_button = ttk.Button(form_frame, text="Agregar", command=self.add_empresa)
        add_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.empresa_tree = ttk.Treeview(tab, columns=("Nombre"), show="headings")
        self.empresa_tree.heading("Nombre", text="Nombre de Empresa")
        self.empresa_tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.refresh_empresa_list()

    def refresh_empresa_list(self):
        for item in self.empresa_tree.get_children():
            self.empresa_tree.delete(item)
        empresas = self.data_manager.consultar_empresas()
        for empresa in empresas:
            self.empresa_tree.insert("", "end", values=(empresa[0],))

    def add_empresa(self):
        nombre = self.nombre_empresa_var.get()
        if nombre:
            self.data_manager.insert_empresa(nombre)
            self.refresh_empresa_list()
        else:
            messagebox.showerror("Error", "El nombre de la empresa no puede estar vacío")

    def create_tab_ubicaciones(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Ubicaciones")

        form_frame = ttk.LabelFrame(tab, text="Agregar Ubicación")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="Nombre del Centro:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_centro_var = tk.StringVar()
        nombre_centro_entry = ttk.Entry(form_frame, textvariable=self.nombre_centro_var)
        nombre_centro_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Grupo de Telegram:").grid(row=1, column=0, padx=5, pady=5)
        self.grupo_telegram_var = tk.StringVar()
        grupo_telegram_entry = ttk.Entry(form_frame, textvariable=self.grupo_telegram_var)
        grupo_telegram_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Nombre de la Empresa:").grid(row=2, column=0, padx=5, pady=5)
        self.nombre_empresa_ubicacion_var = tk.StringVar()
        nombre_empresa_ubicacion_entry = ttk.Entry(form_frame, textvariable=self.nombre_empresa_ubicacion_var)
        nombre_empresa_ubicacion_entry.grid(row=2, column=1, padx=5, pady=5)

        add_button = ttk.Button(form_frame, text="Agregar", command=self.add_ubicacion)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.ubicacion_tree = ttk.Treeview(tab, columns=("Nombre del Centro", "Grupo de Telegram", "Nombre de la Empresa"), show="headings")
        self.ubicacion_tree.heading("Nombre del Centro", text="Nombre del Centro")
        self.ubicacion_tree.heading("Grupo de Telegram", text="Grupo de Telegram")
        self.ubicacion_tree.heading("Nombre de la Empresa", text="Nombre de la Empresa")
        self.ubicacion_tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.refresh_ubicacion_list()

    def refresh_ubicacion_list(self):
        for item in self.ubicacion_tree.get_children():
            self.ubicacion_tree.delete(item)
        ubicaciones = self.data_manager.consultar_ubicaciones()
        for ubicacion in ubicaciones:
            self.ubicacion_tree.insert("", "end", values=(ubicacion[0], ubicacion[1], ubicacion[2]))

    def add_ubicacion(self):
        nombre_centro = self.nombre_centro_var.get()
        grupo_telegram = self.grupo_telegram_var.get()
        nombre_empresa = self.nombre_empresa_ubicacion_var.get()
        if nombre_centro and grupo_telegram and nombre_empresa:
            self.data_manager.insert_ubicacion(nombre_centro, grupo_telegram, nombre_empresa)
            self.refresh_ubicacion_list()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def create_tab_pontones(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Pontones")

        form_frame = ttk.LabelFrame(tab, text="Agregar Pontón")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="Código Naval:").grid(row=0, column=0, padx=5, pady=5)
        self.codigo_naval_var = tk.StringVar()
        codigo_naval_entry = ttk.Entry(form_frame, textvariable=self.codigo_naval_var)
        codigo_naval_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Nombre del Centro:").grid(row=1, column=0, padx=5, pady=5)
        self.nombre_centro_ponton_var = tk.StringVar()
        nombre_centro_ponton_entry = ttk.Entry(form_frame, textvariable=self.nombre_centro_ponton_var)
        nombre_centro_ponton_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Estado:").grid(row=2, column=0, padx=5, pady=5)
        self.estado_var = tk.StringVar()
        estado_entry = ttk.Entry(form_frame, textvariable=self.estado_var)
        estado_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="IA:").grid(row=3, column=0, padx=5, pady=5)
        self.ia_var = tk.StringVar()
        ia_entry = ttk.Entry(form_frame, textvariable=self.ia_var)
        ia_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Observaciones:").grid(row=4, column=0, padx=5, pady=5)
        self.observaciones_var = tk.StringVar()
        observaciones_entry = ttk.Entry(form_frame, textvariable=self.observaciones_var)
        observaciones_entry.grid(row=4, column=1, padx=5, pady=5)

        add_button = ttk.Button(form_frame, text="Agregar", command=self.add_ponton)
        add_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.ponton_tree = ttk.Treeview(tab, columns=("Código Naval", "Nombre del Centro", "Estado", "IA", "Observaciones"), show="headings")
        self.ponton_tree.heading("Código Naval", text="Código Naval")
        self.ponton_tree.heading("Nombre del Centro", text="Nombre del Centro")
        self.ponton_tree.heading("Estado", text="Estado")
        self.ponton_tree.heading("IA", text="IA")
        self.ponton_tree.heading("Observaciones", text="Observaciones")
        self.ponton_tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.refresh_ponton_list()

    def refresh_ponton_list(self):
        for item in self.ponton_tree.get_children():
            self.ponton_tree.delete(item)
        pontones = self.data_manager.consultar_pontones()
        for ponton in pontones:
            estado = "Activo" if ponton[2] else "Inactivo"
            self.ponton_tree.insert("", "end", values=(ponton[0], ponton[1], estado, ponton[3], ponton[4]))

    def add_ponton(self):
        codigo_naval = self.codigo_naval_var.get()
        nombre_centro = self.nombre_centro_ponton_var.get()
        estado = self.estado_var.get().lower() == "true"
        ia = self.ia_var.get()
        observaciones = self.observaciones_var.get()
        if codigo_naval and nombre_centro and ia:
            self.data_manager.insert_ponton(codigo_naval, nombre_centro, estado, ia, observaciones)
            self.refresh_ponton_list()
        else:
            messagebox.showerror("Error", "Los campos Código Naval, Nombre del Centro y IA son obligatorios")

    def create_tab_dispositivos(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Dispositivos")

        form_frame = ttk.LabelFrame(tab, text="Agregar Dispositivo")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="Serial:").grid(row=0, column=0, padx=5, pady=5)
        self.serial_var = tk.StringVar()
        serial_entry = ttk.Entry(form_frame, textvariable=self.serial_var)
        serial_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Dirección IP:").grid(row=1, column=0, padx=5, pady=5)
        self.direccionamiento_ip_var = tk.StringVar()
        direccionamiento_ip_entry = ttk.Entry(form_frame, textvariable=self.direccionamiento_ip_var)
        direccionamiento_ip_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Versión del Firmware:").grid(row=2, column=0, padx=5, pady=5)
        self.firmware_version_var = tk.StringVar()
        firmware_version_entry = ttk.Entry(form_frame, textvariable=self.firmware_version_var)
        firmware_version_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Usuario:").grid(row=3, column=0, padx=5, pady=5)
        self.usuario_var = tk.StringVar()
        usuario_entry = ttk.Entry(form_frame, textvariable=self.usuario_var)
        usuario_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Contraseña:").grid(row=4, column=0, padx=5, pady=5)
        self.contrasena_var = tk.StringVar()
        contrasena_entry = ttk.Entry(form_frame, textvariable=self.contrasena_var)
        contrasena_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Tipo de Dispositivo:").grid(row=5, column=0, padx=5, pady=5)
        self.tipo_dispositivo_var = tk.StringVar()
        tipo_dispositivo_combobox = ttk.Combobox(form_frame, textvariable=self.tipo_dispositivo_var, values=["NIO", "Radar", "Asistente Virtual", "Cámara"])
        tipo_dispositivo_combobox.grid(row=5, column=1, padx=5, pady=5)
        tipo_dispositivo_combobox.bind("<<ComboboxSelected>>", self.on_tipo_dispositivo_selected)

        self.extra_frame = ttk.Frame(form_frame)
        self.extra_frame.grid(row=6, column=0, columnspan=2, pady=10)

        ttk.Label(form_frame, text="Código Naval del Pontón:").grid(row=7, column=0, padx=5, pady=5)
        self.codigo_naval_ponton_var = tk.StringVar()
        self.codigo_naval_ponton_combobox = ttk.Combobox(form_frame, textvariable=self.codigo_naval_ponton_var)
        self.codigo_naval_ponton_combobox.grid(row=7, column=1, padx=5, pady=5)
        self.refresh_codigo_naval_ponton_combobox()

        add_button = ttk.Button(form_frame, text="Agregar", command=self.add_dispositivo)
        add_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.dispositivo_tree = ttk.Treeview(tab, columns=("Serial", "Dirección IP", "Firmware", "ID Credenciales", "Tipo"), show="headings")
        self.dispositivo_tree.heading("Serial", text="Serial")
        self.dispositivo_tree.heading("Dirección IP", text="Dirección IP")
        self.dispositivo_tree.heading("Firmware", text="Firmware")
        self.dispositivo_tree.heading("ID Credenciales", text="ID Credenciales")
        self.dispositivo_tree.heading("Tipo", text="Tipo")
        self.dispositivo_tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.refresh_dispositivo_list()

    def on_tipo_dispositivo_selected(self, event):
        for widget in self.extra_frame.winfo_children():
            widget.destroy()

        tipo_dispositivo = self.tipo_dispositivo_var.get()
        if tipo_dispositivo == "Radar":
            ttk.Label(self.extra_frame, text="Canal RF:").grid(row=0, column=0, padx=5, pady=5)
            self.canal_rf_var = tk.StringVar()
            canal_rf_entry = ttk.Entry(self.extra_frame, textvariable=self.canal_rf_var)
            canal_rf_entry.grid(row=0, column=1, padx=5, pady=5)
        elif tipo_dispositivo == "NIO":
            ttk.Label(self.extra_frame, text="Modelo:").grid(row=0, column=0, padx=5, pady=5)
            self.modelo_var = tk.StringVar()
            modelo_combobox = ttk.Combobox(self.extra_frame, textvariable=self.modelo_var, values=["NIO-DIN", "NIO-App"])
            modelo_combobox.grid(row=0, column=1, padx=5, pady=5)

    def refresh_dispositivo_list(self):
        for item in self.dispositivo_tree.get_children():
            self.dispositivo_tree.delete(item)
        dispositivos = self.data_manager.consultar_dispositivos()
        for dispositivo in dispositivos:
            self.dispositivo_tree.insert("", "end", values=(dispositivo['Serial'], dispositivo['Dirección IP'], dispositivo['Firmware'], dispositivo['ID Credenciales'], dispositivo['Tipo']))

    def refresh_codigo_naval_ponton_combobox(self):
        pontones = self.data_manager.consultar_pontones()
        codigo_navales = [ponton[0] for ponton in pontones]
        self.codigo_naval_ponton_combobox['values'] = codigo_navales

    def add_dispositivo(self):
        serial = self.serial_var.get()
        direccionamiento_ip = self.direccionamiento_ip_var.get()
        firmware_version = self.firmware_version_var.get()
        usuario = self.usuario_var.get()
        contrasena = self.contrasena_var.get()
        tipo_dispositivo = self.tipo_dispositivo_var.get()
        codigo_naval_ponton = self.codigo_naval_ponton_var.get()
        if serial and direccionamiento_ip and firmware_version and usuario and contrasena and tipo_dispositivo and codigo_naval_ponton:
            if tipo_dispositivo == "NIO":
                modelo = self.modelo_var.get()
                self.data_manager.insert_nio(serial, modelo, direccionamiento_ip, firmware_version, usuario, contrasena)
            elif tipo_dispositivo == "Radar":
                canal_rf = self.canal_rf_var.get()
                self.data_manager.insert_radar(serial, canal_rf, direccionamiento_ip, firmware_version, usuario, contrasena)
            elif tipo_dispositivo == "Asistente Virtual":
                self.data_manager.insert_asistente_virtual(serial, direccionamiento_ip, firmware_version, usuario, contrasena)
            elif tipo_dispositivo == "Cámara":
                self.data_manager.insert_camara(serial, direccionamiento_ip, firmware_version, usuario, contrasena)
            self.data_manager.insert_dispositivo_ponton(codigo_naval_ponton, serial, tipo_dispositivo)
            self.refresh_dispositivo_list()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def create_tab_historico(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Histórico")

        form_frame = ttk.LabelFrame(tab, text="Agregar Histórico de Movimientos")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="Código Naval:").grid(row=0, column=0, padx=5, pady=5)
        self.codigo_naval_historico_var = tk.StringVar()
        codigo_naval_historico_entry = ttk.Entry(form_frame, textvariable=self.codigo_naval_historico_var)
        codigo_naval_historico_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="ID Centro Anterior:").grid(row=1, column=0, padx=5, pady=5)
        self.id_centro_anterior_var = tk.StringVar()
        id_centro_anterior_entry = ttk.Entry(form_frame, textvariable=self.id_centro_anterior_var)
        id_centro_anterior_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="ID Centro Nuevo:").grid(row=2, column=0, padx=5, pady=5)
        self.id_centro_nuevo_var = tk.StringVar()
        id_centro_nuevo_entry = ttk.Entry(form_frame, textvariable=self.id_centro_nuevo_var)
        id_centro_nuevo_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Fecha de Instalación (DD-MM-YYYY):").grid(row=3, column=0, padx=5, pady=5)
        self.fecha_instalacion_var = tk.StringVar()
        fecha_instalacion_entry = ttk.Entry(form_frame, textvariable=self.fecha_instalacion_var)
        fecha_instalacion_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Fecha de Término (DD-MM-YYYY):").grid(row=4, column=0, padx=5, pady=5)
        self.fecha_termino_var = tk.StringVar()
        fecha_termino_entry = ttk.Entry(form_frame, textvariable=self.fecha_termino_var)
        fecha_termino_entry.grid(row=4, column=1, padx=5, pady=5)

        add_button = ttk.Button(form_frame, text="Agregar", command=self.add_historico_movimientos)
        add_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.historico_tree = ttk.Treeview(tab, columns=("ID Movimiento", "Código Naval", "ID Centro Anterior", "ID Centro Nuevo", "Fecha de Instalación", "Fecha de Término"), show="headings")
        self.historico_tree.heading("ID Movimiento", text="ID Movimiento")
        self.historico_tree.heading("Código Naval", text="Código Naval")
        self.historico_tree.heading("ID Centro Anterior", text="ID Centro Anterior")
        self.historico_tree.heading("ID Centro Nuevo", text="ID Centro Nuevo")
        self.historico_tree.heading("Fecha de Instalación", text="Fecha de Instalación")
        self.historico_tree.heading("Fecha de Término", text="Fecha de Término")
        self.historico_tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.refresh_historico_list()

    def refresh_historico_list(self):
        for item in self.historico_tree.get_children():
            self.historico_tree.delete(item)
        movimientos = self.data_manager.consultar_historico_movimientos()
        for movimiento in movimientos:
            fecha_instalacion = movimiento[4].strftime("%d-%m-%Y") if movimiento[4] else "N/A"
            fecha_termino = movimiento[5].strftime("%d-%m-%Y") if movimiento[5] else "N/A"
            self.historico_tree.insert("", "end", values=(movimiento[0], movimiento[1], movimiento[2], movimiento[3], fecha_instalacion, fecha_termino))

    def add_historico_movimientos(self):
        codigo_naval = self.codigo_naval_historico_var.get()
        id_centro_anterior = self.id_centro_anterior_var.get()
        id_centro_nuevo = self.id_centro_nuevo_var.get()
        fecha_instalacion = self.fecha_instalacion_var.get()
        fecha_termino = self.fecha_termino_var.get()
        if codigo_naval and id_centro_anterior and id_centro_nuevo and fecha_instalacion and fecha_termino:
            self.data_manager.insert_historico_movimientos(codigo_naval, id_centro_anterior, id_centro_nuevo, fecha_instalacion, fecha_termino)
            self.refresh_historico_list()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def create_tab_historico_movimientos(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Histórico Movimientos")

        form_frame = ttk.LabelFrame(tab, text="Agregar Histórico de Movimientos")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="Código Naval:").grid(row=0, column=0, padx=5, pady=5)
        self.codigo_naval_historico_var = tk.StringVar()
        codigo_naval_historico_entry = ttk.Entry(form_frame, textvariable=self.codigo_naval_historico_var)
        codigo_naval_historico_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="ID Centro Anterior:").grid(row=1, column=0, padx=5, pady=5)
        self.id_centro_anterior_var = tk.StringVar()
        id_centro_anterior_entry = ttk.Entry(form_frame, textvariable=self.id_centro_anterior_var)
        id_centro_anterior_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="ID Centro Nuevo:").grid(row=2, column=0, padx=5, pady=5)
        self.id_centro_nuevo_var = tk.StringVar()
        id_centro_nuevo_entry = ttk.Entry(form_frame, textvariable=self.id_centro_nuevo_var)
        id_centro_nuevo_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Fecha de Instalación (DD-MM-YYYY):").grid(row=3, column=0, padx=5, pady=5)
        self.fecha_instalacion_var = tk.StringVar()
        fecha_instalacion_entry = ttk.Entry(form_frame, textvariable=self.fecha_instalacion_var)
        fecha_instalacion_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Fecha de Término (DD-MM-YYYY):").grid(row=4, column=0, padx=5, pady=5)
        self.fecha_termino_var = tk.StringVar()
        fecha_termino_entry = ttk.Entry(form_frame, textvariable=self.fecha_termino_var)
        fecha_termino_entry.grid(row=4, column=1, padx=5, pady=5)

        add_button = ttk.Button(form_frame, text="Agregar", command=self.add_historico_movimientos)
        add_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.historico_tree = ttk.Treeview(tab, columns=("ID Movimiento", "Código Naval", "ID Centro Anterior", "ID Centro Nuevo", "Fecha de Instalación", "Fecha de Término"), show="headings")
        self.historico_tree.heading("ID Movimiento", text="ID Movimiento")
        self.historico_tree.heading("Código Naval", text="Código Naval")
        self.historico_tree.heading("ID Centro Anterior", text="ID Centro Anterior")
        self.historico_tree.heading("ID Centro Nuevo", text="ID Centro Nuevo")
        self.historico_tree.heading("Fecha de Instalación", text="Fecha de Instalación")
        self.historico_tree.heading("Fecha de Término", text="Fecha de Término")
        self.historico_tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.refresh_historico_list()

    def refresh_historico_list(self):
        for item in self.historico_tree.get_children():
            self.historico_tree.delete(item)
        movimientos = self.data_manager.consultar_historico_movimientos()
        for movimiento in movimientos:
            fecha_instalacion = movimiento[4].strftime("%d-%m-%Y") if movimiento[4] else "N/A"
            fecha_termino = movimiento[5].strftime("%d-%m-%Y") if movimiento[5] else "N/A"
            self.historico_tree.insert("", "end", values=(movimiento[0], movimiento[1], movimiento[2], movimiento[3], fecha_instalacion, fecha_termino))

    def add_historico_movimientos(self):
        codigo_naval = self.codigo_naval_historico_var.get()
        id_centro_anterior = self.id_centro_anterior_var.get()
        id_centro_nuevo = self.id_centro_nuevo_var.get()
        fecha_instalacion = self.fecha_instalacion_var.get()
        fecha_termino = self.fecha_termino_var.get()
        if codigo_naval and id_centro_anterior and id_centro_nuevo and fecha_instalacion and fecha_termino:
            self.data_manager.insert_historico_movimientos(codigo_naval, id_centro_anterior, id_centro_nuevo, fecha_instalacion, fecha_termino)
            self.refresh_historico_list()
            self.refresh_ponton_list()  # Actualizar la lista de pontones
            self.refresh_ubicacion_list()  # Actualizar la lista de ubicaciones
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def create_tab_historico_dispositivos(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Histórico Dispositivos")

        form_frame = ttk.LabelFrame(tab, text="Agregar Histórico de Dispositivos")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="Serial del Dispositivo:").grid(row=0, column=0, padx=5, pady=5)
        self.serial_historico_var = tk.StringVar()
        serial_historico_entry = ttk.Entry(form_frame, textvariable=self.serial_historico_var)
        serial_historico_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Código Naval Anterior:").grid(row=1, column=0, padx=5, pady=5)
        self.codigo_naval_anterior_var = tk.StringVar()
        codigo_naval_anterior_entry = ttk.Entry(form_frame, textvariable=self.codigo_naval_anterior_var)
        codigo_naval_anterior_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Código Naval Nuevo:").grid(row=2, column=0, padx=5, pady=5)
        self.codigo_naval_nuevo_var = tk.StringVar()
        codigo_naval_nuevo_entry = ttk.Entry(form_frame, textvariable=self.codigo_naval_nuevo_var)
        codigo_naval_nuevo_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Fecha de Instalación (DD-MM-YYYY):").grid(row=3, column=0, padx=5, pady=5)
        self.fecha_instalacion_dispositivo_var = tk.StringVar()
        fecha_instalacion_dispositivo_entry = ttk.Entry(form_frame, textvariable=self.fecha_instalacion_dispositivo_var)
        fecha_instalacion_dispositivo_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Fecha de Término (DD-MM-YYYY):").grid(row=4, column=0, padx=5, pady=5)
        self.fecha_termino_dispositivo_var = tk.StringVar()
        fecha_termino_dispositivo_entry = ttk.Entry(form_frame, textvariable=self.fecha_termino_dispositivo_var)
        fecha_termino_dispositivo_entry.grid(row=4, column=1, padx=5, pady=5)

        add_button = ttk.Button(form_frame, text="Agregar", command=self.add_historico_dispositivos)
        add_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.tree_dispositivos = ttk.Treeview(tab, columns=("ID Movimiento Dispositivo", "Serial", "Código Naval Anterior", "Código Naval Nuevo", "Fecha Instalación", "Fecha Término"), show="headings")
        self.tree_dispositivos.heading("ID Movimiento Dispositivo", text="ID Movimiento Dispositivo")
        self.tree_dispositivos.heading("Serial", text="Serial")
        self.tree_dispositivos.heading("Código Naval Anterior", text="Código Naval Anterior")
        self.tree_dispositivos.heading("Código Naval Nuevo", text="Código Naval Nuevo")
        self.tree_dispositivos.heading("Fecha Instalación", text="Fecha Instalación")
        self.tree_dispositivos.heading("Fecha Término", text="Fecha Término")
        self.tree_dispositivos.pack(padx=10, pady=10, fill="both", expand=True)
        self.refresh_historico_dispositivos_list()

    def refresh_historico_dispositivos_list(self):
        for item in self.tree_dispositivos.get_children():
            self.tree_dispositivos.delete(item)
        historico_dispositivos = self.data_manager.consultar_historico_dispositivos()
        for dispositivo in historico_dispositivos:
            fecha_instalacion = dispositivo[4].strftime("%d-%m-%Y") if dispositivo[4] else "N/A"
            fecha_termino = dispositivo[5].strftime("%d-%m-%Y") if dispositivo[5] else "N/A"
            self.tree_dispositivos.insert("", "end", values=(dispositivo[0], dispositivo[1], dispositivo[2], dispositivo[3], fecha_instalacion, fecha_termino))

    def add_historico_dispositivos(self):
        serial = self.serial_historico_var.get()
        id_codigo_naval_anterior = self.codigo_naval_anterior_var.get()
        id_codigo_naval_nuevo = self.codigo_naval_nuevo_var.get()
        fecha_instalacion = self.fecha_instalacion_dispositivo_var.get()
        fecha_termino = self.fecha_termino_dispositivo_var.get()
        if serial and id_codigo_naval_anterior and id_codigo_naval_nuevo and fecha_instalacion and fecha_termino:
            self.data_manager.insert_historico_dispositivos(serial, id_codigo_naval_anterior, id_codigo_naval_nuevo, fecha_instalacion, fecha_termino)
            self.refresh_historico_dispositivos_list()
            self.refresh_dispositivo_list()  # Actualizar la lista de dispositivos
            self.refresh_ponton_list()  # Actualizar la lista de pontones
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")