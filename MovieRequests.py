import requests
import string
from tkinter import *
from PIL import Image,ImageTk

class ApiRequests:

    def __init__(self):
        # self.a = Tk()
        self.filters = {'top':'/top_rated','popular':'/popular','now':'/now_playing'}
        self.api_key = '89a4467d0304ba837d1431f4d0bdbc67'

        self.urlImage = 'https://image.tmdb.org/t/p/original'
        self.mainUrl = "https://api.themoviedb.org/3/movie"
        self.genreUrl = f'https://api.themoviedb.org/3/discover/movie'

        self.genres = {'Action': 28, 'Adventure': 12, 'Animation': 16, 'Comedy': 35, 'Crime': 80, 'Documentary': 99, 'Drama': 18, 'Family': 10751,
                       'Fantasy': 14, 'History': 36, 'Horror': 27, 'Music': 10402, 'Mystery': 9648, 'Romance': 10749, 'Science Fiction': 878,
                       'TV Movie': 10770, 'Thriller': 53, 'War': 10752, 'Western': 37}


    def unpack(self,results): #Распаковка важных элементов из json
        current_information = {}
        new_results = results['results']
        number_of_pages = results['total_pages']

        if number_of_pages < 500:
            pass
        else:
            number_of_pages = 500
        for i in new_results:
            try:
                if i['overview'] == '':
                    descNimg = {'description':'Увы,но описания нет','img':i['poster_path'],'popularity':i['vote_average']}
                else:
                    descNimg = {'description':i['overview'],'img':i['poster_path'],'popularity':i['vote_average']}


                try:
                    descNimg['title'] = i['title']
                    descNimg['data'] = i['release_date']
                    current_information[i['title']] = descNimg
                except KeyError:
                    descNimg['title'] = i['name']
                    descNimg['data'] = i['first_air_date']
                    current_information[i['name']] = descNimg

            except KeyError:
                print('excepted')


        return current_information,number_of_pages

    def filter_search(self,filter,page,lng): #Получение фильмов и их распаковка
        try:
            url =f'{self.mainUrl}{self.filters[filter]}?api_key={self.api_key}&language={lng}&page={page}'


            response = requests.get(url = url).json()
            results,number_of_pages = self.unpack(results = response)
            return results,number_of_pages
        except:
            #Обработка исключения, если не будет найдено рузультатов, удовлетворяющих по поиску
            return 'Нет информации по запросу'

    def global_search(self,query,page,lng):

        global_url = f'https://api.themoviedb.org/3/search/multi?api_key={self.api_key}&query={query.lower()}&language={lng}&page={page}'



        response = requests.get(global_url).json()

        results, number_of_pages = self.unpack(results=response)
        if results != {}:
            return results, number_of_pages

        else:
            return None


    def genre_search(self,genre,page,lng):
        genre_url = f'{self.genreUrl}?api_key={self.api_key}&with_genres={self.genres[genre]}&language={lng}&page={page}'
        try:
            response = requests.get(genre_url).json()

            results,number_of_pages = self.unpack(results = response)
            return results,number_of_pages

        except:
            return 'Нет информации по запросу'

# image = ''
# api_key = '89a4467d0304ba837d1431f4d0bdbc67'
#
# url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=ru&page=3"
# genres_url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres=28'
#
# urlImage = f'https://image.tmdb.org/t/p/original{image}'
# response = requests.get(url = url).json()
# # a = ApiRequests().unpack(response)
# print(response)
# filters = {'top':'top_rated','popular':'popular','now':'now_playing'}
