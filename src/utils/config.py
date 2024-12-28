#src/utils/config.py
CONFIG = {
    'MAX_NUMBERS': 49,        # Número máximo permitido en lotería
    'COMBINATION_SIZE': 6,    # Tamaño de cada combinación
    'MIN_INPUT_NUMBERS': 8,  # Mínimo de números de entrada
    'MIN_HITS_ALLOWED': [3, 4, 5],  # Valores permitidos para garantía mínima
    'MAX_REDUCED_COMBINATIONS': 3000,  # Máximo de combinaciones reducidas
    'MIN_REDUCED_COMBINATIONS': 5,     # Mínimo de combinaciones reducidas
    'UI_THEME': {
        'PRIMARY_COLOR': '#2196F3',  # Azul material design
        'SECONDARY_COLOR': '#FFC107', # Amarillo material design
        'BACKGROUND_COLOR': '#F5F5F5',
        'FONT_FAMILY': 'Arial',
        'PADDING': 10
    }
}
