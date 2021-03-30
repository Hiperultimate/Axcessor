from tkinter import *
from tkinter import ttk

from threading import Thread, Timer

import textwrap

import webbrowser

from search_logic import search_dict

from web_search import google_results

import win32api
import win32con 
import win32gui

from PIL import ImageTk 

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

def process_createbutton(my_frame,main_frame,dict_items, key_items):
    for row in range(len(dict_items.items())):
        #Here try except block handles overlapping of button creation 
        try:
            make_button(my_frame, key_items[row],dict_items[key_items[row]]['location'],dict_items[key_items[row]]['icon'], row)
        except:
            pass
    updateScrollRegion(main_frame, my_frame)

def process_webbuttons(top,my_frame,main_frame,dict_items, key_items):
    for row in range(len(dict_items.items())):
        web_button(top,my_frame,key_items[row] , dict_items[key_items[row]]['hyper_links'], dict_items[key_items[row]]['description'], row)
    updateScrollRegion(main_frame, my_frame)


def get_websearch_makebutton(web_search_text,top,my_frame,main_frame):
    results_=google_results(web_search_text)

    top.deiconify()

    button_thread = Thread(target = process_webbuttons, args = (top,my_frame,main_frame,results_, list(results_)))
    button_thread.start()

timer_function = Timer(1, lambda *args: None)
def search_result(top, search_string, my_frame, main_frame):

    #If search bar is empty
    if(search_string == "" or len(search_string.replace(" ","")) == 0):
        top.withdraw()
        return 
    
    if(search_string.lstrip()[:2] == "s/"):
        clear_frame(my_frame)

        search_value = search_string.lstrip()[2:]

        if(search_value == ""):
            return
        global timer_function
        timer_function.cancel()
        timer_function = Timer(0.3,get_websearch_makebutton,[search_value,top,my_frame,main_frame])
        timer_function.start()

        return

    #If search bar has some string then
    top.deiconify()
    search_string = search_string.lstrip()

    #Removes any existing widgets when the search bar is being typed with new words
    clear_frame(my_frame)

    dict_items = search_dict(search_string)
    key_items = list(dict_items)

    #This thread removes the hanging of program while typing because threading does not interfere with tkinter's loop.
    button_thread = Thread(target = process_createbutton, args = (my_frame,main_frame,dict_items, key_items))
    button_thread.start()

def on_enter(button_name,canvas_name):
    button_name.configure(background="#363636")
    canvas_name.configure(background="#363636")

def on_leave(button_name,canvas_name):
    button_name.configure(background="#171717")
    canvas_name.configure(background="#171717")

def browse_click(url):
    print(url)
    webbrowser.open(url, new=0, autoraise=True)

#Here "images" variable is used to store the references of icons. Without it icons will not be displayed.
images = set()
def make_button(widget,item_name,location,icon,row_):
    icon = ImageTk.PhotoImage(icon)
    images.add(icon)


    item_name = item_name.ljust(600, " ")
    button_frame = Frame(widget, background = "#171717", borderwidth = 1, relief = FLAT)
    icon_canv = Canvas(button_frame, width= 50, height=40, background= "#171717",bd=0, highlightthickness=0,relief='ridge')      #testing
    drawer_button = Button(button_frame, text = item_name , relief = FLAT, borderwidth=0, font = "Calibri 16", bg = "#171717", fg = 'white', activebackground="#363636" ,command = printsome, anchor="w")   #FOR TESTING
    
    drawer_button.bind("<Enter>" , lambda event : on_enter(drawer_button,icon_canv))
    drawer_button.bind("<Leave>" , lambda event : on_leave(drawer_button,icon_canv))

    icon_canv.create_image(25 , 20 , anchor=CENTER, image=icon)
    button_frame.grid(row = row_ , column = 0, sticky = 'we')
    icon_canv.grid(row = 0 , column = 1)
    drawer_button.grid(row = 0 , column = 2, sticky = 'we')

def web_button(top, widget, item_heading,item_url,item_description,row_):
    item_description = "\n".join(textwrap.wrap(item_description,width = 95)) + " "*200

    item_heading = item_heading.ljust(600, " ")
    # button_frame = Canvas(widget, width= 200, height=500, background= "#FFFFFF",bd=0, highlightthickness=0,relief='ridge')
    button_frame = Frame(widget, background = "#171717", borderwidth = 3, relief = FLAT)
    heading_text = Label(button_frame, text = item_heading,anchor=NW,justify=LEFT, bg = "#171717",font = "Calibri 18",fg = 'white')
    description_text = Label(button_frame, text = item_description,anchor=NW, justify=LEFT, bg = "#171717",font = "Calibri 14",fg = 'white')
    # button_frame = Frame(widget, background = "#171717", borderwidth = 1, relief = FLAT)
    # drawer_button = Button(button_frame, text = item_heading , relief = FLAT, borderwidth=0, font = "Calibri 16", bg = "#171717", fg = 'white', activebackground="#363636" ,command = printsome, anchor="w")   #FOR TESTING
    # print(item_heading)
    # print(item_url)
    # print(item_description)

    button_frame.bind("<Enter>" , lambda event : on_enter(heading_text,description_text))
    button_frame.bind("<Leave>" , lambda event : on_leave(heading_text,description_text))
    heading_text.bind("<Button-1>" , lambda event : browse_click(item_url))
    description_text.bind("<Button-1>" , lambda event : browse_click(item_url))

    button_frame.grid(row = row_ , column = 0, sticky = 'we')
    
    heading_text.grid(row=0,column=0,sticky="w")
    description_text.grid(row=1,column=0,sticky="w")
    # heading_text.pack(side=LEFT)
    # description_text.pack(side=LEFT)

    # Grid.rowconfigure(button_frame,row_,weight=1)

    # drawer_button.grid(row = 0 , column = 0, sticky = N+S+E+W )
