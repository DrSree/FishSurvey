import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib import style
from matplotlib import pyplot as plt

import tkinter as tk
from tkinter import ttk
from tkinter import StringVar

import pandas as pd
import numpy as np


#Read the data from my csv files
data = pd.read_csv('data/FullData.csv', sep='|',
                    encoding = 'latin1', header=0).sort('score', ascending=False)

#Set some variables that will be used globally
DEFAULT_FISH = 'Walleye'
DEFAULT_LAKE = 'Clear Lake'

DEFAULT_WIDTH = 0.35

LARGE_FONT = ('Verdana', 12)
NORM_FONT = ('Verdana', 10)
SMALL_FONT = ('Verdana', 8)

style.use('ggplot') #Styling for the plots


def change_fish(fish):
    global DEFAULT_FISH
    DEFAULT_FISH = fish

def change_lake(lake):
    global DEFAULT_LAKE
    DEFAULT_LAKE = lake

#Main window for the app
class AnglerApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.wm_title(self, 'Fish Survey App')
        
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, TopTenPage, ScatterPage, LakeSurvey):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text='Fish Survey App', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text='Top Ten Lakes by Fish',
                            command=lambda: controller.show_frame(TopTenPage))
        button1.pack()

        button2 = ttk.Button(self, text='Survey by Lake',
                            command=lambda: controller.show_frame(LakeSurvey))
        button2.pack()

        button3 = ttk.Button(self, text='Length/Weight Scatter',
                            command=lambda: controller.show_frame(ScatterPage))
        button3.pack()
 
        text = tk.Text(self)
        
        bigfish = data[['fishType', 'lakeName', 'avgLen', 'avgWt']].sort('avgWt', ascending=False).head(1)
        bigwt = bigfish[['avgWt']].to_string(index=False, header=False)
        biglen = bigfish[['avgLen']].to_string(index=False, header=False)
        bigname = bigfish[['fishType']].to_string(index=False, header=False)
        text.insert('1.0', 'The largest fish surveyed was the'+bigname
                            +'. The average weight was'+bigwt
                            +' pounds and the average length was'+biglen+' inches long.')

        mostweight = data[['lakeName', 'countCaught']].groupby('lakeName').agg({'countCaught': np.sum})
        mostweight = mostweight.sort('countCaught', ascending=False).head(1)
        weightcount = mostweight[['countCaught']].to_string(index=False, header=False)
        weightname = str(mostweight.index.get_values()).replace('[', '').replace(']', '').replace("'", '')
        text.insert('2.0', '\nThe lake with the most fish surveyed was '
                            +weightname+' with'+weightcount+' fish recorded.')


        bestcty = data[['countyName', 'countCaught']].groupby('countyName').agg({'countCaught': np.sum})
        bestcty = bestcty.sort('countCaught', ascending=False).head(1)
        ctycount = bestcty[['countCaught']].to_string(index=False, header=False)
        ctyname = str(bestcty.index.get_values()).replace('[', '').replace(']', '').replace("'", '')
        text.insert('3.0', '\nThe county with the most fish surveyed was '
                            +ctyname+' with'+ctycount+' fish recorded.')


        bestzone = data[['countyZone', 'countCaught']].groupby('countyZone').agg({'countCaught': np.sum})
        bestzone = bestzone.sort('countCaught', ascending=False).head(1)
        zonecount = bestzone[['countCaught']].to_string(index=False, header=False)
        zonename = str(bestzone.index.get_values()).replace('[', '').replace(']', '').replace("'", '')
        text.insert('4.0', '\nThe zone with the most fish surveyed was the '
                            +zonename+' zone of Iowa with'+zonecount+' fish recorded.')


        mostfish = data[['fishType', 'countCaught']].groupby('fishType').agg({'countCaught': np.sum})
        mostfish = mostfish.sort('countCaught', ascending=False).head(1)
        fishcount = mostfish[['countCaught']].to_string(index=False, header=False)
        fishname = str(mostfish.index.get_values()).replace('[', '').replace(']', '').replace("'", '')
        text.insert('5.0', '\nThe fish surveyed the most was '
                            +fishname+' with'+fishcount+' recorded.')

        totalfish = sum(data['countCaught'])
        text.insert('6.0', '\nThe total fish surveyed was '+str(totalfish)+'.')
        
        text.pack(fill=tk.X)


class TopTenPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.titleframe = tk.Frame(self)
        self.titleframe.pack()

        self.comboframe = tk.Frame(self)
        self.comboframe.pack()

        self.canvasframe = tk.Frame(self)
        self.canvasframe.pack()


        self.label = tk.Label(self.titleframe, text='Top ten lakes to find: '+DEFAULT_FISH, font=LARGE_FONT)
        self.label.pack(anchor='center', pady=10)

        self.combovals = data['fishType'].unique()
        self.combovals.sort()
        self.var = StringVar()
        self.fishcombo = ttk.Combobox(self.comboframe, textvariable=self.var)
        self.fishcombo.config(values=list(self.combovals))
        self.fishcombo.bind('<<ComboboxSelected>>', lambda x: change_fish(self.var.get()))
        self.fishcombo.pack(side=tk.LEFT, anchor='center', padx=10, pady=10)

        self.button1 = ttk.Button(self.comboframe, text='Refresh',
                                  command=lambda: self.refresh_button())
        self.button1.pack(side=tk.LEFT, anchor='center')

        self.button2 = ttk.Button(self.comboframe, text='Home',
                                  command=lambda: controller.show_frame(StartPage))
        self.button2.pack(side=tk.LEFT, anchor='center')

        self.canvasframe.canvas = self.top_ten_plot()
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=100)

    def top_ten_plot(self):
        f = plt.figure()
        a = f.add_subplot(111)

        q1 = data[data['fishType'] == DEFAULT_FISH].head(10)
        df = q1[['avgLen', 'avgWt', 'lakeName']]

        n = np.arange(len(df['lakeName']))

        a.clear()
        a.barh(n, df['avgLen'], DEFAULT_WIDTH, label='Average Length')
        a.barh(n+DEFAULT_WIDTH, df['avgWt'], DEFAULT_WIDTH, label='Average Weight', color='g')
        a.set_yticks(n+DEFAULT_WIDTH)
        a.set_yticklabels(list(df['lakeName']), rotation=0, fontsize='small')
        a.legend(bbox_to_anchor=(.8, 1.02), loc=8, ncol=2)
        a.grid(False)
        a.invert_yaxis()

        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas = self.canvas.get_tk_widget()

        return self.canvas

    def refresh_button(self):
        self.label.config(text='Top ten lakes to find: '+DEFAULT_FISH)
        self.canvas.destroy()
        self.canvasframe.canvas = self.top_ten_plot()
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=100)

    def set_option(self):
        global DEFAULT_FISH
        DEFAULT_FISH = self.fishcombo.values.get()


class LakeSurvey(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.titleframe = tk.Frame(self)
        self.titleframe.pack()

        self.comboframe = tk.Frame(self)
        self.comboframe.pack()

        self.canvasframe = tk.Frame(self)
        self.canvasframe.pack()


        self.label = tk.Label(self.titleframe, text='Fish survey for: '+DEFAULT_LAKE, font=LARGE_FONT)
        self.label.pack(anchor='center', pady=10)

        self.combovals = data['lakeName'].unique()
        self.combovals.sort()
        self.var = StringVar()
        self.lakecombo = ttk.Combobox(self.comboframe, textvariable=self.var)
        self.lakecombo.config(values=list(self.combovals))
        self.lakecombo.bind('<<ComboboxSelected>>', lambda x: change_lake(self.var.get()))
        self.lakecombo.pack(side=tk.LEFT, anchor='center', padx=10, pady=10)

        self.button1 = ttk.Button(self.comboframe, text='Refresh',
                                  command=lambda: self.refresh_button())
        self.button1.pack(side=tk.LEFT, anchor='center')

        self.button2 = ttk.Button(self.comboframe, text='Home',
                                  command=lambda: controller.show_frame(StartPage))
        self.button2.pack(side=tk.LEFT, anchor='center')

        self.canvasframe.canvas = self.lake_plot()
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=100)

    def lake_plot(self):
        f = plt.figure()
        a = f.add_subplot(111)

        q1 = data[data['lakeName'] == DEFAULT_LAKE]
        df = q1[['avgLen', 'avgWt', 'fishType']]

        n = np.arange(len(df['fishType']))

        a.clear()
        a.bar(n, df['avgLen'], DEFAULT_WIDTH, label='Average Length')
        a.bar(n+DEFAULT_WIDTH, df['avgWt'], DEFAULT_WIDTH, label='Average Weight', color='g')
        a.set_xticks(n+DEFAULT_WIDTH)
        a.set_xticklabels(list(df['fishType']),rotation=0, fontsize='small')
        a.legend(bbox_to_anchor=(.8, 1.02), loc=8, ncol=2)
        a.grid(False)

        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas = self.canvas.get_tk_widget()

        return self.canvas

    def refresh_button(self):
        self.label.config(text='Fish survey for: '+DEFAULT_LAKE)
        self.canvas.destroy()
        self.canvasframe.canvas = self.lake_plot()
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=100)

    def set_option(self):
        global DEFAULT_LAKE
        DEFAULT_LAKE = self.lakecombo.values.get()


class ScatterPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text='With fish, length and weight have a positive relationship.\n'
                                    'The strength of the relationship is varying.\n'
                                    'The relationship begins strong, but as the fish grows longer, it weakens.',
                         font=NORM_FONT, justify=tk.CENTER)
        label.pack(pady=10, padx=10)

        self.button1 = ttk.Button(self, text='Home',
                                  command=lambda: controller.show_frame(StartPage))
        self.button1.pack()

        f = plt.figure()
        a = f.add_subplot(111)
        
        a.clear()
        a.scatter(data['avgLen'], data['avgWt'])
        a.set_xlabel('Length (inches)')
        a.set_ylabel('Weight (pounds)')
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget()
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = AnglerApp()
app.geometry('1280x720')
app.mainloop()
