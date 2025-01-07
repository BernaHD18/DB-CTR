import psycopg2

class MainMenu:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def show_menu(self):
        while True:
            print("\nMenú Principal")
            print("1. Insertar datos")
            print("2. Consultar datos")
            print("3. Salir")
            
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.insert_data_menu()
            elif opcion == "2":
                self.consult_data_menu()
            elif opcion == "3":
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
            print("8. Insertar Histórico de Movimientos")
            print("9. Insertar Histórico de Dispositivos")
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
                estado = input("Ingrese el estado (True/False): ") == "True"
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
            elif opcion == "8":
                codigo_naval = input("Ingrese el código naval: ")
                id_centro_anterior = input("Ingrese el ID del centro anterior: ")
                id_centro_nuevo = input("Ingrese el ID del centro nuevo: ")
                fecha_instalacion_centro = input("Ingrese la fecha de instalación (YYYY-MM-DD): ")
                fecha_termino_centro = input("Ingrese la fecha de término (YYYY-MM-DD): ")
                self.data_manager.insert_historico_movimientos(codigo_naval, id_centro_anterior, id_centro_nuevo, fecha_instalacion_centro, fecha_termino_centro)
            elif opcion == "9":
                serial = input("Ingrese el serial del dispositivo: ")
                id_codigo_naval_anterior = input("Ingrese el ID del código naval anterior: ")
                id_codigo_naval_nuevo = input("Ingrese el ID del código naval nuevo: ")
                fecha_instalacion_dispositivo = input("Ingrese la fecha de instalación (YYYY-MM-DD): ")
                fecha_termino_dispositivo = input("Ingrese la fecha de término (YYYY-MM-DD): ")
                self.data_manager.insert_historico_dispositivos(serial, id_codigo_naval_anterior, id_codigo_naval_nuevo, fecha_instalacion_dispositivo, fecha_termino_dispositivo)
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
            print("5. Consultar Historial de Movimientos")
            print("6. Consultar Historial de Dispositivos")
            print("0. Volver al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                empresas = self.data_manager.consultar_empresas()
                print("\nEmpresas registradas:")
                for empresa in empresas:
                    print(empresa)
            elif opcion == "2":
                ubicaciones = self.data_manager.consultar_ubicaciones()
                print("\nUbicaciones registradas:")
                for ubicacion in ubicaciones:
                    print(ubicacion)
            elif opcion == "3":
                pontones = self.data_manager.consultar_pontones()
                print("\nPontones registrados:")
                for ponton in pontones:
                    print(ponton)
            elif opcion == "4":
                dispositivos = self.data_manager.consultar_dispositivos()
                print("\nDispositivos registrados:")
                for dispositivo in dispositivos:
                    print(dispositivo)
            elif opcion == "5":
                movimientos = self.data_manager.consultar_historico_movimientos()
                print("\nHistórico de Movimientos:")
                for movimiento in movimientos:
                    print(movimiento)
            elif opcion == "6":
                dispositivos_historial = self.data_manager.consultar_historico_dispositivos()
                print("\nHistórico de Dispositivos:")
                for dispositivo in dispositivos_historial:
                    print(dispositivo)
            elif opcion == "0":
                break
            else:
                print("Opción no válida, intente nuevamente.")
