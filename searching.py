import os
import pickle
import win32api


class Searching:
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

    def search(self, term, search_type = "contains"):
        '''search for term based on search type'''
        #reset variables
        self.results.clear()
        self.matches = 0
        self.records = 0

        #perform serach 
        for path, files in self.file_index:
            for file in files:
                self.records += 1
                if( search_type == 'contains' and term.lower() in file.lower() or
                    search_type == 'startwith' and file.lower().startswith(term.lower()) or
                    search_type == 'endswith'  and file.lower.endswith(term.lower())):

                        result = path.replace('\\', '/') + '/' + file
                        self.results.append(result)
                        self.matches += 1
                else:
                    continue
        
        #save search results.
        with open('search_results.txt', 'w') as f:
            for row in self.results:
                f.write(row + '\n')

    def Search_without_path(self, term):
        '''collecting all drives in pc.'''
        drives = win32api.GetLogicalDriveStrings()
        drives = (drives.split('\000')[:-1])
       
       #for time saving we are searching only user directory in C drive.
        if ('C' in drives[0] ):
            drives[0] = 'C:\\Users'

       #creating file indexs for particular drive and searches the drive for the requested file
        for i in range(len(drives)):
            self.create_new_index(drives[i])
            self.search(term)
            print("The query produced the following results: ")
            print(">> There were {:,d} matches out of {:,d} records searched in {} drive".format(self.matches, self.records, drives[i][0]))
        
            for match in self.results:
                print(match)

    
def test():
         s = Searching()
        # s.load_existing_index()
        # s.search('cnLab')

        # print()
        # print(">> There were {:,d} matches out of {:,d} records searched".format(s.matches, s.records))
        # print()
        # print("The query produced the following results: ")
        # for match in s.results:
        #     print(match)
        #s.Search_without_path('hello')


test()


    
