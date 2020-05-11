#!/usr/bin/env python3

from datetime import datetime,timedelta
from datetime import date
from pandas import DataFrame
from numpy import datetime64
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
import matplotlib.pylab as pl
import sys
import os


# ---------------------------------------- generated csv data ------------------------------------------------
# input_df = DataFrame({"event": ["event1","event2",'event3'],"start_date": ["4/12/20","4/13/20","4/15/20"],
#                     "end_date":['4/25/20','4/22/20','5/12/20'],'type':['type1','type2','type1']})
# input_df = input_df.set_index('event')
# input_df.to_excel('schedule.xlsx')
# input_df.to_csv('schedule.csv')
# ------------------------------------------------------------------------------------------------------------

# ---------------------------------------- check number of input -------------------------------------------------
if len(sys.argv) < 4:   
    if len(sys.argv) < 2:
        print("\033[91mPlease upload a file!\033[0m")
    elif len(sys.argv) < 3:
        print("\033[91mPlease enter the title for the graph and a name for the file!\033[0m")
    else:
        print("\033[91mPlease give a name for your file\033[0m")
    quit()
# ----------------------------------------------------------------------------------------------------------------

# upload file via the shell
input_file = sys.argv[1]
# ---------------------------------------- check file type -------------------------------------------------------
if os.path.basename(input_file).split('.')[-1] == 'xlsx':   
    # read input excel file
    input_df = pd.read_excel(input_file)
elif os.path.basename(input_file).split('.')[-1] == 'csv':
    # read input csv file
    input_df = pd.read_csv(input_file)
else: 
    print("\033[91mPlease upload an excel/csv file!\033[0m")
    quit()
# ----------------------------------------------------------------------------------------------------------------

# get length of input display events
length = len(input_df['start_date'].tolist())

# convert start_date column to a list from input dataframe
start_date_list = [date for date in input_df['start_date']]
    # --> equivalent start_date_list = input_df['start_date'].tolist()


# convert end_date column to a list from input dataframe
end_date_list = [date for date in input_df['end_date']]
    # --> equivalent end_date_list = input_df['end_date'].tolist()

# convert start_date to datetime format
start_date_list_time = []
for date in start_date_list:
    date = datetime.strptime(str(date).split(" ")[0], "%Y-%m-%d")
    start_date_list_time.append(date)

# convert end_date to datetime format
end_date_list_time = []
for date in end_date_list:
    date = datetime.strptime(str(date).split(" ")[0], "%Y-%m-%d")
    end_date_list_time.append(date)

# ---------------------------------------- validate data input ------------------------------------------------
try:
    assert start_date_list_time[0] <= end_date_list_time[0], "\033[91mEnd date is before start date!\033[0m"
except Exception as e:
    print(e)
    exit(1)
# ------------------------------------------------------------------------------------------------------------


# calculate the biggest time difference
day_difference_list = [(start_date, end_date) for start_date, end_date in zip(start_date_list_time,end_date_list_time)]

# a list of handler for each event to determine time interval
date_handler_list = []
for date in day_difference_list:
    day_difference = (date[1]-date[0]).days
    date_handler = (day_difference // 7)
    date_handler_list.append(date_handler)

# a list of formatted start date for each event
start_date_list_formatted = []
for start_date in start_date_list:
    # creformat input dates to certain format
    date = start_date.strftime("%Y-%m-%d")
    start_date_list_formatted.append(date) 
# a list of formatted end date for each event
end_date_list_formatted = []
for end_date in end_date_list:
    # convert input start date to time format, then reformat it to certain format
    date = end_date.strftime("%Y-%m-%d")
    end_date_list_formatted.append(date)

# create a two-dimensional list [[event tickles]] 
date_ticker_all = []
for i in range(len(date_handler_list)):
    date_ticker = [start_date_list_formatted[i]]
    counter = 0
    while counter < date_handler_list[i]:
        start_date_list_time[i] += timedelta(days=7)
        date_formatted = start_date_list_time[i].strftime("%Y-%m-%d")
        date_ticker.append(date_formatted)
        counter += 1
    if end_date_list_formatted[i] != date_ticker[-1]:
        date_ticker.append(end_date_list_formatted[i])
        
    date_ticker_all.append(date_ticker)

# define color order
type_list = input_df['type'].tolist()
compare_list = []
order_list = []
# get unique type of the graph
for i in range(length):
    if type_list[i] not in compare_list:
        compare_list.append(type_list[i])

for i in range(len(type_list)):
    order_list.append(compare_list.index(type_list[i]))

# create a list with idex for dataframe
idx_list = []
event_df_list = []
for dates in date_ticker_all:
    event_df = DataFrame({'Date': dates})
    event_df['Date'] = event_df['Date'].astype(datetime64)
    idx = pd.Index(event_df.Date)
    idx_list.append(idx)
    event_df_list.append(event_df)

# get unified index for dataframe
union = idx_list[0].union(idx_list[1])
for i in range(len(idx_list)-2):
    union = union.union(idx_list[i+2])

# get a dataframe that contains all events
df = pd.DataFrame(index=union)

# --------------------------------------------- predefined colors ------------------------------------------------
# list of predefined colors 
# so far it supports 7 event types
# to add more color please go to the website below
# color = ['b','g','r','c','m','y','b']
color = pl.cm.brg(np.linspace(0,0.9,len(compare_list)))
# color = pl.cm.tab10(list(range(0,len(compare_list))))
# print(colors)
# matplotlib list of named colors --> https://matplotlib.org/3.1.0/gallery/color/named_colors.html
# ----------------------------------------------------------------------------------------------------------------

# get the order of color for the plot
color_list = []
for i in order_list:
    line_color = color[i]
    color_list.append(line_color)

# print(color_list)
# create column for each event
for i in range(length):
    df['event%s' % str(i+1)] = df.index.to_series().apply(lambda x: (length-i) if x >= event_df_list[i].Date.min() and x <= event_df_list[i].Date.max() else np.NaN)
p = df.plot(ylim=[0, length+1],legend=False,color=color_list)

# plot vertical lines for each event
for i in range(length):
    plt.vlines(start_date_list_formatted[i],(length-i)-0.1,(length-i)+0.1,colors=color_list[i])
    plt.vlines(end_date_list_formatted[i],(length-i)-0.1,(length-i)+0.1,colors=color_list[i])

# generate a list for y axis to place each event
y_ticks = list(range(1,length+1))
plt.yticks(y_ticks)
# manually generate event names  -->
# event_list = ["event%s" %str(i+1) for i in reversed(input_df.index.tolist())]

# get input event name to the plot
event_list = reversed(input_df['event'].tolist())
p.set_yticklabels(event_list)

# add legend for the plot
# set legend color list
legend_color = []
for row in color_list:
    if list(row) not in legend_color:
        legend_color.append(list(row))

# legend_color = np.vstack({tuple(row) for row in color_list})


# set legend format
lines = [Line2D([0], [0], color=c, linewidth=1, linestyle='-') for c in legend_color]
# add grid to the plot
p.xaxis.grid()
# add minor ticks to the plot
p.xaxis.set_minor_locator(ticker.MultipleLocator(1))
# add major ticks to the plot
p.xaxis.set_major_locator(ticker.MultipleLocator(7))
# ----------------------------------------- change the shape of the plot ------------------------------------------
# change output shape (best value varies based on xrange and yrange) --> 4 and 6 are recommended
# p.set_aspect(6)
# ----------------------------------------------------------------------------------------------------------------
# ------------------------------------------- change font size ----------------------------------------------------
# adjust the font size of the honrizontal tickers --> size 6 or 8 are recommended
plt.xticks(fontsize=6)
# adjust the font size of the vertical tickers --> size 8 or 10 are recommended
plt.yticks(fontsize=8)
# set legend size --> size 6 is recommended
plt.legend(lines, compare_list, prop={'size': 6})
# ----------------------------------------------------------------------------------------------------------------

# ---------------------------------------- set title for the plot ------------------------------------------------
# add title to the plot
title = str(sys.argv[2])
plt.title(title)
# ----------------------------------------------------------------------------------------------------------------
# plot it 
# plt.show()
# save it
graph_name = str(sys.argv[3])
plt.savefig("./%s.png" % graph_name, bbox_inches='tight')

