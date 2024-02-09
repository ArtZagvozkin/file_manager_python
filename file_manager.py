import os, pathlib, time
from tkinter import *
from tkinter import messagebox, simpledialog
from shutil import copyfile, move


class FileManager:
    def __init__(self):
        self.__curPath = os.getcwd() + '\\'

    def getCurPath(self):
        return self.__curPath

    def setCurPath(self, path):
        if os.path.isdir(path):
            self.__curPath = path

    def getObjects(self, path):
        objOfDir = []

        currentDir = pathlib.Path(path)

        direct = [obj.name for obj in currentDir.iterdir() if obj.is_dir()]
        for subdir in direct:
            objOfDir.append(subdir + "\\")

        # get list of files
        files = [obj.name for obj in currentDir.iterdir() if obj.is_file()]
        for file in files:
            objOfDir.append(file)
        return objOfDir

    def openFile(self, path):
        if not os.path.exists(path):
            messagebox.showerror("Error", "File not found")
            return
        os.startfile(path)


def lBoxUpdate():
    path = fileManager.getCurPath()

    searchBox.delete(0, END)
    searchBox.insert(0, path)

    lBox.delete(0, END)

    if len(path) > 3:
        lBox.insert(0, "...")

    itemsOfDir = fileManager.getObjects(path)
    for obj in itemsOfDir:
        lBox.insert(END, obj)

    infoBoxUpdate()


def searchBoxPressEnter(event):
    newPath = searchBox.get()
    if os.path.isfile(newPath):
        open(searchBox.get())
        return
    elif not pathlib.Path(newPath).is_dir():
        messagebox.showerror("Error", "Неверный путь")
        return

    fileManager.setCurPath(newPath)
    lBoxUpdate()


def lBoxClick(event):
    infoBoxUpdate()


def infoBoxUpdate():
    lblName.configure(text="")
    lblType.configure(text="")
    lblEditData.configure(text="")
    lblEditTime.configure(text="")
    lblSize.configure(text="")

    if lBox.curselection() == 0 or len(lBox.curselection()) == 0:
        return

    selectedItem = lBox.get(lBox.curselection())
    fullPath = fileManager.getCurPath() + selectedItem

    if selectedItem == "...":
        itmPath = str.split(fileManager.getCurPath(), "\\")

        objName = itmPath[len(itmPath)-2]
        modDateTime = time.localtime(os.path.getmtime(fullPath))
        modDate = time.strftime('%d-%m-%Y', modDateTime)
        modTime = time.strftime('%H:%M:%S', modDateTime)

        lblName.configure(text=objName)
        lblType.configure(text="Тип: папка")
        lblEditData.configure(text=f"Date of change: {modDate}")
        lblEditTime.configure(text=f"Time of change: {modTime}")
        lblSize.configure(text="")
    elif os.path.isdir(fullPath):
        modDateTime = time.localtime(os.path.getmtime(fullPath))
        modDate = time.strftime('%d-%m-%Y', modDateTime)
        modTime = time.strftime('%H:%M:%S', modDateTime)

        lblName.configure(text=selectedItem)
        lblType.configure(text="Type: dir")
        lblEditData.configure(text=f"Date of change: {modDate}")
        lblEditTime.configure(text=f"Time of change: {modTime}")
        lblSize.configure(text="")
    elif os.path.isfile(fullPath):
        modDateTime = time.localtime(os.path.getmtime(fullPath))
        modDate = time.strftime('%d-%m-%Y', modDateTime)
        modTime = time.strftime('%H:%M:%S', modDateTime)
        fileSize = os.path.getsize(fullPath)

        lblName.configure(text=selectedItem)
        lblType.configure(text="Type: file")
        lblEditData.configure(text=f"Date of change: {modDate}")
        lblEditTime.configure(text=f"Time of change: {modTime}")
        lblSize.configure(text=f"Size: {fileSize} byte")


def lBoxDoubleClick(event):
    pressBtnOpen()


def pressBtnOpen():
    if lBox.curselection() == 0:
        return

    selectedItem = lBox.get(lBox.curselection())
    fullPath = fileManager.getCurPath() + selectedItem

    if selectedItem == "...":
        pathItems = str.split(fullPath, "\\")
        newPath = ""
        for i in range(len(pathItems) - 2):
            newPath += pathItems[i] + "\\"
        fileManager.setCurPath(newPath)
        lBoxUpdate()
    elif os.path.isdir(fullPath):
        newPath = fullPath
        fileManager.setCurPath(newPath)
        lBoxUpdate()
    elif os.path.isfile(fullPath):
        fileManager.openFile(fullPath)
    else:
        messagebox.showerror("Error", "Элемент не существует")


def btnCopyPress():
    usrInput = simpledialog.askstring(title="Copy", prompt="Name file:")
    dstPath = fileManager.getCurPath() + usrInput
    if os.path.exists(dstPath):
        messagebox.showerror("Error", "Файл с таким именем уже существует")
        return

    if lBox.curselection() == 0:
        return
    selectedItem = lBox.get(lBox.curselection())
    srcPath = fileManager.getCurPath() + selectedItem

    if selectedItem == "...":
        return
    elif os.path.isfile(srcPath):
        copyfile(srcPath, dstPath)
        lBoxUpdate()


def btnRenMovePress():
    usrInput = simpledialog.askstring(title="Rename", prompt="File name:")
    dstPath = fileManager.getCurPath() + usrInput
    if os.path.exists(dstPath):
        messagebox.showerror("Error", "Файл с таким именем уже существует")
        return

    if lBox.curselection() == 0:
        return
    selectedItem = lBox.get(lBox.curselection())
    srcPath = fileManager.getCurPath() + selectedItem

    if selectedItem == "...":
        return
    elif os.path.isfile(srcPath):
        move(srcPath, dstPath)
        lBoxUpdate()


def btnMkFilePress():
    usrInput = simpledialog.askstring(title="New file", prompt="Name file:")
    fullPath = fileManager.getCurPath() + usrInput

    if os.path.exists(fullPath):
        messagebox.showerror("Error", "Файл с таким именем уже существует")
        return

    open(fullPath, 'a').close()
    lBoxUpdate()


def btnMkDirPress():
    usrInput = simpledialog.askstring(title="Create new dir", prompt="Name dir:")
    fullPath = fileManager.getCurPath() + usrInput

    if os.path.exists(fullPath):
        messagebox.showerror("Error", "Директория с таким именем уже существует")
        return

    os.mkdir(fullPath)
    lBoxUpdate()


def btnDelPress():
    if lBox.curselection() == 0:
        return

    selectedItem = lBox.get(lBox.curselection())
    fullPath = fileManager.getCurPath() + selectedItem

    if selectedItem == "...":
        return
    if os.path.isdir(fullPath):
        fullPath = fullPath + "\\"
        os.rmdir(fullPath)
        lBoxUpdate()
    elif os.path.isfile(fullPath):
        os.remove(fullPath)
        lBoxUpdate()


fileManager = FileManager()

mainWindow = Tk()
mainWindow.title("File manager")
mainWindow.columnconfigure(tuple(range(1)), weight=1)
mainWindow.rowconfigure(1, weight=1)

# Поле поиска
searchBox = Entry(mainWindow)
searchBox.grid(row=0, column=0, columnspan=2, sticky=W + E, padx=2)
searchBox.bind('<Return>', searchBoxPressEnter)
searchBox.insert(1, fileManager.getCurPath())

# Info panel
infoBox = PanedWindow(mainWindow)
infoBox.grid(row=1, column=1, sticky=S+N)
# Name
lblName = Label(infoBox, width=30, anchor='nw', font='Arial 12', text="Name")
lblName.grid(row=0, pady=5)
# Type
lblType = Label(infoBox, width=30, anchor='nw', font='Arial 12', text="Type")
lblType.grid(row=1, pady=2)
# Date of change
lblEditData = Label(infoBox, width=30, anchor='nw', font='Arial 12', text="Date of change")
lblEditData.grid(row=2, pady=2)
# Time of change
lblEditTime = Label(infoBox, width=30, anchor='nw', font='Arial 12', text="Time of change")
lblEditTime.grid(row=3, pady=2)
# Size
lblSize = Label(infoBox, width=30, anchor='nw', font='Arial 12', text="Size")
lblSize.grid(row=4, pady=2)

# List of objects
lBox = Listbox(mainWindow, font=("Helvetica", 12))
lBox.grid(row=1, column=0, sticky=W+E+S+N)
lBox.delete(0, END)
lBox.bind('<Double-Button>', lBoxDoubleClick)
lBox.bind('<<ListboxSelect>>', lBoxClick)
lBox.select_set = 1
lBoxUpdate()

# ToolBox
toolBox = PanedWindow(mainWindow)
toolBox.grid(row=2, column=0, columnspan=2, sticky=W+E)
btnCopy = Button(toolBox, width=15, text="Copy", command=btnCopyPress)
btnCopy.grid(row=0, column=0, sticky=W+E)
btnRenMove = Button(toolBox, width=15, text="Rename", command=btnRenMovePress)
btnRenMove.grid(row=0, column=1, sticky=W+E)
btnMkFile = Button(toolBox, width=15, text="Create file", command=btnMkFilePress)
btnMkFile.grid(row=0, column=2, sticky=W+E)
btnMkDir = Button(toolBox, width=15, text="Create dir", command=btnMkDirPress)
btnMkDir.grid(row=0, column=3, sticky=W+E)
btnDel = Button(toolBox, width=15, text="Delete", command=btnDelPress)
btnDel.grid(row=0, column=4, sticky=W+E)

toolBox.columnconfigure(tuple(range(5)), weight=1)
toolBox.rowconfigure(tuple(range(5)), weight=1)


mainWindow.mainloop()
