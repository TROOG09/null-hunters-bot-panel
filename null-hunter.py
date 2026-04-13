import tkinter as tk
from tkinter import messagebox
import threading
import asyncio
import discord
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
        else:
            log("Guild no encontrada")
    except Exception as e:
        log(f"Error create_channel: {e}")

async def delete_channel(channel_id):
    try:
        channel = client.get_channel(int(channel_id))
        if channel:
            await channel.delete()
            log(f"Canal eliminado: {channel_id}")
        else:
            log("Canal no encontrado")
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
root.title("Control Panel")
root.geometry("600x500")
root.configure(bg="#2b2b2b")
root.resizable(False, False)

# =========================
# TITLE
# =========================
title = tk.Label(root, text="DISCORD CONTROL PANEL",
                 fg="white", bg="#2b2b2b",
                 font=("Arial", 16, "bold"))
title.pack(pady=10)

# =========================
# INPUTS
# =========================
def create_entry(placeholder):
    entry = tk.Entry(root, width=40, bg="#3c3f41", fg="white", insertbackground="white")
    entry.insert(0, placeholder)
    entry.pack(pady=5)
    return entry

entry_token = create_entry("BOT TOKEN")
tk.Button(root, text="START BOT", command=start_bot,
          bg="#4CAF50", fg="white").pack(pady=5)

entry_guild = create_entry("GUILD ID")
entry_channel = create_entry("CHANNEL ID")
entry_name = create_entry("Nombre del canal")
entry_message = create_entry("Mensaje a enviar")

# =========================
# BUTTONS
# =========================
tk.Button(root, text="SEND MESSAGE",
          command=ui_send,
          bg="#607D8B", fg="white").pack(pady=3)

tk.Button(root, text="CREATE CHANNEL",
          command=ui_create,
          bg="#2196F3", fg="white").pack(pady=3)

tk.Button(root, text="DELETE CHANNEL",
          command=ui_delete,
          bg="#f44336", fg="white").pack(pady=3)

# =========================
# LOG BOX
# =========================
log_box = tk.Listbox(root, width=70, height=10,
                     bg="#1e1e1e", fg="white")
log_box.pack(pady=10)

# =========================
# START LOOP
# =========================
update_logs()
root.mainloop()
