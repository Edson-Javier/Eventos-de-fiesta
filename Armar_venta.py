import tkinter as tk
from tkinter import END, messagebox, ttk    
import sqlite3
import Main as ini
import interfaz as intfz
import Login as lg 

global_paquetes = None

def iniciar_Armar_venta():
	Armar_venta = tk.Tk()
	Armar_venta.geometry(f"{Armar_venta.winfo_screenwidth()}x{Armar_venta.winfo_screenheight()}")  # Ajusta al tamaño de la pantalla
	Armar_venta.title("Gestión de Venta")

	def Autorizacion(Estado):
		if Estado == 'Confirmado':
			btn_Nuevo.config(state = 'disabled')
			txNombreUsuario.config(state = 'readonly')
			txAbonado.config(state = 'readonly')
			txEstado.config(state = 'readonly') 

	def deshabilitar_componentes():
		txBuscarId.delete(0, tk.END)
		txID.delete(0,tk.END)
		txNombreUsuario.delete(0, tk.END)
		txNombreCliente.delete(0, tk.END)
		txTotal.delete(0, tk.END)
		txAbonado.delete(0, tk.END)
		txFecha_pedido.delete(0, tk.END)
		txFecha_entrega.delete(0, tk.END)
		txEstado.delete(0, tk.END)

	def Nuevo():
		txNombreUsuario.delete(0,tk.END)
		txNombreUsuario.insert(0, lg.global_logeado.getNombre())
		txNombreUsuario.config(state= 'readonly')

	def Desbloqueo():
		txID.config(state = 'normal')
		txNombreUsuario.config(state= 'normal')
		txNombreCliente.config(state= 'normal') 
		txFecha_pedido.config(state = 'normal')
		txFecha_entrega.config(state = 'normal')  
		txTotal.config(state = 'normal')
		txAbonado.config(state = 'normal')
		txEstado.config(state = 'normal')
		deshabilitar_componentes()


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

	def Salvar():
		try:
			Id_venta = txID.get()
			id_usuario = lg.global_logeado.getId()
			nombre_usuario=txNombreUsuario.get()
			nombre_cliente=txNombreCliente.get()
			total = txTotal.get()
			abonado = txAbonado.get()
			fecha_inicial = txFecha_pedido.get()
			fecha_final = txFecha_entrega.get()
			estado = txEstado.get()

			if  not nombre_usuario or not nombre_cliente or not total or not abonado or not fecha_inicial or not fecha_final:
				messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
				return

			if not estado or estado != 'Confirmado':
				messagebox.showwarning("Advertencia", "Debes de confirmar la venta.")
				return


			conn, cursor = ini.obtener_conexion()

			try:
				# Realizar el UPDATE en la base de datos usando el ID como referencia
				cursor.execute("""
					UPDATE Armar_venta
					SET ID_usuario = ?, Estado = ?, Abonado = ?
					WHERE ID = ?
				""", (id_usuario, estado, abonado, Id_venta))

				# Guardar los cambios
				conn.commit()

				if cursor.rowcount > 0:  # Si se actualizó algún registro
					Cancelar()
					cargar_datos(tree)
					messagebox.showinfo("Exito", "La tabla venta ha sido actualizada correctamente.")

			except sqlite3.IntegrityError:
				messagebox.showwarning("Advertencia", "Error de integridad. No hubo cambios en la tabla venta del cliente.")

		except Exception as e:
			messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
		finally:
			conn.close()

	def Bloquear_buscar():
		txBuscarId.delete(0, tk.END) 
		txID.config(state = 'readonly')
		txNombreCliente.config(state = 'readonly')
		txTotal.config(state = 'readonly')
		txFecha_pedido.config(state = 'readonly')
		txFecha_entrega.config(state = 'readonly')  

	def Desbloquear_buscar():
		txID.config(state = 'normal')
		txNombreCliente.config(state = 'normal')
		txTotal.config(state = 'normal')
		txFecha_pedido.config(state = 'normal')
		txFecha_entrega.config(state = 'normal')  
		deshabilitar_componentes()

	def Buscar():
		try:
			venta = txBuscarId.get()
			
			if not venta:
				messagebox.showwarning("Advertencia", "Debe ingresar un numero de ID de numero de venta para buscar.")
				Desbloquear_buscar()
				return

			conn, cursor = ini.obtener_conexion()

			cursor.execute("SELECT ID, ID_usuario, ID_cliente, Fecha_pedido, Fecha_entrega, Paquetes, Total, Abonado, Estado FROM Armar_venta WHERE ID = ?", (venta,))
			resultado = cursor.fetchone()

			if resultado:
				Desbloquear_buscar()
				txID.insert(0,resultado[0])
				Nombre_usuario = buscar_dato("usuarios", "ID", resultado[1], "Nombre")
				txNombreUsuario.insert(0, Nombre_usuario)
				Nombre_cliente = buscar_dato("clientes", "ID", resultado[2], "Nombre")
				txNombreCliente.insert(0, Nombre_cliente)
				txFecha_pedido.insert(0, resultado[3])  
				txFecha_entrega.insert(0, resultado[4])
				global_paquetes = resultado[5]
				txTotal.insert(0,resultado[6])
				txAbonado.insert(0, resultado[7])
				txEstado.insert(0, resultado[8])
				Autorizacion(resultado[8])
				cargar_datos_paquetes(tree_derecha,global_paquetes)
				Bloquear_buscar()
				messagebox.showinfo("Éxito", "Venta encontrada.")
			else:
				Desbloquear_buscar()
				messagebox.showwarning("Advertencia", f"No se encontró la venta del cliente con ID :'{venta}'.")

		except Exception as e:
			Desbloquear_buscar()
			messagebox.showerror("Error", f"Ha ocurrido un error al buscar la venta: {str(e)}")
		finally:
			conn.close()
	
	def Eliminar():
		try:
			
			Venta = txID.get()
			Cliente = txNombreCliente.get()

			if not Venta or not Cliente:
				messagebox.showwarning("Advertencia", "Selecciona una venta primero.")
				return

			conn, cursor = ini.obtener_conexion()

			try:
				# Confirmar la eliminación del usuario
				respuesta = messagebox.askyesno("Confirmación", f"¿Estás seguro de que deseas eliminar la venta del cliente : {Cliente}?\nSi tiene un equipo armado tambien lo eliminara.")

				if respuesta:  # Si el usuario confirma
					cursor.execute("DELETE FROM Armar_venta WHERE ID = ?", (Venta,))
					cursor.execute("DELETE FROM Equipos WHERE ID_venta = ?", (Venta,))
					conn.commit()

					if cursor.rowcount > 0:  # Si se eliminó algún registro
						messagebox.showinfo("Exito", "La venta y el equipo se elimninaron correctamente.")
						cargar_datos(tree)
						Cancelar()  # Limpiar las cajas de texto o reiniciar el formulario

			except Exception as e:
				Cancelar()
				messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
		finally:
			conn.close()
		
	def Cancelar():
		Desbloqueo()
		for item in tree_derecha.get_children():
			tree_derecha.delete(item)

	def Salir():
		Armar_venta.destroy()
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

	# Función para cargar los datos en el Treeview
	def cargar_datos(tree):
		# Obtener la conexión y el cursor
		global global_paquetes
		conn, cursor = ini.obtener_conexion()
		try:
			# Limpiar el árbol antes de cargar los nuevos datos
			for item in tree.get_children():
				tree.delete(item)
			
			# Ejecutar la consulta para obtener los datos
			cursor.execute("SELECT * FROM Armar_venta")
			
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
				tree.insert("", "end", values=valores)
		except Exception as e:
			print(f"Error al cargar datos: {e}")
		finally:
			# Cerrar el cursor y la conexión
			cursor.close()
			conn.close()



	# Función para insertar datos en los cuadros de entrada
	def insertar_datos_a_entradas(event):
		seleccionado = tree.selection()
		if seleccionado:
			item = tree.item(seleccionado)
			valores = item['values']
			Desbloquear_buscar()
			txID.insert(0, valores[0])
			txNombreUsuario.insert(0, valores[1])
			txNombreCliente.insert(0, valores[2])
			txFecha_pedido.insert(0, valores[3])
			txFecha_entrega.insert(0, valores[4])
			txTotal.insert(0, valores[6])
			txAbonado.insert(0, valores[7])
			txEstado.set(valores[8])
			cargar_datos_paquetes(tree_derecha,global_paquetes)
			messagebox.showinfo("Éxito", "Usuario seleccionado.\nPuede editar o eliminar el cliente.")
			Autorizacion(valores[8])
			Bloquear_buscar()



	# Panel de búsqueda de usuario
	frame_buscar = tk.Frame(Armar_venta)
	frame_buscar.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

	# Panel de información del usuario
	frame_info = tk.Frame(Armar_venta)
	frame_info.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

	# Nuevo Frame para la tabla en el lado superior derecho
	frame_tabla_derecha = tk.Frame(Armar_venta)
	frame_tabla_derecha.grid(row=1, column=2, pady=10, padx=10, sticky="nsew")

	# Panel de botones de acción
	frame_botones = tk.Frame(Armar_venta)
	frame_botones.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

	# Tabla en el lado superior derecho
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

	# Frame para la tabla principal
	frame_tabla = tk.Frame(Armar_venta)
	frame_tabla.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

	# Configura el frame_tabla para expandirse
	frame_tabla.rowconfigure(0, weight=1)
	frame_tabla.columnconfigure(0, weight=1)

	# Tabla principal
	tree = ttk.Treeview(
		frame_tabla,
		columns=("ID", "Usuario", "Cliente", "Fecha_pedido", "Fecha_entrega", "Paquetes", "Total", "Abonado", "Estado"),
		show="headings"
	)
	tree.grid(row=0, column=0, sticky="nsew")

	# Encabezados de la tabla principal
	tree.heading("ID", text="ID")
	tree.heading("Usuario", text="Usuario")
	tree.heading("Cliente", text="Cliente")
	tree.heading("Fecha_pedido", text="Registro")
	tree.heading("Fecha_entrega", text="Entrega")
	tree.heading("Paquetes", text="Paquetes")
	tree.heading("Total", text="Total")
	tree.heading("Abonado", text="Abonado")
	tree.heading("Estado", text="Estado")

	# Configurar el tamaño de las columnas
	tree.column("ID", width=50)
	tree.column("Usuario", width=100)
	tree.column("Cliente", width=100)
	tree.column("Fecha_pedido", width=100)
	tree.column("Fecha_entrega", width=100)
	tree.column("Paquetes", width=70)
	tree.column("Total", width=70)
	tree.column("Abonado", width=70)
	tree.column("Estado", width=100)

	# Scrollbar para el Treeview principal
	scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
	tree.configure(yscroll=scrollbar.set)
	scrollbar.grid(row=0, column=1, sticky="ns")

	# Configura la ventana principal para que todo se distribuya correctamente
	Armar_venta.columnconfigure(0, weight=2)  # Columna de los frames de entrada
	Armar_venta.columnconfigure(1, weight=1)  # Espacio entre entrada y tabla derecha
	Armar_venta.columnconfigure(2, weight=2)  # Columna de la tabla derecha
	Armar_venta.rowconfigure(1, weight=1)     # Fila que contiene frame_info y tabla derecha
	Armar_venta.rowconfigure(3, weight=2)     # Fila de la tabla principal

	# Widgets del frame_buscar
	tk.Label(frame_buscar, text="Buscar ID:").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
	txBuscarId = tk.Entry(frame_buscar, width=30)
	txBuscarId.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

	btn_Buscar = tk.Button(frame_buscar, text="Buscar", command = Buscar)
	btn_Buscar.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

	# Widgets del frame_info
	tk.Label(frame_info, text="ID:").grid(row=1, column=0, padx=5, pady=5, sticky="ew")
	txID = tk.Entry(frame_info, width=30)
	txID.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

	tk.Label(frame_info, text="Usuario:").grid(row=2, column=0, padx=5, pady=5, sticky="ew")
	txNombreUsuario = tk.Entry(frame_info, width=30)
	txNombreUsuario.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

	tk.Label(frame_info, text="Cliente:").grid(row=3, column=0, padx=5, pady=5, sticky="ew")
	txNombreCliente = tk.Entry(frame_info, width=30)
	txNombreCliente.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

	tk.Label(frame_info, text="Registro:").grid(row=4, column=0, padx=5, pady=5, sticky="ew")
	txFecha_pedido = tk.Entry(frame_info, width=30)
	txFecha_pedido.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

	tk.Label(frame_info, text="Entrega:").grid(row=5, column=0, padx=5, pady=5, sticky="ew")
	txFecha_entrega = tk.Entry(frame_info, width=30)
	txFecha_entrega.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

	tk.Label(frame_info, text="Total:").grid(row=6, column=0, padx=5, pady=5, sticky="ew")
	txTotal = tk.Entry(frame_info, width=30)
	txTotal.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

	tk.Label(frame_info, text="Abonado:").grid(row=7, column=0, padx=5, pady=5, sticky="ew")
	txAbonado = tk.Entry(frame_info, width=30)
	txAbonado.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

	tk.Label(frame_info, text="Estado:").grid(row=8, column=0, padx=5, pady=5, sticky="ew")
	txEstado = ttk.Combobox(frame_info, values=["Confirmado"], width=30)
	txEstado.grid(row=8, column=1, padx=5, pady=5, sticky="ew")

	# Botones del frame_botones
	btn_Nuevo = tk.Button(frame_botones, text="Autorizar", command = Nuevo)
	btn_Nuevo.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

	btn_Salvar = tk.Button(frame_botones, text="Salvar", command = Salvar)
	btn_Salvar.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

	btn_Eliminar = tk.Button(frame_botones, text="Eliminar", command = Eliminar)
	btn_Eliminar.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

	btn_Cancelar = tk.Button(frame_botones, text="Cancelar", command = Cancelar)
	btn_Cancelar.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
	
	btn_Salir = tk.Button(frame_botones, text="Salir", command = Salir)
	btn_Salir.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

	# Vincular evento de selección del Treeview a la función
	tree.bind("<<TreeviewSelect>>", insertar_datos_a_entradas)

	# Cargar datos al iniciar
	cargar_datos(tree)