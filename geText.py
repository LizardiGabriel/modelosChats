import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import random

contador_general = 0
bigramas = {}
trigramas = {}
tipo_ngrama = ""
texto_generado_completo = []

secure_random = random.SystemRandom()

def cargar_csv():
    global bigramas, trigramas, tipo_ngrama
    bigramas.clear()
    trigramas.clear()

    file_path = filedialog.askopenfilename(title="Seleccionar archivo CSV", filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

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


    archivo_label.config(text=f"Archivo cargado: {file_path.split('/')[-1]}")
    messagebox.showinfo("Éxito", f"Archivo de {tipo_ngrama}s cargado correctamente.")

def seleccionar_palabra_por_ruleta(contexto, ngramas):
    global contador_general
    contador_general += 1
    opciones = [(termino[-1], prob) for termino, prob in ngramas.items() if termino[:-1] == contexto]

    print(contador_general)
    print(f"Contexto: {contexto}")
    print(f"Opciones: {opciones}")

    # Verifica si hay opciones disponibles
    if not opciones:
        return "</s>"

    palabras, probabilidades = zip(*opciones)
    return secure_random.choices(palabras, weights=probabilidades, k=1)[0]

def obtener_contexto_inicial():
    global contador_general
    if tipo_ngrama == "bigrama":
        return ("<s>",)
    elif tipo_ngrama == "trigrama":
        # Filtra opciones de contexto de la forma ("<s>", alguna_palabra) en trigramas
        opciones_iniciales = [(term1, term2) for (term1, term2, _) in trigramas.keys() if term1 == "<s>"]

        if opciones_iniciales:
            return secure_random.choice(opciones_iniciales)
    return None

def generar_texto():
    global contador_general
    contador_general = 0
    contexto = obtener_contexto_inicial()
    if contexto is None:
        messagebox.showerror("Error", "No hay contexto inicial válido en el archivo cargado.")
        return

    texto = list(contexto)  # Empieza el texto con el contexto inicial

    while True:
        if tipo_ngrama == "bigrama":
            siguiente_palabra = seleccionar_palabra_por_ruleta(contexto, bigramas)
            contexto = (siguiente_palabra,)
        elif tipo_ngrama == "trigrama":
            siguiente_palabra = seleccionar_palabra_por_ruleta(contexto, trigramas)
            contexto = (contexto[-1], siguiente_palabra)  # Contexto actualizado

        if siguiente_palabra == "</s>":
            break

        texto.append(siguiente_palabra)

    # quitar la primera palabra
    print(texto)
    texto.pop(0)
    print(texto)
    texto_generado.delete("1.0", tk.END)
    texto_generado.insert(tk.END, " ".join(texto))

root = tk.Tk()
root.title("Generador de Texto")

# Botón para cargar archivo
btn_cargar_archivo = tk.Button(root, text="Cargar archivo CSV", command=cargar_csv)
btn_cargar_archivo.grid(row=0, column=0, pady=5)

# Etiqueta para mostrar el nombre del archivo
archivo_label = tk.Label(root, text="Archivo cargado: Ninguno", font=("Helvetica", 12))
archivo_label.grid(row=1, column=0, columnspan=2, pady=5)

# Botón para generar texto
btn_calcular = tk.Button(root, text="Generar texto", command=generar_texto)
btn_calcular.grid(row=2, column=0, columnspan=2, pady=5)

# Campo de texto más grande para el texto generado
texto_generado = tk.Text(root, width=60, height=10)
texto_generado.grid(row=5, column=0, columnspan=2, pady=5)

root.mainloop()
