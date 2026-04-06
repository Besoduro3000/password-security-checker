import tkinter as tk
from tkinter import messagebox
import string
import random

def verificar_contraseña():
    password = entry_password.get()
    
    if not password:
        messagebox.showwarning("Advertencia", "Por favor ingrese una contraseña")
        return
    
    # Verificar características de la contraseña
    upper_case = any(c in string.ascii_uppercase for c in password)
    lower_case = any(c in string.ascii_lowercase for c in password)
    special = any(c in string.punctuation for c in password)
    digits = any(c in string.digits for c in password)
    
    faltantes = []

    if not upper_case:
        faltantes.append(" Mayúsculas")
    if not lower_case:
        faltantes.append(" Minúsculas")
    if not digits:
        faltantes.append(" Números")
    if not special:
        faltantes.append(" Símbolos")

    resultado_texto = ""
    if faltantes:
        resultado_texto += "\n⚠️ Falta: " + ", ".join(faltantes)
    
    # Verificar si es una contraseña común
    try:
        with open(r'C:\Users\User\Desktop\Ejercicios con chat\Ejercicios\common.txt', 'r', encoding='utf-8') as f:
            common = set(f.read().splitlines())
        
        if password in common:
            messagebox.showwarning("Contraseña Insegura", 
                                 f"La contraseña es común, no es segura.\nScore: 0/7")
            label_resultado.config(text="", fg="black")
            return
    except FileNotFoundError:
        messagebox.showwarning("Archivo no encontrado", 
                             "No se pudo verificar contra contraseñas comunes.\nContinuando con la verificación...")
    
    # Calcular score
    characters = [upper_case, lower_case, special, digits]
    length = len(password)
    score = 0
    
    # Puntuación por longitud
    if length > 8:
        score += 1
    if length > 12:
        score += 1
    if length > 16:
        score += 1
    if length > 20:
        score += 1
    
    # Puntuación por variedad de caracteres
    if sum(characters) > 1:
        score += 1
    if sum(characters) > 2:
        score += 1
    if sum(characters) > 3:
        score += 1
    
    # Mostrar resultados
    resultado_texto += f"📏 Longitud: {length} caracteres\n"
    resultado_texto += f"🔤 Tipos de caracteres: {sum(characters)}/4\n"
    resultado_texto += f"⭐ Puntuación total: {score}/7\n\n"
    
    # Determinar nivel de seguridad y color
    if score < 4:
        resultado_texto += "🔴 NIVEL: DÉBIL - No es segura"
        color = "red"
    elif score == 4:
        resultado_texto += "🟡 NIVEL: ACEPTABLE"
        color = "orange"
    elif score > 4 and score < 6:
        resultado_texto += "🟢 NIVEL: BUENA - Podría ser más segura"
        color = "#0055cc"  # Azul más visible
    elif score >= 6:
        resultado_texto += "🟢 NIVEL: FUERTE"
        color = "green"
    
    if score == 7:
        resultado_texto += "\n✨ ¡EXCELENTE! ✨"
    
    label_resultado.config(text=resultado_texto, fg=color)
    

def mostrar_ocultar():
    """Alternar entre mostrar y ocultar la contraseña"""
    if mostrar.get():
        entry_password.config(show="")
        btn_mostrar.config(text="🙈 Ocultar")
        mostrar.set(False)
    else:
        entry_password.config(show="*")
        btn_mostrar.config(text="👁️ Mostrar")
        mostrar.set(True)

def limpiar_campos():
    """Limpiar todos los campos"""
    entry_password.delete(0, tk.END)
    label_resultado.config(text="", fg="black")
    entry_password.focus()

def generar_contraseña():
    """Generar una contraseña segura"""
    # Aseguramos que tenga al menos un carácter de cada tipo
    mayuscula = random.choice(string.ascii_uppercase)
    minuscula = random.choice(string.ascii_lowercase)
    digito = random.choice(string.digits)
    simbolo = random.choice(string.punctuation)
    
    # Completamos con más caracteres aleatorios
    resto = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))
    
    # Mezclamos todos los caracteres
    contraseña_lista = list(mayuscula + minuscula + digito + simbolo + resto)
    random.shuffle(contraseña_lista)
    contraseña = ''.join(contraseña_lista)
    
    # Limpiar y mostrar la nueva contraseña (con asteriscos por seguridad)
    entry_password.delete(0, tk.END)
    entry_password.insert(0, contraseña)
    
    # Opcional: Mostrar mensaje de que se generó la contraseña
    messagebox.showinfo("Contraseña Generada", 
                       "Se ha generado una contraseña segura de 16 caracteres.\n"
                       "Presiona 'Verificar' para evaluar su seguridad.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("🔒 Verificador de Seguridad de Contraseñas 🔒")
ventana.geometry("650x500")  # Ventana más grande
ventana.resizable(True, True)  # Ahora se puede redimensionar
ventana.minsize(550, 450)  # Tamaño mínimo

# Configurar color de fondo con gradiente suave
ventana.configure(bg="#e8f4f8")

# Título con marco
frame_titulo = tk.Frame(ventana, bg="#2c3e50", height=80)
frame_titulo.pack(fill="x", pady=(0, 20))
frame_titulo.pack_propagate(False)

titulo = tk.Label(frame_titulo, text="🔐 VERIFICADOR DE CONTRASEÑAS SEGURAS 🔐", 
                  font=("Arial", 18, "bold"), bg="#2c3e50", fg="white")
titulo.pack(expand=True)

# Marco para la entrada de contraseña
frame_password = tk.Frame(ventana, bg="#e8f4f8")
frame_password.pack(pady=30)

label_password = tk.Label(frame_password, text="🔑 Contraseña:", 
                         font=("Arial", 13, "bold"), bg="#e8f4f8", fg="#2c3e50")
label_password.grid(row=0, column=0, padx=15)

entry_password = tk.Entry(frame_password, show="*", width=35, 
                         font=("Arial", 13), relief="solid", bd=2)
entry_password.grid(row=0, column=1, padx=10, pady=10)
entry_password.bind('<Return>', lambda event: verificar_contraseña())

# Variable para controlar mostrar/ocultar
mostrar = tk.BooleanVar(value=True)

btn_mostrar = tk.Button(frame_password, text="👁️ Mostrar", 
                       command=mostrar_ocultar, font=("Arial", 10, "bold"),
                       bg="#3498db", fg="white", padx=10)
btn_mostrar.grid(row=0, column=2, padx=10)

# Marco para los botones principales
frame_botones = tk.Frame(ventana, bg="#e8f4f8")
frame_botones.pack(pady=20)

btn_verificar = tk.Button(frame_botones, text="✅ Verificar Contraseña", 
                         command=verificar_contraseña, 
                         font=("Arial", 11, "bold"), bg="#27ae60", 
                         fg="white", padx=25, pady=8, cursor="hand2")
btn_verificar.grid(row=0, column=0, padx=12)

btn_limpiar = tk.Button(frame_botones, text="🗑️ Limpiar", 
                       command=limpiar_campos, 
                       font=("Arial", 11, "bold"), bg="#e74c3c", 
                       fg="white", padx=25, pady=8, cursor="hand2")
btn_limpiar.grid(row=0, column=1, padx=12)

btn_generar = tk.Button(frame_botones, text="🎲 Generar Contraseña Segura", 
                       command=generar_contraseña, 
                       font=("Arial", 11, "bold"), bg="#3498db", 
                       fg="white", padx=20, pady=8, cursor="hand2")
btn_generar.grid(row=0, column=2, padx=12)

# Marco para mostrar resultados
frame_resultado = tk.Frame(ventana, bg="white", relief="groove", bd=3)
frame_resultado.pack(pady=20, padx=30, fill="both", expand=True)

# Título del marco de resultados
label_resultado_titulo = tk.Label(frame_resultado, text="📊 RESULTADO DEL ANÁLISIS 📊", 
                                 font=("Arial", 12, "bold"), bg="white", 
                                 fg="#2c3e50")
label_resultado_titulo.pack(pady=(15, 5))

label_resultado = tk.Label(frame_resultado, text="", 
                          font=("Arial", 12), bg="white", 
                          justify="left", wraplength=550)
label_resultado.pack(pady=15, padx=25)

barra = tk.Canvas(frame_resultado, width=300, height=20)
barra.pack(pady=10)

# Información de ayuda
info_frame = tk.Frame(ventana, bg="#e8f4f8")
info_frame.pack(pady=15, fill="x")

info_label = tk.Label(info_frame, 
                     text="💡 CONSEJO: Use mayúsculas, minúsculas, números y símbolos para mayor seguridad\n"
                          "🔒 Las contraseñas generadas son de 16 caracteres y se muestran con asteriscos por seguridad",
                     font=("Arial", 9), bg="#e8f4f8", fg="#555", justify="center")
info_label.pack()

# Barra de estado (footer)
footer = tk.Label(ventana, text="🔐 Verificador de Seguridad v2.0 | Desarrollado con Tkinter", 
                 font=("Arial", 8), bg="#2c3e50", fg="white")
footer.pack(side="bottom", fill="x")

# Iniciar la aplicación
ventana.mainloop()