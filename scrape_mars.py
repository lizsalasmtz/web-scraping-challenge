# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time # use this to ensure that javascript elements load completely before soup.find returns empty objects


# chromedriver.exe should be installed to the root folder; if not, update the path
executable_path = {"executable_path":"\chromedriver.exe"} 


# initialize a browser (called from get_soup using 'with' so browser closes automatically after html extracted)
def get_browser():
    b = Browser("chrome", **executable_path, headless=False)    
    return b


def get_soup(url, wait_time):
    # only keep the browser open to get the soup
    with get_browser() as browser:
        browser.visit(url) 
        time.sleep(wait_time)           
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")

    return soup


# get the latest Mars news from https://mars.nasa.gov/news/
# returns a list of dictionaries containing the 'title' of the article and its 'description'
def get_latest_mars_news():
    mars_news_soup = get_soup('https://mars.nasa.gov/news/', 1)

    # -- create empty lists for the articles
    title = []
    description = []

    # -- loop through 'ul' tags with class 'item_list'
    for item in mars_news_soup.find("ul", class_="item_list"):
        
        # -- get the title in the h3 tag 
        title.append(item.find("h3").text)
        
        # -- ... and the description in the 'div' tag with class 'item_list' 
        description.append(item.find("div", class_="article_teaser_body").text)
        
    # only return the first news article (remove [0] to get all)
    return title[0], description[0]


def get_jpl_mars_feature_image_url():
    # get the soup object for the JPL Mars images
    mars_images_soup = get_soup('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars', 1)
    
    # -- get the relative path of the featured image
    image_rel_path = mars_images_soup.find("article", class_="carousel_item")['style']
    
    # -- remove the extra text:"background-image: url(" at the start and "');" at the end 
    image_rel_path = image_rel_path[image_rel_path.find("url('")+5:image_rel_path.find("');")]
    
    # -- add the base URL
    featured_image_url = 'https://www.jpl.nasa.gov' + image_rel_path
    
    return featured_image_url
    

def get_mars_facts():
    facts_url = 'https://space-facts.com/mars/'

    # read the html into pandas
    facts_ds = pd.read_html(facts_url)

    # create a dataframe with the first column of data (Mars) from the table
    facts_df = pd.DataFrame(facts_ds[0])

    # create an HTML string of the table without headers and an index 
    mars_facts_table_html = facts_df.to_html(header = False, index = False)
        
    return mars_facts_table_html

def get_hemispheres():
    hemispheres_soup = get_soup('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars', 5)
    
    hemisphere_image_urls = []
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    for i in hemispheres_soup.find_all('div', class_='item'):
        # open the URL and get soup of the new page 
        item_soup = get_soup(hemispheres_main_url + i.find('a', class_='itemLink product-item')['href'], 5)

        # get the title from the h3 tag
        title = i.find('h3').text

        # get the text of the div tag with class downloads
        download_soup = item_soup.find('div', class_='downloads')

        # get both links from the downloads
        links_soup = download_soup.find_all('a', target='_blank')

        # get the second URL (to the original)
        hemisphere_image_urls.append({'title':title,'img_url':links_soup[1]['href']})

    # return first 4 hemispheres, change [0:3] to get more
    return hemisphere_image_urls[0:3]


# this is the main function that calls all the other functions and returns
# the news, feature image URL, the facts and the hemisphere image URLs and titles
# in one dictionary
def scrape():
    # get the news
    _news_title, _news_description = get_latest_mars_news()
    
    # get the featured image URL
    _featured_img = get_jpl_mars_feature_image_url()
    
    # get the facts HTML table
    _facts = get_mars_facts()
    
    # get the hemisphere image URLs and titles
    _hemispheres = get_hemispheres()
    
    # put everything into one dictionary and return it
    scraped_data = {'news_title':_news_title, 'news_description':_news_description, 'featured_image': _featured_img, 'facts':_facts, 'hemisphere_images':_hemispheres}
    
    return scraped_data
