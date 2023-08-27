import csv
import sys
import os
import json
import requests
from bs4 import BeautifulSoup


class Scraper:
    def get_input_csv_file(self):
        if len(sys.argv) <= 1:
            raise Exception('Please provide csv file!')
        return sys.argv[1]

    def get_urls_from_csv_file(self, csv_file):
        urls = []

        if os.path.isfile(csv_file) == False:
            raise Exception('Please provide valid csv file')

        with open(csv_file, 'r', newline='') as fh:
            reader = csv.reader(fh)
            for row in reader:
                urls.append(row[0])

        return urls

    def scrape(self, urls):
        products = []

        if len(urls) == 0:
            raise Exception('CSV file is empty or format is not correct')

        for url in urls:
            response = requests.get(url)
            product_html = response.text

            soup = BeautifulSoup(product_html, 'html.parser')

            # title
            title = soup.find('div', {'class': 'product-content'}).find('h1').text

            # price
            price = soup.find('div', {'class': 'detail-price'}).find('span').text
            price = price.replace("€", "")

            # description
            description = soup.find('div', {'id': 'tabs-description'}).text

            # image
            image = soup.find('img', {'class': 'image-zoom'}).get('src')

            product = {'title': title, 'price': price, 'description': description, 'image':image}
            
            products.append(product)

        return products

    def store_products_to_json(self, products):
        if len(products) <= 0:
            raise Exception('Product list is empty')

        products_json = json.dumps(products)
        with open('products/products.json', 'w') as fh:
            fh.write(products_json)
            print('Saved!')

