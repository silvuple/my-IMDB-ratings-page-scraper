import requests
import re
import pandas as pd
from bs4 import BeautifulSoup


my_imdb_ratings = []
base_url = 'https://www.imdb.com'
user_id = ''     # Insert here your 8 digit user id, example '12345678'
next_url = 'https://www.imdb.com/user/ur{}/ratings'.format(user_id)


while True:
    """Get the current page."""
    r = requests.get(next_url)

    """Parse the webpage."""
    soup = BeautifulSoup(r.text, 'html.parser')

    """Find every movie on the page."""
    results = soup.find_all('div', attrs={'class': "lister-item mode-detail"})

    for result in results:
        """Get movie title."""
        title = result.h3.a.text

        """Get year of the movie in the YYYY format."""
        year = result.find('span', attrs={'class': "lister-item-year"}).text
        year = re.search('\d{4}', year)
        year = year.group()

        """Get certificate of the movie if certificate exists."""
        if result.find('span', attrs={'class': "certificate"}):
            certificate = result.find('span', attrs={'class': "certificate"}).text
        else:
            certificate = ""

        """Get runtime of the movie if runtime exists."""
        if result.find('span', attrs={'class': "runtime"}):
            runtime = result.find('span', attrs={'class': "runtime"}).text
        else:
            runtime = ""

        """Get genre of the movie in a clean format if genre exists."""
        if result.find('span', attrs={'class': "genre"}):
            genre = result.find('span', attrs={'class': "genre"}).text
            genre = genre.strip()
        else:
            genre = ""

        """Get total users rating of the movie."""
        rating = result.find_all('span', attrs={'class': "ipl-rating-star__rating"})[0].text

        """Get my rating of the movie."""
        my_rating = result.find_all('span', attrs={'class': "ipl-rating-star__rating"})[1].text

        """Get votes of the movie if votes exists."""
        if result.find('span', attrs={'name':"nv"}):
            votes = result.find('span', attrs={'name':"nv"})['data-value']
        else:
            votes = ""

        """Get director of the movie - the first listed if has several."""
        if result.find('a', href=re.compile("ref_=_li_dr_0")):
            director = result.find('a', href=re.compile("ref_=_li_dr_0")).text
        else:
            director = ""
            
        """Add the movie to the ratings list."""
        my_imdb_ratings.append((title, year, certificate, runtime, genre, rating, my_rating, votes, director))
        
    try:
        """Look for next page url."""
        next_url = base_url + soup.find('a', attrs={'class': "flat-button lister-page-next next-page"})['href']
        
    except TypeError:
        """Break the while loop if next page tag is not found, i.e. last page is reached."""
        break

"""Create DataFrame from the ratings list."""    
df = pd.DataFrame(my_imdb_ratings, columns=['Title', 'Year', 'Certificate', 'Runtime', 'Genre', 'Rating', 'My_rating', 'Votes', 'Director'])

"""Export DataFrame to csv."""
df.to_csv('my_imdb_ratings.csv', index = False)

