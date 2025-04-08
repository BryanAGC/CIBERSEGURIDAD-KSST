import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_passwords():
    try:
        length = int(entry_length.get())
        num_passwords = int(entry_num_passwords.get())
        if length < 8:
            messagebox.showerror("Error", "La longitud de la contraseña debe ser al menos de 8 caracteres")
            return
        if num_passwords <= 0:
            messagebox.showerror("Error", "El número de contraseñas debe ser mayor a 0")
            return
        
        # Construir el conjunto de caracteres según las selecciones
        characters = ""
        if var_uppercase.get():
            characters += string.ascii_uppercase
        if var_lowercase.get():
            characters += string.ascii_lowercase
        if var_digits.get():
            characters += string.digits
        if var_symbols.get():
            characters += string.punctuation

        if not characters:
            messagebox.showerror("Error", "Selecciona al menos un tipo de carácter")
            return
        
        passwords = []
        for _ in range(num_passwords):
            password = ''.join(random.choice(characters) for _ in range(length))
            passwords.append(password)
        
        text_passwords.delete("1.0", tk.END)
        text_passwords.insert(tk.END, "\n".join(passwords))
    except ValueError:
        messagebox.showerror("Error", "Ingrese números válidos")

def copy_to_clipboard():
    passwords = text_passwords.get("1.0", tk.END).strip()
    if passwords:
        root.clipboard_clear()
        root.clipboard_append(passwords)
        root.update()
        messagebox.showinfo("Copiar al portapapeles", "Contraseñas copiadas al portapapeles")
    else:
        messagebox.showwarning("Advertencia", "No hay contraseñas para copiar")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Generador de Contraseñas Seguro y Colorido")
root.geometry("450x500")
root.resizable(False, False)
root.configure(bg="#F3F4F6")  # Fondo color gris claro

# Etiqueta y campo para la longitud de la contraseña
frame_inputs = tk.Frame(root, bg="#F3F4F6")
frame_inputs.pack(pady=10)
tk.Label(frame_inputs, text="Longitud de la contraseña:", bg="#F3F4F6", fg="#333333").grid(row=0, column=0, padx=5, pady=5)
entry_length = tk.Entry(frame_inputs, width=10)
entry_length.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Número de contraseñas:", bg="#F3F4F6", fg="#333333").grid(row=1, column=0, padx=5, pady=5)
entry_num_passwords = tk.Entry(frame_inputs, width=10)
entry_num_passwords.grid(row=1, column=1, padx=5, pady=5)

# Checkboxes para seleccionar tipos de caracteres
frame_options = tk.Frame(root, bg="#F3F4F6")
frame_options.pack(pady=10)
var_uppercase = tk.BooleanVar()
var_lowercase = tk.BooleanVar()
var_digits = tk.BooleanVar()
var_symbols = tk.BooleanVar()

tk.Checkbutton(frame_options, text="Incluir mayúsculas", variable=var_uppercase, bg="#F3F4F6", fg="#333333").grid(row=0, column=0, padx=10, pady=5)
tk.Checkbutton(frame_options, text="Incluir minúsculas", variable=var_lowercase, bg="#F3F4F6", fg="#333333").grid(row=0, column=1, padx=10, pady=5)
tk.Checkbutton(frame_options, text="Incluir números", variable=var_digits, bg="#F3F4F6", fg="#333333").grid(row=1, column=0, padx=10, pady=5)
tk.Checkbutton(frame_options, text="Incluir símbolos", variable=var_symbols, bg="#F3F4F6", fg="#333333").grid(row=1, column=1, padx=10, pady=5)

# Botones
frame_buttons = tk.Frame(root, bg="#F3F4F6")
frame_buttons.pack(pady=10)
tk.Button(frame_buttons, text="Generar", command=generate_passwords, width=15, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_buttons, text="Copiar al portapapeles", command=copy_to_clipboard, width=15, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5, pady=5)

# Área para mostrar las contraseñas generadas
tk.Label(root, text="Contraseñas Generadas:", bg="#F3F4F6", fg="#333333").pack(pady=5)
text_passwords = tk.Text(root, height=10, width=50, bg="#E8EAF6", fg="#333333")
text_passwords.pack(pady=10)

# Iniciar la interfaz gráfica
root.mainloop()
