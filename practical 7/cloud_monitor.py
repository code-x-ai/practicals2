import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cloud Resource Monitoring Dashboard", layout="wide")

st.title("Cloud Resource Monitoring Dashboard")

# ---------------- Simulated Cloud Resources ----------------
vms = pd.DataFrame({
    "VM": ["VM-1", "VM-2", "VM-3"],
    "CPU": [42, 68, 91],
    "Memory": [48, 72, 88],
    "MIPS": [500, 1000, 1500]
})

tasks = pd.DataFrame({
    "Task": ["T1", "T2", "T3", "T4", "T5", "T6"],
    "Workload": [10000, 20000, 15000, 30000, 12000, 25000],
    "Priority": ["Low", "High", "Medium", "Critical", "Low", "High"]
})

# ---------------- Cloud Resources Section ----------------
st.subheader("Cloud Resources")
st.dataframe(vms, hide_index=True)

st.plotly_chart(
    px.bar(
        vms, x="VM", y=["CPU", "Memory"],
        barmode="group",
        title="Resource Utilization"
    ),
    use_container_width=True
)

# ---------------- Scheduling Function ----------------
def schedule(algorithm):
    load = [0, 0, 0]
    result = []

    for i, task in tasks.iterrows():
        if algorithm == "Round Robin":
            vm = i % 3
        else:  # Least Loaded
            vm = load.index(min(load))

        exec_time = task.Workload / vms.MIPS[vm]
        load[vm] += exec_time
        result.append([task.Task, f"VM-{vm + 1}", round(exec_time, 2)])

    df = pd.DataFrame(result, columns=["Task", "VM", "Time"])
    return df, max(load)

# ---------------- Algorithm Selection ----------------
algorithm = st.selectbox(
    "Scheduling Algorithm",
    ["Round Robin", "Least Loaded"]
)

result, makespan = schedule(algorithm)

# Makespan values for both algorithms (used for comparison)
_rr_df, rr_makespan = schedule("Round Robin")
_ll_df, ll_makespan = schedule("Least Loaded")

# ---------------- Metric Cards ----------------
c1, c2, c3 = st.columns(3)
c1.metric("Virtual Machines", len(vms))
c2.metric("Average CPU", f"{vms.CPU.mean():.1f}%")
c3.metric("Current Makespan", f"{makespan:.1f}")

# ---------------- System Status ----------------
if vms.CPU.max() >= 80:
    st.error("SYSTEM STATUS: CRITICAL")
elif vms.CPU.mean() >= 60:
    st.warning("SYSTEM STATUS: WARNING")
else:
    st.success("SYSTEM STATUS: HEALTHY")

# ---------------- Task Performance ----------------
st.subheader("Task Performance")
st.dataframe(result, hide_index=True)

st.plotly_chart(
    px.bar(
        result, x="Task", y="Time",
        color="Time",
        title="Task Execution Time"
    ),
    use_container_width=True
)

# ---------------- Scheduling Comparison ----------------
st.subheader("Scheduling Comparison")

comparison = pd.DataFrame({
    "Algorithm": ["Round Robin", "Least Loaded"],
    "Makespan": [rr_makespan, ll_makespan]
})

st.plotly_chart(
    px.bar(
        comparison, x="Algorithm", y="Makespan",
        color="Algorithm", text="Makespan",
        title="Makespan Comparison"
    ),
    use_container_width=True
)

improvement = ((rr_makespan - ll_makespan) / rr_makespan) * 100
st.metric(
    "Least Loaded Improvement",
    f"{improvement:.1f}%"
)