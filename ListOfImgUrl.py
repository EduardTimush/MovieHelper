from MovieRequests import ApiRequests
r = ApiRequests()
class Unpack:
    def pic_main_page(self,lng):
        values = []
        info_request = r.filter_search('now',1,lng=lng)[0] #Получение запроса
        for i in info_request.values():
            values.append(i['img']) #Вытягивание ссылок на картинки в список

        values = values[0:6]

        return values,info_request
