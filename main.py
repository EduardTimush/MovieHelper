import ssl
from tkinter import *
import requests.exceptions
import urllib3.exceptions
from MainPage import MainPage
from urllib3 import exceptions



if __name__ == '__main__':
    try:
        MainPage().run()
    except ssl.SSLError:
        print('ВЫключи нахрен приложения, которые используют интернет')

    except urllib3.exceptions.SSLError:
        print('ВЫключи нахрен приложения, которые используют интернет')

    except requests.exceptions.SSLError:
        print('ВЫключи нахрен приложения, которые используют интернет')


