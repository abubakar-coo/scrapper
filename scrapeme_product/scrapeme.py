import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_page_url(page_num):
    if page_num == 1:
        return "https://scrapeme.live/shop/"
    else:
        return f"https://scrapeme.live/shop/page/{page_num}/"

def scrape_page(page_num, start_index):
    url = get_page_url(page_num)
    print(f"Scraping page {page_num}/48: {url}")

    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select("li.product")
    page_products = []

    for i, item in enumerate(items):
        title = item.select_one("h2.woocommerce-loop-product__title")
        image = item.select_one("img")
        price = item.select_one("span.price span.woocommerce-Price-amount")

        img_url = image["src"] if image else "N/A"
        if img_url.startswith("//"):
            img_url = "https:" + img_url

        price_text = price.text.strip() if price else "N/A"

        page_products.append({
            "product_number": start_index + i,
            "title": title.text.strip() if title else "N/A",
            "image": img_url,
            "price": price_text
        })

    return page_products

all_products = []

for page in range(1, 49):
    start = (page - 1) * 16 + 1
    products = scrape_page(page, start)
    all_products.extend(products)
    print(f"  Page {page} done — {len(products)} products found — Total: {len(all_products)}")

with open("scrapeme_products.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, ensure_ascii=False, indent=2)

print(f"\nComplete! Total {len(all_products)} products saved in scrapeme_products.json")
print("\nSample (first 3):")
for p in all_products[:3]:
    print(f"  #{p['product_number']} {p['title']} | Price: {p['price']}")