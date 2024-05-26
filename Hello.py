

import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards

LOGGER = get_logger(__name__)

class StockIndex:
    def __init__(self, tickerSymbol, start_date, end_date):
        self.tickerSymbol = tickerSymbol
        self.start_date = start_date
        self.end_date = end_date
        self.tickerDf = None

    def price_data(self):
        self.tickerData = yf.Ticker(self.tickerSymbol)
        self.tickerDf = self.tickerData.history(period='1d', start=self.start_date, end=self.end_date, auto_adjust=True)
        return self.tickerDf

    def price_value(self):
        if self.tickerDf is not None and not self.tickerDf.empty:
            last_row = self.tickerDf.iloc[-1]
            end_date_price = last_row['Close']
            return end_date_price
        else:
            return None

    def index_percent_cal(self):
        if self.tickerDf is not None and not self.tickerDf.empty:
            if len(self.tickerDf) > 1:
                end_date_price = self.tickerDf.iloc[-1]['Close']
                pre_date_price = self.tickerDf.iloc[-2]['Close']
                percentage_increase = (end_date_price / pre_date_price - 1) * 100
                return percentage_increase
            else:
                return None
        else:
            return None


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    # 페이지 제목
    st.write("# Stock Dashboard 👋")

    # 종합 주가 지수(나스닥, S&P500, 다우존스) Metric Card
    end_date_f_index = st.date_input(label = "최근날짜", value = pd.to_datetime("today"))
    nasdaq_index = StockIndex("^IXIC", "2023-01-01", end_date_f_index)
    sp500_index = StockIndex("^GSPC", "2023-01-01", end_date_f_index)
    dow30_index = StockIndex("^DJI", "2023-01-01", end_date_f_index)

    df_nasdaq = nasdaq_index.price_data()
    nasdaq_price = nasdaq_index.price_value()
    nasdaq_percent_increase = nasdaq_index.index_percent_cal()
    df_sp500 = sp500_index.price_data()
    sp500_price = sp500_index.price_value()
    sp500_percent = sp500_index.index_percent_cal()
    df_dow30 = dow30_index.price_data()
    dow30_price = dow30_index.price_value()
    dow30_percent = dow30_index.index_percent_cal()

    col1, col2, col3 = st.columns(3)
    col1.metric(label="NASDAQ", value=f"${nasdaq_price:,.2f}", delta=f"{nasdaq_percent_increase:,.3f}%")
    col2.metric(label="S&P500", value=f"${sp500_price:,.2f}", delta=f"{sp500_percent:,.3f}%")
    col3.metric(label="Dow30", value=f"${dow30_price:,.2f}", delta=f"{dow30_percent:,.3f}%")
    style_metric_cards()


    # 개별 종목 그래프

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
