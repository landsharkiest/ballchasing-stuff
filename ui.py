from tkinter import *
import os
from plotting import *
import matplotlib as plt

currentFig = False
stats = ["count stolen big pads", "count stolen small pads", "amount stolen big pads", "amount stolen small pads", "score", "goals", "saves", "assists", "shots", "shots conceded", "goals conceded", "shooting percentage", "bpm", "avg boost", "amount collected", "0 boost time", "100 boost time", "amount used while supersonic", "amount overfill total", "time slow speed", "time boost speed", "time supersonic speed", "time on ground", "time low in air"]
teams = "teams/"
options = [file for file in os.listdir(teams) if file.endswith(".csv")]
# Create object 
root = Tk() 


def compare():
    compare_teams((teams+clicked.get()), (teams+clicked2.get()), [clicked3.get()])

clicked = StringVar()
clicked.set(options[0])

clicked2 = StringVar()
clicked2.set(options[0])
clicked3 = StringVar()
clicked3.set(stats[0])


drop = OptionMenu(root, clicked, *options)
drop2 = OptionMenu(root, clicked2, *options)
drop3 = OptionMenu(root, clicked3, *stats)
drop3.pack()
drop2.pack()
drop.pack()
button = Button(root, text = "Plot Stats", command=compare).pack()
mainloop()