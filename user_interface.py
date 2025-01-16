import math
import queue
import threading
import time
import tkinter as tk
import warnings

from transfer_util import util, threads
from transfer_util.util import uiupdateQ, actionQ
import customtkinter as ctk
from tkinter import filedialog
import os

folder_icon = None
file_icon = None
delete_item_icon = None
download_icon = None

def ui():
    def get_savelocation():
        util.path = f"{filedialog.askdirectory(initialdir='./', title='Where do you want to save the file?')}"
    def update_progressbar():
        if util.sending_flag == 1:
            progressbar.place(x=615, y=600)
            try:
                progress = util.progressQ.get_nowait()
                progressbar.set(progress)
               # print(progress)
                progress_title.configure(text=f"UPLOAD PROGRESS {progress*100:.0f}%")
            except queue.Empty:
                pass
        elif util.sending_flag == 2:
            progressbar.place(x=615, y=600)
            try:
                progress = util.progressQ.get_nowait()
                progressbar.set(progress)
                # print(progress)
                progress_title.configure(text=f"DOWNLOAD PROGRESS {progress * 100:.0f}%")
            except queue.Empty:
                pass
        elif util.sending_flag == 0:
            #progressbar.place_forget()
            progress_title.configure(text="No Transfer")
            progressbar.set(0)

        root.after(50, update_progressbar)

    warnings.filterwarnings("ignore", module="customtkinter.*")
    global file_to_transfer
    def updateUI(folder_icon, file_icon,delete_item_icon,download_icon):

        for widget in fileframe.winfo_children():
            widget.destroy()
        actionQ.put('c@ls')
        btn = ctk.CTkButton(
            fileframe,
            text="..",
            width=600,
            height=10,
            fg_color='#191919',
            image=folder_icon,
            command=lambda filename="..": (actionQ.put(f"c@cd@{filename}"), updateUI(folder_icon, file_icon,delete_item_icon,download_icon)),# filename)),
            font=("Arial", 18),
            compound=ctk.LEFT,
            anchor="w",
            hover_color="#505050",
            corner_radius=0,
        )
        btn.grid(row=1,column=0)
        data = None

        #print("aici iau din q:", time.time() * 100 % 10000)
        data = uiupdateQ.get()
        #print("aici e ce e in q:", data , "\n", time.time() * 100 % 10000)
        if data is not None:
            data = data.split('\n')
            files = []
            folders = []
            for i in data:
                if i != "":
                    if 'File: ' in i:
                        try:
                            files.append(i.split('File: ')[1])
                        except IndexError:
                            files = []
                    else:
                        try:
                            folders.append(i.split('Folder: ')[1])
                        except IndexError:
                            files = []
            # print(files)
            # print(folders)
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
                    command=lambda filename=i: (actionQ.put(f"c@cd@{filename}"),updateUI(folder_icon, file_icon,delete_item_icon,download_icon)),#filename)),
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
                    command=lambda filename=i: (actionQ.put(f"c@rmdir@{filename}"),updateUI(folder_icon, file_icon,delete_item_icon,download_icon)),
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
                    command=lambda: None,#actionQ.put("cd@i"),
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
                    command=lambda filename=i: (actionQ.put(f"c@rmdir@{filename}"), updateUI(folder_icon, file_icon,delete_item_icon,download_icon)),
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
                    command=lambda filename = i: (get_savelocation(), print("saveloc: ", util.path) ,actionQ.put(f'c@down@{filename}')),
                    # filename)),
                    font=("Arial", 18),
                    compound=ctk.LEFT,
                    anchor="w",
                    hover_color="#505050",
                    corner_radius=0,
                    # border_width=1,
                    # border_width=1,
                    # border_color='white',
                )
                download_btn.grid(row=j, column=2)

    def get_text(textbox) -> str:
        text=textbox.get("0.0", "end")
        return text

    def take_file_path(textbox_element): #pune in variabila globala path-ul fisierului ales
       textbox_element.delete("0.0", "end")
       util.file_to_transfer = filedialog.askopenfilename(filetypes=[("File", "*.*")],
                                              initialdir="./",
                                              title="Load file")
       textbox_element.insert("0.0",  util.file_to_transfer)


    root = ctk.CTk(fg_color="#191919")
    root.title("Controlul Fluxului Prin Fereastra Glisanta - Lefter Andrei, Georgiana Stefania Zaharia =^._.^=")
    root.geometry("1280x720")
    #root.resizable(False, False)

    #icon image source: https://www.freepik.com/icon/folder_7743796
    icon = tk.PhotoImage(file='icons/icon.png')

    root.wm_iconbitmap() #n am idee de ce nu se schimba iconita daca nu e asta sincer
    root.iconphoto(False, icon)

    fileframe = ctk.CTkScrollableFrame(root, width=1200, height=450, corner_radius=0, fg_color='#191919', border_width=2, border_color='#555555')
    fileframe.place(x=34, y=20)
    # =====casuta text
    textbox = ctk.CTkTextbox(root, width=360, height=32, fg_color='#383838', font=("Arial", 18))
    textbox.place(x=155, y=500)
    textbox.insert("0.0", "new")
    new_file_name = textbox.get("0.0", "end").strip()
    textbox.delete("0.0", "end")
    # ========
    # buton creare FOLDER
    btn_new_file = ctk.CTkButton(
        root,
        text="New Folder:",
        width=30,
        height=32,
        fg_color='#191919',
        image="",
        command=lambda: (actionQ.put(f"c@mkdir@{get_text(textbox)}"), updateUI(folder_icon, file_icon, delete_item_icon,download_icon)),
        # filename)),
        font=("Arial", 18),
        compound=ctk.LEFT,
        anchor="w",
        hover_color="#505050",
        corner_radius=5,
        border_width=1,
        border_color='white',
    )
    btn_new_file.place(x=30, y=500) # E FOLDEEEEEEEEEEEEEER

    #======= upload buttons
    upload_icon = tk.PhotoImage(file='icons/upload_icon.png')  # https://www.veryicon.com/icons/miscellaneous/general-icon-12/upload-upload-4.html
    filepath_textbox = ctk.CTkTextbox(root, width=300, height=32, fg_color='#383838', font=("Arial", 18))
    filepath_textbox.place(x=750, y=500)
    filepath_textbox.insert("0.0", " ")
    #file_to_transfer = textbox.get("0.0", "end").strip()
    #filepath_textbox.delete("0.0", "end")
    btn_choose_file = ctk.CTkButton(
        root,
        text="Choose File...",
        width=80,
        height=32,
        fg_color='#191919',
        #image=upload_icon,
        command=lambda fp=filepath_textbox: take_file_path(fp),  # filename)),
        font=("Arial", 18),
        compound=ctk.LEFT,
        anchor="w",
        hover_color="#505050",
        corner_radius=5,
        border_width=1,
        border_color='white',
    )
    btn_choose_file.place(x=615, y=500)
    btn_upload = ctk.CTkButton(
        root,
        text="Upload",
        width=80,
        height=32,
        fg_color='#191919',
        image=upload_icon,
        command= lambda: (
                actionQ.put(f'c@up@{os.path.basename(util.file_to_transfer)}@{math.ceil(os.path.getsize(util.file_to_transfer)/util.packet_data_size)}') if util.file_to_transfer else None,
        ),#lambda fp=filepath_textbox: take_file_path(fp),  # filename)),
        font=("Arial", 18),
        compound=ctk.LEFT,
        anchor="w",
        hover_color="#505050",
        corner_radius=5,
        border_width=1,
        border_color='white',
    )
    btn_upload.place(x=1015, y=500)
    ####################################################
    #packetloss %
    ####################################################
    def update_pack_loss(value):
        util.packet_loss = value

    title_slider = ctk.CTkLabel(root, text="Packet Loss Percentage:", font=("Arial", 18))
    title_slider.place(x=30, y=552)
    var = tk.IntVar()
    var.set(util.packet_loss)
    packloss=ctk.CTkSlider(
        root,
        from_=0,
        to=100,
        number_of_steps=10,
        orientation=ctk.HORIZONTAL,
        variable = var,
        button_color = '#c7c8c9',
        button_hover_color= '#FFFFFF',
        button_corner_radius= 3,
        command=lambda value: (update_pack_loss(var.get()), actionQ.put(f'c@cs@packetloss@{util.packet_loss}'))
    )


    packloss.place(x=320,y=560)
    slider_val = ctk.CTkLabel(root, textvariable=var, font=("Arial", 18))
    slider_val.place(x=290,y=553)
    # ===============

    ####################################################
    # TIMEOUT
    ####################################################
    def update_timeout(value):
        util.timeout = float(value)

    title_slider2 = ctk.CTkLabel(root, text="Timeout:", font=("Arial", 18))
    title_slider2.place(x=155, y=582)
    var2 = tk.DoubleVar()
    var2.set(util.timeout)
    timeout = ctk.CTkSlider(
        root,
        from_=0,
        to=20,
        number_of_steps=80,
        orientation=ctk.HORIZONTAL,
        variable = var2,
        button_color = '#c7c8c9',
        button_hover_color= '#FFFFFF',
        button_corner_radius= 0,
        command=lambda value: (update_timeout(var2.get()), actionQ.put(f'c@cs@timeout@{util.timeout}'))
    )

    timeout.place(x=320, y=590)
    slider_val2 = ctk.CTkLabel(root, textvariable=var2, font=("Arial", 18))
    slider_val2.place(x=290, y=583)
    #===============

    ####################################################
    # WINDOW SIZE
    ####################################################
    def update_size(value):
        util.window_size = int(value)

    title_slider3 = ctk.CTkLabel(root, text="Window Size:", font=("Arial", 18))
    title_slider3.place(x=117, y=612)
    var3 = tk.IntVar()
    var3.set(util.window_size)
    wndsize = ctk.CTkSlider(
        root,
        from_=1,
        to=15,
        number_of_steps=14,
        orientation=ctk.HORIZONTAL,
        variable=var3,
        button_color='#c7c8c9',
        button_hover_color='#FFFFFF',
        button_corner_radius=5,
        command=lambda value: (update_size(var3.get()), actionQ.put(f'c@cs@window_size@{util.window_size}'))
    )

    wndsize.place(x=320, y=620)
    slider_val3 = ctk.CTkLabel(root, textvariable=var3, font=("Arial", 18))
    slider_val3.place(x=290, y=613)
    # ===============
    # global folder_icon, file_icon, delete_item_icon, download_icon
    folder_icon = tk.PhotoImage(file='icons/folders2.png')
    file_icon = tk.PhotoImage(file='icons/files.png')#https://www.pngwing.com/en/free-png-mflca
    delete_item_icon = tk.PhotoImage(file='icons/remove.png') #
    download_icon = tk.PhotoImage(file='icons/download.png') #https://www.veryicon.com/icons/miscellaneous/general-icon-12/download-download-3.html

    #PROGRESSBAR
    progress_title = ctk.CTkLabel(
        root,
        text="Progress",
        font=("Arial", 18)
    )
    progress_title.place(x=615, y=575)
    progressbar = ctk.CTkProgressBar(
        master=root,
        height=15,
        width=505,
        corner_radius=0,
        fg_color='#383838',
        progress_color='#FFFFFF'
    )
    progressbar.set(0)
    progressbar.place(x=615, y=600)
    # ================
    updateUI(folder_icon, file_icon,delete_item_icon,download_icon)
    update_progressbar()

    # update_progressbar()

    # thread = threading.Thread(target=update_progressbar)
    # thread.start()

    def closing_cbk(root): #https://stackoverflow.com/questions/71992792/tkinter-based-app-keeps-running-in-the-background-if-the-window-is-closed-abrupt
        print("closing tkinter")
        time.sleep(1)
        global folder_icon, file_icon, delete_item_icon, download_icon
        folder_icon = None
        file_icon = None
        delete_item_icon = None
        download_icon = None
        root.quit()
        root.destroy()
        util.shutdown_event.set()
        print("closing tkinter threads")

    root.protocol("WM_DELETE_WINDOW", lambda: closing_cbk(root))
    root.mainloop()
    return
