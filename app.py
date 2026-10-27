from decimal import Decimal, ROUND_HALF_UP
import re

import streamlit as st


def calculate_commission(raw_sales):
    """Return commission for a plain dollar amount with at most two decimals."""
    raw_sales = raw_sales.strip()
    if not raw_sales:
        raise ValueError("Enter a sales amount first.")
    if not re.fullmatch(r"-?\d{1,12}(?:\.\d{1,2})?", raw_sales):
        raise ValueError(
            "Enter a number with up to 12 digits before the decimal and "
            "up to 2 after it, without dollar signs or commas."
        )
    sales = Decimal(raw_sales)
    if sales <= 0:
        return Decimal("0.00")
    rate = Decimal("0.10") if sales <= Decimal("50000") else Decimal("0.15")
    return (sales * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


st.title("Sales Commission Calculator")
st.caption("10% of total sales up to $50,000; 15% of all sales above $50,000.")
sales = st.text_input("Total sales ($)", placeholder="Example: 50001.00")

if st.button("Calculate"):
    try:
        commission = calculate_commission(sales)
    except ValueError as error:
        st.error(str(error))
    else:
        if Decimal(sales.strip()) < 0:
            st.warning("Negative sales earn $0 commission under this policy.")
        st.write(f"Commission: ${commission:,.2f}")
