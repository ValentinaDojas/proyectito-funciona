import tkinter as tk
from tkinter import messagebox
from db import conectar

# -------------------
# FUNCIONES
# -------------------

def guardar():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    email = entry_email.get()
    try:
        conexion = conectar()
    except Exception as e:
        messagebox.showerror("Conexión", f"No se pudo conectar a la base de datos:\n{e}")
        return
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO personas (nombre, apellido, email) VALUES (%s, %s, %s)",
        (nombre, apellido, email)
    )
    conexion.commit()
    conexion.close()
    limpiar_campos()

def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_id_modificar.delete(0, tk.END)
    entry_id_eliminar.delete(0, tk.END)

def eliminar():
    id_eliminar = entry_id_eliminar.get()
    if id_eliminar == "":
        return
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM personas WHERE id=%s", (id_eliminar,))
    conexion.commit()
    conexion.close()
    entry_id_eliminar.delete(0, tk.END)

def modificar():
    id_modificar = entry_id_modificar.get()
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    email = entry_email.get()
    if id_modificar == "":
        return
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE personas SET nombre=%s, apellido=%s, email=%s WHERE id=%s",
        (nombre, apellido, email, id_modificar)
    )
    conexion.commit()
    conexion.close()
    limpiar_campos()

# -------------------
# INTERFAZ
# -------------------

ventana = tk.Tk()
ventana.title("ABM Personas")
ventana.geometry("300x400")  # opcional para tamaño de ventana

# ALTA
tk.Label(ventana, text="Nombre").pack(anchor="w", padx=10, pady=2)
entry_nombre = tk.Entry(ventana)
entry_nombre.pack(fill="x", padx=10)

tk.Label(ventana, text="Apellido").pack(anchor="w", padx=10, pady=2)
entry_apellido = tk.Entry(ventana)
entry_apellido.pack(fill="x", padx=10)

tk.Label(ventana, text="Email").pack(anchor="w", padx=10, pady=2)
entry_email = tk.Entry(ventana)
entry_email.pack(fill="x", padx=10)

tk.Button(ventana, text="Guardar", command=guardar).pack(fill="x", padx=10, pady=5)

# BAJA
tk.Label(ventana, text="ID para eliminar").pack(anchor="w", padx=10, pady=2)
entry_id_eliminar = tk.Entry(ventana)
entry_id_eliminar.pack(fill="x", padx=10)
tk.Button(ventana, text="Eliminar", command=eliminar).pack(fill="x", padx=10, pady=5)

# MODIFICACIÓN
tk.Label(ventana, text="ID para modificar").pack(anchor="w", padx=10, pady=2)
entry_id_modificar = tk.Entry(ventana)
entry_id_modificar.pack(fill="x", padx=10)
tk.Button(ventana, text="Modificar", command=modificar).pack(fill="x", padx=10, pady=5)

ventana.mainloop()