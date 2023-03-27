import sys, os, serial, time,re,datetime
import matplotlib.pyplot as plt
import numpy as np
import tkinter.ttk as TTK
import tkinter as tk
from PIL import ImageTk, Image


''''********Global Variables**********'''
def GetTimeStamp():
    x=datetime.datetime.now()
    stamp = str(int((time.mktime(x.timetuple()))))
    return(stamp)
out = []
newtonscale=1
sensor1dataunf=np.array([])
userinput=''
flag=False
stamp=GetTimeStamp()
picname='default.png'

ports=()    #create a tuple
ports+=ports+('Please Choose a COM port',)#create first member of tuple
filename='test'

#This builds the port tuple list for the combo box drop down menu
for each_port in range(60):
    portnum=('COM'+str(each_port))
    ports=ports+(portnum,) #you need this format in order to build a tuple.
          
def initcom(something):
    global ser
    COM=combo.get()
    #COM='COM8' #make this whatever port the arduino is on if you want to use this function
    ser = serial.Serial(COM, baudrate=9600,timeout=5)
    x=ser.readline() #read off the arduino welcome message
    entryreadback.delete(0,tk.END)
    entryreadback.insert(0,x)

    val='t10*'
    ser.write(val.encode('utf-8'))
    x=ser.readline().decode('utf-8')
   
    x=re.split(':\s',x)[1]
    entrytime.delete(0,tk.END)
    entrytime.insert(0,x)

    val='c10*'
    ser.write(val.encode('utf-8'))
    x=ser.readline().decode('utf-8')
    print(x)
    x=re.split(':\s',x)[1]
    entrysamples.delete(0,tk.END)
    entrysamples.insert(0,x)
    return()

def GetTimeStamp():
    x=datetime.datetime.now()
    stamp = str(int((time.mktime(x.timetuple()))))
    return(stamp)

def CreateFigSampledData(data,xlabel='',ylabel='',title='',mysamplerate=1):
    '''#This function takes in a 1-D numpy array. It assumes that the
    data has been regularly sampled. The last entry, mysamplerate, is the
    divisor to convert the x-axis to seconds. So for example, if there are
    600 samples and the sample rate is 50ms, then sample rate would be 200
    as in 200 samples/second. In this example, 600 would be divided by 200
    to give us 3 seconds of total sampled time.
    '''
    global picname
    global stamp

    fig, ax1 = plt.subplots()
    ylimmax=1.25*(np.max(data))
    ylimmin=.75*(np.min(data))
    print('data:'+ str(data))
    t = np.linspace(0,len(data)-1,len(data))
    print(t)
    t=t*samplerate #converts sampled time to seconds
    ax1.plot(t, data, 'b')
    ax1.set_xlabel(xlabel)
# Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel(ylabel, color='b')
    ax1.tick_params('y', colors='b')
    fig.tight_layout()
    ypos=np.max(data)-.1
    plt.title(entrydescr.get())
    '''ax1.text(1,ypos, title, style='italic',\
        bbox={'facecolor':'gray', 'alpha':0.5, 'pad':10})'''
    figout=plt.gcf()


    '''Save off the picture'''
    picname=entrydescr.get()+'_'+stamp+'.png'
    figout.savefig(picname)

    '''Load the saved picture'''
    '''
    imgref = Image.open(picname)
    width,height=imgref.size
    width=int(round(width*.75))
    height=int(round(height*.75))
    imgref = imgref.resize((width, height), Image.ANTIALIAS)
    img=ImageTk.PhotoImage(imgref)
    imgref.close()
    time.sleep(50)
    '''
    img=GetCurrentPic(picname)
    return()


def GetCurrentPic(mypic):
    imgref = Image.open(mypic)
    width,height=imgref.size
    width=int(round(width*.75))
    height=int(round(height*.75))
    imgref = imgref.resize((width, height), Image.ANTIALIAS)
    img=ImageTk.PhotoImage(imgref)
    imgref.close()
    return(img)

def getrawdata():
    global ser
    global out
    out = []
    scaledata=[]
    flag = True
    ser.write('r*'.encode('utf-8'))
    count=0
    avg=ser.readline().decode('utf-8')
    entryreadback.delete(0,tk.END)
    entryreadback.insert(0,avg)

    while(flag):
        x=ser.readline().decode('utf-8')
        print("Getting raw data: here it is: ")
        print(x)
        if(x!='Capture Done!\r\n'):
            flag = True;
            try: x=int(re.split('\r',x)[0])
            except: print(x)
            else: out.append(x)
            count+=1
        else:
            flag = False;

    adcscale = entry_adc.get()
    print('The ADC Scale is: ')
    print(adcscale)
    scaledata=np.array(out)#Input data is a list. Convert it to an array
    scaledata=scaledata*float(adcscale) #To multiply all array members by a constant, this has to be an np.array
    print("What is in the samples entry box?")
    print(type(entrysamples.get()))
    print(entrysamples.get())
    samplerate = float(entrysamples.get())


    mytitle = entrydescr.get()
    CreateFigSampledData(scaledata,xlabel='time (ms)',ylabel='samples',title=mytitle,mysamplerate=samplerate)
    img=GetCurrentPic(picname)
    plotteddata.config(image='')
    plotteddata.config(image=img)
    plotteddata.image=img
    return()

def ScaleData(dataout1,scale):
    '''#Scales the input data to be in newtons and in integer form. It is
    meant to be used after readData()
    data1out is a list of data values as strings
    '''
    sensor1=[]
    for each_item in dataout1:
        d=int(re.split('\r',each_item)[0])
        sensor1.append(d)
    k=scale*np.array(sensor1)#in Newtons
    return(k) #k is an nparray of integer data values
    '''COMPORT = combo.get()
    ser=ConnectToArduino(COMPORT)

    #Tell the arduino to send the data
    ser.write('g')
    time.sleep(1)#should change this to be smarter
    dirtydata=readData(ser) #get data from arduino
    newtonscale=float(entry3.get())
    cleandata=ScaleData(dirtydata,newtonscale) #convert to int and scale it
    avgdata=np.around(GetMovingAvg(cleandata,10),2)#average it
    filename=entry1.get()+'_'+stamp
    SaveCSV(filename,avgdata)
    fig=CreateFigSampledData(avgdata)
    SaveFig(fig,filename,'.png')
    entry6.delete(0,tk.END)
    entry6.insert(0,filename+'.png')
    mypic=entry6.get()

    img=GetCurrentPic(mypic)
    plotteddata.config(image='')
    plotteddata.config(image=img)
    plotteddata.image=img
    ser.close()
    '''
    #return()

def changenumsamples():
    global ser
    val='c'+entrysamples.get()+'*'
    ser.write(val.encode('utf-8'))
    x=ser.readline().decode('utf-8')
    entryreadback.delete(0,tk.END)
    entryreadback.insert(0,x)
    return()

def changesampletime():
    global ser
    val='t'+entrytime.get()+'*'
    ser.write(val.encode('utf-8'))
    x=ser.readline().decode('utf-8')
    entryreadback.delete(0,tk.END)
    entryreadback.insert(0,x)
    return()

def getaverage():
    global ser
    val='g*'
    ser.write(val.encode('utf-8'))
    x=ser.readline().decode('utf-8')
    entryaverage.delete(0,tk.END)
    entryaverage.insert(0,x)
    return()

def alldone():
    global ser
    ser.close()
    master.quit()
    return()

ser = serial.Serial()


master=tk.Tk() #This creates the master
master.geometry('1000x700')
#Here we make an entry box for our filename
topframe=tk.Frame(master, bd=3)
topframe.grid(row=0,column=0,columnspan=2,sticky='nsew')
borderframe1=tk.Frame(master)
borderframe1.grid(row=1,column=0,columnspan=2,)
middleframe=tk.Frame(master,bd=3)
middleframe.grid(row=2,column=0,columnspan=2,sticky='nsew')
borderframe2=tk.Frame(master)
borderframe2.grid(row=3,column=0,columnspan=2,)
leftbottomframe=tk.Frame(master,bd=3)
leftbottomframe.grid(row=4,column=0,sticky='nsew')
rightbottomframe=tk.Frame(master,bd=3)
rightbottomframe.grid(row=4,column=1,sticky='nsew')

'''Items in the TOP frame'''
l1=tk.Label(topframe, text="Enter a file description here:")
l1.grid(row=0,column=0)
entrydescr=tk.Entry(topframe,width=50,bd=3) #The box is 50 pixels wide
entrydescr.insert(0,filename)
entrydescr.focus()
entrydescr.grid(row=0,column=1,sticky='nsew')
l2=tk.Label(topframe,text='Pick your COM port')
l2.grid(row=1,column=0,sticky='nsew')
combo = TTK.Combobox(topframe) #For some reason a combo box lives in a different library.
                            #It is called with TTK. See import at the top of the file

combo['values']=ports #This has to be a tuple. I populated this at the very beginning of the file
combo.current(0)
combo.grid(row=1,column=1,sticky='nsew')
combo.bind("<<ComboboxSelected>>", initcom)
l_adc=tk.Label(topframe, text="Enter an ADC scale factor here:")
l_adc.grid(row=2,column=0,sticky='nsew')
entry_adc=tk.Entry(topframe,width=50,bd=3) #The box is 50 pixels wide
entry_adc.insert(0,str(newtonscale))
entry_adc.grid(row=2,column=1,sticky='nsew')

#Serial readback window
entryreadback=tk.Entry(topframe,width=50)
entryreadback.grid(row=1,column=2,sticky='nsew',padx=100)#how do I make a column 60 wide? and put a 50 width item in it?
buttonconnect=tk.Button(topframe,text='Connect',bd=3,command=initcom)
buttonconnect.grid(row=3,column=1,sticky='nsew')


'''Widget for the borderframe1'''
lborder1=tk.Label(borderframe1,text='  ')
lborder1.pack()

'''Items in the Middle Frame'''
entrysamples=tk.Entry(middleframe,width=50,bd=3)
entrysamples.grid(row=0,column=0,sticky='nsew')
buttonsamples=tk.Button(middleframe,text='Change # of Samples',bd=3, command=changenumsamples)
buttonsamples.grid(row=1,column=0,sticky='nsew')

entrytime=tk.Entry(middleframe,width=50,bd=3)
entrytime.grid(row=0,column=1,sticky='nsew')
buttontime=tk.Button(middleframe,text='Change Sample Time',bd=3,command=changesampletime)
buttontime.grid(row=1,column=1,sticky='nsew')

entryaverage=tk.Entry(middleframe,width=50,bd=3)
entryaverage.grid(row=0,column=2,sticky='nsew')
buttonaverage=tk.Button(middleframe,text='Get Average',bd=3,command=getaverage)
buttonaverage.grid(row=1,column=2,sticky='nsew')


'''Widget for the borderframe2'''
lborder2=tk.Label(borderframe2,text=' ')
lborder2.pack()
#Here is our GO button
buttonrawdata=tk.Button(leftbottomframe,text="Get Raw Data", command=getrawdata,width=25)
buttonrawdata.grid(row = 0, column=0)
#Here is our quit button

img=GetCurrentPic(picname)
plotteddata = tk.Label(rightbottomframe, image = img)
plotteddata.grid(row=0,column=1,rowspan=2)
#sz=master.grid_size() #how big is our grid


btnend=tk.Button(leftbottomframe,text="QUIT", command=alldone,width=5)
#For some reason master.destroy hangs up but master.quit works?!?!?!?
btnend.grid(row = 1, column=0)
master.mainloop() #start running it
