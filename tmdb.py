import requests
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
    
    def movie_details(self, id : int, full_details = False):
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
        
        response = requests.get(url, headers=headers).json()
        response = pd.Series(response).drop(['backdrop_path', 'adult'])
        

        ## drop unnecessary features when full_details = False
        short = response.drop(['homepage','imdb_id','id','original_language','overview','poster_path','production_companies','production_countries','status','tagline','title','video'])
        
        #short['genres'] = short['genres'][0]['name']
        #short['spoken_languages'] = short['spoken_languages'][0]['english_name']

        if full_details:
            return response
        else:
            return short

    def movie_df(self, page : int, category = 'now_playing', full_details = False):
        columns = [f'{i}' for i in range(page * 19)]

        df = pd.DataFrame(columns=columns)

        id_list = self.movie_id(page, category)
        
        movie_series = [self.movie_details(id) for id in id_list]
        
        df = pd.concat(movie_series, axis=1)
        return df.transpose()
    
    def movies_df(self, num = 19, category ='top_rated', full_details = False):
        page = num //19
        return self.movie_df(page, category = category, full_details=full_details)

# tm = Tmdb(key)
# print(tm.movies_df(300))
