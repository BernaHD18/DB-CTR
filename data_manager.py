import logging

class DataManager:
    def __init__(self, connection):
        self.connection = connection

    def insert_empresa(self, nombre_empresa):
        try:
            self.connection.cur.execute("INSERT INTO Empresa (Nombre_Empresa) VALUES (%s);", (nombre_empresa,))
            self.connection.conn.commit()
            logging.info(f"Empresa '{nombre_empresa}' insertada correctamente")
        except Exception as e:
            logging.error(f"Error al insertar empresa: {e}")
    
    def delete_empresa(self, nombre_empresa):
        try:
            self.connection.cur.execute("DELETE FROM Empresa WHERE Nombre_Empresa = %s;", (nombre_empresa,))
            self.connection.conn.commit()
            logging.info(f"Empresa '{nombre_empresa}' borrada correctamente")
        except Exception as e:
            logging.error(f"Error al borrar empresa: {e}")


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

    def delete_ubicacion(self, nombre_centro):
        try:
            self.connection.cur.execute("DELETE FROM Ubicacion WHERE Nombre_Centro = %s;", (nombre_centro,))
            self.connection.conn.commit()
            logging.info(f"Ubicación '{nombre_centro}' borrada correctamente")
        except Exception as e:
            logging.error(f"Error al borrar ubicación: {e}")

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

    def insert_dispositivo(self, serial, direccionamiento_ip, firmware, usuario, contrasena):
        try:
            # Insertar credenciales y obtener el ID generado
            self.connection.cur.execute("""
                INSERT INTO Credenciales (Usuario, Contraseña)
                VALUES (%s, %s)
                RETURNING ID_Credenciales;
            """, (usuario, contrasena))
            id_credenciales = self.connection.cur.fetchone()[0]
            logging.info(f"Credenciales insertadas correctamente con ID: {id_credenciales}")

            # Insertar dispositivo con el ID de credenciales
            self.connection.cur.execute("""
                INSERT INTO Dispositivos (Serial, Direccionamiento_IP, Firmware_Version, ID_Credenciales)
                VALUES (%s, %s, %s, %s);
            """, (serial, direccionamiento_ip, firmware, id_credenciales))
            self.connection.conn.commit()
            logging.info(f"Dispositivo '{serial}' insertado correctamente")
        except Exception as e:
            logging.error(f"Error al insertar dispositivo: {e}")
            self.connection.conn.rollback()

    def insert_nio(self, serial, modelo, direccionamiento_ip, firmware_version, usuario, contrasena):
        try:
            self.insert_dispositivo(serial, direccionamiento_ip, firmware_version, usuario, contrasena)
            self.connection.cur.execute("""
                INSERT INTO NIO (Serial, Modelo)
                VALUES (%s, %s);
            """, (serial, modelo))
            self.connection.conn.commit()
            logging.info(f"NIO '{serial}' insertado correctamente")
        except Exception as e:
            logging.error(f"Error al insertar NIO: {e}")
            self.connection.conn.rollback()

    def insert_radar(self, serial, canal_rf, direccionamiento_ip, firmware_version, usuario, contrasena):
        try:
            self.insert_dispositivo(serial, direccionamiento_ip, firmware_version, usuario, contrasena)
            self.connection.cur.execute("""
                INSERT INTO Radar (Serial, Canal_RF)
                VALUES (%s, %s);
            """, (serial, canal_rf))
            self.connection.conn.commit()
            logging.info(f"Radar '{serial}' insertado correctamente")
        except Exception as e:
            logging.error(f"Error al insertar Radar: {e}")
            self.connection.conn.rollback()

    def insert_asistente_virtual(self, serial, direccionamiento_ip, firmware_version, usuario, contrasena):
        try:
            self.insert_dispositivo(serial, direccionamiento_ip, firmware_version, usuario, contrasena)
            self.connection.cur.execute("""
                INSERT INTO Asistente_Virtual (Serial)
                VALUES (%s);
            """, (serial,))
            self.connection.conn.commit()
            logging.info(f"Asistente Virtual '{serial}' insertado correctamente")
        except Exception as e:
            logging.error(f"Error al insertar Asistente Virtual: {e}")
            self.connection.conn.rollback()

    def insert_camara(self, serial, direccionamiento_ip, firmware_version, usuario, contrasena):
        try:
            self.insert_dispositivo(serial, direccionamiento_ip, firmware_version, usuario, contrasena)
            self.connection.cur.execute("""
                INSERT INTO Camara (Serial)
                VALUES (%s);
            """, (serial,))
            self.connection.conn.commit()
            logging.info(f"Cámara '{serial}' insertada correctamente")
        except Exception as e:
            logging.error(f"Error al insertar Cámara: {e}")
            self.connection.conn.rollback()

    def insert_ponton(self, codigo_naval, nombre_centro, estado, ia, observaciones):
        try:
            # Verificar si el código naval ya está asociado a otro centro
            self.connection.cur.execute("SELECT Nombre_Centro FROM Ponton WHERE Codigo_Naval = %s;", (codigo_naval,))
            resultado = self.connection.cur.fetchone()
            if resultado and resultado[0] != nombre_centro:
                raise ValueError(f"El código naval '{codigo_naval}' ya está asociado al centro '{resultado[0]}'")

            # Verificar si el centro ya está asociado a otro código naval
            self.connection.cur.execute("SELECT Codigo_Naval FROM Ponton WHERE Nombre_Centro = %s;", (nombre_centro,))
            resultado = self.connection.cur.fetchone()
            if resultado and resultado[0] != codigo_naval:
                raise ValueError(f"El centro '{nombre_centro}' ya está asociado al código naval '{resultado[0]}'")

            # Insertar el nuevo pontón
            self.connection.cur.execute("""
                INSERT INTO Ponton (Codigo_Naval, Nombre_Centro, Estado, IA, Observaciones)
                VALUES (%s, %s, %s, %s, %s);
            """, (codigo_naval, nombre_centro, estado, ia, observaciones))
            self.connection.conn.commit()
            logging.info(f"Pontón '{codigo_naval}' insertado correctamente")
        except Exception as e:
            logging.error(f"Error al insertar pontón: {e}")
            self.connection.conn.rollback()

    def consultar_centros(self):
        try:
            self.connection.cur.execute("""
                SELECT Nombre_Centro 
                FROM Ubicacion 
                WHERE Nombre_Centro NOT IN (SELECT Nombre_Centro FROM Ponton);
            """)
            resultados = self.connection.cur.fetchall()
            return [resultado[0] for resultado in resultados]
        except Exception as e:
            logging.error(f"Error al consultar centros: {e}")
            return []
    
    def delete_ponton(self, codigo_naval):
        try:
            self.connection.cur.execute("DELETE FROM Ponton WHERE Codigo_Naval = %s;", (codigo_naval,))
            self.connection.conn.commit()
            logging.info(f"Pontón '{codigo_naval}' borrado correctamente")
        except Exception as e:
            logging.error(f"Error al borrar pontón: {e}")
            raise
        
    def insert_dispositivo_ponton(self, codigo_naval_ponton, serial, tipo_dispositivo):
        try:
            self.connection.cur.execute("""
                INSERT INTO Ponton_Dispositivos (codigo_naval, serial_dispositivo, tipo_dispositivo)
                VALUES (%s, %s, %s);
            """, (codigo_naval_ponton, serial, tipo_dispositivo))
            self.connection.conn.commit()
            logging.info(f"Dispositivo '{serial}' asociado al pontón '{codigo_naval_ponton}' como '{tipo_dispositivo}'")
        except Exception as e:
            logging.error(f"Error al asociar dispositivo al pontón: {e}")
            self.connection.conn.rollback()



    def insert_historico_movimientos(self, codigo_naval, id_centro_anterior, id_centro_nuevo, fecha_instalacion_centro, fecha_termino_centro):
        try:
            # Insertar en la tabla Historico_Movimientos
            self.connection.cur.execute("""
                INSERT INTO Historico_Movimientos (Codigo_Naval, ID_CentroAnterior, ID_CentroNuevo, Fecha_Instalacion_Centro, Fecha_Termino_Centro)
                VALUES (%s, %s, %s, %s, %s);
            """, (codigo_naval, id_centro_anterior, id_centro_nuevo, fecha_instalacion_centro, fecha_termino_centro))
            
            # Actualizar la tabla Ponton con la nueva ubicación
            self.connection.cur.execute("""
                UPDATE Ponton
                SET Nombre_Centro = %s
                WHERE Codigo_Naval = %s;
            """, (id_centro_nuevo, codigo_naval))
            
            self.connection.conn.commit()
            print("Histórico de movimientos insertado y pontón actualizado correctamente")
        except Exception as e:
            print(f"Error al insertar histórico de movimientos y actualizar pontón: {e}")

    def insert_historico_dispositivos(self, serial, id_codigo_naval_anterior, id_codigo_naval_nuevo, fecha_instalacion_dispositivo, fecha_termino_dispositivo):
        try:
            # Insertar en la tabla Historico_Dispositivos
            self.connection.cur.execute("""
                INSERT INTO Historico_Dispositivos (Serial, ID_Codigo_NavalAnterior, ID_Codigo_NavalNuevo, Fecha_Instalacion_Dispositivo, Fecha_Termino_Dispositivo)
                VALUES (%s, %s, %s, %s, %s);
            """, (serial, id_codigo_naval_anterior, id_codigo_naval_nuevo, fecha_instalacion_dispositivo, fecha_termino_dispositivo))
            
            # Actualizar la tabla Dispositivos con la nueva ubicación
            self.connection.cur.execute("""
                UPDATE Dispositivos
                SET ID_Codigo_Naval = %s
                WHERE Serial = %s;
            """, (id_codigo_naval_nuevo, serial))
            
            self.connection.conn.commit()
            print("Histórico de dispositivos insertado y dispositivo actualizado correctamente")
        except Exception as e:
            print(f"Error al insertar histórico de dispositivos y actualizar dispositivo: {e}")


    def consultar_empresas(self):
        try:
            self.connection.cur.execute("SELECT Nombre_Empresa FROM Empresa;")
            resultados = self.connection.cur.fetchall()
            return resultados
        except Exception as e:
            logging.error(f"Error al consultar empresas: {e}")
            return []
        
    def consultar_ubicaciones(self):
        try:
            self.connection.cur.execute("SELECT * FROM Ubicacion;")
            resultados = self.connection.cur.fetchall()
            return resultados
        except Exception as e:
            print(f"Error al consultar ubicaciones: {e}")

    def consultar_pontones(self):
        try:
            self.connection.cur.execute("SELECT Codigo_Naval, Nombre_Centro, Estado, IA, Observaciones FROM Ponton;")
            resultados = self.connection.cur.fetchall()
            return resultados
        except Exception as e:
            logging.error(f"Error al consultar pontones: {e}")
            return []

    def consultar_dispositivos(self):
        try:
            self.connection.cur.execute("""
                SELECT d.Serial, d.Direccionamiento_IP, d.Firmware_Version, c.Usuario, c.Contraseña
                FROM Dispositivos d
                JOIN Credenciales c ON d.ID_Credenciales = c.ID_Credenciales;
            """)
            dispositivos = self.connection.cur.fetchall()
            return dispositivos if dispositivos else []
        except Exception as e:
            logging.error(f"Error al consultar dispositivos: {e}")
            return []
        
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

    def consultar_dispositivos_ponton(self, codigo_naval):
        try:
            self.connection.cur.execute("""
                SELECT d.Serial, d.Direccionamiento_IP, d.Firmware_Version, d.ID_Credenciales, pd.tipo_dispositivo
                FROM Dispositivos d
                JOIN Ponton_Dispositivos pd ON d.Serial = pd.serial_dispositivo
                WHERE pd.codigo_naval = %s;
            """, (codigo_naval,))
            dispositivos = self.connection.cur.fetchall()

            if not dispositivos:
                return []  # Devolver una lista vacía si no hay dispositivos

            dispositivos_formateados = []
            for dispositivo in dispositivos:
                dispositivos_formateados.append({
                    "Serial": dispositivo[0],
                    "Dirección IP": dispositivo[1],
                    "Firmware": dispositivo[2],
                    "ID Credenciales": dispositivo[3],
                    "Tipo": dispositivo[4]
                })

            return dispositivos_formateados
        except Exception as e:
            print(f"Error al consultar dispositivos en el pontón '{codigo_naval}': {e}")
            return []  # Retornar una lista vacía en caso de error

    def consultar_credenciales(self, serial_dispositivo):
        try:
            self.connection.cur.execute("""
                SELECT c.Usuario, c.Contraseña
                FROM Credenciales c
                JOIN Dispositivos d ON c.ID_Credenciales = d.ID_Credenciales
                WHERE d.Serial = %s;
            """, (serial_dispositivo,))
            credenciales = self.connection.cur.fetchone()

            if not credenciales:
                print(f"No se encontraron credenciales para el dispositivo con serial '{serial_dispositivo}'.")
                return None

            return {
                "Usuario": credenciales[0],
                "Contraseña": credenciales[1]
            }
        except Exception as e:
            print(f"Error al consultar credenciales para el dispositivo '{serial_dispositivo}': {e}")
            return None

    def normalize_input(prompt, to_lower=False, to_bool=False):
        value = input(prompt).strip()  # Elimina espacios extra
        if to_lower:
            value = value.lower()
        if to_bool:
            return value == "true"
        return value


