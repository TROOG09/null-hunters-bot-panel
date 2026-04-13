import tkinter as tk
from tkinter import ttk, messagebox
import threading
import discord
import json
import queue
import asyncio

# =========================
# CONFIG
# =========================
CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

config = load_config()

# =========================
# LOG SYSTEM
# =========================
log_queue = queue.Queue()

def log(text):
    log_queue.put(text)

def update_logs():
    while not log_queue.empty():
        msg = log_queue.get()
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)
    root.after(200, update_logs)

# =========================
# DISCORD BOT
# =========================
intents = discord.Intents.default()
client = discord.Client(intents=intents)

bot_token = None
target_channel_id = None


@client.event
async def on_ready():
    log(f"✅ Conectado como {client.user}")


def run_bot():
    try:
        client.run(bot_token)
    except Exception as e:
        log(f"❌ Error bot: {e}")


# =========================
# BOT ACTIONS (BUTTONS)
# =========================
def send_message():
    if not target_channel_id:
        messagebox.showerror("Error", "Configura Channel ID")
        return

    message = entry_message.get()

    async def task():
        channel = client.get_channel(int(target_channel_id))
        if channel:
            await channel.send(message)
            log("📨 Mensaje enviado")
        else:
            log("❌ Canal no encontrado")

    asyncio.run_coroutine_threadsafe(task(), client.loop)


def ping_test():
    async def task():
        for guild in client.guilds:
            log(f"📡 Servidor: {guild.name}")

    asyncio.run_coroutine_threadsafe(task(), client.loop)


# =========================
# START BOT
# =========================
def start_bot():
    global bot_token, target_channel_id

    bot_token = entry_token.get().strip()
    target_channel_id = entry_channel.get().strip()

    if not bot_token:
        messagebox.showerror("Error", "Token requerido")
        return

    config["token"] = bot_token
    config["channel_id"] = target_channel_id
    save_config(config)

    threading.Thread(target=run_bot, daemon=True).start()
    log("🚀 Iniciando bot...")


# =========================
# GUI (DASHBOARD)
# =========================
root = tk.Tk()
root.title("Control Center Bot Dashboard")
root.geometry("700x500")
root.configure(bg="#1e1e2e")

style = ttk.Style()
style.theme_use("clam")

# ===== TOP FRAME =====
top = ttk.Frame(root)
top.pack(fill="x", padx=10, pady=10)

ttk.Label(top, text="Bot Token").grid(row=0, column=0)
entry_token = ttk.Entry(top, width=40)
entry_token.grid(row=0, column=1)

ttk.Label(top, text="Channel ID").grid(row=1, column=0)
entry_channel = ttk.Entry(top, width=40)
entry_channel.grid(row=1, column=1)

# load config
if "token" in config:
    entry_token.insert(0, config["token"])
if "channel_id" in config:
    entry_channel.insert(0, config["channel_id"])

ttk.Button(top, text="Start Bot", command=start_bot).grid(row=2, column=1, pady=5)

# ===== BUTTON PANEL =====
btn_frame = ttk.LabelFrame(root, text="Control Panel")
btn_frame.pack(fill="x", padx=10, pady=10)

entry_message = ttk.Entry(btn_frame, width=50)
entry_message.grid(row=0, column=0, padx=5, pady=5)

ttk.Button(btn_frame, text="Send Message", command=send_message).grid(row=0, column=1, padx=5)
ttk.Button(btn_frame, text="Ping Servers", command=ping_test).grid(row=0, column=2, padx=5)

# ===== LOGS =====
log_frame = ttk.LabelFrame(root, text="Live Logs")
log_frame.pack(fill="both", expand=True, padx=10, pady=10)

log_box = tk.Listbox(log_frame, bg="black", fg="lime")
log_box.pack(fill="both", expand=True)

# start log updater
update_logs()

root.mainloop()
