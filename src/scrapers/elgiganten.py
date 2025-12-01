import requests
from bs4 import BeautifulSoup

def get_elgiganten_deals():
    url = "https://www.elgiganten.se/rea"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    deals = []

    for item in soup.select(".product-tile"):
        try:
            title = item.select_one(".product-title").text.strip()
            price = item.select_one(".price").text.strip()
            link = "https://www.elgiganten.se" + item.a["href"]

            deals.append({
                "store": "Elgiganten",
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
