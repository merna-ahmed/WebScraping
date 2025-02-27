

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def scrape_page(driver):
    wait = WebDriverWait(driver, 10)
    extracted_data = []

  
    beds_items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'MuiGrid-item')))
    
    for i in beds_items:
        try:
            bed_name = i.find_element(By.CLASS_NAME, 'base-productCard_productCard_name__r_Ltu').text
        except:
            bed_name = "No name"
        
        try:
            bed_price = i.find_element(By.CLASS_NAME, "base-product-price_bold__DqOea").text
        except:
            bed_price = "No price"
        
        try:
            bed_discount = i.find_element(By.CLASS_NAME, 'prices_discount__DliS1').text
        except:
            bed_discount = "No discount"
        
        try:
            bed_stock = i.find_element(By.CLASS_NAME, 'base-typography_p__HIG5b').text
        except:
            bed_stock = "In stock"
        
        extracted_data.append({
            "Bed Name": bed_name,
            "Bed Price": bed_price,
            "Bed Discount": bed_discount,
            "Bed Stock": bed_stock
        })

    return extracted_data

def printing(extracted_data):
    if not extracted_data:
        print("No data to write to CSV.")
        return
    
    header = extracted_data[0].keys()
    Path = 'D:/beds_items_merna_ahmed5.csv'

    with open(Path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, header)
        writer.writeheader()
        writer.writerows(extracted_data)
        print('File printed successfully')

def main():
    base_url = 'https://homzmart.com/en/search/bed?page='
    driver = webdriver.Chrome()
    all_data = []

    for page_number in range(1, 100):  # من الصفحة 1 إلى 99
        driver.get(base_url + str(page_number))
        time.sleep(2)  

       
        page_data = scrape_page(driver)
        all_data.extend(page_data)

        print(f"Scraped page {page_number}")

    driver.quit()

    print(f"Total products extracted: {len(all_data)}")
    printing(all_data)

if __name__ == "__main__":
    main()