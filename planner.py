from datetime import datetime, timedelta
import pandas as pd


# Convert minutes to HH:MM:SS


def convert_time(minutes):
    td = timedelta(minutes=minutes)

    total_seconds = int(td.total_seconds())
    h, rem = divmod(total_seconds, 3600)
    m, s = divmod(rem, 60)

    return f"{h:02}:{m:02}:{s:02}"



# Convert HH:MM:SS to timedelta


def time_to_timedelta(time_str):
    h, m, s = map(int, time_str.split(":"))
    return timedelta(hours=h, minutes=m, seconds=s)


# Load one train line

def load_line(csv_file):

    df = pd.read_csv(csv_file)

    stations = df["name"].str.lower().tolist()

    travel_times = [
        convert_time(t)
        for t in df["estimated_segment_travel_min"].tolist()[1:]
    ]

    return {
        "stations": stations,
        "times": travel_times
    }

from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

train_lines = {
    "Blue": load_line(DATA_DIR / "Blue_line.csv"),
    "Red": load_line(DATA_DIR / "Red_line.csv"),
    "Yellow": load_line(DATA_DIR / "Yellow_line.csv"),
}
# Print complete journey

def calculate_journey(start_point, end_point, line_name):

    line = train_lines[line_name]

    stations = line["stations"]
    travel_times = line["times"]

    start_idx = stations.index(start_point)
    end_idx = stations.index(end_point)

    if start_idx < end_idx:

        route = stations[start_idx:end_idx + 1]
        segment_times = travel_times[start_idx:end_idx]

    else:

        route = stations[end_idx:start_idx + 1][::-1]
        segment_times = travel_times[end_idx:start_idx][::-1]

    departure = datetime.now()

    current = departure
    total = timedelta()

    print("\n")
    print("=" * 60)
    print(f"Best Line : {line_name}")
    print(f"Departure : {departure:%Y-%m-%d %H:%M:%S}")
    print(f"Route      : {' -> '.join(route)}")
    print("=" * 60)

    for i, travel in enumerate(segment_times):

        duration = time_to_timedelta(travel)

        arrival = current + duration

        print(
            f"{i+1}. "
            f"{route[i]} -> {route[i+1]} | "
            f"Travel: {travel} | "
            f"Depart: {current:%H:%M:%S} | "
            f"Arrive: {arrival:%H:%M:%S}"
        )

        total += duration
        current = arrival

    print("\nSummary")
    print("-" * 60)
    print("Total travel time :", total)
    print("Estimated arrival :", departure + total)


# Define the fastest line

def find_best_route(start, end):
    results = []

    for line_name, line in train_lines.items():
        stations = line["stations"]

        if start in stations and end in stations:

            start_idx = stations.index(start)
            end_idx = stations.index(end)

            if start_idx < end_idx:
                segment_times = line["times"][start_idx:end_idx]
                route = stations[start_idx:end_idx + 1]
            else:
                segment_times = line["times"][end_idx:start_idx]
                route = stations[end_idx:start_idx + 1][::-1]

            total = timedelta()
            for t in segment_times:
                total += time_to_timedelta(t)

            results.append((line_name, total, route))

    if not results:
        #return None, None, None
        return ("", timedelta(0), [])

    best_line, best_time, best_route = min(results, key=lambda x: x[1])

    return best_line, best_time, best_route


# Main Function

if __name__ == "__main__":

    print("=" * 60)
    print("TRAIN ROUTE PLANNER")
    print("=" * 60)

    start = input("Enter start station: ").lower().strip()
    end = input("Enter destination: ").lower().strip()

    find_best_route(start, end)