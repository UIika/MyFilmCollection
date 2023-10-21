from .myimdb import HEADERS
from bs4 import BeautifulSoup
from requests import get

def parse_names(start):
    response = get(f'https://www.imdb.com/search/title/?title_type=feature&num_votes=10000,&view=simple&sort=num_votes,desc&start={start}&ref_=adv_nxt', headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    ids = [n.find('a', href=True)['href'].split('/')[2][2:] for n in soup.find_all('div', class_='lister-item mode-simple')]
    
    return ids

def start(file_destination):

    result = [parse_names(i) for i in range(1, 10542, 50)]
    with open(file_destination, 'w') as f:
        for page in result:
            for name in page:
                try:
                    f.write(name + '\n')
                except UnicodeEncodeError:
                    pass

if __name__ == '__main__':
    start('films_ids.txt')

