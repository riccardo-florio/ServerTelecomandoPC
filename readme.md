# ServerTelecomando

## Come creare l'eseguibile (EXE) con pyinstaller

Per creare l'eseguibile

``` shell
pyinstaller --onefile --windowed --name ServerTelecomando --icon=assets/icon.ico --add-data "assets;assets" --hidden-import pycaw --hidden-import comtypes.server.localserver --hidden-import customtkinter --hidden-import win32com --hidden-import win32com.client --hidden-import win32com.servers server_gui.py
```

L'eseguibile sarà dentro la cartella dist.

Puoi anche eliminare la cartella 'build' e 'pycache' e il file 'ServerTelecomando.spec'
