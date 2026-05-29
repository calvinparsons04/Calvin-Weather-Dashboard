
import pandas as pd
import streamlit as st
import time
import math

st.set_page_config(page_title="Winston Salem, NC Weather Dashboard", layout="wide")

df = pd.read_csv("weather_data_big.csv")
df["Time"] = pd.to_datetime(df["Time"])
latest = df.iloc[-1]

def f_to_c(f):
    return (f - 32) * 5 / 9 if pd.notna(f) else 0

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #061229, #0b1f4d);
    color: white;
}
.card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 24px;
    min-height: 170px;
}
.big {
    font-size: 48px;
    font-weight: 700;
}
.small {
    font-size: 22px;
    color: #7da2ff;
}
.label {
    font-size: 20px;
    font-weight: 700;
}
.rain-card {
    background: rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 16px;
    height: 150px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 📍 Winston Salem, NC Weather Dashboard")
st.markdown(f"Last updated: **{latest['Time']}**  \n🟢 Auto-refreshing every 60 seconds")

temp_f = latest["Temperature"]
feels_f = latest["Feels Like"]
humidity = latest["Humidity"]
dew = latest["Dew Point"]
wind = latest["Wind Speed"]
gust = latest["Wind Gust"]
wind_dir = latest["Wind Direction"]
pressure = latest["Pressure"]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="card">
        <div class="label">🌡️ Temperature</div><br>
        <div class="big">{temp_f:.1f} °F</div>
        <div class="small">{f_to_c(temp_f):.1f} °C</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div class="label">🧍 Feels Like</div><br>
        <div class="big">{feels_f:.1f} °F</div>
        <div class="small">{f_to_c(feels_f):.1f} °C</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        <div class="label">💧 Humidity</div><br>
        <div class="big">{humidity:.0f}%</div>
        <div class="small">Dew Point: {dew:.1f} °F</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="card">
        <div class="label">🌬️ Wind</div><br>
        <div class="big">{wind:.1f} mph</div>
        <div class="small">Direction: {wind_dir:.0f}°</div>
        <div class="small">Gust: {gust:.1f} mph</div>
    </div>
    """, unsafe_allow_html=True)

left, right = st.columns([2, 1])

with left:
    st.markdown("## 🌧️ Daily Rainfall")

today_rain = latest["Rain Today"]

st.markdown(f"""
<div style="
background: rgba(255,255,255,0.07);
border-radius:18px;
padding:30px;
width:250px;
height:180px;
">
    <div style="font-size:22px;font-weight:700;">
        {latest['Time'].strftime('%m/%d')}
    </div>

    <br>

    <div style="font-size:48px;font-weight:700;">
        {today_rain:.2f}
        <span style="font-size:24px;">in</span>
    </div>

    <div style="
        margin-top:20px;
        height:20px;
        background:rgba(255,255,255,0.12);
        border-radius:20px;
    ">
        <div style="
            width:{min(today_rain*20,100)}%;
            height:20px;
            background:#4d79ff;
            border-radius:20px;
        ">
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

with right:
    st.markdown("## 🧭 Pressure")

    min_p = 28.5
    max_p = 31.5
    pct = max(0, min(100, ((pressure - min_p) / (max_p - min_p)) * 100))

    st.markdown(f"""
    <div class="card">
        <div class="big">{pressure:.2f}</div>
        <div class="small">inHg</div><br>
        <div style="background:rgba(255,255,255,0.15);border-radius:20px;height:24px;">
            <div style="background:#4d79ff;width:{pct}%;height:24px;border-radius:20px;"></div>
        </div>
        <br>
        <div class="small">{min_p} → {max_p} inHg</div>
        <div class="small">Trend: {latest["Pressure Trend"]}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

graph1, graph2 = st.columns(2)

with graph1:
    st.markdown("## 🌡️ Temperature History")
    st.line_chart(df.set_index("Time")[["Temperature", "Feels Like"]])

with graph2:
    st.markdown("## 🧭 Pressure History")
    st.line_chart(df.set_index("Time")[["Pressure"]])

with st.expander("Show raw weather data"):
    st.dataframe(df)

time.sleep(60)
st.rerun()
