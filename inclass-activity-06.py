from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

START = date.today() - timedelta(days=365)
END = date.today() - timedelta(days=1)

st.set_page_config(layout="wide")
st.title("Stock Analysis")

st.sidebar.header("Inputs")
ticker = st.sidebar.text_input("Stock ticker", "AAPL").strip().upper()
comparison_ticker = st.sidebar.text_input("Comparison ticker", "SPY").strip().upper()
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("Start date", START)
end_date = col2.date_input("End date", END)
moving_average = st.sidebar.slider("Moving average", 5, 100, 20)
run_button = st.sidebar.button("Run analysis")


@st.cache_data
def get_stock_data(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        if data is None or data.empty:
            return None, f"No data for {ticker}"
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        data = data.dropna(subset=["Close"])
        if data.empty:
            return None, f"No data for {ticker}"
        return data, None
    except Exception as e:
        return None, f"Download failed: {e}"


if run_button:
    df, error = get_stock_data(ticker, start_date, end_date)
    comparison_df, comparison_error = get_stock_data(comparison_ticker, start_date, end_date)

    if error or comparison_error:
        st.error(error or comparison_error)
    else:
        df["Moving average"] = df["Close"].rolling(moving_average).mean()
        df["normalized_close"] = (df["Close"] / df["Close"].iloc[0]) * 100
        comparison_df["normalized_close"] = (comparison_df["Close"] / comparison_df["Close"].iloc[0]) * 100

        tab1, tab2, tab3, tab4 = st.tabs(["Prices", "Data", "Statistics", "📈 Comparison"])

        with tab1:
            fig = px.line(df, x=df.index, y=["Close", "Moving average"], title=ticker)
            st.plotly_chart(fig)

        with tab2:
            st.dataframe(df)

        with tab3:
            st.dataframe(df[["Close", "Volume"]].describe())

        with tab4:
            comparison = pd.DataFrame({
                ticker: df["normalized_close"],
                comparison_ticker: comparison_df["normalized_close"]
            })
            fig = px.line(
                comparison,
                x=comparison.index,
                y=comparison.columns,
                title=f"{ticker} vs {comparison_ticker} Performance (Base 100)",
                labels={"value": "Normalized close", "variable": "Ticker", "index": "Date"}
            )
            st.plotly_chart(fig)

            summary = pd.DataFrame({
                "Ticker": [ticker, comparison_ticker],
                "Min": [df["normalized_close"].min(), comparison_df["normalized_close"].min()],
                "Max": [df["normalized_close"].max(), comparison_df["normalized_close"].max()],
                "Final Normalized Value": [df["normalized_close"].iloc[-1], comparison_df["normalized_close"].iloc[-1]]
            })
            st.dataframe(summary)
