import pandas as pd


def compute_omc(open_col, mid_col, close_col):
    """
    open_col  -> list of 3 vertical digits (e.g. [7, 9, 9])
    mid_col   -> list with 1 value (e.g. [51])
    close_col -> list of 3 vertical digits (e.g. [1, 5, 5])
    """

    def build_number(col, expected_len):
        digits = []

        for x in col:
            if pd.isna(x):
                return None
            try:
                digits.append(str(int(x)))
            except (ValueError, TypeError):
                return None

        if len(digits) != expected_len:
            return None

        return int("".join(digits))

    # OPEN → exactly 3 vertical digits
    open_value = build_number(open_col, 3)

    # MID → single value (2 digits already in Excel)
    mid_value = None
    for x in mid_col:
        if pd.notna(x):
            try:
                mid_value = int(x)
                break
            except (ValueError, TypeError):
                return None

    # CLOSE → exactly 3 vertical digits
    close_value = build_number(close_col, 3)

    if open_value is None or mid_value is None or close_value is None:
        return None

    return {
        'open_value': open_value,
        'mid_value': mid_value,
        'close_value': close_value,
    }
