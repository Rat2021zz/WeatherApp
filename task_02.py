import requests
import pandas as pd
import datetime


def task(name, key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid={key}&units=metric"
    a = requests.get(url)
    return a.json()


data = pd.read_csv("data/temperature_data.csv")

key = "e28540aada37d0679364b986687cbbfc"
name = "New York"
resp = task(name, key)
tem = resp["main"]["temp"]
m = datetime.datetime.now().month
m_mean = {1:"winter",2:"winter",3:"spring",4:"spring",5:"spring",6:"summer",7:"summer",8:"summer",9:"autumn",
          10:"autumn",11:"autumn",12:"winter"}
cur_s = m_mean[m]
sor_data = data[(data["city"]==name)&(data["season"]==cur_s)]
sr_zn = sor_data["temperature"].mean()
eps = sor_data["temperature"].std()
if sr_zn - 2*eps <= tem <= sr_zn + 2*eps:
    print(f"В городе {name} температура {tem} в пределах нормы.")
else:
    print(f"В городе {name} температура {tem} является аномальной.")
