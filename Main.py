import interfaz
import sqlite3
import Login as log

def obtener_conexion():
    conn = sqlite3.connect('Base_de_datos.db')  # Cambia por tu base de datos
    cursor = conn.cursor()
    return conn, cursor


def main():
    log.iniciar_login()

if __name__ == "__main__":
    main()