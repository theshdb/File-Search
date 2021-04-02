import os
import pickle
import win32api
from tkinter import *
import re
import time

class Search_Operations:
    def __init__(self):
        self.file_index = []
        self.results = []
        self.exception = [".git", "$RECYCLE.BIN", "AppData"]
    
    #writes into file
    def Writing_in_file(self):    
        #save search results.
        with open('search_results.txt', 'w') as f:
            for row,i in zip(self.results, range(len(self.results))): 
                f.write (str(i+1) +  "\t" + row +  '\n')

    def create_new_index(self, root_path):
        '''create a new index and save to file'''
        self.file_index = []
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

        #perform serach 
        for path, files in self.file_index:
            for file in files:
                if ((format == 'Term' and word.lower() in file.lower()) or
                     (format == 'File format' and (file.lower()).endswith(word.lower()))):

                        result = path.replace('\\', '/') + '/' + file
                        if not any(ext in result for ext in self.exception):
                            self.results.append(result)
                else:
                    continue

    #searches files based on their modification date
    def Search_Modified(self, number):
        #reset variables
        self.results.clear()

        for path, files in self.file_index:
            for file in files:
                result = path.replace('\\', '/') + '/' + file
                if not any(ext in result for ext in self.exception):
                    self.results.append(result)

        #sorting file based on there last modification date (latest first)
        self.results.sort(key=os.path.getmtime)
        self.results = list(reversed(self.results))

        #save output to file
        with open('search_results.txt', 'w') as f:
            for row,i in zip(self.results, range(len(self.results))):
                if(i+1 <= number):
                    f.write (str(i+1) +  "\t" + row +  '\n')
                else:
                    continue
    
    #gives all the files careted on given date
    def Search_Created(self, date):
        #reset variables
        self.results.clear()

        for path, files in self.file_index:
            for file in files:
                result = path.replace('\\', '/') + '/' + file
                if(date.lower() in str(time.ctime(os.path.getctime(result))).lower()) and (not any(ext in result for ext in self.exception)):
                    self.results.append(result)
        #saving o/p in file
        self.Writing_in_file()

    def Search_without_path(self, word):
        if(os.path.exists('search_results.txt')):
            f = open('search_results.txt', 'r+')
            f.truncate(0)
            
        '''collecting all drives in pc.'''
        drives = win32api.GetLogicalDriveStrings()
        drives = (drives.split('\000')[:-1])
       
       #for time saving we are searching only user directory in C drive.
        if ('C' in drives[0] ):
            drives[0] = 'C:\\Users'
    
       #creating file indexs for particular drive and searches the drive for the requested file
        for x in range(len(drives)):
            self.create_new_index(drives[x])
            self.search("Term", word)

            if(os.stat("search_results.txt").st_size != 0):
                with open('search_results.txt', 'r') as f:
                    lines = f.read().splitlines()
                    last_line = lines[-1]
                i = int(last_line[0])
                with open("search_results.txt", "a") as a:
                    for row in self.results: 
                        a.write( str(i+1) + "\t" + row + '\n' )
                        i +=1
            else:
                i=1
                with open('search_results.txt', 'w') as b:
                    for row in self.results:
                        b.write(str(i) + '\t' + row + '\n')
                        i += 1

    def Open_file(self, number):
        files_saved = {}
        i=1
        with open('search_results.txt', 'r') as f:
            for line in f:
                files_saved[i] = line
                i += 1

        try:
            path = re.sub('\s+', '', files_saved[number])
            path = path[1:]
            os.system(f'start {os.path.realpath(path)}')
        except:
            #root.messagebox.showerror("showerror", "Error")
            print("error")
