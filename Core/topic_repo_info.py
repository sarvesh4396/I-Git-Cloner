import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from Core.util import *


class TopicRepoInfo:
    def __init__(self , repository_url , name):
        self.repository_url = repository_url
        self.name = name
        self.repository = self.get_soup()
        self.domain_url = 'https://github.com'
        self.info = OrderedDict()
        self.classes = {
                        "Description": ['f4 mt-3' , 0],
                        "star": ['social-count js-social-count', 0],
                        "fork": ['social-count', 2],
                        "Topics":['topic-tag topic-tag-link' , 0]
                        }
        self.start()


    def get_soup(self):
        res = requests.get(self.repository_url)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text , 'html.parser')
            return soup
        else:
            quit()

    # Function to check whether a element exists or not
    def check_class(self , soup , class_):
        return bool(soup.find_all(class_ = class_))

    def check_prop(self , soup , prop):
        return bool(soup.find(itemprop=prop))


    
    def get_prop_info(self , prop):
        if self.check_prop(self.repository , prop):
            return self.repository.find(itemprop=prop).getText().strip() 
        else:
            return ''
        
    def get_class_info(self , class_ , index):
        if self.check_class(self.repository , class_):
            return self.get_info(self.repository , class_ , index)
        else:
            return ''

    def licence(self):
        # Licence
        info = {'law':''}
        bottom_menus = self.repository.find_all(class_ = 'mt-3')
        for bottom_menu in bottom_menus:
            try:
                a_tag = bottom_menu.find_all('a')
                for a in a_tag:
                    class_ = a.find('svg')['class']
                    for key in info:
                        if bool([ele for ele in class_ if(key in ele)]):
                            info[key] = a.getText().strip()
                            break
            except:
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
    
    def get_languages(self):
        blocks  = self.repository.find_all(class_ = 'BorderGrid-cell')
        for block in blocks:
            text = block.getText().strip()
            if 'Languages' in text:
                list_ = text.replace("Languages" , '').strip().split()
                self.info["Programming Language"] =  [lang for lang in list_ if not any(c.isdigit() for c in lang)]
                 
        
        return
            
    def change_key(self , old_key , new_key):
        self.info[new_key] = self.info.pop(old_key)
        
    def get_info(self , soup , class_ , index=0):
        text = soup.find_all(class_ = class_)
        if len(text)>0:
            text = text[index].getText()
            text = text.strip()
        else:
            text = None
        return text

    def start(self):
        self.info['Name'] = self.name
        for class_ in self.classes:
            try:
                class_info = self.get_class_info(class_ = self.classes[class_][0] , index= self.classes[class_][1])
                self.info[class_] = class_info
            except:
                pass


        self.licence()
        self.change_key('law' , 'Licence')
        # Last Updated
        updated = self.repository.find('relative-time')
        self.info["Last Updated"] = updated.getText() if updated else ''

        # Repositry url
        self.info["Repositry url"] = self.repository_url
        
        self.get_languages()