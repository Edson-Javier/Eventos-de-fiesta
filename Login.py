import tkinter as tk
from tkinter import END, messagebox, ttk
import Main as ini    
import interfaz as intfz

global_logeado = None  # Inicialmente está vacía


class sesion_guardada:
    """docstring for sesion_guardada"""
    def __init__(self, Id, Nombre, User_name, Password, Perfil):
        self.Id = Id
        self.Nombre = Nombre
        self.User_name = User_name
        self.Password = Password
        self.Perfil = Perfil
    
    def getId(self):
        return self.Id

    def getNombre(self):
        return self.Nombre

    def getUser_name(self):
        return self.User_name

    def getPassword(self):
        return self.Password 

    def getPerfil(self):
        return self.Perfil

        

def iniciar_login():
    Login = tk.Tk()
    Login.config(width=300, height=200)
    Login.title("Login")

    def deshabilitar_componentes():
        txUsuario.delete(0, tk.END)
        txContraseña.delete(0, tk.END)


    def obtener_datos_usuario(user_name):
        try:

            # Conexión a la base de datos
            conn, cursor = ini.obtener_conexion()
            
            # Consulta a la base de datos
            cursor.execute("SELECT ID, Nombre, User_name, Password, Perfil FROM usuarios WHERE User_name = ?", (user_name,))
            resultado = cursor.fetchone()
            
            return resultado  # Devuelve el resultado de la consulta

        except Exception as e:
            raise Exception(f"Error al obtener datos del usuario: {str(e)}")

        finally:
            conn.close()  # Asegura que se cierra la conexión


    def Logear():

        global global_logeado  # Para modificar la variable global

        try:
            user_name=txUsuario.get()
            contraseña=txContraseña.get()

            if not user_name or not contraseña:
                messagebox.showwarning('Campos incompletos', 'Llene todos los campos para ingresar.')
                deshabilitar_componentes()
                return

            resultado = obtener_datos_usuario(user_name)

            # Verificar si el usuario fue encontrado y la contraseña es correcta
            if resultado and resultado[2] == user_name and resultado[3] == contraseña:
                messagebox.showinfo('Ingreso correcto', 'Acceso concedido.')
                global_logeado = sesion_guardada(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4])
                Login.destroy()  # Cierra la ventana de Login
                intfz.iniciar_interfaz()  # Inicia la interfaz
            else:
                deshabilitar_componentes()
                messagebox.showwarning("Error", "Usuario o contraseña incorrectos.")

        except Exception as e:
            deshabilitar_componentes()
            messagebox.showwarning("Advertencia", f"Error durante el proceso de login: {str(e)}.")


    tk.Label(Login, text="Usuario:").place(x=10, y = 50)
    txUsuario = tk.Entry(Login, width=20)
    txUsuario.place(x=90, y=50)

    tk.Label(Login, text="Contraseña:").place(x=10, y = 100)
    txContraseña = tk.Entry(Login, width=20, show = "*")
    txContraseña.place(x=90, y=100)

    btn_Logear = tk.Button(Login, text = "Logear", command = Logear)
    btn_Logear.place(x=140,y=150)

    Login.mainloop()
