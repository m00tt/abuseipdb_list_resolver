import socket
import requests
import os
import json
from datetime import datetime


def getList(filename):
    with open(filename, "r") as f:
        ip_list_tmp = f.readlines()
    ip_list_tmp = [x.strip() for x in ip_list_tmp]
    ip_list = []
    for x in ip_list_tmp:
        item = None
        try:
            ip_list.append(socket.gethostbyname(x))
        except:
            print(x+" : Unresolvable host")
    f.close()
    return ip_list

def createFile(filetype):
    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M:%S")
    if filetype == 0:
        full_path = os.path.realpath(__file__)
        f = open(os.path.dirname(full_path) + "/AbuseIPDB_results.json", 'a+')
        f.write('\n\n\n'+'Timestamp : '+now+'\n')
    else:
        full_path = os.path.realpath(__file__)
        f = open(os.path.dirname(full_path) + "/AbuseIPDB_results.txt", 'a+')
        f.write('\n\n\n'+now+'\n')
    f.close()

def checkIp(ip_list, maxAgeInDays, api_key, filetype):
    # Defining the api-endpoint
    url = 'https://api.abuseipdb.com/api/v2/check'

    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }

    for x in ip_list:
        queryString = {'ipAddress':x, 'maxAgeInDays':maxAgeInDays}
        response = requests.request(method='GET', url=url, headers=headers, params=queryString)
        # Formatted output
        decodedResponse = json.loads(response.text)
        full_path = os.path.realpath(__file__)
        if filetype == 0:
            f = open(os.path.dirname(full_path) + "/AbuseIPDB_results.json", 'a')
            f.write(json.dumps(decodedResponse, sort_keys=True, indent=4))
        else:
            data = str(decodedResponse.get("data").get("ipAddress"))
            reports = str(decodedResponse.get("data").get("abuseConfidenceScore"))
            str_tmp = "IP Address: " + data + " \tScore: " + reports + "\n"
            f = open(os.path.dirname(full_path) + "/AbuseIPDB_results.txt", 'a')
            f.writelines(str_tmp)
        f.close()



filetype = None
maxAgeInDays = 90
filename = None

tmp = input("Search days (Press enter for DEFAULT = 90 days): ")
if(tmp.strip() != ""):
    maxAgeInDays = tmp.strip()

api_key = input("Insert your AbuseIPDB API_KEY: ")
api_key = api_key.strip()

while filename == None or filename == "":
    filename = input("Enter the full path of the file to import (.txt): ")
    filename = filename.strip()

while filetype != 0 and filetype != 1:
    try:
        filetype = int(input("Choose the output format (JSON = 0, COMPACT TXT = 1): "))
    except:
        print("Dude, no jokes")

ip_list = getList(filename)
createFile(filetype)
checkIp(ip_list, maxAgeInDays, api_key, filetype)
