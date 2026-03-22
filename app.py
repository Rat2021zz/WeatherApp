import streamlit as str
import pandas as pd
import datetime
import plotly.express as pl
import requests

str.title("Погода в городах")
file_up = str.file_uploader("CSV файл", type=["csv"])
if file_up:
    data = pd.read_csv(file_up)
    citys = data["city"].unique()
    city = str.selectbox("Город", citys)
    key = str.text_input("API key", type="password")
    data = data[data["city"] == city]
    str.subheader("Общая статистика")
    str.dataframe(data["temperature"].describe())
    t1 = data.groupby("season")["temperature"].agg(["mean", "std"]).reset_index()
    str.subheader("Статистика по сезонам")
    str.dataframe(t1)
    m_n = datetime.datetime.now().month
    m_mean = {1: "winter", 2: "winter", 3: "spring", 4: "spring", 5: "spring", 6: "summer", 7: "summer",
              8: "summer", 9: "autumn", 10: "autumn", 11: "autumn", 12: "winter"}
    cur_s = m_mean[m_n]
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data = data.sort_values("timestamp")
    data["sr_zn"] = data["temperature"].rolling(30).mean()
    data["eps"] = data["temperature"].rolling(30).std()
    data = data.dropna()
    data["anomaly"] = ((data["temperature"] > data["sr_zn"] + 2 * data["eps"]) |
                       (data["temperature"] < data["sr_zn"] - 2 * data["eps"]))
    str.subheader(f"Временный ряд для города {city}")
    gr = pl.line(data, x="timestamp", y="temperature")
    t1 = data[data["anomaly"] == True]
    gr.add_scatter(x=t1["timestamp"], y=t1["temperature"], mode="markers", name="Аномальные точки")
    gr.add_scatter(x=data["timestamp"], y=data["sr_zn"], mode="lines", name="Скользящее среднее")
    str.plotly_chart(gr)
    if key:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
        ans = requests.get(url).json()
        if ans.get("cod") == 401:
            str.error("Неверный API ключ")
        else:
            tem = ans["main"]["temp"]
            str.subheader(f"Текущая температура в городе {city}")
            str.write(f"{tem} °C")
            dat_s = data[data["season"] == cur_s]
            sr_t = dat_s["temperature"].mean()
            eps = dat_s["temperature"].std()
            if sr_t - 2 * eps <= tem <= sr_t + 2 * eps:
                str.write("Температура в пределах нормы")
            else:
                str.write("Температура аномальная")
    else:
        str.warning("Введите API ключ для получения текущей температуры")







