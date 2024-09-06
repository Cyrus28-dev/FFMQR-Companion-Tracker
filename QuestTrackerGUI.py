
import tkinter as tk
from tkinter import filedialog
import re

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.gameinfo = None
        self.processed_text =  tk.StringVar()
        self.display_label = tk.Label(self.root, textvariable=self.processed_text, bg="#000000", fg="white", anchor="w", justify="left")
        self.companions = {
            "kaeli": {
                "active": True,
                "quests": [],
                "spells": []
            },
            "tristam": {
                "active": True,
                "quests": [],
                "spells": []
            },
            "phoebe": {
                "active": True,
                "quests": [],
                "spells": []
            },
            "reuben": {
                "active": True,
                "quests": [],
                "spells": []
            },
        }

    def create_menu(self):
        menubar = tk.Menu(self.root, tearoff=0)

        menu_file = tk.Menu(menubar, tearoff=0)
        menu_help = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label="Import..", command=self.file_menu_open)

        menubar.add_cascade(menu=menu_help, label='Help')

        self.root['menu'] = menubar

    def file_menu_open(self):
        file_types = [
            ("FFMQR GameInfo File", "*.txt")
        ]
        f = filedialog.askopenfile(initialdir="/", filetypes=file_types, mode="r")

        if (f):
            file = [line.rstrip() for line in f]
            f.close()

            if (file[0][0:5]) == "FFMQR":
                # valid gameinfo file
                self.gameinfo = file
                self.process_gameinfo()
                self.generate_text()
            else:
                tk.messagebox.showerror(title="Invalid gameinfo file!", message="Invalid GameInfo file selected. File does not start with the string \"FFMQR\").")
            
    def process_gameinfo(self):
        mode = None
        companion = None
        self.companions_reset()
        

        for line in self.gameinfo:
            companions = re.search(r"\[(\w+)\]", line)
            quest = re.search(r"\d. (\w+.*)", line)
            spells = re.search(r"Spells: (\w+ \(\w+ \d+\).*)", line)

            if companions:
                mode = "companion_mode"
                companion = str(companions.group(1)).lower()

            if mode == "companion_mode":
                if spells:
                    spells_list = spells.group(1).split(", ")

                    for item in spells_list:
                        item = item.replace("Seal", "")
                        item = item.replace("Book", "")
                        self.companions[companion]["spells"].append(item)

                if "Nothing here" in line:
                    self.companions[companion]["active"] = False

                if quest:
                    self.companions[companion]["quests"].append(quest.group(1))
        
        print(self.companions)

    def generate_text(self):
        self.open_button.destroy()

        temp_txt = ""
        self.processed_text.set("")
        indent = "  "

        for key, values in self.companions.items():
            if values["active"] == True:
                temp_txt += str(key).capitalize() + "\n"
                temp_txt += ("-" * (len(str(key))+ 2)) + "\n"

                if values["quests"]:
                    temp_txt += indent + "Quests: \n"
                    
                    for item in values["quests"]:
                        temp_txt += indent + indent + "- " + item + "\n"
                    
                    temp_txt += "\n"

                if values["spells"]:
                    temp_txt += indent + "Spells: \n"

                    for item in values["spells"]:
                        temp_txt += indent + indent + "- " + item + "\n"

                temp_txt += "\n"


        self.processed_text.set(temp_txt)
        self.display_label.destroy()
        self.display_label = tk.Label(self.root, textvariable=self.processed_text, bg="#000000", fg="white", anchor="w", justify="left")
        self.display_label.pack()

    def companions_reset(self):
        self.companions = {
            "kaeli": {
                "active": True,
                "quests": [],
                "spells": []
            },
            "tristam": {
                "active": True,
                "quests": [],
                "spells": []
            },
            "phoebe": {
                "active": True,
                "quests": [],
                "spells": []
            },
            "reuben": {
                "active": True,
                "quests": [],
                "spells": []
            },
        }

    def setup(self):
        self.create_menu()
        self.root.minsize(300, 50)
        self.root.configure(background='black')
        self.root.title("FFMQR Quest Tracker")

        self.open_button = tk.Button(self.root, text='Click here to import a GameInfo file!', anchor="center", command=self.file_menu_open, padx=5, pady=5)
        self.open_button.pack(pady=25)

        self.root.mainloop()