import tkinter as tk
from tkinter import END, messagebox, ttk    
import sqlite3
import Main as ini
import interfaz as intfz
import Login as lg 


Ancho = 800  # Puedes ajustar estos valores
Largo = 400

global_pruductos = None
Id_venta = None

def iniciar_Armar_venta():
	Armar_venta = tk.Tk()
	Armar_venta.config(width=Ancho, height=Largo)
	Armar_venta.title("Armar_venta")

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
		deshabilitar_componentes()  
		txNombreUsuario.insert(0, lg.global_logeado.getNombre())
		txNombreUsuario.config(state= 'readonly')
		btn_Nuevo.config(state='disabled')
		btn_Salvar.config(state='normal')

	def Desbloqueo():
		txID.config(state = 'normal')
		txNombreUsuario.config(state= 'normal')
		txNombreCliente.config(state= 'normal') 
		txFecha_pedido.config(state = 'normal')
		txFecha_entrega.config(state = 'normal')  
		txTotal.config(state = 'normal')
		txAbonado.config(state = 'normal')
		deshabilitar_componentes()
		btn_Nuevo.config(state='normal')
		btn_Salvar.config(state = 'disabled')


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
					Desbloqueo()
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
		txAbonado.config(state = 'readonly')
		txFecha_pedido.config(state = 'readonly')
		txFecha_entrega.config(state = 'readonly')  

	def Desbloquear_buscar():
		txID.config(state = 'normal')
		txNombreCliente.config(state = 'normal')
		txTotal.config(state = 'normal')
		txAbonado.config(state = 'normal')
		txFecha_pedido.config(state = 'normal')
		txFecha_entrega.config(state = 'normal')  
		deshabilitar_componentes()

	def Buscar():
		try:
			global global_pruductos
			global Id_venta
			venta = txBuscarId.get()
			
			if not venta:
				messagebox.showwarning("Advertencia", "Debe ingresar un numero de ID de numero de venta para buscar.")
				Desbloquear_buscar()
				return

			# Conexión a la base de datos
			conn, cursor = ini.obtener_conexion()

			# Buscar el usuario en la base de datos
			cursor.execute("SELECT ID, ID_cliente, Fecha_pedido, Fecha_entrega, Paquetes, Total, Estado FROM Armar_venta WHERE ID = ?", (venta,))
			resultado = cursor.fetchone()

			if resultado:
				Desbloquear_buscar()
				txID.insert(0,resultado[0])
				Nombre_cliente = buscar_dato("clientes", "ID", resultado[1], "Nombre")
				txNombreCliente.insert(0, Nombre_cliente)
				txFecha_pedido.insert(0, resultado[2])  
				txFecha_entrega.insert(0, resultado[3])
				global_pruductos = resultado[4]
				txTotal.insert(0,resultado[5])
				txAbonado.insert(0, 0.0)
				txEstado.insert(0, resultado[6])
				Bloquear_buscar()
				messagebox.showinfo("Éxito", "Venta encontrada.")
			else:
				# Si no se encuentra el usuario, mostrar un mensaje de error
				Desbloquear_buscar()
				messagebox.showwarning("Advertencia", f"No se encontró la venta del cliente con ID :'{venta}'.")

		except Exception as e:
			# Manejo de errores generales
			Desbloquear_buscar()
			messagebox.showerror("Error", f"Ha ocurrido un error al buscar el cliente: {str(e)}")
		finally:
			# Cerrar la conexión a la base de datos
			conn.close()
	"""
	def Eliminar():
		try:
			
			# Obtener el ID del usuario a eliminar
			Id = txIdCliente.get()  # Solo se utiliza para identificar al usuario

			conn, cursor = ini.obtener_conexion()

			try:
				# Confirmar la eliminación del usuario
				respuesta = messagebox.askyesno("Confirmación", f"¿Estás seguro de que deseas eliminar al cliente con ID : {Id}?")

				if respuesta:  # Si el usuario confirma
					cursor.execute("DELETE FROM Armar_venta WHERE ID_Cliente = ?", (Id,))
					conn.commit()

					if cursor.rowcount > 0:  # Si se eliminó algún registro
						messagebox.showinfo("Exito", f"Cliente con ID {Id} ha sido eliminado correctamente.")
						Desbloquear_buscar()  # Limpiar las cajas de texto o reiniciar el formulario

			except Exception as e:
				Desbloquear_buscar()
				messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
		finally:
			conn.close()
		"""
	def Cancelar():
		Armar_venta.destroy()
		intfz.iniciar_interfaz()


	tk.Label(Armar_venta, text="Buscar ID:").place(x=400, y=10)
	txBuscarId = tk.Entry(Armar_venta, width=10)
	txBuscarId.place(x=400, y=30)
	
	tk.Label(Armar_venta, text="ID:").place(x=10, y=10)
	txID = tk.Entry(Armar_venta, width=10)
	txID.place(x=10, y=30)
	
	tk.Label(Armar_venta, text="Nombre de usuario:").place(x=10, y=60)
	txNombreUsuario = tk.Entry(Armar_venta, width=30)
	txNombreUsuario.place(x=10, y=80)

	tk.Label(Armar_venta, text="Nombre de cliente:").place(x=10, y=110)
	txNombreCliente = tk.Entry(Armar_venta, width=30)
	txNombreCliente.place(x=10, y=130)

	
	tk.Label(Armar_venta, text="Total:").place(x=10, y=160)
	txTotal = tk.Entry(Armar_venta, width=10)
	txTotal.place(x=10, y=180)

	tk.Label(Armar_venta, text="Abonado:").place(x=170, y=160)
	txAbonado = tk.Entry(Armar_venta, width=10)
	txAbonado.place(x=170, y=180)

	tk.Label(Armar_venta, text="Fecha del registro:").place(x=10, y=210)
	txFecha_pedido= tk.Entry(Armar_venta, state= "normal", width=10)
	txFecha_pedido.place(x=10, y=230)
	
	tk.Label(Armar_venta, text="Fecha del evento:").place(x=170, y=210)
	txFecha_entrega = tk.Entry(Armar_venta, state= "normal", width=10)
	txFecha_entrega.place(x=170, y=230)

	tk.Label(Armar_venta, text="Estado:").place(x=10, y=260)
	txEstado = ttk.Combobox(Armar_venta, state= "normal", values=["Confirmado"])
	txEstado.place(x=10, y=280)


	# Botones de acción
	btn_Buscar = tk.Button(Armar_venta, text="Buscar", command= Buscar)
	btn_Buscar.place(x=500, y=30)
	btn_Buscar.config(state='normal')

	btn_Nuevo = tk.Button(Armar_venta, text="Nuevo", command= Nuevo)
	btn_Nuevo.place(x=10, y=310)
	btn_Nuevo.config(state='normal')

	btn_Salvar = tk.Button(Armar_venta, text="Salvar", command= Salvar)
	btn_Salvar.place(x=80, y=310)
	btn_Salvar.config(state='disabled')
	"""
	btn_Editar = tk.Button(Armar_venta, text="Editar", command= prueba)
	btn_Editar.place(x=240, y=280)
	btn_Editar.config(state='disabled')

	btn_Eliminar = tk.Button(Armar_venta, text="Eliminar", command= prueba)
	btn_Eliminar.place(x=310, y=280)
	btn_Eliminar.config(state='disabled')
	"""
	btn_Cancelar = tk.Button(Armar_venta, text="Cancelar", command=Cancelar)
	btn_Cancelar.place(x=150, y=310)
