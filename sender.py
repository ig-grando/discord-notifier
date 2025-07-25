from datetime import date
import sys
import os
import csv
import requests
import json

def verify_file(file_name):
    if not os.path.exists(file_name):
        print("The data.csv file does not exist or has a differnt name")
        return False
    if not os.access(file_name, os.R_OK | os.W_OK):
        print("The program don't have permission to modify data.csv")
        return False
    return True

date = date.today()
with open("settings.json", "r") as file:
    config = json.load(file)
webhook_url = config.get("DISCORD_WEBHOOK")
file_name = "data.csv"
if not verify_file(file_name):
    sys.exit()
with open(file_name) as arq:
    read_csv = csv.reader(arq)
    list_csv = list(read_csv)
    for row in range (len(list_csv) -1, -1, -1):
        if (date.day == int(list_csv[row][1])) and (date.month == int(list_csv[row][2])):
            message = list_csv[row][0]
            bot_name = config.get("BOT_NAME")
            data_msg = {"content": message,
                        "username": bot_name}
            awnser = requests.post(webhook_url, json=data_msg)
            if awnser.status_code ==  204:
                print("Message send sucessfully")
            else:
                print("Unable to send the message:")
                print(message)
            if int(list_csv[row][3]) == 1:
                with open(file_name) as arq:
                    list_csv = list(csv.reader(arq))
                list_csv.pop(row)
                with open(file_name, "w", newline="") as arq:
                    writer_csv = csv.writer(arq)
                    writer_csv.writerows(list_csv)
