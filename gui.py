import tkinter as tk
import logging
from tkinter import ttk, messagebox
from data_manager import DataManager
from tkcalendar import DateEntry
from datetime import datetime


class App(tk.Tk):
    def __init__(self, data_manager, table_manager):
        super().__init__()
        self.data_manager = data_manager
        self.table_manager = table_manager
        self.title("Gestión de Base de Datos")
        self.geometry("1300x600")

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
        self.clear_historico_dispositivos_fields()
        self.clear_historico_movimientos_fields()

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

        # Gestión de Tablas
        table_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Gestión de Tablas", menu=table_menu)
        table_menu.add_command(label="Crear Tablas", command=self.confirm_create_tables)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.show_about)


    def show_about(self):
        messagebox.showinfo("Acerca de", "Gestión de Base de Datos\nVersión 1.0")

    def confirm_create_tables(self):
        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea borrar todas las tablas y generar nuevas? Haciendo esto perderá toda la información ya ingresada.")
        if confirm:
            self.table_manager.create_tables()
            self.clear_dispositivo_fields()
            self.clear_ponton_fields()
            self.clear_ubicacion_fields()
            self.clear_empresa_fields()
            self.clear_historico_dispositivos_fields()
            self.clear_historico_movimientos_fields()
            messagebox.showinfo("Éxito", "Tablas creadas correctamente")
            
            if hasattr(self, 'refresh_ponton_list'):
                self.refresh_ponton_list()
            if hasattr(self, 'refresh_empresa_list'):
                self.refresh_empresa_list()
            if hasattr(self, 'refresh_dispositivo_list'):
                self.refresh_dispositivo_list()
            if hasattr(self, 'refresh_historico_dispositivos_list'):
                self.refresh_historico_dispositivos_list()
            if hasattr(self, 'refresh_historico_movimientos_list'):
                self.refresh_historico_movimientos_list()
            if hasattr(self, 'refresh_ubicacion_list'):
                self.refresh_ubicacion_list()
            if hasattr(self, 'refresh_nombre_centro_ponton_combobox'):
                self.refresh_nombre_centro_ponton_combobox()
            if hasattr(self, 'refresh_nombre_empresa_combobox'):
                self.refresh_nombre_empresa_combobox()
            if hasattr(self, 'refresh_id_centro_anterior_combobox'):
                self.refresh_id_centro_anterior_combobox()
            if hasattr(self, 'refresh_id_centro_nuevo_combobox'):
                self.refresh_id_centro_nuevo_combobox()
            if hasattr(self, 'refresh_codigo_naval_anterior_combobox'):
                self.refresh_codigo_naval_anterior_combobox()
            if hasattr(self, 'refresh_codigo_naval_dispositivos_combobox'):
                self.refresh_codigo_naval_dispositivos_combobox()
        else:
            messagebox.showinfo("Información", "Operación cancelada")

    def create_tab_empresas(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Empresas")

        # Marco para el formulario de agregar empresa
        form_frame = ttk.LabelFrame(tab, text="Agregar Empresa")
        form_frame.pack(padx=10, pady=10, fill="x")

        # Campo de texto para ingresar el nombre de la empresa
        ttk.Label(form_frame, text="Nombre de la Empresa:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_empresa_entry = ttk.Entry(form_frame)
        self.nombre_empresa_entry.grid(row=0, column=1, padx=5, pady=5)
        self.nombre_empresa_entry.focus_set()  # Aseguramos que tenga el foco al iniciar

        # Botón para agregar empresa
        add_button = ttk.Button(form_frame, text="Agregar", command=self.add_empresa)
        add_button.grid(row=1, column=0, padx=5, pady=10)
        # Tabla para mostrar las empresas
        table_frame = ttk.Frame(tab)
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.empresa_tree = ttk.Treeview(table_frame, columns=("Nombre"), show="headings")
        self.empresa_tree.heading("Nombre", text="Nombre")
        self.empresa_tree.pack(side="left", fill="both", expand=True)

        # Barra de desplazamiento para la tabla
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.empresa_tree.yview)
        self.empresa_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Botón para borrar empresa
        delete_button = ttk.Button(form_frame, text="Borrar", command=self.delete_empresa)
        delete_button.grid(row=1, column=1, padx=20, pady=10)  # Aumentar el espacio horizontal entre los botones

        # Cargar la lista inicial de empresas
        self.refresh_empresa_list()


    def refresh_empresa_list(self):
        for item in self.empresa_tree.get_children():
            self.empresa_tree.delete(item)
        empresas = self.data_manager.consultar_empresas()
        if empresas:
            for empresa in empresas:
                self.empresa_tree.insert("", "end", values=(empresa[0],))

    def add_empresa(self):
        # Obtener el valor directamente desde el Entry
        nombre_empresa = self.nombre_empresa_entry.get().strip()

        # Validar si el campo está vacío
        if not nombre_empresa:
            messagebox.showerror("Error", "El campo nombre de la empresa es obligatorio")
            return

        # Intentar insertar el valor en la base de datos
        try:
            self.data_manager.insert_empresa(nombre_empresa)
            self.refresh_empresa_list()
            self.refresh_nombre_empresa_combobox()
            self.clear_empresa_fields()
            messagebox.showinfo("Éxito", f"Empresa '{nombre_empresa}' insertada correctamente")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar empresa: {e}")

    def delete_empresa(self):
        # Obtener la selección del usuario
        selected_item = self.empresa_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una empresa para borrar")
            return

        # Recuperar el nombre de la empresa seleccionada
        nombre_empresa = self.empresa_tree.item(selected_item, "values")[0]
        confirm = messagebox.askyesno("Confirmar", f"¿Seguro que desea borrar la empresa '{nombre_empresa}'?")
        if not confirm:
            return

        # Intentar borrar la empresa de la base de datos
        try:
            self.data_manager.delete_empresa(nombre_empresa)
            self.refresh_empresa_list()  # Actualizar la lista de empresas en la interfaz
            self.refresh_nombre_empresa_combobox()  # Actualizar el combobox de nombre de empresa en ubicaciones
            messagebox.showinfo("Éxito", f"La empresa '{nombre_empresa}' fue borrada exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo borrar la empresa: {e}")

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
            nombre_centro = self.ubicacion_tree.item(selected_item, "values")[0]
            confirm = messagebox.askyesno("Confirmar", f"¿Seguro que desea borrar la ubicación '{nombre_centro}'?")
            if not confirm:
                return

            try:
                self.data_manager.delete_ubicacion(nombre_centro)
                self.refresh_ubicacion_list()
                self.refresh_nombre_centro_ponton_combobox()
                self.refresh_id_centro_anterior_combobox()
                self.refresh_id_centro_nuevo_combobox()
                messagebox.showinfo("Éxito", f"La ubicacion '{nombre_centro}' fue borrada exitosamente")
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
            except Exception as e:
                messagebox.showerror("Error", f"Error al borrar ubicación: {e}")
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
        nombre_centro = self.nombre_centro_var.get().strip()
        grupo_telegram = self.grupo_telegram_var.get().strip()
        nombre_empresa = self.nombre_empresa_var.get().strip()

        if not nombre_centro or not nombre_empresa:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            self.data_manager.insert_ubicacion(nombre_centro, grupo_telegram, nombre_empresa)
            self.refresh_ubicacion_list()
            self.refresh_id_centro_anterior_combobox()
            self.refresh_id_centro_nuevo_combobox()
            self.refresh_nombre_centro_ponton_combobox()
            self.clear_ubicacion_fields()
            messagebox.showinfo("Éxito", f"Ubicación '{nombre_centro}' insertada correctamente")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar ubicación: {e}")

    def create_tab_pontones(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Pontones")

        form_frame = ttk.LabelFrame(tab, text="Agregar Pontón")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="Código Naval:").grid(row=0, column=0, padx=5, pady=5)
        self.codigo_naval_var = tk.StringVar()
        self.codigo_naval_entry = ttk.Entry(form_frame, textvariable=self.codigo_naval_var)
        self.codigo_naval_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Nombre del Centro:").grid(row=1, column=0, padx=5, pady=5)
        self.nombre_centro_ponton_var = tk.StringVar()
        self.nombre_centro_ponton_combobox = ttk.Combobox(form_frame, textvariable=self.nombre_centro_ponton_var)
        self.nombre_centro_ponton_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.refresh_nombre_centro_ponton_combobox()

        ttk.Label(form_frame, text="Estado:").grid(row=2, column=0, padx=5, pady=5)
        self.estado_var = tk.StringVar()
        estado_combobox = ttk.Combobox(form_frame, textvariable=self.estado_var, values=["Activo", "Inactivo"])
        estado_combobox.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="IA:").grid(row=3, column=0, padx=5, pady=5)
        self.ia_var = tk.StringVar()
        ia_combobox = ttk.Combobox(form_frame, textvariable=self.ia_var, values=["Funcionando con IA", "Entrenando", "Configurando", "No"])
        ia_combobox.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Observaciones:").grid(row=4, column=0, padx=5, pady=5)
        self.observaciones_var = tk.StringVar()
        observaciones_entry = ttk.Entry(form_frame, textvariable=self.observaciones_var)
        observaciones_entry.grid(row=4, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        add_button = ttk.Button(button_frame, text="Agregar", command=self.add_ponton)
        add_button.pack(side="left", padx=5)

        delete_button = ttk.Button(button_frame, text="Borrar", command=self.delete_ponton)
        delete_button.pack(side="left", padx=20)

        table_frame = ttk.Frame(tab)
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.ponton_tree = ttk.Treeview(table_frame, columns=("Código Naval", "Nombre del Centro", "Estado", "IA", "Observaciones"), show="headings")
        self.ponton_tree.heading("Código Naval", text="Código Naval")
        self.ponton_tree.heading("Nombre del Centro", text="Nombre del Centro")
        self.ponton_tree.heading("Estado", text="Estado")
        self.ponton_tree.heading("IA", text="IA")
        self.ponton_tree.heading("Observaciones", text="Observaciones")
        self.ponton_tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.ponton_tree.yview)
        self.ponton_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.refresh_ponton_list()

    def refresh_nombre_centro_ponton_combobox(self):
        centros = self.data_manager.consultar_centros()
        self.nombre_centro_ponton_combobox['values'] = centros

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
        codigo_naval = self.codigo_naval_var.get().strip()
        nombre_centro = self.nombre_centro_ponton_var.get().strip()
        estado = self.estado_var.get() == "Activo"
        ia = self.ia_var.get().strip()
        observaciones = self.observaciones_var.get().strip()

        if not codigo_naval or not nombre_centro or not ia:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            self.data_manager.insert_ponton(codigo_naval, nombre_centro, estado, ia, observaciones)
            self.refresh_ponton_list()
            self.refresh_codigo_naval_dispositivos_combobox()
            self.refresh_codigo_naval_historico_combobox()
            self.refresh_nombre_centro_ponton_combobox()
            self.refresh_codigo_naval_nuevo_combobox()
            self.clear_ponton_fields()
            messagebox.showinfo("Éxito", f"Pontón '{codigo_naval}' insertado correctamente")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar pontón: {e}")

    def delete_ponton(self):
        selected_item = self.ponton_tree.selection()
        if selected_item:
            codigo_naval = self.ponton_tree.item(selected_item, "values")[0]
            confirm = messagebox.askyesno("Confirmar", f"¿Seguro que desea borrar el pontón '{codigo_naval}'?")
            if not confirm:
                return

            try:
                self.data_manager.delete_ponton(codigo_naval)
                self.refresh_ponton_list()
                self.refresh_codigo_naval_dispositivos_combobox()
                self.refresh_codigo_naval_historico_combobox()
                self.refresh_nombre_centro_ponton_combobox()
                messagebox.showinfo("Éxito", f"Pontón '{codigo_naval}' borrado correctamente")
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
            except Exception as e:
                messagebox.showerror("Error", f"Error al borrar pontón: {e}")
        else:
            messagebox.showerror("Error", "Seleccione un pontón para borrar")

    def create_tab_dispositivos(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Dispositivos")

        form_frame = ttk.LabelFrame(tab, text="Agregar Dispositivo")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="Serial del Dispositivo:").grid(row=0, column=0, padx=5, pady=5)
        self.serial_dispositivo_entry = ttk.Entry(form_frame)
        self.serial_dispositivo_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Direccionamiento IP:").grid(row=1, column=0, padx=5, pady=5)
        self.direccionamiento_ip_entry = ttk.Entry(form_frame)
        self.direccionamiento_ip_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Firmware Version:").grid(row=2, column=0, padx=5, pady=5)
        self.firmware_version_entry = ttk.Entry(form_frame)
        self.firmware_version_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Usuario:").grid(row=3, column=0, padx=5, pady=5)
        self.usuario_entry = ttk.Entry(form_frame)
        self.usuario_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Contraseña:").grid(row=4, column=0, padx=5, pady=5)
        self.contrasena_entry = ttk.Entry(form_frame, show="*")
        self.contrasena_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Tipo de Dispositivo:").grid(row=5, column=0, padx=5, pady=5)
        self.tipo_dispositivo_combobox = ttk.Combobox(form_frame, values=["NIO", "Radar", "Asistente Virtual", "Cámara"])
        self.tipo_dispositivo_combobox.grid(row=5, column=1, padx=5, pady=5)
        self.tipo_dispositivo_combobox.bind("<<ComboboxSelected>>", self.on_tipo_dispositivo_selected)

        ttk.Label(form_frame, text="Código Naval:").grid(row=6, column=0, padx=5, pady=5)
        self.codigo_naval_dispositivo_combobox = ttk.Combobox(form_frame)
        self.codigo_naval_dispositivo_combobox.grid(row=6, column=1, padx=5, pady=5)
        self.refresh_codigo_naval_dispositivos_combobox()

        self.extra_frame = ttk.Frame(form_frame)
        self.extra_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)

        add_button = ttk.Button(button_frame, text="Agregar", command=self.add_dispositivo)
        add_button.pack(side="left", padx=5)

        delete_button = ttk.Button(button_frame, text="Borrar", command=self.delete_dispositivo)
        delete_button.pack(side="left", padx=20)

        table_frame = ttk.Frame(tab)
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.dispositivo_tree = ttk.Treeview(table_frame, columns=("Serial", "Tipo de Dispositivo", "Ponton Asociado", "Dirección IP", "Firmware Version", "Usuario"), show="headings")
        self.dispositivo_tree.heading("Serial", text="Serial")
        self.dispositivo_tree.heading("Tipo de Dispositivo", text="Tipo de Dispositivo")
        self.dispositivo_tree.heading("Ponton Asociado", text="Ponton Asociado")
        self.dispositivo_tree.heading("Dirección IP", text="Dirección IP")
        self.dispositivo_tree.heading("Firmware Version", text="Firmware Version")
        self.dispositivo_tree.heading("Usuario", text="ID Credenciales")
        self.dispositivo_tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.dispositivo_tree.yview)
        self.dispositivo_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.refresh_dispositivo_list()

    def delete_dispositivo(self):
        selected_item = self.dispositivo_tree.selection()
        if selected_item:
            serial = self.dispositivo_tree.item(selected_item, "values")[0]
            confirm = messagebox.askyesno("Confirmar", f"¿Seguro que desea borrar el dispositivo '{serial}'?")
            if not confirm:
                return

            try:
                self.data_manager.delete_dispositivo(serial)
                self.refresh_dispositivo_list()
                messagebox.showinfo("Éxito", f"Dispositivo '{serial}' borrado correctamente")
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
            except Exception as e:
                messagebox.showerror("Error", f"Error al borrar dispositivo: {e}")
        else:
            messagebox.showerror("Error", "Seleccione un dispositivo para borrar")

    def on_tipo_dispositivo_selected(self, event):
        for widget in self.extra_frame.winfo_children():
            widget.destroy()

        tipo_dispositivo = self.tipo_dispositivo_combobox.get()
        if tipo_dispositivo == "NIO":
            ttk.Label(self.extra_frame, text="Modelo:").grid(row=0, column=0, padx=5, pady=5)
            self.modelo_combobox = ttk.Combobox(self.extra_frame, values=["NIO-DIO", "NIO-App"])
            self.modelo_combobox.grid(row=0, column=1, padx=5, pady=5)
        elif tipo_dispositivo == "Radar":
            ttk.Label(self.extra_frame, text="Canal:").grid(row=0, column=0, padx=5, pady=5)
            self.canal_rf_entry = ttk.Entry(self.extra_frame)
            self.canal_rf_entry.grid(row=0, column=1, padx=5, pady=5)
        # Agregar más campos según sea necesario para otros tipos de dispositivos

    def refresh_dispositivo_list(self):
        for item in self.dispositivo_tree.get_children():
            self.dispositivo_tree.delete(item)
        dispositivos = self.data_manager.consultar_dispositivos()
        for dispositivo in dispositivos:
            self.dispositivo_tree.insert("", "end", values=(dispositivo[0], dispositivo[4], dispositivo[1], dispositivo[2], dispositivo[3], dispositivo[5]))
            
    def refresh_codigo_naval_ponton_combobox(self):
        pontones = self.data_manager.consultar_pontones()
        codigos_navales = [ponton[0] for ponton in pontones]
        self.codigo_naval_ponton_combobox['values'] = codigos_navales
        
    def refresh_id_centro_anterior_combobox(self):
        centros = self.data_manager.consultar_centros()
        if hasattr(self, 'id_centro_anterior_combobox'):
            self.id_centro_anterior_combobox['values'] = centros

    def refresh_id_centro_nuevo_combobox(self):
        centros = self.data_manager.consultar_centros()
        if centros:
            self.id_centro_nuevo_combobox['values'] = centros
        else:
            self.id_centro_nuevo_combobox['values'] = []

    def add_dispositivo(self):
        serial = self.serial_dispositivo_entry.get().strip()
        direccionamiento_ip = self.direccionamiento_ip_entry.get().strip()
        firmware_version = self.firmware_version_entry.get().strip()
        usuario = self.usuario_entry.get().strip()
        contrasena = self.contrasena_entry.get().strip()
        tipo_dispositivo = self.tipo_dispositivo_combobox.get().strip()
        codigo_naval = self.codigo_naval_dispositivo_combobox.get().strip()

        if not serial or not direccionamiento_ip or not usuario or not contrasena or not tipo_dispositivo or not codigo_naval:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            if tipo_dispositivo == "NIO":
                self.data_manager.insert_nio(serial, direccionamiento_ip, firmware_version, usuario, contrasena, codigo_naval)
            elif tipo_dispositivo == "Radar":
                self.data_manager.insert_radar(serial, direccionamiento_ip, firmware_version, usuario, contrasena, codigo_naval)
            elif tipo_dispositivo == "Asistente Virtual":
                self.data_manager.insert_asistente_virtual(serial, direccionamiento_ip, firmware_version, usuario, contrasena, codigo_naval)
            elif tipo_dispositivo == "Cámara":
                self.data_manager.insert_camara(serial, direccionamiento_ip, firmware_version, usuario, contrasena, codigo_naval)
            
            self.refresh_dispositivo_list()
            self.refresh_serial_dispositivo_combobox()
            self.clear_dispositivo_fields()
            messagebox.showinfo("Éxito", f"Dispositivo '{serial}' insertado correctamente")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar dispositivo: {e}")

    def create_tab_historico_movimientos(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Movimiento Pontones")

        form_frame = ttk.LabelFrame(tab, text="Agregar Histórico de Movimientos")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="Código Naval:").grid(row=0, column=0, padx=5, pady=5)
        self.codigo_naval_historico_var = tk.StringVar()
        self.codigo_naval_historico_combobox = ttk.Combobox(form_frame, textvariable=self.codigo_naval_historico_var)
        self.codigo_naval_historico_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.codigo_naval_historico_combobox.bind("<<ComboboxSelected>>", self.on_codigo_naval_selected)
        self.refresh_codigo_naval_combobox()

        ttk.Label(form_frame, text="Centro Anterior:").grid(row=1, column=0, padx=5, pady=5)
        self.id_centro_anterior_var = tk.StringVar()
        self.id_centro_anterior_entry = ttk.Entry(form_frame, textvariable=self.id_centro_anterior_var, state='readonly')
        self.id_centro_anterior_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Centro Nuevo:").grid(row=2, column=0, padx=5, pady=5)
        self.id_centro_nuevo_var = tk.StringVar()
        self.id_centro_nuevo_combobox = ttk.Combobox(form_frame, textvariable=self.id_centro_nuevo_var)
        self.id_centro_nuevo_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.refresh_id_centro_nuevo_combobox()

        ttk.Label(form_frame, text="Fecha de Instalación:").grid(row=3, column=0, padx=5, pady=5)
        self.fecha_instalacion_mov_var = tk.StringVar()
        self.fecha_instalacion_mov_entry = DateEntry(form_frame, textvariable=self.fecha_instalacion_mov_var, date_pattern='dd-mm-yyyy')
        self.fecha_instalacion_mov_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Fecha de Término:").grid(row=4, column=0, padx=5, pady=5)
        self.fecha_termino_mov_var = tk.StringVar()
        self.fecha_termino_mov_entry = DateEntry(form_frame, textvariable=self.fecha_termino_mov_var, date_pattern='dd-mm-yyyy')
        self.fecha_termino_mov_entry.grid(row=4, column=1, padx=5, pady=5)

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
        codigo_naval = self.codigo_naval_historico_var.get().strip()
        id_centro_anterior = self.id_centro_anterior_var.get().strip()
        id_centro_nuevo = self.id_centro_nuevo_var.get().strip()
        fecha_instalacion_mov = self.fecha_instalacion_mov_var.get().strip()
        fecha_termino_mov = self.fecha_termino_mov_var.get().strip()

        if not codigo_naval or not id_centro_anterior or not id_centro_nuevo or not fecha_instalacion_mov:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        confirm = messagebox.askyesno("Confirmar", "¿Está seguro que desea insertar un histórico de movimiento? Esto provocará que se actualice la ubicación del pontón seleccionado.")
        if not confirm:
            return

        try:
            self.data_manager.insert_historico_movimientos(codigo_naval, id_centro_anterior, id_centro_nuevo, fecha_instalacion_mov, fecha_termino_mov)
            self.refresh_historico_movimientos_list()
            self.refresh_dispositivo_list()
            self.refresh_ponton_list()
            self.refresh_nombre_centro_ponton_combobox()
            self.clear_historico_movimientos_fields()
            messagebox.showinfo("Éxito", "Histórico de movimientos insertado correctamente")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar histórico de movimientos: {e}")

    def clear_historico_movimientos_fields(self):
        self.codigo_naval_historico_var.set('')
        self.id_centro_anterior_var.set('')
        self.id_centro_nuevo_var.set('')
        self.fecha_instalacion_mov_var.set('')
        self.fecha_termino_mov_var.set('')
    
    def clear_dispositivo_fields(self):
        self.serial_dispositivo_entry.delete(0, tk.END)
        self.direccionamiento_ip_entry.delete(0, tk.END)
        self.firmware_version_entry.delete(0, tk.END)
        self.usuario_entry.delete(0, tk.END)
        self.contrasena_entry.delete(0, tk.END)
        self.tipo_dispositivo_combobox.set('')
        self.codigo_naval_dispositivo_combobox.set('')

    def clear_ponton_fields(self):
        self.codigo_naval_var.set('')
        self.nombre_centro_ponton_var.set('')
        self.estado_var.set('')
        self.ia_var.set('')
        self.observaciones_var.set('')
    
    def clear_ubicacion_fields(self):
        self.nombre_centro_var.set('')
        self.grupo_telegram_var.set('')
        self.nombre_empresa_var.set('')
    
    def clear_empresa_fields(self):
        self.nombre_empresa_var.set('')

    def refresh_historico_movimientos_list(self):
        for item in self.historico_movimientos_tree.get_children():
            self.historico_movimientos_tree.delete(item)
        movimientos = self.data_manager.consultar_historico_movimientos()
        for movimiento in movimientos:
            fecha_instalacion_mov = movimiento[3].strftime("%d-%m-%Y") if movimiento[3] else "N/A"
            fecha_termino_mov = movimiento[4].strftime("%d-%m-%Y") if movimiento[4] else "N/A"
            self.historico_movimientos_tree.insert("", "end", values=(movimiento[0], movimiento[1], movimiento[2], fecha_instalacion_mov, fecha_termino_mov))
        
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
        self.fecha_instalacion_disp_var = tk.StringVar()
        self.fecha_instalacion_disp_entry = DateEntry(form_frame, textvariable=self.fecha_instalacion_disp_var, date_pattern='dd-mm-yyyy')
        self.fecha_instalacion_disp_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Fecha de Término:").grid(row=4, column=0, padx=5, pady=5)
        self.fecha_termino_disp_var = tk.StringVar()
        self.fecha_termino_disp_entry = DateEntry(form_frame, textvariable=self.fecha_termino_disp_var, date_pattern='dd-mm-yyyy')
        self.fecha_termino_disp_entry.grid(row=4, column=1, padx=5, pady=5)

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

    def on_serial_dispositivo_selected(self, event):
        serial = self.serial_dispositivo_var.get()
        codigo_naval_anterior = self.data_manager.consultar_codigo_naval_anterior(serial)
        self.codigo_naval_anterior_var.set(codigo_naval_anterior)
        self.codigo_naval_anterior_entry.config(state='readonly')

        codigos_navales_disponibles = self.data_manager.consultar_codigos_navales()
        self.codigo_naval_nuevo_combobox['values'] = [codigo for codigo in codigos_navales_disponibles if codigo != codigo_naval_anterior]
    
    def on_codigo_naval_selected(self, event):
        codigo_naval = self.codigo_naval_historico_var.get()
        centro_anterior = self.data_manager.consultar_centro_por_codigo_naval(codigo_naval)
        self.id_centro_anterior_var.set(centro_anterior)
        self.id_centro_anterior_entry.config(state='readonly')

        centros_disponibles = self.data_manager.consultar_centros()
        self.id_centro_nuevo_combobox['values'] = [centro for centro in centros_disponibles if centro != centro_anterior]

    def refresh_codigo_naval_combobox(self):
        codigos_navales = self.data_manager.consultar_codigos_navales()
        self.codigo_naval_historico_combobox['values'] = codigos_navales

    def refresh_historico_list(self):
        for item in self.historico_tree.get_children():
            self.historico_tree.delete(item)
        movimientos = self.data_manager.consultar_historico_movimientos()
        for movimiento in movimientos:
            fecha_instalacion = movimiento[4].strftime("%d-%m-%Y") if movimiento[4] else "N/A"
            fecha_termino = movimiento[5].strftime("%d-%m-%Y") if movimiento[5] else "N/A"
            self.historico_tree.insert("", "end", values=(movimiento[0], movimiento[1], movimiento[2], movimiento[3], fecha_instalacion, fecha_termino))

    def refresh_historico_dispositivos_list(self):
        for item in self.historico_dispositivos_tree.get_children():
            self.historico_dispositivos_tree.delete(item)
        dispositivos = self.data_manager.consultar_historico_dispositivos()
        for dispositivo in dispositivos:
            fecha_instalacion_disp = dispositivo[3].strftime("%d-%m-%Y") if dispositivo[3] else "N/A"
            fecha_termino_disp = dispositivo[4].strftime("%d-%m-%Y") if dispositivo[4] else "N/A"
            self.historico_dispositivos_tree.insert("", "end", values=(dispositivo[0], dispositivo[1], dispositivo[2], fecha_instalacion_disp, fecha_termino_disp))
            
    def refresh_serial_dispositivo_combobox(self):
        dispositivos = self.data_manager.consultar_dispositivos()
        seriales = [dispositivo[0] for dispositivo in dispositivos]
        self.serial_dispositivo_combobox['values'] = seriales
    
    def refresh_codigo_naval_anterior_combobox(self):
        pontones = self.data_manager.consultar_pontones()
        codigos_navales = [ponton[0] for ponton in pontones]
        if hasattr(self, 'codigo_naval_anterior_combobox'):
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
        serial = self.serial_dispositivo_var.get().strip()
        codigo_naval_anterior = self.codigo_naval_anterior_var.get().strip()
        codigo_naval_nuevo = self.codigo_naval_nuevo_var.get().strip()
        fecha_instalacion_disp = self.fecha_instalacion_disp_var.get().strip()
        fecha_termino_disp = self.fecha_termino_disp_var.get().strip()

        if not serial or not codigo_naval_anterior or not codigo_naval_nuevo or not fecha_instalacion_disp:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        confirm = messagebox.askyesno("Confirmar", "¿Está seguro que desea insertar un histórico de dispositivo? Esto provocará que se actualice la ubicación del dispositivo seleccionado.")
        if not confirm:
            return

        try:
            self.data_manager.insert_historico_dispositivos(serial, codigo_naval_anterior, codigo_naval_nuevo, fecha_instalacion_disp, fecha_termino_disp)
            self.refresh_historico_dispositivos_list()
            self.refresh_dispositivo_list()
            self.clear_historico_dispositivos_fields()
            messagebox.showinfo("Éxito", "Histórico de dispositivos insertado correctamente")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar histórico de dispositivos: {e}")

    def clear_historico_dispositivos_fields(self):
        self.serial_dispositivo_var.set('')
        self.codigo_naval_anterior_var.set('')
        self.codigo_naval_nuevo_var.set('')
        self.fecha_instalacion_disp_var.set('')
        self.fecha_termino_disp_var.set('')


