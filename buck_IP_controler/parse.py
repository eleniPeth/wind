import csv
import time
from collections import deque


def get_last_wind_speed(path: str) -> float | None:
    """
    Opens the local CSV at `path`, keeps only the last row in memory,
    and returns its Wind Speed (m/s) value.
    """
    try:
        with open(path, newline='') as f:
            reader   = csv.DictReader(f, delimiter=',')  # or '\t' if TSV
            last_row = deque(reader, maxlen=1)
        if not last_row:
            return None
        return float(last_row[0]["Wind Speed (m/s)"])
    except (FileNotFoundError, KeyError, ValueError) as e:
        
        #File might not exist yet, missing column, or unparsable number
        print(f"[Warning] couldn’t read wind speed: {e}")
        
        return None