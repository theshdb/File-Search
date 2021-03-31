from tkinter import *
from tkinter.font import BOLD
from tkinter import filedialog
import sys
from Searching import Search_Operations

class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.title("File Serach Engine")
        self.iconbitmap()
        self.geometry("700x680")
        self.configure(bg='#202020')

        self.frame_search = Frame(self, bg="#202020")
        self.frame_search_address = Frame(self, bg="#202020")
        self.frame_file_open = Frame(self, bg="#202020")
        global s
        s = Search_Operations()
        s.load_existing_index()

    #func to get the search type from user and process it
    def Search_Option(self):

        self.frame_search.pack()
        self.frame_search.place(x=70, y=170) 

        self.frame_search_address.pack()
        self.frame_search_address.place(x=70, y=220)

        self.button_search.pack()
        self.button_search.place(x=160, y=290)

        if self.variable.get() =="Term": 
            self.text_term.delete(1.0, "end")
            self.label_output.pack_forget()
            self.label_output.place_forget()
            self.frame_file_open.pack_forget()
            self.frame_file_open.place_forget()
            self.label_term.config(text = "Search Term : ")
        
        if self.variable.get() =="File format":
            self.text_term.delete(1.0, "end")
            self.label_output.pack_forget()
            self.label_output.place_forget()
            self.frame_file_open.pack_forget()
            self.frame_file_open.place_forget()
            self.label_term.config(text = "File format : ")
        
        if self.variable.get() == "Last Modified":
            self.text_term.delete(1.0, "end")
            self.label_output.pack_forget()
            self.label_output.place_forget()
            self.frame_file_open.pack_forget()
            self.frame_file_open.place_forget()
            self.label_term.config(text = "Files modified after(Date) : ")

        if self.variable.get() == "Created On":
            self.text_term.delete(1.0, "end")
            self.label_output.pack_forget()
            self.label_output.place_forget()
            self.frame_file_open.pack_forget()
            self.frame_file_open.place_forget()
            self.label_term.config(text = "Date : ")

        if self.variable.get() == 'Without Path':
            self.text_term.delete(1.0, "end")
            self.frame_search_address.pack_forget()
            self.frame_search_address.place_forget()
            self.label_output.pack_forget()
            self.label_output.place_forget()
            self.frame_file_open.pack_forget()
            self.frame_file_open.place_forget()
            self.label_term.config(text = "Search Term : ")
            self.label_discription = Label(self, text = "This will search the locations -> C:\\User\\ and other drives present on this PC.", font=("Arial", 12, BOLD), bg='#202020', fg='#9DC88D', relief= FLAT)
            self.label_discription.pack()
            self.label_discription.place(x = 70, y=240)

    #Search output display
    def Search(self):
        self.label_output.config(text = "")
        self.label_output.pack()
        self.label_output.place(x = 20, y = 350)
        self.text_number.delete(1.0, "end")
        self.frame_file_open.pack()
        self.frame_file_open.place(x = 70, y= 570)

        #performing search for search types "term" and "file format".
        if self.variable.get() =="Term" or self.variable.get() == "File Format":
            s.search(self.variable.get(), self.text_term.get("1.0",'end-1c'))

            print()
            for f, i in zip(s.results, range(len(s.results))):
                print(i+1, end='')
                print("\t"+f)
            
            print(">> There were {:,d} matches out of {:,d} records searched".format(s.matches, s.records))
            print()


        #performing search for search type "Last Modified".
        if self.variable.get() == "Last Modified":
            pass

        #performing search for search type "Created On".
        if self.variable.get() == "Created On" :
            pass

        #performing search for search type "Without Path".
        if self.variable.get() == "Without Path":
            s.Search_without_path( self.text_term.get("1.0",'end-1c'))


    #to open file browser
    def Browse_files(self):
        foldername = filedialog.askdirectory()
        self.text_address.delete(1.0, "end")
        self.text_address.insert(1.0, foldername)

    #to relocate searching directory
    def Redirect(self):
        s.create_new_index(self.text_address.get("1.0",'end-1c'))
        print()
        print("File path has been initialized to search.")
        print()

    #File opening
    def Open(self):
        s.Open_file(int(self.text_number.get("1.0",'end-1c')))

    def Widegets(self):

        #Note text
        self.label_note = Label( self, text = "NOTE: Click Re Index button while giving a new \"selfh Path\" or while changing the \"self Path\".\n"
                            "If searching in the same \"self Path\" then don\'t click Re Index button.", font=("Arial",  10, BOLD), bg='#202020',fg='#9DC88D', relief=FLAT)
        self.label_note.pack()
        self.label_note.place(x=35, y=20)

        #Search text
        self.label_search_by = Label( self, text = "Search by: ", font=("Arial", 14, BOLD), bg='#202020', fg='#FFFFFF', relief= FLAT)
        self.label_search_by.pack()
        self.label_search_by.place(x=20, y=90)

        # Option Menu
        self.variable = StringVar(self)
        self.variable.set("Term")

        self.search_menu = OptionMenu(self, self.variable, "Term", "File format", "Last Modified", "Created On","Without Path")
        self.search_menu.pack()
        self.search_menu.config(bg = "#202020", fg = "#9DC88D")
        self.search_menu.place(x=150, y=90)

        #Select button for menu
        self.button_ok = Button(self,text = "Select" ,font=("Arial", 12, BOLD), bg = "#F1B24A", fg="#202020", width=8, command=self.Search_Option)
        self.button_ok.pack()
        self.button_ok.place(x=280, y=90)

        '''Frame for search type'''
        #label in frame
        self.label_term = Label(self.frame_search, text="",font=("Arial", 12, BOLD), bg='#202020', fg='#FFFFFF', relief= FLAT)
        self.label_term.pack(side= LEFT, padx= 5, pady= 5)

        #text field for term in frame
        self.text_term = Text(self.frame_search, height=2, width=25)
        self.text_term.pack(side = LEFT, padx=10, pady=7)

        '''frame for self path'''
        #label for self address
        self.label_address = Label(self.frame_search_address, text="Root Path : ",font=("Arial", 12, BOLD), bg='#202020', fg='#FFFFFF', relief= FLAT)
        self.label_address.pack(side= LEFT, padx= 5, pady= 5)

        #text field for adress in frame
        self.text_address = Text(self.frame_search_address, height=2, width=25)
        self.text_address.pack(side = LEFT, padx=30, pady=7)

        #button to perform search
        self.button_browse = Button(self.frame_search_address, text = "Browse" ,font=("Arial", 12, BOLD), bg = "#F1B24A", fg="#202020", width=8, height=1, command=self.Browse_files)
        self.button_browse.pack(side = LEFT, padx=5, pady=9)

        #button to scan all files in selected self path
        self.button_redirect = Button(self.frame_search_address, text = "Re-Direct" ,font=("Arial", 12, BOLD), bg = "#F1B24A", fg="#202020", width=8, height=1, command=self.Redirect)
        self.button_redirect.pack(side = LEFT, padx=9, pady=9)

        '''not in any frame'''
        #search button
        self.button_search = Button(self, text = "Search" ,font=("Arial", 14, BOLD), bg = "#4D774E", fg="#FFFFFF", width=9, height=1, command=self.Search)

        #label to display output
        self.label_output = Label(self, text = "", font=("Arial", 12, BOLD),  fg='#FFFFFF', relief= FLAT, width=65, height = 10)


        '''frame to open file'''
        #label in frame_open_file
        self.label_number = Label(self.frame_file_open, text = "File Number : ", font=("Arial", 12, BOLD), bg='#202020', fg='#FFFFFF', relief= FLAT)
        self.label_number.pack(side = LEFT, padx=5, pady=7)

        #text filed for number of file
        self.text_number = Text(self.frame_file_open, height=2, width=25)
        self.text_number.pack(side = LEFT, padx=5, pady=7)

        #Open button
        self.button_open = Button(self.frame_file_open, text = "Open" ,font=("Arial", 12, BOLD), bg = "#F1B24A", fg="#202020", width=8, height=1, command=self.Open)
        self.button_open.pack(side = LEFT, padx=5, pady=9)

if __name__ == "__main__":
    root = GUI()
    root.Widegets()
    root.mainloop()