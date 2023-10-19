import requests
from bs4 import BeautifulSoup
import csv
import time
import csv
import re


def is_valid_url(url):
    url_pattern = re.compile(r'^https?://[a-zA-Z0-9.-]+')
    return re.match(url_pattern, url)


csv_file = 'amazon_product_listings.csv'
txt_file = 'product_urls.txt'

valid_urls = []

try:
    with open(csv_file, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row: 
                url = row[0]  
                if is_valid_url(url):
                    valid_urls.append(url)
                else:
                    print(f"Skipping invalid URL: {url}")
except FileNotFoundError:
    print(f"Error: The CSV file '{csv_file}' was not found.")


with open(txt_file, 'w') as txtfile:
    for url in valid_urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                txtfile.write(url + '\n')
            else:
                print(f"Failed to retrieve URL: {url}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect to URL: {url} - {e}")

print(f"Valid URLs extracted and saved to {txt_file}")



def scrape_amazon_product_page(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_info = {}

        
        product_info['Description'] = soup.find('div', {'id': 'productDescription'})
        product_info['ASIN'] = soup.find('th', text='ASIN').find_next('td')
        product_info['Product Description'] = soup.find('ul', {'class': 'a-unordered-list'})
        product_info['Manufacturer'] = soup.find('th', text='Manufacturer').find_next('td')

        
        for key, element in product_info.items():
            if element:
                product_info[key] = element.get_text().strip()
            else:
                product_info[key] = 'N/A'

        return product_info
    else:
        print(f"Failed to retrieve the page. Status Code: {response.status_code}")
        return {}


with open('product_urls.txt', 'r') as url_file:
    product_urls = url_file.read().splitlines()


all_product_data = []


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.42.34 Safari/537.36'
}


for product_url in product_urls[:200]:
    product_data = scrape_amazon_product_page(product_url, headers)
    if product_data:
        all_product_data.append(product_data)
    time.sleep(2) 
with open('amazon_product_info.csv', 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Description', 'ASIN', 'Product Description', 'Manufacturer']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_product_data)

print(f"Scraped information for {len(all_product_data)} products and saved to amazon_product_info.csv")
