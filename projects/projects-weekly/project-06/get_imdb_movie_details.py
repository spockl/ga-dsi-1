# import relevant libraries

# basic libraries
import pandas as pd
import numpy as np

# data collection libraries
from selenium import webdriver
import bs4
import json

# path to phantomjs
phan_path = '//Applications/phantomjs'

# url templates
low_ratings = 'http://www.imdb.com/search/title?genres={}&title_type=feature&sort=user_rating,asc&page={}&ref_=adv_nxt'
high_ratings = 'http://www.imdb.com/search/title?genres={}&title_type=feature&sort=user_rating,desc&page={}&ref_=adv_nxt'
high_num = 'http://www.imdb.com/search/title?genres={}&title_type=feature&sort=num_votes,desc&page={}&ref_=adv_nxt'
low_num = 'http://www.imdb.com/search/title?genres={}&title_type=feature&sort=num_votes,asc&page={}&ref_=adv_nxt'
main_url = 'http://www.imdb.com/title/{}/'
summary_url = 'http://www.imdb.com/title/{}/plotsummary?ref_=tt_stry_pl'
keywords_url = 'http://www.imdb.com/title/{}/keywords?ref_=tt_stry_kw'

# variables
all_genres = []
all_ids = []
url_list = [low_ratings, high_ratings, high_num, low_num]


def create_driver():
    return webdriver.PhantomJS(executable_path=phan_path)

def get_genre_list():
    driver = create_driver()
    driver.get('http://www.imdb.com/genre/')
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
    genre_list = []
    for i in soup.findAll('a'):
        try:
            if 'genre/' in i['href'] and 'genre/?' not in i['href'] and i.find('span'):
                genre_list.append(i.text.split()[0])
        except:
            pass
    return genre_list

def get_id(genre, target_url,page):
    driver = create_driver()
    driver.get(target_url.format(genre, page))
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
    ids = []
    for i in soup.findAll('a'):
        try:
            if 'title/tt' in i['href'] and 'http' not in i['href']:
                try:
                    for j in i['href'].split('/'):
                        if 'tt' in j and '_' not in j:
                            ids.append(j.strip())
                except:
                    pass
        except:
            pass
    return ids

def get_title(id_num):
    driver = create_driver()
    driver.get(main_url.format(id_num))
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

    # Get title of the movie
    try:
        title = soup.find('title').text
    except:
        title = ''

    return title

def get_genres(id_num):
    driver = create_driver()
    driver.get(main_url.format(id_num))
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

    # Get genre(s) of the movie
    genres = []
    for i in soup.find('div', class_='subtext').findAll('span', itemprop='genre'):
        genres.append(i.text)
    genres = ' '.join(genres)

    return genres

def get_rating(id_num):
    driver = create_driver()
    driver.get(main_url.format(id_num))
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

    # Get rating of the movie
    try:
        rating = soup.find('div', class_='ratingValue').find('strong')['title'].split()[0]
    except:
        rating = ''

    return rating

def get_num_rating(id_num):
    driver = create_driver()
    driver.get(main_url.format(id_num))
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

    # Get number of user ratings
    try:
        num_rating = soup.find('div', class_='ratingValue').find('strong')['title'].split()[-3]
    except:
        num_rating = ''

    return num_rating

def get_length(id_num):
    driver = create_driver()
    driver.get(main_url.format(id_num))
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

    # Get length of movie
    try:
        length = soup.find('div', class_='subtext').find('time').text.strip()
    except:
        length = ''

    return length

def get_cert(id_num):
    driver = create_driver()
    driver.get(main_url.format(id_num))
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

    # Get certification
    try:
        certification = soup.find('span', itemprop='contentRating').text
    except:
        certification = ''

    return certification

def get_directors(id_num):
    driver = create_driver()
    driver.get(main_url.format(id_num))
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

    # Get directors, names are linked by underscores
    directors = []
    for j in soup.findAll('div', class_='credit_summary_item'):
        if 'Direct' in j.find('h4').text:
            for i in j.findAll('span', itemprop='name'):
                directors.append('_'.join(i.text.split()))
    directors = ' '.join(directors)

    return directors

def get_writers(id_num):
    driver = create_driver()
    driver.get(main_url.format(id_num))
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

    # Get writers, names are linked by underscores
    writers = []
    for j in soup.findAll('div', class_='credit_summary_item'):
        if 'Writ' in j.find('h4').text:
            for i in j.findAll('span', itemprop='name'):
                writers.append('_'.join(i.text.split()))
    writers = ' '.join(writers)
    return writers

def get_stars(id_num):
    driver = create_driver()
    driver.get(main_url.format(id_num))
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

    # Get stars, names are linked by underscores
    stars = []
    for j in soup.findAll('div', class_='credit_summary_item'):
        if 'Star' in j.find('h4').text:
            for i in j.findAll('span', itemprop='name'):
                stars.append('_'.join(i.text.split()))
    stars = ' '.join(stars)
    return stars

def get_plot(id_num):
    driver = create_driver()
    driver.get(main_url.format(id_num))
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

    # Get one-liner for the movie
    plot = []
    plot.append(soup.find('div', class_='summary_text').text.strip())

    driver = create_driver()
    driver.get(summary_url.format(id_num))
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
    for j in soup.findAll('p', class_='plotSummary'):
        plot.append(j.text.strip())
    plot = ' '.join(plot)
    return plot

def get_keywords(id_num):
    driver = create_driver()
    driver.get(keywords_url.format(id_num))
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
    keywords = []
    for j in soup.findAll('div', class_='sodatext'):
        keywords.append('_'.join(j.text.strip().split()))
    keywords = ' '.join(keywords)

    return keywords

all_genres = get_genre_list()

for i in all_genres:
    print i
    for j in range(len(url_list)):
        for k in [1,15]:
            id_l = get_id(i,url_list[j],k)
            print j, k, len(id_l)
            all_ids.extend(id_l)

all_ids = set(all_ids)

df = pd.DataFrame(all_ids, columns=['id'])

df['title'] = df['id'].map(get_title)

df.to_csv('titles.csv')

df['genre'] = df['id'].map(get_genres)

df.to_csv('genres.csv')
