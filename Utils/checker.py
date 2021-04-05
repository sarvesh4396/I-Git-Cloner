import requests
from Utils.colours import *
import math

def check_profile(name):
    url = 'https://github.com/{}'
    res = requests.get(url.format(name))
    return res.status_code == 200


def check_topic(topic):
    url = 'https://github.com/search?q={}'
    res = requests.get(url.format(topic))
    return res.status_code == 200




def list_columns(obj, cols=4, columnwise=True, gap=4):
    """
    Print the given list in evenly-spaced columns.

    Parameters
    ----------
    obj : list
        The list to be printed.
    cols : int
        The number of columns in which the list should be printed.
    columnwise : bool, default=True
        If True, the items in the list will be printed column-wise.
        If False the items in the list will be printed row-wise.
    gap : int
        The number of spaces that should separate the longest column
        item/s from the next column. This is the effective spacing
        between columns based on the maximum len() of the list items.
    """

    sobj = ['[{}] '.format(index) + str(item) for index , item in enumerate(obj , start=1)]
    if cols > len(sobj): cols = len(sobj)
    max_len = max([len(item) for item in sobj])
    if columnwise: cols = int(math.ceil(float(len(sobj)) / float(cols)))
    plist = [sobj[i: i+cols] for i in range(0, len(sobj), cols)]
    if columnwise:
        if not len(plist[-1]) == cols:
            plist[-1].extend(['']*(len(sobj) - len(plist[-1])))
        plist = zip(*plist)
    printer = '\n'.join([
        ''.join([c.ljust(max_len + gap) for c in p])
        for p in plist])
    print(printer)



def print_and_get_repos(repos):
    names = list(repos.keys())
    all_num = len(names) + 1
    no_num = 0
    
    print_info(blue , f"Found {len(names)} repositries.")
    print()
    print_info(blue , "Enter the serial numbers of repositries you want to clone.")
    print()
    
    list_columns(names, cols=3) 
    
    print_info(yellow , f'[{all_num}]  All repositries')
    print_info(red , f'[{no_num}]  No repositries')


    print()
    while True:
        try:
            numbers = list(map(int , input().split(",")))
            break
        except:
            print("Enter valid input.")
            print("Try again..")
            print()

    all_repos = bool([res for res in numbers if res == all_num])
    no_repos = bool([res for res in numbers if res == no_num])


    
    if all_repos:
        links = set(repos.values())
    elif no_repos:
        links = set()
    else:
        links = set()
        for num in numbers:
            name = names[num-1]
            link = repos[name]
            links.add(link)

    return links
        