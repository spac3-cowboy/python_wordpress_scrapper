import requests
from bs4 import BeautifulSoup
import re
import pymysql

def connect_to_db():
    # Replace with your actual credentials
    db = pymysql.connect(host="localhost", user="root", password="", database="choti")
    return db

def create_table_if_not_exists(db):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BlogPosts (
            id INT AUTO_INCREMENT,
            title VARCHAR(255),
            details TEXT,
            url VARCHAR(255),
            scraped_at DATETIME,
            PRIMARY KEY (id)
        )
    ''')
    db.commit()

def remove_english_alphabets(text):
    return re.sub('[a-zA-Z]', '', text)

def remove_html_tags(text):
    return re.sub('<[^<]+?>', '', text)

def scrape_single_post(url, db):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1', class_='entry-title', itemprop='headline').text
    details = soup.find('div', class_='entry-content').text

    title = remove_english_alphabets(title)
    details = remove_english_alphabets(details)
    details = remove_html_tags(details)

    cursor = db.cursor()
    print(title)
    sql = "INSERT INTO BlogPosts(TITLE, DETAILS) VALUES ('%s', '%s')" % (title, details)
    cursor.execute(sql)
    db.commit()

def scrape_single_page(url, db):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('h2', class_='entry-title', itemprop='headline')

    for post in posts:
        post_url = post.find('a')['href']
        scrape_single_post(post_url, db)

def get_next_page_url(url):
    page_number = int(url.split('/')[-2]) + 1
    next_page_url = 'https:///page/' + str(page_number) + '/'
    return next_page_url

def scrape_all_pages(start_url):
    db = connect_to_db()
    create_table_if_not_exists(db)
    url = start_url

    while url is not None:
        scrape_single_page(url, db)
        url = get_next_page_url(url)

scrape_all_pages('https:///page/1/')