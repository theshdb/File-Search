import os
import pickle
import win32api
import PySimpleGUI as sg
sg.ChangeLookAndFeel('Dark')
class Gui:
    def __init__(self):
        self.layout=[[sg.Text("NOTE: Click Re Index button while giving a new \"Rooth Path\" or while changing the \"Root Path\".", size = (100, 1))],
                        [sg.Text("\tIf searching in the same \"Root Path\" then don\'t click Re Index button.", size = (100, 1))],
                        [sg.Text('Search Term', size = (10, 1)),
                        sg.Input(size = (45,1), focus = True, key = "TERM"), 
                        sg.Radio('Contains', size = (10, 1),  group_id ='choice', key = "CONTAINS", default = True),
                        sg.Radio('Starts With', size = (10, 1), group_id = 'choice', key = 'STARTSWITH'),
                        sg.Radio('Ends with', size = (10, 1), group_id = 'choice', key = "ENDSWITH")],
                        [sg.Text('Root Path', size=(10, 1)), 
                        sg.Input('', size = (45,1), key = "PATH"), 
                        sg.FolderBrowse('Browse', size = (10, 1)), 
                        sg.Button('Re-Index', size = (10,1), key = "_INDEX_"), 
                        sg.Button('Search', size = (10, 1), bind_return_key = True, key = "_SEARCH_")],
                        [sg.Output(size= (100, 25))],
                        [sg.Text('File Number: '),
                        sg.Input(size = (45,1), focus= True, key = "FILENUMBER"),
                        sg.Button('Open', size =  (10,1), key= "_OPEN_")]]
        self.window = sg.Window('File Search Engine', self.layout, element_justification='left')

class Searching:
    def __init__(self):
        self.file_index = []
        self.results = []
        self.records = 0
        self.matches = 0
        
    def create_new_index(self, values):
        '''create a new index and save to file'''
        root_path = values['PATH']
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

    def search(self, values):
        '''search for term based on search type'''

        term = values['TERM']
        #reset variables
        self.results.clear()
        self.matches = 0
        self.records = 0

        #perform serach 
        for path, files in self.file_index:
            for file in files:
                self.records += 1
                if( values['CONTAINS'] and term.lower() in file.lower() or
                    values['STARTSWITH'] and file.lower().startswith(term.lower()) or
                    values['ENDSWITH']  and file.lower.endswith(term.lower())):

                        result = path.replace('\\', '/') + '/' + file
                        self.results.append(result)
                        self.matches += 1
                        
                        
                else:
                    continue
        
        #save search results.
        with open('search_results.txt', 'w') as f:
            for row in self.results:
                f.write(row +  '\n')

    def Search_without_path(self, values):
        '''collecting all drives in pc.'''
        drives = win32api.GetLogicalDriveStrings()
        drives = (drives.split('\000')[:-1])
       
       #for time saving we are searching only user directory in C drive.
        if ('C' in drives[0] ):
            drives[0] = 'C:\\Users'

        term = values['TERM']
       #creating file indexs for particular drive and searches the drive for the requested file
        for i in range(len(drives)):
            self.create_new_index(drives[i])
            self.search(term)
            print("The query produced the following results: ")
            print(">> There were {:,d} matches out of {:,d} records searched in {} drive".format(self.matches, self.records, drives[i][0]))
        
            for match in self.results:
                print(match)

def main():
    g = Gui()
    s = Searching()
    s.load_existing_index()

    while True:
        event, values = g.window.Read()

        if event is None:
            break

        if event == '_INDEX_':
            s.create_new_index(values)

            print()
            print("New index has been created")
            print()
        
        if event == '_SEARCH_':
            s.search(values)

            #print results to output element
            print()
            for f, i in zip(s.results, range(len(s.results))):
                print(i+1, end='')
                print("\t"+f)
            
            print(">> There were {:,d} matches out of {:,d} records searched".format(s.matches, s.records))
            print()

        if event == '_OPEN_':
            files_saved = {}
            i=1
            with open('search_results.txt', 'r') as f:
                for line in f:
                    files_saved[i] = line
                    i += 1
 
            path = files_saved[int(values['FILENUMBER'])]

            try:
                os.system(f'start {os.path.realpath(path)}')
            except:
                sg.Popup('File can\'t be open', keep_on_top=True)

main()





    
