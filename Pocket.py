'''
    File name: Pocket.py
    Author: Aravind Mathi
    Date created: 8/7/2020
    Python Version: 3.6
'''

from tkinter import *
import csv
import subprocess

bnum=5

#config files to detect Browser
with open('interface.ini','r') as f:
    conf_dict={}
    for line in f:
        items=line.split('=')
        conf_dict[items[0].strip()] = items[1].strip()

#launch the java url in browser
def urllaunch(url):
    subprocess.Popen([{conf_dict["browser"]}, url])

root = Tk()
root.title("Pocket Baseline")
root.iconbitmap('logo.ico')
root.geometry("600x300")

# Processing the CSV file of SAP Baseline servers
def csvproc(text):
    with open('baseline.csv', 'r') as csv_file:
        lst = []
        csv_reader = csv.DictReader(csv_file)

        for line in csv_reader:
            if line['SID'].strip().upper()  == text or line['Hostname'].strip().upper() ==text or\
                    line['IP'].strip() == text:
                lst.append([line['SID'], line['Type'], line['Hostname'], line['IP']])
        return lst

#processing 2nd CSV file for Java urls
def csvJavaUrl(text):
    with open('javaurl.csv', 'r') as csv_file:
        lst = []
        csv_reader = csv.DictReader(csv_file)

        for line in csv_reader:
            if line['SID'].strip().upper() == text:
                lst.append([line['SID'], line['url']])
        return lst

# Destroying the text widget if the input is wrong
def desttext():
    try:
        enlst
    except:
        pass
    else:
        for col in enlst:
            col.destroy()


# Destroying the Label widget if the input is correct
def destLabel():
    try:
        global labLst
        for lab in labLst:
            lab.destroy()
        labLst = []
    except:
        pass

#To launch Putty
def launch(ip):
    subprocess.Popen("putty.exe -ssh {}".format(ip))

# if user press enter below function will get executed
def ret(event):
    #if radio button is Baseline then execute
    if select.get() == 1:
        ret_lst = csvproc(input_entry.get().strip().upper())
        global myLabel

        # If user input is invalid show invalid on screen
        if ret_lst == []:
            desttext()
            destLabel()
            myLabel = Label(root, text="Invalid Input!!!!")
            myLabel.config(font=("Courier", 20))
            myLabel.grid(row=5, column=2, columnspan=3)
            labLst.append(myLabel)

        # If user input is valid below will be executed
        else:
            destLabel()
            cnt = 0
            global enlst
            desttext()
            enlst = []
            for res in ret_lst:
                for i in range(len(res)):
                    if len(str(res[i].strip())) == 3:
                        ret_text = Text(root, height=1, width=3)
                    elif i == 1:
                        ret_text = Text(root, height=1, width=5)
                    else:
                        ret_text = Text(root, height=1, width=15)

                    ret_text.insert(1.0, res[i])
                    ret_text.grid(row=bnum + cnt, column=2 + i)
                    if i == 3:
                        myButton = Button(root, text="Launch", command=lambda opt=res[i]: launch(opt))
                        myButton.grid(row=bnum + cnt, column=4 + i)
                        enlst.append(myButton)
                    enlst.append(ret_text)
                cnt += 1
    #Copy of same above if condition, need to trim the code.
    #if the radio button is anything else other than Baseline
    else:
        desttext()
        ret_lst = csvJavaUrl(input_entry.get().strip().upper())
        #(ret_lst)
        if ret_lst == []:
            desttext()
            destLabel()
            myLabel = Label(root, text="Invalid Input!!!!")
            myLabel.config(font=("Courier", 20))
            myLabel.grid(row=82, column=2, columnspan=3)
            labLst.append(myLabel)
        else:
            destLabel()
            cnt = 0
            #global enlst
            desttext()
            enlst = []
            for res in ret_lst:
                for i in range(len(res)):
                    if len(str(res[i].strip())) == 3:
                        continue
                        ret_text = Text(root, height=1, width=3)
                    else:
                        ret_text = Text(root, height=1, width=50)

                    ret_text.insert(1.0, res[i])
                    ret_text.grid(row=82 + cnt, column=1 + i,columnspan=4)
                    if i == 1:
                        myButton = Button(root, text="Launch", command=lambda opt=res[i]: urllaunch(opt))
                        myButton.grid(row=82 + cnt, column=5 + i)
                        enlst.append(myButton)
                    enlst.append(ret_text)
                cnt += 1

# Default Widgets on screen when launched
name_label = Label(root, text="Search", padx=2, pady=5).grid(row=1, column=0)
name_label = Label(root, text="SID", padx=2, pady=5).grid(row=bnum-1, column=2)
name_label = Label(root, text="Type", padx=15, pady=5).grid(row=bnum-1, column=3)
name_label = Label(root, text="Hostname", padx=15, pady=5).grid(row=bnum-1, column=4)
name_label = Label(root, text="IP", padx=10, pady=5).grid(row=bnum-1, column=5)
#name_label = Label(root, text="Mobauser", padx=10, pady=5,width=10).grid(row=bnum-1, column=5)
name_label= Label(root, text="url", padx=10, pady=20).grid(row=82, column=1)
labLst = []
#selection of Radio button
MODES=[("Baseline",1),("JavaUrl",80)]
select= IntVar()
select.set(1)

for text,mode in MODES:
    #print(index,name)
    my_radio=Radiobutton(root,text=text,variable=select,value=mode)
    my_radio.grid(row =1+mode,column=1)

r = StringVar()
r.set('SID')
# User Input text Box
input_entry = Entry(root, text="SID", width=15, borderwidth=2, textvariable=r)
input_entry.grid(row=1, column=1)
# When user press enter will go to function ret
input_entry.bind('<Return>', ret)
root.mainloop()