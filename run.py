from file import *
from tkinter import*

def runClean():
    console.delete("1.0", "end")
    runbuton.configure(text="Probíhá uklízení", state='disabled', bg= '#ff5555')
    fileeditor.setVarieble(days.get(),tester.get(), vyroba.get())
    fileeditor.cleanTesterFolder(console, okno)
    # print ("read")
    runbuton.configure(text="Začít uklízet", state='normal', bg= '#55ff55')

def findJob():
    console.delete("1.0", "end")

    copyChe =  copyCheckButon.get()
    fileeditor.setVarieble(days.get(), tester.get(),vyroba.get() )
    fileeditor.findJob(find.get(), copyChe, console, okno)

def on_enter_pressed(event):
    findBUtton.invoke()

okno = Tk()
fileeditor = file(0)
okno.title("Soubor manger")
okno.minsize(200, 200)
okno.bind('<Return>', on_enter_pressed)

# current_dir = os.path.dirname(os.path.abspath(__file__))
# print(current_dir)
# icon_file = "icon.ico"

# exe_dir = os.path.dirname(sys.executable)
# icon_path = os.path.join(exe_dir, "cleaner.ico")
icon_path = Path(__file__).with_name("cleaner.ico")
okno.iconbitmap(icon_path)

frame = Frame (okno, width=400, height=200)
frame.grid(row=0, column=0, padx=10, pady=10)

textFrame = Frame (frame)
textFrame.grid(row=0, column=0, padx=0, pady=0)

Label(textFrame, text="Vyroba: ", anchor="e").grid(row=0,column=1, padx=5, pady=5)
vyroba = Entry(textFrame, textvariable = "S:/Vyroba")
vyroba.insert(0, fileeditor.VyrobaPath)
vyroba.grid(row=0,column=2, padx=5, pady=5)

Label(textFrame, text="Tester Boards: ", anchor="e").grid(row= 1,column=1, padx=5, pady=5)
tester = Entry(textFrame)
tester.insert(0, fileeditor.TesterPath)
tester.grid(row=1,column=2, padx=5, pady=5)

Label(textFrame, text="Počet dní: ", anchor="e").grid(row=3, column=1, padx=5, pady=5)
days = Spinbox(textFrame, from_=0, to=100)
days.delete("0", "end")
days.insert(0, 2)
days.grid(row=3,column=2, padx=5, pady=5)

console = Text(frame, width = 40, height = 15)
console.grid(row=0, column = 1, padx = 5, pady = 5)
scrollbar = Scrollbar(frame)
scrollbar.grid(row=0, column=2, sticky=NS)
console.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=console.yview)

runbuton = Button (textFrame, text = "Začít uklízet", command= runClean, bg= '#55ff55')
runbuton.grid(row=4, column=1, padx=20, pady=10)

textFrame2 = Frame (frame)
textFrame2.grid(row=3, column=0, padx=0, pady=0)
Label(textFrame2, text="Najít zakázku: ", anchor="e").grid(row= 1,column=1, padx=5, pady=5)
find = Entry(textFrame2)

find.grid(row=1,column=2, padx=5, pady=5)
find.focus_set()

findBUtton = Button (textFrame2, text = "Najít zakázku: ", command= findJob, bg= '#55ff55')
findBUtton.grid(row=2, column=1, padx=20, pady=10)
copyCheckButon = BooleanVar()
copyCheck = Checkbutton(textFrame2, text="kopírovat testovací soubory", variable = copyCheckButon, onvalue = 1, offvalue = 0)
copyCheck.grid(row=2, column=2, padx=10, pady=10)

center_window(okno)
okno.mainloop()

