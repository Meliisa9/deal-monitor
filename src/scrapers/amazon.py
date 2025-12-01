import requests
from bs4 import BeautifulSoup

def get_amazon_deals():
    url = "https://www.amazon.se/gp/goldbox"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    deals = []

    for item in soup.select(".DealContent"):
        try:
            title = item.text.strip()[:120]
            link = "https://www.amazon.se"

            deals.append({
                "store": "Amazon",
                "title": title,
                "price": "Se sida",
                "old_price": "Okänd",
                "discount": 50,
                "link": link,
                "image": None
            })
        except:
            pass

    return deals
