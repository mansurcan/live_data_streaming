URL = "https://www.amazon.co.uk/"
SEARCH_TERM = "iPhone 13"

XPATH_COOKIES = "//input[@type='submit' and @id='sp-cc-accept']"
XPATH_SEARCH_BOX = "//input[@id='twotabsearchtextbox']"
XPATH_APPLE_BRAND = "//span[text()='Apple']"

# They require .text
data_dict = {"price": ".//span[contains(@class,'a-price-whole')]",
             "sku" : "//span[contains(@class,'a-size-large product-title-word-break')]",
             "tech_properties" : "//ul[contains(@class, 'a-unordered-list a-vertical a-spacing-mini')]",
             "note" : "//div[contains(@id,'apEligibility_feature_div')]",
             "reviews" : "//span[@id='acrCustomerReviewText']",
             "asin" : "//input[contains(@id, 'attach-baseAsin')]"
             }

# They require .get_attribute('src') and .get_attribute('href') 
# "image_link_list" : ".//img[@class='s-image']",

XPATH_IMAGES = "//img[@class='a-dynamic-image a-stretch-vertical'][1]"

# XPATH_IMAGE_LINK = ".//img[@class='s-image']"
XPATH_PRODUCT_LINK = ".//a[@class='a-link-normal s-no-outline']"
XPATH_NEXT_PAGE = "//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']"

