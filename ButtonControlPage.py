from tkinter import *
from MovieRequests import ApiRequests
r = ApiRequests()
class ButtonControl:
    def __init__(self,p_builder,filter,genre,query):
        self.filter = filter
        self.p_builder = p_builder
        self.genre = genre
        self.query = query

        self.first_btn = Button()
        self.previous_button = ''

        self.buttons_frame = Frame(background='#21B0DE')


        self.num = 0

        self.buttons_numbers  = []
        self.buttons_dozens_list = []

        self.current_btns_frame = []
        self.all_curennt_buttons = []

        self.previous_button_frame = Button(text='<<',
                                        command=self.switch_frame_buttons)


        self.current_language = 'ru'
        self.num_pages = self.p_builder.number_of_pages


    def buttons_creation(self):
        if self.p_builder.number_of_pages >= 10:
            self.buttons_numbers = [Button(master = self.buttons_frame,text = i,
                                           command = lambda item = i : self.work_manager_for_group(page = item))
                                           for i in range(2,self.p_builder.number_of_pages)]

        elif self.num_pages == 1:
            self.buttons_numbers = []

        elif self.num_pages == 2:

            self.buttons_numbers = [Button(master = self.buttons_frame,text = 2,command = lambda :self.work_manager_for_group(page = 2))]

        elif self.num_pages >2 and self.p_builder.number_of_pages <10:
            self.buttons_numbers = [Button(master=self.buttons_frame,text=i,command = lambda  item = i:self.work_manager_for_group(page = item))
                                           for i in range(2,self.p_builder.number_of_pages + 1)]


    def build(self,root,lng):
        self.current_language = lng

        self.first_btn = Button(master = root,text = 1,state = 'disabled',command = lambda : self.first_button_command(page = 1),bg = 'red')
        self.previous_button = self.first_btn
        self.first_btn.place(x = 800, y = 960)


        self.buttons_creation()
        self.start_placing_frame_buttons()


    def first_button_command(self,page):
        self.first_btn.configure(state = 'disabled')
        self.check_material(page = page)
        self.destroy_current_btns()
        self.start_placing_frame_buttons()
        self.previous_button.configure(state = 'active')
        self.previous_button = self.first_btn

    def start_placing_frame_buttons(self):
        item = 0
        if self.p_builder.number_of_pages >= 20:

            for i in range(10):
                self.buttons_numbers[i].grid(row = 0,column = i)
                self.current_btns_frame.append(self.buttons_numbers[i])
            self.all_curennt_buttons.append(self.current_btns_frame)
            self.previous_button_frame.place(x=820, y=960)
            self.buttons_frame.place(x=860, y=960)

        elif self.p_builder.number_of_pages < 20:

            for i in range(self.p_builder.number_of_pages-1):
                self.buttons_numbers[i].grid(row = 0,column = i)
                self.current_btns_frame.append(self.buttons_numbers[i])
            self.all_curennt_buttons.append(self.current_btns_frame)
            self.buttons_frame.place(x=840, y=960)

    def check_material(self,page):
        try:

            if self.filter != 0:
                self.p_builder.destroy_scroll_page()
                search_result = r.filter_search(filter = self.filter,page = page,lng = self.current_language)
                self.p_builder.build(search_result)

            elif self.genre != 0:
                self.p_builder.destroy_scroll_page()
                search_result = r.genre_search(genre= self.genre, page=page, lng=self.current_language)
                self.p_builder.build(search_result)

            elif self.query != 0:
                self.p_builder.destroy_scroll_page()
                search_result = r.global_search(query = self.query, page=page, lng=self.current_language)
                self.p_builder.build(search_result)
        except:

            self.p_builder.destroy_scroll_page()
            self.p_builder.trouble_window()


    def dis_en_able(self,page):
        self.buttons_numbers[page-2].configure(bg ='red')

        self.previous_button.configure(state='active')
        self.previous_button = self.buttons_numbers[page-2]

        self.previous_button.configure(state='disabled')

    def work_manager_for_group(self,page):
        self.dis_en_able(page=page)
        self.check_material(page=page)
        self.remake_buttons_frame(page = page)

    def find_index(self,page):

        if self.buttons_numbers[page - 2] == self.current_btns_frame[-1]:
            return page - 2,-1

        else:
            return 'no','no'
    def destroy_current_btns(self):
        for i in self.current_btns_frame:
            i.grid_forget()

    def remake_buttons_frame(self,page):

        index,placement = self.find_index(page = page)

        if index != 'no' and placement != 'no' and self.p_builder.number_of_pages >=20:
            self.current_btns_frame = []

            if placement == -1:

                if len(self.buttons_numbers[9*self.num:]) > 9:

                    self.destroy_current_btns()
                    for i in range(10):
                        new_index = index-1+i
                        btn_grided = self.buttons_numbers[new_index]
                        btn_grided.grid(row = 0,column = i)
                        self.current_btns_frame.append(btn_grided)

                    if self.current_btns_frame not in self.all_curennt_buttons:
                        self.all_curennt_buttons.append(self.current_btns_frame)
                    self.num += 1

    def switch_frame_buttons(self):
        if self.num != 0:
            self.destroy_current_btns()

            item = 0
            self.current_btns_frame = []

            for i in self.all_curennt_buttons[self.num - 1]:
                self.current_btns_frame.append(i)
                i.grid(row = 0,column = item)
                item+=1
            self.num -=1
            self.current_btns_frame[-1]['state'] = 'active'