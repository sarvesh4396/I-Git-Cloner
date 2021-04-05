import os , csv

class MakeFile:
    def __init__(self , info_dict , path , filename):
        self.info_dict = info_dict
        self.path = path
        self.filename = filename + '.csv'
        self.full_path  = os.path.join(self.path , self.filename)
        self.keys = list(self.info_dict.keys())
        self.values  = list(self.info_dict.values())
        self.make_path()
        self.generate_file()

    def make_path(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def generate_file(self):
        if not os.path.exists(self.full_path):
            with open(self.full_path , 'w'  , newline='' , encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.keys)
                writer.writerow(self.values)
        else:
            with open(self.full_path , 'a' , newline='' , encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.values)



