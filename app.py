from datetime import datetime

import streamlit as st

from planner import (
    train_lines,
    find_best_route
)

st.title("🚆Train Planner")

st.write("Find the fastest train route.")

stations = set()

for line in train_lines.values():
    stations.update(line["stations"])

stations = sorted(list(stations))

start = st.selectbox("Select start station:", stations)
destination = st.selectbox("Select destination station:", stations)

if st.button("Find Route"):
    find_best_route(start, destination)

result = find_best_route(start, destination)

if result is None:
    st.error("No route found")
    st.stop()

best_line, best_time, route = result

st.success(f"Best line: {best_line}")

total_seconds = int(best_time.total_seconds())
minutes = total_seconds // 60
seconds = total_seconds % 60

st.metric("Travel Time", f"{minutes}m {seconds}s")

st.subheader("Journey")

for stop in route:
    st.write("🚉", stop)


departure = datetime.now()

arrival = departure + best_time

st.write("Departure:", departure.strftime("%H:%M"))

st.write("Arrival:", arrival.strftime("%H:%M"))

col1, col2 = st.columns(2)

with col1:
    st.metric("Travel Time", best_time)

with col2:
    st.metric("Line", best_line)

for i, station in enumerate(route):

    st.write(f"🚉 **{station.title()}**")

    if i != len(route)-1:
        st.write("⬇️")
