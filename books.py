import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

STAR_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def get_page_url(page_num):
    if page_num == 1:
        return "https://books.toscrape.com/"
    else:
        return f"https://books.toscrape.com/catalogue/page-{page_num}.html"

def scrape_page(page_num, start_index):
    url = get_page_url(page_num)
    print(f"Scraping page {page_num}/50: {url}")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select("article.product_pod")
    page_products = []

    for i, item in enumerate(items):
        title = item.select_one("h3 a")
        image = item.select_one("img")
        stars = item.select_one("p.star-rating")
        availability = item.select_one("p.availability")
        price = item.select_one("p.price_color")

        star_word = stars["class"][1] if stars else "One"
        star_number = STAR_MAP.get(star_word, 0)

        avail_text = availability.text.strip().lower() if availability else ""
        avail_status = "in_stock" if "in stock" in avail_text else "not"

        page_products.append({
            "book_number": start_index + i,
            "title": title["title"] if title else "N/A",
            "image": "https://books.toscrape.com/" + image["src"].replace("../", "") if image else "N/A",
            "stars": star_number,
            "price": price.text.strip() if price else "N/A",
            "availability": avail_status
        })

    return page_products

all_products = []

for page in range(1, 51):
    start = (page - 1) * 20 + 1
    products = scrape_page(page, start)
    all_products.extend(products)
    print(f"  Page {page} done — {len(products)} books found — Total so far: {len(all_products)}")

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, ensure_ascii=False, indent=2)

print(f"\nComplete! Total {len(all_products)} books saved in products.json")
print("\nSample (first 3):")
for p in all_products[:3]:
    print(f"  #{p['book_number']} {p['title']} | Stars: {p['stars']} | Price: {p['price']} | {p['availability']}")