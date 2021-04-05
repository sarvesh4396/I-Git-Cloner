import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from Core.util import *
# Ignoring future warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class RepoInfo:
    def __init__(self , repository):
        self.repository = repository
        
        self.domain_url = 'https://github.com'
        self.info = OrderedDict()
        self.props = {
                        "Name": 'name codeRepository',
                        "Description": 'description',
                        "Programming Language": 'programmingLanguage',
                        }
        self.start()


    # Function to check whether a element exists or not
    def check_class(self , soup , class_):
        return bool(soup.find_all(class_ = class_))

    def check_prop(self , soup , prop):
        return bool(soup.find(itemprop=prop))

    def get_soup(self):
        url = 'https://github.com/{}'
        res = requests.get(url.format(self.username))
        soup = BeautifulSoup(res.text , 'html.parser')
        return soup

    
    def get_prop_info(self , prop):
        if self.check_prop(self.repository , prop):
            return self.repository.find(itemprop=prop).getText().strip() 
        else:
            return ''
        
    def get_class_info(self , class_ , index):
        if self.check_class(self.repository , class_):
            return get_info(self.repository , class_ , index)
        else:
            return ''

    def licence(self):
        # Licence
        bottom_menu = self.repository.find(class_ = 'f6 color-text-secondary mt-2')
        span_tag = bottom_menu.find_all('span')
        info = {'law':''}
        for span in span_tag:
            try:
                class_ = span.find('svg')['class']
                for key in info:
                    if bool([ele for ele in class_ if(key in ele)]):
                        info[key] = span.getText().strip()
            except:
                pass

        self.info.update(info)

    def stars_and_forks(self):
        # Star and Forks
        bottom_menu = self.repository.find(class_ = 'f6 color-text-secondary mt-2')
        a_tag = bottom_menu.find_all('a')
        info = {'star':'' , 'fork': ''}
        for a in a_tag:
            try:
                class_ = a.find('svg')['class']
                for key in info:
                    if bool([ele for ele in class_ if(key in ele)]):
                        info[key] = a.getText().strip()
            except :
                pass

        self.info.update(info)

    def topics(self):
        # Topics
        repositry_topics_class = 'topics-row-container d-inline-flex flex-wrap flex-items-center f6 my-1'
        if self.check_class(self.repository , repositry_topics_class):
            info = get_info(self.repository , repositry_topics_class).split()
        else:
            info = ''
        self.info['Topics'] = info
            
    def change_key(self , old_key , new_key):
        self.info[new_key] = self.info.pop(old_key)

    def start(self):
        for prop in self.props:
            prop_info = self.get_prop_info(self.props[prop])
            self.info[prop] = prop_info


        self.licence()
        self.change_key('law' , 'Licence')
        self.stars_and_forks()
        self.topics()
        # Last Updated
        updated = self.repository.find('relative-time')
        self.info["Last Updated"] = updated.getText() if updated else ''

        # Repositry url
        self.info["Repositry url"] = self.domain_url + get_href(self.repository)
