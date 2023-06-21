# import statements
from colorama import Fore, Back, Style
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


class RevUtils:
    def check_url(url):
        is_valid = False
        site = ""
        # Check if input is url or not and check if it contains amazon or flipkart
        if url.startswith("https://") or url.startswith("http://"):
            is_valid = True
            url_list = url.split("/")
            # check if www.amazon.in in url_list
            if "www.amazon.in" in url_list:
                site = "amazon"
            # check if www.flipkart.com in url_list
            elif "www.flipkart.com" in url_list:
                site = "flipkart"
            else:
                is_valid = False
        else:
            is_valid = False

        return [is_valid, site]


class GetURL:
    def get_FLIP(product_name):

        error_flag = False

        flip_template_url = f"http://www.flipkart.com/search?q={product_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&sort=relevance"
        r = requests.get(flip_template_url, headers=HEADERS)

        if (r.status_code == 200):
            print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.WHITE}[SYSTEM]{Style.RESET_ALL} Connection Successful")
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
            print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.WHITE}[SYSTEM]{Style.RESET_ALL} Failed to find products on both sites")
            error_flag = True
            return None, error_flag

    def get_AMZN(product_name):

        error_flag = False

        amzn_template_url = f"https://www.amazon.in/s?k={product_name}&ref=nb_sb_noss_1"
        r = requests.get(amzn_template_url, headers=HEADERS)

        if (r.status_code == 200):
            print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.YELLOW}[AMZN]{Style.RESET_ALL} Connection Successful")
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
            print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.YELLOW}[AMZN]{Style.RESET_ALL} Failed to connect to Amazon")
            error_flag = True
            return None, error_flag


class GetAMZ:
    def get_basic_info(amzn_url):
        try:
            r = requests.get(amzn_url, headers=HEADERS)
            if (r.status_code == 200):
                print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.YELLOW}[AMZN]{Style.RESET_ALL} Connection Successful")
                html_data = r.text
                soup = bs(html_data, 'html.parser')
                # get product name
                try:
                    for item in soup.find_all("span", class_="a-size-large product-title-word-break"):
                        product_name = item.get_text()
                except Exception as e:
                    print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.YELLOW}[AMZN]{Style.RESET_ALL} Error in getting product name")
                    product_name = "Not Available"
                # get product price
                try:
                    price_element = soup.find('span', class_='a-offscreen')
                    product_price = price_element.get_text()
                except Exception as e:
                    print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.YELLOW}[AMZN]{Style.RESET_ALL} Error in getting product price")
                    product_price = "Not Available"
                # get product image
                try:
                    image_element = soup.find('div', id='imgTagWrapperId')
                    product_image = image_element.find('img')['src']
                except Exception as e:
                    print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.YELLOW}[AMZN]{Style.RESET_ALL} Error in getting product image")
                    product_image = "Not Available"

                return [product_name, product_price, product_image]
        except Exception as e:
            print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.YELLOW}[AMZN]{Style.RESET_ALL} Error in getting basic info")
            product_name = "Not Available"
            product_price = "Not Available"
            product_image = "Not Available"
            return [product_name, product_price, product_image]


class GetFLIP:

    def get_basic_info(flip_url):
        try:
            r = requests.get(flip_url, headers=HEADERS)
            if (r.status_code == 200):
                print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.BLUE}[FLIP]{Style.RESET_ALL} Connection Successful")
                html_data = r.text
                soup = bs(html_data, 'html.parser')
                # get product name
                try:
                    for item in soup.find_all("span", class_="B_NuCI"):
                        product_name = item.get_text()
                except Exception as e:
                    print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.BLUE}[FLIP]{Style.RESET_ALL} Error in getting product name")
                    product_name = "Not Available"
                # get product price
                try:
                    price_element = soup.find('div', class_="_30jeq3 _16Jk6d")
                    product_price = price_element.get_text()
                except Exception as e:
                    print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.BLUE}[FLIP]{Style.RESET_ALL} Error in getting product price")
                    product_price = "Not Available"
                # get product image
                try:
                    product_image = soup.find("img",
                                              class_="_396cs4 _2amPTt _3qGmMb").get("src")
                except Exception as e:
                    print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.BLUE}[FLIP]{Style.RESET_ALL} Error in getting product image")
                    product_image = "Not Available"
                return [product_name, product_price, product_image]
        except Exception as e:
            print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.BLUE}[FLIP]{Style.RESET_ALL} Error in getting basic info")
            product_name = "Not Available"
            product_price = "Not Available"
            product_image = "Not Available"
            return [product_name, product_price, product_image]


class GetREV:
    def get_amz_main_reviews(amzn_url):
        try:
            r = requests.get(amzn_url, headers=HEADERS)
            if (r.status_code == 200):
                review_list = []
                print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.YELLOW}[AMZN]{Style.RESET_ALL} Connection Successful")
                html_data = r.text
                soup = bs(html_data, 'html.parser')
                # get product reviews
                try:
                    for review in soup.find_all("div", class_="a-expander-content reviewText review-text-content a-expander-partial-collapse-content"):
                        for span in review:
                            review_list.append(span.text)

                    for each_elmt in review_list:
                        if each_elmt == "" or each_elmt == " " or each_elmt == '\n':
                            review_list.remove(each_elmt)
                except Exception as e:
                    print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.YELLOW}[AMZN]{Style.RESET_ALL} Error in getting product reviews")
                    review_list = ["Not Available"]

                return review_list
        except Exception as e:
            print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.YELLOW}[AMZN]{Style.RESET_ALL} Error in getting product reviews")
            review_list = ["Not Available"]
            return review_list

    def get_flip_main_reviews(flip_url):
        try:
            r = requests.get(flip_url, headers=HEADERS)
            if (r.status_code == 200):
                review_list = []
                print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.BLUE}[FLIP]{Style.RESET_ALL} Connection Successful")
                html_data = r.text
                soup = bs(html_data, 'html.parser')
                # get product reviews
                try:
                    for review in soup.find_all("div", class_="t-ZTKy"):
                        for span in review:
                            review_list.append(span.text)

                    for each_elmt in review_list:
                        if each_elmt == "" or each_elmt == " " or each_elmt == '\n':
                            review_list.remove(each_elmt)
                except Exception as e:
                    print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.BLUE}[FLIP]{Style.RESET_ALL} Error in getting product reviews")
                    review_list = ["Not Available"]

                return review_list
        except Exception as e:
            print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.BLUE}[FLIP]{Style.RESET_ALL} Error in getting product reviews")
            review_list = ["Not Available"]
            return review_list

    def get_amz_proc_reviews(amz_url):
        try:
            r = requests.get(amz_url, headers=HEADERS)
            if (r.status_code == 200):
                html_data = r.text
                soup = bs(html_data, 'html.parser')
                # get product reviews
                try:
                    review_list = []
                    main_reviews = []
                    for item in soup.find_all("a", class_="a-link-emphasis a-text-bold"):
                        new_url = "https://www.amazon.in" + item['href']

                    for i in range(1, 5):
                        proc_url = new_url + "&pageNumber=" + str(i)

                        r = requests.get(proc_url, headers=HEADERS)
                        if (r.status_code == 200):
                            print(
                                f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.YELLOW}[AMZN]{Style.RESET_ALL} Connection Successful to page " + str(i))
                            reviews = soup.find_all(
                                "div", {"data-hook": "review-collapsed"})
                            for i in range(len(reviews)):
                                review_list.append(reviews[i].text)

                            main_reviews += review_list
                        else:
                            print(
                                f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.YELLOW}[AMZN]{Style.RESET_ALL} Connection Failed to page " + str(i))
                            main_reviews = ["Not Available"]
                    proc_url = new_url
                except Exception as e:
                    print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.YELLOW}[AMZN]{Style.RESET_ALL} Error in getting product reviews")
                    main_reviews = ["Not Available"]
            else:
                print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.YELLOW}[AMZN]{Style.RESET_ALL} Connection Failed")
                main_reviews = ["Not Available"]

            return main_reviews
        except Exception as e:
            print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.YELLOW}[AMZN]{Style.RESET_ALL} Error in getting product reviews")
            main_reviews = ["Not Available"]
            return main_reviews

    def get_flip_proc_reviews(flip_url):
        try:
            r = requests.get(flip_url, headers=HEADERS)
            if (r.status_code == 200):
                html_data = r.text
                soup = bs(html_data, 'html.parser')
                # get product reviews
                try:
                    review_list = []
                    main_reviews = []

                    rdiv = soup.find("div", class_="col JOpGWq")
                    link_div = rdiv.find_all("a")
                    link = link_div[len(link_div)-1].get("href")
                    new_url = "https://www.flipkart.com" + link

                    for i in range(2, 5):
                        proc_url = new_url + f"&page={str(i)}"

                        response = requests.get(proc_url, headers=HEADERS)
                        if response.status_code == 200:
                            print(
                                f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.BLUE}[FLIP]{Style.RESET_ALL} Connection Successful to page " + str(i))

                            parent_div = soup.find_all("div", class_="t-ZTKy")
                            for divs in parent_div:
                                new_div = divs.find_all("div")
                                for _ in new_div:
                                    new_new = _.find_all("div", class_="")
                                    for __ in new_new:
                                        review_list.append(__.get_text())

                    return review_list

                except Exception as e:
                    print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.BLUE}[FLIP]{Style.RESET_ALL} Error in getting product reviews")
                    main_reviews = ["Not Available"]

        except Exception as e:
            print(f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.BLUE}[FLIP]{Style.RESET_ALL} Error in getting product reviews")
            main_reviews = ["Not Available"]
            return main_reviews
