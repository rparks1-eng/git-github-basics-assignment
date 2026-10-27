import streamlit as st

st.title("Sales Commission Calculator")

sales = st.number_input("Total sales ($)", value=0.0, step=100.0)

if st.button("Calculate"):
    if sales <= 50000:
        commission = sales * 0.10
    else:
        commission = 50000 * 0.10 + (sales - 50000) * 0.15

    st.write(f"Commission: ${commission:,.2f}")
