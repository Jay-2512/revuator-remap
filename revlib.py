# import statements
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs
from flask import flash

# load environment variables
load_dotenv()

user_agent = os.getenv("USER_AGENT")
accpt_lang = os.getenv("ACCEPT_LANGUAGE")
HEADERS = ({'User-Agent': user_agent, 'Accept-Language': accpt_lang})


class GetURL:
    def get_FLIP(product_name):

        error_flag = False

        flip_template_url = f"http://www.flipkart.com/search?q={product_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&sort=relevance"
        r = requests.get(flip_template_url, headers=HEADERS)

        if (r.status_code == 200):
            print("LOG: Connection Successful")
            soup = bs(r.content, 'html.parser')

            # get the first product url
            product_element = soup.find('a', {'class': '_1fQZEK'})
            try:
                product_url = 'http://www.flipkart.com' + \
                    product_element.get('href')
                return product_url, error_flag
            except:
                error_flag = True
                return None, error_flag
        else:
            print("LOG: Failed to connect to Flipkart")
            error_flag = True
            return None, error_flag

    def get_AMZN(product_name):

        error_flag = False

        amzn_template_url = f"https://www.amazon.in/s?k={product_name}&ref=nb_sb_noss_1"
        r = requests.get(amzn_template_url, headers=HEADERS)

        if (r.status_code == 200):
            print("LOG: Connection Successful")
            soup = bs(r.content, 'html.parser')
            product_element = soup.find(
                "div", {"data-component-type": "s-search-result"})
            try:
                product_url = "https://www.amazon.in" + \
                    product_element.find(
                        "a", {"class": "a-link-normal"})["href"]
                return product_url, error_flag
            except:
                error_flag = True
                return None, error_flag
        else:
            print("LOG: Failed to connect to Amazon")
            error_flag = True
            return None, error_flag


class GetAMZ:

    def get_basic_info(amzn_url):
        try:
            r = requests.get(amzn_url, headers=HEADERS)
            if (r.status_code == 200):
                print("LOG: [FLIP] Connection Successful")
                html_data = r.text
                soup = bs(html_data, 'html.parser')
                # get product name
                try:
                    for item in soup.find_all("span", class_="a-size-large product-title-word-break"):
                        product_name = item.get_text()
                except Exception as e:
                    print("LOG: [AMZN] Error in getting product name")
                    product_name = "Not Available"
                # get product price
                try:
                    price_element = soup.find('span', class_='a-offscreen')
                    product_price = price_element.get_text()
                except Exception as e:
                    print("LOG: [AMZN] Error in getting product price")
                    product_price = "Not Available"
                # get product image
                try:
                    img_element = soup.find("div", class_="imgTagWrapper")
                    product_image = img_element.find(
                        "img", class_="a-dynamic-image a-stretch-vertical").get('src')
                except Exception as e:
                    print("LOG: [AMZN] Error in getting product image")
                    product_image = "Not Available"

                    return [product_name, product_price, product_image]
        except Exception as e:
            print("LOG: [AMZN] Error in getting basic info")
            product_name = "Not Available"
            product_price = "Not Available"
            product_image = "Not Available"
            return [product_name, product_price, product_image]


class GetFLIP:

    def get_basic_info(flip_url):
        try:
            r = requests.get(flip_url, headers=HEADERS)
            if (r.status_code == 200):
                print("LOG: [FLIP] Connection Successful")
                html_data = r.text
                soup = bs(html_data, 'html.parser')
                # get product name
                try:
                    for item in soup.find_all("span", class_="B_NuCI"):
                        product_name = item.get_text()
                except Exception as e:
                    print("LOG: [FLIP] Error in getting product name")
                    product_name = "Not Available"
                # get product price
                try:
                    price_element = soup.find('div', class_="_30jeq3 _16Jk6d")
                    product_price = price_element.get_text()
                except Exception as e:
                    print("LOG: [FLIP] Error in getting product price")
                    product_price = "Not Available"
                # get product image
                try:
                    product_image = soup.find("img",
                                              class_="_396cs4 _2amPTt _3qGmMb").get("src")
                except Exception as e:
                    print("LOG: [FLIP] Error in getting product image")
                    product_image = "Not Available"
                return [product_name, product_price, product_image]
        except Exception as e:
            print("LOG: [FLIP] Error in getting basic info")
            product_name = "Not Available"
            product_price = "Not Available"
            product_image = "Not Available"
            return [product_name, product_price, product_image]
