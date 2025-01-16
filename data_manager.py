import logging
import psycopg2

class DataManager:
    def __init__(self, connection):
        self.connection = connection

    def insert_empresa(self, nombre_empresa):
        if not nombre_empresa or nombre_empresa.isspace():
            raise ValueError("El campo nombre de la empresa es obligatorio")
        try:
            # Verificar si la empresa ya existe
            self.connection.cur.execute("SELECT COUNT(*) FROM Empresa WHERE Nombre_Empresa = %s;", (nombre_empresa,))
            if self.connection.cur.fetchone()[0] > 0:
                raise ValueError(f"La empresa '{nombre_empresa}' ya existe.")
            
            self.connection.cur.execute("""
                INSERT INTO Empresa (Nombre_Empresa) VALUES (%s);
            """, (nombre_empresa,))
            self.connection.conn.commit()
            logging.info(f"Empresa '{nombre_empresa}' insertada correctamente")
        except ValueError as ve:
            logging.error(f"Error al insertar empresa: {ve}")
            self.connection.conn.rollback()
            raise ve
        except Exception as e:
            logging.error(f"Error al insertar empresa: {e}")
            self.connection.conn.rollback()
            raise e

    def delete_empresa(self, nombre_empresa):
        try:
            self.connection.cur.execute("DELETE FROM Empresa WHERE Nombre_Empresa = %s;", (nombre_empresa,))
            self.connection.conn.commit()
            logging.info(f"Empresa '{nombre_empresa}' borrada correctamente")
        except Exception as e:
            logging.error(f"Error al borrar empresa: {e}")
            self.connection.conn.rollback()
            raise e

    def delete_dispositivo(self, serial):
        try:
            # Obtener el tipo de dispositivo
            self.connection.cur.execute("SELECT tipo_dispositivo FROM Ponton_Dispositivos WHERE serial_dispositivo = %s;", (serial,))
            tipo_dispositivo = self.connection.cur.fetchone()
            
            if tipo_dispositivo:
                tipo_dispositivo = tipo_dispositivo[0]
                # Borrar el dispositivo de su tabla específica
                if tipo_dispositivo == "NIO":
                    self.connection.cur.execute("DELETE FROM NIO WHERE Serial = %s;", (serial,))
                elif tipo_dispositivo == "Radar":
                    self.connection.cur.execute("DELETE FROM Radar WHERE Serial = %s;", (serial,))
                elif tipo_dispositivo == "Asistente Virtual":
                    self.connection.cur.execute("DELETE FROM Asistente_Virtual WHERE Serial = %s;", (serial,))
                elif tipo_dispositivo == "Cámara":
                    self.connection.cur.execute("DELETE FROM Camara WHERE Serial = %s;", (serial,))

            # Borrar la relación con el código naval en Ponton_Dispositivos
            self.connection.cur.execute("DELETE FROM Ponton_Dispositivos WHERE serial_dispositivo = %s;", (serial,))
            
            # Obtener el ID de credenciales antes de borrar el dispositivo
            self.connection.cur.execute("SELECT ID_Credenciales FROM Dispositivos WHERE Serial = %s;", (serial,))
            id_credenciales = self.connection.cur.fetchone()
            
            # Borrar el dispositivo de la tabla Dispositivos
            self.connection.cur.execute("DELETE FROM Dispositivos WHERE Serial = %s;", (serial,))
            
            # Borrar las credenciales asociadas
            if id_credenciales:
                self.connection.cur.execute("DELETE FROM Credenciales WHERE ID_Credenciales = %s;", (id_credenciales[0],))
            
            self.connection.conn.commit()
            logging.info(f"Dispositivo '{serial}' borrado correctamente")
        except psycopg2.errors.ForeignKeyViolation as e:
            logging.error(f"Error al borrar dispositivo: {e}")
            self.connection.conn.rollback()
            raise ValueError(f"No se puede borrar el dispositivo '{serial}' porque está referenciado en otra tabla.")
        except Exception as e:
            logging.error(f"Error al borrar dispositivo: {e}")
            self.connection.conn.rollback()
            raise e

    def insert_ubicacion(self, nombre_centro, grupo_telegram, nombre_empresa):
        try:
            self.connection.cur.execute("""
                INSERT INTO Ubicacion (Nombre_Centro, Grupo_Telegram, Nombre_Empresa)
                VALUES (%s, %s, %s);
            """, (nombre_centro, grupo_telegram, nombre_empresa))
            self.connection.conn.commit()
            logging.info(f"Ubicación '{nombre_centro}' insertada correctamente")
        except psycopg2.errors.UniqueViolation as e:
            logging.error(f"Error al insertar ubicación: {e}")
            self.connection.conn.rollback()
            raise ValueError(f"La ubicación con nombre de centro '{nombre_centro}' ya existe.")
        except Exception as e:
            logging.error(f"Error al insertar ubicación: {e}")
            self.connection.conn.rollback()
            raise e

    def delete_ubicacion(self, nombre_centro):
        try:
            self.connection.cur.execute("DELETE FROM Ubicacion WHERE Nombre_Centro = %s;", (nombre_centro,))
            self.connection.conn.commit()
            logging.info(f"Ubicación '{nombre_centro}' borrada correctamente")
        except psycopg2.errors.ForeignKeyViolation as e:
            logging.error(f"Error al borrar ubicación: {e}")
            self.connection.conn.rollback()
            raise ValueError(f"No se puede borrar la ubicación '{nombre_centro}' porque está referenciada en otra tabla.")
        except Exception as e:
            logging.error(f"Error al borrar ubicación: {e}")
            self.connection.conn.rollback()
            raise e

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
        except psycopg2.errors.UniqueViolation as e:
            logging.error(f"Error al insertar dispositivo: {e}")
            self.connection.conn.rollback()
            raise ValueError(f"El dispositivo con serial '{serial}' ya existe.")
        except Exception as e:
            logging.error(f"Error al insertar dispositivo: {e}")
            self.connection.conn.rollback()
            raise e
        
    def insert_nio(self, serial, direccionamiento_ip, firmware_version, usuario, contrasena, codigo_naval_ponton):
        try:
            self.insert_dispositivo(serial, direccionamiento_ip, firmware_version, usuario, contrasena)
            self.connection.cur.execute("""
                INSERT INTO NIO (Serial, Modelo)
                VALUES (%s, %s);
            """, (serial, "Modelo NIO"))
            self.insert_dispositivo_ponton(codigo_naval_ponton, serial, "NIO")
            self.connection.conn.commit()
            logging.info(f"NIO '{serial}' insertado correctamente")
        except Exception as e:
            logging.error(f"Error al insertar NIO: {e}")
            self.connection.conn.rollback()
            raise e

    def insert_radar(self, serial, direccionamiento_ip, firmware_version, usuario, contrasena, codigo_naval_ponton):
        try:
            self.insert_dispositivo(serial, direccionamiento_ip, firmware_version, usuario, contrasena)
            self.connection.cur.execute("""
                INSERT INTO Radar (Serial, Canal_RF)
                VALUES (%s, %s);
            """, (serial, "Canal RF"))
            self.insert_dispositivo_ponton(codigo_naval_ponton, serial, "Radar")
            self.connection.conn.commit()
            logging.info(f"Radar '{serial}' insertado correctamente")
        except Exception as e:
            logging.error(f"Error al insertar Radar: {e}")
            self.connection.conn.rollback()
            raise e

    def insert_asistente_virtual(self, serial, direccionamiento_ip, firmware_version, usuario, contrasena, codigo_naval_ponton):
        try:
            self.insert_dispositivo(serial, direccionamiento_ip, firmware_version, usuario, contrasena)
            self.connection.cur.execute("""
                INSERT INTO Asistente_Virtual (Serial)
                VALUES (%s);
            """, (serial,))
            self.insert_dispositivo_ponton(codigo_naval_ponton, serial, "Asistente Virtual")
            self.connection.conn.commit()
            logging.info(f"Asistente Virtual '{serial}' insertado correctamente")
        except Exception as e:
            logging.error(f"Error al insertar Asistente Virtual: {e}")
            self.connection.conn.rollback()
            raise e

    def insert_camara(self, serial, direccionamiento_ip, firmware_version, usuario, contrasena, codigo_naval_ponton):
        try:
            self.insert_dispositivo(serial, direccionamiento_ip, firmware_version, usuario, contrasena)
            self.connection.cur.execute("""
                INSERT INTO Camara (Serial)
                VALUES (%s);
            """, (serial,))
            self.insert_dispositivo_ponton(codigo_naval_ponton, serial, "Cámara")
            self.connection.conn.commit()
            logging.info(f"Cámara '{serial}' insertada correctamente")
        except Exception as e:
            logging.error(f"Error al insertar Cámara: {e}")
            self.connection.conn.rollback()
            raise e

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
        except psycopg2.errors.UniqueViolation as e:
            logging.error(f"Error al insertar pontón: {e}")
            self.connection.conn.rollback()
            raise ValueError(f"El pontón con código naval '{codigo_naval}' ya existe.")
        except Exception as e:
            logging.error(f"Error al insertar pontón: {e}")
            self.connection.conn.rollback()
            raise e

    def consultar_centros(self):
        try:
            self.connection.cur.execute("""
                SELECT Nombre_Centro 
                FROM Ubicacion 
                WHERE Nombre_Centro NOT IN (SELECT Nombre_Centro FROM Ponton);
            """)
            centros = self.connection.cur.fetchall()
            return [centro[0] for centro in centros] if centros else []
        except Exception as e:
            logging.error(f"Error al consultar centros: {e}")
            return []
        
    def delete_ponton(self, codigo_naval):
        try:
            self.connection.cur.execute("DELETE FROM Ponton WHERE Codigo_Naval = %s;", (codigo_naval,))
            self.connection.conn.commit()
            logging.info(f"Pontón '{codigo_naval}' borrado correctamente")
        except psycopg2.errors.ForeignKeyViolation as e:
            logging.error(f"Error al borrar pontón: {e}")
            self.connection.conn.rollback()
            raise ValueError(f"No se puede borrar el pontón '{codigo_naval}' porque está referenciado en otra tabla.")
        except Exception as e:
            logging.error(f"Error al borrar pontón: {e}")
            self.connection.conn.rollback()
            raise e
    
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
            # Verificar si el centro nuevo ya está asociado a otro pontón
            self.connection.cur.execute("SELECT Codigo_Naval FROM Ponton WHERE Nombre_Centro = %s;", (id_centro_nuevo,))
            resultado = self.connection.cur.fetchone()
            if resultado and resultado[0] != codigo_naval:
                raise ValueError(f"El centro '{id_centro_nuevo}' ya está asociado al pontón '{resultado[0]}'")

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
            logging.info("Histórico de movimientos insertado y pontón actualizado correctamente")
        except ValueError as ve:
            logging.error(f"Error al insertar histórico de movimientos: {ve}")
            self.connection.conn.rollback()
            raise ve
        except Exception as e:
            logging.error(f"Error al insertar histórico de movimientos: {e}")
            self.connection.conn.rollback()
            raise e

    def insert_historico_dispositivos(self, serial, id_codigo_naval_anterior, id_codigo_naval_nuevo, fecha_instalacion_dispositivo, fecha_termino_dispositivo):
        try:
            # Verificar si el dispositivo ya está asociado a otro código naval
            self.connection.cur.execute("SELECT codigo_naval FROM Ponton_Dispositivos WHERE serial_dispositivo = %s;", (serial,))
            resultado = self.connection.cur.fetchone()
            if resultado and resultado[0] != id_codigo_naval_anterior:
                raise ValueError(f"El dispositivo '{serial}' ya está asociado al código naval '{resultado[0]}'")

            # Insertar en la tabla Historico_Dispositivos
            self.connection.cur.execute("""
                INSERT INTO Historico_Dispositivos (Serial, ID_Codigo_NavalAnterior, ID_Codigo_NavalNuevo, Fecha_Instalacion_Dispositivo, Fecha_Termino_Dispositivo)
                VALUES (%s, %s, %s, %s, %s);
            """, (serial, id_codigo_naval_anterior, id_codigo_naval_nuevo, fecha_instalacion_dispositivo, fecha_termino_dispositivo))
            
            # Actualizar la tabla Ponton_Dispositivos con la nueva ubicación
            self.connection.cur.execute("""
                UPDATE Ponton_Dispositivos
                SET codigo_naval = %s
                WHERE serial_dispositivo = %s;
            """, (id_codigo_naval_nuevo, serial))
            
            self.connection.conn.commit()
            logging.info("Histórico de dispositivos insertado y dispositivo actualizado correctamente")
        except ValueError as ve:
            logging.error(f"Error al insertar histórico de dispositivos: {ve}")
            self.connection.conn.rollback()
            raise ve
        except Exception as e:
            logging.error(f"Error al insertar histórico de dispositivos: {e}")
            self.connection.conn.rollback()
            raise e

    def consultar_empresas(self):
        try:
            self.connection.cur.execute("SELECT Nombre_Empresa FROM Empresa;")
            return self.connection.cur.fetchall()
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
                SELECT d.Serial, pd.codigo_naval, d.Direccionamiento_IP, d.Firmware_Version, pd.tipo_dispositivo, d.ID_Credenciales
                FROM Dispositivos d
                JOIN Credenciales c ON d.ID_Credenciales = c.ID_Credenciales
                LEFT JOIN Ponton_Dispositivos pd ON d.Serial = pd.serial_dispositivo;
            """)
            dispositivos = self.connection.cur.fetchall()
            return dispositivos if dispositivos else []
        except Exception as e:
            logging.error(f"Error al consultar dispositivos: {e}")
            return []
        
    def consultar_historico_movimientos(self):
        try:
            self.connection.cur.execute("""
                SELECT Codigo_Naval, ID_CentroAnterior, ID_CentroNuevo, Fecha_Instalacion_Centro, Fecha_Termino_Centro 
                FROM Historico_Movimientos;
            """)
            resultados = self.connection.cur.fetchall()
            return resultados if resultados else []
        except Exception as e:
            logging.error(f"Error al consultar histórico de movimientos: {e}")
            return []

    def consultar_historico_dispositivos(self):
        try:
            self.connection.cur.execute("""
                SELECT Serial, ID_Codigo_NavalAnterior, ID_Codigo_NavalNuevo, Fecha_Instalacion_Dispositivo, Fecha_Termino_Dispositivo 
                FROM Historico_Dispositivos;
            """)
            resultados = self.connection.cur.fetchall()
            return resultados if resultados else []
        except Exception as e:
            print(f"Error al consultar histórico de dispositivos: {e}")
            return []

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

    def consultar_codigos_navales(self):
        try:
            self.connection.cur.execute("SELECT Codigo_Naval FROM Ponton;")
            codigos_navales = self.connection.cur.fetchall()
            return [codigo[0] for codigo in codigos_navales] if codigos_navales else []
        except Exception as e:
            logging.error(f"Error al consultar códigos navales: {e}")
            return []   
    
    def consultar_codigo_naval_por_serial(self, serial):
        try:
            self.connection.cur.execute("""
                SELECT codigo_naval 
                FROM Ponton_Dispositivos 
                WHERE serial_dispositivo = %s;
            """, (serial,))
            resultado = self.connection.cur.fetchone()
            return resultado[0] if resultado else None
        except Exception as e:
            logging.error(f"Error al consultar código naval por serial: {e}")
            return None
        
    def consultar_codigo_naval_anterior(self, serial):
        try:
            self.connection.cur.execute("""
                SELECT codigo_naval 
                FROM Ponton_Dispositivos 
                WHERE serial_dispositivo = %s;
            """, (serial,))
            resultado = self.connection.cur.fetchone()
            return resultado[0] if resultado else None
        except Exception as e:
            logging.error(f"Error al consultar código naval anterior por serial: {e}")
            return None
            
    def consultar_codigos_navales_disponibles(self):
        try:
            self.connection.cur.execute("""
                SELECT codigo_naval
                FROM Ponton;
            """)
            return [row[0] for row in self.connection.cur.fetchall()]
        except Exception as e:
            logging.error(f"Error al consultar códigos navales disponibles: {e}")
            return []
        
    def consultar_centro_por_codigo_naval(self, codigo_naval):
        try:
            self.connection.cur.execute("""
                SELECT Nombre_Centro 
                FROM Ponton 
                WHERE Codigo_Naval = %s;
            """, (codigo_naval,))
            resultado = self.connection.cur.fetchone()
            return resultado[0] if resultado else None
        except Exception as e:
            logging.error(f"Error al consultar centro por código naval: {e}")
            return None

