#imports:
from tkinter import *
from tkinter.filedialog import asksaveasfile
from json import dump as jsonDump #for saving board as JSON format
from tkinter.ttk import *
try:
    import sv_ttk
except:
    pass

tk = Tk() #tk is master
try:
    sv_ttk.use_light_theme() #set light theme of window
except:
    pass
tk.resizable(height=False, width=False) #disable resizing window
tk.title("Design Manager: GameOfLIFE")

#create Checkbutton (cells)
cells = dict() #the format of this dictionary is like this: {!label:[cellvariable&location, dead or live]}
k = dict() #used for locating cell location from tkinter output like !label3. {!labeln:cellx_y}
for x in range(1, 21):
    for y in range(1, 21):
        cellname = "cell{x}_{y}".format(x=x, y=y)
        globals()[cellname] = Checkbutton(tk) #create a label(cell) with the name from cellname string.
        globals()[cellname].state(['!alternate'])
        globals()[cellname].grid(row=x+1, column=y)
        #cells[locals()[cellname]] = [cellname, "dead"]
        cells[cellname] = "dead"
        k[locals()[cellname]] = cellname

#Saving board as JSON file:
def Save():
    filepath = asksaveasfile(defaultextension=".json", filetypes=[("JSON file", "*.json")])
    for x in k.keys():
        CellName = k[x]
        if x.instate(['selected']):
            cells[CellName] = "live"
        else:
            cells[CellName] = "dead"
    jsonDump(cells, filepath) #savefile


Button(tk, text="Save Board", command=Save).grid(row=1, column=0) #create Save button
Button(tk, text="Quit", command=exit).grid(row=2, column=0) #create Save button
tk.mainloop()