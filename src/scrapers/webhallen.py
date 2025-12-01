import requests
from bs4 import BeautifulSoup

def get_webhallen_deals():
    url = "https://www.webhallen.com/se/category/438-Rea"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    deals = []

    for item in soup.select(".product-list-item"):
        try:
            title = item.select_one(".product-name").text.strip()
            price = item.select_one(".price").text.strip()
            link = "https://www.webhallen.com" + item.a["href"]

            deals.append({
                "store": "Webhallen",
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
