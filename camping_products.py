import httpx
from selectolax.parser import HTMLParser
import time
from urllib.parse import urljoin
from dataclasses import dataclass, asdict, fields
import json
import csv

@dataclass
class Item:
    name:str | None
    price:str | None
    rating:float | None

def get_html(url):

    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    }

    response = httpx.get(url, headers=headers, follow_redirects=True)
    #print(response.status_code)
    
    try:
        html = HTMLParser(response.text)
        
        return html
    except Exception as e:
        print(f"An error occurred: {e}")

def parse_search_page(html):
    if html is None:
        print("No HTML content to parse.")
        return

    products = html.css("li.VcGDfKKy_dvNbxUqm29K")
    for product in products:
        yield urljoin("https://www.rei.com",product.css_first("a").attributes["href"])

def parse_product_page(html):
    if html is None:
        print("No HTML content to parse.")
        return
    
    new_item = Item(
        name = extract_text(html,"h1#product-page-title"),
        price= extract_text(html,"span#buy-box-product-price"),
        rating= extract_text(html,"span.cdr-rating__number_15-1-0")
    )

    return asdict(new_item)

def export_json(products):
    with open("products.json", "w", encoding="utf=8") as f:
        json.dump(products, f, indent=4)
    print("Data exported to JSON")


def export_csv(products):
    field_names = [field.name for field in fields(Item)]
    with open("products.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(products)
    print("Data exported to CSV")


def append_to_csv(products):
    field_names = [field.name for field in fields(Item)]
    with open("allproducts.csv", "a") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writerow(products)
    print("Data appended to CSV")


def extract_text(html,selector):
    try:
        element = html.css_first(selector)
        return clean_data(element)
    except Exception as e:
        print(f"An error occurred while extracting text: {e}")
        return None
    
def clean_data(value):
    value = value.text(separator="").replace(u'\u00a0', '')
    chars_to_remove = ["$"]
    for char in chars_to_remove:
        value = value.replace(char, "")
    return value.strip()
    
def main():
    products = []
    url = "https://www.rei.com/c/camping-and-hiking/f/scd-deals?page="
    for page in range(1,2):
        print(f"Gathering page {page}")
        page_url = url + str(page)
        html = get_html(page_url)
        product_urls = parse_search_page(html)
        for url in product_urls:
            print(url)
            html = get_html(url)
            product = parse_product_page(html)
            print(product)
            # append_to_csv(product)
            products.append(product)
            time.sleep(0.4)


            
    export_json(products)
    export_csv(products)
            
            


if __name__ == "__main__":
    main()



