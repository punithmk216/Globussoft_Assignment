from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime

driver = webdriver.Chrome()
driver.get("https://www.amazon.in/s?k=laptops")

products = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')

data = []

for p in products:
    try:
        title = p.find_element(By.TAG_NAME, "h2").text
    except:
        title = None

    try:
        price = p.find_element(By.CLASS_NAME, "a-price-whole").text
    except:
        price = None

    try:
        rating = p.find_element(By.CLASS_NAME, "a-icon-alt").text
    except:
        rating = None

    try:
        image = p.find_element(By.TAG_NAME, "img").get_attribute("src")
    except:
        image = None

    # Ad detection
    try:
        ad = p.find_element(By.XPATH, ".//span[text()='Sponsored']")
        ad_type = "Ad"
    except:
        ad_type = "Organic"

    data.append([title, price, rating, image, ad_type])

df = pd.DataFrame(data, columns=["Title", "Price", "Rating", "Image", "Type"])

filename = f"amazon_laptops_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df.to_csv(filename, index=False)

driver.quit()