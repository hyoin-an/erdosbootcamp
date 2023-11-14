import requests
from collections import Counter
import pandas as pd


url = 'https://api.themoviedb.org/3/'

key = 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4OGJkYWFmYTU3MjNhOGRkMmNjNjhlNDVjNjgyNjRiYiIsInN1YiI6IjY1NDgyZmRiNmJlYWVhMDEyYzhmMGJkZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tam6Qgp_P3HxfAEVUmLD2kl3NJYS0am3zXRSChVfmFM'

header = {   "accept": "application/json",
                "Authorization": key}

class Tmdb():
    def __init__(self,key):
        self.key = key

    def movie_id(self, page : int, category = 'now_playing'):
        """returns the list of id of movies up to the specified pages
        
            page : page number (inclusive)

            category : default is 'now_playing'. Possible values are 

            'now_playing', 'popular', 'top_rated', 'upcoming'
        """
        id_list = []
        for _ in range(1,page+1):
            url = f"https://api.themoviedb.org/3/movie/{category}?language=en-US&page={_}" 

            headers = {
                "accept": "application/json",
                "Authorization": self.key
            }

            response = requests.get(url, headers=headers).json()
            
            for _ in response['results']:
                id_list.append(_['id'])
        return id_list
    
    def movie_details(self, id : int, drop_col = []):
        """
        returns a pd.Series consisting of the movie corresponding to the given id

        id : movie id

        full_details : default is False. When = False, only returns relevant data.
        """
        url = f'https://api.themoviedb.org/3/movie/{id}?language=en-US"'

        headers = {
                "accept": "application/json",
                "Authorization": self.key
            }
        drop_col += ['backdrop_path','adult','imdb_id','video']
        response = requests.get(url, headers=headers).json()
        response = pd.Series(response)
        
        response['keywords'] = self.get_keywords(id)
        response['cast'] = self.get_cast(id)    
        response['directors'] = self.get_director(id)

        response = response.drop(drop_col)
       
        return response
        
        
    def get_cast(self,id, num_casts = 5):
        
        url = f"https://api.themoviedb.org/3/movie/{id}/credits?language=en-US"

        headers = {
                "accept": "application/json",
                "Authorization": self.key
            }
        response = requests.get(url, headers=headers).json()
        response = response['cast']
        response = sorted(response, key = lambda x: x['popularity'], reverse=True)

        cast_name = []
       
        for _ in range(num_casts):
            cast_name.append(response[_]['name'])
            # cast_popularity.append(response[_]['popularity'])
            
        return cast_name
    
    def get_director(self,id):
        
        url = f"https://api.themoviedb.org/3/movie/{id}/credits?language=en-US"

        headers = {
                "accept": "application/json",
                "Authorization": self.key
            }
        response = requests.get(url, headers=headers).json()
        crew = response['crew']

        directors = []
        # cast_popularity =[]
        for _ in crew:
            if _['job'] == 'Director':
                directors.append(_['name'])            
        return directors

    def get_keywords(self, id):

        url = f"https://api.themoviedb.org/3/movie/{id}/keywords"

        headers = {
                "accept": "application/json",
                "Authorization": self.key
            }
        
        response = requests.get(url, headers=headers).json()
        response = response['keywords']
        
        keywords = []
        for _ in response:
            keywords.append(_['name'])

        return keywords



    def movie_df(self, page : int, category = 'now_playing', drop_col =[]):
        columns = [f'{i}' for i in range(page * 19)]

        df = pd.DataFrame(columns=columns)

        id_list = self.movie_id(page, category)
        
        movie_series = [self.movie_details(id, drop_col=drop_col) for id in id_list]
        
        df = pd.concat(movie_series, axis=1)
        return df.transpose()
    
    def movies_df(self, num = 19, category ='top_rated', drop_col =[]):
        page = num //19
        return self.movie_df(page, category = category, drop_col = drop_col)

#tm = Tmdb(key)
#print(tm.movie_details(123))
