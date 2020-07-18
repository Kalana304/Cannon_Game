# Author: Kalana Abeywardena
# Created On: 17/07/2020

import matplotlib
import matplotlib.pyplot as plt 
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from tkinter import *
from tkinter import ttk
import pandas as pd 
from collections import defaultdict

class appclass:
    def __init__(self,  window, companies, dataFile):
        self.companies = companies
        self.dataFile = dataFile
        self.cmap = plt.cm.prism

        # creating the root window of 720 x 980 
        self.window = window
        self.window.geometry("720x980")
        self.window.title("Analysis Visualization") # title of the screen 
        
        # Placing the widgets
        mainlabel = Label(window, text = "WELCOME!!")
        mainlabel.config(font=("comic sans ms", 44, "bold"))
        mainlabel.place(relx = 0.05, rely = 0.05,relwidth = 0.9)

        labelTop = Label(window, text = "Choose Company")
        labelTop.config(font=("fixedsys", 14))
        labelTop.place(relx = 0.05, rely = 0.45,relwidth = 0.9)

        self.combo = ttk.Combobox(window, values = companies)
        self.combo.place(relx = 0.1, rely = 0.5, height = 50, relwidth = 0.7)

        button = Button (window, text="OK", command=self.open_new)
        button.place(relx = 0.8, rely = 0.5, height = 50, relwidth = 0.05)
    
    # Function to extract the data from excel sheet
    def data_extractor(self, compName):
        data = self.dataFile.parse(compName)            # reading the relevant sheet of company

        categories = {}
        map_cat = {}
        self.cat_names = []
        self.cat_scores = []
        
        ref_no = data["WBS"].tolist()                   # level number to differentiate cat and sub-cat
        scores = data["Score"].tolist()                 # scores given (read as decimal values)
        areas = data["Area of Assessment"].tolist()     # area of assessment

        for id in range(len(ref_no)):                   # loop through to get the data
            wbs_n = ref_no[id]
            floored = np.floor(wbs_n)
            if floored == wbs_n:
                categories[wbs_n] = {}                  # for each category, identify sub-cat and their score
                map_cat[areas[id]] = wbs_n              # mapping dict for later purposes
                self.cat_names.append(areas[id])
                self.cat_scores.append(scores[id])

            else:
                categories[floored][areas[id]] = scores[id]
        return categories, map_cat

    # Function to open a new window when the company name is selected
    def open_new(self):
        self.window2 = Toplevel(height = 980, width = 720)
        #print(self.combo.current())
        if self.combo.current() < 0:    # if None is selected in the drop down menu, -1 will be returned. Handling exceptions
            self.window2.destroy()
        else:
            self.compName = self.companies[self.combo.current()]    # company name selected
            self.window2.title(self.compName)                           # title of new window opened set to company name selected
            self.plot()                                             # plot pie chart for main categories
               
    # Function to plot the main category split
    def plot (self):
        _, _= self.data_extractor(self.compName)                    # calling this function assigns cat names and scores
        explode = np.ones(len(self.cat_names))*0.1                  # variables for pie chart
        colors = self.cmap(np.linspace(0,1,len(self.cat_names)))    # variables for pie chart

        self.fig = Figure(figsize=(5,5))                            # set figure size
        ax = self.fig.add_subplot(111)
        # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.pie.html
        wedges, plt_labels, _ = ax.pie( self.cat_scores, 
                                        explode=explode, 
                                        colors = colors, 
                                        center = (0,20), 
                                        textprops = dict(weight = "bold"),
                                        wedgeprops=dict(width=0.5, linewidth=4), 
                                        startangle=-40,autopct='%1.1f%%',
                                        labels=self.cat_names, 
                                        pctdistance=0.7, labeldistance=1.1)
        ax.axis('equal')
        ax.set_title(self.compName + " - Main Categories", fontsize=18, weight = "bold", pad=1.0, color = 'darkred')
                    
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window2)              # initiaitng the canvas on the opened window2
        self.canvas.get_tk_widget().place(relx = 0.05, rely = 0.15)
        self.canvas.draw()                                                          # drawing the plot on the canvas
        self.canvas._tkcanvas.pack(padx=10, pady=10, fill=BOTH, expand=True)        # placing the canvas on window2 

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window2)              # navigational toolbar to save images and move it around
        self.toolbar.update()
        
        self.exit = Button(self.window2, text="Exit", command = self.window2.destroy)   # exit button. When pressed the opened window2 will close
        self.exit.place(relx = 0.9, rely = 0.945, height = 30, relwidth = 0.08)
        
        self.make_picker(wedges)              # call a function to check whether any event happens on the shown graph
    
    # Funtion to return the plot from sub-cat to main cat plot
    def returnplot(self):
        self.clearPlotPage()
        self.plot()

    # Function to clear the current canvas. may occur a glitch due to the lag in plotting next plot
    def clearPlotPage(self):
        self.canvas._tkcanvas.destroy()
        self.toolbar.destroy()

    # Function to plot the sub categories of selected category
    def make_picker(self, wedges):
        def plot_subplot(area):
            categ, mapping = self.data_extractor(self.compName)
            scores = list(categ[mapping[area]].values())            # scores of sub categories
            subcat = list(categ[mapping[area]].keys())              # lables of sub catgories

            explode = np.ones(len(subcat))*0.1
            colors = self.cmap(np.linspace(0,1,len(subcat)))
            
            self.fig = Figure(figsize=(5,5))
            ax = self.fig.add_subplot(111)
            wedges, plt_labels, _ = ax.pie( scores, 
                                            explode=explode, 
                                            colors = colors, 
                                            wedgeprops=dict(linewidth=4),
                                            autopct='%1.1f%%',
                                            labels=subcat, 
                                            textprops = dict(weight = "bold", fontsize = 9),
                                            pctdistance=0.7, labeldistance=0.94)
            
            ax.axis('equal')
            ax.set_title("{}: {} Sub Categories".format(self.compName, area), fontsize=14, weight = "bold", pad=1.0, color = 'navy')
            
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.window2)              # drawing the new figure on the opened window2
            self.canvas.get_tk_widget().place(relx = 0.05, rely = 0.15)
            self.canvas._tkcanvas.pack(padx=10, pady=10, fill=BOTH, expand=True)
            self.canvas.draw()

            self.toolbar = NavigationToolbar2Tk(self.canvas, self.window2)
            self.toolbar.update()
            
            self.back = Button(self.window2, text="Back", command = self.returnplot)    # back button to go back to main catgory site
            self.back.place(relx = 0.9, rely = 0.94, height = 20, relwidth = 0.08)
            
        def on_pick(event):
            self.clearPlotPage()                # clears current canvas
            wedge = event.artist                # get the wedge of the pie chart where a click happens
            label = wedge.get_label()           # get the label of the wedge
            plot_subplot(label)                 # pass that label to plot the sub-catgories of that category selected
        
        for wedge in wedges:
            wedge.set_picker(True)

        self.fig.canvas.mpl_connect('pick_event', on_pick)

# main function to run
def main(fileName):
    excel_file = pd.ExcelFile(fileName)     # opens excel file instant
    sheetNames = excel_file.sheet_names     # get the sheet names (company names)
    
    window = Tk()                               # initiates main window
    appclass(window, sheetNames, excel_file)    # call the above class of app
    window.mainloop()                           # loop thruogh

if __name__ == "__main__":
    excelName = "./test.xlsx"
    matplotlib.rcParams['font.size'] = 11.0
    main(excelName)

