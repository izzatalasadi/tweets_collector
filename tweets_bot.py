import random
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Twitter_hashtags_crawler:
    def __init__(self):
        # Set options for Chrome browser
        op = Options()
        # For Mac or Linux, set to fullscreen mode
        op.add_argument("--kiosk")

        # Set Chrome driver service using webdriver_manager
        s = Service(ChromeDriverManager().install())
        # Start the Chrome browser
        self.driver = webdriver.Chrome(service=s, options=op)
        # Initialize a list to store visited hashtags
        self.visited_hashtag = []

    # Define a method to close the Chrome browser
    def __del__(self):
        self.driver.close()

    def visit_twitter_page(self, url):
        # Load the page in the browser
        self.driver.get(url)
        try:
            # Wait for the tweet feeds to load in the browser
            tweets = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[@class='css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']")
                ))
            # Return a list of text content for each tweet
            return [tweet.text for tweet in tweets]
        except TimeoutException:
            # If the page doesn't load in time, return None
            print("Timed out waiting for page to load")
            return None

    # Define a method to collect hashtags from a Twitter page
    def collect_hashtags(self, url):
        # Load the page in the browser
        self.driver.get(url)
        # Wait for the hashtags to load in the browser
        hashtags_links = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@class='css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-1bymd8e r-bcqeeo r-qvutc0' and @dir='ltr']//span")))
        # Extract text content from each hashtag link
        hashtags = [str(tag.text).replace("#", "").replace(" ","") for tag in hashtags_links]
        # Return a list of hashtags
        return hashtags

    # Define a method to randomly select a hashtag from a list of hashtags
    def select_random_hashtag(self, hashtags):
        # Filter out hashtags that have been visited before
        available_hashtags = [
            h for h in hashtags if h not in self.visited_hashtag]
        # If all hashtags have been visited before, reset the list of visited hashtags
        if not available_hashtags:
            # reset the list of chosen hashtags if all of them have been visited
            self.visited_hashtag.clear()
            available_hashtags = hashtags
        # Randomly select a hashtag from the available list
        random_hashtag = random.choice(available_hashtags)
        self.visited_hashtag.append(random_hashtag)
        # Return the selected hashtag
        return random_hashtag

    # Define a method to visit
    def visit_hashtag(self, hashtag):
        url = f"https://twitter.com/search?q=%23{hashtag}&src=typed_query&f=live"
        tweets = self.visit_twitter_page(url)
        return tweets

    # Print tweets
    def print_tweets(self, tweets, hashtag):
        print(
            f"==============================\nTweets for #{hashtag}:\n==============================")
        if tweets:
            for i, t in enumerate(tweets):
                print(
                    f"Tweet(#{hashtag})-{i+1}:\n{t}\n--------------------------------")
        else:
            print(f"No tweets found for #{hashtag}\n")

    # Run the code
    def run(self, url, max_pages=6):
        hashtags = self.collect_hashtags(url)
        if hashtags:
            for _ in range(max_pages):
                random_tag = self.select_random_hashtag(hashtags)
                tweets = self.visit_hashtag(random_tag)
                self.print_tweets(tweets, random_tag)
            time.sleep(0.1)


bot = Twitter_hashtags_crawler()
url = 'https://twitter.com/i/trends'
bot.run(url)
