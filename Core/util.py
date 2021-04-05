import json
# Some utility functions
def get_info(soup , class_ , index=0):
    text = soup.find_all(class_ = class_)
    if len(text)>0:
        text = text[index].getText()
        text = text.strip()
    else:
        text = None
    return text

def get_href(soup ,  index=0):
    text = soup.find_all('a')
    if len(text)>0:
        text = text[index]['href']
        text = text.strip()
    else:
        text = None
    return text

def get_json(soup):
    try:
        text = soup.find(class_ = 'v-align-middle')
        info = text['data-hydro-click']
        info = json.loads(info)
    except:
        info = None

    return info



def get_image_src(soup ,  index=0):
    text = soup.find_all('img')
    if len(text)>0:
        text = text[index]['src']
        text = text.strip()
    else:
        text = None
    return text

def check(soup , class_):
    return bool(soup.find_all(class_ = class_))


