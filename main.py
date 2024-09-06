import tkinter as tk
import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl

# Definición del sistema difuso
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
climatization_action = ctrl.Consequent(np.arange(0, 11, 1), 'climatization_action')

temperature.automf(3)
humidity.automf(3)

climatization_action['low'] = fuzz.trimf(climatization_action.universe, [0, 0, 5])
climatization_action['medium'] = fuzz.trimf(climatization_action.universe, [0, 5, 10])
climatization_action['high'] = fuzz.trimf(climatization_action.universe, [5, 10, 10])

rule1 = ctrl.Rule(temperature['poor'] & humidity['poor'], climatization_action['high'])
rule2 = ctrl.Rule(temperature['average'] & humidity['average'], climatization_action['medium'])
rule3 = ctrl.Rule(temperature['good'] & humidity['good'], climatization_action['low'])

climatization_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
climatization_simulation = ctrl.ControlSystemSimulation(climatization_ctrl)

def evaluate_climatization():
    try:
        temp = temperature_var.get()
        hum = humidity_var.get()
        climatization_simulation.input['temperature'] = temp
        climatization_simulation.input['humidity'] = hum
        climatization_simulation.compute()

        output = climatization_simulation.output
        action_value = int(output['climatization_action'])
        
        # Determinar la recomendación
        if action_value <= 3:
            recommendation = 'Acción alta: Aumentar la climatización'
        elif action_value <= 7:
            recommendation = 'Acción media: Climatización moderada'
        else:
            recommendation = 'Acción baja: Reducir la climatización'
        
        # Actualizar las etiquetas con hechos y recomendaciones
        result_label.config(text=f'Recomendación: {recommendation}')
        
        # Mostrar hechos y reglas activadas
        facts_text = (
            f"Hechos:\n"
            f"- Temperatura: {temp}°C\n"
            f"- Humedad: {hum}%\n"
        )
        
        details_label.config(
            text=facts_text,
            wraplength=300
        )
    except ValueError:
        result_label.config(text='Error: Entrada inválida')
    except Exception as e:
        result_label.config(text=f'No hay recomendación para estas entradas')

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Sistema de Climatización")
root.configure(bg='#f0f0f0')

# Opciones para temperatura y humedad
temperature_options = [0, 10, 20, 30, 40]
humidity_options = [0, 25, 50, 75, 100]

# Variables para almacenar las selecciones
temperature_var = tk.IntVar(value=temperature_options[0])
humidity_var = tk.IntVar(value=humidity_options[0])

# Diseño del formulario
frame = tk.Frame(root, bg='#ffffff', padx=10, pady=10)
frame.pack(padx=20, pady=20)

tk.Label(frame, text="Seleccione la temperatura (°C):", bg='#ffffff', font=('Arial', 12)).pack(pady=5)
temperature_menu = tk.OptionMenu(frame, temperature_var, *temperature_options)
temperature_menu.config(width=15)
temperature_menu.pack()

tk.Label(frame, text="Seleccione la humedad (%):", bg='#ffffff', font=('Arial', 12)).pack(pady=5)
humidity_menu = tk.OptionMenu(frame, humidity_var, *humidity_options)
humidity_menu.config(width=15)
humidity_menu.pack()

tk.Button(frame, text="Evaluar", command=evaluate_climatization, bg='#4CAF50', fg='white', font=('Arial', 12)).pack(pady=10)

result_label = tk.Label(frame, text="", bg='#ffffff', font=('Arial', 12, 'bold'), wraplength=300)
result_label.pack()

details_label = tk.Label(frame, text="", bg='#ffffff', font=('Arial', 10), wraplength=300)
details_label.pack()

root.geometry("500x400")
root.mainloop()
