# src/gui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from src.core.combination_reducer import CombinationReducer
from src.utils.config import CONFIG
import json
from datetime import datetime
import random


class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Reductor de Combinaciones de Lotería")
        self.root.geometry("800x600")

        self.reducer = CombinationReducer()
        self.setup_ui()
        self.last_results = None

    def generate_combinations(self):
        try:
            # Obtener y validar números
            numbers_text = self.numbers_entry.get().strip()
            if not numbers_text:
                raise ValueError("Por favor, ingrese números primero")

            numbers = [int(x) for x in numbers_text.split()]
            if len(numbers) < CONFIG['MIN_INPUT_NUMBERS']:
                raise ValueError(f"Debe ingresar al menos {CONFIG['MIN_INPUT_NUMBERS']} números")

            # Validar rango y unicidad
            if len(set(numbers)) != len(numbers):
                raise ValueError("No puede haber números repetidos")
            if any(n < 1 or n > CONFIG['MAX_NUMBERS'] for n in numbers):
                raise ValueError(f"Los números deben estar entre 1 y {CONFIG['MAX_NUMBERS']}")

            # Generar combinaciones
            self.reducer.set_numbers(numbers)
            combinations = self.reducer.generate_combinations()

            # Advertir si hay muchas combinaciones
            if len(combinations) > 1000:
                if not messagebox.askyesno("Advertencia",
                                           f"Se generarán {len(combinations)} combinaciones. ¿Desea continuar?"):
                    return

            # Mostrar resultados
            self.results_text.delete(1.0, tk.END)
            for i, combo in enumerate(combinations, 1):
                formatted_combo = ", ".join(map(str, combo))
                self.results_text.insert(tk.END, f"Combinación {i}: ({formatted_combo})\n")

            # Actualizar estadísticas
            expected = self.reducer.calculate_expected_combinations(len(numbers), CONFIG['COMBINATION_SIZE'])
            self.stats_label.config(text=(
                f"Total de combinaciones generadas: {len(combinations)}\n"
                f"Combinaciones esperadas: {expected}\n"
                f"Números utilizados: {', '.join(map(str, sorted(numbers)))}"
            ))

            self.last_results = combinations
            self.status_var.set(f"Se han generado {len(combinations)} combinaciones")

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error al generar combinaciones")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            self.status_var.set("Error al generar combinaciones")

    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        title_label = ttk.Label(main_frame,
                                text="Reductor de Combinaciones de Lotería",
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Panel de entrada
        input_frame = ttk.LabelFrame(main_frame, text="Entrada de Números", padding=10)
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(input_frame, text="Números (separados por espacios):").grid(row=0, column=0, sticky=tk.W)
        self.numbers_entry = ttk.Entry(input_frame, width=50)
        self.numbers_entry.grid(row=0, column=1, padx=5)

        # Botones en el panel de entrada
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=2, sticky=tk.E)

        ttk.Button(button_frame,
                   text="Números Aleatorios",
                   command=self.generate_random_numbers).grid(row=0, column=0, padx=2)

        ttk.Button(button_frame,
                   text="Generar Combinaciones",
                   command=self.generate_combinations).grid(row=0, column=1, padx=2)

        # Opciones de garantía
        options_frame = ttk.LabelFrame(main_frame, text="Garantía de Aciertos", padding=10)
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        self.min_hits = tk.StringVar(value="3")
        for i, val in enumerate(['3', '4', '5']):
            ttk.Radiobutton(options_frame,
                            text=f"{val} aciertos",
                            variable=self.min_hits,
                            value=val).grid(row=0, column=i, padx=10)

        # Botón de reducción
        ttk.Button(main_frame,
                   text="Reducir Combinaciones",
                   command=self.reduce_combinations).grid(row=3, column=0, columnspan=3, pady=10)

        # Panel de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding=10)
        results_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.stats_label = ttk.Label(results_frame, text="")
        self.stats_label.grid(row=0, column=0, columnspan=3, sticky=tk.W)

        # Área de resultados con scroll
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=60)
        self.results_text.grid(row=1, column=0, columnspan=3, pady=5)

        # Botones de acción
        button_frame = ttk.Frame(results_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=5)

        ttk.Button(button_frame, text="Guardar", command=self.save_results).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Copiar", command=self.copy_to_clipboard).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_results).grid(row=0, column=2, padx=5)

        # Barra de estado
        self.status_var = tk.StringVar(value="Listo")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

    def generate_random_numbers(self):
        """Genera 10 números aleatorios únicos entre 1 y 49"""
        numbers = random.sample(range(1, CONFIG['MAX_NUMBERS'] + 1), CONFIG['MIN_INPUT_NUMBERS'])
        self.numbers_entry.delete(0, tk.END)
        self.numbers_entry.insert(0, " ".join(map(str, sorted(numbers))))

    def reduce_combinations(self):
        try:
            numbers = [int(x) for x in self.numbers_entry.get().strip().split()]

            if len(numbers) < CONFIG['MIN_INPUT_NUMBERS']:
                raise ValueError(f"Debe ingresar al menos {CONFIG['MIN_INPUT_NUMBERS']} números")

            min_hits = int(self.min_hits.get())
            self.reducer.set_numbers(numbers)
            reduced = self.reducer.reduce_combinations(min_hits)
            self.last_results = reduced

            # Limpiar y mostrar resultados
            self.results_text.delete(1.0, tk.END)
            for i, combo in enumerate(reduced, 1):
                self.results_text.insert(tk.END, f"Combinación {i}: {combo}\n")

            # Actualizar estadísticas
            total_original = len(self.reducer.generate_combinations())
            self.stats_label.config(text=(
                f"Combinaciones originales: {total_original}\n"
                f"Combinaciones reducidas: {len(reduced)}\n"
                f"Factor de reducción: {total_original / len(reduced):.2f}x"
            ))

            self.status_var.set("Reducción completada con éxito")

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error en el proceso")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            self.status_var.set("Error en el proceso")

    def save_results(self):
        if not self.last_results:
            messagebox.showinfo("Info", "No hay resultados para guardar")
            return

        try:
            filename = f"combinaciones_reducidas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            data = {
                "fecha": datetime.now().isoformat(),
                "numeros_originales": self.numbers_entry.get().strip().split(),
                "garantia_minima": self.min_hits.get(),
                "combinaciones": [list(combo) for combo in self.last_results]
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self.status_var.set(f"Resultados guardados en {filename}")
            messagebox.showinfo("Éxito", f"Resultados guardados en {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    def copy_to_clipboard(self):
        if not self.results_text.get(1.0, tk.END).strip():
            messagebox.showinfo("Info", "No hay resultados para copiar")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(self.results_text.get(1.0, tk.END))
        self.status_var.set("Resultados copiados al portapapeles")

    def clear_results(self):
        self.results_text.delete(1.0, tk.END)
        self.stats_label.config(text="")
        self.last_results = None
        self.status_var.set("Resultados limpiados")

    def run(self):
        self.root.mainloop()