import tkinter as tk
from tkinter import END, messagebox, ttk    
import sqlite3
import Main as ini
import interfaz as intfz
import Login as lg 

global_paquetes = None
global_venta = None
global_equipo = None


def iniciar_equipos():

	Equipos = tk.Tk()
	Equipos.geometry(f"{Equipos.winfo_screenwidth()}x{Equipos.winfo_screenheight()}")  # Ajusta al tamaño de la pantalla
	Equipos.title("Gestión de equipos")




	def buscar_dato(tabla, campo_busqueda, valor_busqueda, campo_resultado):
		try:
			conn, cursor = ini.obtener_conexion()
			query = f"SELECT {campo_resultado} FROM {tabla} WHERE {campo_busqueda} = ?"
			cursor.execute(query, (valor_busqueda,))
			resultado = cursor.fetchone()
			cursor.close()

			if resultado:
				return resultado[0]  # Retorna solo el valor del campo solicitado
			else:
				return f"{campo_resultado} no encontrado"
		except sqlite3.Error as e:
			print(f"Error al buscar en la base de datos: {e}")
			return None

	def obtener_ids_de_treeview(tree):
		items = tree.get_children()
		# Extraer el ID (primer valor) de cada fila en el Treeview
		ids = [tree.item(item, "values")[0] for item in items]
		# Unir los IDs en un string separados por espacios
		ids_string = " ".join(ids)
		return ids_string

	def Guardar():
		try:
			ids = obtener_ids_de_treeview(tree_equipo)
			conn, cursor = ini.obtener_conexion()
			try:

				cursor.execute("INSERT INTO Equipos (ID_venta,  Equipo) VALUES (?, ?)", (global_venta, ids))
				conn.commit()

				Cancelar()
				messagebox.showinfo("Exito", f"Equipo Registrado.\n El Equipo se guardo correctamente ")


			except sqlite3.IntegrityError:	
				messagebox.showwarning("Advertencia", "Puede que algun ya exista la informacion en la base de datos.\n Verifique su informacion.")

		except Exception as e:
			messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
		finally:
			conn.close()

	def Editar():
		try:
			ids = obtener_ids_de_treeview(tree_equipo)
			conn, cursor = ini.obtener_conexion()

			try:
				cursor.execute("""
					UPDATE Equipos
					SET Equipo = ?
					WHERE ID_venta = ?
				""", (ids, global_venta))

				conn.commit()

				if cursor.rowcount > 0:  
					Cancelar()
					messagebox.showinfo("Exito", "Equipo actualizado correctamente.")

			except sqlite3.IntegrityError:
				Cancelar()
				messagebox.showwarning("Advertencia", "Error de integridad. Verifique los datos.")
			
		except Exception as e:
			Cancelar()
			messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
		
		finally:
			conn.close()


	def Eliminar():
		try:
			
			Venta = global_venta

			if not Venta :
				messagebox.showwarning("Advertencia", "Selecciona una venta primero.")
				return

			conn, cursor = ini.obtener_conexion()

			try:
				# Confirmar la eliminación del usuario
				respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar el equipo del cliente ?\nSe eliminara tambien la venta.")

				if respuesta:  # Si el usuario confirma
					cursor.execute("DELETE FROM Armar_venta WHERE ID = ?", (Venta,))
					cursor.execute("DELETE FROM Equipos WHERE ID_venta = ?", (Venta,))
					conn.commit()

					if cursor.rowcount > 0:  # Si se eliminó algún registro
						cargar_datos(tree_izquierda)
						messagebox.showinfo("Exito", "La venta y el equipo se elimninaron correctamente.")
						Cancelar()  # Limpiar las cajas de texto o reiniciar el formulario

			except Exception as e:
				Cancelar()
				messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
		finally:
			conn.close()


	def Cancelar():
		for item in tree_derecha.get_children():
			tree_derecha.delete(item)
		for item in tree_equipo.get_children():
			tree_equipo.delete(item)		
		for item in tree.get_children():
			tree.delete(item)
		btn_guardar.config(state = 'disabled')
		btn_Editar.config(state = 'disabled')
		btn_Eliminar.config(state = 'disabled')

	def Salir():
		Equipos.destroy()
		intfz.iniciar_interfaz()


	def cargar_datos_paquetes(tree_derecha, paquetes_ids_str):
			# Obtener la conexión y el cursor
			conn, cursor = ini.obtener_conexion()
			try:
				# Limpiar el árbol antes de cargar los nuevos datos
				for item in tree_derecha.get_children():
					tree_derecha.delete(item)

				# Convertir el string de IDs a una lista
				paquetes_ids = paquetes_ids_str.split()  # Divide por espacios, genera una lista de strings
				paquetes_ids = [int(id_) for id_ in paquetes_ids]  # Convertir a enteros

				# Crear la consulta dinámica para múltiples IDs
				placeholders = ",".join("?" for _ in paquetes_ids)  # Crear un "?, ?, ?" dinámico
				query = f"SELECT ID, Tipo, Descripcion, Precio FROM Paquetes WHERE ID IN ({placeholders})"

				# Ejecutar la consulta con la lista de IDs
				cursor.execute(query, paquetes_ids)
				resultados = cursor.fetchall()

				# Insertar los resultados en el Treeview
				for fila in resultados:
					tree_derecha.insert("", "end", values=fila)
			except Exception as e:
				print(f"Error al cargar datos: {e}")
			finally:
				# Cerrar el cursor y la conexión
				cursor.close()
				conn.close()


	def cargar_datos_equipo(tree, paquetes_ids_str):
		# Obtener la conexión y el cursor
		conn, cursor = ini.obtener_conexion()
		try:
			# Limpiar el árbol antes de cargar los nuevos datos
			for item in tree.get_children():
				tree.delete(item)

			# Convertir el string de IDs a una lista
			paquetes_ids = paquetes_ids_str.split()  # Divide por espacios, genera una lista de strings
			paquetes_ids = [int(id_) for id_ in paquetes_ids]  # Convertir a enteros

			# Crear la consulta dinámica para múltiples IDs
			placeholders = ",".join("?" for _ in paquetes_ids)  # Crear un "?, ?, ?" dinámico
			query = f"SELECT ID, Nombre, Perfil FROM usuarios WHERE ID IN ({placeholders})"

			# Ejecutar la consulta con la lista de IDs
			cursor.execute(query, paquetes_ids)
			resultados = cursor.fetchall()

			# Insertar los resultados en el Treeview
			for fila in resultados:
				tree.insert("", "end", values=fila)
		except Exception as e:
			print(f"Error al cargar datos: {e}")
		finally:
			# Cerrar el cursor y la conexión
			cursor.close()
			conn.close()


	# Función para cargar los datos en el Treeview
	def cargar_datos(tree_izquierda):
		# Obtener la conexión y el cursor
		global global_paquetes
		conn, cursor = ini.obtener_conexion()
		try:
			# Limpiar el árbol antes de cargar los nuevos datos
			for item in tree_izquierda.get_children():
				tree_izquierda.delete(item)
			
			# Ejecutar la consulta para obtener los datos
			cursor.execute("SELECT * FROM Armar_venta WHERE Estado = 'Confirmado'")
			
			# Iterar sobre las filas devueltas por la consulta
			for row in cursor.fetchall():
				# Convertir la fila en una lista para poder modificarla
				valores = list(row)
				
				# Realizar las modificaciones específicas en los índices deseados
				if len(valores) > 1:  # Verificar que hay suficientes elementos
					valores[1] = buscar_dato("usuarios", "ID", valores[1], "Nombre")
				if len(valores) > 2:
					valores[2] = buscar_dato("clientes", "ID", valores[2], "Nombre")
				if len(valores) > 5: 
					global_paquetes = valores[5]
					valores[5] = len(valores[5].replace(" ", ""))
				# Insertar los datos en el árbol
				tree_izquierda.insert("", "end", values=valores)
		except Exception as e:
			print(f"Error al cargar datos: {e}")
		finally:
			# Cerrar el cursor y la conexión
			cursor.close()
			conn.close()


	def cargar_datos_usuarios(tree):
		# Obtener conexión a la base de datos
		conn, cursor = ini.obtener_conexion()
		try:
			for item in tree.get_children():
				tree.delete(item)
			# Consulta para obtener todos los paquetes
			cursor.execute("SELECT ID, Nombre, Perfil FROM usuarios")

			# Recorrer los resultados de la consulta y añadirlos al Treeview
			for row in cursor.fetchall():
				tree.insert("", tk.END, values=row)

		except Exception as e:
			print(f"Error al cargar datos: {e}")

		finally:
			# Cerrar la conexión
			cursor.close()
			conn.close()


	
	def verificar_equipo(id_venta):
		try:

			conn, cursor = ini.obtener_conexion()
			cursor.execute("SELECT Equipo FROM Equipos WHERE ID_venta = ?", (id_venta,))
			resultado = cursor.fetchone()
			
			# Verificar si el ID_venta existe
			if resultado:
				equipo = resultado[0]  # Obtener el valor del equipo
				messagebox.showinfo("Información", f"Puedes editar tu equipo: {equipo}")
				cargar_datos_equipo(tree_equipo, equipo)
				btn_Editar.config(state = 'normal')
				btn_Eliminar.config(state = 'normal')
			else:
				messagebox.showwarning("Información", "Crea un equipo para esta venta.")
				btn_guardar.config(state = 'normal')
		except Exception as e:
			print(f"Error al cargar datos: {e}")

		finally:
			# Cerrar la conexión
			cursor.close()
			conn.close()

	# Función para insertar datos en los cuadros de entrada
	def insertar_datos_a_entradas(event):
		global global_venta
		seleccionado = tree_izquierda.selection()
		if seleccionado:
			item = tree_izquierda.item(seleccionado)
			valores = item['values']
			messagebox.showinfo("Éxito", "Puedes verificar los paquetes del cliente para organizar tu equipo.")
			global_venta = valores[0]
			verificar_equipo(global_venta)
			cargar_datos_paquetes(tree_derecha,global_paquetes)
			cargar_datos_usuarios(tree)
			#Autorizacion(valores[8])
	
		
	# Frame contenedor para las tablas superiores
	frame_superior = tk.Frame(Equipos)
	frame_superior.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

	# Configura el frame_superior para expandirse
	frame_superior.columnconfigure(0, weight=1)  # Tabla izquierda
	frame_superior.columnconfigure(1, weight=0)  # Espacio entre tablas
	frame_superior.columnconfigure(2, weight=1)  # Tabla derecha

	# Frame para la tabla principal (lado izquierdo)
	frame_tabla_izquierda = tk.Frame(frame_superior)
	frame_tabla_izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 5))  # Espacio derecho

	# Frame para la tabla derecha (lado derecho)
	frame_tabla_derecha = tk.Frame(frame_superior)
	frame_tabla_derecha.grid(row=0, column=2, sticky="nsew", padx=(5, 0))  # Espacio izquierdo

	# Configuración de las tablas en sus respectivos frames
	# Tabla principal (lado izquierdo)
	tree_izquierda = ttk.Treeview(
		frame_tabla_izquierda,
		columns=("ID", "Usuario", "Cliente", "Fecha_pedido", "Fecha_entrega", "Paquetes", "Total", "Abonado", "Estado"),
		show="headings"
	)
	tree_izquierda.grid(row=0, column=0, sticky="nsew")

	# Encabezados de la tabla izquierda
	tree_izquierda.heading("ID", text="ID")
	tree_izquierda.heading("Usuario", text="Usuario")
	tree_izquierda.heading("Cliente", text="Cliente")
	tree_izquierda.heading("Fecha_pedido", text="Registro")
	tree_izquierda.heading("Fecha_entrega", text="Entrega")
	tree_izquierda.heading("Paquetes", text="Paquetes")
	tree_izquierda.heading("Total", text="Total")
	tree_izquierda.heading("Abonado", text="Abonado")
	tree_izquierda.heading("Estado", text="Estado")

	# Configurar el tamaño de las columnas de la tabla izquierda
	tree_izquierda.column("ID", width=50)
	tree_izquierda.column("Usuario", width=100)
	tree_izquierda.column("Cliente", width=100)
	tree_izquierda.column("Fecha_pedido", width=100)
	tree_izquierda.column("Fecha_entrega", width=100)
	tree_izquierda.column("Paquetes", width=70)
	tree_izquierda.column("Total", width=70)
	tree_izquierda.column("Abonado", width=70)
	tree_izquierda.column("Estado", width=100)

	# Scrollbar para el Treeview izquierdo
	scrollbar_izquierda = ttk.Scrollbar(frame_tabla_izquierda, orient="vertical", command=tree_izquierda.yview)
	tree_izquierda.configure(yscroll=scrollbar_izquierda.set)
	scrollbar_izquierda.grid(row=0, column=1, sticky="ns")

	# Tabla derecha
	tree_derecha = ttk.Treeview(
		frame_tabla_derecha,
		columns=("ID", "Tipo", "Descripcion", "Precio"),
		show="headings"
	)
	tree_derecha.grid(row=0, column=0, sticky="nsew")

	# Encabezados de la tabla derecha
	tree_derecha.heading("ID", text="ID")
	tree_derecha.heading("Tipo", text="Tipo")
	tree_derecha.heading("Descripcion", text="Descripción")
	tree_derecha.heading("Precio", text="Precio")

	# Configurar ancho de columnas
	tree_derecha.column("ID", width=150)
	tree_derecha.column("Tipo", width=150)
	tree_derecha.column("Descripcion", width=200)
	tree_derecha.column("Precio", width=150)

	# Scrollbar para la tabla derecha
	scrollbar_derecha = ttk.Scrollbar(frame_tabla_derecha, orient="vertical", command=tree_derecha.yview)
	tree_derecha.configure(yscroll=scrollbar_derecha.set)
	scrollbar_derecha.grid(row=0, column=1, sticky="ns")

	# Frame inferior
	frame_inferior = tk.Frame(Equipos)
	frame_inferior.grid(row=1, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

	# Configura el frame_inferior para expandirse
	frame_inferior.columnconfigure(0, weight=1)  # Elemento izquierdo
	frame_inferior.columnconfigure(1, weight=0)  # Espacio entre elementos (para scrollbars)
	frame_inferior.columnconfigure(2, weight=1)  # Elemento derecho
	frame_inferior.columnconfigure(3, weight=0)  # Espacio entre elementos (para scrollbars)

	# Treeview para mostrar usuarios (izquierda)
	tree = ttk.Treeview(frame_inferior, columns=("ID", "Nombre", "Perfil"), show="headings")
	tree.grid(row=0, column=0, sticky="nsew")

	# Definir encabezados de las columnas
	tree.heading("ID", text="ID")
	tree.heading("Nombre", text="Nombre")
	tree.heading("Perfil", text="Perfil")

	# Configurar el tamaño de las columnas (opcional)
	tree.column("ID", width=50)
	tree.column("Nombre", width=200)
	tree.column("Perfil", width=100)

	# Scrollbar para el Treeview de usuarios
	scrollbar_usuarios = ttk.Scrollbar(frame_inferior, orient="vertical", command=tree.yview)
	tree.configure(yscroll=scrollbar_usuarios.set)
	scrollbar_usuarios.grid(row=0, column=1, sticky="ns")

	# Treeview para mostrar equipos (derecha)
	tree_equipo = ttk.Treeview(frame_inferior, columns=("ID", "Nombre", "Perfil"), show="headings")
	tree_equipo.grid(row=0, column=2, sticky="nsew")

	# Definir encabezados de las columnas
	tree_equipo.heading("ID", text="ID")
	tree_equipo.heading("Nombre", text="Nombre")
	tree_equipo.heading("Perfil", text="Perfil")

	# Configurar el tamaño de las columnas (opcional)
	tree_equipo.column("ID", width=50)
	tree_equipo.column("Nombre", width=200)
	tree_equipo.column("Perfil", width=100)

	# Scrollbar para el Treeview de equipos
	scrollbar_equipo = ttk.Scrollbar(frame_inferior, orient="vertical", command=tree_equipo.yview)
	tree_equipo.configure(yscroll=scrollbar_equipo.set)
	scrollbar_equipo.grid(row=0, column=3, sticky="ns")


	def agregar_usuario_a_equipo():
		"""
		Mueve un usuario seleccionado de la tabla de usuarios a la tabla de equipos,
		verificando que no se repita en la tabla de equipos.
		"""
		# Obtener la selección en la tabla de usuarios
		selected_item = tree.selection()
		if not selected_item:
			messagebox.showwarning("Advertencia", "Primero selecciona una venta para poder armar tu equipo.")
			return  # No hay selección
		
		# Recuperar los valores del elemento seleccionado
		values = tree.item(selected_item, "values")
		
		# Verificar si el dato ya existe en la tabla de equipos
		for item in tree_equipo.get_children():
			equipo_values = tree_equipo.item(item, "values")
			if values == equipo_values:
				messagebox.showwarning("Advertencia", "Este usuario ya está en el equipo.")
				return  # Dato repetido, no agregar
		
		# Insertar los valores en la tabla de equipos si no hay repetición
		tree_equipo.insert("", "end", values=values)


	# Panel de botones de acción
	frame_botones = tk.Frame(Equipos)
	frame_botones.grid(row=2, column=1, columnspan=3, pady=10, padx=10, sticky="ew")

	# Botón para mover el dato
	boton_agregar = tk.Button(frame_botones, text="Agregar", command=agregar_usuario_a_equipo)
	boton_agregar.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
	
	# Botones del frame_botones
	btn_guardar = tk.Button(frame_botones, text="Guardar",command = Guardar )
	btn_guardar.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
	btn_guardar.config(state = 'disabled')

	# Botones del frame_botones
	btn_Editar = tk.Button(frame_botones, text="Editar", command = Editar )
	btn_Editar.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
	btn_Editar.config(state = 'disabled')	

	btn_Eliminar = tk.Button(frame_botones, text="Eliminar", command = Eliminar )
	btn_Eliminar.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
	btn_Eliminar.config(state = 'disabled')

	btn_Cancelar = tk.Button(frame_botones, text="Cancelar", command = Cancelar )
	btn_Cancelar.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

	btn_Salir = tk.Button(frame_botones, text="Salir", command = Salir )
	btn_Salir.grid(row=1, column=4, padx=5, pady=5, sticky="ew")

	tree_izquierda.bind("<<TreeviewSelect>>", insertar_datos_a_entradas)
	cargar_datos(tree_izquierda)
	