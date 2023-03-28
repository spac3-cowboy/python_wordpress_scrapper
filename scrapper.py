import requests
import mysql.connector
from bs4 import BeautifulSoup

#Connect to MySQL database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="wp_scrapper"
)

#Create a cursor object to execute SQL queries
cursor = db.cursor()

#Send HTTP request to get JSON response of all posts
url = "https://any-wordpress-website.com/wp-json/wp/v2/posts?per_page=100"
response = requests.get(url)
data = response.json()

#Loop through all posts and insert title and content into database
for post in data:
    post_title = BeautifulSoup(post["title"]["rendered"], "html.parser").get_text(strip=True)
    post_content = BeautifulSoup(post["content"]["rendered"], "html.parser").get_text(strip=True)
    sql = "INSERT INTO bangla (title, content) VALUES (%s, %s)"
    values = (post_title, post_content)
    cursor.execute(sql, values)
    db.commit()

#Close database connection
db.close()

print("Data inserted into the database successfully.")