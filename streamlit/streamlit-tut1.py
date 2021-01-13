import yfinance as yf
import streamlit as sl
import pandas as pd

# Writes the header of the app in Markdown
sl.write("""
# A simple Stock Price App

Shown are the stock closing   price and volume of Google. """ )
tickerSymbol = 'GOOGL'
tickerData = yf.Ticker(tickerSymbol)
tickerDF = tickerData.history(period='1d', start='2010-5-31', end='2010-5-31')

sl.line_chart(tickerDF.Close)
sl.line_chart(tickerDF.Volume)

# run this file in command line to use
# $streamlit run filename.py