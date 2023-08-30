from tkinter import *
from tkinter.ttk import Combobox

class FilterBox:
    def __init__(self,root,lng):
        self.lng = lng
        self.selection = 'Популярный'
        self.filters = {"ru":['Топ','Популярный','Сейчас смотрят'],'en':['Top','Popular','Watching']}
        self.combobox = Combobox(root,values = self.filters[lng],state='readonly')
        self.combobox.set(value = self.filters[lng][1])


    def get_value(self):
        if self.selection != self.combobox.get():

            self.selection = self.combobox.get()
            if self.selection == self.filters[self.lng][0]:

                return 'top'

            elif self.selection == self.filters[self.lng][1]:

                return 'popular'

            elif self.selection == self.filters[self.lng][2]:

                return 'now'
        else: return 0









