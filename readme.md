# ServerTelecomando

Applicazione server per Windows che consente di controllare il PC da remoto tramite un'app mobile Flutter (sviluppata separatamente). Questo progetto trasforma il tuo dispositivo mobile in un telecomando avanzato per il tuo computer.

## Funzionalità

- **Controllo del Volume**: Aumenta o diminuisci il volume del sistema.
- **Navigazione**: Simula i tasti direzionali (sinistra, destra, su, giù).
- **Riproduzione Multimediale**: Metti in play o in pausa i contenuti multimediali.
- **Spegnimento Programmato**: Pianifica lo spegnimento del PC con un comando remoto.
- **Avvio Automatico**: Il server può essere configurato per avviarsi automaticamente all'accensione del PC.
- **Icona nella System Tray**: Accesso rapido alle funzionalità tramite un menu contestuale nell'icona di sistema.

## Prerequisiti

- **Sistema Operativo**: Windows
- **Python 3.x** installato

## Come Clonare il Progetto

Per clonare il repository, esegui il seguente comando nel terminale:

```shell
git clone https://github.com/riccardo-florio/server_telecomando.git
```

## Installazione

### Creare e Attivare l'Ambiente Virtuale

1. **Creare l'Ambiente Virtuale**

   Nella directory del progetto, esegui:

   ```shell
   python -m venv venv
   ```

2. **Attivare l'Ambiente Virtuale**

   Su **Windows**:

   ```shell
   venv\Scripts\Activate.ps1
   ```

   Su **Linux/MacOS**:

   ```shell
   source venv/bin/activate
   ```

### Installare le Dipendenze

Con l'ambiente virtuale attivato, installa le dipendenze richieste:

```shell
pip install -r requirements.txt
```

## Esecuzione dell'Applicazione

Per avviare l'applicazione server, esegui:

```shell
python server_gui.py
```

## Come Creare l'Eseguibile (EXE) con PyInstaller

Per creare l'eseguibile, utilizza il seguente comando:

```shell
pyinstaller --onefile --windowed --name ServerTelecomando --icon=assets/icon.ico --add-data "assets;assets" --hidden-import pycaw --hidden-import comtypes.server.localserver --hidden-import customtkinter --hidden-import win32com --hidden-import win32com.client --hidden-import win32com.servers server_gui.py
```

L'eseguibile verrà generato nella cartella `dist`.

Puoi eliminare le seguenti cartelle e file generati durante la compilazione:

- La cartella `build`
- La cartella `__pycache__`
- Il file `ServerTelecomando.spec`

## Note Aggiuntive

- **Firewall**: Assicurati che il firewall di Windows permetta al server di ricevere connessioni sulla porta specificata.
- **App Mobile Flutter**: Questo server è progettato per funzionare con un'app mobile Flutter (sviluppata separatamente). Assicurati di avere l'app installata sul tuo dispositivo mobile per poter inviare comandi al server.
- **Permessi di Amministratore**: Alcune funzionalità potrebbero richiedere permessi di amministratore per funzionare correttamente.

## Contribuire

Se desideri contribuire al progetto, sentiti libero di fare fork del repository e aprire delle pull request.

## Licenza

Questo progetto è distribuito sotto la licenza MIT. Vedi il file [LICENSE](LICENSE) per maggiori dettagli.
