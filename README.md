# ERP_System

### Project Description

It is a Python based ERP System for college attendance management. It implements  
basic Python concepts and uses various libraries like numpy.py, smtplib.py,  
pyrebase.py etc. It is also interfaced with Google Firebase to store login data  
and attendance records.
It is a menu driven program with multiple features for students, faculty  
and management respectively. Some of it's features include:
* Storing online and a local attendance record of students and faculty seperately.
* The system alerts the student or facutly member if they have an attendance less than 50%.
* Faculty has an option email a leave application to the management, which would be  
  principal's email account.
* The Principal has the access to the management profile, and can view graphical  
  representation of the attendance records if  he/she wants to.


### Dependencies Required

The following depedencies should be installed in your system before running this  
program.
* pyrebase
* time
* sys
* os
* datetime
* smtplib
* pandas
* numpy
* matplotlib
* winsound

### Usage Instructions

* Clone the repository in your local machine and install the dependencies  
in your present working directory.  
* Run the code in cmd using the command `python mainLogic.py` or if you have  
  python3 installed `python3 mainLogic.py`.
* The recorded data is stored locally in `Student_data.csv` and `Faculty_data.csv`  
  respectively.
  
**Note:** This code is written for windows OS. If you are using some other OS,  
change the `os.name` value in `clear()` function accordingly.
