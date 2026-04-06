
import streamlit as st
import numpy as np
from scipy.optimize import linprog

st.title("ODT Optimization Dashboard")

demand = st.number_input("Demand", value=1000)

cost_a = st.number_input("Cost A", value=10)
cap_a = st.number_input("Capacity A", value=500)
risk_a = st.number_input("Risk A", value=0.2)
lead_a = st.number_input("Lead A", value=5)

cost_b = st.number_input("Cost B", value=12)
cap_b = st.number_input("Capacity B", value=700)
risk_b = st.number_input("Risk B", value=0.5)
lead_b = st.number_input("Lead B", value=7)

cost_c = st.number_input("Cost C", value=11)
cap_c = st.number_input("Capacity C", value=400)
risk_c = st.number_input("Risk C", value=0.3)
lead_c = st.number_input("Lead C", value=6)

w_cost = st.slider("Cost Weight", 0.0, 1.0, 0.6)
w_risk = st.slider("Risk Weight", 0.0, 1.0, 0.2)
w_lead = st.slider("Lead Weight", 0.0, 1.0, 0.2)

if st.button("Optimize"):

    cost = np.array([cost_a, cost_b, cost_c])
    risk = np.array([risk_a, risk_b, risk_c])
    lead = np.array([lead_a, lead_b, lead_c])

    objective = w_cost*cost + w_risk*risk + w_lead*lead

    A_ub = [
        [-1,-1,-1],
        [1,0,0],[0,1,0],[0,0,1],
        [1,0,0],[0,1,0],[0,0,1]
    ]

    b_ub = [
        -demand,
        cap_a,cap_b,cap_c,
        0.6*demand,0.6*demand,0.6*demand
    ]

    bounds = [(0,None)]*3

    res = linprog(c=objective, A_ub=A_ub, b_ub=b_ub, bounds=bounds)

    if res.success:
        x = res.x
        st.success("Done!")
        st.write("A:", x[0])
        st.write("B:", x[1])
        st.write("C:", x[2])
    else:
        st.error("Optimization failed")
