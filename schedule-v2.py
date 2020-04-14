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


# ---------------------------------------- generated csv data ------------------------------------------------
# input_df = DataFrame({"event": ["event1","event2",'event3'],"start_date": ["4/12/20","4/13/20","4/15/20"],
#                     "end_date":['4/25/20','4/22/20','5/12/20'],'type':['type1','type2','type1']})
# input_df.to_csv('schedule.csv')
# ------------------------------------------------------------------------------------------------------------

# read input csv file
input_df = pd.read_csv("schedule.csv")

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
    date = datetime.strptime(date, "%m/%d/%y")
    start_date_list_time.append(date)

# convert end_date to datetime format
end_date_list_time = []
for date in end_date_list:
    date = datetime.strptime(date, "%m/%d/%y")
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
    # convert input start date to time format, then reformat it to certain format
    date = datetime.strptime(start_date, "%m/%d/%y").strftime("%Y-%m-%d")
    start_date_list_formatted.append(date) 
# a list of formatted end date for each event
end_date_list_formatted = []
for end_date in end_date_list:
    # convert input start date to time format, then reformat it to certain format
    date = datetime.strptime(end_date, "%m/%d/%y").strftime("%Y-%m-%d")
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
        date_ticker.append(end_date_list_formatted[i])
        counter += 1
    date_ticker_all.append(date_ticker)

# define color order
type_list = input_df['type'].tolist()
compare_list = []
order_list = []
for i in range(length):
    if type_list[i] not in compare_list:
        compare_list.append(type_list[i])
        order_list.append(i)
    else:
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

# list of predefined colors 
color = ['b','g','r','c','m','y','b']
# matplotlib list of named colors --> https://matplotlib.org/3.1.0/gallery/color/named_colors.html

# get the order of color for the plot
color_list = []
for i in order_list:
    line_color = color[i]
    color_list.append(line_color)

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
# set legend format
lines = [Line2D([0], [0], color=c, linewidth=1, linestyle='-') for c in list(set(color_list))]
# plot legend
plt.legend(lines, input_df['type'].tolist())
# add grid to the plot
p.xaxis.grid()
# add minor ticks to the plot
p.xaxis.set_minor_locator(ticker.MultipleLocator(1))
# add major ticks to the plot
p.xaxis.set_major_locator(ticker.MultipleLocator(7))

# change output shape (best value varies based on xrange and yrange)
# p.set_aspect(2)


# ---------------------------------------- set title for the plot ------------------------------------------------
# add title to the plot
plt.title("Schedule")
# ----------------------------------------------------------------------------------------------------------------
# plot it 
plt.show()
    

