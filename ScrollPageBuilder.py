import tkinter as tk
from MovieRequests import ApiRequests
from CurrentMoviePage import CurrentPage
from PIL import Image, ImageTk
from io import BytesIO
import requests

# from tkinter import ttk
r = ApiRequests()
cur_page = CurrentPage()

class PageBuilder:
    def __init__(self, root):
        self.movie_info_dict = ''

        self.container = tk.Frame()
        self.canvas = tk.Canvas(master=self.container, width=510, height=550)
        self.canvas.bind('<MouseWheel>',self.scroll_control)
        self.vscroll = tk.Scrollbar(master=self.container, orient='vertical', command=self.canvas.yview)

        self.number_of_pages = 0

    def scroll_control(self,e):
        self.canvas.yview_scroll(int(-1*(e.delta/120)),'units')

    def build(self,search_result):
        self.scrollable_frame = tk.Frame(master=self.canvas)

        self.scrollable_frame.bind('<Configure>',lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.scrollable_frame.pack()
        self.canvas.create_window((0, 0), window=self.scrollable_frame)
        self.canvas.configure(yscrollcommand=self.vscroll.set)
        self.check_material(search_result=search_result)

        self.placing_widgets()

        self.container.place(x=800, y=400)


        self.canvas.pack(side="left", fill="both")
        self.vscroll.pack(side="right", fill="y")
        self.canvas.yview_moveto(0)
        # self.canvas.yview_moveto(0)


        # self.pack()

    def check_material(self,search_result):


        if search_result!= None:
            self.movie_info_dict,self.number_of_pages = search_result

    def set_scroll_position(self):
        pass

    def placing_widgets(self):
        row = 0
        column = 0
        for key, values in self.movie_info_dict.items():
            cut_url = values['img']
            if cut_url != None:
                response_img = requests.get(f'{r.urlImage}{cut_url}')


                image = ImageTk.PhotoImage(
                    Image.open(BytesIO(response_img.content)).resize((250, 330),
                                                                     Image.LANCZOS))  # Расшифровка из байтов и превращени в картинку для ТК


                img_lbl = tk.Label(master = self.scrollable_frame, image=image)
                img_lbl.bind('<MouseWheel>',self.scroll_control)
                img_lbl.image = image

                img_lbl.bind('<Button-1>', lambda e, response=self.movie_info_dict, cut_url=cut_url, response_img=response_img:

                cur_page.build_current_movie_page(
                    e, response=response, cut_url=cut_url, response_img=response_img))

                img_lbl.grid(row=row, column=column)

            else:
                img_lbl = tk.Label(master=self.scrollable_frame,text = 'Нет картинки')
                img_lbl.grid(row = row,column = column)

            desc_lbl = tk.Label(self.scrollable_frame, text=values['description'], wraplength=220,height = 22)
            desc_lbl.grid(row=row, column=column + 1)
            desc_lbl.bind('<MouseWheel>',self.scroll_control)

            row += 1



    def pack(self):
        # self.vscroll.set(0, 2)
        self.container.place(x=800, y=400)
        self.canvas.pack(side="left", fill="both")
        self.vscroll.pack(side="right", fill="y")

        self.set_scroll_position()

    def destroy_scroll_page(self):
        self.canvas.delete('all')
        self.scrollable_frame.destroy()

    def trouble_window(self):
        z = 20
        for i in range(0,10):
            tk.Label(self.scrollable_frame,text = '''Ошибка 404
            Страница отсутствует по тех причинам''',font = 20).place(x = 10,y = z)
            z+=100

