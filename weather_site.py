
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Calvin's Weather Station", layout="wide")

st.title("🌦️ Calvin's Winston-Salem Weather Station")
st.caption("Live personal weather dashboard")

df = pd.read_csv("weather_data_big.csv")
df["Time"] = pd.to_datetime(df["Time"])

latest = df.iloc[-1]

st.markdown("### Current Conditions")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🌡️ Temperature", f"{latest['Temperature']} °F")
col2.metric("🥵 Feels Like", f"{latest['Feels Like']} °F")
col3.metric("💧 Humidity", f"{latest['Humidity']} %")
col4.metric("🌬️ Wind", f"{latest['Wind Speed']} mph")

col5, col6, col7, col8 = st.columns(4)
col5.metric("💨 Wind Gust", f"{latest['Wind Gust']} mph")
col6.metric("🧭 Wind Direction", f"{latest['Wind Direction']}°")
col7.metric("🌧️ Rain Today", f"{latest['Rain Today']} in")
col8.metric("📉 Pressure", f"{latest['Pressure']} inHg")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Temperature / Feels Like")
    st.line_chart(df.set_index("Time")[["Temperature", "Feels Like"]])

    st.subheader("Wind / Gusts")
    st.line_chart(df.set_index("Time")[["Wind Speed", "Wind Gust"]])

    st.subheader("Rain")
    st.line_chart(df.set_index("Time")[["Rain Today", "Rain Rate"]])

with right:
    st.subheader("Humidity")
    st.line_chart(df.set_index("Time")[["Humidity"]])

    st.subheader("Pressure")
    st.line_chart(df.set_index("Time")[["Pressure"]])

    st.subheader("Dew Point")
    st.line_chart(df.set_index("Time")[["Dew Point"]])

st.divider()

with st.expander("Show raw weather data"):
    st.dataframe(df)
