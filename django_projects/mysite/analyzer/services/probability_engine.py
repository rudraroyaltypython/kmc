from .probability_weights import DIGIT_WEIGHTS, BASE_PROBABILITY


def calculate_probability(number: int):
    """
    number: 00–99
    """
    tens = number // 10
    units = number % 10

    tens_weight = DIGIT_WEIGHTS[tens]
    units_weight = DIGIT_WEIGHTS[units]

    avg_weight = round((tens_weight + units_weight) / 2, 3)
    probability = round(BASE_PROBABILITY * avg_weight, 3)

    return {
        "number": f"{number:02d}",
        "tens": tens,
        "units": units,
        "avg_weight": avg_weight,
        "probability": probability
    }


def generate_probability_table():
    table = []
    for n in range(100):
        table.append(calculate_probability(n))

    # Sort by probability DESC (like your example)
    table.sort(key=lambda x: x["probability"], reverse=True)
    return table
