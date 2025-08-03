import os
import socket
import psutil
import platform
import subprocess
import time
from datetime import datetime
import sys

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def typer(text, delay=0.005):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def typer_rapide(text):
    typer(text, delay=0.001)

def typer_reponse(text):
    typer(text, delay=0.003)

def input_vert(prompt):
    return input("\033[92m" + prompt + "\033[0m")

def print_title():
    left = [
        " ___       _______           ________     ___    ___ ",
        "|\  \     |\  ___ \         |\   __  \   |\  \  /  /|",     
        "\ \  \    \ \   __/|        \ \  \|\  \  \ \  \/  / /",
        " \ \  \    \ \  \_|/__       \ \   _  _\  \ \    / / ",
        "  \ \  \____\ \  \_|\ \       \ \  \\  \|  /     \/  ",
        "   \ \_______\ \_______\       \ \__\\ _\ /  /\   \  ",
        "    \|_______|\|_______|        \|__|\|__/__/ /\ __\ ",
        "                                         |__|/ \|__| "
    ]

    right = [ 
        "______  ___      _______________    _____            ______",
        "___   |/  /___  ____  /_  /___(_)   __  /_______________  /",
        "__  /|_/ /_  / / /_  /_  __/_  /    _  __/  __ \\  __ \\_  / ",
        "_  /  / / / /_/ /_  / / /_ _  /     / /_ / /_/ / /_/ /  /  ",
        " /_/  /_/  \\__,_/ /_/  \__/ /_/      \__/ \____/\____//_/   "
    ]

    print("\033[92m", end='')
    for i in range(max(len(left), len(right))):
        ligne_gauche = left[i] if i < len(left) else " " * len(left[0])
        ligne_droite = right[i] if i < len(right) else ""
        typer_rapide(f"{ligne_gauche}   {ligne_droite}")
    print("\033[0m", end='')

    total_width = len(left[0]) + 3 + max(len(line) for line in right)
    texte_sous_titre = "github.com/rinixlerx/LeRX-Tool"
    espace_gauche = (total_width - len(texte_sous_titre)) // 2
    print(" " * espace_gauche + texte_sous_titre)

    print("\033[0m", end='')

def menu():
    typer_reponse("\033[92m1. \U0001F50D Scanner les ports")
    typer_reponse("2. \U0001F4E1 Surveiller le r\u00e9seau")
    typer_reponse("3. \U0001F321 Temp\u00e9rature CPU")
    typer_reponse("4. \u2699 Voir les processus")
    typer_reponse("5. \U0001F4BB Infos syst\u00e8me")
    typer_reponse("6. \U0001F5D1 Vider la corbeille")
    typer_reponse("7. \U0001F5AE Supprimer fichiers inutiles (temp)")
    typer_reponse("8. \U0001F4F6 Test de vitesse Internet (ping)")
    typer_reponse("9. \U0001F4BD Afficher espace disque")
    typer_reponse("10. \U0001F50D Recherche fichiers volumineux (>100 Mo)")
    typer_reponse("11. \U0001F6E1 V\u00e9rification antivirus basique")
    typer_reponse("0. \u274C Quitter\033[0m")

def scanner_ports():
    clear()
    target = input_vert("Entrez l'adresse IP ou l'h\u00f4te \u00e0 scanner : ")
    typer("Scan des ports en cours (1-1024)...")
    try:
        for port in range(1, 1025):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))
            if result == 0:
                typer_reponse(f"Port {port} \033[92m[OUVERT]\033[0m")
            sock.close()
    except Exception as e:
        typer_reponse(f"\033[91mErreur : {e}\033[0m")

def surveiller_reseau():
    clear()
    net_io = psutil.net_io_counters()
    typer_reponse(f"Octets envoy\u00e9s : {net_io.bytes_sent}")
    typer_reponse(f"Octets re\u00e7us : {net_io.bytes_recv}")

def afficher_temperature():
    clear()
    try:
        temp = psutil.sensors_temperatures()
        if not temp:
            typer_reponse("Aucune donn\u00e9e de temp\u00e9rature disponible.")
            return
        for name, entries in temp.items():
            typer(f"{name} :")
            for entry in entries:
                typer_reponse(f"  {entry.label or 'Capteur'}: {entry.current}\u00b0C")
    except Exception as e:
        typer_reponse(f"Erreur : {e}")

def afficher_processus():
    clear()
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        typer_reponse(f"PID: {proc.info['pid']} - Nom: {proc.info['name']} - Utilisateur: {proc.info['username']}")

def infos_systeme():
    clear()
    typer_reponse(f"Nom de la machine : {platform.node()}")
    typer_reponse(f"Syst\u00e8me : {platform.system()} {platform.release()}")
    typer_reponse(f"Processeur : {platform.processor()}")
    typer_reponse(f"Architecture : {platform.architecture()[0]}")
    typer_reponse(f"RAM disponible : {round(psutil.virtual_memory().total / (1024**3), 2)} Go")

def vider_corbeille():
    clear()
    try:
        if os.name == 'nt':
            subprocess.run("powershell.exe Clear-RecycleBin -Force", shell=True)
        else:
            trash_path = os.path.expanduser("~/.local/share/Trash/files")
            if os.path.exists(trash_path):
                subprocess.run(["rm", "-rf", trash_path])
        typer_reponse("Corbeille vid\u00e9e avec succ\u00e8s.")
    except Exception as e:
        typer_reponse(f"Erreur : {e}")

def supprimer_fichiers_inutiles():
    clear()
    try:
        if os.name == 'nt':
            temp_path = os.getenv('TEMP')
            subprocess.run(f"del /q/f/s {temp_path}\\*", shell=True)
        else:
            subprocess.run(["rm", "-rf", "/tmp/*"])
        typer_reponse("Fichiers temporaires supprim\u00e9s.")
    except Exception as e:
        typer_reponse(f"Erreur : {e}")

def test_vitesse_internet():
    clear()
    typer("Test de ping vers google.com...")
    try:
        if os.name == 'nt':
            subprocess.run("ping google.com -n 4", shell=True)
        else:
            subprocess.run(["ping", "-c", "4", "google.com"])
    except Exception as e:
        typer_reponse(f"Erreur : {e}")

def afficher_espace_disque():
    clear()
    partitions = psutil.disk_partitions()
    for part in partitions:
        usage = psutil.disk_usage(part.mountpoint)
        typer_reponse(f"{part.mountpoint} : {round(usage.used / (1024**3), 2)} Go utilisés sur {round(usage.total / (1024**3), 2)} Go")

def recherche_fichiers_volumineux():
    clear()
    chemin = input_vert("Chemin du dossier \u00e0 scanner (ex: /home/user) : ")
    try:
        for dossier, _, fichiers in os.walk(chemin):
            for fichier in fichiers:
                chemin_complet = os.path.join(dossier, fichier)
                if os.path.isfile(chemin_complet):
                    taille = os.path.getsize(chemin_complet)
                    if taille > 100 * 1024 * 1024:
                        typer_reponse(f"{chemin_complet} - {round(taille / (1024**2), 2)} Mo")
    except Exception as e:
        typer_reponse(f"Erreur : {e}")

def verification_antivirus():
    clear()
    typer("Simuler une v\u00e9rification antivirus...")
    time.sleep(2)
    typer_reponse("Aucune menace d\u00e9tect\u00e9e. (Simulation)")

def menu_secret():
    clear()
    typer_rapide("\033[92mBravo, tu as trouvé le menu secret 🎉\033[0m\n")
    typer_rapide("\033[92mTu es observé 👁\033[0m\n")
    typer_rapide("""\033[1;92m
     _        _        _        _        _    
   _( )__   _( )__   _( )__   _( )__   _( )__ 
 _|     _|_|     _|_|     _|_|     _|_|     _| 
(_ B _ (_(_ R _ (_(_ A _ (_(_ V _ (_(_ 0 _ (_ 
  |_( )__| |_( )__| |_( )__| |_( )__| |_( )__|
\033[0m""")
    input_vert("\nAppuie sur Entrée pour revenir au menu principal...")

def main():
    while True:
        clear()
        print_title()
        menu()
        choix = input_vert("Choisis une option ou tape le code secret : ").strip()
        if choix == "1":
            scanner_ports()
        elif choix == "2":
            surveiller_reseau()
        elif choix == "3":
            afficher_temperature()
        elif choix == "4":
            afficher_processus()
        elif choix == "5":
            infos_systeme()
        elif choix == "6":
            vider_corbeille()
        elif choix == "7":
            supprimer_fichiers_inutiles()
        elif choix == "8":
            test_vitesse_internet()
        elif choix == "9":
            afficher_espace_disque()
        elif choix == "10":
            recherche_fichiers_volumineux()
        elif choix == "11":
            verification_antivirus()
        elif choix.lower() == "lerx2025":
            menu_secret()
        elif choix == "0":
            typer_reponse("\033[92mAu revoir !\033[0m")
            break
        else:
            typer_reponse("\033[91mOption invalide, r\u00e9essaie.\033[0m")
        input_vert("\nAppuie sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
