from tkinter import *
from tkinter import ttk

from search_logic import search_dict

from win32com.shell import shell, shellcon  
import win32api
import win32con
import win32ui  
import win32gui

from PIL import Image, ImageTk 

################################################################################################################
#FOR TESTING
def printsome():
    print("henlo")
################################################################################################################

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

def updateScrollRegion(main_frame, my_canvas):
	main_frame.update_idletasks()
	main_frame.config(scrollregion=my_canvas.bbox())

#Call this function to set focus of the pointer to the search bar 
altkey = 0x12
set_to_foreground = win32gui.SetForegroundWindow    #SetForegroundWindow :- https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setforegroundwindow
def steal_focus(root, search_bar):
    win32api.keybd_event(altkey, 0,0,0)     #Alt Key down           keybd_event is used for virutal key press and unpress
    set_to_foreground(root.winfo_id())      # root.winfo_id() is a system-specific window identifier
    win32api.keybd_event(altkey, 0, win32con.KEYEVENTF_KEYUP ,0)     #Alt Key up
    search_bar.focus_set()

def clear_frame(full_frame):
    # destroy all widgets from frame
    for widget in full_frame.winfo_children():
        widget.destroy()
    
    # this will clear frame and frame will be empty
    # if you want to hide the empty panel then
    full_frame.pack_forget()

# def search_result(root, top, search_string, my_canvas, my_scrollbar, second_frame):
def search_result(top, search_string, my_frame, main_frame):

    #If search bar is empty
    if(search_string == "" or len(search_string.replace(" ","")) == 0):
        top.withdraw()
        return 

    #If search bar has some string
    top.deiconify()
    search_string = search_string.lstrip()

    #Removes any existing widgets when the search bar is being typed with new words
    clear_frame(my_frame)

    dict_items = search_dict(search_string)
    key_items = list(dict_items)
    for row in range(len(dict_items.items())):
        make_button(my_frame, key_items[row],dict_items[key_items[row]], row)

    updateScrollRegion(main_frame, my_frame)

def on_enter(button_name):
    button_name['background'] = "#363636"

def on_leave(button_name):
    button_name['background'] = "#171717"

#Make sure the icon location object exists 
    #Maybe its better to save the icons and load them here
images = []
def make_button(widget,item_name,location,row_):

    icon = ImageTk.PhotoImage(get_icon(location,"large"))
    images.append(icon)
    print(type(icon), location)


    item_name = item_name.ljust(600, " ")
    button_frame = Frame(widget, background = "#171717", borderwidth = 1, relief = FLAT)
    icon_canv = Canvas(button_frame, width= 80, height=80)      #testing
    drawer_button = Button(button_frame, text = item_name , relief = FLAT, borderwidth=0, font = "Calibri 16", bg = "#171717", fg = 'white', activebackground="#363636" ,command = printsome, anchor="w")   #FOR TESTING
    
    drawer_button.bind("<Enter>" , lambda event : on_enter(drawer_button))
    drawer_button.bind("<Leave>" , lambda event : on_leave(drawer_button))

    icon_canv.create_image(20 , 20 , anchor=NW, image=icon)
    button_frame.grid(row = row_ , column = 0, sticky = 'we')
    icon_canv.grid(row = 0 , column = 1)
    drawer_button.grid(row = 0 , column = 2, sticky = 'we')

# def make_button(widget,item_name,location,row_):
#     item_name = item_name.ljust(600, " ")
#     drawer_button = Button(widget, text = item_name , relief = FLAT, font = "Calibri 16", bg = "#171717",fg = 'white' ,command = printsome, anchor="w")   #FOR TESTING
#     drawer_button.grid(row = row_ , column = 0, sticky = 'we', pady= 8, padx=8)
#     drawer_button.config(highlightbackground='PINK')