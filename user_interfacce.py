import os
import time
import tkinter as tk
from util import uiupdateQ, actionQ
import customtkinter as ctk
from tkinter import filedialog


def ui():
    def updateUI(folder_icon, file_icon,delete_item_icon,download_icon):
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
            command=lambda filename="..": (actionQ.put(f"cd@{filename}"), updateUI(folder_icon, file_icon,delete_item_icon,download_icon)),# filename)),
            font=("Arial", 18),
            compound=ctk.LEFT,
            anchor="w",
            hover_color="#505050",
            corner_radius=0,
        )
        btn.grid(row=1,column=0)
        data = None

        print("aici iau din q:", time.time() * 100 % 10000)
        data = uiupdateQ.get()
        print(data)
        print("aici e ce e in q:", data , "\n", time.time() * 100 % 10000)
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
                    command=lambda filename=i: (actionQ.put(f"cd@{filename}"),updateUI(folder_icon, file_icon,delete_item_icon,download_icon)),#filename)),
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
                    width=30,
                    height=32,
                    image=delete_item_icon,
                    fg_color='#191919',
                    command=lambda filename=i: (actionQ.put(f"rmdir@{filename}"),updateUI(folder_icon, file_icon,delete_item_icon,download_icon)),
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
                    width=30,
                    height=32,
                    fg_color='#191919',
                    image=delete_item_icon,
                    command=lambda filename=i: (actionQ.put(f"rm@{filename}"), updateUI(folder_icon, file_icon,delete_item_icon,download_icon)),
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
                download_btn = ctk.CTkButton(
                    fileframe,
                    text="Download",
                    width=30,
                    height=32,
                    fg_color='#191919',
                    image=download_icon,
                    #command=lambda filename=i: (),
                    # filename)),
                    font=("Arial", 18),
                    compound=ctk.LEFT,
                    anchor="w",
                    hover_color="#505050",
                    corner_radius=0,
                    # border_width=1,
                    # border_color='white',
                )
                download_btn.grid(row=j, column=2)

    def get_text(textbox) -> str:
        text=textbox.get("0.0", "end")
        return text

    def take_file_path(): #pune in variabila globala path-ul fisierului ales
        global upload_file_path
        upload_file_path = filedialog.askopenfilename(filetypes=[("File", "*.*")],
                                              initialdir="C:/",
                                              title="Load file")
        print(upload_file_path)

    root = ctk.CTk(fg_color="#191919")
    root.title("Controlul Fluxului Prin Fereastra Glisanta - Lefter Andrei, Georgiana Stefania Zaharia =^._.^=")
    root.geometry("1280x720")
    #root.resizable(False, False)

    #icon image source: https://www.freepik.com/icon/folder_7743796
    icon = tk.PhotoImage(file='icon.png')

    root.wm_iconbitmap() #n am idee de ce nu se schimba iconita daca nu e asta sincer
    root.iconphoto(False, icon)

    fileframe = ctk.CTkScrollableFrame(root, width=1200, height=450, corner_radius=0, fg_color='#191919', border_width=2, border_color='#555555')
    fileframe.place(x=34, y=20)
    # =====casuta text
    textbox = ctk.CTkTextbox(root, width=300, height=32, font=("Arial", 18))
    textbox.place(x=150, y=500)
    textbox.insert("0.0", "new")
    new_file_name = textbox.get("0.0", "end").strip()
    textbox.delete("0.0", "end")
    # ========
    # buton creare fisier
    btn_new_file = ctk.CTkButton(
        root,
        text="New Folder:",
        width=30,
        height=32,
        fg_color='#191919',
        image="",
        command=lambda: (actionQ.put(f"mkdir@{get_text(textbox)}"), updateUI(folder_icon, file_icon, delete_item_icon,download_icon)),
        # filename)),
        font=("Arial", 18),
        compound=ctk.LEFT,
        anchor="w",
        hover_color="#505050",
        corner_radius=0,
        border_width=1,
        border_color='white',
    )
    btn_new_file.place(x=30, y=500)

    upload_icon = tk.PhotoImage(
        file='upload_icon.png')  # https://www.veryicon.com/icons/miscellaneous/general-icon-12/upload-upload-4.html
    btn_upload = ctk.CTkButton(
        root,
        text="Upload",
        width=80,
        height=32,
        fg_color='#191919',
        image=upload_icon,
        command=take_file_path,  # filename)),
        font=("Arial", 18),
        compound=ctk.LEFT,
        anchor="w",
        hover_color="#505050",
        corner_radius=0,
        border_width=1,
        border_color='white',
    )
    btn_upload.place(x=615, y=500)

    # ===============

    folder_icon = tk.PhotoImage(file='folders2.png')
    file_icon = tk.PhotoImage(file='files.png')#https://www.pngwing.com/en/free-png-mflca
    delete_item_icon=tk.PhotoImage(file='remove.png') #
    download_icon=tk.PhotoImage(file='download.png') #https://www.veryicon.com/icons/miscellaneous/general-icon-12/download-download-3.html
    # upload_icon=tk.PhotoImage(file='upload_icon.png') #https://www.veryicon.com/icons/miscellaneous/general-icon-12/upload-upload-4.html

    updateUI(folder_icon, file_icon,delete_item_icon,download_icon)

    root.mainloop()
