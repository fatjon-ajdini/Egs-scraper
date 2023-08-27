from classes.Scraper import Scraper

s = Scraper()

try:
    csv_file = s.get_input_csv_file()
    urls = s.get_urls_from_csv_file(csv_file)
    products = s.scrape(urls)
    s.store_products_to_json(products)
except Exception as e:
    print(f'{e}')

