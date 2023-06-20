# import statements
import time

from flask import Flask, render_template, request, flash
from revlib import GetURL as GU
from revlib import GetAMZ as GA
from revlib import GetFLIP as GF

# global variables
url = ""

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
        # amzn_details = GA.get_basic_info(amzn_url)
        time.sleep(1)
        # get flipkart details
        # flip_details = GF.get_basic_info(flip_url)
        flip_details = []

    return render_template('dashboard.html', params=flip_details)


# run app
if __name__ == "__main__":
    app.secret_key = 'AANISND12313'
    app.run(debug=True)
