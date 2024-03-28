import tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from _datetime import datetime
from BenHotel import Priceselector
from BenHotel import numOfdays
from BenHotel import cancel
from BenHotel import generate_random_id
from BenHotel import RoomConstraint
import csv


root = Tk()
root.title("Benny Hotel")
myList = []

# Load the background image
bg_image = tk.PhotoImage(file="hotel.png")

# Create a label with the background image
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Read the CSV file
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

b_frame = Frame(root)
c_frame = Frame(root)
cancel_frame = Frame(root)
tobeCancelled_frame = Frame(root)
cancelled_Receipt_frame = Frame(root)

maxpeople_list = ['1', '2', '3', '4']


# Make sure user doesn't enter a date in the past
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


# Make sure user enters a valid Checkout date which is not less than the checkin date
def validate_date2(entry_date, exit_date):
    # Get the entered date from the entry widget
    try:
        # Convert the entered date string to a datetime object
        entered_datetime = datetime.strptime(entry_date, "%d/%m/%Y").date()
        exit_datetime = datetime.strptime(exit_date, "%d/%m/%Y").date()
        # Get the current date
        current_date = datetime.now().date()
        # Compare the entered date with the current date
        if (entered_datetime < current_date) or (exit_datetime < entered_datetime):
            messagebox.showerror("Invalid Date", "Please enter a valid Checkout date.")
        else:
            return entered_datetime
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter a valid date")


# Function to Check if the room is booked or available
def RTSelector(roomType):
    try:
        with open('ben_hotel_room.csv', newline='') as csvfile:
            for row in csv.reader(csvfile):
                if (row[1] == roomType) and (row[5] != 'F'):
                    print(row[1] + ' room available')
                    break
            else:
                return 'Null'
    except FileNotFoundError:
        print("File not found. Check the path variable and filename")


# This function gathers the reservation details after clicking submit
def submit_form():
    with open('MyReservations.csv', 'r') as file:
        random_id = generate_random_id()
        myFile = csv.reader(file)
        for row in myFile:
            myList.append(row)
    RID = random_id
    roomID = RID
    theRoom = room_dropdown.get()
    Routput = RTSelector(theRoom)
    if Routput == 'Null':
        messagebox.showerror("Error", f"Sorry,  {theRoom} fully booked.")
    else:
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
                messagebox.showerror("Error", "Standard Single rooms takes only 1 Customer")
            elif (theRoom == 'Standard-Double' and int(people) > 2) or (theRoom == 'Deluxe-Double' and int(people) > 2):
                messagebox.showerror('Error', 'All Double rooms take maximum of two(2) Customers')
            else:
                RoomConstraint(theRoom)
                save_to_csv(roomID, name, theRoom, people, Price, InDate, OutDate, days, cancelled)
        else:
            messagebox.showerror('Error', 'All fields must be filled')


b_frame_created = False


# This function saves the user reservation in MyReservations.csv file.
def save_to_csv(roomID, name, theRoom, people, rate, InDate, OutDate, days, cancelled):
    with open('MyReservations.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Check if the file is empty and write the header if needed
        if csvfile.tell() == 0:
            writer.writerow(
                ['RoomID', 'User', 'RoomType', 'MaxPeople', 'Rate', 'Checkin', 'Checkout', 'Days',
                 'IsCancelled'])

        # Write the form data to the CSV file
        writer.writerow([roomID, name, theRoom, people, rate, InDate, OutDate, days, cancelled])
        name_entry.delete(0, 'end')
        check_in_entry.delete(0, 'end')
        check_out_entry.delete(0, 'end')
        people_dropdown.delete(0, 'end')
        room_dropdown.delete(0, 'end')

    Myreceipt(roomID)


# This is a receipt to show that your reservation was successful.
def Myreceipt(roomID):
    b_frame.pack_forget()
    c_frame.pack_forget()
    cancel_frame.pack_forget()
    # c_frame.pack()
    try:
        with open('MyReservations.csv', 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                if row[0] == str(roomID):
                    toPay = int(row[7]) * int(row[4])
                    roundtoPay = round(toPay, 2)
                    fromdate = row[5]
                    todate = row[6]
                    resID = row[0]
                    username = row[1]
                    days = row[7]
                    roomType = row[2]
                    roomRate = row[4]
                    TotalPay = str(roundtoPay)
                    user_details = (
                        f"--------- Reservation Number :  {resID} ----------\n\n"
                        f"Name: {username}\n"
                        f"From :  {fromdate}  To  {todate}  - Total  :  {days}  Night(s)\n\n"
                        f"Room Type : {roomType}\n"
                        f"Room Rate : {roomRate} .00\n"
                        f"-------------------------------------------------\n\n"
                        f"Booked : {days}  Night(s) X  {roomRate}.00 GBP\n\n"
                        f"You need to pay {TotalPay} GBP\n"
                        f"-------------------------------------------------\n\n"
                        f"-------------------------------------------------\n\n"

                        f"Please write down your Reservation Number: {resID} for future references. \n"

                    )
                    messagebox.showinfo("Reservation Details", user_details)
                    TBC_created = False
                    for i in tobeCancelled_frame.winfo_children():
                        i.destroy()
                        tobeCancelled_frame.pack_forget()
                    Book_room_action()
                    break

    except FileNotFoundError:
        messagebox.showerror("Error", "CSV file not found.")


b_frame_created = False


# This function displays a form to make a reservation
def Book_room_action():
    global b_frame_created
    c_frame.forget()
    cancel_frame.forget()
    b_frame.pack()

    if not b_frame_created:
        b_frame_created = True

        global name_entry, people_dropdown, check_in_entry, check_out_entry, room_dropdown

        name_label = tk.Label(b_frame, text="Enter Your Name: ")
        name_label.pack(padx=40, pady=5)
        name_entry = tk.Entry(b_frame)
        name_entry.pack(padx=40, pady=5)

        roomlabel = tk.Label(b_frame, text="Select a room: ")
        roomlabel.pack(padx=40, pady=5)
        room_dropdown = ttk.Combobox(b_frame, values=names_list, state="readonly")
        room_dropdown.pack(padx=40, pady=5)
        room_dropdown.set("Standard-Single")

        peoplelabel = tk.Label(b_frame, text="How many people? : ")
        peoplelabel.pack(padx=40, pady=5)
        people_dropdown = ttk.Combobox(b_frame, values=maxpeople_list, state="readonly")
        people_dropdown.pack(padx=40, pady=5)
        people_dropdown.set(1)

        check_in_label = tk.Label(b_frame, text="Enter Check-in date (DD/MM/YYYY): ")
        check_in_label.pack(padx=40, pady=5)
        check_in_entry = tk.Entry(b_frame)
        check_in_entry.pack(padx=40, pady=5)

        check_out_label = tk.Label(b_frame, text="Enter Check-out date (DD/MM/YYYY): ")
        check_out_label.pack(padx=40, pady=5)
        check_out_entry = tk.Entry(b_frame)
        check_out_entry.pack(padx=40, pady=5)

        submit_button = tkinter.Button(b_frame, text='Book', bg="#127ba7", command=submit_form)
        submit_button.pack()


TBC_created = False


# This function is called after a user enters a reservation number to cancel
def toBeCancelled():
    global TBC_created
    b_frame.pack_forget()
    c_frame.pack_forget()
    cancel_frame.pack_forget()
    roomID = res_entry.get()
    if not TBC_created:
        TBC_created = True
        tobeCancelled_frame.pack()

        try:
            with open('MyReservations.csv', newline='') as csvfile:
                for row in csv.reader(csvfile):
                    if row[0] == str(roomID) and row[8] != 'Yes':
                        toPay = int(row[7]) * int(row[4])
                        roundtoPay = round(toPay, 2)
                        fromdate = row[5]
                        todate = row[6]
                        TotalPay = str(roundtoPay)
                        display_label0 = tk.Label(tobeCancelled_frame,
                                                  text='--------- Reservation Number : ' + row[0] + ' ---------')
                        display_label0.pack(padx=40, pady=5)
                        name_label = tk.Label(tobeCancelled_frame, text='Name : ' + row[1])
                        name_label.pack(padx=40, pady=5)
                        from_label = tk.Label(tobeCancelled_frame, text=(
                                'From : ' + fromdate + ' to ' + todate + ' - Total: ' + row[7] + ' Night(s)'))
                        from_label.pack(padx=40, pady=5)
                        roomType_label = tk.Label(tobeCancelled_frame, text='Room Type : ' + row[2])
                        roomType_label.pack(padx=40, pady=5)
                        roomRate_label = tk.Label(tobeCancelled_frame, text='Room Rate : ' + row[4] + '.00')
                        roomRate_label.pack(padx=40, pady=5)
                        Paid_label = tk.Label(tobeCancelled_frame, text='Reservation Amount : ' + TotalPay + ' GBP')
                        Paid_label.pack(padx=40, pady=5)
                        dash_label = tk.Label(tobeCancelled_frame, text='---------------------------')
                        dash_label.pack(padx=40, pady=5)
                        submit_button = tkinter.Button(tobeCancelled_frame, text='Confirm Cancellation', bg="#127ba7",
                                                       command=show_yes_no_popup)
                        submit_button.pack()
                        break
                else:
                    tobeCancelled_frame.pack_forget()
                    cancel_frame.pack_forget()
                    c_frame.pack_forget()
                    b_frame.pack_forget()
                    res_entry.delete(0, 'end')
                    messagebox.showerror("Error", "Wrong Reservation Selected. Please try again ")
                    TBC_created = False
                    Cancel_reservation()
        except FileNotFoundError:
            print("File not found. Check the path variable and filename")


# This function asks the user if they really want to cancel the reservation.
def show_yes_no_popup():
    global TBC_created
    roomID = res_entry.get()
    answer = messagebox.askyesno("Confirmation", "Are you sure you want to cancel?")
    if answer:
        cancel(roomID)
    else:
        for i in tobeCancelled_frame.winfo_children():
            i.destroy()
        tobeCancelled_frame.pack_forget()
        TBC_created = False
        res_entry.delete(0, 'end')
    Cancel_reservation()


# This function cancels the reservation in the csv file by setting the cancel column to Yes
def cancel(roomID):
    global TBC_created, cancel_frame_created

    with open('MyReservations.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    for i, row in enumerate(data):
        if row[0] == str(roomID):
            data[i][8] = 'Yes'
            break
    else:
        print(f"Reservation {roomID} not found.")
        return

    with open('MyReservations.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"Reservation  {roomID} has been {'Cancelled'}.")
    cancelLedReceipt(roomID)


# This function displays a receipt for a cancelled reservation and shows the refund amount.
def cancelLedReceipt(roomID):
    global TBC_created
    tobeCancelled_frame.pack_forget()
    cancel_frame.pack_forget()
    b_frame.pack_forget()
    c_frame.pack_forget()

    try:
        with open('MyReservations.csv', 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                if row[0] == str(roomID) and row[8] == 'Yes':
                    toPay = (70 / 100) * float(row[7]) * float(row[4])
                    roundtoPay = round(toPay, 2)
                    PaidAmt = int(row[7]) * int(row[4])
                    fromdate = row[5]
                    todate = row[6]
                    resID = row[0]
                    username = row[1]
                    days = row[7]
                    roomType = row[2]
                    roomRate = row[4]
                    Refund = str(roundtoPay)
                    user_details = (
                        f"--------- Reservation :  {resID} -----Cancelled-----\n\n"
                        f"Name: {username}\n"
                        f"From :  {fromdate} to  {todate}  - Total  :  {days}  Night(s)\n\n"
                        f"Room Type : {roomType}\n"
                        f"Room Rate : {roomRate} .00\n"
                        f"Reservation Amount : {PaidAmt}  GBP\n"
                        f"-------------------------------------------------\n\n"
                        f"Refund : 70% X  {days}  Night(s) X  {roomRate} .00 GBP\n\n"
                        f"Cancellation Policy: Only 70% of room fee is refundable.\n\n"
                        f"Your refund is {Refund} GBP\n"
                        f"-------------------------------------------------\n\n"

                    )
                    messagebox.showinfo("Cancellation Details", user_details)
                    TBC_created = False
                    for i in tobeCancelled_frame.winfo_children():
                        i.destroy()
                        tobeCancelled_frame.pack_forget()
                    res_entry.delete(0, 'end')
                    Cancel_reservation()
                    break  # Only display details for the first row

    except FileNotFoundError:
        messagebox.showerror("Error", "CSV file not found.")


cancel_frame_created = False


# This function opens for the user to enter a reservation number to be cancelled.
def Cancel_reservation():
    global cancel_frame_created
    b_frame.pack_forget()
    c_frame.pack_forget()
    cancel_frame.pack()

    if not cancel_frame_created:
        cancel_frame_created = True

        global res_entry

        name_label = tk.Label(cancel_frame, text="Enter Your Reservation Number : ")
        name_label.pack(padx=40, pady=5)
        res_entry = tk.Entry(cancel_frame)
        res_entry.pack(padx=40, pady=5)

        submit_button = tkinter.Button(cancel_frame, text='Search', bg="#127ba7", command=toBeCancelled)
        submit_button.pack()
        cancel_frame.pack()


# This function exits the program when exit button is clicked.
def quit_application():
    root.quit()

# This is the top header part of the window
frame = tk.Frame()
Intro_label = tk.Label(frame, text='Welcome to Benny Hotel!', font=('Algerian', 20))
Intro_label.pack(padx=20, pady=20)

frame.pack()
b_frame.pack()
cancel_frame.pack()

# These are the 3 menu buttons on the page.
Book_Button = tk.Button(frame, text="Book a room", command=Book_room_action)
Cancel_Button = tk.Button(frame, text="Cancel a Reservation", command=Cancel_reservation)
Quit_Button = tk.Button(frame, text="Quit", command=quit_application)

Book_Button.pack(side="left", expand=True, fill="both")
Cancel_Button.pack(side="left", expand=True, fill="both")
Quit_Button.pack(side="right", expand=True, fill="both")

root.mainloop()
