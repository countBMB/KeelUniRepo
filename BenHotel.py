import csv
from _datetime import datetime
import random

FMT = '%Y-%m-%d'
myList = []


# This function displays the price of each room.
def Priceselector(price):
    try:
        with open('ben_hotel_room.csv', newline='') as csvfile:
            for row in csv.reader(csvfile):
                if row[1] == str(price):
                    return row[3]
    except FileNotFoundError:
        print("File not found. Check the path variable and filename")


# This function calculates the number of days that a user has booked.
def numOfdays(chkout, chkin):
    daysoutput = 0
    daysIn = chkout - chkin
    if daysIn.days == 0:
        daysoutput = 1
    else:
        daysoutput = daysIn.days
    return daysoutput


# This function cancels the reservation by setting the cancelled column in the csv to Yes
def cancel(roomID):
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
    cancelReceipt(roomID)


# This function generates 3 random numbers for the Reservation ID
def generate_random_id():
    random_id = random.randint(100, 9999)
    return str(random_id)


# This function uses alphabets to make sure rooms are booked based on availability
def RoomConstraint(roomoutput):
    with open('ben_hotel_room.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    for i, row in enumerate(data):
        if row[1] == str(roomoutput) and str(roomoutput) == 'Standard-Single' and row[5] == 'A':
            data[i][5] = 'B'
        elif row[1] == str(roomoutput) and str(roomoutput) == 'Standard-Single' and row[5] == 'B':
            data[i][5] = 'F'
        elif row[1] == str(roomoutput) and str(roomoutput) == 'Standard-Double' and row[5] == 'A':
            data[i][5] = 'B'
        elif row[1] == str(roomoutput) and str(roomoutput) == 'Standard-Double' and row[5] == 'B':
            data[i][5] = 'C'
        elif row[1] == str(roomoutput) and str(roomoutput) == 'Standard-Double' and row[5] == 'C':
            data[i][5] = 'D'
        elif row[1] == str(roomoutput) and str(roomoutput) == 'Standard-Double' and row[5] == 'D':
            data[i][5] = 'F'
        elif row[1] == str(roomoutput) and str(roomoutput) == 'Deluxe-Double' and row[5] == 'A':
            data[i][5] = 'B'
        elif row[1] == str(roomoutput) and str(roomoutput) == 'Deluxe-Double' and row[5] == 'B':
            data[i][5] = 'C'
        elif row[1] == str(roomoutput) and str(roomoutput) == 'Deluxe-Double' and row[5] == 'C':
            data[i][5] = 'F'
        elif row[1] == str(roomoutput) and str(roomoutput) == 'Family' and row[5] == 'A':
            data[i][5] = 'B'
        elif row[1] == str(roomoutput) and str(roomoutput) == 'Family' and row[5] == 'B':
            data[i][5] = 'F'
        elif row[1] == str(roomoutput) and str(roomoutput) == 'Suit' and row[5] == 'A':
            data[i][5] = 'F'
            break
    with open('ben_hotel_room.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


if __name__ == "__main__":

    # This function displays the available room types to the user
    def RoomTypes():
        try:
            with open('ben_hotel_room.csv', newline='') as csvfile:
                data = csv.DictReader(csvfile)
                print("-----Available Rooms-----")
                for row in data:
                    print('[' + row['Room ID'] + ']',
                          row['Room Type'] + ' (£' + row['Price'] + '/Night - ' + row['Max People'] + ' ' + row[
                              'Person'] + ' Max)')
        except FileNotFoundError:
            print("File not found. Check the path variable and filename")

# This function prints the receipt after a booking is done successfully
    def receipt(roomID):
        try:
            with open('MyReservations.csv', newline='') as csvfile:
                for row in csv.reader(csvfile):
                    if row[0] == str(roomID):
                        toPay = int(row[7]) * int(row[4])
                        fromdate = row[5]
                        todate = row[6]
                        dt1 = datetime.strptime(fromdate, FMT)
                        dt2 = datetime.strptime(todate, FMT)
                        print('------ Reservation Details --------')
                        print('Reference Number : ' + row[0])
                        print('Name : ' + row[1])
                        print(
                            'From : ' + '{0}/{1}/{2}'.format(dt1.day, dt1.month,
                                                             dt1.year) + ' to ' + '{0}/{1}/{2}'.format(
                                dt2.day, dt2.month, dt2.year) + ' - Total: ' + row[7] + ' Night(s)')
                        print('Room Type : ' + row[2])
                        print('Room Rate : ' + row[4] + '.00')
                        print('--------------------------------------------')
                        print(row[7] + ' Night(s) X ' + row[4] + '.00 GBP')
                        print('You need to pay ' + str(toPay) + '.00 GBP')
                        print('--------------------------------------------')
                        print('Booking Completed!')
                        print('Back to Main Menu')
                        print('=============================================')
                        Menu()
                        break
                else:
                    print('Wrong room selected'.format(roomID))
        except FileNotFoundError:
            print("File not found. Check the path variable and filename")

# This function displays a receipt after cancellation is done successfully.
    def cancelReceipt(roomID):
        try:
            with open('MyReservations.csv', newline='') as csvfile:
                for row in csv.reader(csvfile):
                    if row[0] == str(roomID) and row[8] == 'Yes':
                        toPay = (70 / 100) * float(row[7]) * float(row[4])
                        roundtoPay = round(toPay, 2)
                        fromdate = row[5]
                        todate = row[6]
                        print('------ Cancellation Details --------')
                        print('Reference Number : ' + row[0])
                        print('Name : ' + row[1])
                        print('From : ' + fromdate + ' to ' + todate + ' - Total: ' + row[7] + ' Night(s)')
                        print('Room Type : ' + row[2])
                        print('Room Rate : ' + row[4] + '.00')
                        print('--------------------------------------------')
                        print('Refund 70% X ' + row[7] + ' Night(s) X ' + row[4] + '.00 GBP')
                        print('Cancellation Policy: Only 70% of room fee is refundable. ')
                        print('Your refund is ' + str(roundtoPay) + ' GBP')
                        print('--------------------------------------------')
                        print('Cancellation Completed!')
                        print('Back to Main Menu')
                        print('=============================================')
                        Menu()
                        break
                else:
                    print('Wrong room selected'.format(roomID))
        except FileNotFoundError:
            print("File not found. Check the path variable and filename")

# This function prints a receipt prior to cancelling a reservation
    def toBeCancelled(roomID):
        try:
            with open('MyReservations.csv', newline='') as csvfile:
                for row in csv.reader(csvfile):
                    if row[0] == str(roomID) and row[8] != 'Yes':
                        toPay = float(row[7]) * float(row[4])
                        roundtoPay = round(toPay, 2)
                        fromdate = row[5]
                        todate = row[6]
                        print('------ Reservation ' + row[0] + '  Details ------')
                        print('Name : ' + row[1])
                        print('From : ' + fromdate + ' to ' + todate + ' - Total: ' + row[7] + ' Night(s)')
                        print('Room Type : ' + row[2])
                        print('Room Rate : ' + row[4] + '.00')
                        print('Reservation Amount : ' + str(roundtoPay) + ' GBP')
                        print('--------------------------------------------')
                        confirm(roomID)
                        break
                else:
                    print('Wrong Reservation selected')
                    Menu()
        except FileNotFoundError:
            print("File not found. Check the path variable and filename")

# This function asks for confirmation if the user wants to cancel a reservation
    def confirm(roomID):
        switch = 1
        while switch == 1:
            try:
                option = int(input("""Do you want to cancel this reservation? 
            Confirm: 
             [1] Yes
             [2] No
        """
                                   )
                             )
                if option == 1:
                    switch = 0
                    return cancel(roomID)
                elif option == 2:
                    switch = 0
                    print('Back to Main Menu')
                    print('=============================================')
                    Menu()
                else:
                    print('Invalid Entry. Please enter 1 or 2\n')
            except ValueError:
                print('Invalid Entry. Please enter 1 or 2\n')

# This function checks to see if the room is fully booked or available.
    def RTSelector(roomType):
        global theroomName
        try:
            with open('ben_hotel_room.csv', newline='') as csvfile:
                for row in csv.reader(csvfile):
                    if row[0] == str(roomType):
                        theroomName = row[1]
                    if (row[0] == str(roomType)) and (row[5] != 'F'):
                        print(row[1] + ' room available')
                        break
                else:
                    print('Sorry, ' + theroomName + ' rooms are fully booked\n')
                    Menu()
        except FileNotFoundError:
            print("File not found. Check the path variable and filename")
        return row[1]

# This function checks if the user has entered a valid date, and it's not in the past
    def read_date(prompt, def_date=None):
        switch = 1
        while switch == 1:
            week = input(prompt) or def_date
            present = datetime.now().date()
            try:
                week = datetime.strptime(week, '%d/%m/%Y').date()
                if week >= present:
                    switch = 0
                else:
                    print('Invalid date, please check date format: dd/mm/yyyy or enter valid date\n')
            except ValueError:
                print('Invalid date, please check date format: dd/mm/yyyy or enter valid date\n')
        return week

# This function also checks to see if the checkout date is not less than the checkin date
    def read_date2(prompt, checkindate):
        switch = 1
        while switch == 1:
            week = input(prompt)
            present = datetime.now().date()
            try:
                week = datetime.strptime(week, '%d/%m/%Y').date()
                if week >= present and week >= checkindate:
                    switch = 0
                else:
                    print('Invalid date, please check date format: dd/mm/yyyy or enter valid date\n')
            except ValueError:
                print('Invalid date, please check date format: dd/mm/yyyy or enter valid date\n')
        return week

# This function checks if the user has entered the right number of people for each type of room.
    def maxvalidator(prompt, roomoutput):
        switch = 1
        while switch == 1:
            max = int(input(prompt))
            try:
                if max > 0 and max < 5:
                    if roomoutput == 'Standard-Single' and max > 1:
                        print('Sorry, Standard Single rooms takes only 1 Customer ')
                    elif (roomoutput == 'Standard-Double' and max > 2) or (roomoutput == 'Deluxe-Double' and max > 2):
                        print('All Double rooms take maximum of two(2) Customers')
                    else:
                        switch = 0
                else:
                    print('Number of people should be between 1 and 4\n')
            except ValueError:
                print('Number of people should be between 1 and 4\n')
        return max

# This is the main menu that starts the program
    def TheMenu():
        switch = 1
        while switch == 1:
            try:
                print('--- Welcome to Benny Hotel--- \nMain Menu')
                print('-------------')

                print('[1] Book a room')
                print('[2] Cancel a reservation')
                print('[0] Quit')
                option = int(input('Select an option: \n'))
                if option == 1 or option == 2 or option == 0:
                    switch = 0
                    switcher(option)
                else:
                    print('Invalid Entry Please try again\n')
            except ValueError:
                print('Invalid Entry Please try again\n')

# This function checks to see if the user entered the right room type
    def RoomValidator2(prompt):
        while True:
            try:
                # Get user input
                user_input = int(input(prompt))
                if user_input == 1 or user_input == 2 or user_input == 3 or user_input == 4 or user_input == 5:
                    return RTSelector(user_input)
                else:
                    print("Invalid input: Please select the right room [1-5]")
            except ValueError:
                print("Invalid input: Please enter a valid Number.")

# This validator checks to see if the user entered the right name
    def NameValidator():
        while True:
            user_input = input("Enter your Name: ")
            # Validate the input
            if is_valid_string(user_input):
                break  # Exit the loop if the input is valid
            else:
                print("Invalid input: Please enter a valid string without numbers or special characters.")
        return user_input

# This function is part of the correct username check
    def is_valid_string(user_input):
        # Check if the input is a string
        if not isinstance(user_input, str):
            return False

        # Check if the string contains only letters
        if not user_input.isalpha():
            return False

        return True


    def is_positive_integer(x):
        return x > 0

# This code checks to see if the user entered correct reservation number
    def resvalidator():
        switch = 1
        while switch == 1:
            res = int(input('Enter Reservation Number : \n'))
            try:
                if is_positive_integer(res):
                    switch = 0
                    return toBeCancelled(res)
                else:
                    print('String entered, Please enter valid Reservation Number \n')
            except ValueError:
                print('String entered, Please enter valid Reservation Number \n')


    def Menu():
        return TheMenu()


    def checkIn():
        return read_date('Enter CheckIn Date: DD/MM/YYYY\n')


    def checkOut(checkindate):
        return read_date2('Enter CheckOut Date: DD/MM/YYYY\n', checkindate)


    def MaxChecker(roomoutput):
        return maxvalidator('Enter number of people:\n', roomoutput)


    def RoomChecker():
        return RoomValidator2('Select your preferred room: 1-5: \n')

# This switcher function controls the three menu items.
    def switcher(userinput):
        match userinput:
            case 1:
                datatoAppend = []
                while True:
                    count = 0
                    with open('MyReservations.csv', 'r') as file:
                        random_id = generate_random_id()
                        myFile = csv.reader(file)
                        for row in myFile:
                            myList.append(row)
                    RID = random_id
                    datatoAppend.append(RID)
                    count = count + 1
                    print("--- Book a room ---  ")
                    name = NameValidator()
                    datatoAppend.append(name)
                    dateoutput = checkIn()
                    date2output = checkOut(dateoutput)
                    print()
                    RoomTypes()
                    roomoutput = RoomChecker()
                    datatoAppend.append(roomoutput)
                    count = count + 1
                    maxoutput = MaxChecker(roomoutput)
                    RoomConstraint(roomoutput)
                    datatoAppend.append(maxoutput)
                    count = count + 1
                    Price = Priceselector(roomoutput)
                    datatoAppend.append(Price)
                    count = count + 1
                    datatoAppend.append(dateoutput)
                    count = count + 1
                    datatoAppend.append(date2output)
                    count = count + 1
                    bookeddays = numOfdays(date2output, dateoutput)
                    datatoAppend.append(bookeddays)
                    count = count + 1
                    datatoAppend.append('N')
                    count = count + 1

                    if count == 8:
                        break
                file = open('MyReservations.csv', 'a', newline='')
                writer = csv.writer(file)
                writer.writerow(datatoAppend)
                file.close()
                receipt(datatoAppend[0])

            case 2:
                print('Cancellation Selected')
                resvalidator()

            case 0:
                print('Thanks for using this program ---Exiting---')
                exit()

            case _:
                print("Invalid option, Please try again")
                TheMenu()
                option = int(input('Select an option: '))
                switcher(option)


    Menu()
    pass
