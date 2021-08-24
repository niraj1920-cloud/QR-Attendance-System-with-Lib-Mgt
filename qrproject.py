from tkinter import *
from tkinter import messagebox
import pyqrcode
import os
import sqlite3
import tkinter.messagebox as MessageBox
from tkinter.messagebox import showerror
import cv2
import pyzbar.pyzbar as pyzbar
from pyzbar.pyzbar import decode
import base64
import sys
import time
import datetime
window=Tk()
window.title("QR")
window.geometry("400x300+300+300")
def register():
    global reg_screen
    reg_screen=Toplevel(window)
    reg_screen.title("Registration")
    reg_screen.geometry("400x350+250+250")
    def generate():
        if len(subject1.get() and subject2.get() and subject3.get() and subject4.get()) != 0:
            global myQr
            myQr = pyqrcode.create(subject1.get())
            qrImage = myQr.xbm(scale=6)
            global photo
            photo = BitmapImage(data=qrImage)
        else:
            messagebox.showinfo("Error" , "All fields are required")
        try:
            showCode()
        except:
            pass
    def showCode():
        global photo
        notificationLabel.config(image=photo)
        subLabel.config(text="Showing QR Code for: " + subject1.get())

    lab1 = Label(reg_screen , text="Name" , font=("bold" , 12))
    lab1.place(x=20,y=30)

    subject1 = StringVar()
    subjectEntry = Entry(reg_screen , textvariable=subject1 , font=("Helvetica" , 12))
    subjectEntry.place(x=150,y=30)

    subLabel = Label(reg_screen , text="")
    subLabel.grid(row=3 , column=1 , sticky=N + S + E + W)

    lab2 = Label(reg_screen , text="id" , font=("bold" , 12))
    lab2.place(x=20,y=60)

    subject2 = StringVar()
    subjectEntry = Entry(reg_screen , textvariable=subject2 , font=("Helvetica" , 12))
    subjectEntry.place(x=150,y=60)

    lab3 = Label(reg_screen , text="Email" , font=("bold" , 12))
    lab3.place(x=20,y=90)

    subject3 = StringVar()
    subjectEntry = Entry(reg_screen , textvariable=subject3 , font=("Helvetica" , 12))
    subjectEntry.place(x=150,y=90)

    lab4 = Label(reg_screen , text="Contact" , font=("bold" , 12))
    lab4.place(x=20,y=120)

    subject4 = StringVar()
    subjectEntry = Entry(reg_screen , textvariable=subject4 , font=("Helvetica" , 12))
    subjectEntry.place(x=150,y=120)

    def savedata():
        s1=subject1.get()
        s2=subject2.get()
        s3=subject3.get()
        s4=subject4.get()

        if(s1=="" or s2=="" or s3=="" or s4==""):
            pass
        else:
            conn=sqlite3.connect('database1.db')
            c=conn.cursor()
            c.execute('INSERT INTO users1(name,id,Email,Contact) VALUES (?,?,?,?)',(subject1.get(),subject2.get(),subject3.get(),subject4.get()))
            conn.commit()
            MessageBox.showinfo("Registration Status" , "Registered")

    createButton = Button(reg_screen , text="Register" , font=("Helvetica" , 12) , width=10 , command=lambda:[generate(),savedata()])
    createButton.place(x=150,y=160)
    notificationLabel = Label(reg_screen)
    notificationLabel.grid(row=5 , column=1 , sticky=N + S + E + W)
    subLabel = Label(reg_screen , text="")
    subLabel.grid(row=6 , column=1 , sticky=N + S + E + W)

    totalRows = 3
    totalCols = 3
    for row in range(totalRows  + 1):
        reg_screen.grid_rowconfigure(row , weight=1)
    for col in range(totalCols + 1):
        reg_screen.grid_columnconfigure(col , weight=1)

def attendance():
    global attend_screen
    attend_screen=Toplevel(window)
    attend_screen.title("Attendance")
    attend_screen.geometry("300x200+150+150")
    unix=time.time()
    date=str(datetime.datetime.fromtimestamp(unix).strftime('%d-%m-%y %H:%M:%S'))
    timer=str(datetime.datetime.fromtimestamp(unix).strftime('%d-%m-%y'))

    def cloud():
        cap = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_PLAIN

        def checkData(data):
            try:
                success, img = cap.read()
                for barcode in decode(img):
                    data=str(barcode.data.decode('utf-8'))
            except(TypeError):
                print('Invalid ID !!!')
                return

            while True:
                with sqlite3.connect("database1.db") as db1:
                    cursor=db1.cursor()
                    find_user=("SELECT * FROM users1 WHERE name=?")
                    cursor.execute(find_user,[(data)])
                    results=cursor.fetchall()

                    if results:
                        for i in results:
                            id=i[1]
                            name=i[0]
                            Contact=i[3]
                            ts=date
                            tt=timer
                            selected=clicked.get()
                            if selected == "Python":
                                with sqlite3.connect("Python.db") as db1:
                                    cursor=db1.cursor()
                                    #cursor.execute("CREATE TABLE IF NOT EXISTS pattend( id integer , name TEXT , Contact integer , Timestamp integer)")
                                    cursor.execute("INSERT INTO pattend(id,name,Contact,Timestamp) VALUES(?,?,?,?)",(id,name,Contact,ts))
                                    MessageBox.showinfo("attendance status",i[0]+" attendance for python marked as of "+tt)
                                    db1.commit()
                            if selected == "Php":
                                with sqlite3.connect("Php.db") as db2:
                                    cursor=db2.cursor()
                                    #cursor.execute("CREATE TABLE IF NOT EXISTS phattend( id integer , name TEXT , Contact integer , Timestamp integer)")
                                    cursor.execute("INSERT INTO phattend(id,name,Contact,Timestamp) VALUES(?,?,?,?)",(id,name,Contact,ts))
                                    MessageBox.showinfo("attendance status",i[0]+" attendance for php marked as of "+tt)
                                    db2.commit()
                            if selected == "Java":
                                with sqlite3.connect("java.db") as db3:
                                    cursor=db3.cursor()
                                    #cursor.execute("CREATE TABLE IF NOT EXISTS jattend( id integer , name TEXT , Contact integer , Timestamp integer)")
                                    cursor.execute("INSERT INTO jattend(id,name,Contact,Timestamp) VALUES(?,?,?,?)",(id,name,Contact,ts))
                                    MessageBox.showinfo("attendance status",i[0]+" attendance for java marked as of "+tt)
                                    db3.commit()
                    else:
                        showerror("attendance status"," register your name first")
                    break
            
        while True:
              _, frame = cap.read()

              decodedObjects = pyzbar.decode(frame)
              for obj in decodedObjects:
                  checkData(obj.data)
                  time.sleep(1)
              cv2.imshow("Frame", frame)
              if cv2.waitKey(1)& 0xFF == ord('s'):
                  cv2.destroyAllWindows()
                  break

    def show():
        myLabel = Label(attend_screen,text=clicked.get()).pack()

    options = [
        "Python",
        "Php",
        "Java"
        ]
    clicked=StringVar()
    clicked.set(options[0])

    drop=OptionMenu(attend_screen,clicked,*options)
    drop.pack()

    B=Button(attend_screen,text="Scan",command=cloud)
    B.pack(pady=6)

def library():
    global lib_screen
    lib_screen=Toplevel(window)
    lib_screen.title("Library")
    lib_screen.geometry("400x200+150+150")
    unix=time.time()
    timer=str(datetime.datetime.fromtimestamp(unix).strftime('%d-%m-%y'))

    def cloud1():
        cap = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_PLAIN

        def checkData(data):
            try:
                success, img = cap.read()
                for barcode in decode(img):
                    data=str(barcode.data.decode('utf-8'))
            except(TypeError):
                print('Invalid ID!!!')
                return

            while True:
                e1=Entry1.get()
                e2=Entry2.get()
                with sqlite3.connect("library.db") as db1:
                    cursor=db1.cursor()
                    find_user=("SELECT * FROM lib WHERE Book=? and Author=?")
                    cursor.execute(find_user , [ (e1) , (e2) ] )
                    results=cursor.fetchall()

                    if results:
                        for i in results:
                            book=i[0]
                            author=i[1]
                            with sqlite3.connect("database1.db") as db2:
                                cursor=db2.cursor()
                                find_user1=("SELECT * FROM users1 WHERE name=?")
                                cursor.execute(find_user1,[(data)])
                                results1=cursor.fetchall()

                                if results1:
                                    for j in results1:
                                        id=j[1]
                                        name=j[0]
                                        Contact=j[3]
                                        tt=timer
                                        with sqlite3.connect("Libattend.db") as db3:
                                            cursor=db3.cursor()
                                            cursor.execute("INSERT INTO libatd(Book,Author,Dateofissue,id,name,Contact) VALUES(?,?,?,?,?,?)",(book,author,tt,id,name,Contact))
                                            MessageBox.showinfo("Library Status","entry made")
                    else:
                        showerror("attendance status","no such book or author")
                    break
            
        while True:
              _, frame = cap.read()

              decodedObjects = pyzbar.decode(frame)
              for obj in decodedObjects:
                  checkData(obj.data)
                  time.sleep(1)
              cv2.imshow("Frame", frame)
              if cv2.waitKey(1)& 0xFF == ord('s'):
                  cv2.destroyAllWindows()
                  break

    lab1 = Label(lib_screen , text="Book" , font=("bold" , 12))
    lab1.place(x=20,y=30)

    Entry1 = StringVar()
    subjectEntry = Entry(lib_screen , textvariable=Entry1 , font=("bold" , 12))
    subjectEntry.place(x=150,y=30)

    lab2 = Label(lib_screen , text="Author" , font=("bold" , 12))
    lab2.place(x=20,y=60)

    Entry2=StringVar()
    subjectEntry = Entry(lib_screen , textvariable=Entry2 , font=("bold" , 12))
    subjectEntry.place(x=150,y=60)

    def empty():
        if len(Entry1.get() and Entry2.get()) == 0:
            MessageBox.showinfo("attendance status","All fields are required")
        else:
            cloud1()

    createButton = Button(lib_screen,text="scan & issue", font=("bold" , 12) , width=10 , command=empty)
    createButton.place(x=150,y=160)

l1=Label(window,text="QR Attendance System",height="2",width="30",fg = "black",bd=5,font=("italic" , 12))
l1.pack(side=TOP, expand=YES)

b1=Button(window,text="Register",height="2",width="30",fg = "blue",bd=5,font=("italic" , 12),command=register)
b1.pack(side=TOP, expand=YES)#ipadx=20,ipady=20,side=TOP)

b2=Button(window,text="Attendance",height="2",width="30",fg = "blue",bd=5,font=("italic" , 12),command=attendance)
b2.pack(side=TOP, expand=YES)#side=TOP,ipadx=20,ipady=20,)

b3=Button(window,text="Library",height="2",width="30",fg = "blue",bd=5,font=("italic" , 12),command=library)
b3.pack(side=TOP, expand=YES)#side=TOP,ipadx=20,ipady=20,)

window.mainloop()

    
    
