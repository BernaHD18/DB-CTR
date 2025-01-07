class DataManager:
    def __init__(self, connection):
        self.connection = connection

    def insert_empresa(self, nombre_empresa):
        try:
            self.connection.cur.execute("""
                INSERT INTO Empresa (Nombre_Empresa) VALUES (%s);
            """, (nombre_empresa,))
            self.connection.conn.commit()
            print(f"Empresa '{nombre_empresa}' insertada correctamente")
        except Exception as e:
            print(f"Error al insertar empresa: {e}")

    def insert_ubicacion(self, nombre_centro, grupo_telegram, nombre_empresa):
        try:
            self.connection.cur.execute("""
                INSERT INTO Ubicacion (Nombre_Centro, Grupo_Telegram, Nombre_Empresa)
                VALUES (%s, %s, %s);
            """, (nombre_centro, grupo_telegram, nombre_empresa))
            self.connection.conn.commit()
            print(f"Ubicación '{nombre_centro}' insertada correctamente")
        except Exception as e:
            print(f"Error al insertar ubicación: {e}")

    def insert_credenciales(self, usuario, contrasena):
        try:
            self.connection.cur.execute("""
                INSERT INTO Credenciales (Usuario, Contraseña)
                VALUES (%s, %s)
                RETURNING ID_Credenciales;
            """, (usuario, contrasena))
            id_credenciales = self.connection.cur.fetchone()[0]
            self.connection.conn.commit()
            print(f"Credenciales insertadas correctamente con ID: {id_credenciales}")
            return id_credenciales
        except Exception as e:
            print(f"Error al insertar credenciales: {e}")

    def insert_dispositivo(self, serial, direccionamiento_ip, firmware_version, id_credenciales):
        try:
            self.connection.cur.execute("""
                INSERT INTO Dispositivos (Serial, Direccionamiento_IP, Firmware_Version, ID_Credenciales)
                VALUES (%s, %s, %s, %s);
            """, (serial, direccionamiento_ip, firmware_version, id_credenciales))
            self.connection.conn.commit()
            print(f"Dispositivo '{serial}' insertado correctamente")
        except Exception as e:
            print(f"Error al insertar dispositivo: {e}")

    def insert_nio(self, serial, modelo, direccionamiento_ip, firmware_version, usuario, contrasena):
        try:
            id_credenciales = self.insert_credenciales(usuario, contrasena)
            self.insert_dispositivo(serial, direccionamiento_ip, firmware_version, id_credenciales)
            self.connection.cur.execute("""
                INSERT INTO NIO (Serial, Modelo)
                VALUES (%s, %s);
            """, (serial, modelo))
            self.connection.conn.commit()
            print(f"NIO '{serial}' insertado correctamente")
        except Exception as e:
            print(f"Error al insertar NIO: {e}")

    def insert_radar(self, serial, canal_rf, direccionamiento_ip, firmware_version, usuario, contrasena):
        try:
            id_credenciales = self.insert_credenciales(usuario, contrasena)
            self.insert_dispositivo(serial, direccionamiento_ip, firmware_version, id_credenciales)
            self.connection.cur.execute("""
                INSERT INTO Radar (Serial, Canal_RF)
                VALUES (%s, %s);
            """, (serial, canal_rf))
            self.connection.conn.commit()
            print(f"Radar '{serial}' insertado correctamente")
        except Exception as e:
            print(f"Error al insertar Radar: {e}")

    def insert_asistente_virtual(self, serial, direccionamiento_ip, firmware_version, usuario, contrasena):
        try:
            id_credenciales = self.insert_credenciales(usuario, contrasena)
            self.insert_dispositivo(serial, direccionamiento_ip, firmware_version, id_credenciales)
            self.connection.cur.execute("""
                INSERT INTO Asistente_Virtual (Serial)
                VALUES (%s);
            """, (serial,))
            self.connection.conn.commit()
            print(f"Asistente Virtual '{serial}' insertado correctamente")
        except Exception as e:
            print(f"Error al insertar Asistente Virtual: {e}")

    def insert_camara(self, serial, direccionamiento_ip, firmware_version, usuario, contrasena):
        try:
            id_credenciales = self.insert_credenciales(usuario, contrasena)
            self.insert_dispositivo(serial, direccionamiento_ip, firmware_version, id_credenciales)
            self.connection.cur.execute("""
                INSERT INTO Camara (Serial)
                VALUES (%s);
            """, (serial,))
            self.connection.conn.commit()
            print(f"Cámara '{serial}' insertada correctamente")
        except Exception as e:
            print(f"Error al insertar Cámara: {e}")

    def insert_ponton(self, codigo_naval, nombre_centro, estado, ia, serial_nio, serial_radar, serial_asistente_virtual, serial_camara, observaciones):
        try:
            self.connection.cur.execute("""
                INSERT INTO Ponton (Codigo_Naval, Nombre_Centro, Estado, IA, Serial_NIO, Serial_Radar, Serial_Asistente_Virtual, Serial_Camara, Observaciones)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (codigo_naval, nombre_centro, estado, ia, serial_nio, serial_radar, serial_asistente_virtual, serial_camara, observaciones))
            self.connection.conn.commit()
            print(f"Pontón '{codigo_naval}' insertado correctamente")
        except Exception as e:
            print(f"Error al insertar pontón: {e}")

    def insert_historico_movimientos(self, codigo_naval, id_centro_anterior, id_centro_nuevo, fecha_instalacion_centro, fecha_termino_centro):
        try:
            self.connection.cur.execute("""
                INSERT INTO Historico_Movimientos (Codigo_Naval, ID_CentroAnterior, ID_CentroNuevo, Fecha_Instalacion_Centro, Fecha_Termino_Centro)
                VALUES (%s, %s, %s, %s, %s);
            """, (codigo_naval, id_centro_anterior, id_centro_nuevo, fecha_instalacion_centro, fecha_termino_centro))
            self.connection.conn.commit()
            print("Histórico de movimientos insertado correctamente")
        except Exception as e:
            print(f"Error al insertar histórico de movimientos: {e}")

    def insert_historico_dispositivos(self, serial, id_codigo_naval_anterior, id_codigo_naval_nuevo, fecha_instalacion_dispositivo, fecha_termino_dispositivo):
        try:
            self.connection.cur.execute("""
                INSERT INTO Historico_Dispositivos (Serial, ID_Codigo_NavalAnterior, ID_Codigo_NavalNuevo, Fecha_Instalacion_Dispositivo, Fecha_Termino_Dispositivo)
                VALUES (%s, %s, %s, %s, %s);
            """, (serial, id_codigo_naval_anterior, id_codigo_naval_nuevo, fecha_instalacion_dispositivo, fecha_termino_dispositivo))
            self.connection.conn.commit()
            print("Histórico de dispositivos insertado correctamente")
        except Exception as e:
            print(f"Error al insertar histórico de dispositivos: {e}")

    def consultar_empresas(self):
        try:
            self.connection.cur.execute("SELECT * FROM Empresa;")
            resultados = self.connection.cur.fetchall()
            return resultados
        except Exception as e:
            print(f"Error al consultar empresas: {e}")

    def consultar_ubicaciones(self):
        try:
            self.connection.cur.execute("SELECT * FROM Ubicacion;")
            resultados = self.connection.cur.fetchall()
            return resultados
        except Exception as e:
            print(f"Error al consultar ubicaciones: {e}")

    def consultar_pontones(self):
        try:
            self.connection.cur.execute("SELECT * FROM Ponton;")
            resultados = self.connection.cur.fetchall()
            return resultados
        except Exception as e:
            print(f"Error al consultar pontones: {e}")

    def consultar_dispositivos(self):
        try:
            self.connection.cur.execute("SELECT * FROM Dispositivos;")
            resultados = self.connection.cur.fetchall()
            return resultados
        except Exception as e:
            print(f"Error al consultar dispositivos: {e}")

    def consultar_historico_movimientos(self):
        try:
            self.connection.cur.execute("SELECT * FROM Historico_Movimientos;")
            resultados = self.connection.cur.fetchall()
            return resultados
        except Exception as e:
            print(f"Error al consultar histórico de movimientos: {e}")

    def consultar_historico_dispositivos(self):
        try:
            self.connection.cur.execute("SELECT * FROM Historico_Dispositivos;")
            resultados = self.connection.cur.fetchall()
            return resultados
        except Exception as e:
            print(f"Error al consultar histórico de dispositivos: {e}")
