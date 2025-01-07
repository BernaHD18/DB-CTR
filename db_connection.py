import psycopg2

class DatabaseConnection:
    def __init__(self, dbname, user, password, host="localhost", port="5432"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cur = self.conn.cursor()
            print("Conexión exitosa a la base de datos")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            exit()

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("Conexión cerrada")
