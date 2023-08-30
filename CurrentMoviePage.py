from tkinter import *
from io import BytesIO
from PIL import Image,ImageTk
from ListOfImgUrl import Unpack
img_url = Unpack()
from MovieRequests import ApiRequests
r = ApiRequests()
import requests


class CurrentPage:
        # self.values, self.info_request = img_url.pic_main_page()

    def find_element(self,response,cut_url):
        for key,value in response.items():
            if cut_url == value['img']:
                current_movie = key

        return current_movie

    def build_current_movie_page(self,event,response,cut_url,response_img):
        current_movie = self.find_element(response = response,cut_url = cut_url)

        new_window = Toplevel()
        new_window.resizable(False,False)
        new_window.title(response[current_movie]['title'])
        # new_window.geometry('620x590')

        image = ImageTk.PhotoImage(Image.open(BytesIO(response_img.content)).resize((380,500),Image.LANCZOS))

        lbl_image = Label(new_window,image = image)
        lbl_image.image = image
        lbl_image.pack(side=TOP)

        lbl_text = Label(new_window,text = response[current_movie]['description'],wraplength = 500)
        lbl_text.pack(side = TOP)

        lbl_year = Label(new_window,text = response[current_movie]['data'])
        lbl_year.pack(side = TOP)

        lbl_popularity = Label(new_window,text= response[current_movie]['popularity'])
        lbl_popularity.pack(side = TOP)




# CurrentPage().movie_carousel()