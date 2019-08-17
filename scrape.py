import urllib2
import csv
from bs4 import BeautifulSoup

def get_seasons( number_of_seasons ):
    i = 1
    all_seasons = []
    while i < number_of_seasons + 1:
        all_seasons.append(scrape_page(i))
        i += 1
    
    write_seasons(all_seasons)

def scrape_page( season_num ):
    imdb_page = 'https://www.imdb.com/title/tt0096697/episodes?season=%s' % season_num
    request = urllib2.Request(imdb_page, headers={'User-Agent': 'your user-agent'})
    page = urllib2.urlopen(request)
    soup = BeautifulSoup(page, 'html.parser')
    
    episode_list = soup.find('div', attrs={ "class" : "eplist" })
    episodes = episode_list.find_all('div', attrs={ "class" : "list_item"}, recursive=False)

    season_episodes = []
    episode_num = 1
    for episode in episodes:
        title = encode_text(episode.find('a', attrs={'itemprop':'name'}))
        airdate = encode_text(episode.find('div', attrs={'class':'airdate'}))
        description = encode_text(episode.find('div', attrs={'class':"item_description"}))
        image_url = format_image_url(episode.find('img')['src'])
        season_episodes.append([season_num, episode_num, title, airdate, description, image_url])
        episode_num += 1
    
    return season_episodes

def write_seasons( seasons ):
    file = open('simpsons_data.csv', 'wb')
    writer = csv.writer(file)

    writer.writerow(['Season', 'Episode', 'Title', 'Airdate', 'Description', 'Image URL'])
    for episodes in seasons:
        for episode in episodes:
            writer.writerow(episode)
    
    file.close()

def encode_text( txt ):
    return txt.text.strip().encode('utf-8')

def format_image_url( url ):
    return (url.split("_V1_")[0] + "_V1_.jpg").encode('utf-8')

get_seasons(30)