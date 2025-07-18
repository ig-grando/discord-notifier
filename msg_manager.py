import csv
import os
import sys
from io import SEEK_END
from dotenv import load_dotenv


def opt():
    print("-="*20)
    print("1 - Show All Reminders")
    print("2 - New Reminder")
    print("3 - Delete Remider")
    print("4 - Exit")
    print("-="*20)

#verify if the data.csv file exists
def verify_file(file_name):
    if not os.path.exists(file_name):
        with open(file_name, "w", newline="") as file:
            writer = csv.writer(file)
        return True
    if not os.access(file_name, os.R_OK | os.W_OK):
        print("The program don't have permission to modify data.csv")
        return False
    return True

#display all the messages and dates
def show_all(file_name):
    with open(file_name) as arq:
        read_csv = csv.reader(arq)
        i = 1
        for row in read_csv:
            print(str(i) + ". " + row[0] + " " + row[1] + "/" + row[2])
            i+=1

#create a new message
def new_row(file_name):
    with open(file_name, "r+", newline="") as arq:
        arq.seek(0, SEEK_END)
        name = input("Type the message: ")
        try:
            day = int(input("Type the day to remember: "))
            month = int(input("Type the month to remember: "))
            if(day > 31 or month > 12):
                print("Type a valid date")
                return
            #date =  str(day) + "/" + str(month)
            #print("0 - ")
        except ValueError:
            print("Type a valid date")
            return
        try:
            freq = int(input("Want to remove after notifing? 1 = Yes, 0 = No: "))
            if freq not in (0, 1):
                print("Type a valid number")
                return
        except ValueError:
            print("Type a valid number")
            return
        new_list = [name, day, month, freq]
        writer = csv.writer(arq)
        writer.writerow(new_list)

#remove a message
def remove_row(file_name):
    with open(file_name) as arq:
        list_csv = list(csv.reader(arq))
    print("-="*20)
    show_all(file_name)
    try:
        opt = int(input("Type the row to be removed: "))
        if opt >= 1 and opt <= len(list_csv):
            list_csv.pop(opt - 1)
            with open(file_name, "w", newline="") as arq: #this delete the old file
                writer_csv = csv.writer(arq)
                writer_csv.writerows(list_csv) #write the new file
        else:
            print("Type a valid row")
    except ValueError:
        print("Type a valid row")
        return

#main
def main():
    load_dotenv()
    file_name = os.getenv("FILE_NAME")
    if not verify_file(file_name):
        sys.exit()
    while True:
        while True:
            opt()
            try:
                option = int(input("Select the option: "))
                if((option <= 4) and (option > 0)):
                    break
                print("Type a valid value")
            except ValueError:
                print("Type a valid value")
        match option:
            case 1:
                show_all(file_name)
            case 2:
                new_row(file_name)
            case 3:
                remove_row(file_name)
            case 4:
                print("See you next time!")
                break

if __name__ == "__main__": #it's purpouse it's to not call the main while calling the remove function in sender.py
    main()