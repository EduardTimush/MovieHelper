from tkinter import *
from tkinter.ttk import Combobox
class LanguageBox:
    def __init__(self,root):
        self.selection = 'ru'
        lngs = ['ru','en']
        self.combobox = Combobox(master = root,values = lngs,state = 'readonly')
        self.combobox.set(value = 'ru')

    def got_value(self):

        if self.selection != self.combobox.get():
            self.selection = self.combobox.get()
            return self.selection

        else:
            return 0

