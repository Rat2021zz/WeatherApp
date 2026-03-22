import asyncio
import aiohttp
import pandas as pd
import datetime


async def task_as(name, key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid={key}&units=metric"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


async def main():
    key = "API"  # Ключ от openweather
    name = "New York"  # Можно вставить любое название из ['New York' 'London' 'Paris' 'Tokyo' 'Moscow' 'Sydney' 'Berlin'
    # 'Beijing' 'Rio de Janeiro' 'Dubai' 'Los Angeles' 'Singapore' 'Mumbai' 'Cairo' 'Mexico City']
    resp = await task_as(name, key)
    if resp.get("cod") != 401:
       tem = resp['main']['temp']
       data = pd.read_csv("data/temperature_data.csv")
       m = datetime.datetime.now().month
       m_mean = {1: "winter", 2: "winter", 3: "spring", 4: "spring", 5: "spring", 6: "summer", 7: "summer", 8: "summer",
                 9: "autumn",
                 10: "autumn", 11: "autumn", 12: "winter"}
       cur_s = m_mean[m]
       sor_data = data[(data["city"] == name) & (data["season"] == cur_s)]
       sr_zn = sor_data["temperature"].mean()
       eps = sor_data["temperature"].std()
       if sr_zn - 2 * eps <= tem <= sr_zn + 2 * eps:
           print(f"В городе {name} температура {tem} в пределах нормы.")
       else:
           print(f"В городе {name} температура {tem} является аномальной.")

    else:
        print("Ошибка 401")


asyncio.run(main())