READ ME

Notes:
 - please save chromedriver.exe to your root folder or update the location in scrape_mars.py and Mission to Mars.ipynb
 - adjust the wait time parameter if you get empty objects (websites loading javascripts too slowly or slow internet)
 - you should have a mongodb database created called mars_app, it does not need to have a collection pre-loaded into it

Overview:
 - the scrape_mars.py script scrapes 4 websites for Mars-related news, facts, and images
 - the code is called in a Flask app (app.py) that creates a website that summarizes the information
 - the template files for the website are saved in the templates folder (along with a css stylesheet)

To run, launch the app.py and navigate to the localhost webpage (likely http://127.0.0.1:5000/)
