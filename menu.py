class MainMenu:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def show_menu(self):
        while True:
            print("\nMenú Principal")
            print("1. Insertar datos")
            print("2. Consultar datos")
            print("3. Gestión de Histórico")
            print("4. Salir")
            
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.insert_data_menu()
            elif opcion == "2":
                self.consult_data_menu()
            elif opcion == "3":
                self.gestion_historico_menu()
            elif opcion == "4":
                print("Saliendo del programa.")
                break
            else:
                print("Opción no válida, intente nuevamente.")

    def insert_data_menu(self):
        while True:
            print("\nMenú de Inserción de Datos")
            print("1. Insertar Empresa")
            print("2. Insertar Ubicación")
            print("3. Insertar Pontón")
            print("4. Insertar Dispositivo NIO")
            print("5. Insertar Dispositivo Radar")
            print("6. Insertar Asistente Virtual")
            print("7. Insertar Cámara")
            print("0. Volver al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                nombre_empresa = input("Ingrese el nombre de la empresa: ")
                self.data_manager.insert_empresa(nombre_empresa)
            elif opcion == "2":
                nombre_centro = input("Ingrese el nombre del centro: ")
                grupo_telegram = input("Ingrese el grupo de Telegram: ")
                nombre_empresa = input("Ingrese el nombre de la empresa asociada: ")
                self.data_manager.insert_ubicacion(nombre_centro, grupo_telegram, nombre_empresa)
            elif opcion == "3":
                codigo_naval = input("Ingrese el código naval: ")
                nombre_centro = input("Ingrese el nombre del centro: ")
                estado = input("Ingrese el estado (True/False): ") == "False"
                ia = input("Ingrese IA: ")
                serial_nio = input("Ingrese el serial del NIO: ")
                serial_radar = input("Ingrese el serial del Radar: ")
                serial_asistente_virtual = input("Ingrese el serial del Asistente Virtual: ")
                serial_camara = input("Ingrese el serial de la Cámara: ")
                observaciones = input("Ingrese observaciones: ")
                self.data_manager.insert_ponton(codigo_naval, nombre_centro, estado, ia, serial_nio, serial_radar, serial_asistente_virtual, serial_camara, observaciones)
            elif opcion == "4":
                serial = input("Ingrese el serial del NIO: ")
                modelo = input("Ingrese el modelo: ")
                direccionamiento_ip = input("Ingrese el direccionamiento IP: ")
                firmware_version = input("Ingrese la versión de firmware: ")
                usuario = input("Ingrese el usuario: ")
                contrasena = input("Ingrese la contraseña: ")
                self.data_manager.insert_nio(serial, modelo, direccionamiento_ip, firmware_version, usuario, contrasena)
            elif opcion == "5":
                serial = input("Ingrese el serial del Radar: ")
                canal_rf = input("Ingrese el canal RF: ")
                direccionamiento_ip = input("Ingrese el direccionamiento IP: ")
                firmware_version = input("Ingrese la versión de firmware: ")
                usuario = input("Ingrese el usuario: ")
                contrasena = input("Ingrese la contraseña: ")
                self.data_manager.insert_radar(serial, canal_rf, direccionamiento_ip, firmware_version, usuario, contrasena)
            elif opcion == "6":
                serial = input("Ingrese el serial del Asistente Virtual: ")
                direccionamiento_ip = input("Ingrese el direccionamiento IP: ")
                firmware_version = input("Ingrese la versión de firmware: ")
                usuario = input("Ingrese el usuario: ")
                contrasena = input("Ingrese la contraseña: ")
                self.data_manager.insert_asistente_virtual(serial, direccionamiento_ip, firmware_version, usuario, contrasena)
            elif opcion == "7":
                serial = input("Ingrese el serial de la Cámara: ")
                direccionamiento_ip = input("Ingrese el direccionamiento IP: ")
                firmware_version = input("Ingrese la versión de firmware: ")
                usuario = input("Ingrese el usuario: ")
                contrasena = input("Ingrese la contraseña: ")
                self.data_manager.insert_camara(serial, direccionamiento_ip, firmware_version, usuario, contrasena)
            elif opcion == "0":
                break
            else:
                print("Opción no válida, intente nuevamente.")

    def consult_data_menu(self):
        while True:
            print("\nMenú de Consultas")
            print("1. Consultar todas las Empresas")
            print("2. Consultar todas las Ubicaciones")
            print("3. Consultar todos los Pontones")
            print("4. Consultar todos los Dispositivos")
            print("0. Volver al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":  # Consultar Empresas
                empresas = self.data_manager.consultar_empresas()
                if empresas:
                    print("\nEmpresas registradas:")
                    print(f"{'Nombre de Empresa':<30}")
                    print("=" * 30)
                    for empresa in empresas:
                        print(f"{empresa[0]:<30}")
                else:
                    print("No se encontraron empresas registradas.")

            elif opcion == "2":  # Consultar Ubicaciones
                ubicaciones = self.data_manager.consultar_ubicaciones()
                if ubicaciones:
                    print("\nUbicaciones registradas:")
                    print(f"{'Nombre del Centro':<30} {'Grupo de Telegram':<30} {'Nombre de Empresa':<30}")
                    print("=" * 90)
                    for ubicacion in ubicaciones:
                        print(f"{ubicacion[0]:<30} {ubicacion[1]:<30} {ubicacion[2]:<30}")
                else:
                    print("No se encontraron ubicaciones registradas.")

            elif opcion == "3":  # Consultar Pontones
                pontones = self.data_manager.consultar_pontones()
                if pontones:
                    print("\nPontones registrados:")
                    print(f"{'Codigo Naval':<15} {'Nombre del Centro':<22} {'Estado':<10} {'IA':<25} {'Serial nio':<15} {'Serial radar':<15}")
                    print("=" * 107)
                    for ponton in pontones:
                        estado = "Activo" if ponton[2] else "Inactivo"
                        print(f"{ponton[0]:<15} {ponton[1]:<22} {estado:<10} {ponton[3]:<25} {ponton[4]:<15} {ponton[5]:<15}")
                else:
                    print("No se encontraron pontones registrados.")
            elif opcion == "4":
                dispositivos = self.data_manager.consultar_dispositivos()
            elif opcion == "0":
                break
            else:
                print("Opción no válida, intente nuevamente.")

    def gestion_historico_menu(self):
        while True:
            print("\nGestión de Histórico")
            print("1. Insertar Histórico de Movimientos")
            print("2. Insertar Histórico de Dispositivos")
            print("3. Consultar Histórico de Movimientos")
            print("4. Consultar Histórico de Dispositivos")
            print("0. Volver al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                codigo_naval = input("Ingrese el código naval: ")
                id_centro_anterior = input("Ingrese el ID del centro anterior: ")
                id_centro_nuevo = input("Ingrese el ID del centro nuevo: ")
                fecha_instalacion_centro = input("Ingrese la fecha de instalación (YYYY-MM-DD): ")
                fecha_termino_centro = input("Ingrese la fecha de término (YYYY-MM-DD): ")
                self.data_manager.insert_historico_movimientos(codigo_naval, id_centro_anterior, id_centro_nuevo, fecha_instalacion_centro, fecha_termino_centro)
            elif opcion == "2":
                serial = input("Ingrese el serial del dispositivo: ")
                id_codigo_naval_anterior = input("Ingrese el ID del código naval anterior: ")
                id_codigo_naval_nuevo = input("Ingrese el ID del código naval nuevo: ")
                fecha_instalacion_dispositivo = input("Ingrese la fecha de instalación (YYYY-MM-DD): ")
                fecha_termino_dispositivo = input("Ingrese la fecha de término (YYYY-MM-DD): ")
                self.data_manager.insert_historico_dispositivos(serial, id_codigo_naval_anterior, id_codigo_naval_nuevo, fecha_instalacion_dispositivo, fecha_termino_dispositivo)
            elif opcion == "3":  # Consultar Histórico de Movimientos
                movimientos = self.data_manager.consultar_historico_movimientos()
                if movimientos:
                    print("\nHistórico de Movimientos:")
                    print(f"{'ID Movimiento':<18} {'Codigo Naval':<16} {'ID Centro Anterior':<22} {'ID Centro Nuevo':<20} {'Fecha de Instalacion':<27} {'Fecha de Termino':<20}")
                    print("=" * 125)  # Ajustamos el separador para que coincida con el número de columnas
                    for movimiento in movimientos:
                        fecha_instalacion = movimiento[4].strftime("%Y-%m-%d") if movimiento[4] else "N/A"
                        fecha_termino = movimiento[5].strftime("%Y-%m-%d") if movimiento[5] else "N/A"
                        
                        # Aquí aseguramos que cada columna tenga suficiente espacio
                        print(f"{movimiento[0]:<18} {movimiento[1]:<16} {movimiento[2]:<22} {movimiento[3]:<20} {fecha_instalacion:<27} {fecha_termino:<20}")
                else:
                    print("No se encontraron registros en el histórico de movimientos.")
            elif opcion == "4":  # Consultar Histórico de Dispositivos
                historico_dispositivos = self.data_manager.consultar_historico_dispositivos()
                if historico_dispositivos:
                    print("\nHistórico de Dispositivos:")
                    print(f"{'ID Mov_Dispositivo':<22} {'Serial':<10} {'Codigo Naval Anterior':<24} {'Codigo Naval Nuevo':<22} {'Fecha de Instalacion':<23} {'Fecha de Termino':<20}")
                    print("=" * 125)  # Ajustamos el separador a 140 caracteres
                    for dispositivo in historico_dispositivos:
                        # Formatear las fechas adecuadamente con strftime
                        fecha_instalacion = dispositivo[4].strftime("%Y-%m-%d") if dispositivo[4] else "N/A"
                        fecha_termino = dispositivo[5].strftime("%Y-%m-%d") if dispositivo[5] else "N/A"
                        
                        # Aquí aseguramos que cada columna tenga suficiente espacio
                        print(f"{dispositivo[0]:<22} {dispositivo[1]:<10} {dispositivo[2]:<24} {dispositivo[3]:<22} {fecha_instalacion:<23} {fecha_termino:<20}")
                else:
                    print("No se encontraron registros en el histórico de dispositivos.")
            elif opcion == "0":
                break
            else:
                print("Opción no válida, intente nuevamente.")
