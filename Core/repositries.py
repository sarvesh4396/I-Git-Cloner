import requests
from bs4 import BeautifulSoup
import Core.util as util
from collections import OrderedDict

# This class takes an valid username end returns all the repositries and links
class Repositries:
    def __init__(self , username):
        self.domain_url = 'https://github.com'
        self.repositry_url = 'https://github.com/{}?tab=repositories'.format(username)
        tabs = self.get_tabs()
        self.repositry_list = self.get_repositry_list(tabs)
        self.repositry_info = self.get_repositries_info()
        
    # Function to return repositry page link
    def get_tab_link(self , soup):
        page_class = 'paginate-container'
        page = soup.find(class_ = page_class)
        buttons = page.find_all(class_ = 'btn btn-outline BtnGroup-item')
        for button in buttons:
            text = button.getText()
            if text == 'Next':
                link = button['href']
                return link

    # Function to return all repository page links
    def get_repositories_tabs(self , soup , first_tab):
        tabs = []
        tabs.append(first_tab)
        try:
            while bool(self.get_tab_link(soup)):
                link = self.get_tab_link(soup)
                res = requests.get(link)
                soup = BeautifulSoup(res.text , 'html.parser')
                tabs.append(link)
        except:
            return tabs

    # # Function to start the process
    def get_tabs(self):
        first = self.repositry_url
        res = requests.get(first)
        soup = BeautifulSoup(res.text , 'html.parser')
        tabs = self.get_repositories_tabs(soup , first)
        return tabs

    # Function to return all reopsitories on a single page
    def get_repositry_list(self , tabs):
        repositry_list = []
        user_repositories_id = 'user-repositories-list'
        
        for tab in tabs:
            res = requests.get(tab)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text , 'html.parser')
                list_ = soup.find_all(id = user_repositories_id)[0].find_all('li')
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
            link = self.domain_url + util.get_href(repositry)
            name = repositry.find(itemprop="name codeRepository").getText().strip()
            info[name] = link
        return info