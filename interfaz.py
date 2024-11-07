import tkinter as tk
from tkinter import END, messagebox, ttk    
import Login as lg
import Usuarios as usrs
import Cliente as cliente
import Armar_venta as armar
import Paquetes as pack

Ancho = 700  # Puedes ajustar estos valores
Largo = 500

def iniciar_interfaz():
	Menu = tk.Tk()
	Menu.config(width=Ancho, height=Largo)
	Menu.title("Menu")

	def fin_interfaz():
		Menu.destroy()
		lg.iniciar_login()


	def inicio_paquetes():
		Menu.destroy()
		pack.iniciar_Paquetes()


	def inicio_users():
	    Menu.destroy()
	    usrs.iniciar_usuarios()
	    
	def inicio_clientes():
	    Menu.destroy()
	    cliente.iniciar_Clientes()

	def inicio_armar():
		Menu.destroy()
		armar.iniciar_Armar_venta()
	    

	"""
	def verificacion():
		resultado = lg.obtener_datos_usuario(user_name)
		perfil = resultado[4]
		if perfil != 'Gerente':
			btn_Usuarios.config(state= 'disabled')
	"""

	btn_Productos = tk.Button(Menu,text="Paquetes",command = inicio_paquetes)
	btn_Productos.place(x=10,y=30)

	btn_Usuarios = tk.Button(Menu,text="Usuarios",command = inicio_users)
	btn_Usuarios.place(x=10,y=80)

	btn_Clientes = tk.Button(Menu,text="Clientes",command = inicio_clientes)
	btn_Clientes.place(x=10,y=130)

	btn_Armar = tk.Button(Menu,text="Armar\nventa",command = inicio_armar)
	btn_Armar.place(x=10,y=180)


	btn_Salir = tk.Button(Menu, text = "Salir", command = fin_interfaz)
	btn_Salir.place(x=10,y=280)
