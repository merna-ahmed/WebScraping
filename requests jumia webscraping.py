
import requests
from bs4 import BeautifulSoup
import csv

link = 'https://www.jumia.com.eg/?srsltid=AfmBOoqp0LTpQRNkqq2d3r_zSzsOm_AO646GyFITFeuS9Jq8X74BExRc'

   
headers = {"User-Agent": "Mozilla/5.0"}
page = requests.get(link, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')

product_items = soup.find_all('article', {'class': 'prd'})

extracted_data = []

for i in product_items:
    product_name_div = i.find('div', {'class': 'name'})
    product_price_div = i.find('div', {'class': 'prc'})
    product_discount_div = i.find('div', {'class': 'bdg _dsct'})
    product_stock_div = i.find('div', {'class': 'stk'})
    product_link_tag = i.find('a', {'class': 'core'})
    product_img_tag = i.find('img', {'class': 'img'})

    product_name = product_name_div.text.strip() if product_name_div else "No name"
    product_price = product_price_div.text.strip() if product_price_div else "No price"
    product_discount = product_discount_div.text if product_discount_div else "No discount"
    product_stock = product_stock_div.text.strip() if product_stock_div else "In stock"
    
    product_link = f"https://www.jumia.com.eg{product_link_tag.get('href')}" if product_link_tag else "No link"
    product_img = product_img_tag.get('data-src') if product_img_tag else "No image"
    extracted_data.append({
        "Product Name": product_name,
        "Product Image": product_img,
        "Product Price": product_price,
        "Product Discount": product_discount,
        "Product Stock": product_stock,
        "Product Link": product_link
    })

next_page = soup.find('a', {'aria-label': 'Next'})
if next_page:
        base_url = "https://www.jumia.com.eg" + next_page.get('href')
else:
        base_url = None 

def printing():
    header = extracted_data[0].keys()
    Path='D:/product_items_merna_ahmed.csv'

    with open(Path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file,header)
        writer.writeheader()
        writer.writerows(extracted_data)
        print('file printed successfully')

print(f"Total products extracted: {len(extracted_data)}")

printing()