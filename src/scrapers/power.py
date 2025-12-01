import requests
from bs4 import BeautifulSoup

def get_power_deals():
    url = "https://www.power.se/erbjudanden"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    deals = []

    for item in soup.select(".product-card"):
        try:
            title = item.select_one(".title").text.strip()
            price = item.select_one(".price").text.strip()
            link = "https://www.power.se" + item.a["href"]

            deals.append({
                "store": "Power",
                "title": title,
                "price": price,
                "old_price": "Okänd",
                "discount": 50,
                "link": link,
                "image": None
            })
        except:
            pass

    return deals
