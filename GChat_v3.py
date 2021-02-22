from tkinter import Frame,Button,Entry,IntVar,END,INSERT,Radiobutton,Tk,filedialog
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
import arabic_reshaper
from bidi.algorithm import get_display
import re

# opening file dialog and selecting file destination
def open_file():
    file = filedialog.askopenfilename()
    text_entry.delete(0, END)
    text_entry.insert(0,file)

# prepare persian text for display in pyplot        
def _(text):
    return get_display(arabic_reshaper.reshape(u'%s' % str(text)))

# create window 
window = Tk()
window.title("آمار مشارکت دانش آموزان")
window.geometry("500x120+400+300")
content = Frame(window, bd = 10)
content.grid(row = 0, column = 0)
r1_content = Frame(content, bd = 5)
r1_content.grid(row=0)
r3_content = Frame(content, bd = 5)
r3_content.grid(row=1)
r4_content = Frame(content, bd = 5)
r4_content.grid(row=2)
#Select input button
btn = Button(r1_content,text="انتخاب فایل", command = open_file, width = 20)
btn.grid(row=0,column =1)


#file address field
text_entry = Entry(r1_content, width= 50)
text_entry.grid(row=0,column = 0)

chat_type = IntVar()
sky_radio = Radiobutton(r3_content, text="skyroom", variable = chat_type, value = 1)
adobe_radio = Radiobutton(r3_content, text="adobe", variable = chat_type, value = 2)
bigblue_radio = Radiobutton(r3_content, text="bigbluebutton", variable = chat_type, value = 3)
sky_radio.grid(row=0,column=0)
adobe_radio.grid(row=0,column=1)
bigblue_radio.grid(row=0,column=2)

def calculate_sky():
    #extracting data from chat file
    chat = open(text_entry.get(),"r",encoding="utf-8")
    text = ""
    for line in chat.readlines():
        text += line
    pattern = r"(.+)\n(.+\n)+\d\d\/\d\d\/\d\d\d\d, (\d\d):(\d\d):(\d\d) \w\w"
    matches = re.findall(pattern,text)
    time_dict = dict()
    for match in matches:
        hour = int(match[2])
        minute = int(match[3])
        time = hour*60+minute
        a = time_dict.get(match[0])
        if a == None :
            time_dict[match[0]] = []
        else:
            time_dict[match[0]].append(time)
    return time_dict


def calculate_adobe():
    chat_file = open(text_entry.get(),'r',encoding='utf-8')
    text = ""
    for line in  chat_file.readlines():
        text += line
    soup = BeautifulSoup(text, features="html.parser")
    time_dict = dict()
    for obj in soup.find_all("object"):
        if obj.find_next('name').text != ' ':
            a = time_dict.get(obj.find_next('name').text)
            if a == None :
                time_dict[obj.find_next('name').text] = []
            else:
                time_dict[obj.find_next('name').text].append(int(int(obj.time.text)/60000))
    return time_dict


def calculate_blue():
    chat = open(text_entry.get(),"r",encoding="utf-8")
    text = ""
    for line in chat.readlines():
        text += line
    pattern = r'\[(\d\d):(\d\d)] (.+) : (.+)'
    matches = re.findall(pattern,text)
    time_dict = dict()
    for match in matches:
        hour = int(match[0])
        minute = int(match[1])
        time = hour*60+minute
        a = time_dict.get(match[2])
        if a == None :
            time_dict[match[2]] = []
        else:
            time_dict[match[2]].append(time)
    return time_dict

#draw plot
def show_plot(time_dict):
        names = []
        times_series = []
        all_times = []
        for key in time_dict.keys():
            for x in time_dict[key]:
                all_times.append(int(x))
        min_time =  np.min(all_times)
        avg_time = np.mean(all_times) - min_time
        for key in time_dict.keys():
            names.append(_(key))
            t = []
            for x in time_dict[key]:
                t.append(int(x)-min_time)
            times_series.append(t)   
        names.append("")
        times_series.append([])
        fig1, ax1 = plt.subplots(figsize=(13,7))
        fig1.subplots_adjust(left=0.06, right=0.94 , bottom=0.3)
        ax1.set_title(_("گزارش مشارکت دانش اموزان در کلاس"))
        ax1.boxplot(times_series, medianprops={'color':'darkorange','linewidth':2}, boxprops={"color":"green",'linewidth':2})
        ax1.axhline(avg_time,linestyle="--", color='red', alpha=0.5)
        plt.annotate(_("میانگین زمان کل پیامها"),xy=(len(names),avg_time), xytext=(len(names),avg_time+5),
            arrowprops=dict(facecolor='black', shrink=0.05),rotation=90)
        plt.ylabel(_("زمان به دقیقه"),color='red')
        plt.grid(True,linestyle='--', which='major',color='blue', alpha=.25)
        for i in range(len(names)):
            y = times_series[i]
            x = np.random.normal([i+1],0.05,len(y))
            plt.plot(x, y, 'ro', alpha=0.3)
        prop = FontProperties()
        prop.set_file("IRANSansWeb.ttf")
        plt.xticks(range(1,len(names)+1),names,rotation=90, fontproperties=prop)
        plt.show()

def calculate():
    if chat_type.get() == 1:
        show_plot(calculate_sky())
    if chat_type.get() == 2:
        show_plot(calculate_adobe())
    if chat_type.get() == 3:
        show_plot(calculate_blue())
btn_3 = Button(r4_content,text="نمایش نمودار", command = calculate, width = 20)
btn_3.grid(row=0)
window.mainloop()