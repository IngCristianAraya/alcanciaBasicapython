import tkinter as tk
from tkinter import messagebox, ttk
import os
from hashlib import sha256

class AlcanciaDigital:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        self.estilo_global()

        self.login_window = tk.Toplevel()
        self.login_window.title("Inicio de Sesión")
        self.login_window.geometry("320x220")
        self.login_window.configure(bg="#f2f2f2")
        self.login_window.resizable(False, False)

        self.crear_archivo_usuarios()
        self.crear_login()

    def estilo_global(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TEntry", padding=4)
        style.configure("TLabel", font=("Segoe UI", 10))
        style.map("TButton", background=[("active", "#a0d8ef")])

    def crear_archivo_usuarios(self):
        if not os.path.exists("usuarios.txt"):
            with open("usuarios.txt", "w") as f:
                f.write("admin:" + sha256("admin123".encode()).hexdigest() + "\n")

    def crear_login(self):
        frame = ttk.Frame(self.login_window, padding=20)
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text="Usuario:").grid(row=0, column=0, pady=10, sticky="e")
        self.usuario_entry = ttk.Entry(frame, width=25)
        self.usuario_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Contraseña:").grid(row=1, column=0, pady=10, sticky="e")
        self.password_entry = ttk.Entry(frame, show="*", width=25)
        self.password_entry.grid(row=1, column=1)

        ttk.Button(frame, text="Ingresar", command=self.verificar_login).grid(row=2, column=0, columnspan=2, pady=20)

    def verificar_login(self):
        usuario = self.usuario_entry.get()
        password = sha256(self.password_entry.get().encode()).hexdigest()

        try:
            with open("usuarios.txt", "r") as f:
                for line in f:
                    user, pwd = line.strip().split(":")
                    if user == usuario and pwd == password:
                        self.login_window.destroy()
                        self.inicializar_aplicacion()
                        return
            messagebox.showerror("Error", "Credenciales incorrectas")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def inicializar_aplicacion(self):
        self.root.deiconify()
        self.root.title("Alcancía Digital")
        self.root.geometry("700x600")
        self.root.configure(bg="#f7f9fc")

        self.total = tk.DoubleVar()
        self.cargar_saldo()
        self.crear_interfaz()

    def crear_boton_canvas(self, parent, texto, forma, color, width, height, valor):
        canvas = tk.Canvas(parent, width=width, height=height, bg="#f7f7f7",
                           bd=0, highlightthickness=0, cursor="hand2")
        
        if forma == "moneda":
            canvas.create_oval(2, 2, width - 2, height - 2, fill=color, outline="#444")
        else:
            canvas.create_rectangle(2, 2, width - 2, height - 2, fill=color, outline="#444")

        canvas.create_text(width / 2, height / 2, text=texto, font=("Segoe UI", 10, "bold"))

        def on_enter(event): canvas.configure(bg="#e8f0fe")
        def on_leave(event): canvas.configure(bg="#f7f7f7")

        canvas.bind("<Button-1>", lambda e: self.agregar_monto(valor))
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)

        return canvas

    def crear_interfaz(self):
        main_frame = tk.Frame(self.root, bg="#f7f9fc", padx=30, pady=30)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Título
        tk.Label(main_frame, text="Total Ahorrado (S/.)", font=("Segoe UI", 16, "bold"), bg="#f7f9fc").pack(pady=10)

        total_display = tk.Label(main_frame, textvariable=self.total, font=("Segoe UI", 32, "bold"),
                                 bg="#ffffff", fg="#333333", relief=tk.RIDGE, width=15, pady=10)
        total_display.pack(pady=20)

        # Área de botones
        button_frame = tk.Frame(main_frame, bg="#f7f9fc")
        button_frame.pack(pady=20)

        denominaciones = [ # Valores 
            {"texto": "10¢", "valor": 0.10, "tipo": "moneda", "color": "#FFD700"},
            {"texto": "50¢", "valor": 0.50, "tipo": "moneda", "color": "#CD7F32"},
            {"texto": "1 Sol", "valor": 1.00, "tipo": "moneda", "color": "#C0C0C0"},
            {"texto": "2 Soles", "valor": 2.00, "tipo": "moneda", "color": "#B87333"},
            {"texto": "5 Soles", "valor": 5.00, "tipo": "moneda", "color": "#E5E4E2"},
            {"texto": "10 Soles", "valor": 10.00, "tipo": "billete", "color": "#98FB98"},
            {"texto": "20 Soles", "valor": 20.00, "tipo": "billete", "color": "#87CEEB"},
            {"texto": "50 Soles", "valor": 50.00, "tipo": "billete", "color": "#D8BFD8"},
            {"texto": "100 Soles", "valor": 100.00, "tipo": "billete", "color": "#FFB6C1"},
        ]

        row, col = 0, 0
        for d in denominaciones:
            btn = self.crear_boton_canvas(button_frame, d["texto"], d["tipo"], d["color"],
                                          80 if d["tipo"] == "moneda" else 120,
                                          80 if d["tipo"] == "moneda" else 60,
                                          d["valor"])
            btn.grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col > 2:
                col = 0
                row += 1

        # Botón de reinicio
        tk.Button(main_frame, text="Reiniciar Ahorros", font=("Segoe UI", 12),
                  bg="#dc3545", fg="white", padx=10, pady=5,
                  command=self.reiniciar_ahorros).pack(pady=30)

    def agregar_monto(self, valor):
        self.total.set(round(self.total.get() + valor, 2))
        self.guardar_saldo()

    def reiniciar_ahorros(self):
        if messagebox.askyesno("Confirmar", "¿Seguro que deseas reiniciar tu ahorro?"):
            self.total.set(0.00)
            self.guardar_saldo()

    def guardar_saldo(self):
        with open("saldo.txt", "w") as f:
            f.write(str(self.total.get()))

    def cargar_saldo(self):
        if os.path.exists("saldo.txt"):
            try:
                with open("saldo.txt", "r") as f:
                    self.total.set(float(f.read()))
            except:
                self.total.set(0.00)
        else:
            self.total.set(0.00)


if __name__ == "__main__":
    root = tk.Tk()
    app = AlcanciaDigital(root)
    root.mainloop()
