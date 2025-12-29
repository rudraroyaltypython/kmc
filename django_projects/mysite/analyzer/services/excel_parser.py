import pandas as pd
from datetime import datetime
from .logic import compute_omc


DAY_MAP = {
    'MON': (1, 2, 3),
    'TUE': (4, 5, 6),
    'WED': (7, 8, 9),
    'THU': (10, 11, 12),
    'FRI': (13, 14, 15),
    'SAT': (16, 17, 18),
}


def parse_excel(path, uploaded_file):
    df = pd.read_excel(path)
    results = []

    i = 0
    total_rows = len(df)

    while i < total_rows:
        row = df.iloc[i]

        # Detect date row
        if isinstance(row.iloc[0], datetime):
            current_date = row.iloc[0].date()

            # We expect next 3 rows to contain vertical digits
            rows_block = df.iloc[i:i + 3]

            for day, idxs in DAY_MAP.items():
                open_col = []
                mid_col = []
                close_col = []

                for r_index, r in rows_block.iterrows():
                    open_col.append(r.iloc[idxs[0]])
                    close_col.append(r.iloc[idxs[2]])

                    # Mid value only from FIRST row
                    if r_index == rows_block.index[0]:
                        mid_col.append(r.iloc[idxs[1]])

                # Skip if all empty
                if (
                    all(pd.isna(x) for x in open_col)
                    and all(pd.isna(x) for x in mid_col)
                    and all(pd.isna(x) for x in close_col)
                ):
                    continue

                result = compute_omc(open_col, mid_col, close_col)
                if not result:
                    continue

                results.append({
                    'date': current_date,
                    'day': day,
                    'open_value': int(result['open_value']),
                    'mid_value': int(result['mid_value']),
                    'close_value': int(result['close_value']),
                    'source': uploaded_file
                })

            # Move to next date block
            i += 3
        else:
            i += 1

    return results
