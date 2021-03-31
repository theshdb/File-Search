import os
import pickle
import win32api
from tkinter import *

class Search_Operations:
    def __init__(self):
        self.file_index = []
        self.results = []
        self.records = 0
        self.matches = 0
        
    def create_new_index(self, root_path):
        '''create a new index and save to file'''
        self.file_index = [(root, files) for root, dirs, files in os.walk(root_path) if files]

        #save to file
        with open('file_index.pkl', 'wb') as f:
            pickle.dump(self.file_index, f)

    def load_existing_index(self):
        '''load existing index'''
        try:
            with open('file_index.pkl', 'rb') as f:
                self.file_index = pickle.load(f)
        except:
            self.file_index = []

    def search(self, format, word):
        '''search for term based on search type'''
        #reset variables
        self.results.clear()
        self.matches = 0
        self.records = 0

        #perform serach 
        for path, files in self.file_index:
            for file in files:
                self.records += 1
                if ((format == 'Term' and word.lower() in file.lower()) or
                     format == 'File Format'  and file.lower.endswith(word.lower())):

                        result = path.replace('\\', '/') + '/' + file
                        self.results.append(result)
                        self.matches += 1
                else:
                    continue
        
        #save search results.
        with open('search_results.txt', 'w') as f:
            for row in self.results:
                f.write(row +  '\n')

    def Search_Modified(self, date):
        pass

    def Search_Created(self, date):
        pass

    def Search_without_path(self, word):
        '''collecting all drives in pc.'''
        drives = win32api.GetLogicalDriveStrings()
        drives = (drives.split('\000')[:-1])
       
       #for time saving we are searching only user directory in C drive.
        if ('C' in drives[0] ):
            drives[0] = 'C:\\Users'

       #creating file indexs for particular drive and searches the drive for the requested file
        for i in range(len(drives)):
            self.create_new_index(drives[i])
            self.search(word)

            print()
            for f, i in zip(self.results, range(len(self.results))):
                print(i+1, end='')
                print("\t"+f)
            
            print(">> There were {:,d} matches out of {:,d} records searched".format(self.matches, self.records))
            print()


    def Open_file(self, number):
        files_saved = {}
        i=1
        with open('search_results.txt', 'r') as f:
            for line in f:
                files_saved[i] = line
                i += 1

        try:
            os.system(f'start {os.path.realpath(files_saved[number])}')
        except:
            #root.messagebox.showerror("showerror", "Error")
            print("error")





    
