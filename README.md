# Web Scraping Tool

This script scrapes product data from the REI website. It collects information about products, including their name, price, and rating, from the search results and individual product pages. The data is then saved in both JSON and CSV formats.

## Features

- **Data Collection:**
  - Scrapes product information from REI's camping and hiking deals page.

- **Data Extraction:**
  - Extracts product names, prices, and ratings from both search results and product detail pages.

- **Data Export:**
  - Saves the collected data to JSON and CSV files.

## Functions

- `get_html(url)`: 
  - Fetches the HTML content from the specified URL using HTTPX and parses it with Selectolax.

- `parse_search_page(html)`: 
  - Extracts URLs of individual product pages from the search results page.

- `parse_product_page(html)`: 
  - Extracts product details from a product page and returns them as a dictionary.

- `export_json(products)`: 
  - Saves the product data to a JSON file.

- `export_csv(products)`: 
  - Saves the product data to a CSV file.

- `append_to_csv(products)`: 
  - Appends new product data to an existing CSV file.

- `extract_text(html, selector)`: 
  - Extracts and cleans text content from a specified HTML element.

- `clean_data(value)`: 
  - Cleans extracted text by removing unwanted characters and extra spaces.

## Usage

1. Run the script to scrape product data from the specified REI URL.
2. The data will be saved in `products.json` and `products.csv`.

## Notes

- Adjust the URL and page range in the `main()` function as needed.
- Ensure that the `httpx`, `selectolax`, and other required packages are installed.