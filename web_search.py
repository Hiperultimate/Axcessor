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
    # print(parts)
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))

# hex_chars = {'%00': 'NUL', '%01': 'SOH', '%02': 'STX', '%03': 'ETX', '%04': 'EOT', '%05': 'ENQ', '%06': 'ACK', '%07': 'BEL',
#             '%08': 'BS', '%09': 'HT', '%0A': 'LF', '%0B': 'VT', '%0C': 'FF', '%0D': 'CR', r'%0E': 'SO', r'%0F': 'SI', '%10': 'DLE', '%11': 'DC1',
#             '%12': 'DC2', '%13': 'DC3', '%14': 'DC4', '%15': 'NAK', '%16': 'SYN', '%17': 'ETB', '%18': 'CAN', '%19': 'EM', '%1A': 'SUB', '%1B': 'ESC',
#             '%1C': 'FS', '%1D': 'GS', r'%1E': 'RS', r'%1F': 'US', '%20': 'space', '%21': '!', '%22': '"', '%23': '#', '%24': '$', '%25': '%',
#             '%26': '&', '%27': "'", '%28': '(', '%29': ')', '%2A': '*', '%2B': '+', '%2C': ',', '%2D': '-', r'%2E': '.', r'%2F': '/', '%30': '0',
#             '%31': '1', '%32': '2', '%33': '3', '%34': '4', '%35': '5', '%36': '6', '%37': '7', '%38': '8', '%39': '9', '%3A': ':', '%3B': ';',
#             '%3C': '<', '%3D': '=', r'%3E': '>', r'%3F': '?', '%40': '@', '%41': 'A', '%42': 'B', '%43': 'C', '%44': 'D', '%45': 'E', '%46': 'F',
#             '%47': 'G', '%48': 'H', '%49': 'I', '%4A': 'J', '%4B': 'K', '%4C': 'L', '%4D': 'M', r'%4E': 'N', r'%4F': 'O', '%50': 'P', '%51': 'Q',
#             '%52': 'R', '%53': 'S', '%54': 'T', '%55': 'U', '%56': 'V', '%57': 'W', '%58': 'X', '%59': 'Y', '%5A': 'Z', '%5B': '[', '%5C': '\\',
#             '%5D': ']', r'%5E': '^', r'%5F': '_', '%60': '`', '%61': 'a', '%62': 'b', '%63': 'c', '%64': 'd', '%65': 'e', '%66': 'f', '%67': 'g',
#             '%68': 'h', '%69': 'i', '%6A': 'j', '%6B': 'k', '%6C': 'l', '%6D': 'm', r'%6E': 'n', r'%6F': 'o', '%70': 'p', '%71': 'q', '%72': 'r',
#             '%73': 's', '%74': 't', '%75': 'u', '%76': 'v', '%77': 'w', '%78': 'x', '%79': 'y', '%7A': 'z', '%7B': '{', '%7C': '|', '%7D': '}',
#             r'%7E': '~', r'%7F': 'DEL'}
    
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

    #To check the webpage code
    # with open(file="html_code.html", mode = "w") as f:
    #     f.write(str(webpage))

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
    
    # print(parsed_info)
    return(parsed_info)

    
# google_results("Parsing made easy")
# google_results("Create paper planes")

