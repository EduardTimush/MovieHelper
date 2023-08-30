from tkinter.ttk import Combobox
from tkinter import *
from MovieRequests import ApiRequests

api = ApiRequests()
class GenresBox:
    def __init__(self,root,lng):
        self.selection = ''
        genres = {'ru':'Жанр фильма','en':'Genre'}
        genres_values = list(api.genres.keys())

        self.genres_combobox = Combobox(master = root,values = genres_values,state = 'readonly')
        self.genres_combobox.set(value = genres[lng])


    def get_value(self):
        if self.selection != self.genres_combobox.get():
            self.selection = self.genres_combobox.get()

            return self.selection

        else:

            return 0