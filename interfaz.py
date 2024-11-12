import tkinter as tk
from tkinter import END, messagebox, ttk    
import Login as lg
import Usuarios as usrs
import Cliente as cliente
import Armar_venta as armar
import Paquetes as pack

def iniciar_interfaz():
	Menu = tk.Tk()
	Menu.geometry("800x600")
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

	Menu.columnconfigure(0, weight=1)
	Menu.columnconfigure(1, weight=1)
	Menu.columnconfigure(2, weight=1)
	Menu.rowconfigure(10, weight=1)

	# Panel de búsqueda de usuario

	btn_Productos = tk.Button(Menu,text="Paquetes",command = inicio_paquetes)
	btn_Productos.grid(row=0, column=0, padx=5, pady=5, sticky="w")

	btn_Usuarios = tk.Button(Menu,text="Usuarios",command = inicio_users)
	btn_Usuarios.grid(row=1, column=0, padx=5, pady=5, sticky="w")

	btn_Clientes = tk.Button(Menu,text="Clientes",command = inicio_clientes)
	btn_Clientes.grid(row=3, column=0, padx=5, pady=5, sticky="w")

	btn_Armar = tk.Button(Menu,text="Venta",command = inicio_armar)
	btn_Armar.grid(row=4, column=0, padx=5, pady=5, sticky="w")


	btn_Salir = tk.Button(Menu, text = "Salir", command = fin_interfaz)
	btn_Salir.grid(row=6, column=0, padx=5, pady=5, sticky="w")
