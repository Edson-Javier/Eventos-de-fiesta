import tkinter as tk
from tkinter import END, messagebox, ttk    
import sqlite3
import Main as ini
import interfaz as intfz

def iniciar_Paquetes():
	Paquetes = tk.Tk()
	Paquetes.geometry("800x600")
	Paquetes.title("Paquetes")

	def deshabilitar_componentes():
		txBuscarID.delete(0, tk.END)
		txID.delete(0, tk.END)
		txTipo.delete(0, tk.END)
		txDescripcion.delete(0, tk.END)
		txPrecio.delete(0, tk.END)

	def Nuevo():
		deshabilitar_componentes()
		txID.config(state='disabled')
		btn_Buscar.config(state='disabled')
		btn_Nuevo.config(state='disabled')
		btn_Salvar.config(state='normal')

	def Desbloqueo_Nuevo():
		txID.config(state='normal')
		deshabilitar_componentes()
		btn_Buscar.config(state='normal')
		btn_Nuevo.config(state='normal')
		btn_Salvar.config(state = 'disabled')

	def Salvar():
		try:
			Tipo = txTipo.get()
			Descripcion = txDescripcion.get()
			Precio = txPrecio.get()

			if  not Tipo or not Descripcion or not Precio:
				messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
				return
			
			conn, cursor = ini.obtener_conexion()
			
			try:
				cursor.execute("INSERT INTO Paquetes (Tipo, Descripcion, Precio) VALUES ( ?, ?, ?)", (Tipo, Descripcion, Precio))
				conn.commit()

				nuevo_id = cursor.lastrowid
				actualizar_combobox_tipos()
				messagebox.showinfo("Exito", f"Paquete Registrado.\n El ID del usuario es {nuevo_id} ")
				cargar_datos(tree)
				Desbloqueo_Nuevo()
			except sqlite3.IntegrityError:	
				messagebox.showwarning("Advertencia", "Puede que la informacion ya exista en la base de datos.\nVerifique su informacion.")

		except Exception as e:
			messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
		finally:
			conn.close()

	def Bloquear_buscar():
		btn_Nuevo.config(state= 'disabled')
		btn_Editar.config(state= 'normal')
		btn_Eliminar.config(state= 'normal')
		txID.config(state='readonly')

	def Desbloquear_buscar():
		txID.config(state='normal')
		deshabilitar_componentes()
		btn_Nuevo.config(state= 'normal')
		btn_Editar.config(state= 'disabled')
		btn_Eliminar.config(state= 'disabled')

	def Buscar():
		try:
			# Obtener el Tipo de usuario desde el campo de entrada
			ID = txBuscarID.get()
			# Validar que el campo no esté vacío
			
			if not ID:
				messagebox.showwarning("Advertencia", "Debe ingresar un ID del producto ya registrado.")
				Desbloquear_buscar()
				return

			# Conexión a la base de datos
			conn, cursor = ini.obtener_conexion()

			# Buscar el usuario en la base de datos
			cursor.execute("SELECT ID, Tipo, Descripcion, Precio FROM Paquetes WHERE ID = ?", (ID,))
			resultado = cursor.fetchone()

			if resultado:
				txID.config(state='normal')
				deshabilitar_componentes()
				txID.insert(0, resultado[0])  
				txTipo.insert(0, resultado[1])  
				txDescripcion.insert(0, resultado[2])
				txPrecio.insert(0, resultado[3])
				Bloquear_buscar()

				messagebox.showinfo("Éxito", "Producto encontrado.")
			else:
				# Si no se encuentra el usuario, mostrar un mensaje de error
				Desbloquear_buscar()
				messagebox.showwarning("Advertencia", f"No se encontró el Producto con ID :'{ID}'.")

		except Exception as e:
			# Manejo de errores generales
			Desbloquear_buscar()
			messagebox.showerror("Error", f"Ha ocurrido un error al buscar el ID: {str(e)}")
		finally:
			# Cerrar la conexión a la base de datos
			conn.close()

	
	def Editar():

		try:
			# Obtener los datos de las cajas de texto
			ID = txID.get()  # Se usa solo para identificar al usuario, no se modifica
			Tipo = txTipo.get()
			Descripcion = txDescripcion.get()
			Precio = txPrecio.get()

			if not ID or not Tipo or not Descripcion or not Precio:
				messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
				return

			conn, cursor = ini.obtener_conexion()

			try:
				# Realizar el UPDATE en la base de datos usando el ID como referencia
				cursor.execute("""
					UPDATE Paquetes
					SET Tipo = ?, Descripcion = ?, Precio = ?
					WHERE ID = ?
				""", (Tipo, Descripcion, Precio, ID))

				# Guardar los cambios
				conn.commit()

				if cursor.rowcount > 0:  # Si se actualizó algún registro
					Desbloquear_buscar()
					actualizar_combobox_tipos()
					cargar_datos(tree)
					messagebox.showinfo("Exito", f"Paquete con ID : {ID}, ha sido actualizado correctamente.")

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
			
			# Obtener el ID del usuario a eliminar
			ID = txID.get()  # Solo se utiliza para identificar al usuario

			conn, cursor = ini.obtener_conexion()

			try:
				# Confirmar la eliminación del usuario
				respuesta = messagebox.askyesno("Confirmación", f"¿Estás seguro de que deseas eliminar el paquete con el ID : {ID}?")

				if respuesta:  # Si el usuario confirma
					cursor.execute("DELETE FROM Paquetes WHERE ID = ?", (ID,))
					conn.commit()

					if cursor.rowcount > 0:  # Si se eliminó algún registro
						actualizar_combobox_tipos()
						messagebox.showinfo("Exito", f"Paquete con ID : {ID}, ha sido eliminado correctamente.")
						Desbloquear_buscar()  # Limpiar las cajas de texto o reiniciar el formulario
						cargar_datos(tree)

			except Exception as e:
				Desbloquear_buscar()
				messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
		finally:
			conn.close()


	# Función para cancelar
	def Cancelar():
		Paquetes.destroy()
		intfz.iniciar_interfaz()

	def obtener_tipos_unicos():
		conn, cursor = ini.obtener_conexion()
		tipos_unicos = set()
		if cursor:
			try:
				cursor.execute("SELECT Tipo FROM Paquetes")
				for row in cursor.fetchall():
					tipos_unicos.add(row[0])
			finally:
				conn.close()
		return list(tipos_unicos)

	def actualizar_combobox_tipos():
		Tipos_unicos = obtener_tipos_unicos()
		txTipo['values'] = Tipos_unicos


	def cargar_datos(tree):
		# Obtener conexión a la base de datos
		conn, cursor = ini.obtener_conexion()
		try:
			for item in tree.get_children():
				tree.delete(item)
			# Consulta para obtener todos los paquetes
			cursor.execute("SELECT * FROM Paquetes")

			# Recorrer los resultados de la consulta y añadirlos al Treeview
			for row in cursor.fetchall():
				tree.insert("", tk.END, values=row)

		except Exception as e:
			print(f"Error al cargar datos: {e}")

		finally:
			# Cerrar la conexión
			cursor.close()
			conn.close()



	# Configurar el grid principal de la ventana
	Paquetes.columnconfigure(0, weight=1)
	Paquetes.columnconfigure(1, weight=1)
	Paquetes.columnconfigure(2, weight=1)
	Paquetes.rowconfigure(3, weight=1)

	# Panel de búsqueda de paquete
	frame_buscar = tk.Frame(Paquetes)
	frame_buscar.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

	# Panel de información de paquete
	frame_info = tk.Frame(Paquetes)
	frame_info.grid(row=1, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

	# Panel de botones de acción
	frame_botones = tk.Frame(Paquetes)
	frame_botones.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

	# Treeview para mostrar los paquetes
	frame_treeview = tk.Frame(Paquetes)
	frame_treeview.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

	# Panel de búsqueda de paquete
	tk.Label(frame_buscar, text="Buscar ID:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
	txBuscarID = tk.Entry(frame_buscar, width=10)
	txBuscarID.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

	btn_Buscar = tk.Button(frame_buscar, text="Buscar", command= Buscar)
	btn_Buscar.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
	btn_Buscar.config(state='normal')

	# Panel de información de paquete
	tk.Label(frame_info, text="ID:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
	txID = tk.Entry(frame_info, width=10)
	txID.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

	tk.Label(frame_info, text="Tipo:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
	txTipo = ttk.Combobox(frame_info, state="normal", values=[])
	txTipo.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

	tk.Label(frame_info, text="Descripción:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
	txDescripcion = tk.Entry(frame_info, width=30)
	txDescripcion.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

	tk.Label(frame_info, text="Precio:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
	txPrecio = tk.Entry(frame_info, width=10)
	txPrecio.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

	# Panel de botones de acción
	btn_Nuevo = tk.Button(frame_botones, text="Nuevo", command= Nuevo)
	btn_Nuevo.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
	btn_Nuevo.config(state='normal')

	btn_Salvar = tk.Button(frame_botones, text="Salvar", command= Salvar)
	btn_Salvar.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
	btn_Salvar.config(state='disabled')

	btn_Editar = tk.Button(frame_botones, text="Editar", command= Editar)
	btn_Editar.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
	btn_Editar.config(state='disabled')

	btn_Eliminar = tk.Button(frame_botones, text="Eliminar", command= Eliminar)
	btn_Eliminar.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
	btn_Eliminar.config(state='disabled')

	btn_Cancelar = tk.Button(frame_botones, text="Cancelar", command= Cancelar)
	btn_Cancelar.grid(row=0, column=4, padx=10, pady=5, sticky="ew")

	# Panel del Treeview para mostrar los paquetes
	tree = ttk.Treeview(frame_treeview, columns=("ID", "Tipo", "Descripcion", "Precio"), show="headings")
	tree.grid(row=0, column=0, columnspan=3, sticky="nsew")

	# Definir encabezados de las columnas
	tree.heading("ID", text="ID")
	tree.heading("Tipo", text="Tipo")
	tree.heading("Descripcion", text="Descripción")
	tree.heading("Precio", text="Precio")

	# Configurar el tamaño de las columnas (opcional)
	tree.column("ID", width=50)
	tree.column("Tipo", width=150)
	tree.column("Descripcion", width=250)
	tree.column("Precio", width=80)

	# Configurar el Scrollbar para el Treeview
	scrollbar_paquetes = ttk.Scrollbar(frame_treeview, orient="vertical", command=tree.yview)
	tree.configure(yscroll=scrollbar_paquetes.set)
	scrollbar_paquetes.grid(row=0, column=3, sticky="ns")

	# Configurar la expansión del Treeview
	frame_treeview.rowconfigure(0, weight=1)
	frame_treeview.columnconfigure(0, weight=1)

	# Cargar los datos en el Treeview
	actualizar_combobox_tipos()
	cargar_datos(tree)


