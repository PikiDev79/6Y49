# src/core/validator.py
from typing import List
from src.utils.config import CONFIG


class InputValidator:
    @staticmethod
    def validate_numbers(numbers: List[int]) -> bool:
        """Valida la lista de números de entrada"""
        if len(numbers) < CONFIG['MIN_INPUT_NUMBERS']:
            return False

        if not all(1 <= n <= CONFIG['MAX_NUMBERS'] for n in numbers):
            return False

        if len(set(numbers)) != len(numbers):
            return False

        return True

    @staticmethod
    def validate_min_hits(min_hits: int) -> bool:
        """Valida que el número mínimo de aciertos sea válido"""
        return 3 <= min_hits <= 5