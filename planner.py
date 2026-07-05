from pathlib import Path
from datetime import timedelta
import pandas as pd

# -------------------------------------------------
# Data location
# -------------------------------------------------

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"


# -------------------------------------------------
# Load a train line
# -------------------------------------------------

def load_line(csv_file):
    df = pd.read_csv(csv_file)

    stations = (
        df["name"]
        .astype(str)
        .str.lower()
        .str.strip()
        .tolist()
    )

    travel_times = [
        timedelta(minutes=float(t))
        for t in df["estimated_segment_travel_min"].tolist()[1:]
    ]

    return {
        "stations": stations,
        "times": travel_times,
    }


# -------------------------------------------------
# Load all train lines
# -------------------------------------------------

train_lines = {
    "Blue": load_line(DATA_DIR / "Blue_line.csv"),
    "Red": load_line(DATA_DIR / "Red_line.csv"),
    "Yellow": load_line(DATA_DIR / "Yellow_line.csv"),
}


# -------------------------------------------------
# Find fastest route
# -------------------------------------------------

def find_best_route(start, end):

    start = start.lower().strip()
    end = end.lower().strip()

    # Same station
    if start == end:
        return (
            "Already at destination",
            timedelta(0),
            [start],
        )

    results = []

    for line_name, line in train_lines.items():

        stations = line["stations"]

        if start not in stations or end not in stations:
            continue

        start_idx = stations.index(start)
        end_idx = stations.index(end)

        if start_idx < end_idx:
            route = stations[start_idx:end_idx + 1]
            segment_times = line["times"][start_idx:end_idx]
        else:
            route = stations[end_idx:start_idx + 1][::-1]
            segment_times = line["times"][end_idx:start_idx][::-1]

        total_time = sum(segment_times, timedelta())

        results.append(
            (
                line_name,
                total_time,
                route,
            )
        )

    if not results:
        return None, None, None

    return min(results, key=lambda x: x[1])