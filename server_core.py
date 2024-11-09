# server_core.py

import socket
import threading
import comtypes
from commands import (
    volume_up, volume_down, move_left, move_right,
    move_up, move_down, play_pause, power_off
)
from constants import HOST, PORT, DISCOVERY_PORT
from queue import Queue

class ServerCore:
    def __init__(self, log_queue):
        self.log_queue = log_queue
        self.server_running = False
        self.stop_event = threading.Event()

    def start(self):
        self.server_running = True
        self.stop_event.clear()
        self.command_thread = threading.Thread(target=self.handle_commands, daemon=True)
        self.discovery_thread = threading.Thread(target=self.handle_discovery, daemon=True)
        self.command_thread.start()
        self.discovery_thread.start()

    def stop(self):
        self.server_running = False
        self.stop_event.set()

    def handle_commands(self):
        comtypes.CoInitialize()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind((HOST, PORT))
                s.settimeout(1.0)
                self.log('Server UDP in esecuzione sulla porta {}'.format(PORT))
                while not self.stop_event.is_set():
                    try:
                        data, addr = s.recvfrom(1024)
                        comando = data.decode('utf-8').strip()
                        self.log('Comando ricevuto da {}: {}'.format(addr, comando))
                        risposta = self.execute_command(comando)
                        s.sendto(risposta.encode('utf-8'), addr)
                    except socket.timeout:
                        continue
                    except Exception as e:
                        self.log('Errore nel gestire il comando: {}'.format(e))
        finally:
            comtypes.CoUninitialize()
            self.log('Server dei comandi terminato.')

    def handle_discovery(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('', DISCOVERY_PORT))
            s.settimeout(1.0)
            self.log('Server in ascolto per le richieste di scoperta sulla porta {}'.format(DISCOVERY_PORT))
            while not self.stop_event.is_set():
                try:
                    data, addr = s.recvfrom(1024)
                    messaggio = data.decode('utf-8').strip()
                    if messaggio == 'DISCOVERY_REQUEST':
                        self.log('Richiesta di scoperta ricevuta da {}'.format(addr))
                        s.sendto('DISCOVERY_RESPONSE'.encode('utf-8'), addr)
                except socket.timeout:
                    continue
                except Exception as e:
                    self.log('Errore nel gestire la scoperta: {}'.format(e))
            self.log('Server di scoperta terminato.')

    def execute_command(self, command):
        commands = {
            'spegni': power_off,
            'volume_su': volume_up,
            'volume_giu': volume_down,
            'sinistra': move_left,
            'destra': move_right,
            'su': move_up,
            'giu': move_down,
            'play_pause': play_pause,
        }

        action = commands.get(command)
        if action:
            try:
                result = action()
                return result if result else 'Comando eseguito.'
            except Exception as e:
                return 'Errore nell\'esecuzione del comando: {}'.format(e)
        else:
            return 'Comando non riconosciuto.'

    def log(self, message):
        self.log_queue.put(message)
