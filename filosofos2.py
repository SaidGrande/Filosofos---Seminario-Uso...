import threading
import time
import random
import tkinter as tk
from tkinter import ttk
from colorama import init, Fore, Style
import keyboard

init(autoreset=True)

NUM_FILOSOFOS = 5
COMIDAS_REQUERIDAS = 6
PENSANDO = 0
HAMBRIENTO = 1
COMIENDO = 2
ESTADOS_STR = ["Pensando", "Hambriento", "Comiendo"]
COLORES = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA]

class FilosofosComensales:
    def __init__(self):
        self.estados = [PENSANDO] * NUM_FILOSOFOS
        self.tenedores = [threading.Lock() for _ in range(NUM_FILOSOFOS)]
        self.mutex = threading.Lock()
        self.condiciones = [threading.Condition(self.mutex) for _ in range(NUM_FILOSOFOS)]
        self.comidas_completadas = [0] * NUM_FILOSOFOS
        self.filosofos_terminados = 0
        self.ejecutando = True
        self.pausa = False

        self.crear_interfaz()

    def crear_interfaz(self):
        self.root = tk.Tk()
        self.root.title("Filósofos Comensales")
        self.root.geometry("720x500")
        self.root.configure(bg="#f5f5f5")

        self.estilo = ttk.Style()
        self.estilo.configure("TLabel", font=("Segoe UI", 10))
        self.estilo.configure("TButton", font=("Segoe UI", 10))

        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, pady=10, padx=20)

        self.btn_iniciar = ttk.Button(top_frame, text="Iniciar", command=self.iniciar_simulacion)
        self.btn_iniciar.pack(side=tk.LEFT, padx=5)

        self.btn_pausar = ttk.Button(top_frame, text="Pausar / Reanudar", command=self.pausar_reanudar)
        self.btn_pausar.pack(side=tk.LEFT, padx=5)
        self.btn_pausar.config(state=tk.DISABLED)

        self.btn_salir = ttk.Button(top_frame, text="Salir", command=self.salir)
        self.btn_salir.pack(side=tk.RIGHT, padx=5)

        self.info_frame = ttk.Frame(self.root)
        self.info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        self.etiquetas_estado = []
        self.barras_progreso = []
        self.etiquetas_comidas = []

        for i in range(NUM_FILOSOFOS):
            fila = ttk.Frame(self.info_frame)
            fila.pack(fill=tk.X, pady=5)

            ttk.Label(fila, text=f"Filósofo {i+1}", width=12).pack(side=tk.LEFT)

            estado = ttk.Label(fila, text="Pensando", width=14)
            estado.pack(side=tk.LEFT, padx=5)
            self.etiquetas_estado.append(estado)

            barra = ttk.Progressbar(fila, length=200, maximum=COMIDAS_REQUERIDAS)
            barra.pack(side=tk.LEFT, padx=5)
            self.barras_progreso.append(barra)

            comidas = ttk.Label(fila, text="0/6 comidas")
            comidas.pack(side=tk.LEFT, padx=5)
            self.etiquetas_comidas.append(comidas)

        ttk.Label(self.root, text="Registro de Actividades:", font=("Segoe UI", 10, "bold"), background="#f5f5f5")\
            .pack(anchor=tk.W, padx=20, pady=(10, 0))

        frame_texto = ttk.Frame(self.root)
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        self.texto_registro = tk.Text(frame_texto, height=10, wrap=tk.WORD, bg="white", font=("Consolas", 9))
        self.texto_registro.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame_texto, command=self.texto_registro.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.texto_registro.config(yscrollcommand=scrollbar.set)

        self.root.protocol("WM_DELETE_WINDOW", self.salir)
        keyboard.add_hotkey('space', self.pausar_reanudar)
        keyboard.add_hotkey('escape', self.salir)

    def actualizar_interfaz(self):
        for i in range(NUM_FILOSOFOS):
            estado_str = ESTADOS_STR[self.estados[i]]
            self.etiquetas_estado[i].config(text=estado_str)
            self.barras_progreso[i]["value"] = self.comidas_completadas[i]
            self.etiquetas_comidas[i].config(text=f"{self.comidas_completadas[i]}/{COMIDAS_REQUERIDAS} comidas")

            color = "blue" if estado_str == "Pensando" else "red" if estado_str == "Hambriento" else "green"
            self.etiquetas_estado[i].config(foreground=color)

        self.root.update()

    def registrar_actividad(self, mensaje):
        tiempo = time.strftime("%H:%M:%S")
        limpio = mensaje.replace(Style.RESET_ALL, "").replace("\x1b[0m", "")
        self.texto_registro.insert(tk.END, f"[{tiempo}] {limpio}\n")
        self.texto_registro.see(tk.END)
        print(f"[{tiempo}] {mensaje}")

    def comprobar_filosofo(self, i):
        if self.estados[i] == HAMBRIENTO and \
           self.estados[(i-1) % NUM_FILOSOFOS] != COMIENDO and \
           self.estados[(i+1) % NUM_FILOSOFOS] != COMIENDO:
            self.estados[i] = COMIENDO
            self.condiciones[i].notify()

    def tomar_tenedores(self, i):
        with self.mutex:
            self.estados[i] = HAMBRIENTO
            self.registrar_actividad(f"{COLORES[i]}Filósofo {i+1} está hambriento{Style.RESET_ALL}")
            self.actualizar_interfaz()
            self.comprobar_filosofo(i)
            if self.estados[i] != COMIENDO:
                self.condiciones[i].wait()
        self.registrar_actividad(f"{COLORES[i]}Filósofo {i+1} está comiendo{Style.RESET_ALL}")
        self.actualizar_interfaz()

    def dejar_tenedores(self, i):
        with self.mutex:
            self.estados[i] = PENSANDO
            self.comidas_completadas[i] += 1
            self.actualizar_interfaz()
            self.registrar_actividad(f"{COLORES[i]}Filósofo {i+1} terminó de comer ({self.comidas_completadas[i]}/{COMIDAS_REQUERIDAS}){Style.RESET_ALL}")
            self.comprobar_filosofo((i-1) % NUM_FILOSOFOS)
            self.comprobar_filosofo((i+1) % NUM_FILOSOFOS)
            if self.comidas_completadas[i] >= COMIDAS_REQUERIDAS:
                self.filosofos_terminados += 1
                self.registrar_actividad(f"{COLORES[i]}Filósofo {i+1} ha terminado todas sus comidas{Style.RESET_ALL}")
                if self.filosofos_terminados >= NUM_FILOSOFOS:
                    self.registrar_actividad("Todos los filósofos han terminado. Simulación finalizada.")
                    self.ejecutando = False

    def filosofo(self, i):
        while self.ejecutando and self.comidas_completadas[i] < COMIDAS_REQUERIDAS:
            while self.pausa and self.ejecutando:
                time.sleep(0.1)
            if not self.ejecutando: break

            t_pensar = random.uniform(1, 2)
            self.registrar_actividad(f"{COLORES[i]}Filósofo {i+1} está pensando {t_pensar:.1f}s{Style.RESET_ALL}")
            self.actualizar_interfaz()
            time.sleep(t_pensar)
            if not self.ejecutando: break

            self.tomar_tenedores(i)
            if not self.ejecutando: break

            t_comer = random.uniform(1, 2)
            time.sleep(t_comer)
            self.dejar_tenedores(i)

    def iniciar_simulacion(self):
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_pausar.config(state=tk.NORMAL)
        self.estados = [PENSANDO] * NUM_FILOSOFOS
        self.comidas_completadas = [0] * NUM_FILOSOFOS
        self.filosofos_terminados = 0
        self.ejecutando = True
        self.pausa = False
        self.texto_registro.delete(1.0, tk.END)
        self.registrar_actividad("Iniciando simulación...")
        for i in range(NUM_FILOSOFOS):
            hilo = threading.Thread(target=self.filosofo, args=(i,), daemon=True)
            hilo.start()

    def pausar_reanudar(self):
        self.pausa = not self.pausa
        if self.pausa:
            self.registrar_actividad("Simulación pausada. Presiona espacio para continuar.")
        else:
            self.registrar_actividad("Simulación reanudada.")

    def salir(self):
        self.ejecutando = False
        time.sleep(0.5)
        self.root.destroy()

    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    print(Fore.CYAN + "\nProblema de los Filósofos Comensales - Python GUI Minimalista\n" + Style.RESET_ALL)
    print("Controles:\n- Espacio: Pausar/Reanudar\n- ESC: Salir")
    app = FilosofosComensales()
    app.ejecutar()