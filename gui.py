from tkinter import *
from tkinter import ttk
from logic import steal_focus, search_result
import win32api
import win32con
import win32gui
import time
import threading

from search_logic import windows_exe_search_registry, windows_search_startmenu


root = Tk()

root.overrideredirect(True)
root.configure(background='black')

#Search Bar Size
Screen_Width = root.winfo_screenwidth()
Screen_Height = root.winfo_screenheight()
x_size = 600 + Screen_Width/9
y_size = 35 + Screen_Height/36
x_pos = Screen_Width/2 - x_size/2
y_pos = Screen_Height/2 - y_size/2 - Screen_Height/5
root.geometry("%dx%d+%d+%d" % (x_size,y_size,x_pos,y_pos))
# print(x_size,y_size,x_pos,y_pos)

#Search Drawer
top = Toplevel(root, bg = 'black')
top.overrideredirect(True)
Screen_Width = root.winfo_screenwidth()
Screen_Height = root.winfo_screenheight()
x_size = 600 + Screen_Width/9  
y_size = 300 + Screen_Height/36     #For testing
y_pos = Screen_Height/2 - y_size/2 - Screen_Height/8 + 135     #For testing
x_pos = Screen_Width/2 - x_size/2
top.geometry("%dx%d+%d+%d" % (x_size,y_size,x_pos,y_pos))

#All Created Widgets block
searchbar_border = Frame(root, background = '#555555', borderwidth = 1, relief = FLAT)
search_bar = Entry(searchbar_border, font = "Calibri 24" , bg = "#171717", relief = FLAT ,fg = 'white',insertbackground='white')

#All Widget Pushed block
searchbar_border.grid(row = 0 , column = 0, sticky = 'we')
search_bar.grid(row = 0 , column = 0, ipady = 10, sticky = 'we')


#Search Drawer Configurations
main_frame = Canvas(top, background = '#171717')
my_frame = Frame(main_frame, background = '#171717')
my_scrollbar = ttk.Scrollbar(top)
main_frame.config(yscrollcommand=my_scrollbar.set, highlightthickness=0)
my_scrollbar.config(orient=VERTICAL, command=main_frame.yview)
my_scrollbar.pack(fill=Y , side = RIGHT, expand = FALSE)
main_frame.pack(fill = BOTH, side = LEFT, expand = TRUE)
main_frame.create_window(0, 0, window=my_frame, anchor=NW)

#Scrollwheel bind to scrolling
def _on_mousewheel( event):
    main_frame.yview_scroll(int(-1*(event.delta/120)), "units")
top.bind_all("<MouseWheel>",_on_mousewheel)

#Grid Config Block
searchbar_border.grid_columnconfigure(0, weight = 1)
root.grid_columnconfigure(0, weight=1)
top.grid_columnconfigure(0, weight=8)

#Checks if search_collection exists or not. If not, then creates one.
try:
    dict_file = open("search_collection.bin", "rb")
    dict_file.close()
except FileNotFoundError:
    windows_search_startmenu()
    windows_exe_search_registry()

#This function detects the hotkey (shift+ctrl) and will be used to open and close up the program's GUI
def open_close():
    toggling = 1
    once_counter = 0    #Stops toggling code to run more than once after toggling changes
    while True:
        if(win32api.GetAsyncKeyState(win32con.VK_LWIN) == -32768 and win32api.GetAsyncKeyState(win32con.VK_SHIFT) == -32768):
            if(toggling == 1):
                toggling = 0 
                top.withdraw()
                search_bar.delete(0,'end')  #Deletes all text from the entry once the axcessor is minimized.
            elif(toggling == 0):
                toggling = 1
            print("Activated :" , toggling)
            while(win32api.GetAsyncKeyState(win32con.VK_LWIN) == -32768 or win32api.GetAsyncKeyState(win32con.VK_SHIFT) == -32768):
                continue
        if(toggling == 0):
            if(once_counter == 1):
                root.withdraw()
                top.withdraw()
                once_counter = 0
        elif(toggling == 1):
            search_bar.bind("<KeyRelease>" , lambda event : search_result(top, search_bar.get(),my_frame, main_frame))        #Checks if the keyboard is pressing any keys or not
            if(once_counter == 0):
                search_bar.delete(0,'end')
                steal_focus(root,search_bar)
                root.deiconify()
                top.deiconify()
                once_counter = 1
        time.sleep(0.01)

#Creates a thread for open_close() function and runs it for entirety of this program
HotKeyFuncThread = threading.Thread(target = open_close)
HotKeyFuncThread.start()

top.mainloop()
root.mainloop()