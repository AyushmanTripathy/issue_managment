from db import *

vpid = add_user("Vishnu Prasad", "23cse000.vishnu@giet.edu", "12345678", True)
stid = add_user("Sachin Tendulkar", "ayushman@giet.edu", "12345678", False)
vtid = add_user("Virat Kholi", "ayush@giet.edu", "12345678", False)
atid = add_user("Ayushman Tripathy", "tripathy@giet.edu", "12345678", False)

insert_complaint(vpid, stid, "Water shortage", "recently water tap near hostel broke and it has not been fixed yet, kindly look into the issue.")
insert_complaint(vpid, atid, "Attendence below 80%", "My attendence has not reached 80%, i request you to consider my attendence from the events i have participated in.")
insert_complaint(vpid, atid, "Request for equipment", "My SIH project related to IOT requires a few hardware components, i request you to kindly provide them, they are listed as folllows")
insert_complaint(vpid, vtid, "Bus shortage", "due lack of buses, much time of students are being wasted waiting at the bus stop. increasing no of buses or their frequency will help hugely.")

insert_otp("lol", 1234)

print(select_faculty())
print(select_student_complaints(vpid))
print(select_faculty_complaints(atid))
