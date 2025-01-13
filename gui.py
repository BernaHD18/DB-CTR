import tkinter as tk
import logging
from tkinter import ttk, messagebox
from data_manager import DataManager
from tkcalendar import DateEntry

class App(tk.Tk):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.title("Gestión de Base de Datos")
        self.geometry("1200x600")

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
        style.theme_use('clam')
        style.configure('Treeview', font=('Helvetica', 11), rowheight=25)
        style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'))


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

        ttk.Label(form_frame, text="Nombre de la Empresa:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_empresa_var = tk.StringVar()
        nombre_empresa_entry = ttk.Entry(form_frame, textvariable=self.nombre_empresa_var)
        nombre_empresa_entry.grid(row=0, column=1, padx=5, pady=5)

        add_button = ttk.Button(form_frame, text="Agregar", command=self.add_empresa)
        add_button.grid(row=1, column=0, columnspan=2, pady=10)

        delete_button = ttk.Button(form_frame, text="Borrar", command=self.delete_empresa)
        delete_button.grid(row=1, column=2, columnspan=2, pady=10)

        self.empresa_tree = ttk.Treeview(tab, columns=("Nombre"), show="headings")
        self.empresa_tree.heading("Nombre", text="Nombre")
        self.empresa_tree.pack(padx=10, pady=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.empresa_tree.yview)
        self.empresa_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.refresh_empresa_list()


    def refresh_empresa_list(self):
        for item in self.empresa_tree.get_children():
            self.empresa_tree.delete(item)
        empresas = self.data_manager.consultar_empresas()
        for empresa in empresas:
            self.empresa_tree.insert("", "end", values=(empresa[0],))

    def add_empresa(self):
        nombre_empresa = self.nombre_empresa_var.get()
        if nombre_empresa:
            self.data_manager.insert_empresa(nombre_empresa)
            self.refresh_empresa_list()
        else:
            messagebox.showerror("Error", "El campo Nombre de la Empresa es obligatorio")

    def delete_empresa(self):
        selected_item = self.empresa_tree.selection()
        if selected_item:
            nombre_empresa = self.empresa_tree.item(selected_item, 'values')[0]
            self.data_manager.delete_empresa(nombre_empresa)
            self.refresh_empresa_list()
        else:
            messagebox.showerror("Error", "Seleccione una empresa para borrar")

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
        self.nombre_empresa_var = tk.StringVar()
        self.nombre_empresa_combobox = ttk.Combobox(form_frame, textvariable=self.nombre_empresa_var)
        self.nombre_empresa_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.refresh_nombre_empresa_combobox()

        add_button = ttk.Button(form_frame, text="Agregar", command=self.add_ubicacion)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

        delete_button = ttk.Button(form_frame, text="Borrar", command=self.delete_ubicacion)
        delete_button.grid(row=3, column=2, columnspan=2, pady=10)

        self.ubicacion_tree = ttk.Treeview(tab, columns=("Nombre del Centro", "Grupo de Telegram", "Nombre de la Empresa"), show="headings")
        self.ubicacion_tree.heading("Nombre del Centro", text="Nombre del Centro")
        self.ubicacion_tree.heading("Grupo de Telegram", text="Grupo de Telegram")
        self.ubicacion_tree.heading("Nombre de la Empresa", text="Nombre de la Empresa")
        self.ubicacion_tree.pack(padx=10, pady=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.ubicacion_tree.yview)
        self.ubicacion_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.refresh_ubicacion_list()
    

    def delete_ubicacion(self):
        selected_item = self.ubicacion_tree.selection()
        if selected_item:
            nombre_centro = self.ubicacion_tree.item(selected_item, 'values')[0]
            self.data_manager.delete_ubicacion(nombre_centro)
            self.refresh_ubicacion_list()
            self.refresh_nombre_centro_ponton_combobox()  # Actualizar el combobox de nombre de centro en pontones
        else:
            messagebox.showerror("Error", "Seleccione una ubicación para borrar")

    def on_centro_anterior_selected(self, event):
        selected_centro_anterior = self.id_centro_anterior_var.get()
        centros = self.data_manager.consultar_centros()
        ids_centros = [centro[0] for centro in centros if centro[0] != selected_centro_anterior]
        self.id_centro_nuevo_combobox['values'] = ids_centros

    def refresh_ubicacion_list(self):
        for item in self.ubicacion_tree.get_children():
            self.ubicacion_tree.delete(item)
        ubicaciones = self.data_manager.consultar_ubicaciones()
        for ubicacion in ubicaciones:
            self.ubicacion_tree.insert("", "end", values=(ubicacion[0], ubicacion[1], ubicacion[2]))

    def add_ubicacion(self):
        nombre_centro = self.nombre_centro_var.get()
        grupo_telegram = self.grupo_telegram_var.get()
        nombre_empresa = self.nombre_empresa_var.get()
        if nombre_centro and nombre_empresa:
            self.data_manager.insert_ubicacion(nombre_centro, grupo_telegram, nombre_empresa)
            self.refresh_ubicacion_list()
            self.refresh_nombre_centro_ponton_combobox()  # Actualizar el combobox de nombre de centro en pontones
        else:
            messagebox.showerror("Error", "Los campos Nombre del Centro y Nombre de la Empresa son obligatorios")

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
        self.nombre_centro_ponton_combobox = ttk.Combobox(form_frame, textvariable=self.nombre_centro_ponton_var)
        self.nombre_centro_ponton_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.refresh_nombre_centro_ponton_combobox()

        ttk.Label(form_frame, text="Estado:").grid(row=2, column=0, padx=5, pady=5)
        self.estado_var = tk.StringVar()
        estado_combobox = ttk.Combobox(form_frame, textvariable=self.estado_var, values=["Activo", "No Activo"])
        estado_combobox.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="IA:").grid(row=3, column=0, padx=5, pady=5)
        self.ia_var = tk.StringVar()
        ia_combobox = ttk.Combobox(form_frame, textvariable=self.ia_var, values=["Funcionando con IA", "Entrenando", "Configurando", "No"])
        ia_combobox.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Observaciones:").grid(row=4, column=0, padx=5, pady=5)
        self.observaciones_var = tk.StringVar()
        observaciones_entry = ttk.Entry(form_frame, textvariable=self.observaciones_var)
        observaciones_entry.grid(row=4, column=1, padx=5, pady=5)

        add_button = ttk.Button(form_frame, text="Agregar", command=self.add_ponton)
        add_button.grid(row=5, column=0, columnspan=2, pady=10)

        delete_button = ttk.Button(form_frame, text="Borrar", command=self.delete_ponton)
        delete_button.grid(row=5, column=2, columnspan=2, pady=10)

        self.ponton_tree = ttk.Treeview(tab, columns=("Código Naval", "Nombre del Centro", "Estado", "IA", "Observaciones"), show="headings")
        self.ponton_tree.heading("Código Naval", text="Código Naval")
        self.ponton_tree.heading("Nombre del Centro", text="Nombre del Centro")
        self.ponton_tree.heading("Estado", text="Estado")
        self.ponton_tree.heading("IA", text="IA")
        self.ponton_tree.heading("Observaciones", text="Observaciones")
        self.ponton_tree.pack(padx=10, pady=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.ponton_tree.yview)
        self.ponton_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.refresh_ponton_list()

    def refresh_nombre_centro_ponton_combobox(self):
        centros = self.data_manager.consultar_centros()
        nombres_centros = [centro[0] for centro in centros]
        self.nombre_centro_ponton_combobox['values'] = nombres_centros

    def refresh_nombre_empresa_combobox(self):
        empresas = self.data_manager.consultar_empresas()
        nombres_empresas = [empresa[0] for empresa in empresas]
        self.nombre_empresa_combobox['values'] = nombres_empresas

    def refresh_ponton_list(self):
        for item in self.ponton_tree.get_children():
            self.ponton_tree.delete(item)
        pontones = self.data_manager.consultar_pontones()
        for ponton in pontones:
            estado = "Activo" if ponton[2] else "No Activo"
            self.ponton_tree.insert("", "end", values=(ponton[0], ponton[1], estado, ponton[3], ponton[4]))
    
    def refresh_codigo_naval_dispositivos_combobox(self):
        pontones = self.data_manager.consultar_pontones()
        codigos_navales = [ponton[0] for ponton in pontones]
        self.codigo_naval_dispositivo_combobox['values'] = codigos_navales

    def refresh_codigo_naval_historico_combobox(self):
        pontones = self.data_manager.consultar_pontones()
        codigos_navales = [ponton[0] for ponton in pontones]
        self.codigo_naval_historico_combobox['values'] = codigos_navales

    def add_ponton(self):
        codigo_naval = self.codigo_naval_var.get()
        nombre_centro = self.nombre_centro_ponton_var.get()
        estado = self.estado_var.get() == "Activo"
        ia = self.ia_var.get()
        observaciones = self.observaciones_var.get()
        if codigo_naval and nombre_centro and ia:
            self.data_manager.insert_ponton(codigo_naval, nombre_centro, estado, ia, observaciones)
            self.refresh_ponton_list()
            self.refresh_codigo_naval_dispositivos_combobox()  # Actualizar el combobox de código naval en dispositivos
            self.refresh_nombre_centro_ponton_combobox
        else:
            messagebox.showerror("Error", "Los campos Código Naval, Nombre del Centro y IA son obligatorios")

    def delete_ponton(self):
        selected_item = self.ponton_tree.selection()
        if selected_item:
            codigo_naval = self.ponton_tree.item(selected_item, 'values')[0]
            self.data_manager.delete_ponton(codigo_naval)
            self.refresh_ponton_list()
            self.refresh_codigo_naval_dispositivos_combobox()  # Actualizar el combobox de código naval en dispositivos
        else:
            messagebox.showerror("Error", "Seleccione un pontón para borrar")

    def create_tab_dispositivos(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Dispositivos")

        form_frame = ttk.LabelFrame(tab, text="Agregar Dispositivo")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="Serial:").grid(row=0, column=0, padx=5, pady=5)
        self.serial_var = tk.StringVar()
        self.serial_entry = ttk.Entry(form_frame, textvariable=self.serial_var)
        self.serial_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Código Naval:").grid(row=1, column=0, padx=5, pady=5)
        self.codigo_naval_dispositivo_var = tk.StringVar()
        self.codigo_naval_dispositivo_combobox = ttk.Combobox(form_frame, textvariable=self.codigo_naval_dispositivo_var)
        self.codigo_naval_dispositivo_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.refresh_codigo_naval_dispositivos_combobox()

        ttk.Label(form_frame, text="Dirección IP:").grid(row=2, column=0, padx=5, pady=5)
        self.direccionamiento_ip_var = tk.StringVar()
        self.direccionamiento_ip_entry = ttk.Entry(form_frame, textvariable=self.direccionamiento_ip_var)
        self.direccionamiento_ip_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Firmware:").grid(row=3, column=0, padx=5, pady=5)
        self.firmware_var = tk.StringVar()
        self.firmware_entry = ttk.Entry(form_frame, textvariable=self.firmware_var)
        self.firmware_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Usuario:").grid(row=4, column=0, padx=5, pady=5)
        self.usuario_var = tk.StringVar()
        self.usuario_entry = ttk.Entry(form_frame, textvariable=self.usuario_var)
        self.usuario_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Contraseña:").grid(row=5, column=0, padx=5, pady=5)
        self.contrasena_var = tk.StringVar()
        self.contrasena_entry = ttk.Entry(form_frame, textvariable=self.contrasena_var, show="*")
        self.contrasena_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Tipo de Dispositivo:").grid(row=6, column=0, padx=5, pady=5)
        self.tipo_dispositivo_var = tk.StringVar()
        self.tipo_dispositivo_combobox = ttk.Combobox(form_frame, textvariable=self.tipo_dispositivo_var, values=["NIO", "Radar", "Asistente Virtual", "Cámara"])
        self.tipo_dispositivo_combobox.grid(row=6, column=1, padx=5, pady=5)
        self.tipo_dispositivo_combobox.bind("<<ComboboxSelected>>", self.on_tipo_dispositivo_selected)

        self.extra_frame = ttk.Frame(form_frame)
        self.extra_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        add_button = ttk.Button(form_frame, text="Agregar", command=self.add_dispositivo)
        add_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.dispositivo_tree = ttk.Treeview(tab, columns=("Serial", "Codigo_Naval", "Direccionamiento_IP", "Firmware_Version", "ID_Credenciales", "Tipo_Dispositivo"), show="headings")
        self.dispositivo_tree.heading("Serial", text="Serial")
        self.dispositivo_tree.heading("Codigo_Naval", text="Código Naval")
        self.dispositivo_tree.heading("Direccionamiento_IP", text="Dirección IP")
        self.dispositivo_tree.heading("Firmware_Version", text="Firmware")
        self.dispositivo_tree.heading("ID_Credenciales", text="ID Credenciales")
        self.dispositivo_tree.heading("Tipo_Dispositivo", text="Tipo de Dispositivo")
        self.dispositivo_tree.pack(padx=10, pady=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.dispositivo_tree.yview)
        self.dispositivo_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.refresh_dispositivo_list()

    def on_tipo_dispositivo_selected(self, event):
        for widget in self.extra_frame.winfo_children():
            widget.destroy()

        tipo_dispositivo = self.tipo_dispositivo_var.get()
        if tipo_dispositivo == "NIO":
            ttk.Label(self.extra_frame, text="Modelo:").grid(row=0, column=0, padx=5, pady=5)
            self.modelo_var = tk.StringVar()
            self.modelo_combobox = ttk.Combobox(self.extra_frame, textvariable=self.modelo_var, values=["NIO-DIO", "NIO-App"])
            self.modelo_combobox.grid(row=0, column=1, padx=5, pady=5)
        elif tipo_dispositivo == "Radar":
            ttk.Label(self.extra_frame, text="Canal RF:").grid(row=0, column=0, padx=5, pady=5)
            self.canal_rf_var = tk.StringVar()
            self.canal_rf_entry = ttk.Entry(self.extra_frame, textvariable=self.canal_rf_var)
            self.canal_rf_entry.grid(row=0, column=1, padx=5, pady=5)
        # Agregar más campos según sea necesario para otros tipos de dispositivos

    def refresh_dispositivo_list(self):
        for item in self.dispositivo_tree.get_children():
            self.dispositivo_tree.delete(item)
        dispositivos = self.data_manager.consultar_dispositivos()
        if dispositivos:
            for dispositivo in dispositivos:
                self.dispositivo_tree.insert("", "end", values=dispositivo)
        else:
            logging.error("No se encontraron dispositivos")

    def refresh_codigo_naval_ponton_combobox(self):
        pontones = self.data_manager.consultar_pontones()
        codigo_navales = [ponton[0] for ponton in pontones]
        self.codigo_naval_ponton_combobox['values'] = codigo_navales
    
    def refresh_id_centro_anterior_combobox(self):
        centros = self.data_manager.consultar_centros()
        ids_centros = [centro[0] for centro in centros]
        self.id_centro_anterior_combobox['values'] = ids_centros

    def refresh_id_centro_nuevo_combobox(self):
        centros = self.data_manager.consultar_centros()
        ids_centros = [centro[0] for centro in centros]
        self.id_centro_nuevo_combobox['values'] = ids_centros

    def add_dispositivo(self):
        serial = self.serial_var.get().strip()
        direccionamiento_ip = self.direccionamiento_ip_var.get().strip()
        firmware_version = self.firmware_var.get().strip()
        usuario = self.usuario_var.get().strip()
        contrasena = self.contrasena_var.get().strip()
        tipo_dispositivo = self.tipo_dispositivo_var.get().strip()
        codigo_naval_ponton = self.codigo_naval_dispositivo_var.get().strip()

        if serial and direccionamiento_ip and firmware_version and usuario and contrasena and tipo_dispositivo and codigo_naval_ponton:
            if tipo_dispositivo == "NIO":
                modelo = self.modelo_var.get().strip()
                self.data_manager.insert_nio(serial, modelo, direccionamiento_ip, firmware_version, usuario, contrasena)
            elif tipo_dispositivo == "Radar":
                canal_rf = self.canal_rf_var.get().strip()
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
        codigo_naval = self.codigo_naval_var.get().strip()
        centro_anterior = self.centro_anterior_var.get().strip()
        centro_nuevo = self.centro_nuevo_var.get().strip()
        fecha_instalacion = self.fecha_instalacion_var.get().strip()
        fecha_termino = self.fecha_termino_var.get().strip()

        if codigo_naval and centro_anterior and centro_nuevo and fecha_instalacion and fecha_termino:
            self.data_manager.insert_historico_movimientos(codigo_naval, centro_anterior, centro_nuevo, fecha_instalacion, fecha_termino)
            self.refresh_historico_movimientos_list()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
    
    def refresh_historico_movimientos_list(self):
        for item in self.historico_movimientos_tree.get_children():
            self.historico_movimientos_tree.delete(item)
        historico_movimientos = self.data_manager.consultar_historico_movimientos()
        if historico_movimientos:
            for movimiento in historico_movimientos:
                fecha_instalacion = movimiento[3].strftime("%d-%m-%Y") if movimiento[3] else "N/A"
                fecha_termino = movimiento[4].strftime("%d-%m-%Y") if movimiento[4] else "N/A"
                self.historico_movimientos_tree.insert("", "end", values=(movimiento[0], movimiento[1], movimiento[2], fecha_instalacion, fecha_termino))
        else:
            logging.error("No se encontraron movimientos históricos")

    def refresh_centro_anterior_combobox(self):
        centros = self.data_manager.consultar_centros()
        nombres_centros = [centro[0] for centro in centros]
        self.centro_anterior_combobox['values'] = nombres_centros

    def refresh_centro_nuevo_combobox(self):
        centros = self.data_manager.consultar_centros()
        nombres_centros = [centro[0] for centro in centros]
        self.centro_nuevo_combobox['values'] = nombres_centros

    def refresh_codigo_naval_combobox(self):
        codigos_navales = self.data_manager.consultar_codigos_navales()
        self.codigo_naval_combobox['values'] = codigos_navales

    def create_tab_historico_movimientos(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Histórico Movimientos")

        form_frame = ttk.LabelFrame(tab, text="Agregar Histórico de Movimientos")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="Código Naval:").grid(row=0, column=0, padx=5, pady=5)
        self.codigo_naval_var = tk.StringVar()
        self.codigo_naval_combobox = ttk.Combobox(form_frame, textvariable=self.codigo_naval_var)
        self.codigo_naval_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.refresh_codigo_naval_combobox()

        ttk.Label(form_frame, text="Centro Anterior:").grid(row=1, column=0, padx=5, pady=5)
        self.centro_anterior_var = tk.StringVar()
        self.centro_anterior_combobox = ttk.Combobox(form_frame, textvariable=self.centro_anterior_var)
        self.centro_anterior_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.refresh_centro_anterior_combobox()

        ttk.Label(form_frame, text="Centro Nuevo:").grid(row=2, column=0, padx=5, pady=5)
        self.centro_nuevo_var = tk.StringVar()
        self.centro_nuevo_combobox = ttk.Combobox(form_frame, textvariable=self.centro_nuevo_var)
        self.centro_nuevo_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.refresh_centro_nuevo_combobox()

        ttk.Label(form_frame, text="Fecha de Instalación:").grid(row=3, column=0, padx=5, pady=5)
        self.fecha_instalacion_var = tk.StringVar()
        self.fecha_instalacion_entry = DateEntry(form_frame, textvariable=self.fecha_instalacion_var, date_pattern='dd-mm-yyyy')
        self.fecha_instalacion_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Fecha de Término:").grid(row=4, column=0, padx=5, pady=5)
        self.fecha_termino_var = tk.StringVar()
        self.fecha_termino_entry = DateEntry(form_frame, textvariable=self.fecha_termino_var, date_pattern='dd-mm-yyyy')
        self.fecha_termino_entry.grid(row=4, column=1, padx=5, pady=5)

        add_button = ttk.Button(form_frame, text="Agregar", command=self.add_historico_movimientos)
        add_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.historico_movimientos_tree = ttk.Treeview(tab, columns=("Código Naval", "Centro Anterior", "Centro Nuevo", "Fecha Instalación", "Fecha Término"), show="headings")
        self.historico_movimientos_tree.heading("Código Naval", text="Código Naval")
        self.historico_movimientos_tree.heading("Centro Anterior", text="Centro Anterior")
        self.historico_movimientos_tree.heading("Centro Nuevo", text="Centro Nuevo")
        self.historico_movimientos_tree.heading("Fecha Instalación", text="Fecha Instalación")
        self.historico_movimientos_tree.heading("Fecha Término", text="Fecha Término")
        self.historico_movimientos_tree.pack(padx=10, pady=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.historico_movimientos_tree.yview)
        self.historico_movimientos_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.refresh_historico_movimientos_list()

    def refresh_historico_list(self):
        for item in self.historico_tree.get_children():
            self.historico_tree.delete(item)
        movimientos = self.data_manager.consultar_historico_movimientos()
        for movimiento in movimientos:
            fecha_instalacion = movimiento[4].strftime("%d-%m-%Y") if movimiento[4] else "N/A"
            fecha_termino = movimiento[5].strftime("%d-%m-%Y") if movimiento[5] else "N/A"
            self.historico_tree.insert("", "end", values=(movimiento[0], movimiento[1], movimiento[2], movimiento[3], fecha_instalacion, fecha_termino))

    def add_historico_movimientos(self):
        codigo_naval = self.codigo_naval_var.get().strip()
        centro_anterior = self.centro_anterior_var.get().strip()
        centro_nuevo = self.centro_nuevo_var.get().strip()
        fecha_instalacion = self.fecha_instalacion_var.get().strip()
        fecha_termino = self.fecha_termino_var.get().strip()

        if codigo_naval and centro_anterior and centro_nuevo and fecha_instalacion and fecha_termino:
            self.data_manager.insert_historico_movimientos(codigo_naval, centro_anterior, centro_nuevo, fecha_instalacion, fecha_termino)
            self.refresh_historico_movimientos_list()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def on_serial_dispositivo_selected(self, event):
        serial = self.serial_dispositivo_var.get()
        codigo_naval_anterior = self.data_manager.consultar_codigo_naval_por_serial(serial)
        self.codigo_naval_anterior_var.set(codigo_naval_anterior)
        self.codigo_naval_anterior_entry.config(state='readonly')


    def create_tab_historico_dispositivos(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Histórico Dispositivos")

        form_frame = ttk.LabelFrame(tab, text="Agregar Histórico de Dispositivos")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="Serial del Dispositivo:").grid(row=0, column=0, padx=5, pady=5)
        self.serial_dispositivo_var = tk.StringVar()
        self.serial_dispositivo_combobox = ttk.Combobox(form_frame, textvariable=self.serial_dispositivo_var)
        self.serial_dispositivo_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.serial_dispositivo_combobox.bind("<<ComboboxSelected>>", self.on_serial_dispositivo_selected)
        self.refresh_serial_dispositivo_combobox()

        ttk.Label(form_frame, text="Código Naval Anterior:").grid(row=1, column=0, padx=5, pady=5)
        self.codigo_naval_anterior_var = tk.StringVar()
        self.codigo_naval_anterior_entry = ttk.Entry(form_frame, textvariable=self.codigo_naval_anterior_var, state='readonly')
        self.codigo_naval_anterior_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Código Naval Nuevo:").grid(row=2, column=0, padx=5, pady=5)
        self.codigo_naval_nuevo_var = tk.StringVar()
        self.codigo_naval_nuevo_combobox = ttk.Combobox(form_frame, textvariable=self.codigo_naval_nuevo_var)
        self.codigo_naval_nuevo_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.refresh_codigo_naval_nuevo_combobox()

        ttk.Label(form_frame, text="Fecha de Instalación:").grid(row=3, column=0, padx=5, pady=5)
        self.fecha_instalacion_var = tk.StringVar()
        self.fecha_instalacion_entry = DateEntry(form_frame, textvariable=self.fecha_instalacion_var, date_pattern='dd-mm-yyyy')
        self.fecha_instalacion_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Fecha de Término:").grid(row=4, column=0, padx=5, pady=5)
        self.fecha_termino_var = tk.StringVar()
        self.fecha_termino_entry = DateEntry(form_frame, textvariable=self.fecha_termino_var, date_pattern='dd-mm-yyyy')
        self.fecha_termino_entry.grid(row=4, column=1, padx=5, pady=5)

        add_button = ttk.Button(form_frame, text="Agregar", command=self.add_historico_dispositivos)
        add_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.historico_dispositivos_tree = ttk.Treeview(tab, columns=("Serial", "Código Naval Anterior", "Código Naval Nuevo", "Fecha Instalación", "Fecha Término"), show="headings")
        self.historico_dispositivos_tree.heading("Serial", text="Serial")
        self.historico_dispositivos_tree.heading("Código Naval Anterior", text="Código Naval Anterior")
        self.historico_dispositivos_tree.heading("Código Naval Nuevo", text="Código Naval Nuevo")
        self.historico_dispositivos_tree.heading("Fecha Instalación", text="Fecha Instalación")
        self.historico_dispositivos_tree.heading("Fecha Término", text="Fecha Término")
        self.historico_dispositivos_tree.pack(padx=10, pady=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.historico_dispositivos_tree.yview)
        self.historico_dispositivos_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.refresh_historico_dispositivos_list()

    def add_historico_dispositivos(self):
        serial = self.serial_dispositivo_var.get()
        codigo_naval_anterior = self.codigo_naval_anterior_var.get()
        codigo_naval_nuevo = self.codigo_naval_nuevo_var.get()
        fecha_instalacion = self.fecha_instalacion_var.get()
        fecha_termino = self.fecha_termino_var.get()

        if not serial or not codigo_naval_nuevo or not fecha_instalacion:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            self.data_manager.insertar_historico_dispositivos(serial, codigo_naval_anterior, codigo_naval_nuevo, fecha_instalacion, fecha_termino)
            self.refresh_historico_dispositivos_list()
            messagebox.showinfo("Éxito", "Histórico de dispositivos agregado correctamente")
        except Exception as e:
            logging.error(f"Error al insertar histórico de dispositivos: {e}")
            messagebox.showerror("Error", f"Error al insertar histórico de dispositivos: {e}")


    def refresh_serial_dispositivo_combobox(self):
        dispositivos = self.data_manager.consultar_dispositivos()
        seriales = [dispositivo[0] for dispositivo in dispositivos]
        self.serial_dispositivo_combobox['values'] = seriales
    
    def refresh_codigo_naval_anterior_combobox(self):
        pontones = self.data_manager.consultar_pontones()
        codigos_navales = [ponton[0] for ponton in pontones]
        self.codigo_naval_anterior_combobox['values'] = codigos_navales

    def refresh_codigo_naval_nuevo_combobox(self):
        pontones = self.data_manager.consultar_pontones()
        codigos_navales = [ponton[0] for ponton in pontones]
        self.codigo_naval_nuevo_combobox['values'] = codigos_navales

    def on_codigo_naval_anterior_selected(self, event):
        selected_codigo_naval_anterior = self.codigo_naval_anterior_var.get()
        pontones = self.data_manager.consultar_pontones()
        codigos_navales = [ponton[0] for ponton in pontones if ponton[0] != selected_codigo_naval_anterior]
        self.codigo_naval_nuevo_combobox['values'] = codigos_navales

    def add_historico_dispositivos(self):
        serial = self.serial_dispositivo_var.get()
        codigo_naval_anterior = self.codigo_naval_anterior_var.get()
        codigo_naval_nuevo = self.codigo_naval_nuevo_var.get()
        fecha_instalacion = self.fecha_instalacion_var.get()
        fecha_termino = self.fecha_termino_var.get()

        if not serial or not codigo_naval_nuevo or not fecha_instalacion:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            self.data_manager.insertar_historico_dispositivos(serial, codigo_naval_anterior, codigo_naval_nuevo, fecha_instalacion, fecha_termino)
            self.refresh_historico_dispositivos_list()
            messagebox.showinfo("Éxito", "Histórico de dispositivos agregado correctamente")
        except Exception as e:
            logging.error(f"Error al insertar histórico de dispositivos: {e}")
            messagebox.showerror("Error", f"Error al insertar histórico de dispositivos: {e}")

    def refresh_historico_dispositivos_list(self):
        try:
            historico_dispositivos = self.data_manager.consultar_historico_dispositivos()
            if historico_dispositivos is None:
                logging.error("No se encontraron movimientos históricos")
                return

            for i in self.historico_dispositivos_tree.get_children():
                self.historico_dispositivos_tree.delete(i)

            for dispositivo in historico_dispositivos:
                self.historico_dispositivos_tree.insert("", "end", values=dispositivo)
        except Exception as e:
            logging.error(f"Error al consultar histórico de dispositivos: {e}")
            print(f"Error al consultar histórico de dispositivos: {e}")


