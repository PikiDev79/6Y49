from typing import List, Tuple
import itertools
import random
from src.utils.config import CONFIG


class CombinationReducer:
    def __init__(self):
        self.original_numbers = []
        self.reduced_combinations = []

    def set_numbers(self, numbers: List[int]):
        """Establece la lista de números iniciales"""
        self.original_numbers = sorted(list(set(numbers)))  # Asegura números únicos y ordenados

    def calculate_expected_combinations(self, n: int, r: int) -> int:
        """Calcula el número esperado de combinaciones"""

        def factorial(num):
            result = 1
            for i in range(1, num + 1):
                result *= i
            return result

        return factorial(n) // (factorial(r) * factorial(n - r))

    def generate_combinations(self, combination_size: int = CONFIG['COMBINATION_SIZE']) -> List[Tuple[int, ...]]:
        """Genera todas las combinaciones posibles"""
        if not self.original_numbers:
            raise ValueError("No hay números para generar combinaciones")

        n = len(self.original_numbers)
        if n < CONFIG['MIN_INPUT_NUMBERS']:
            raise ValueError(f"Se necesitan al menos {CONFIG['MIN_INPUT_NUMBERS']} números. Actualmente hay {n}")

        # Calcular número esperado de combinaciones
        expected = self.calculate_expected_combinations(n, combination_size)
        print(f"Generando combinaciones para {n} números tomados de {combination_size} en {combination_size}")
        print(f"Se esperan {expected} combinaciones")

        # Generar combinaciones
        all_combinations = list(itertools.combinations(self.original_numbers, combination_size))

        # Verificar
        if len(all_combinations) != expected:
            raise ValueError(
                f"Error en la generación: se esperaban {expected} combinaciones, se generaron {len(all_combinations)}")

        return all_combinations

    def calculate_hits(self, combo1: Tuple[int, ...], combo2: Tuple[int, ...]) -> int:
        """Calcula el número de aciertos entre dos combinaciones"""
        return len(set(combo1).intersection(set(combo2)))

    def reduce_combinations(self, min_hits: int) -> List[Tuple[int, ...]]:
        """Reduce las combinaciones garantizando un mínimo de aciertos"""
        all_combinations = self.generate_combinations()
        if not all_combinations:
            return []

        # Si hay menos combinaciones que el máximo permitido, devolver todas
        if len(all_combinations) <= CONFIG['MAX_REDUCED_COMBINATIONS']:
            return all_combinations

        reduced = []
        first_combo = random.choice(all_combinations)
        reduced.append(first_combo)
        remaining = set(all_combinations) - {first_combo}

        while remaining and len(reduced) < CONFIG['MAX_REDUCED_COMBINATIONS']:
            best_combo = None
            best_score = -1

            # Tomar una muestra de las combinaciones restantes
            sample = random.sample(list(remaining), min(100, len(remaining)))

            for combo in sample:
                valid = True
                score = 0

                for selected in reduced:
                    hits = self.calculate_hits(combo, selected)
                    if hits < min_hits:
                        valid = False
                        break
                    score += hits

                if valid and score > best_score:
                    best_score = score
                    best_combo = combo

            if best_combo is None:
                break

            reduced.append(best_combo)
            remaining.remove(best_combo)

        return reduced

    def validate_reduction(self, reduced_combinations: List[Tuple[int, ...]], min_hits: int) -> bool:
        """Valida que todas las combinaciones cumplan con el mínimo de aciertos"""
        for i, combo1 in enumerate(reduced_combinations):
            for combo2 in reduced_combinations[i + 1:]:
                if self.calculate_hits(combo1, combo2) < min_hits:
                    return False
        return True