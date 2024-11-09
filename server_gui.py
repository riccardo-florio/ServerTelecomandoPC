# server_gui.py

import customtkinter as ctk
from tkinter import messagebox
from server_core import ServerCore
from startup_manager import is_in_startup, add_to_startup, remove_from_startup
from constants import APP_NAME
from queue import Queue, Empty
import threading
import sys
import os
import ctypes
from PIL import Image
import pystray

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.iconbitmap(self.resource_path(os.path.join('assets', 'icon.ico')))
        self.root.configure(fg_color="white")  # Imposta lo sfondo bianco

        # Ingrandisci la finestra e imposta una dimensione minima
        self.root.geometry('600x400')  # Dimensione iniziale (larghezza x altezza)
        self.root.minsize(600, 400)    # Dimensione minima

        self.server_core = None
        self.log_queue = Queue()
        self.is_window_visible = True

        # Carica l'immagine dell'icona
        self.icon_image = Image.open(self.resource_path(os.path.join("assets", "icon.png")))

        self.create_widgets()
        self.update_log()
        self.setup_tray_icon()  # Crea l'icona della tray
        self.check_startup_args()

        # Avvia il server all'avvio dell'applicazione
        self.start_server()

        # Avvia l'icona della tray una volta che tutto è stato configurato
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def create_widgets(self):
        # Etichetta di stato
        self.status_label = ctk.CTkLabel(
            self.root,
            text="Server in esecuzione",  # Imposta lo stato iniziale
            text_color="green",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(pady=10)

        # Frame per i bottoni
        self.button_frame = ctk.CTkFrame(self.root, fg_color="white")
        self.button_frame.pack(pady=10)

        # Pulsante Toggle per Avviare/Fermare il Server
        self.toggle_button = ctk.CTkButton(
            self.button_frame,
            text="Ferma Server",  # Il server è già avviato
            command=self.toggle_server,
            width=150,
            fg_color="#607d8b",
            text_color="white"
        )
        self.toggle_button.grid(row=0, column=0, padx=5, pady=5)

        # Bottone "Esci"
        self.exit_button = ctk.CTkButton(
            self.button_frame,
            text="Esci",
            command=self.quit_application,
            width=150,
            fg_color="#607d8b",
            text_color="white"
        )
        self.exit_button.grid(row=0, column=1, padx=5, pady=5)

        # Etichetta "Log"
        self.log_label = ctk.CTkLabel(self.root, text="Log:", fg_color="white")
        self.log_label.pack(pady=(10, 0))

        # Textbox per il log
        self.log_text = ctk.CTkTextbox(self.root, height=200)
        self.log_text.configure(state='disabled')
        self.log_text.pack(fill='both', expand=True, padx=10, pady=5)

        # Checkbox per l'avvio automatico
        self.startup_var = ctk.BooleanVar()
        self.startup_var.set(is_in_startup())
        self.startup_checkbox = ctk.CTkCheckBox(
            self.root,
            text="Esegui all'avvio di Windows",
            variable=self.startup_var,
            command=self.toggle_startup,
            fg_color="white"
        )
        self.startup_checkbox.pack(pady=5)

        # Gestione della chiusura della finestra
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def toggle_server(self, icon=None, item=None):
        if not self.server_core:
            self.start_server()
        else:
            self.stop_server()

    def start_server(self, icon=None, item=None):
        if not self.server_core:
            self.server_core = ServerCore(self.log_queue)
            self.server_core.start()
            self.status_label.configure(text="Server in esecuzione", text_color="green")
            self.toggle_button.configure(text="Ferma Server")
            self.update_tray_menu()  # Aggiorna il menu della tray
            self.log("Server avviato.")

    def stop_server(self, icon=None, item=None):
        if self.server_core:
            self.server_core.stop()
            self.server_core = None
            self.status_label.configure(text="Server fermo", text_color="red")
            self.toggle_button.configure(text="Avvia Server")
            self.update_tray_menu()  # Aggiorna il menu della tray
            self.log("Server fermato.")

    def toggle_startup(self):
        if self.startup_var.get():
            add_to_startup()
            self.log("Aggiunto all'avvio automatico.")
        else:
            remove_from_startup()
            self.log("Rimosso dall'avvio automatico.")

    def log(self, message):
        self.log_queue.put(message)

    def update_log(self):
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.configure(state='normal')
                self.log_text.insert('end', message + '\n')
                self.log_text.see('end')
                self.log_text.configure(state='disabled')
        except Empty:
            pass
        self.root.after(100, self.update_log)

    def on_closing(self):
        self.hide_window()

    def hide_window(self):
        self.root.withdraw()
        self.is_window_visible = False

    def show_window(self, icon=None, item=None):
        self.root.deiconify()
        self.root.state('normal')
        self.root.focus_force()
        self.is_window_visible = True

    def quit_application(self, icon=None, item=None):
        self.stop_server()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.destroy()
        sys.exit(0)

    def setup_tray_icon(self):
        # Crea l'icona della tray senza avviarla
        self.tray_icon = pystray.Icon(
            "server_tray",
            self.icon_image,
            APP_NAME,
            menu=self.create_tray_menu()
        )

    def update_tray_menu(self):
        # Aggiorna il menu dell'icona della tray
        self.tray_icon.menu = self.create_tray_menu()

    def create_tray_menu(self):
        # Crea il menu dell'icona della tray in base allo stato del server
        menu_items = [
            pystray.MenuItem('Mostra Finestra', self.show_window, default=True),
        ]

        if self.server_core:
            # Se il server è in esecuzione, abilita 'Ferma Server'
            menu_items.append(pystray.MenuItem('Ferma Server', self.stop_server))
        else:
            # Se il server è fermo, abilita 'Avvia Server'
            menu_items.append(pystray.MenuItem('Avvia Server', self.start_server))

        menu_items.append(pystray.MenuItem('Esci', self.quit_application))

        return pystray.Menu(*menu_items)

    def check_startup_args(self):
        if len(sys.argv) > 1 and sys.argv[1] == '--minimized':
            self.root.after(0, self.hide_window)

    def resource_path(self, relative_path):
        """Ottiene il percorso assoluto per le risorse, compatibile con PyInstaller."""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    ctk.set_appearance_mode("Light")  # Imposta l'aspetto su chiaro
    ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

    # Assicura che l'applicazione venga eseguita come singola istanza
    mutex = ctypes.windll.kernel32.CreateMutexW(None, ctypes.c_bool(False), "ServerTelecomandoMutex")
    if ctypes.GetLastError() == 183:
        messagebox.showerror("Errore", "Il server è già in esecuzione.")
        sys.exit(0)

    root = ctk.CTk()
    app = ServerGUI(root)
    root.mainloop()
