import pandas as pd
import time
from multiprocessing import Process, cpu_count, Pool


def task(data):
    data = data.sort_values("timestamp")
    data["sr_temp"] = data["temperature"].rolling(window=30).mean()
    data["otk"] = data["temperature"].rolling(window=30).std()
    data = data.dropna()
    data["anomaly"] = ((data["temperature"] > data["sr_temp"] + 2 * data["otk"]) |
                         (data["temperature"] < data["sr_temp"] - 2 * data["otk"]))
    return data


if __name__ == "__main__":
    data = pd.read_csv("data/temperature_data.csv")
    cities = data["city"].unique()
    s1 = time.time()
    test_1 = []
    for city in cities:
        dat = data[data["city"] == city]
        test_1.append(task(dat))
    e1 = time.time()
    print(f"Время без параллелизации: {e1 - s1}")
    s2 = time.time()
    with Pool(cpu_count()) as p:
        test_2 = p.map(task, [g for trash, g in data.groupby("city")])
    e2 = time.time()
    print(f"Время c параллелизации: {e2 - s2}")

