import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from Core.util import *

class Profile:
    def __init__(self , username):
        self.username = username
        self.soup = self.get_soup()
        self.info = OrderedDict()
        self.props = {
                        "name": 'name',
                        "username": 'additionalName',
                        "Working for": 'worksFor',
                        "Home Location": 'homeLocation',
                        "Website": 'url',
                        "Twitter Handle": 'twitter',
                        "Read me Text": 'text'
                        }
        self.classes = {
                        "Bio": ['p-note user-profile-bio mb-3 js-user-profile-bio f4', 0],
                        "Followers": ['text-bold text-gray-dark', 0],
                        "Following": ['text-bold text-gray-dark', 1],
                        "stars": ['text-bold text-gray-dark', 2],
                        "Number of repositries": ['Counter', 0]
                        }
        self.start()


    # Function to check whether a element exists or not
    def check_class(self , soup , class_):
        return bool(soup.find_all(class_ = class_))

    def check_prop(self , soup , prop):
        return bool(soup.find(itemprop = prop))

    def get_soup(self):
        url = 'https://github.com/{}'
        res = requests.get(url.format(self.username))
        soup = BeautifulSoup(res.text , 'html.parser')
        return soup

    
    def get_prop_info(self , prop):
        if self.check_prop(self.soup , prop):
            return self.soup.find(itemprop=prop).getText().strip() 
        else:
            return ''
        
    def get_class_info(self , class_ , index):
        if self.check_class(self.soup , class_):
            return get_info(self.soup , class_ , index)
        else:
            return ''

    def start(self):
        for prop in self.props:
            prop_info = self.get_prop_info(self.props[prop])
            self.info[prop] = prop_info

        for class_ in self.classes:
            class_info = self.get_class_info(class_ = self.classes[class_][0] , index= self.classes[class_][1])
            self.info[class_] = class_info
        try:
            image = self.soup.find(itemprop='image')['href']
        except:
            image = ''
        self.info["image url"] = image

