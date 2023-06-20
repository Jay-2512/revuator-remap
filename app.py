# import statements
import time

from itertools import chain
from flask import Flask, render_template, request, flash
from revlib import GetURL as GU
from revlib import GetAMZ as GA
from revlib import GetFLIP as GF
from revlib import GetREV as GR
from nlplib import ReviewAnalyzer as RA

# global variables
url = ""
main_review_list = []
amzn_url = ""
flip_url = ""

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

# dashboard route


@app.route("/dashboard", methods=['POST'])
def dashboard():
    product_name = request.form.get("search")

    # global variables
    global amzn_url
    global flip_url

    # get flipkart url
    flip_url, flip_error = GU.get_FLIP(product_name)
    # get amazon url
    amzn_url, amzn_error = GU.get_AMZN(product_name)

    # check for errors
    if flip_error:
        print("LOG: Flipkart Error")
        return render_template('search.html')
    elif amzn_error:
        print("LOG: Amazon Error")
        return render_template('search.html')
    else:
        print("URL Fetching Complete")
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

        # get main reviews
        global main_review_list

        main_review_list.append(GR.get_amz_main_reviews(amzn_url))
        main_review_list.append(GR.get_flip_main_reviews(flip_url))

        # JSON data to be sent to the dashboard
        product_data = {
            "productName": amzn_details[0],
            "productPrice": lowest_price,
            "productSite": low_price_site,
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

    return render_template('analysis.html', sentiment=sentiment, img_path=img_path)


# run app
if __name__ == "__main__":
    app.secret_key = 'AANISND12313'
    app.run(debug=True)
