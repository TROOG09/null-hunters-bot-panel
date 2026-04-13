import tkinter as tk
from tkinter import messagebox
import threading
import asyncio
import discord
from PIL import Image, ImageTk
import queue
import winsound

# =========================
# DISCORD BOT SETUP
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)

bot_loop = None
log_queue = queue.Queue()

# IMPORTANTE: mantener referencia de imagen
bg_photo = None


# =========================
# LOG SYSTEM
# =========================
def log(msg):
    log_queue.put(msg)


def update_logs():
    while not log_queue.empty():
        msg = log_queue.get()
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)
    root.after(500, update_logs)


# =========================
# SOUND
# =========================
def startup_sound():
    try:
        winsound.Beep(800, 100)
        winsound.Beep(1200, 150)
    except:
        pass


# =========================
# DISCORD EVENTS
# =========================
@client.event
async def on_ready():
    log(f"BOT conectado como: {client.user}")


# =========================
# SAFE ACTIONS
# =========================
async def send_message(channel_id, content):
    try:
        channel = client.get_channel(int(channel_id))
        if channel:
            await channel.send(content)
            log(f"Mensaje enviado a {channel_id}")
        else:
            log("Canal no encontrado")
    except Exception as e:
        log(f"Error send_message: {e}")


async def create_channel(guild_id, name):
    try:
        guild = client.get_guild(int(guild_id))
        if guild:
            channel = await guild.create_text_channel(name)
            log(f"Canal creado: {channel.name}")
    except Exception as e:
        log(f"Error create_channel: {e}")


async def delete_channel(channel_id):
    try:
        channel = client.get_channel(int(channel_id))
        if channel:
            await channel.delete()
            log(f"Canal eliminado: {channel_id}")
    except Exception as e:
        log(f"Error delete_channel: {e}")


# =========================
# RUN ASYNC
# =========================
def run_coro(coro):
    global bot_loop
    if bot_loop:
        asyncio.run_coroutine_threadsafe(coro, bot_loop)


# =========================
# START BOT THREAD
# =========================
def start_bot():
    token = entry_token.get().strip()

    if not token:
        messagebox.showerror("Error", "Introduce el token")
        return

    def run():
        global bot_loop
        bot_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(bot_loop)

        try:
            bot_loop.run_until_complete(client.start(token))
        except Exception as e:
            log(f"Bot error: {e}")

    threading.Thread(target=run, daemon=True).start()

    startup_sound()
    log("Iniciando bot...")


# =========================
# UI ACTIONS
# =========================
def ui_send():
    run_coro(send_message(entry_channel.get(), entry_message.get()))


def ui_create():
    run_coro(create_channel(entry_guild.get(), entry_name.get()))


def ui_delete():
    if messagebox.askyesno("Confirmación", "¿Seguro que quieres borrar este canal?"):
        run_coro(delete_channel(entry_channel.get()))


# =========================
# UI WINDOW
# =========================
root = tk.Tk()
root.title("NULL HUNTERS SYSTEM")
root.geometry("900x550")
root.configure(bg="black")
root.resizable(False, False)


# =========================
# BACKGROUND IMAGE (TU FOTO)
# =========================
try:
    img = Image.open("/mnt/data/image.png")
    img = img.resize((900, 550))
    bg_photo = ImageTk.PhotoImage(img)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

except Exception as e:
    print("Error cargando fondo:", e)


# =========================
# TITLE
# =========================
title = tk.Label(root, text="NULL HUNTERS CONTROL PANEL",
                 fg="lime", bg="black",
                 font=("Courier", 18, "bold"))
title.pack(pady=10)


# =========================
# INPUTS
# =========================
entry_token = tk.Entry(root, width=45, bg="black", fg="lime", insertbackground="lime")
entry_token.insert(0, "BOT TOKEN")
entry_token.pack(pady=5)

tk.Button(root, text="START BOT", command=start_bot,
          bg="green", fg="black").pack(pady=5)

entry_guild = tk.Entry(root, width=45, bg="black", fg="lime")
entry_guild.insert(0, "GUILD ID")
entry_guild.pack(pady=5)

entry_channel = tk.Entry(root, width=45, bg="black", fg="lime")
entry_channel.insert(0, "CHANNEL ID")
entry_channel.pack(pady=5)

entry_name = tk.Entry(root, width=45, bg="black", fg="lime")
entry_name.insert(20, "𝙽̷𝚄̷𝙻̷𝙻̷-𝙷̷𝚄̷𝙽̷𝚃̷𝙴̷𝚁̷𝚂̷ 𝙸̷𝚂̷ 𝙷̷𝙴̷𝚁̷𝙴̷E")
entry_name.pack(pady=5)

entry_message = tk.Entry(root, width=45, bg="black", fg="lime")
entry_message.insert(200, "𝙽̷𝚄̷𝙻̷𝙻̷-𝙷̷𝚄̷𝙽̷𝚃̷𝙴̷𝚁̷𝚂̷ 𝙸̷𝚂̷ 𝙷̷𝙴̷𝚁̷𝙴̷ https://discord.gg/Rfs9N3fya4 ")
entry_message.pack(pady=5)


# =========================
# BUTTONS
# =========================
tk.Button(root, text="SEND MESSAGE",
          command=ui_send,
          bg="gray", fg="white").pack(pady=3)

tk.Button(root, text="CREATE CHANNEL",
          command=ui_create,
          bg="blue", fg="white").pack(pady=3)

tk.Button(root, text="DELETE CHANNEL",
          command=ui_delete,
          bg="red", fg="white").pack(pady=3)


# =========================
# LOG BOX
# =========================
log_box = tk.Listbox(root, width=80, height=10,
                     bg="black", fg="lime")
log_box.pack(pady=10)


# =========================
# START LOOP
# =========================
update_logs()
root.mainloop()
