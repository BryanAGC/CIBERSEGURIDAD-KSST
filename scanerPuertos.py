import os
import re
import tkinter as tk
from tkinter import ttk, messagebox
import socket
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Función para obtener la IP de tu computadora
def obtener_ip_local():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip

# Función para escanear la red
def escanear_red():
    network = entry_red.get()
    label_status.config(text="Escaneando la red...", fg="blue")
    ventana.update()

    ip_local = obtener_ip_local()
    result = os.popen(f"nmap -sn {network}").read()
    dispositivos = re.findall(r"Nmap scan report for (\S+).*?MAC Address: (\S+) \((.*?)\)", result, re.DOTALL)

    for row in tree.get_children():
        tree.delete(row)

    tree.insert("", "end", values=(ip_local, "Local", "MiPC"))

    if dispositivos:
        for ip, mac, vendor in dispositivos:
            tree.insert("", "end", values=(ip, mac, vendor))
        label_status.config(text="Escaneo completado.", fg="green")
    else:
        label_status.config(text="No se encontraron dispositivos.", fg="red")

# Función para ver puertos abiertos de un dispositivo
def ver_puertos():
    selected_item = tree.selection()
    if selected_item:
        ip = tree.item(selected_item[0])['values'][0]
        label_status.config(text=f"Verificando puertos abiertos de {ip}...", fg="blue")
        ventana.update()

        result = os.popen(f"nmap -p- {ip}").read()
        puertos = re.findall(r"(\d+)/tcp\s+open", result)

        for row in tree_puertos.get_children():
            tree_puertos.delete(row)

        if puertos:
            for puerto in puertos:
                tree_puertos.insert("", "end", values=(puerto,))
            label_status.config(text=f"Puertos abiertos de {ip}:", fg="green")
        else:
            label_status.config(text=f"No se encontraron puertos abiertos en {ip}.", fg="red")
    else:
        messagebox.showwarning("Seleccionar dispositivo", "Por favor, selecciona un dispositivo para ver los puertos.")

# Función para generar el PDF
def generar_pdf():
    selected_item = tree.selection()
    if selected_item:
        ip = tree.item(selected_item[0])['values'][0]
        mac = tree.item(selected_item[0])['values'][1]
        vendor = tree.item(selected_item[0])['values'][2]

        pdf_filename = f"dispositivo_{ip}_informacion.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)

        c.setFont("Helvetica", 16)
        c.drawString(30, 750, f"Información del dispositivo {ip}:")

        c.setFont("Helvetica", 12)
        c.drawString(30, 730, f"IP: {ip}")
        c.drawString(30, 710, f"MAC: {mac}")
        c.drawString(30, 690, f"Fabricante: {vendor}")

        result = os.popen(f"nmap -p- {ip}").read()
        puertos = re.findall(r"(\d+)/tcp\s+open", result)

        c.drawString(30, 670, "Puertos abiertos:")
        y_position = 650
        for puerto in puertos:
            c.drawString(30, y_position, f"Puerto {puerto} TCP")
            y_position -= 20

        c.save()
        messagebox.showinfo("PDF generado", f"Se ha generado el PDF con la información de {ip}.")
    else:
        messagebox.showwarning("Seleccionar dispositivo", "Por favor, selecciona un dispositivo para generar el PDF.")

# Crear ventana
ventana = tk.Tk()
ventana.title("Escáner de Red Colorido")
ventana.geometry("800x500")
ventana.configure(bg="#F3F4F6")

frame = tk.Frame(ventana, bg="#F3F4F6")
frame.pack(pady=10)

label_red = tk.Label(frame, text="Red a escanear (ej. 192.168.0.0/24):", bg="#F3F4F6", fg="#333333")
label_red.pack()
entry_red = tk.Entry(frame, width=30)
entry_red.insert(0, "192.168.0.0/24")
entry_red.pack(pady=5)

btn_escanear = tk.Button(frame, text="Escanear Red", command=escanear_red, bg="#4CAF50", fg="white", width=20)
btn_escanear.pack(pady=5)

label_status = tk.Label(frame, text="Introduce la red y presiona el botón para iniciar el escaneo.", bg="#F3F4F6", fg="#555555")
label_status.pack(pady=5)

columns = ("IP", "MAC", "Fabricante")
tree = ttk.Treeview(ventana, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(pady=10)

btn_ver_puertos = tk.Button(frame, text="Ver Puertos Abiertos", command=ver_puertos, bg="#2196F3", fg="white", width=20)
btn_ver_puertos.pack(pady=5)

columns_puertos = ("Puerto",)
tree_puertos = ttk.Treeview(ventana, columns=columns_puertos, show="headings")
for col in columns_puertos:
    tree_puertos.heading(col, text=col)
    tree_puertos.column(col, width=150)
tree_puertos.pack(pady=10)

btn_generar_pdf = tk.Button(frame, text="Generar PDF", command=generar_pdf, bg="#FFC107", fg="black", width=20)
btn_generar_pdf.pack(pady=10)

ventana.mainloop()
