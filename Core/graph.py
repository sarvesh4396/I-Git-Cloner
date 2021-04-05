import plotly.express as px
import pandas as pd
import os
from collections import Counter 

class Graph:
    def __init__(self , stats_directory , graph_type , index=1):
        self.graph_type = graph_type
        self.stats_directory = stats_directory
        self.file = self.get_file(index)
        self.repositories = self.get_dataframe()
        self.info = self.get_info()
        self.start()


    def get_file(self , index):
        file = os.path.join(self.stats_directory , os.listdir(self.stats_directory)[index])
        return file

    def get_dataframe(self):
        repositories = pd.read_csv(self.file)
        repositories['fork']=  repositories['fork'].str.replace(',','')
        repositories['fork']=  repositories['fork'].str.replace('.','')
        repositories['fork']=  pd.to_numeric(repositories['fork'].str.replace('k','000'))
        repositories['star']=  repositories['star'].str.replace(',','')
        repositories['star']=  repositories['star'].str.replace('.','')
        repositories['star']=  pd.to_numeric(repositories['star'].str.replace('k','000'))
        repositories = repositories.fillna(0)
        return repositories

    def get_forked_df(self):
        forked_df = pd.DataFrame(data = {'Forks': self.repositories['fork'],
                           'Repositories': self.repositories['Name']})
        df = forked_df.sort_values(by='Forks', axis=0, ascending=False)

        top_forked = df[df['Forks'] >0].head(15)
        return top_forked

    def get_starred_df(self):
        starred_df = pd.DataFrame(data = {'Stars': self.repositories['star'],
                           'Repositories': self.repositories['Name']})
        df = starred_df.sort_values(by='Stars', axis=0, ascending=False)
        top_starred = df[df['Stars'] >0].head(15)
        return top_starred

    def get_languange_df(self):
        occ = dict(Counter(self.repositories['Programming Language']))
        top_languages = [(language, frequency) for language, frequency in occ.items()]

        top_languages = list(zip(*top_languages))

        language_df = pd.DataFrame(data = {'languages': top_languages[0],
                                'frequency': top_languages[1]}).head(15)

        
        language_df.sort_values(by='frequency', axis=0, inplace=True, ascending=False)
        return language_df


    def get_info(self):
        forked_df = self.get_forked_df()
        starred_df = self.get_starred_df()
        language_df = self.get_languange_df()
        # {"image_name" : [title , dataframe , x_axis , y_axis ]}

        info = {
                "Stars": ['Count of stars on a repository', starred_df , 'Repositories' , 'Stars'],
                "Forks": ['Count of forks on a repository', forked_df, 'Repositories' , 'Forks'],
                "Languages": ['Frequency of languages', language_df , 'languages' , 'frequency']
                }
        return info

    def generate_bargraph(self ,title, dataframe , x_axis , y_axis):
        graph = px.bar(dataframe, 
             x = x_axis, 
             y = y_axis,
             hover_data = [y_axis],
             title = title
            )
        return graph

    def generate_piechart(self ,title, dataframe , names , values):

        graph = px.pie(dataframe, 
             values = values, 
             names = names,
             title = title
            )
        return graph


    def save_graph(self , graph , image_name):
        graph.write_image(os.path.join(self.stats_directory , image_name + '.png'))


    def start(self):
        if self.graph_type == 'bar':
            for image in self.info:
                title = self.info[image][0]
                dataframe = self.info[image][1]
                x_axis = self.info[image][2]
                y_axis = self.info[image][3]
                graph = self.generate_bargraph(title=title , dataframe=dataframe , x_axis=x_axis , y_axis=y_axis)
                self.save_graph(graph=graph , image_name=image)
        else:
            
            for image in self.info:
                title = self.info[image][0]
                dataframe = self.info[image][1]
                names = self.info[image][2]
                values = self.info[image][3]
                graph = self.generate_piechart(title=title , dataframe=dataframe , names=names , values=values)
                self.save_graph(graph=graph , image_name=image)
            
