# import statements
import time

from itertools import chain
from flask import Flask, render_template, request, flash
from colorama import Fore, Back, Style
from revlib import GetURL as GU
from revlib import GetAMZ as GA
from revlib import GetFLIP as GF
from revlib import GetREV as GR
from revlib import RevUtils as RU
from nlplib import ReviewAnalyzer as RA

# global variables
url = ""
main_review_list = []
amzn_url = ""
flip_url = ""
site = ""
is_url = False

# initialize app
app = Flask(__name__)

# routes


@app.route("/")
@app.route("/home")
def index():
    return render_template('home.html')

# seartch route


@app.route("/search")
def search():
    return render_template('search.html')

# search individual sites route


@app.route("/search/product")
def search_product():
    return render_template('product.html')

# dashboard route


@app.route("/dashboard", methods=['POST'])
def dashboard():
    product_name = request.form.get("search")

    # global variables
    global amzn_url
    global flip_url
    global main_review_list
    global site
    global is_url

    is_url, site = RU.check_url(product_name)

    if not is_url:
        # get flipkart url
        flip_url, flip_error = GU.get_FLIP(product_name)
        # get amazon url
        amzn_url, amzn_error = GU.get_AMZN(product_name)

        # check for errors
        if flip_error:
            print(
                f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.BLUE}[FLIP]{Style.RESET_ALL} Flipkart Error")
            return render_template('search.html')
        elif amzn_error:
            print(
                f"{Fore.GREEN}LOG:{Style.RESET_ALL} {Back.YELLOW}[AMZN]{Style.RESET_ALL} Amazon Error")
            return render_template('search.html')
        else:
            # get amazon details
            amzn_details = GA.get_basic_info(amzn_url)
            time.sleep(1)
            # get flipkart details
            flip_details = GF.get_basic_info(flip_url)

            # get the lowest price
            if (amzn_details[1] < flip_details[1]):
                lowest_price = amzn_details[1]
                low_price_site = "amazon.in"
            else:
                lowest_price = flip_details[1]
                low_price_site = "flipkart.com"

            main_review_list.append(GR.get_amz_main_reviews(amzn_url))
            main_review_list.append(GR.get_flip_main_reviews(flip_url))

            # JSON data to be sent to the dashboard
            product_data = {
                "productName": amzn_details[0],
                "productPrice": lowest_price,
                "productSite": low_price_site,
                "productImage": flip_details[2]
            }
    else:
        global url
        if site == "amazon":
            url = product_name
            # get amazon reviews
            amzn_details = GA.get_basic_info(url)

            main_review_list.append(GR.get_amz_main_reviews(url))

            # JSON data to be sent to the dashboard
            product_data = {
                "productName": amzn_details[0],
                "productPrice": amzn_details[1],
                "productSite": "amazon.in",
                "productImage": amzn_details[2]
            }
        elif site == "flipkart":
            url = product_name
            # get flipkart reviews
            flip_details = GF.get_basic_info(url)

            main_review_list.append(GR.get_flip_main_reviews(url))

            # JSON data to be sent to the dashboard
            product_data = {
                "productName": flip_details[0],
                "productPrice": flip_details[1],
                "productSite": "flipkart.com",
                "productImage": flip_details[2]
            }

    return render_template('dashboard.html', params=product_data)


# review route
@app.route("/reviews")
def reviews():
    global main_review_list

    merged_list = list(chain.from_iterable(main_review_list))

    return render_template('reviews.html', review_list=merged_list)

# analysis route


@app.route("/analysis")
def analysis():
    global site
    global is_url
    global url

    if not is_url:
        amz_proc_reviews = GR.get_amz_proc_reviews(amzn_url)
        flip_proc_reviews = GR.get_flip_proc_reviews(flip_url)

        proc_list = amz_proc_reviews + flip_proc_reviews
        sentiment_score = RA.find_sentiment(proc_list)
        RA.generate_word_cloud(proc_list, sentiment_score)

        if sentiment_score == 1:
            sentiment = "Positive"
            img_path = "static/images/positive.jpg"
        elif sentiment_score == 0:
            sentiment = "Neutral"
            img_path = "static/images/neutral.jpg"
        else:
            sentiment = "Negative"
            img_path = "static/images/negative.jpg"
    else:
        if site == "amazon":
            proc_list = GR.get_amz_proc_reviews(url)
            sentiment_score = RA.find_sentiment(proc_list)
            RA.generate_word_cloud(proc_list, sentiment_score)
            if sentiment_score == 1:
                sentiment = "Positive"
                img_path = "static/images/positive.jpg"
            elif sentiment_score == 0:
                sentiment = "Neutral"
                img_path = "static/images/neutral.jpg"
            else:
                sentiment = "Negative"
                img_path = "static/images/negative.jpg"
        elif site == "flipkart":
            proc_list = GR.get_flip_proc_reviews(url)
            sentiment_score = RA.find_sentiment(proc_list)
            RA.generate_word_cloud(proc_list, sentiment_score)
            if sentiment_score == 1:
                sentiment = "Positive"
                img_path = "static/images/positive.jpg"
            elif sentiment_score == 0:
                sentiment = "Neutral"
                img_path = "static/images/neutral.jpg"
            else:
                sentiment = "Negative"
                img_path = "static/images/negative.jpg"
        else:
            return render_template('search.html')

    return render_template('analysis.html', sentiment=sentiment, img_path=img_path)


# run app
if __name__ == "__main__":
    app.secret_key = 'AANISND12313'
    app.run(debug=True)
