# import winapps
import os
import glob
import pickle

from win32com.shell import shell, shellcon  
import win32api
import win32con
import win32ui  
import win32gui

from PIL import Image, ImageTk 

"""
Program Search Display Priority Scaling:
        1 - Highest Priority
        2 - Second Highest Priority
        3 - ...
        ...
        10 - Least Priority

"""

# for app in winapps.search_installed(""):
#     """ 
#     C:\ProgramData\Microsoft\Windows\Start Menu\Programs        <-- This is where power toys run was getting all its file searches from

#     Creates a Dictionary which contains : 
#         File name, File Path
    
#     And dumps that dictionary using pickle in a file
#     """
#     # print(app.name)
#     print(app)

def get_icon(PATH, size):  
    SHGFI_ICON = 0x000000100  
    SHGFI_ICONLOCATION = 0x000001000  
    if size == "small":  
        SHIL_SIZE= 0x00001  
    elif size == "large":  
        SHIL_SIZE= 0x00002  
    else:  
        raise TypeError("Invalid argument for 'size'. Must be equal to 'small' or 'large'")  
    ret, info = shell.SHGetFileInfo(PATH, 0, SHGFI_ICONLOCATION | SHGFI_ICON | SHIL_SIZE)  
    hIcon, iIcon, dwAttr, name, typeName = info  
    ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)  
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))  
    hbmp = win32ui.CreateBitmap()  
    hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_x)  
    hdc = hdc.CreateCompatibleDC()  
    hdc.SelectObject(hbmp)  
    hdc.DrawIcon((0, 0), hIcon)  
    win32gui.DestroyIcon(hIcon)  
    
    bmpinfo = hbmp.GetInfo()  
    bmpstr = hbmp.GetBitmapBits(True)  
    img = Image.frombuffer(  
        "RGBA",  
        (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),  
        bmpstr, "raw", "BGRA", 0, 1  
    )  
    
    if size == "small":  
        img = img.resize((16, 16), Image.ANTIALIAS)  
    return img  

def windows_search_startmenu():
    """
    For Start Menu Search Only
    
    Gets all shortcuts name and address located on the location (search_location) and stores it a dictionary and dumps it 

    """
    applications_dict = {}
    search_location = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"

    current_directory = os.getcwd()
    os.chdir(search_location)
    all_shortcut_list = (glob.glob("**/*.lnk" , recursive= True))
    
    for shortcuts in all_shortcut_list:
        name = os.path.basename(os.path.normpath(shortcuts)[:-4])
        location = os.sep.join([search_location, str(shortcuts)])
        icon = get_icon(location,"large")
        applications_dict[name] = {}
        applications_dict[name]['location'] =  location
        applications_dict[name]['icon'] =  icon


    dump_tofile = open(current_directory+'\\search_collection.bin', 'ab') 
    pickle.dump(applications_dict, dump_tofile)
    dump_tofile.close()
    os.chdir(current_directory)

def search_dict(search_string):
    """
    Get dumped dictionary and search for substrings
    Eg:
    for keys in a_dict.keys():
            if(search in keys):
                    print(a_dict[keys])
    """

    print(os.getcwd())
    dict_file = open("search_collection.bin", "rb")
    applications_dict = pickle.load(dict_file)
    search_result = {keys : {'location':applications_dict[keys]["location"], 'icon': applications_dict[keys]["icon"] } for keys in applications_dict.keys() if search_string.lower() in keys.lower()}
    return(search_result)

    # for keys in applications_dict.keys():
    #     if(search.lower() in keys.lower()):
    #         print(keys , " ", applications_dict[keys]['location'])
    # search_result = [(keys, applications_dict[keys]["location"]) for keys in applications_dict.keys() if search in keys]


windows_search_startmenu()
# search_dict("valo")
