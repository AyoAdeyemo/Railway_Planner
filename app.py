from datetime import datetime

import streamlit as st

from planner import train_lines, find_best_route

st.set_page_config(page_title="Train Planner", page_icon="🚆")

st.title("🚆 Train Planner")
st.write("Find the fastest train route.")


stations = set()

for line in train_lines.values():
    stations.update(line["stations"])

stations = sorted(stations)

start = st.selectbox("Select start station", stations)
destination = st.selectbox("Select destination station", stations)


def format_duration(td):
    if td is None:
        return "N/A"

    total_seconds = int(td.total_seconds())

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    if hours:
        return f"{hours} hr {minutes} min"

    return f"{minutes} min"


if st.button("Find Route"):

    best_line, best_time, route = find_best_route(start, destination)

    if best_line is None:
        st.error("No route found.")
        st.stop()

    st.success(f"Best Line: {best_line}")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Travel Time", format_duration(best_time))

    with col2:
        st.metric("Train Line", best_line)

    departure = datetime.now()
    arrival = departure + best_time

    st.write(f"Departure: {departure.strftime('%H:%M')}")
    st.write(f"Arrival: {arrival.strftime('%H:%M')}")

    st.subheader("Journey")

    for i, station in enumerate(route):

        st.write(f"🚉 {station.title()}")

        if i < len(route) - 1:
            st.write("⬇️")