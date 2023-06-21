import re
import nltk
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem.wordnet import WordNetLemmatizer
from colorama import Fore, Back, Style
from nltk.corpus import stopwords


class ReviewAnalyzer:
    def __init__(self):
        print("LOG: Downloading Prerequisites")
        nltk.download('vader_lexicon')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('omw-1.4')

    def find_sentiment(review_list):
        # TF-IDF vectorizer
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(review_list)

        sia = SentimentIntensityAnalyzer()

        sentiment_scores = []
        for i in range(len(review_list)):
            review = review_list[i]

            # Get TF-IDF representation of the current review
            review_tfidf = tfidf_matrix[i]

            # Calculate sentiment score based on TF-IDF weights
            sentiment = sia.polarity_scores(review)
            print(sentiment)
            sentiment_score = sentiment['compound']
            print(sentiment_score)
            weighted_sentiment_score = sentiment_score * np.sum(review_tfidf)
            print(weighted_sentiment_score)
            sentiment_scores.append(weighted_sentiment_score)

        # Calculate the average sentiment score
        average_sentiment_score = sum(sentiment_scores) / len(sentiment_scores)

        # Set a threshold for classifying reviews as positive or negative
        threshold = 0.1

        # Calculate the percentage of positive and negative reviews
        positive_reviews_percentage = len(
            [score for score in sentiment_scores if score > threshold]) / len(sentiment_scores) * 100
        negative_reviews_percentage = len(
            [score for score in sentiment_scores if score < -threshold]) / len(sentiment_scores) * 100

        print(
            f"LOG: {Back.WHITE}[SYSTEM]{Style.RESET_ALL} Positive Sentiment Score: {positive_reviews_percentage}")
        print(
            f"LOG: {Back.WHITE}[SYSTEM]{Style.RESET_ALL} Negative Sentiment Score: {negative_reviews_percentage}")

        if average_sentiment_score > threshold:
            return [1, positive_reviews_percentage, negative_reviews_percentage]
        elif average_sentiment_score < -threshold:
            return [-1, positive_reviews_percentage, negative_reviews_percentage]
        else:
            return [0, positive_reviews_percentage, negative_reviews_percentage]

    def generate_word_cloud(review_list, sentiment):
        sentiment_words = []

        custom_stopwords = [
            'product', 'android', 'iphone', 'much', 'buy', 'purchase', 'seller', 'amazon', 'flipkart', 'website', 'online', 'store',
            'shop', 'customer', 'review', 'rating', 'recommend', 'quality', 'price', 'value', 'money',
            'shipping', 'delivery', 'packaging', 'order', 'item', 'size', 'color', 'brand', 'return',
            'refund', 'exchange', 'warranty', 'service', 'experience', 'satisfied', 'dissatisfied',
            'happy', 'unhappy', 'impressed', 'disappointed', 'expectation', 'expect', 'surprise',
            'recommendation', 'purchase', 'buyer', 'seller', 'rating', 'feedback', 'opinion', 'impression',
            'performance', 'transaction', 'deal', 'authentic', 'genuine', 'authenticity', 'original',
            'counterfeit', 'fake', 'defective', 'broken', 'damaged', 'excellent', 'good', 'average',
            'poor', 'best', 'worst', 'value for money', 'user-friendly', 'easy to use', 'durability',
            'customer support', 'customer service', 'responsive', 'prompt', 'fast', 'slow', 'timely',
            'quick', 'reliable', 'disclaimer', 'warranty', 'guarantee', 'return policy', 'shipping policy',
            'price range', 'size chart', 'color options', 'brand reputation', 'packaging quality',
            'delivery speed', 'shopping experience', 'customer feedback', 'product description',
            'product image', 'positive', 'negative', 'neutral', 'happy customer', 'unhappy customer',
            'customer satisfaction', 'recommendable', 'popular', 'trending', 'bestselling', 'new arrival',
            'limited stock', 'discount', 'offer', 'deal', 'promotion', 'sale', 'clearance', 'bargain',
            'shopping cart', 'checkout', 'payment', 'payment options', 'credit card', 'debit card',
            'net banking', 'cash on delivery', 'user review', 'verified purchase', 'product rating',
            'star rating', 'comment', 'testimonial', 'product comparison', 'product feature',
            'product specification', 'product performance', 'product usage', 'product benefit',
            'product drawback', 'product pros', 'product cons', 'product recommendation', 'product hype',
            'product popularity', 'product demand', 'product availability', 'product unavailability',
            'product stock', 'product inventory', 'product update', 'product version', 'product variant',
            'product enhancement', 'product improvement', 'product innovation', 'product launch',
            'product trend', 'product analysis', 'product comparison', 'product research',
            'product selection', 'product variety', 'product assortment', 'product category',
            'product niche', 'product market', 'product purchase', 'product lifecycle', 'product lifespan',
            'product longevity', 'product investment', 'product value', 'product upgrade', 'product downgrade',
            'product replacement', 'product upgradation', 'product recall', 'product warranty',
            'product authenticity', 'product testing', 'product feedback', 'product maintenance',
            'product recommendation', 'product popularity', 'product promotion', 'product advertisement']

        stop_words = set(stopwords.words('english')
                         ).union(set(custom_stopwords))

        sia = SentimentIntensityAnalyzer()

        for review in review_list:
            review = re.sub("[^A-Za-z]+", " ", review).lower()
            review = re.sub("[0-9]+", " ", review)
            rev_tkns = review.split()
            wordnet = WordNetLemmatizer()
            rev_tkns = [wordnet.lemmatize(
                word) for word in rev_tkns if word not in stop_words]
            sentiment_words.extend(rev_tkns)

        sentiment_words_str = " ".join(sentiment_words)

        # Analyze sentiment of the sentiment words
        sentiment_scores = sia.polarity_scores(sentiment_words_str)

        # Extract positive and negative words based on sentiment scores
        positive_words = [word for word,
                          score in sentiment_scores.items() if score > 0]
        negative_words = [word for word,
                          score in sentiment_scores.items() if score < 0]

        # Filter sentiment words based on sentiment type
        if sentiment == 1:
            filtered_words = [
                word for word in sentiment_words if word not in negative_words]
        elif sentiment == -1:
            filtered_words = [
                word for word in sentiment_words if word not in positive_words]
        else:
            filtered_words = [word for word in sentiment_words if word not in (
                positive_words + negative_words)]

        filtered_words_str = " ".join(filtered_words)

        # Generate word cloud based on sentiment words
        wordcloud = WordCloud(
            width=500, height=500, background_color='white').generate(sentiment_words_str)

        # save the word cloud
        wordcloud.to_file('static/output/wordcloud.png')
