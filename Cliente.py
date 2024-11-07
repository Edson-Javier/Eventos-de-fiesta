import tkinter as tk
from tkinter import END, messagebox, ttk    
import sqlite3
import Main as ini
import interfaz as intfz
import Login as lg 

def iniciar_Clientes():
	Clientes = tk.Tk()
	Clientes.geometry("800x600")
	Clientes.title("Clientes")



	def deshabilitar_componentes():
		txBuscarId.delete(0, tk.END)
		txIdCliente.delete(0, tk.END)
		txNombreCliente.delete(0, tk.END)
		txEdad.delete(0, tk.END)
		txEmail.delete(0, tk.END)
		txContraseña.delete(0, tk.END)
		txTelefono.delete(0, tk.END)

	def Nuevo():
		deshabilitar_componentes()
		txIdCliente.config(state = 'disabled')
		btn_Buscar.config(state='disabled')
		btn_Nuevo.config(state='disabled')
		btn_Salvar.config(state='normal')

	def Desbloqueo_Nuevo():
		txIdCliente.config(state = 'normal')
		deshabilitar_componentes()
		btn_Buscar.config(state='normal')
		btn_Nuevo.config(state='normal')
		btn_Salvar.config(state = 'disabled')

	def Salvar():
		try:
			nombre_cliente=txNombreCliente.get()
			edad = txEdad.get()
			email = txEmail.get()
			contraseña = txContraseña.get()
			Telefono=txTelefono.get()
			

			if not nombre_cliente or not edad or not email or not contraseña :
				messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
				return
			
			if not Telefono.isdigit() or len(Telefono) != 10:
				messagebox.showerror("Error de entrada", "Ingrese un número de teléfono de 10 dígitos.")
				return
			
			conn, cursor = ini.obtener_conexion()
			
			try:
				cursor.execute("INSERT INTO clientes (Nombre, Edad, Telefono, EMail, Password) VALUES (?, ?, ?, ?, ?)", (nombre_cliente, edad,Telefono, email, contraseña))
				conn.commit()

				nuevo_id = cursor.lastrowid
				messagebox.showinfo("Exito", f"Cliente Registrado.\n El ID del usuario es {nuevo_id} ")
				Desbloqueo_Nuevo()
			except sqlite3.IntegrityError:	
				messagebox.showwarning("Advertencia", "Puede que algun campo de entre nombre a contraseña ya exista en la base de datos.\n Verifique su informacion.")

		except Exception as e:
			messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
		finally:
			conn.close()

	def Bloquear_buscar():
		txIdCliente.config(state = 'readonly')
		btn_Nuevo.config(state= 'disabled')
		btn_Editar.config(state= 'normal')
		btn_Eliminar.config(state= 'normal')

	def Desbloquear_buscar():
		txIdCliente.config(state = 'normal')
		deshabilitar_componentes()
		btn_Nuevo.config(state= 'normal')
		btn_Editar.config(state= 'disabled')
		btn_Eliminar.config(state= 'disabled')

	def Buscar():
		try:
			cliente = txBuscarId.get()
			
			if not cliente:
				messagebox.showwarning("Advertencia", "Debe ingresar un numero de ID de usuario para buscar.")
				Desbloquear_buscar()
				return

			conn, cursor = ini.obtener_conexion()

			cursor.execute("SELECT ID, Nombre, Edad, Telefono, EMail, Password FROM clientes WHERE ID = ?", (cliente,))
			resultado = cursor.fetchone()

			if resultado:
				txIdCliente.config(state = 'normal')
				deshabilitar_componentes()
				
				txIdCliente.insert(0, resultado[0])  
				txNombreCliente.insert(0, resultado[1]) 
				txEdad.insert(0, resultado[2])  
				txTelefono.insert(0, resultado[3])
				txEmail.insert(0, resultado[4])
				txContraseña.insert(0, resultado[5]) 
				Bloquear_buscar()
				messagebox.showinfo("Éxito", "Cliente encontrado.")
			else:
				Desbloquear_buscar()
				messagebox.showwarning("Advertencia", f"No se encontró el Cliente con ID :'{cliente}'.")

		except Exception as e:
			Desbloquear_buscar()
			messagebox.showerror("Error", f"Ha ocurrido un error al buscar el cliente: {str(e)}")
		finally:
			conn.close()

	
	def Editar():

		try:
			id_cliente = txIdCliente.get()
			nombre_cliente = txNombreCliente.get()
			edad = txEdad.get()
			email = txEmail.get()
			contraseña = txContraseña.get()
			Telefono=txTelefono.get()

			if not id_cliente or not nombre_cliente or not edad or not email or not contraseña:
				messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
				return

			if not Telefono.isdigit() or len(Telefono) != 10:
				messagebox.showerror("Error de entrada", "Ingrese un número de teléfono de 10 dígitos.")
				return

			conn, cursor = ini.obtener_conexion()

			try:
				cursor.execute("""
					UPDATE clientes
					SET Nombre = ?, Edad = ?, Telefono = ?, EMail = ?, Password = ?
					WHERE ID = ?
				""", (nombre_cliente, edad, Telefono, email, contraseña, id_cliente))

				conn.commit()

				if cursor.rowcount > 0:  
					Desbloquear_buscar()
					messagebox.showinfo("Exito", f"Cliente con ID: {id_cliente} ha sido actualizado correctamente.")

			except sqlite3.IntegrityError:
				Desbloquear_buscar()
				messagebox.showwarning("Advertencia", "Error de integridad. Verifique los datos.")
			
		except Exception as e:
			Desbloquear_buscar()
			messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
		
		finally:
			conn.close()
			

	def Eliminar():
		try:
			Id = txIdCliente.get()

			conn, cursor = ini.obtener_conexion()

			try:
				respuesta = messagebox.askyesno("Confirmación", f"¿Estás seguro de que deseas eliminar al cliente con ID : {Id}?")

				if respuesta: 
					cursor.execute("DELETE FROM clientes WHERE ID = ?", (Id,))
					conn.commit()

					if cursor.rowcount > 0:
						messagebox.showinfo("Exito", f"Cliente con ID {Id} ha sido eliminado correctamente.")
						Desbloquear_buscar() 

			except Exception as e:
				Desbloquear_buscar()
				messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
		finally:
			conn.close()

	def Cancelar():
		Clientes.destroy()
		intfz.iniciar_interfaz()

	def cargar_datos(tree):
		# Obtener conexión a la base de datos
		conn, cursor = ini.obtener_conexion()
		try:
			for item in tree.get_children():
				tree.delete(item)
			# Consulta para obtener todos los paquetes
			cursor.execute("SELECT * FROM clientes")

			# Recorrer los resultados de la consulta y añadirlos al Treeview
			for row in cursor.fetchall():
				tree.insert("", tk.END, values=row)

		except Exception as e:
			print(f"Error al cargar datos: {e}")

		finally:
			# Cerrar la conexión
			cursor.close()
			conn.close()

	frame_tabla_clientes = tk.Frame(Clientes)
	frame_tabla_clientes.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

	# Treeview para mostrar los Clientes
	tree = ttk.Treeview(frame_tabla_clientes, columns=("ID", "Nombre", "Edad", "Telefono", "Email", "Contraseña"), show="headings")
	tree.grid(row=0, column=0, sticky="nsew")

	# Definir encabezados de las columnas
	tree.heading("ID", text="ID")
	tree.heading("Nombre", text="Nombre")
	tree.heading("Edad", text="Edad")
	tree.heading("Telefono", text="Telefono")
	tree.heading("Email", text="Email")
	tree.heading("Contraseña", text="Contraseña")

	# Configurar el tamaño de las columnas (opcional)
	tree.column("ID", width=60)
	tree.column("Nombre", width=200)
	tree.column("Edad", width=60)
	tree.column("Telefono",width = 100)
	tree.column("Email", width = 200)
	tree.column("Contraseña", width=150)

	# Scrollbar para el Treeview
	scrollbar_Clientes = ttk.Scrollbar(frame_tabla_clientes, orient="vertical", command=tree.yview)
	tree.configure(yscroll=scrollbar_Clientes.set)
	scrollbar_Clientes.grid(row=0, column=1, sticky="ns")

	# Configurar expansión del Treeview
	frame_tabla_clientes.rowconfigure(0, weight=1)
	frame_tabla_clientes.columnconfigure(0, weight=1)

	# Panel principal
	Clientes.columnconfigure(0, weight=1)
	Clientes.columnconfigure(1, weight=1)
	Clientes.columnconfigure(2, weight=1)
	Clientes.rowconfigure(7, weight=1)

	# Panel de búsqueda de usuario
	frame_buscar_cliente = tk.Frame(Clientes)
	frame_buscar_cliente.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

	# Panel de información del usuario
	frame_info_cliente = tk.Frame(Clientes)
	frame_info_cliente.grid(row=1, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

	# Panel de botones de acción
	frame_botones_cliente = tk.Frame(Clientes)
	frame_botones_cliente.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

	# Panel de búsqueda de usuario
	tk.Label(frame_buscar_cliente, text="Buscar ID:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
	txBuscarId = tk.Entry(frame_buscar_cliente, width=10)
	txBuscarId.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

	btn_Buscar = tk.Button(frame_buscar_cliente, text="Buscar", command=Buscar)
	btn_Buscar.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
	btn_Buscar.config(state='normal')

	# Panel de información del cliente
	tk.Label(frame_info_cliente, text="ID:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
	txIdCliente = tk.Entry(frame_info_cliente, width=10)
	txIdCliente.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

	tk.Label(frame_info_cliente, text="Nombre:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
	txNombreCliente = tk.Entry(frame_info_cliente, width=30)
	txNombreCliente.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

	tk.Label(frame_info_cliente, text="Edad:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
	txEdad = tk.Entry(frame_info_cliente, width=10)
	txEdad.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

	tk.Label(frame_info_cliente, text="Telefono:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
	txTelefono = tk.Entry(frame_info_cliente, width=30)
	txTelefono.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
	
	tk.Label(frame_info_cliente, text="Email:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
	txEmail = tk.Entry(frame_info_cliente, width=30)
	txEmail.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

	tk.Label(frame_info_cliente, text="Contraseña:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
	txContraseña = tk.Entry(frame_info_cliente, width=30, show="*")
	txContraseña.grid(row=5, column=1, padx=10, pady=5, sticky="ew")


	# Panel de botones de acción
	btn_Nuevo = tk.Button(frame_botones_cliente, text="Nuevo", command=Nuevo)
	btn_Nuevo.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
	btn_Nuevo.config(state='normal')

	btn_Salvar = tk.Button(frame_botones_cliente, text="Salvar", command=Salvar)
	btn_Salvar.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
	btn_Salvar.config(state='disabled')

	btn_Editar = tk.Button(frame_botones_cliente, text="Editar", command=Editar)
	btn_Editar.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
	btn_Editar.config(state='disabled')

	btn_Eliminar = tk.Button(frame_botones_cliente, text="Eliminar", command=Eliminar)
	btn_Eliminar.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
	btn_Eliminar.config(state='disabled')

	btn_Cancelar = tk.Button(frame_botones_cliente, text="Cancelar", command=Cancelar)
	btn_Cancelar.grid(row=0, column=4, padx=10, pady=5, sticky="ew")

	cargar_datos(tree)