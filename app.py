import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Customer Review Sentiment Dashboard", layout="wide")

st.title("💬 Customer Review Sentiment Dashboard")

uploaded = st.file_uploader("Upload reviews CSV", type="csv")

if uploaded:
    df = pd.read_csv(uploaded, parse_dates=["Date"])
else:
    df = pd.read_csv("customer_reviews_sample.csv", parse_dates=["Date"])

# KPIs
st.metric("Average Rating", f"{df['Rating'].mean():.2f}")
st.metric("% Positive", f"{(df['SentimentLabel'].eq('Positive').mean()*100):.1f}%")
st.metric("% Neutral", f"{(df['SentimentLabel'].eq('Neutral').mean()*100):.1f}%")
st.metric("% Negative", f"{(df['SentimentLabel'].eq('Negative').mean()*100):.1f}%")

# Sentiment over time
sent_trend = df.groupby([df['Date'].dt.to_period('M'), 'SentimentLabel']).size().reset_index(name="Count")
sent_trend["Date"] = sent_trend["Date"].astype(str)
fig = px.line(sent_trend, x="Date", y="Count", color="SentimentLabel", title="Sentiment Trend Over Time")
st.plotly_chart(fig, use_container_width=True)

# Drilldown
st.dataframe(df)