import requests
import collections
from bs4 import BeautifulSoup


def main():
    response = requests.get("https://weather.com/weather/today")
    content = response.content

    source = BeautifulSoup(content, "html.parser")
    weather_now = get_weather_now(source)
    print(get_weather_now_str(weather_now))


def get_weather_now(html_doc):
    today_now_container = html_doc.select("section.today_nowcard-container")[0]
    now_temp = today_now_container.select("div.today_nowcard-temp")[0].text
    feel_temp = today_now_container.select("span.deg-feels")[0].text
    current_uv_index = (today_now_container
                        .select("div.today_nowcard-hilo > div > span")[1].text)
    current_uv_index = current_uv_index.split(' ')
    uv_index = current_uv_index[0]
    uv_max = current_uv_index[-1]

    Weather = collections.namedtuple("Weather", [
                                            "temp",
                                            "feel",
                                            "uv_index",
                                            "uv_max"])

    return Weather(now_temp, feel_temp, int(uv_index), int(uv_max))


def get_weather_now_str(weather_now):

    def get_uv_instructions(uv_index):
        advice = "==> "
        if uv_index <= 2:
            advice += "Low radiation. No protection required."
        elif uv_index <= 5:
            advice += "Moderate radiation. Protection required."
        elif uv_index <= 7:
            advice += "High radiation. Protection required."
        elif uv_index <= 10:
            advice += "VERY HIGH RADIATION! Protection essential."
        elif uv > 10:
            advice += "EXTREME RADIATION! Protection essential."
        else:
            print("ERROR! Invalid uv_index")
            return -1

        return advice

    s = f"The temperature now is {weather_now.temp}.\n"
    s += f"It feels like {weather_now.feel}.\n"
    s += f"UV index is {weather_now.uv_index} out of {weather_now.uv_max}.\n"
    s += "\t"
    s += get_uv_instructions(weather_now.uv_index)

    return s



main()
