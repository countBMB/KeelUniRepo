import tkinter
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import csv
from _datetime import datetime
from BenHotel import Priceselector
from BenHotel import numOfdays
from tkinter import filedialog

root = Tk()
root.title("Benny Hotel")
myList = []


def read_csv(file_path):
    room = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header if present
        for row in reader:
            room.append(row[1])
    return room


# Read names from CSV
names_list = read_csv('ben_hotel_room.csv')

# Adjust size
height = 600
width = 900
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def validate_date(entry_date):
    try:
        entered_datetime = datetime.strptime(entry_date, "%d/%m/%Y").date()
        current_date = datetime.now().date()
        if entered_datetime < current_date:
            messagebox.showerror("Invalid Date", "Please don't back date.")
        else:
            return entered_datetime
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter a valid date")


def validate_date2(entry_date, exit_date):
    try:
        entered_datetime = datetime.strptime(entry_date, "%d/%m/%Y").date()
        exit_datetime = datetime.strptime(exit_date, "%d/%m/%Y").date()
        current_date = datetime.now().date()
        if (entered_datetime < current_date) or (exit_datetime < entered_datetime):
            messagebox.showerror("Invalid Date", "Please enter a valid Checkout date.")
        else:
            return entered_datetime
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter a valid date")


def submit_form():
    with open('hotel_room.csv', 'r') as file:
        myFile = csv.reader(file)
        for row in myFile:
            myList.append(row)
    RID = len(myList) + 1
    roomID = RID
    theRoom = room_dropdown.get()
    Price = Priceselector(theRoom)
    InDate = validate_date(check_in_entry.get())
    OutDate = validate_date2(check_in_entry.get(), check_out_entry.get())

    InDateObject = datetime.strptime(check_in_entry.get(), '%d/%m/%Y').date()
    OutDateObject = datetime.strptime(check_out_entry.get(), '%d/%m/%Y').date()

    days = numOfdays(OutDateObject, InDateObject)
    cancelled = 'N'
    name = name_entry.get()
    people = people_dropdown.get()

    if name and people and InDate and OutDate and theRoom:
        if theRoom == 'Standard-Single' and int(people) > 1:
            messagebox.showerror("Error", "Standard Single rooms take only 1 Customer")
        elif (theRoom == 'Standard-Double' and int(people) > 2) or (theRoom == 'Deluxe-Double' and int(people) > 2):
            messagebox.showerror('Error', 'All Double rooms take a maximum of two(2) Customers')
        else:
            save_to_csv(roomID, name, theRoom, people, Price, InDate, OutDate, days, cancelled)

    name_entry.delete(0, 'end')
    check_in_entry.delete(0, 'end')
    check_out_entry.delete(0, 'end')
    people_dropdown.delete(0, 'end')
    room_dropdown.delete(0, 'end')





def save_to_csv(roomID, name, theRoom, people, rate, InDate, OutDate, days, cancelled):
    with open('hotel_room.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:
            writer.writerow(
                ['RoomID', 'User', 'RoomType', 'MaxPeople', 'Rate', 'Checkin', 'Checkout', 'Days', 'IsCancelled'])
        writer.writerow([roomID, name, theRoom, people, rate, InDate, OutDate, days, cancelled])
    Myreceipt(roomID)


def Myreceipt(roomID):
    b_frame = Frame(root)
    c_frame = Frame(root)
    b_frame.destroy()
    c_frame.pack()
    user_id = roomID
    with open('hotel_room.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    for i, row in enumerate(data):
        if row[0] == str(roomID):
            display_label1 = tk.Label(c_frame, text='User : ' + row[1])
            display_label1.pack(padx=40, pady=5)
            display_label2 = tk.Label(c_frame, text='Room Type: ' + row[2])
            display_label2.pack(padx=40, pady=5)
            break
    else:
        print(f"Reservation {roomID} not found.")
        return


def Book_room_action():
    b_frame = Frame(root)
    c_frame = Frame(root)
    b_frame.pack()

    global name_entry, people_dropdown, check_in_entry, check_out_entry, room_dropdown

    name_label = tk.Label(b_frame, text="Enter Your Name: ")
    name_label.pack(padx=40, pady=5)
    name_entry = tk.Entry(b_frame)
    name_entry.pack(padx=40, pady=5)

    # Dropdown for selecting names
    roomlabel = tk.Label(b_frame, text="Select a room: ")
    roomlabel.pack(padx=40, pady=5)
    room_dropdown = ttk.Combobox(b_frame, values=names_list, state="readonly")
    room_dropdown.pack(padx=40, pady=5)
    room_dropdown.set("Standard-Single")

    # Dropdown for selecting max people
    peoplelabel = tk.Label(b_frame, text="How many people? : ")
    peoplelabel.pack(padx=40, pady=5)
    people_dropdown = ttk.Combobox(b_frame, values=['1', '2', '3', '4'], state="readonly")
    people_dropdown.pack(padx=40, pady=5)
    people_dropdown.set('1')

    check_in_label = tk.Label(b_frame, text="Enter Check-in date (DD/MM/YYYY): ")
    check_in_label.pack(padx=40, pady=5)
    check_in_entry = tk.Entry(b_frame)
    check_in_entry.pack(padx=40, pady=5)

    check_out_label = tk.Label(b_frame, text="Enter Check-out date (DD/MM/YYYY): ")
    check_out_label.pack(padx=40, pady=5)
    check_out_entry = tk.Entry(b_frame)
    check_out_entry.pack(padx=40, pady=5)

    submit_button = tkinter.Button(b_frame, text='Book', command=submit_form)
    submit_button.pack()


frame2 = tk.Frame(root)

frame = tk.Frame()
Intro_label = tk.Label(frame, text='Welcome to Benny Hotel!', font=('Algerian', 20))
Intro_label.pack(padx=20, pady=20)

frame.pack()

Book_Button = tk.Button(frame, text="Book a room", command=Book_room_action)
Cancel_Button = tk.Button(frame, text="Cancel a Reservation")
Quit_Button = tk.Button(frame, text="Quit")

Book_Button.pack(side="left", expand=True, fill="both")
Cancel_Button.pack(side="left", expand=True, fill="both")
Quit_Button.pack(side="right", expand=True, fill="both")

root.mainloop()
