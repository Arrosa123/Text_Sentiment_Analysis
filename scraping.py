# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import json

def scrape_all():
    # Initiate headless driver for deployment
    print(f'Started at :{dt.datetime.now()}')
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Run all scraping functions and store results in dictionary
    data = {
        "tw_title": "Twitter Trends",
        "tw_trend_loc": "United States",
        "tw_trends" : twitter_trends(browser)
    }

    browser.quit()
    return data 


## Twitter Trends
def twitter_trends(browser):
    # Visit the Mars Hemisphere site
    url = 'https://twitter-trends.iamrohit.in/united-states'
    browser.visit(url)

    # Create a list to hold the images and titles.
    twitter_hashtags = []

    # Retrieve the image urls and titles for each hemisphere.
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        #Use the div tag to return the 4 titles and the anchor tags to the full image pages. 
        hashtags = img_soup.find('tbody', {"id":"copyData"}).find_all(attrs={"class" : "tweet"})

        #Loop through the hemispheres
        hashtag_count = 0
        for hashtag in hashtags:
            hashtag_count = hashtag_count + 1
            if hashtag_count > 10:
                break 
            hashtag_dict = {}
            #assign the title from each description

            #save the retrieved image url and the tile to the hemispheres_dict
            hashtag_dict['hashtag'] = hashtag.contents[0] 
            hashtag_dict['rank'] = hashtag['rank']

            #append the hemispheres_dict to the final list.
            twitter_hashtags.append(hashtag_dict)
    except BaseException as e:
        print(f'Exception in twitter_trends: {e}')
        return None

    #Return the list that holds the dictionary of each image url and title.
    return twitter_hashtags


if __name__ == "__main__":
   print(json.dumps(scrape_all()))