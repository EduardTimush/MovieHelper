import requests
import string
from MovieRequests import ApiRequests
from tkinter import *
from io import BytesIO
from PIL import Image,ImageTk
from CurrentMoviePage import CurrentPage
from ListOfImgUrl import Unpack
from ScrollPageBuilder import PageBuilder
from ButtonControlPage import ButtonControl
from FIlterCombobox import FilterBox
from GenresCombobox import GenresBox
from LanguageCombobox import LanguageBox

img_url = Unpack()
cur_page = CurrentPage()
r = ApiRequests()

class MainPage:

    def __init__(self):
        self.current_language = 'ru'
        self.root = Tk()
        self.root.title('Movie Helper')
        self.root.geometry('1920x1080')
        self.root.configure(bg = '#21B0DE')
        self.root.bind('<Return>',self.control_scroll_query)
        self.movie_carousel()
        self.query_requests = 0
        self.lowers = {'ru':string.ascii_lowercase,'en':'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'}



        self.lbl = Label(text = 'Расширенный поиск',font = 20,bg = '#21B0DE' )
        self.lbl.place(x = 40,y=300)



        self.f_box = FilterBox(self.root,lng=self.current_language)
        self.f_box.combobox.bind('<<ComboboxSelected>>', self.control_scroll_filters)
        self.f_box.combobox.place(x=40, y=350)


        self.p_builder = PageBuilder(self.root)
        search_result = r.filter_search(page=1, filter='popular',lng = self.current_language)
        self.p_builder.build(search_result)
        self.p_builder.canvas.yview_moveto(0)

        self.btn_control = ButtonControl( p_builder=self.p_builder,filter='popular',genre = 0,query = 0)
        self.btn_control.build(root = self.root,lng=self.current_language)

        self.g_box = GenresBox(self.root,lng = self.current_language)
        self.g_box.genres_combobox.bind('<<ComboboxSelected>>',self.control_scroll_genres)
        self.g_box.genres_combobox.place(x = 40,y = 400)

        self.entry_query = Entry()
        self.entry_query.place(x = 40,y = 500)

        self.btn_search = Button(text = 'Поиск',font = 10,command = lambda:self.control_scroll_query(e = None))
        self.btn_search.place(x = 40,y= 520)

        self.l_box = LanguageBox(root=self.root)
        self.l_box.combobox.bind('<<ComboboxSelected>>',self.control_language_page)
        self.l_box.combobox.place(x = 10,y = 20)


    def run(self):

        self.root.mainloop()

    def control_language_page(self,e):
        self.current_language = self.l_box.got_value()

        self.f_box = FilterBox(self.root,lng=self.current_language)
        self.f_box.combobox.bind('<<ComboboxSelected>>', self.control_scroll_filters)
        self.f_box.combobox.place(x=40, y=350)

        self.g_box = GenresBox(self.root, lng=self.current_language)
        self.g_box.genres_combobox.bind('<<ComboboxSelected>>', self.control_scroll_genres)
        self.g_box.genres_combobox.place(x=40, y=400)


        if self.current_language == 'en':
            self.btn_search['text'] = 'Search'
            self.lbl['text' ] = 'Global Search'

        else:
            self.btn_search['text'] = 'Поиск'
            self.lbl['text'] = 'Расширенный поиск'

        self.movie_carousel()

        self.p_builder.destroy_scroll_page()
        search_result = r.filter_search(page=1, filter='popular', lng=self.current_language)
        self.p_builder.build(search_result = search_result)

        self.btn_control.destroy_current_btns()
        self.btn_control = ButtonControl(p_builder=self.p_builder, filter='popular', genre=0, query=0)
        self.btn_control.build(root=self.root, lng=self.current_language)



    def error_query_language(self):
        self.a = Toplevel()
        self.a.focus_set()

        image = ImageTk.PhotoImage(Image.open('grusti.png'))
        if self.current_language == 'ru':
            lbl_txt = Label(master=self.a,text = '''По запросу ничего не найдено :)
            ''',font = 20)
        else:
            lbl_txt = Label(master=self.a,text = '''Wasn't found anything :)
            ''',font = 20)

        lbl_image = Label(master=self.a,image = image)
        lbl_image.image = image

        lbl_image.pack()
        lbl_txt.pack()


    def movie_carousel(self):
        x = 254
        urls,response = img_url.pic_main_page(lng = self.current_language)
        for cut_url in urls:

            new_url = f'{r.urlImage}{cut_url}'
            response_img = requests.get(new_url)# Получение картинки
            image = ImageTk.PhotoImage(Image.open(BytesIO(response_img.content)).resize((150, 220),
                                                                                    Image.LANCZOS))  # Расшифровка из байтов и превращени в картинку для ТК

            lbl = Label(image=image)
            lbl.bind('<Button-1>',lambda e, response = response , cut_url = cut_url, response_img = response_img : cur_page.build_current_movie_page(
                event=e,response=response,cut_url=cut_url,response_img = response_img))

            lbl.image = image
            lbl.place(x=x, y=3)
            x += 254

    def control_scroll_filters(self,e):

        got_filter = self.f_box.get_value()

        if got_filter != 0:
            self.p_builder.destroy_scroll_page()
            search_result = r.filter_search(filter = got_filter,page = 1,lng = self.current_language)
            self.p_builder.build(search_result = search_result)

            self.btn_control.destroy_current_btns()
            self.btn_control = ButtonControl(p_builder=self.p_builder, filter=got_filter,genre = 0,query = 0 )
            self.btn_control.build(root = self.root,lng=self.current_language)

    def control_scroll_genres(self,e):
        got_genre = self.g_box.get_value()

        if got_genre != 0 and got_genre != 'Жанр фиьма':
            self.p_builder.destroy_scroll_page()

            search_result = r.genre_search(genre = got_genre,page=  1,lng = self.current_language)

            self.p_builder.build(search_result = search_result)
            self.btn_control.destroy_current_btns()
            self.btn_control = ButtonControl(filter = 0,p_builder= self.p_builder,genre = got_genre,query = 0 )
            self.btn_control.build(root = self.root,lng=self.current_language)

    def control_scroll_query(self,e):

        error_query = False
        got_query = self.entry_query.get()
        self.entry_query.delete(0,END)

        for i in list(got_query):
            if i in self.lowers[self.current_language] and self.query_requests == 0:
                self.error_query_language()
                error_query = True
                break

        if got_query.isspace() == False and got_query != '' and error_query == False:

            search_result = r.global_search(query = got_query,page = 1,lng = self.current_language)

            if search_result != None:

                self.p_builder.destroy_scroll_page()

                self.p_builder.build(search_result=search_result)

                self.btn_control.destroy_current_btns()
                self.btn_control.previous_button_frame.place_forget()
                self.btn_control = ButtonControl(filter=0,p_builder=self.p_builder,genre = 0,query = got_query)
                self.btn_control.build(root = self.root,lng = self.current_language)

            else:
                self.error_query_language()

