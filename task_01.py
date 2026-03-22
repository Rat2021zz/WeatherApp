import pandas as pd

data = pd.read_csv("data/temperature_data.csv")
s_data = data.sort_values(["city", "timestamp"])
s_data["sr_temp"] = s_data.groupby("city")["temperature"].rolling(window=30).mean().reset_index(level=0, drop=True)
s_data["otk"] = s_data.groupby("city")["temperature"].rolling(window=30).std().reset_index(level=0, drop=True)
s_data = s_data.dropna()
ans_s = data.groupby(["city","season"])["temperature"].agg(["mean", "std"]).reset_index()
s_data["anomaly"] = ((s_data["temperature"] > s_data["sr_temp"] + 2*s_data["otk"])|
                     (s_data["temperature"] < s_data["sr_temp"] - 2*s_data["otk"]))
ans_a = s_data[s_data["anomaly"] == True]
print("Аномалии:")
print(ans_a.head())
print("Сезоны:")
print(ans_s.head())
print(data["city"].unique())