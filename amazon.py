import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_amazon_page(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_info = []

        products = soup.find_all('div', class_='s-result-item')  

        for product in products:
            product_data = {}
            product_url = product.find('a', class_='a-link-normal')
            if product_url:
                product_data['Product URL'] = 'https://www.amazon.in' + product_url['href']
            else:
                product_data['Product URL'] = 'N/A'

            product_name_element = product.find('span', class_='a-text-normal')
            product_data['Product Name'] = product_name_element.text if product_name_element else 'N/A'

            price = product.find('span', class_='a-price')
            product_data['Product Price'] = price.find('span', class_='a-offscreen').text if price else 'N/A'

           
            rating_element = product.find('span', class_='a-icon-alt')
            product_data['Rating'] = rating_element.text if rating_element else 'N/A'

            reviews = product.find('span', class_='a-size-base')
            product_data['Number of Reviews'] = reviews.text if reviews else 'N/A'

            product_info.append(product_data)

        return product_info
    else:
        print(f"Failed to retrieve the page. Status Code: {response.status_code}")
        return []


amazon_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'


num_pages_to_scrape = 20


all_product_data = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.42.34 Safari/537.36'
}


for page_number in range(1, num_pages_to_scrape + 1):
    current_page_url = f'{amazon_url}&page={page_number}'
    page_data = scrape_amazon_page(current_page_url, headers)
    all_product_data.extend(page_data)
    time.sleep(2 + page_number % 4)  


with open('amazon_product_listings.csv', 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_product_data)

print(f"Scraped {len(all_product_data)} product listings and saved to amazon_product_listings.csv")


