from tkinter import *
from tkinter import ttk
from search_logic import search_dict
import win32api
import win32con
import win32gui
import winapps

################################################################################################################
#FOR TESTING
def printsome():
    print("henlo")
################################################################################################################

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

def make_button(widget,item_name,location,row_):
    item_name = item_name.ljust(600, " ")
    button_frame = Frame(widget, background = "#171717", borderwidth = 1, relief = FLAT)
    drawer_button = Button(button_frame, text = item_name , relief = FLAT, borderwidth=0, font = "Calibri 16", bg = "#171717", fg = 'white', activebackground="#363636" ,command = printsome, anchor="w")   #FOR TESTING
    
    drawer_button.bind("<Enter>" , lambda event : on_enter(drawer_button))
    drawer_button.bind("<Leave>" , lambda event : on_leave(drawer_button))
    
    button_frame.grid(row = row_ , column = 0, sticky = 'we')
    drawer_button.grid(row = 0 , column = 0, sticky = 'we')

# def make_button(widget,item_name,location,row_):
#     item_name = item_name.ljust(600, " ")
#     drawer_button = Button(widget, text = item_name , relief = FLAT, font = "Calibri 16", bg = "#171717",fg = 'white' ,command = printsome, anchor="w")   #FOR TESTING
#     drawer_button.grid(row = row_ , column = 0, sticky = 'we', pady= 8, padx=8)
#     drawer_button.config(highlightbackground='PINK')