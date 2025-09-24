import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin, urlparse

BASE_URL= "http://books.toscrape.com/catalogue/category/books/"
CATEGORIES= [
    "travel_2/index.html",
    "mystery_3/index.html",
    "historical-fiction_4/index.html"
]
HEADERS= {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

RATING_MAP= {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

def get_soup(url):
    resp= requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def extract_book_info(product):
    title = product.h3.a.get("title", product.h3.a.text).strip()

    price_tag= product.select_one(".price_color")
    price= price_tag.text.strip() if price_tag else ""

    avail_tag= product.select_one(".instock.availability")
    availability= avail_tag.get_text(strip=True) if avail_tag else ""

    rating=0
    p_tag= product.select_one("p.star-rating")
    if p_tag:
        classes= p_tag.get("class", [])
        for c in classes:
            if c in RATING_MAP:
                rating = RATING_MAP[c]
                break
    return {
        "Title": title,
        "Price": price,
        "Availability": availability,
        "Rating": rating
    }

def get_books_from_category(category_url):
    books = []
    url = urljoin(BASE_URL, category_url)

    while url:
        print("Loading:", url)
        soup = get_soup(url)

        for product in soup.select(".product_pod"):
            books.append(extract_book_info(product))


        next_button = soup.select_one("li.next a")
        if next_button:
            next_href = next_button.get("href")
            url = urljoin(url, next_href)
            time.sleep(1)
        else:
            url = None

    return books


def main():
    all_books = []
    for category in CATEGORIES:
        print("Category:", category)
        all_books.extend(get_books_from_category(category))

    #Save to csv
    with open("books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Price", "Availability", "Rating"])
        writer.writeheader()
        writer.writerows(all_books)

    print(f"Finish script. General books: {len(all_books)}. File: books.csv")


if __name__ == "__main__":
    main()