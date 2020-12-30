# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo 
import scrape_mars
import pymongo
import os

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Scrape Route to Import `scrape_mars.py` Script & Call `scrape` Function
@app.route("/scrape")
def scrapper():
    mars = mongo.db.mars
    
    mars_data = scrape_mars.scrape()

    # for debugging app without refreshing scrape
    # mars_data = {'news_title': "A Martian Roundtrip: NASA's Perseverance Rover Sample Tubes", 'news_description': "Marvels of engineering, the rover's sample tubes must be tough enough to safely bring Red Planet samples on the long journey back to Earth in immaculate condition. ", 'featured_image': 'https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA17563-1920x1200.jpg', 'facts': '<table border="1" class="dataframe">\n  <tbody>\n    <tr>\n      <td>Equatorial Diameter:</td>\n      <td>6,792 km</td>\n    </tr>\n    <tr>\n      <td>Polar Diameter:</td>\n      <td>6,752 km</td>\n    </tr>\n    <tr>\n      <td>Mass:</td>\n      <td>6.39 × 10^23 kg (0.11 Earths)</td>\n    </tr>\n    <tr>\n      <td>Moons:</td>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <td>Orbit Distance:</td>\n      <td>227,943,824 km (1.38 AU)</td>\n    </tr>\n    <tr>\n      <td>Orbit Period:</td>\n      <td>687 days (1.9 years)</td>\n    </tr>\n    <tr>\n      <td>Surface Temperature:</td>\n      <td>-87 to -5 °C</td>\n    </tr>\n    <tr>\n      <td>First Record:</td>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <td>Recorded By:</td>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>', 'hemisphere_images': []}

    mars.update({}, mars_data, upsert=True)
    return "Refresh complete. Please return to the previous page and hit refresh."

# Define Main Behavior
if __name__ == "__main__":
    # app.run(debug=True)
    app.run()
    