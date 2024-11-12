import tkinter as tk
from tkinter import END, messagebox, ttk    
import sqlite3
import Main as ini
import interfaz as intfz

def iniciar_usuarios():
	Usuarios = tk.Tk()
	Usuarios.geometry("800x600") 
	Usuarios.title("Usuarios")

	def deshabilitar_componentes_Usuario():
		txBuscarIdUsuario.delete(0, tk.END)
		txIdUsuario.delete(0, tk.END)
		txNombreUsuario.delete(0, tk.END)
		txUser_name.delete(0, tk.END)
		txContraseñaUsuario.delete(0, tk.END)
		txPerfilUsuario.delete(0, tk.END)

	def Nuevo_Usuario():
		deshabilitar_componentes_Usuario()
		btn_Buscar_Usuario.config(state='disabled')
		btn_Nuevo_Usuario.config(state='disabled')
		btn_Salvar_Usuario.config(state='normal')
		txIdUsuario.config(state='disabled')

	def Desbloqueo_Nuevo_Usuario():
		deshabilitar_componentes_Usuario()
		btn_Buscar_Usuario.config(state='normal')
		btn_Nuevo_Usuario.config(state='normal')
		btn_Salvar_Usuario.config(state = 'disabled')
		txIdUsuario.config(state='normal')

	def Salvar_Usuario():
		try:
			nombre=txNombreUsuario.get()
			usuario=txUser_name.get()
			contraseña=txContraseñaUsuario.get()
			perfil=txPerfilUsuario.get()

			if not nombre or not usuario or not contraseña or not perfil:
				messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
				return
			
			conn, cursor = ini.obtener_conexion()
			
			try:
				cursor.execute("INSERT INTO usuarios (Nombre, User_name, Password, Perfil) VALUES (?, ?, ?, ?)", (nombre, usuario, contraseña, perfil))
				conn.commit()

				nuevo_id = cursor.lastrowid
				messagebox.showinfo("Exito", f"Cliente Registrado.\n El ID del usuario es {nuevo_id} ")
				Desbloqueo_Nuevo_Usuario()
				cargar_datos(tree)
				actualizar_combobox_perfil()
			except sqlite3.IntegrityError:	
				messagebox.showwarning("Advertencia", "Puede que algun campo de entre nombre a contraseña ya exista en la base de datos.\n Verifique su informacion.")

		except Exception as e:
			messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
		finally:
			conn.close()

	def Bloquear_buscar():
		btn_Nuevo_Usuario.config(state= 'disabled')
		btn_Editar_Usuario.config(state= 'normal')
		btn_Eliminar_Usuario.config(state= 'normal')
		txIdUsuario.config(state='readonly')

	def Desbloquear_buscar():
		txIdUsuario.config(state='normal')
		deshabilitar_componentes_Usuario()
		btn_Nuevo_Usuario.config(state= 'normal')
		btn_Editar_Usuario.config(state= 'disabled')
		btn_Eliminar_Usuario.config(state= 'disabled')

	def Buscar_Usuario():
		try:
			# Obtener el nombre de usuario desde el campo de entrada
			usuario = txBuscarIdUsuario.get()
			# Validar que el campo no esté vacío
			
			if not usuario:
				messagebox.showwarning("Advertencia", "Debe ingresar un numero de ID de usuario para buscar.")
				Desbloquear_buscar()
				return

			# Conexión a la base de datos
			conn, cursor = ini.obtener_conexion()

			# Buscar el usuario en la base de datos
			cursor.execute("SELECT ID, Nombre, User_name, Password, Perfil FROM usuarios WHERE ID = ?", (usuario,))
			resultado = cursor.fetchone()

			if resultado:
				txIdUsuario.config(state='normal')
				deshabilitar_componentes_Usuario()
				# Si se encuentra el usuario, mostrar los datos en los campos correspondientes
				txIdUsuario.insert(0, resultado[0])  # Insertar el ID encontrado
				txNombreUsuario.insert(0, resultado[1])  # Insertar el Nombre encontrado
				txUser_name.insert(0, resultado[2])  # Insertar el User_name encontrado
				txContraseñaUsuario.insert(0, resultado[3])  # Insertar la Contraseña encontrada
				txPerfilUsuario.insert(0, resultado[4])  # Insertar el Perfil encontrado
				Bloquear_buscar()

				messagebox.showinfo("Éxito", "Usuario encontrado.")
			else:
				# Si no se encuentra el usuario, mostrar un mensaje de error
				Desbloquear_buscar()
				messagebox.showwarning("Advertencia", f"No se encontró el usuario con ID :'{usuario}'.")

		except Exception as e:
			# Manejo de errores generales
			Desbloquear_buscar()
			messagebox.showerror("Error", f"Ha ocurrido un error al buscar el usuario: {str(e)}")
		finally:
			# Cerrar la conexión a la base de datos
			conn.close()

	
	def Editar_Usuario():

		try:
			# Obtener los datos de las cajas de texto
			Id = txIdUsuario.get()  # Se usa solo para identificar al usuario, no se modifica
			nombre = txNombreUsuario.get()
			usuario = txUser_name.get()
			contraseña = txContraseñaUsuario.get()
			perfil = txPerfilUsuario.get()

			if not Id or not nombre or not usuario or not contraseña or not perfil:
				messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
				return

			conn, cursor = ini.obtener_conexion()

			try:
				# Realizar el UPDATE en la base de datos usando el ID como referencia
				cursor.execute("""
					UPDATE usuarios
					SET Nombre = ?, User_name = ?, Password = ?, Perfil = ?
					WHERE ID = ?
				""", (nombre, usuario, contraseña, perfil, Id))

				# Guardar los cambios
				conn.commit()

				if cursor.rowcount > 0:  # Si se actualizó algún registro
					Desbloquear_buscar()
					cargar_datos(tree)
					actualizar_combobox_perfil()
					messagebox.showinfo("Exito", f"Usuario con ID {Id} ha sido actualizado correctamente.")

			except sqlite3.IntegrityError:
				Desbloquear_buscar()
				messagebox.showwarning("Advertencia", "Error de integridad. Verifique los datos.")
			
		except Exception as e:
			Desbloquear_buscar()
			messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
		
		finally:
			conn.close()
			
	def Eliminar_Usuario():
		try:
			
			# Obtener el ID del usuario a eliminar
			Id = txIdUsuario.get()  # Solo se utiliza para identificar al usuario

			conn, cursor = ini.obtener_conexion()

			try:
				# Confirmar la eliminación del usuario
				respuesta = messagebox.askyesno("Confirmación", f"¿Estás seguro de que deseas eliminar al usuario con ID {Id}?")

				if respuesta:  # Si el usuario confirma
					cursor.execute("DELETE FROM usuarios WHERE ID = ?", (Id,))
					conn.commit()

					if cursor.rowcount > 0:  # Si se eliminó algún registro
						messagebox.showinfo("Exito", f"Usuario con ID {Id} ha sido eliminado correctamente.")
						Desbloquear_buscar()  # Limpiar las cajas de texto o reiniciar el formulario
						cargar_datos(tree)
						actualizar_combobox_perfil()

			except Exception as e:
				Desbloquear_buscar()
				messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
		finally:
			conn.close()


	# Función para cancelar
	def Cancelar():
		Usuarios.destroy()
		intfz.iniciar_interfaz()

	def cargar_datos(tree):
		# Obtener conexión a la base de datos
		conn, cursor = ini.obtener_conexion()
		try:
			for item in tree.get_children():
				tree.delete(item)
			# Consulta para obtener todos los paquetes
			cursor.execute("SELECT * FROM usuarios")

			# Recorrer los resultados de la consulta y añadirlos al Treeview
			for row in cursor.fetchall():
				tree.insert("", tk.END, values=row)

		except Exception as e:
			print(f"Error al cargar datos: {e}")

		finally:
			# Cerrar la conexión
			cursor.close()
			conn.close()

	def obtener_perfiles_unicos():
		conn, cursor = ini.obtener_conexion()
		perfiles_unicos = set()
		if cursor:
			try:
				cursor.execute("SELECT Perfil FROM usuarios")
				for row in cursor.fetchall():
					perfiles_unicos.add(row[0])
			finally:
				conn.close()
		return list(perfiles_unicos)

	def actualizar_combobox_perfil():
		perfiles_unicos = obtener_perfiles_unicos()
		txPerfilUsuario['values'] = perfiles_unicos

	frame_tabla_usuario = tk.Frame(Usuarios)
	frame_tabla_usuario.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

	# Treeview para mostrar los usuarios
	tree = ttk.Treeview(frame_tabla_usuario, columns=("ID", "Nombre", "Username", "Contraseña", "Perfil"), show="headings")
	tree.grid(row=0, column=0, sticky="nsew")

	# Definir encabezados de las columnas
	tree.heading("ID", text="ID")
	tree.heading("Nombre", text="Nombre")
	tree.heading("Username", text="Nombre de usuario")
	tree.heading("Contraseña", text="Contraseña")
	tree.heading("Perfil", text="Perfil")

	# Configurar el tamaño de las columnas (opcional)
	tree.column("ID", width=50)
	tree.column("Nombre", width=200)
	tree.column("Username", width=150)
	tree.column("Contraseña", width=150)
	tree.column("Perfil", width=100)

	# Scrollbar para el Treeview
	scrollbar_usuarios = ttk.Scrollbar(frame_tabla_usuario, orient="vertical", command=tree.yview)
	tree.configure(yscroll=scrollbar_usuarios.set)
	scrollbar_usuarios.grid(row=0, column=1, sticky="ns")

	# Configurar expansión del Treeview
	frame_tabla_usuario.rowconfigure(0, weight=1)
	frame_tabla_usuario.columnconfigure(0, weight=1)

	def insertar_datos_a_entradas(event):
		seleccionado = tree.selection()  # Obtener el elemento seleccionado
		if seleccionado:
			Desbloquear_buscar()
			item = tree.item(seleccionado)
			valores = item['values']
			# Insertar los datos en los cuadros de entrada
			
			txIdUsuario.insert(0, valores[0])
			txNombreUsuario.insert(0, valores[1])
			txUser_name.insert(0, valores[2])
			txContraseñaUsuario.insert(0, valores[3])
			txPerfilUsuario.insert(0, valores[4])
			Bloquear_buscar()
			messagebox.showinfo("Éxito", "Usuario seleccionado.\nPuede editar o eliminar el cliente.")
	# Vincular el evento de selección del Treeview a la función
	tree.bind("<<TreeviewSelect>>", insertar_datos_a_entradas)

	# Panel principal
	Usuarios.columnconfigure(0, weight=1)
	Usuarios.columnconfigure(1, weight=1)
	Usuarios.columnconfigure(2, weight=1)
	Usuarios.rowconfigure(3, weight=1)

	# Panel de búsqueda de usuario
	frame_buscar_usuario = tk.Frame(Usuarios)
	frame_buscar_usuario.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

	# Panel de información del usuario
	frame_info_usuario = tk.Frame(Usuarios)
	frame_info_usuario.grid(row=1, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

	# Panel de botones de acción
	frame_botones_usuario = tk.Frame(Usuarios)
	frame_botones_usuario.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

	# Panel de búsqueda de usuario
	tk.Label(frame_buscar_usuario, text="Buscar ID:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
	txBuscarIdUsuario = tk.Entry(frame_buscar_usuario, width=10)
	txBuscarIdUsuario.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

	btn_Buscar_Usuario = tk.Button(frame_buscar_usuario, text="Buscar", command=Buscar_Usuario)
	btn_Buscar_Usuario.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
	btn_Buscar_Usuario.config(state='normal')

	# Panel de información del usuario
	tk.Label(frame_info_usuario, text="ID:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
	txIdUsuario = tk.Entry(frame_info_usuario, width=10)
	txIdUsuario.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

	tk.Label(frame_info_usuario, text="Nombre:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
	txNombreUsuario = tk.Entry(frame_info_usuario, width=30)
	txNombreUsuario.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

	tk.Label(frame_info_usuario, text="Nombre de usuario:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
	txUser_name = tk.Entry(frame_info_usuario, width=30)
	txUser_name.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

	tk.Label(frame_info_usuario, text="Contraseña:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
	txContraseñaUsuario = tk.Entry(frame_info_usuario, width=30, show="*")
	txContraseñaUsuario.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

	tk.Label(frame_info_usuario, text="Perfil:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
	txPerfilUsuario = ttk.Combobox(frame_info_usuario, state="normal", values=[])
	txPerfilUsuario.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
	actualizar_combobox_perfil()

	# Panel de botones de acción
	btn_Nuevo_Usuario = tk.Button(frame_botones_usuario, text="Nuevo", command=Nuevo_Usuario)
	btn_Nuevo_Usuario.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
	btn_Nuevo_Usuario.config(state='normal')

	btn_Salvar_Usuario = tk.Button(frame_botones_usuario, text="Salvar", command=Salvar_Usuario)
	btn_Salvar_Usuario.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
	btn_Salvar_Usuario.config(state='disabled')

	btn_Editar_Usuario = tk.Button(frame_botones_usuario, text="Editar", command=Editar_Usuario)
	btn_Editar_Usuario.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
	btn_Editar_Usuario.config(state='disabled')

	btn_Eliminar_Usuario = tk.Button(frame_botones_usuario, text="Eliminar", command=Eliminar_Usuario)
	btn_Eliminar_Usuario.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
	btn_Eliminar_Usuario.config(state='disabled')

	btn_Cancelar = tk.Button(frame_botones_usuario, text="Cancelar", command=Cancelar)
	btn_Cancelar.grid(row=0, column=4, padx=10, pady=5, sticky="ew")

	cargar_datos(tree)
