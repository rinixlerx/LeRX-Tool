import tkinter as tk
from tkinter import messagebox, simpledialog
import socket
import psutil
import os
import wmi

# Couleurs style vert néon
BG_COLOR = "#0d1b0d"
BTN_COLOR = "#39ff14"
BTN_HOVER = "#2ecc40"
TEXT_COLOR = "#39ff14"
FONT_TITLE = ("Consolas", 36, "bold")
FONT_SUBTITLE = ("Consolas", 16, "bold")
FONT_BTN = ("Consolas", 12, "bold")
FONT_TEXT = ("Consolas", 10)

def on_enter(e):
    e.widget['background'] = BTN_HOVER

def on_leave(e):
    e.widget['background'] = BTN_COLOR

def scanner_ports_gui():
    ip = simpledialog.askstring("Scan de ports", "Entrez une adresse IP :")
    if ip:
        ports_ouverts = []
        for port in range(1, 1025):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            resultat = sock.connect_ex((ip, port))
            if resultat == 0:
                ports_ouverts.append(port)
            sock.close()
        if ports_ouverts:
            messagebox.showinfo("Résultat", f"Ports ouverts : {ports_ouverts}")
        else:
            messagebox.showinfo("Résultat", "Aucun port ouvert détecté.")

def surveiller_reseau_gui():
    stats = psutil.net_io_counters()
    message = f"Octets envoyés : {stats.bytes_sent}\nOctets reçus : {stats.bytes_recv}"
    messagebox.showinfo("Surveillance réseau", message)

def afficher_temperature_gui():
    try:
        capteur = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        capteurs = capteur.Sensor()
        temp_list = ""
        for c in capteurs:
            if c.SensorType == u'Temperature':
                temp_list += f"{c.Name} : {c.Value}°C\n"
        messagebox.showinfo("Température CPU", temp_list or "Aucune température détectée.")
    except Exception:
        messagebox.showerror("Erreur", "Vérifie qu'OpenHardwareMonitor est lancé.")

def nettoyer_temp_gui():
    temp = os.getenv('TEMP')
    fichiers_supprimes = 0
    for racine, dossiers, fichiers in os.walk(temp):
        for f in fichiers:
            chemin = os.path.join(racine, f)
            try:
                os.remove(chemin)
                fichiers_supprimes += 1
            except:
                continue
    messagebox.showinfo("Nettoyage", f"{fichiers_supprimes} fichiers supprimés.")

def afficher_processus_gui():
    processus = ""
    for p in psutil.process_iter(['pid', 'name']):
        processus += f"PID: {p.info['pid']} | Nom: {p.info['name']}\n"
    messagebox.showinfo("Processus actifs", processus[:1000])  # Limite le texte

def afficher_infos_systeme_gui():
    try:
        c = wmi.WMI()
        cpu = c.Win32_Processor()[0].Name.strip()
        mem = psutil.virtual_memory()
        ram_gb = mem.total / (1024 ** 3)
        disque = psutil.disk_usage('C:\\')
        disque_total_gb = disque.total / (1024 ** 3)
        disque_libre_gb = disque.free / (1024 ** 3)
        gpu = "Non détectée"
        gpus = c.Win32_VideoController()
        if gpus:
            gpu = gpus[0].Name.strip()
        
        info = (
            f"💻 Processeur : {cpu}\n"
            f"🧠 RAM : {ram_gb:.2f} GB\n"
            f"💾 Disque C: : {disque_total_gb:.2f} GB total, {disque_libre_gb:.2f} GB libre\n"
            f"🎮 Carte graphique : {gpu}"
        )
        messagebox.showinfo("Infos système", info)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de récupérer les infos système.\n{e}")

# Fenêtre principale
fenetre = tk.Tk()
fenetre.title("Le RX - Multi Tool")
fenetre.geometry("450x520")
fenetre.configure(bg=BG_COLOR)
fenetre.resizable(False, False)

# Titre énorme "Le RX"
titre = tk.Label(fenetre, text="Le RX", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR)
titre.pack(pady=(20, 5))

# Sous-titre
sous_titre = tk.Label(fenetre, text="🛠 Multi Tool - Version Graphique", font=FONT_SUBTITLE, bg=BG_COLOR, fg=TEXT_COLOR)
sous_titre.pack(pady=(0, 25))

# Boutons et actions
boutons = [
    ("🔍 Scanner les ports", scanner_ports_gui),
    ("📡 Surveiller le réseau", surveiller_reseau_gui),
    ("🌡 Température CPU", afficher_temperature_gui),
    ("🧹 Nettoyage fichiers temp", nettoyer_temp_gui),
    ("⚙ Voir les processus", afficher_processus_gui),
    ("🖥 Infos système", afficher_infos_systeme_gui),
]

for nom, action in boutons:
    btn = tk.Button(fenetre, text=nom, command=action, bg=BTN_COLOR, fg="black", font=FONT_BTN,
                    activebackground=BTN_HOVER, activeforeground="black", bd=0, relief="flat", cursor="hand2")
    btn.pack(pady=10, ipadx=10, ipady=8)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

fenetre.mainloop()
