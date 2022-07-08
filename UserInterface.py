import tkinter as tk
from tkinter import ttk

import SpyderlingFactory
import JDSeleniumSpyderling

root = tk.Tk()

# Change the title and icon of the program
root.title("Spyderling")
root.iconbitmap("./spider.ico")

# Place a label of the program name on the root window
web = tk.Label(root, text="Webpage Selection")
web.pack()


def continue_button_clicked():
    controller = SpyderlingFactory.new_spyderling('JD', "all", {
        "seller": True,
        "price": True,
        "title": True,
    })
    controller.front_page_search('壮阳')
    controller.searched_page_search('壮阳免疫力')
    controller.extract_info()

    JDSeleniumSpyderling.end(controller.get_driver())


button = ttk.Button(root, text='Continue', command=continue_button_clicked)
button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)

# Sets the window size
root.geometry('640x360+50+50')

root.mainloop()
