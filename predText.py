import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
import csv

# Variables globales para bigramas y trigramas
bigramas = {}
trigramas = {}
tipo_ngrama = ""

# Función para cargar el archivo de bigramas o trigramas desde CSV
def cargar_archivo():
    global bigramas, trigramas, tipo_ngrama
    bigramas.clear()
    trigramas.clear()

    file_path = filedialog.askopenfilename(title="Seleccionar archivo CSV", filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Leer la primera línea como encabezado

        # Detectar si es un archivo de bigramas o trigramas
        if header[:3] == ["Term1", "Term2", "Term3"]:
            tipo_ngrama = "trigrama"
            for row in reader:
                term1, term2, term3, freq, context_freq, prob = row
                trigramas[(term1, term2, term3)] = float(prob)
        elif header[:2] == ["Term1", "Term2"]:
            tipo_ngrama = "bigrama"
            for row in reader:
                term1, term2, freq, context_freq, prob = row
                bigramas[(term1, term2)] = float(prob)
        else:
            messagebox.showerror("Error", "Formato de archivo no válido.")
            return

    messagebox.showinfo("Éxito", f"Archivo de {tipo_ngrama}s cargado correctamente.")

# Función para calcular las siguientes palabras probables
def calcular_siguientes_palabras():
    entrada = placeholder_entry.get().strip().split()
    if not entrada:
        messagebox.showwarning("Advertencia", "Escribe al menos una palabra para empezar.")
        return

    palabras_probables = []

    # Lógica para calcular las siguientes palabras probables según bigramas o trigramas
    if tipo_ngrama == "bigrama" and len(entrada) >= 1:
        ultima_palabra = entrada[-1]
        palabras_probables = [term2 for (term1, term2) in bigramas if term1 == ultima_palabra]

    elif tipo_ngrama == "trigrama" and len(entrada) >= 2:
        penultima_palabra, ultima_palabra = entrada[-2], entrada[-1]
        palabras_probables = [term3 for (term1, term2, term3) in trigramas if term1 == penultima_palabra and term2 == ultima_palabra]

    # Limpiar y mostrar las palabras probables en la lista de sugerencias
    lista_sugerencias.delete(0, tk.END)
    for palabra in palabras_probables[:5]:  # Mostrar solo las 5 más probables
        lista_sugerencias.insert(tk.END, palabra)

# Función para agregar una palabra seleccionada al texto generado
def agregar_palabra():
    seleccion = lista_sugerencias.curselection()
    if seleccion:
        palabra = lista_sugerencias.get(seleccion)
        texto_generado.insert(tk.END, palabra + " ")
        placeholder_entry.insert(tk.END, " " + palabra)
        calcular_siguientes_palabras()  # Calcular nuevas palabras tras agregar una

# Configuración de la interfaz
root = tk.Tk()
root.title("Generador de Texto")

# Botón para cargar archivo
btn_cargar_archivo = tk.Button(root, text="Cargar archivo CSV", command=cargar_archivo)
btn_cargar_archivo.grid(row=0, column=0, pady=5)

# Placeholder para escribir la palabra o palabras iniciales
placeholder_label = tk.Label(root, text="Palabras iniciales:")
placeholder_label.grid(row=1, column=0, sticky="e")
placeholder_entry = tk.Entry(root, width=30)
placeholder_entry.grid(row=1, column=1)

# Botón para calcular las palabras probables
btn_calcular = tk.Button(root, text="Calcular siguientes palabras", command=calcular_siguientes_palabras)
btn_calcular.grid(row=2, column=0, columnspan=2, pady=5)

# Lista de palabras sugeridas
lista_sugerencias = Listbox(root, width=30, height=5)
lista_sugerencias.grid(row=3, column=0, columnspan=2, pady=5)

# Botón para agregar palabra seleccionada
btn_agregar_palabra = tk.Button(root, text="Add word", command=agregar_palabra)
btn_agregar_palabra.grid(row=4, column=0, columnspan=2, pady=5)

# Texto generado
texto_generado = tk.Text(root, width=40, height=5)
texto_generado.grid(row=5, column=0, columnspan=2, pady=5)

root.mainloop()
