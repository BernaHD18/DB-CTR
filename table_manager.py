class TableManager:
    def __init__(self, connection):
        self.connection = connection

    def create_tables(self):
        commands = [
            # Eliminar tablas existentes para reiniciar desde cero
            "DROP TABLE IF EXISTS Historico_Dispositivos CASCADE;",
            "DROP TABLE IF EXISTS Historico_Movimientos CASCADE;",
            "DROP TABLE IF EXISTS Camara CASCADE;",
            "DROP TABLE IF EXISTS Asistente_Virtual CASCADE;",
            "DROP TABLE IF EXISTS Radar CASCADE;",
            "DROP TABLE IF EXISTS NIO CASCADE;",
            "DROP TABLE IF EXISTS Ponton_Dispositivos CASCADE;",
            "DROP TABLE IF EXISTS Ponton CASCADE;",
            "DROP TABLE IF EXISTS Dispositivos CASCADE;",
            "DROP TABLE IF EXISTS Credenciales CASCADE;",
            "DROP TABLE IF EXISTS Ubicacion CASCADE;",
            "DROP TABLE IF EXISTS Empresa CASCADE;",
            
            # Crear tablas
            """
            CREATE TABLE Empresa (
                Nombre_Empresa VARCHAR PRIMARY KEY
            );
            """,
            """
            CREATE TABLE Ubicacion (
                Nombre_Centro VARCHAR PRIMARY KEY,
                Grupo_Telegram VARCHAR,
                Nombre_Empresa VARCHAR NOT NULL,
                CONSTRAINT FK_Nombre_Empresa FOREIGN KEY (Nombre_Empresa)
                REFERENCES Empresa (Nombre_Empresa)
            );
            """,
            """
            CREATE TABLE Credenciales (
                ID_Credenciales SERIAL PRIMARY KEY,
                Usuario VARCHAR NOT NULL,
                Contraseña VARCHAR NOT NULL
            );
            """,
            """
            CREATE TABLE Dispositivos (
                Serial VARCHAR PRIMARY KEY,
                Direccionamiento_IP VARCHAR NOT NULL,
                Firmware_Version VARCHAR,
                ID_Credenciales INTEGER,
                CONSTRAINT FK_ID_Credenciales FOREIGN KEY (ID_Credenciales)
                REFERENCES Credenciales (ID_Credenciales)
            );
            """,
            """
            CREATE TABLE Ponton (
                Codigo_Naval VARCHAR PRIMARY KEY,
                Nombre_Centro VARCHAR,
                Estado BOOLEAN NOT NULL,
                IA VARCHAR,
                Observaciones TEXT,
                CONSTRAINT FK_Nombre_Centro FOREIGN KEY (Nombre_Centro)
                REFERENCES Ubicacion (Nombre_Centro)
            );
            """,
            """
            CREATE TABLE Ponton_Dispositivos (
                id SERIAL PRIMARY KEY,
                codigo_naval VARCHAR(50) NOT NULL,
                serial_dispositivo VARCHAR(50) NOT NULL,
                tipo_dispositivo VARCHAR(50) NOT NULL,
                FOREIGN KEY (codigo_naval) REFERENCES Ponton(Codigo_Naval),
                FOREIGN KEY (serial_dispositivo) REFERENCES Dispositivos(Serial)
            );
            """,
            """
            CREATE TABLE NIO (
                Serial VARCHAR PRIMARY KEY,
                Modelo VARCHAR
            );
            """,
            """
            CREATE TABLE Radar (
                Serial VARCHAR PRIMARY KEY,
                Canal_RF VARCHAR
            );
            """,
            """
            CREATE TABLE Asistente_Virtual (
                Serial VARCHAR PRIMARY KEY
            );
            """,
            """
            CREATE TABLE Camara (
                Serial VARCHAR PRIMARY KEY
            );
            """,
            """
            CREATE TABLE Historico_Movimientos (
                ID_Movimiento SERIAL PRIMARY KEY,
                Codigo_Naval VARCHAR,
                ID_CentroAnterior VARCHAR,
                ID_CentroNuevo VARCHAR,
                Fecha_Instalacion_Centro DATE,
                Fecha_Termino_Centro DATE,
                CONSTRAINT FK_Codigo_Naval FOREIGN KEY (Codigo_Naval)
                REFERENCES Ponton (Codigo_Naval),
                CONSTRAINT FK_ID_CentroAnterior FOREIGN KEY (ID_CentroAnterior)
                REFERENCES Ubicacion (Nombre_Centro),
                CONSTRAINT FK_ID_CentroNuevo FOREIGN KEY (ID_CentroNuevo)
                REFERENCES Ubicacion (Nombre_Centro)
            );
            """,
            """
            CREATE TABLE Historico_Dispositivos (
                ID_Movimiento_Dispositivo SERIAL PRIMARY KEY,
                Serial VARCHAR,
                ID_Codigo_NavalAnterior VARCHAR,
                ID_Codigo_NavalNuevo VARCHAR,
                Fecha_Instalacion_Dispositivo DATE,
                Fecha_Termino_Dispositivo DATE,
                CONSTRAINT FK_Serial FOREIGN KEY (Serial)
                REFERENCES Dispositivos (Serial) ON DELETE NO ACTION,
                CONSTRAINT FK_ID_Codigo_NavalAnterior FOREIGN KEY (ID_Codigo_NavalAnterior)
                REFERENCES Ponton (Codigo_Naval),
                CONSTRAINT FK_ID_Codigo_NavalNuevo FOREIGN KEY (ID_Codigo_NavalNuevo)
                REFERENCES Ponton (Codigo_Naval)
            );
            """
        ]

        try:
            for command in commands:
                self.connection.cur.execute(command)
                print("Tabla creada correctamente")
            self.connection.conn.commit()
        except Exception as e:
            print(f"Error al crear tablas: {e}")
            self.connection.conn.rollback()

    # ...existing code...


    def alter_tables(self):
        commands = [
            "INSERT INTO Empresa (Nombre_Empresa) VALUES ('Prueba');" # Insertar datos de prueba


        ]

        try:
            for command in commands:
                self.connection.cur.execute(command)
                print("Tabla alterada correctamente")
            self.connection.conn.commit()
        except Exception as e:
            print(f"Error al alterar tablas: {e}")

    def drop_tables(self):
        commands = [
            # Eliminar tablas existentes para reiniciar desde cero
            "DROP TABLE IF EXISTS Historico_Dispositivos CASCADE;",
            "DROP TABLE IF EXISTS Historico_Movimientos CASCADE;",
            "DROP TABLE IF EXISTS Camara CASCADE;",
            "DROP TABLE IF EXISTS Asistente_Virtual CASCADE;",
            "DROP TABLE IF EXISTS Radar CASCADE;",
            "DROP TABLE IF EXISTS NIO CASCADE;",
            "DROP TABLE IF EXISTS Ponton CASCADE;",
            "DROP TABLE IF EXISTS Dispositivos CASCADE;",
            "DROP TABLE IF EXISTS Credenciales CASCADE;",
            "DROP TABLE IF EXISTS Ubicacion CASCADE;",
            "DROP TABLE IF EXISTS Empresa CASCADE;",
        ]

        try:
            for command in commands:
                self.connection.cur.execute(command)
                print("Tabla eliminada correctamente")
            self.connection.conn.commit()
        except Exception as e:
            print(f"Error al eliminar tablas: {e}")
