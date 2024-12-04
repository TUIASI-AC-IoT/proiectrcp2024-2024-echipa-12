import time
import tkinter as tk
from util import uiupdateQ, actionQ
import customtkinter as ctk

def ui():
    def updateUI(folder_icon, file_icon,delete_item_icon):
        for widget in fileframe.winfo_children():
            widget.destroy()
        actionQ.put('ls')
        btn = ctk.CTkButton(
            fileframe,
            text="..",
            width=600,
            height=10,
            fg_color='#191919',
            image=folder_icon,
            command=lambda filename="..": (actionQ.put(f"cd@{filename}"), updateUI(folder_icon, file_icon,delete_item_icon)),# filename)),
            font=("Arial", 18),
            compound=ctk.LEFT,
            anchor="w",
            hover_color="#505050",
            corner_radius=0,
        )
        btn.grid(row=1,column=0)
        data = None
        while uiupdateQ.qsize() != 0:
            data = uiupdateQ.get()
        print(data)
        if data is not None:
            data = data.split('\n')
            files = []
            folders = []
            for i in data:
                if i != "":
                    if 'File: ' in i:
                        files.append(i.split('File: ')[1])
                    else:
                        folders.append(i.split('Folder: ')[1])
            j=1
            for i in folders:
                j=j+1
                btn = ctk.CTkButton(
                    fileframe,
                    text=i,
                    width=600,
                    height=10,
                    fg_color='#191919',
                    image=folder_icon,
                    command=lambda filename=i: (actionQ.put(f"cd@{filename}"),updateUI(folder_icon, file_icon,delete_item_icon)),#filename)),
                    font=("Arial", 18),
                    compound=ctk.LEFT,
                    anchor="w",
                    hover_color="#505050",
                    corner_radius=0,
                    # border_width=1,
                    # border_color='white',
                )
                btn.grid(row=j,column=0)
                #buton pentru stergere fisier
                delete_btn = ctk.CTkButton(
                    fileframe,
                    text="",
                    width=32,
                    height=32,
                    image=delete_item_icon,
                    fg_color='#191919',
                    command=lambda filename=i: (actionQ.put(f"rmdir@{filename}"),updateUI(folder_icon, file_icon,delete_item_icon)),
                    # filename)),
                    font=("Arial", 18),
                    compound=ctk.LEFT,
                    anchor="w",
                    hover_color="#505050",
                    corner_radius=0,
                    # border_width=1,
                    # border_color='white',
                )
                delete_btn.grid(row=j, column=1)
                #======================================
            for i in files:
                j=j+1
                btn = ctk.CTkButton(
                    fileframe,
                    text=i,
                    width=600,
                    height=10,
                    fg_color='#191919',
                    image=file_icon,
                    command=lambda: actionQ.put("cd@i"),
                    font=("Arial", 18),
                    compound=ctk.LEFT,
                    anchor="w",
                    hover_color="#505050",
                    corner_radius=0,
                    # border_width=1,
                    # border_color='white',
                )
                btn.grid(row=j, column=0)
                #buton pentru stergere fisier
                delete_btn = ctk.CTkButton(
                    fileframe,
                    text="",
                    width=32,
                    height=32,
                    fg_color='#191919',
                    image=delete_item_icon,
                    command=lambda filename=i: (actionQ.put(f"rm@{filename}"), updateUI(folder_icon, file_icon,delete_item_icon)),
                    # filename)),
                    font=("Arial", 18),
                    compound=ctk.LEFT,
                    anchor="w",
                    hover_color="#505050",
                    corner_radius=0,
                    # border_width=1,
                    # border_color='white',
                )
                delete_btn.grid(row=j, column=1)

    root = ctk.CTk(fg_color="#191919")
    root.title("Controlul Fluxului Prin Fereastra Glisanta - Lefter Andrei, Georgiana Stefania Zaharia =^._.^=")
    root.geometry("1280x720")
    root.resizable(False, False)

    #icon image source: https://www.freepik.com/icon/folder_7743796
    icon = tk.PhotoImage(file='icon.png')

    root.wm_iconbitmap() #n am idee de ce nu se schimba iconita daca nu e asta sincer
    root.iconphoto(False, icon)

    fileframe = ctk.CTkScrollableFrame(root, width=1200, height=450, corner_radius=0, fg_color='#191919')
    fileframe.place(x=34, y=20)

    folder_icon = tk.PhotoImage(file='folders2.png')
    file_icon = tk.PhotoImage(file='files.png')#https://www.pngwing.com/en/free-png-mflca
    delete_item_icon=tk.PhotoImage(file='delete_icon.png')
    updateUI(folder_icon, file_icon,delete_item_icon)

    root.mainloop()
