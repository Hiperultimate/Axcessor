from lxml import html

import re

from urllib.request import Request, urlopen

def stringify_children(node):
    from lxml.etree import tostring
    from itertools import chain
    parts = ([node.text] +
            list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
            [node.tail])
    parts = [(i if type(i) == str else i.decode()) for i in parts if(i)]
    parts = [re.sub("<.*?>","",i ) for i in parts]
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))
    
hex_chars = {
        '%21': '!', '%22': '"', '%23': '#', '%24': '$', '%25': '%', '%26': '&', '%27': "'", '%28': '(', '%29': ')', '%2A': '*', 
        '%2B': '+', '%2C': ',', '%2D': '-', r'%2E': '.', r'%2F': '/', '%3A': ':', '%3B': ';','%3C': '<', '%3D': '=', r'%3E': '>',
        r'%3F': '?', '%40': '@', '%5B': '[', '%5C': '\\','%5D': ']', r'%5E': '^', r'%5F': '_', '%60': '`', '%7B': '{', '%7C': '|', '%7D': '}',r'%7E': '~'
    }
def decode_url(link):
    #Fixes URL which are encased with hex characters 
    for hex_keys in hex_chars.keys():
        if(hex_keys in link):
            link = link.replace(hex_keys,hex_chars[hex_keys])

    return(link)

#Google search results using xPath 
def google_results(search_string):
    #Takes in a search string to google and returns a google search results which gives description, url and heading

    searching = "https://www.google.com/search?q="+"%20".join(search_string.split())
    req = Request(searching,headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()

    tree = html.fromstring(webpage)

    parsed_info = {}
    url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

    
    hyper_links = tree.xpath('//*[@id="main"]/div[*]/div/div[1]/a')#[7:]
    
    results = len(hyper_links)
    descriptions = tree.xpath('//*[@id="main"]/div[*]/div/div[3]/div/div/div/div/div')
    descriptions = [stringify_children(x) for x in descriptions ]
    headings = tree.xpath('//*[@id="main"]/div[*]/div/div[1]/a/h3/div/text()')
    results = [len(headings),len(hyper_links),len(descriptions)]
    for iter in range(min(results)):
        dirty_url = hyper_links[iter].attrib["href"].split("&sa=")[0]
        cleaned_url = decode_url(dirty_url)
        cleaned_url = re.findall(url_regex,cleaned_url) 
        if(len(cleaned_url) == 0):
            continue
        parsed_info[headings[iter]] = {}
        parsed_info[headings[iter]]['hyper_links'] = cleaned_url[0][0]
        parsed_info[headings[iter]]['description'] = descriptions[iter]#.text

    return(parsed_info)

    
# google_results("Parsing made easy")
# google_results("Create paper planes")

