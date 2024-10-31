import tkinter as tk
from tkinter import filedialog, messagebox


modelos_bigrama = {}
modelos_trigrama = {}
modelos_seleccionados = []


def cargar_csv():
    file_paths = filedialog.askopenfilenames(title="Seleccionar archivos CSV", filetypes=[("CSV Files", "*.csv")])
    if not file_paths:
        return

    for file_path in file_paths:
        with open(file_path, newline='') as csvfile:
            header = csvfile.readline().strip().split(",")

            modelo_nombre = file_path.split('/')[-1]  # Nombre del archivo

            if header[:3] == ["Term1", "Term2", "Term3"]:
                modelos_trigrama[modelo_nombre] = file_path
                lista_trigrama.insert(tk.END, modelo_nombre)
            elif header[:2] == ["Term1", "Term2"]:
                modelos_bigrama[modelo_nombre] = file_path
                lista_bigrama.insert(tk.END, modelo_nombre)
            else:
                messagebox.showerror("Error", f"Formato de archivo no válido para '{modelo_nombre}'.")
                continue

    messagebox.showinfo("Éxito", "Archivos cargados correctamente.")



def seleccionar_modelos():
    tipo_ngrama = var_ngrama.get()
    modelos_seleccionados.clear()

    if tipo_ngrama == "bigrama":
        modelos_seleccionados.extend(modelos_bigrama.keys())
    elif tipo_ngrama == "trigrama":
        modelos_seleccionados.extend(modelos_trigrama.keys())


def calcular_probabilidad():

    frase = entrada_frase.get("1.0", tk.END).strip()

    if not frase or not modelos_seleccionados:
        messagebox.showerror("Error", "Por favor, ingrese una frase y seleccione modelos.")
        return

    resultados = calcular_probabilidades(frase, modelos_seleccionados)

    resultados_area.delete("1.0", tk.END)
    for modelo, probabilidad in resultados.items():
        resultados_area.insert(tk.END, f"{modelo}: {probabilidad:.2f}%\n")


def calcular_probabilidades(frase, modelos_seleccionados):

    resultados = {}
    for modelo in modelos_seleccionados:
        resultados[modelo] = 10 + (len(modelo) % 50)
    return resultados


root = tk.Tk()
root.title("Cargador y Selector de Modelos de Lenguaje")

btn_cargar_archivo = tk.Button(root, text="Cargar modelos CSV", command=cargar_csv)
btn_cargar_archivo.grid(row=0, column=0, pady=5, columnspan=2)

tk.Label(root, text="Modelos de Bigramas:").grid(row=1, column=0, pady=5)
tk.Label(root, text="Modelos de Trigramas:").grid(row=1, column=1, pady=5)

lista_bigrama = tk.Listbox(root, width=30, height=10, selectmode=tk.MULTIPLE)
lista_bigrama.grid(row=2, column=0, pady=5)
lista_trigrama = tk.Listbox(root, width=30, height=10, selectmode=tk.MULTIPLE)
lista_trigrama.grid(row=2, column=1, pady=5)

var_ngrama = tk.StringVar(value="bigrama")
radio_bigrama = tk.Radiobutton(root, text="Usar Bigramas", variable=var_ngrama, value="bigrama", command=seleccionar_modelos)
radio_bigrama.grid(row=3, column=0, pady=5)
radio_trigrama = tk.Radiobutton(root, text="Usar Trigramas", variable=var_ngrama, value="trigrama", command=seleccionar_modelos)
radio_trigrama.grid(row=3, column=1, pady=5)

tk.Label(root, text="Escriba una frase:").grid(row=6, column=0, columnspan=2, pady=5)
entrada_frase = tk.Text(root, width=60, height=3)
entrada_frase.grid(row=7, column=0, columnspan=2, pady=5)

btn_calcular_probabilidad = tk.Button(root, text="Calcular Probabilidad", command=calcular_probabilidad)
btn_calcular_probabilidad.grid(row=8, column=0, columnspan=2, pady=5)

tk.Label(root, text="Resultados:").grid(row=9, column=0, columnspan=2, pady=5)
resultados_area = tk.Text(root, width=65, height=5)
resultados_area.grid(row=10, column=0, columnspan=2, pady=5)

root.mainloop()