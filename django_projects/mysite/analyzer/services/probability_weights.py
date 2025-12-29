import pandas as pd
from typing import Dict, List
from collections import Counter

BASE_PROBABILITY = 1.0  # 1% default baseline

# Cached weights to avoid recalculating every request
DIGIT_WEIGHTS: Dict[int, float] = {}
WEIGHTS_READY = False


def load_excel_data(path: str, column_name: str = "result"):
    """
    Load Excel containing historical results.
    Expected column: 2-digit values like 00–99
    """
    df = pd.read_excel(path)

    # clean & normalize
    numbers = (
        df[column_name]
        .dropna()
        .astype(int)
        .tolist()
    )

    return numbers


def calculate_digit_weights(numbers: List[int]) -> Dict[int, float]:
    """
    Convert historical results → digit frequency weights
    """

    digits = []

    for n in numbers:
        n = int(n)
        tens = n // 10
        units = n % 10
        digits.append(tens)
        digits.append(units)

    counts = Counter(digits)

    max_freq = max(counts.values())
    min_freq = min(counts.values())

    # normalize weights into approx 0.85–1.30 range
    weights = {}

    for d in range(10):
        freq = counts.get(d, 0)

        normalized = 0.85 + (freq - min_freq) / (max_freq - min_freq) * (1.30 - 0.85)

        weights[d] = round(normalized, 3)

    return weights


def init_weights(excel_path: str, column_name: str = "result"):
    """
    Call this once (e.g., app startup or after upload)
    """
    global DIGIT_WEIGHTS, WEIGHTS_READY

    numbers = load_excel_data(excel_path, column_name)
    DIGIT_WEIGHTS = calculate_digit_weights(numbers)
    WEIGHTS_READY = True


def calculate_probability(number: int) -> Dict:
    if not WEIGHTS_READY:
        raise RuntimeError("Digit weights not initialized")

    if not 0 <= number <= 99:
        raise ValueError("Number must be between 00 and 99")

    tens = number // 10
    units = number % 10

    avg_weight = round((DIGIT_WEIGHTS[tens] + DIGIT_WEIGHTS[units]) / 2, 3)
    probability = round(BASE_PROBABILITY * avg_weight, 3)

    return {
        "number": f"{number:02d}",
        "tens": tens,
        "units": units,
        "avg_weight": avg_weight,
        "probability": probability,
    }


def generate_probability_table() -> List[Dict]:
    return [calculate_probability(i) for i in range(100)]


def highest_weighted_numbers(limit=5):
    return sorted(generate_probability_table(),
                  key=lambda x: x["probability"],
                  reverse=True)[:limit]


def lowest_weighted_numbers(limit=5):
    return sorted(generate_probability_table(),
                  key=lambda x: x["probability"])[:limit]
