import tkinter as tk
from tkinter import END, messagebox, ttk    
import Login as lg
import Usuarios as usrs
import Cliente as cliente
import Armar_venta as armar
import Paquetes as pack
import Equipos as team

def iniciar_interfaz():
	Menu = tk.Tk()
	Menu.geometry(f"{Menu.winfo_screenwidth()}x{Menu.winfo_screenheight()}")
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
	    
	def inicio_equipos():
		Menu.destroy()
		team.iniciar_equipos()
	"""
	def verificacion():
		resultado = lg.obtener_datos_usuario(user_name)
		perfil = resultado[4]
		if perfil != 'Gerente':
			btn_Usuarios.config(state= 'disabled')
	"""

	# Configurar el frame del menú
	Menu.columnconfigure(0, weight=1)  # Permitir expansión horizontal

	# Estilo de los botones
	button_font = ("Arial", 14, "bold")  # Fuente grande y negrita
	button_width = 15  # Ancho de los botones
	button_padding = {"padx": 20, "pady": 10}  # Espaciado alrededor de los botones

	# Botones del menú
	btn_Productos = tk.Button(Menu, text="Paquetes", command=inicio_paquetes, font=button_font, width=button_width)
	btn_Productos.grid(row=0, column=0, **button_padding, sticky="ew")

	btn_Usuarios = tk.Button(Menu, text="Usuarios", command=inicio_users, font=button_font, width=button_width)
	btn_Usuarios.grid(row=1, column=0, **button_padding, sticky="ew")

	btn_Clientes = tk.Button(Menu, text="Clientes", command=inicio_clientes, font=button_font, width=button_width)
	btn_Clientes.grid(row=2, column=0, **button_padding, sticky="ew")

	btn_Armar = tk.Button(Menu, text="Venta", command=inicio_armar, font=button_font, width=button_width)
	btn_Armar.grid(row=3, column=0, **button_padding, sticky="ew")

	btn_Equipos = tk.Button(Menu, text="Equipos", command=inicio_equipos, font=button_font, width=button_width)
	btn_Equipos.grid(row=4, column=0, **button_padding, sticky="ew")

	btn_Salir = tk.Button(Menu, text="Salir", command=fin_interfaz, font=button_font, width=button_width, fg="red")
	btn_Salir.grid(row=5, column=0, **button_padding, sticky="ew")