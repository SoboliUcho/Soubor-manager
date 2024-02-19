import os
from pathlib import Path
import re
import shutil
import time
from itertools import groupby
import subprocess
from tkinter import*
import json

def center_window(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f"+{x}+{y}")

class file:
    def __init__(self, days) -> None:
        # self.TesterPath = "C:/Users/sobol/Desktop/python/prace/tester"
        self.TesterPath = "S:/Tester_Boards"
        # self.VyrobaPath = "C:/Users/sobol/Desktop/python/prace/vyroba"
        self.VyrobaPath = "S:/Vyroba"
        self.TestFolders = []
        self.VyrobaFolders = []
        self.TotalComander= ""
        self.date = self.curentdate
        self.pastDays = days
        self.mesice = {
            'leden': 12,
            'unor': 11,
            'brezen': 10,
            'duben': 9,
            'kveten': 8,
            'cerven': 7,
            'cervec':6,
            'srpen':5,
            'zari':4,
            'rijen':3,
            'listopad':2,
            'prosinec': 1
        }
        self.load_init()
        
    def load_init(self):
        # print(self.mesice)
        # exe_dir = os.path.dirname(sys.executable)
        # file_path = os.path.join(exe_dir, "load.ini")
        file_path = Path(__file__).with_name("load.ini")
        with open(file_path, 'r') as json_file:
            rule = json.load(json_file)
        self.VyrobaPath = rule["VyrobaPath"]
        self.TesterPath = rule["TesterPath"]
        self.mesice = rule["mesice"]
        self.TotalComander = rule["TotalComanderPath"]
        # print (self.TesterPath)

        # self.mesice = json.loads(mesice)

    def findAllSUbFolders(self, folder):
        if os.path.isdir(folder):
            Folders = os.listdir(Path(folder))
        else: 
            Folders = False
        return Folders 
    
    def vyrobaFolder(self):
        Folders = self.findAllSUbFolders(self.VyrobaPath)
        Folders= sorted(Folders, key=self.foderValue)
        # print(Folders)
        for folder in Folders:
            if re.search(r"\d{2}.*|POOL",folder) and os.path.isdir(self.VyrobaPath+"/" + folder):
                self.VyrobaFolders.append(folder)
        # print(self.VyrobaFolders)
        return self.VyrobaFolders

    def dateOfFolder(self, folder):
        timer=os.path.getmtime(folder)
        folders = self.findAllSUbFolders(folder)
        for element in folders:
            if os.path.isdir(folder+"/"+element):
                subtimer = self.dateOfFolder(folder+"/"+element)
            else:
                subtimer = os.path.getmtime(folder+"/"+element)
            if subtimer > timer:
                timer=subtimer
        return timer

    def curentdate(self):
        self.date = time.time()
        return self.date
        
    def isFolderOlder(self, folder):
        timer=self.dateOfFolder(folder)
        # print (timer)
        if timer < self.curentdate()- (self.pastDays * 24 *60 *60):
            return True
        return False
        
    def copyFolder(self, folder, target):
        # url= shutil.copy2(folder, target)
        url= shutil.copytree(folder, target)
        # shutil.copytree
        return url
    
    def moveFolder(self, folder, target):
        url = shutil.move(folder, target)
        return url

    def deleteFolder(self, folder):
        url = shutil.rmtree(folder)
        return url

    def findFile(self, name, folderurl):
        if folderurl == False: 
            return False
        folders = self.findAllSUbFolders(folderurl)
        if folders == False:
            return False
        folders.sort(reverse=True)
        print (folders)
        for slozka in folders:
            if name == slozka or name + ".cam" == slozka: #AOI název pool = pool 
                # print (folders)
                return folderurl
        return False
    
    def findFile2(self, name, folderurl):
        nameEnd = name.endswith(";")
        name = name.replace(";", "")
        if folderurl == False: 
            return False
        folders = self.findAllSUbFolders(folderurl)
        if folders == False:
            return False
        folders.sort(reverse=True)
        # print (folders)
        for slozka in folders:
            if name in slozka: #AOI název pool = pool
                if nameEnd and name == slozka:
                    return folderurl + "/"+slozka
                elif nameEnd:
                    continue
                # print (folders)
                # return folderurl
                return folderurl + "/"+slozka
        return False
    
    def isInFolder(self, foledr, maneFile):
        # os.path.exists(path)
        # os.path.isdir(path)
        # os.path.isfile(path)
        return False
    
    def foderValue (self, string):
        number = self.mesice.get(string[2:], float('inf'))
        if string[:2].isdigit():
            number -= int(string[:2])*100
        # print(number)
        return number

    def findJobInVyroba(self, name):
        self.vyrobaFolder()
        for folder in self.VyrobaFolders:
            slozka = self.findFile2(name, self.VyrobaPath + "/"+ folder)
            if slozka != False:
                # print (slozka, folder)
                return slozka
        return False

    def findNameInVyroba (self, name):
        print ("finding " + name + " in Vyroba")
        self.vyrobaFolder()
        print(self.VyrobaFolders)
        for folder in self.VyrobaFolders:
            folders2 = self.findAllSUbFolders(self.VyrobaPath+"/"+folder) #složky ve mesicích 
            if folders2 == False:
                return False
            folders2.sort(reverse=True)
            print (folders2)
            for folder2 in folders2:
                slozka = self.findFile(name, self.VyrobaPath + "/"+ folder+"/"+folder2) #složka zakázky
                # print (slozka)
                # print("slozka 1 ", slozka)
                # slozka = self.findFile(name, self.VyrobaPath + "/"+ folder)
                # print("slozka 2 ", slozka)

                

                if slozka != False:
                    return slozka
        return False
    
    def testerFolder(self):
        tester = self.findAllSUbFolders(self.TesterPath)
        tester2=[]
        for test in tester:
            if os.path.isdir(self.TesterPath + "/"+ test)==False or test.startswith('Zz_') or test == "Tester":
                continue
            else:
                tester2.append(test)
        # print (tester2)
        grouped_strings = [list(group) for key, group in groupby(tester2, lambda x: x.split('_')[0])]
        self.TestFolders = grouped_strings
        return grouped_strings

    def foldersIsOlder(self, folders):
        older = True
        for folder in folders:
            if self.isFolderOlder(self.TesterPath + "/"+folder) == False:
                older = False
        return older

    def cleanTesterFolder(self, console, windo):
        if os.path.exists(self.VyrobaPath) and os.path.isdir(self.VyrobaPath):
            pass 
        else: 
            console.insert('end', "Vyroba neexistuje")
            return False
        if os.path.exists(self.TesterPath) and os.path.isdir(self.TesterPath):
            pass 
        else: 
            console.insert('end', "Tester neexistuje")
            return False
        start_time = time.time()

        self.testerFolder()
        # print(self.TestFolders)
        for folders in self.TestFolders:
           if self.foldersIsOlder(folders):
                print(folders)
                console.insert('end', folders)
                print ("is older then " + str(self.pastDays) + " days")
                console.insert('end', "\nje starší než " + str(self.pastDays) + " dní\n")
                windo.update()
                name = folders[0].replace("_A3","")
                name = name.replace("_A5","")
                name = name.replace("_A7","")
                vyrobaPath = self.findNameInVyroba(name)
                print("Vyroby path",vyrobaPath)
                if vyrobaPath == False:
                    print (name + " does not exist in Vyroba")
                    console.insert('end', name + " neexistuje ve Vyroba\n\n")
                    windo.update()
                    continue
                for folder in folders:
                    print ("copying folder:")
                    console.insert('end', "kopírování adresáře " + folder + "\n")
                    windo.update()
                    if os.path.exists(vyrobaPath + "/"+folder):
                        self.deleteFolder(vyrobaPath + "/"+folder)
                    url = ""
                    url= self.moveFolder(self.TesterPath + "/" + folder, vyrobaPath+"/"+folder)
                    print ("moved " + folder + " to: " + url)
                    console.insert('end', folder + " byl přesunut do: \n" + url+"\n\n")
                    console.see(END)
                    windo.update()
        
        end_time = time.time()
        execution_time = end_time - start_time
        print("\nExecution time:", execution_time, "seconds")
        console.insert('end', "\nExecution time:" + str(execution_time) + "seconds \n")
        return (execution_time)
    
    def setVarieble(self, days, tester, vyroba):
        # print(days, tester, vyroba)
        days = days.replace(",", ".")
        self.pastDays = float(days)
        self.TesterPath = tester
        self.VyrobaPath = vyroba

        # self.TesterPath = "C:/Users/sobol/Desktop/python/prace/tester"
        # # self.TesterPath = "S:/Tester_Boards"
        # self.VyrobaPath = "C:/Users/sobol/Desktop/python/prace/vyroba"
        # # self.VyrobaPath = "S:/Vyroba"

    def findJob(self, name, copy, console, windo):
        if os.path.exists(self.VyrobaPath) and os.path.isdir(self.VyrobaPath):
            pass 
        else: 
            console.insert('end', "Vyroba neexistuje")
            return False
        if os.path.exists(self.TesterPath) and os.path.isdir(self.TesterPath):
            pass 
        else: 
            console.insert('end', "Tester neexistuje")
            return False
        
        name = name.replace("CZ", "")
        name = name.replace("/", "-")
        name = name.replace("p", "P")
        url = self.findJobInVyroba(name)
        if url:
            print("job url is: ", url)
            console.insert('end', "job url je: \n" + url)
            console.see(END)
            windo.update()
        else:
            print("job isnt exist ")
            console.insert('end',"job neexistuje ")
            windo.update()
            return

        
        if copy == 1:
            folders = self.findAllSUbFolders(url)
            # folders = []
            # for folder in folders1:
            #     if 
            windowe = window(url, console, folders, self)
        else:
            print ("Openinig Total Comander")
            console.insert("end","\nOtvírání Total Comanderu")
            try:
                subprocess.Popen([self.TotalComander,"/o",'/R=',url])
            except FileNotFoundError:
                print("Total Commander is not installed or not found.")
                console.insert("end", "\nTotal Comander nexistuje nebo nebyl nalezen")

    
            
class window:
    def __init__(self, url, console, subfolders, folder) -> None:
        self.console = console
        self.url = url
        self.subfolders = subfolders
        self.checkboxes = []
        self.folder = folder
        self.newWindow()
        # self.windows = Toplevel()
        
    def newWindow(self):
        print (self.subfolders)
        folders1 = []
        for rolder in self.subfolders:
            if os.path.isdir(self.url +"/"+ rolder) and "AOI_" not in rolder and "DDI" not in rolder and "SINGLE_FR" not in rolder and "aoi_" not in rolder and "aser" not in rolder:
                folders1.append(rolder)
        self.subfolders = folders1

        submit = Toplevel()

        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # icon_path = os.path.join(current_dir, "cleaner.ico")
        # self.windows = submit

        # exe_dir = os.path.dirname(sys.executable)
        # icon_path = os.path.join(exe_dir, "cleaner.ico")
        icon_path = Path(__file__).with_name("cleaner.ico")
        submit.iconbitmap(icon_path)
        submit.minsize(200, 200)

        last_position = self.url.rfind("/")
        label = Label(submit, text= self.url[last_position + 1:])
        label.pack()

        print(self.subfolders)
        self.buttons(self.subfolders, submit)
        
        copyButton = Button (submit, text="Kopírovat", command=lambda: self.selectToCopy(submit, copyButton), bg= '#55ff55')
        copyButton.pack()
        
        close_button = Button(submit, text="Close Window", command=submit.destroy)
        close_button.pack()

        center_window(submit)

    def buttons(self, items, windows):
        for i in range(len(items)):
            var = IntVar()
            checkbox = Checkbutton(windows, text=items[i], variable=var)
            checkbox.pack()
            self.checkboxes.append(var)

    def selectToCopy(self, windo, copyButton):
        copyButton.configure(text="Probíhá kopírování", state='disabled', bg= '#ff5555')

        selected_items = [item.get() for item in self.checkboxes]
        print("Selected items:", selected_items)
        for i in range(len (selected_items)):
            if selected_items[i] == 1:
                print("copying " + self.subfolders[i] + " to tester folder")
                self.console.insert("end", "\nkopírování " + self.subfolders[i] + " do TesterBoards\n")
                windo.update()
                if os.path.exists(self.folder.TesterPath + "/"+self.subfolders[i]) == False:
                    self.folder.copyFolder(self.url+ "/" +self.subfolders[i], self.folder.TesterPath+"/"+self.subfolders[i])
                    print ("Copying finished")
                    self.console.insert("end", "Kopírování skončeno")
                    windo.update()
                else:
                    print (self.subfolders[i] + " Folder is in tester directory")
                    self.console.insert("end", self.subfolders[i] + " je již v TesterBoards")
                    windo.update()
        copyButton.configure(text="Kopírovat", state='normal', bg= '#55ff55')

  