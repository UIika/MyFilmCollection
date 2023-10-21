import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from db import Movie
from PIL import Image

HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'Accept-Language': 'en-US',
}

engine = create_engine('sqlite:///instance/moviesdb.db')
session = sessionmaker(bind=engine)()

def img_download(url):
    img_data = requests.get(url).content
    path = 'static/images/' + url.split('/')[-1]
    with open(path, 'wb') as handler:
        handler.write(img_data)
    foo = Image.open(path)
    foo = foo.resize((int(foo.width/3),int(foo.height/3)),Image.LANCZOS)
    foo.save(path, quality=95)
    foo.save(path, optimize=True, quality=95)
    
    return path

def parse_movie(film_id):
    try:
        response = requests.get(f'https://www.imdb.com/title/tt{film_id}/', headers=HEADERS)
        soup = BeautifulSoup(response.text, 'lxml')

        title = soup.find('meta', property='og:title')['content'].split('|')[0][:-13].strip()
        year = int(soup.find('title').text[-12:-8])
        genres = soup.find('meta', property='og:title')['content'].split('|')[1].strip()
        directors = ', '.join([s.text for s in soup.find('li', class_='ipc-metadata-list__item').\
                                                    find_all('li', class_='ipc-inline-list__item')])
        image_url = soup.find('meta', property='og:image')['content']
        rating = float(soup.find('span', class_='sc-bde20123-1 iZlgcd').text)

        movie = Movie(title=title,
                        year=year,
                        genres=genres,
                        directors=directors,
                        image=img_download(image_url),
                        imdb_rating=rating)
        try:
            session.add(movie)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
    except:
        print(film_id)

def start(file_source):
    with open(file_source, 'r') as f:
        for id in f.readlines():
            parse_movie(id.strip())


if __name__ == '__main__':
    start('films_ids.txt')