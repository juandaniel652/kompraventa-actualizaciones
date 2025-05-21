import sqlite3 as sql

class datos_guardados : 

    def __init__(self, producto, precio, cantidad, fecha, total, mes, anio):
        self.producto = producto
        self.precio = precio
        self.cantidad = cantidad
        self.fecha = fecha
        self.total = total
        self.mes = mes
        self.anio = anio

    def guardar_en_base_datos(self):
        # Conectar a la base de datos
        conexion = sql.connect("ventas.db")
        cursor = conexion.cursor()

        # Crear la tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto TEXT,
                precio REAL,
                cantidad INTEGER,
                fecha TEXT,
                total REAL,
                mes TEXT,
                anio INTEGER
            )
        ''')

        # Insertar los datos en la tabla
        cursor.execute('''
            INSERT INTO ventas (producto, precio, cantidad, fecha, total, mes, anio)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.producto, self.precio, self.cantidad, self.fecha, self.total, self.mes, self.anio))

        # Guardar los cambios y cerrar la conexión
        conexion.commit()
        conexion.close()


    def seleccionar_meses_y_anio (self, mes, anio): 

        conexion = sql.connect("ventas.db")
        cursor = conexion.cursor()

        cursor.execute(f"SELECT mes, anio , MAX(cantidad) FROM ventas WHERE mes = '{mes}' AND anio = {anio};")
        datos = cursor.fetchall()

        conexion.close()

        return datos
    
    
    def seleccionar_fecha_y_su_total(self, mes):

        conexion = sql.connect("ventas.db")
        cursor = conexion.cursor()

        cursor.execute(f"SELECT fecha, SUM(precio * cantidad) AS total_ventas FROM ventas WHERE mes = '{mes}' GROUP BY fecha ORDER BY id ASC;")
        datos = cursor.fetchall()

        conexion.close()

        return datos
    
    
    def abrir_detalles_de_la_fecha(self, fecha):

        conexion = sql.connect("ventas.db")
        cursor = conexion.cursor()

        cursor.execute(f"SELECT producto, cantidad, precio, total FROM ventas WHERE fecha = '{fecha}';")
        datos = cursor.fetchall()

        conexion.close()

        return datos

    
    def abrir_total_precio_de_fecha (self, fecha) : 

        conexion = sql.connect("ventas.db")
        cursor = conexion.cursor()

        cursor.execute(f"SELECT SUM(precio * cantidad) AS total_ventas FROM ventas WHERE fecha  = '{fecha}' GROUP BY fecha ORDER BY id ASC;")
        datos = cursor.fetchall()

        conexion.close()

        return datos

    def abrir_total_cantidad_de_fecha (self, fecha) : 

        conexion = sql.connect("ventas.db")
        cursor = conexion.cursor()

        cursor.execute(f"SELECT SUM(cantidad) AS total_ventas FROM ventas WHERE fecha  = '{fecha}' GROUP BY fecha ORDER BY id ASC;")
        datos = cursor.fetchall()

        conexion.close()

        return datos