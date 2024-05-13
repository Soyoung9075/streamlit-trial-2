

import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Stock Dashboard 👋")

    ticker = st.sidebar.text_input('Ticker')
    start_date = st.sidebar.date_input('Start Date')
    end_date = st.sidebar.date_input('End Date')

    # Get data on this ticker
    tickerData = yf.Ticker(ticker)

    # Get the historical prices for this ticker
    tickerDf = tickerData.history(period = '1d', start = start_date, end = end_date)
    fig = px.line(tickerDf, x= tickerDf.index, y= tickerDf['Close'], title = ticker)
    st.plotly_chart(fig)

    pricedf = tickerDf.copy()
    pricedf['%Change'] = (tickerDf['Close'] / tickerDf['Close'].shift(1) - 1)*100
    pricedf = pricedf[['Open', 'High', 'Low', 'Close', '%Change','Volume', 'Dividends', 'Stock Splits','Capital Gains']]
    
    # Function to highlight negative values
    def highlight_negative(val):
        color = '#F7727F' if val < 0 else ''
        return f'background-color: {color}'

    # Apply the styling to column '%Change'
    styled_df = pricedf.style.applymap(highlight_negative, subset=['%Change'])
    
    st.dataframe(styled_df)




if __name__ == "__main__":
    run()
