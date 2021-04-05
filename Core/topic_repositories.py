import requests
from bs4 import BeautifulSoup
import Core.util as util
from collections import OrderedDict


# This class takes an valid username end returns all the repositries and links
class Repositries:
    def __init__(self , topic , limit):
        self.topic = topic
        self.profiles = set()
        self.limit = limit//10
        self.domain_url = 'https://github.com'
        self.repositry_url = 'https://github.com/search?q={}'.format(topic)
        tabs = self.get_tabs()
        

        self.repositry_list = self.get_repositry_list(tabs)
        self.repositry_info = self.get_repositries_info()
        
    


    # Function to get the tabs upto limit
    def get_tabs(self):
        first = self.repositry_url
        tabs = [first]
        for page_count in range(2 , self.limit+1):
            url = self.domain_url + "/search?p={}&amp;q={}&amp;type=Repositories".format(page_count , self.topic)
            tabs.append(url)
        return tabs

    # Function to return all reopsitories on a single page
    def get_repositry_list(self , tabs):
        repositry_list = []
        repositories_class = 'repo-list'
        for tab in tabs:
            res = requests.get(tab)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text , 'html.parser')
                list_ = soup.find_all(class_ = repositories_class)[0].find_all('li')
                repositry_list.append(list_)
                
        return self.process_repositry_tabs(repositry_list)

    # Function to process all repositries in a single list
    def process_repositry_tabs(self , repositry_list):
        repositries = []
        for repo_tab in repositry_list:
            for repo in repo_tab:
                repositries.append(repo)
        return repositries

    # Function to get links of repositries
    def get_repositries_info(self):
        info = OrderedDict()
        for repositry in self.repositry_list:
            result = util.get_json(repositry)
            if bool(result):
                link = result['payload']['result']['url']
                name = link.replace(self.domain_url , '')
                profile = link.split("/")[3]
                self.profiles.add(profile)
                info[name] = link
            
        return info