import winreg

import glob, os
# from os import getcwd, chdir
# r"E:\Games\SteamLibrary\steamapps\common\rocketleague\Binaries" , ".exe"


# os.chdir(r"C:\Users\hiper\AppData\Local\Discord")       #os.chdir changes the current working directory to the given path.
# ls = glob.glob("**/*.exe" , recursive= True)
# print(ls)

#Locations to get software paths from
    #HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Uninstall\         Uses "InstallLocation" for file location
    #HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Uninstall\        Uses "InstallLocation" for file location
    #HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\        Uses "InstallLocation" for file location        Could have uninstalled stuff locations as well
    #HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths              Uses "Path" for file location

#Connecting to a key in registry
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
                print(f_keys, repr(pathname) )
                half_path.append(pathname)
            # os.chdir(pathname)       #os.chdir changes the current working directory to the given path.
            # ls = glob.glob("**/*.exe" , recursive= True)
            # ls = [pathname + "\\" + str(x) for x in ls]
        except:
            pass
        n += 1


print("HALF_PATH :\n" ,half_path)
half_path = list(set(half_path))
for i in range(len(half_path)):
    temp_encode = (half_path[i])
    try:
        os.chdir(temp_encode)       #os.chdir changes the current working directory to the given path.
        allexeList = (glob.glob("**/*.exe" , recursive= True))
        if(temp_encode[-1] != "\\"):
            full_path.extend( [os.sep.join([half_path[i], str(x)]) for x in allexeList])
            print(len(full_path))
        else:
            full_path.extend([f"{half_path[i]}{str(x)}" for x in allexeList])
            print(len(full_path))
    except Exception as e:
            print("Error on :", temp_encode)
            print("Error name:", e)


full_path = list(set(full_path))        
print("FULL PATH :\n",full_path)
