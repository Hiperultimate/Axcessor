import os
import glob
import pickle
import winreg

from win32com.shell import shell, shellcon  
import win32api
import win32con
import win32ui  
import win32gui

from PIL import Image, ImageTk 


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

    Overwrites all existing contents in search_collection.bin file

    """
    # try:
    #     dict_file = open("search_collection.bin", "rb")
    #     applications_dict = pickle.load(dict_file)
    #     dict_file.close()
    # except FileNotFoundError:
    #     applications_dict = {}
        
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


    dump_tofile = open(current_directory+'\\search_collection.bin', 'wb') 
    pickle.dump(applications_dict, dump_tofile)
    dump_tofile.close()
    os.chdir(current_directory)

def windows_exe_search_registry():
    current_directory = os.getcwd()
    print(current_directory)
    try:
        dict_file = open("search_collection.bin", "rb")
        applications_dict = pickle.load(dict_file)
        dict_file.close()
    except FileNotFoundError:
        applications_dict = {}

    # print("Dictionary Items : ", applications_dict.items())

    access_registryLM = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)     #LM - Local_Machine
    access_registryCU = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)      #CU - Current_User

    access_key_1 = winreg.OpenKey(access_registryLM , "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall")       #Uses "InstallLocation" for regtype
    access_key_2 = winreg.OpenKey(access_registryLM , "SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall")       #Uses "InstallLocation" for regtype
    access_key_3 = winreg.OpenKey(access_registryCU , "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall")       #Uses "Path" for regtype
    access_key_4 = winreg.OpenKey(access_registryLM , "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths")       #Uses "InstallLocation" for regtype

    every_key = [access_key_1,access_key_2,access_key_3,access_key_4]
    KEYvaluename_Path = ["InstallLocation" , "Path"]
    half_path = []
    full_path = []

    for i in range(4):
        n = 0
        vnPath_Switch = 0
        if(i == 3):
            vnPath_Switch = 1
        while(True):
            try:
                f_keys = winreg.EnumKey(every_key[i],n)     #Keys under uninstall
            except:
                break
            skeys = winreg.OpenKey(every_key[i] , f_keys, 0 , winreg.KEY_READ)
            try:
                pathname, regtype = winreg.QueryValueEx(skeys , KEYvaluename_Path[vnPath_Switch])
                
                if(pathname != ""):
                    if("/" not in pathname):
                        half_path.append(pathname)
                    else:
                        pathname.replace("/","\\")
            except:
                pass
            n += 1

    half_path = list(set(half_path))
    for i in range(len(half_path)):
        temp_encode = (half_path[i])
        try:
            os.chdir(temp_encode)       #os.chdir changes the current working directory to the given path.
            allexeList = (glob.glob("**/*.exe" , recursive= True))
            if(temp_encode[-1] != "\\"):
                full_path.extend( [os.sep.join([half_path[i], str(x)]) for x in allexeList])
            else:
                full_path.extend([f"{half_path[i]}{str(x)}" for x in allexeList])
        except Exception as e:
                pass
    full_path = list(set(full_path))

    # applications_dict = {}
    for file_path in full_path:
        name = os.path.basename(os.path.normpath(file_path)[:-4])
        location = file_path
        icon = get_icon(location,"large")
        applications_dict[name] = {}
        applications_dict[name]['location'] =  location
        applications_dict[name]['icon'] =  icon

    dump_tofile = open(current_directory+'\\search_collection.bin', 'wb') 
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

    # print(os.getcwd())
    dict_file = open("search_collection.bin", "rb")
    applications_dict = pickle.load(dict_file)
    search_result = {keys : {'location':applications_dict[keys]["location"], 'icon': applications_dict[keys]["icon"] } for keys in applications_dict.keys() if search_string.lower() in keys.lower()}
    return(search_result)

# windows_search_startmenu()
# windows_exe_search_registry()
# search_dict("valo")
