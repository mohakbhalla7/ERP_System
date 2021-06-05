'''

Project: ERP System
Made by: Mohak Bhalla
'''

from datetime import datetime, date
from time import sleep
from os import system
import sys
import pyrebase
import smtplib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import winsound

config = {
    "apiKey": "apiKey",
    "authDomain": "ENTER YOUR DOMAIN NAME HERE",
    "databaseURL": "ENTER DATABASE URL HERE",
    "storageBucket": "ENTER YOUR DOMAIN NAME HERE"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
today = date.today()
today = str(today)

studentDB = pd.read_csv("Student_data.csv", index_col="Enroll ID")
facultyDB = pd.read_csv("Faculty_data.csv", index_col="Faculty ID")

#Clear function
def clear():
    system('cls')


#The start menu function
def start_function(flag='y'):
    clear()
    day = datetime.now().strftime("%a")
    if day != "Sat" and day != "Sun":
        default_attendance()
    while flag == 'y':
        try:
            print("\nERP System\n")
            ch = int(input("""Would you like to :-
                    1. Log In 
                    2. Sign Up
                    3. Exit
                 Choice : (1 / 2 / 3) -> """))
            if 1 <= ch <= 3:
                if ch == 1:
                    log_in_choice()
                if ch == 2:
                    if day != "Sat" and day != "Sun":
                        sign_up_choice()
                    else:
                        print("\nThe institution is not functional on weekends.")
                if ch == 3:
                    print(" ")
                    print("Exiting the program....")
                    sys.exit()
            else:
                print("Wrong choice:")
                continue
        except ValueError:
            print("Wrong choice:")
            continue


#Log-in menu function
def log_in_choice():
    day = datetime.now().strftime("%a")
    while 1:
        print(" ")
        ch = int(input("""Select an account type to Log In :-
                            1. For Students
                            2. For Faculty
                            3. For Management
                            4. Back
                         Choice : (1 / 2 / 3 / 4) -> """))
        if 1 <= ch <= 4:
            if ch == 1:
                if day != "Sat" and day != "Sun":
                        for_student()
                else:
                    print('''\nThe institution is not functional on weekends.
Attendance records are locked.''')
            if ch == 2:
                if day != "Sat" and day != "Sun":
                        for_faculty()
                else:
                    print('''\nThe institution is not functional on weekends.
Attendance records are locked.''')
            if ch == 3:
                for_management()
            if ch == 4:
                print(" ")
                print("Moving to previous Window....")
                start_function('y')
        else:
            print("Wrong choice.")
            continue


#Sign-up menu function
def sign_up_choice():
    while 1:
        print(" ")
        ch = int(input("""Select an account type to Sign-Up :-
                            1. For Students
                            2. For Faculty
                            3. Back
                         Choice : (1 / 2 / 3 ) -> """))
        if 1 <= ch <= 3:
            if ch == 1:
                sign_up("Student")
            elif ch == 2:
                sign_up("Faculty")
            elif ch == 3:
                print(" ")
                print("Moving to previous Window....")
                start_function('y')
            else:
                print("Wrong choice:")
                continue


#Sign-up function
def sign_up(dept_name):
    clear()
    csvdate = datetime.now().strftime("%d-%b")
    if dept_name == "Student":
        enroll_id = input("Enter your Enrollment id: ")
        a = 0
        while a == 0:
            if enroll_id not in list(db.child("Student_Data").get().val()):
                a = 1
                std_name = input("Enter Student Name: ")
                en_pass = input("Enter a new Password: ")
                data = {enroll_id: {en_pass: std_name}}
                db.child("Student_Data").update(data)
                if enroll_id in list(db.child("Student_Data").get().val()):
                    print("You have successfully enrolled as a Student.")
                studentDB.loc[enroll_id, csvdate] = ['P']
                studentDB.loc[enroll_id, ["Student Name"]] = [std_name]
                print("\nYou have been marked PRESENT, " + std_name)
                studentDB.to_csv("Student_data.csv")
            else:
                print("This Enrollment ID is already registered.")
                print("Please Log in!..")
                log_in_choice()
    else:
        faculty_id = input("Enter your Faculty id: ")
        a = 0
        while a == 0:
            if faculty_id not in list(db.child("Faculty_Data").get().val()):
                a = 1
                fac_name = input("Enter Faculty Name: ")
                en_pass = input("Enter a new Password: ")
                data = {faculty_id: {en_pass: fac_name}}
                db.child("Faculty_Data").update(data)
                if faculty_id in list(db.child("Faculty_Data").get().val()):
                    print("You have successfully enrolled as a Faculty.")
                facultyDB.loc[faculty_id, csvdate] = ['P']
                facultyDB.loc[faculty_id, ["Faculty Name"]] = [fac_name]
                print("\nYou have been marked PRESENT, " + fac_name)
                facultyDB.to_csv("Faculty_data.csv")
            else:
                print("This Faculty ID is already registered.")
                print("Please Log in!..")
                log_in_choice()


#List to string function
def list_to_string(s):
    str1 = ""
    return str1.join(s)


#Student Sign-in functon
def for_student():
    clear()
    members = db.child("Student_Data").get().val()
    b = 0
    d = 0
    while b == 0:
        enroll_id = input("Enter your Enrollment ID: ")
        if enroll_id in list(db.child("Student_Data").get().val()):
            b = 1
            while d == 0:
                password = input("Enter your Password: ")
                db_pass = list_to_string(list(members[enroll_id].keys()))
                if db_pass == password:
                    d = 1
                    attendance(enroll_id, "Student Attendance")
                    print("\nYou have been marked PRESENT, " + members[enroll_id][password] + ".")
                else:
                    d = 0
                    print("Wrong password . Try again...")

        elif input("Did you enter the correct username? (y/n) ") == 'y':
            print("Username does not exist!")
            print("Please Sign Up ")
            sign_up_choice()
        else:
            b = 0
            continue


#Faculty Sign-in functon
def for_faculty():
    clear()
    members = db.child("Faculty_Data").get().val()
    b = 0
    d = 0
    while b == 0:
        enroll_id = input("Enter your Faculty ID: ")
        if enroll_id in list(db.child("Faculty_Data").get().val()):
            b = 1
            while d == 0:
                password = input("Enter your Password: ")
                db_pass = list_to_string(list(members[enroll_id].keys()))
                if db_pass == password:
                    d = 1
                    r = attendance(enroll_id, "Faculty Attendance")
                    if r == 1:
                        print("You have been marked PRESENT, " + members[enroll_id][password] + ".")
                    elif r == 0:
                        print("Your LEAVE application has been mailed to the Principal, " + members[enroll_id][password] + ".")
                else:
                    d = 0
                    print("Wrong password . Try again...")

        elif input("Did you enter the correct username? (y/n) ") == 'y':
            print("Username does not exist!")
            print("Please Sign Up ")
            sign_up_choice()
        else:
            b = 0
            continue


#Marking default attendance function
def default_attendance():
    fac_att = db.child("Faculty Attendance").get()
    student_att = db.child("Student Attendance").get()

    csvdate = datetime.now().strftime("%d-%b")
    series = pd.Series(np.array([]))
    studentDB[csvdate] = series
    facultyDB[csvdate] = series

    for enroll_id in fac_att.each():
        Date = max(enroll_id.val())
        if today > Date:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            data = {current_time: "A"}
            facultyDB[csvdate].fillna("A", inplace=True)
            db.child("Faculty Attendance").child(enroll_id.key()).update({today: data})
            facultyDB.to_csv("Faculty_data.csv")

    for enroll_id in student_att.each():
        Date = max(enroll_id.val())
        if today > Date:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            data = {current_time: "A"}
            studentDB[csvdate].fillna("A", inplace=True)
            db.child("Student Attendance").child(enroll_id.key()).update({today: data})
            studentDB.to_csv("Student_data.csv")


#Marking attendance function
'''
        Add your email id in place of "PRINVIPAL_ID"
        to receive the email.
        Also, add 'googlemail.com' instead of 'gmail.com'
        at the end of your email id.
'''
def attendance(enroll_id, temp):
    csvdate = datetime.now().strftime("%d-%b")
    if temp == "Faculty Attendance":
        if fifty_alarm("Faculty Attendance", enroll_id) is True:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            print("Your Attendance is less than 50%. ")

        ch = input("\nInput 'P' to mark Present.\n"
                   "Input 'L' to inform for Leave.\n"
                   "Enter your choice: ").upper()
        if ch == 'L':
            emailid = input("Enter your Email ID:-  ")
            pswd = getpass.getpass("Enter your Password: ")
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.ehlo()
            s.starttls()
            s.login(emailid, pswd)
            print("\nType 'END' to end the message")
            print("Type here...")
            buffer = ''
            text = ''
            while buffer != 'END':
                text += "\n" + buffer
                buffer = input()
            message = 'Subject: {}\n\n{}'.format("Leave Application for " + csvdate, text)
            s.sendmail(emailid, "PRINCIPAL_ID", message)
            s.close()

        facultyDB = pd.read_csv("Faculty_data.csv", index_col="Faculty ID")
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        data = {current_time: ch}
        db.child(temp).child(enroll_id).update({today: data})
        tempDB = facultyDB.to_dict()
        tempDB[csvdate][int(enroll_id)] = ch
        DataB = pd.DataFrame(tempDB)
        DataB.index.name = 'Faculty ID'
        DataB.to_csv("Faculty_data.csv")
        if ch == 'P':
            return 1
        else:
            return 0

    else:
        if fifty_alarm("Student Attendance", enroll_id) is True:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            print("Your Attendance is less than 50%. ")
        studentDB = pd.read_csv("Student_data.csv", index_col="Enroll ID")
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        data = {current_time: "P"}
        db.child(temp).child(enroll_id).update({today: data})
        tempDB = studentDB.to_dict()
        tempDB[csvdate][int(enroll_id)] = 'P'
        DataB = pd.DataFrame(tempDB)
        DataB.index.name = 'Enroll ID'
        DataB.to_csv("Student_data.csv")


#Alarm function
def fifty_alarm(dept_name, enroll_id):
    if dept_name == "Faculty Attendance":
        FacultyDB = pd.read_csv("Faculty_data.csv", index_col="Faculty ID")
        tempDB = FacultyDB.to_dict()
        p = 0
        a = 0
        for ident in tempDB:
            if ident != "Faculty Name":
                if tempDB[ident][int(enroll_id)] == "P":
                    p += 1
                elif tempDB[ident][int(enroll_id)] == "A" or "L":
                    a += 1
        perc = p / (p + a) * 100
        if perc < 50.00:
            return True
    else:
        studentDB = pd.read_csv("Student_data.csv", index_col="Enroll ID")
        tempDB = studentDB.to_dict()
        p = 0
        a = 0
        for ident in tempDB:
            if ident != "Faculty Name":
                if tempDB[ident][int(enroll_id)] == "P":
                    p += 1
                elif tempDB[ident][int(enroll_id)] == "A":
                    a += 1
        perc = p / (p + a) * 100
        if perc < 50.00:
            return True


#Displaying Graph function
def view_graph(dept_name):
    if dept_name == "Student":
        studentDB = pd.read_csv("Student_data.csv", index_col="Enroll ID")
        print("")
        print(studentDB)
        tempDB = studentDB.to_dict('index')
        name = []
        percent = []
        for ident in tempDB:
            data = tempDB[ident]
            name.append(data.pop("Student Name"))
            t = 0
            c = 0
            for given_date in data:
                if data[given_date] == 'P':
                    t += 1
                    c += 1
                elif data[given_date] == 'A':
                    t += 1
            percent.append(100 * c / t)

        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(name, percent)
        ax.set_title("Student's Attendance Records Chart")
        ax.set_xlabel("Name")
        ax.set_ylabel("Attendance Percentage")
        plt.show()

    else:
        facultyDB = pd.read_csv("Faculty_data.csv", index_col="Faculty ID")
        print("")
        print(facultyDB)
        tempDB = facultyDB.to_dict('index')
        name = []
        percent = []
        for ident in tempDB:
            data = tempDB[ident]
            name.append(data.pop("Faculty Name"))
            t = 0
            c = 0
            for given_date in data:
                if data[given_date] == 'P':
                    t += 1
                    c += 1
                elif data[given_date] == 'A' or 'L':
                    t += 1
            percent.append(100 * c / t)

        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(name, percent)
        ax.set_title("Student's Attendance Records Chart")
        ax.set_xlabel("Name")
        ax.set_ylabel("Attendance Percentage")
        plt.show()


#Management view function
def for_management():
    princi = db.child("Principal").get().val()
    b = 0
    while b == 0:
        pswd = input("\nEnter the password: ")
        if pswd in db.child("Principal").child(pswd).get().key():
            print("\nWelcome Principal " + princi[pswd])
            b = 1
            while 1:
                print(" ")
                ch = int(input("""Access attendance records of:-
                                    1. Students
                                    2. Faculty
                                    3. Back
                                 Choice : (1 / 2 / 3 ) -> """))
                if 1 <= ch <= 3:
                    if ch == 1:
                        view_graph("Student")
                    if ch == 2:
                        view_graph("Faculty")
                    if ch == 3:
                        print(" ")
                        print("Moving to previous Window....")
                        log_in_choice()
                else:
                    print("Incorrect choice.")
                    continue
        else:
            b = 0
            print("Incorrect Password.")
            print("Try Again.")
            continue


#Program start commands

print("Connecting to Database....")
sleep(2)
print("Connected!")
print("Loading Main Screen....")
sleep(3)
start_function()
