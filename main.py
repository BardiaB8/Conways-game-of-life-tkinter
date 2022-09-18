#import librarysL
from tkinter import *
from json import load as jsonLoad
from time import sleep

tk = Tk() #tk is master.
tk.resizable(height=False, width=False) #disable user resizing window
tk.config(bg="#aeaeae") #set tkinter background
tk.title("GAME OF LIFE") #title of window

#cell images:
live = PhotoImage(file="data/livecell.png")
dead = PhotoImage(file="data/deadcell.png")

#create cells:
cells = dict() #the format of this dictionary is like this: {!label:[cellvariable&location, dead or live]}
k = dict() #used for locating cell location from tkinter output like !label3. {!labeln:cellx_y}
for x in range(1, 21):
    for y in range(1, 21):
        cellname = "cell{x}_{y}".format(x=x, y=y)
        globals()[cellname] = Label(tk, image=dead) #create a label(cell) with the name from cellname string.
        globals()[cellname].grid(row=x, column=y)
        cells[locals()[cellname]] = [cellname, "dead"]
        k[cellname] = locals()[cellname]

#make some cells live:
'''
for x in range(randint(80, 90)): #how many buttons to make live is also random.
    livecell = choice(tk.winfo_children()) #select a cell to make live
    while cells[livecell] == [cells[livecell][0], "live"]:
        livecell = choice(tk.winfo_children()) #tk.winfo_children creates a list of all objects in tk, e.g. [!label1, !label2, ...]
    old_cell = cells[livecell]
    cells[livecell] = [old_cell[0], "live"]
'''

#load cell data:
with open("celldata.json", "r") as celldata_file:
    celldata = jsonLoad(celldata_file)
    for cell in celldata.keys():
        cells[k[cell]] = [cell, celldata[cell]]

def CalculateNearbyCells(CellLocation):
    #calcualte cells located on top, bottom, right or left of a given cell.
    CellLocation = CellLocation.split("_")
    CellLocation = [CellLocation[1], CellLocation[0][4:]]
    #output = ["cell"+str(int(CellLocation[0])-1)+"_"+CellLocation[1], "cell"+str(int(CellLocation[0])+1)+"_"+CellLocation[1], "cell"+CellLocation[0]+"_"+str(int(CellLocation[1])-1), "cell"+CellLocation[0]+"_"+str(int(CellLocation[1])+1)]    
    cellTop = "cell"+str(int(CellLocation[0])-1)+"_"+CellLocation[1]
    cellBottom = "cell"+str(int(CellLocation[0])+1)+"_"+CellLocation[1]
    cellRight = "cell"+CellLocation[0]+"_"+str(int(CellLocation[1])+1)
    cellLeft = "cell"+CellLocation[0]+"_"+str(int(CellLocation[1])-1)
    cellTopRight = "cell"+str(int(CellLocation[0])-1)+"_"+str(int(CellLocation[1])+1)
    cellTopLeft = "cell"+str(int(CellLocation[0])-1)+"_"+str(int(CellLocation[1])-1)
    cellBottomRight = "cell"+str(int(CellLocation[0])+1)+"_"+str(int(CellLocation[1])+1)
    cellBottomLeft = "cell"+str(int(CellLocation[0])+1)+"_"+str(int(CellLocation[1])-1)
    output = [cellTop, cellBottom, cellRight, cellLeft, cellTopRight, cellTopLeft, cellBottomRight, cellBottomLeft]
    
    #remove every cell containing 0 or 21 in output, because they don't exist.
    for x in output[:-1]: 
        if '0' in x:
            output.remove(x)
        elif '21' in x:
            output.remove(x)
    for x in output:
        if '0' in x:
            output.remove(x)
        elif '21' in x:
            output.remove(x)

    #print("CALCNEARBY: ", output) #used for debugging.
    return output
def CalculateLiveCells(nearbycells): #calculate which cells are alive from a list of given cells.
    NearbyLiveCells = 0
    for NearbyCell in nearbycells:
        #print(cells[k[NearbyCell]])
        if cells[k[NearbyCell]][1] == "live":
            NearbyLiveCells += 1
    return NearbyLiveCells
def updateBoard():
    #puts changes in main dictionary, configs labels according to cells dict, and updates tk window.
    global cells
    cells = CellsWithChanges.copy()
    for CellKey in cells.keys():
        if cells[CellKey][1] == "live":
            CellKey.config(image=live)
        elif cells[CellKey][1] == "dead":
            CellKey.config(image=dead)
    tk.update()
while True:
    sleep(1) #the delay between changes of generation.
    CellsWithChanges = cells.copy() #creating a dict to store changes in, to avoid modifying the main dictionary.
    #updateBoard()
    for CellKey in cells.keys():
        #print(cells[CellKey],"\n",type(cells[CellKey][0]),"\n\n")
        NearbyCells = CalculateNearbyCells(cells[CellKey][0])
        NearbyLiveCells = CalculateLiveCells(NearbyCells)
        #print(NearbyCells, "\n", NearbyLiveCells)
        #Rules:
        if cells[CellKey][1] == "live": #Rules for live cells:
            #kill this cell if underpopulated:
            if NearbyLiveCells < 2:
                CellsWithChanges[CellKey] = [cells[CellKey][0], "dead"]
                #print("this cell has {} neighbors and is underpopulated".format(NearbyLiveCells))
            elif NearbyLiveCells == 2 or NearbyLiveCells == 3:
                pass #next generation.
            #kill if overpopulated:
            elif NearbyLiveCells < 3:
                CellsWithChanges[CellKey] = [cells[CellKey][0], "dead"]
                #print("this cell has {} neighbors and is overpopulated".format(NearbyLiveCells))
        elif cells[CellKey][1] == "dead":
            #reproduction:
            if NearbyLiveCells == 3:
                CellsWithChanges[CellKey] = [cells[CellKey][0], "live"]
                #print("this cell has {} neighbors and will be reproduced".format(NearbyLiveCells))
    
    #update board!
    updateBoard()