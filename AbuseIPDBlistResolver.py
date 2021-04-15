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
    ip_unresolvable = []
    for x in ip_list_tmp:
        try:
            ip_list.append(socket.gethostbyname(x))
        except:
            ip_unresolvable.append(x)
    f.close()
    return {"resolved":ip_list, "unresolved":ip_unresolvable}

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

def checkIp(ip_list, ip_unresolvable, maxAgeInDays, api_key, filetype, scoreFilter):
    # Defining the api-endpoint
    url = 'https://api.abuseipdb.com/api/v2/check'

    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }

    full_path = os.path.realpath(__file__)
    if filetype == 0:
        f = open(os.path.dirname(full_path) + "/AbuseIPDB_results.json", 'a')
    else:
        f = open(os.path.dirname(full_path) + "/AbuseIPDB_results.txt", 'a')

    for x in ip_list:
        queryString = {'ipAddress':x, 'maxAgeInDays':maxAgeInDays}
        response = requests.request(method='GET', url=url, headers=headers, params=queryString)
        # Formatted output
        decodedResponse = json.loads(response.text)
        if filetype == 0:
            if(int(decodedResponse.get("data").get("abuseConfidenceScore")) >= scoreFilter):
                f.write(json.dumps(decodedResponse, sort_keys=True, indent=4))
        else:
            data = str(decodedResponse.get("data").get("ipAddress"))
            reports = str(decodedResponse.get("data").get("abuseConfidenceScore"))
            if(int(reports)>=scoreFilter):
                str_tmp = "IP Address: " + data + "\t\tScore: " + reports + "\n"
                f.writelines(str_tmp)
    
    for x in ip_unresolvable:
        if filetype == 0:
            f.writelines('\n{"Unresolvable host" : "'+x+'" }')
        else:
            f.writelines("Unresolvable host: "+x)
            
    f.close()




filetype = None
maxAgeInDays = None
filename = None
scoreFilter = None

while maxAgeInDays == None:
    tmp = input("Search days (Press enter for DEFAULT = 90 days): ")
    if(tmp.strip() == ""):
        maxAgeInDays = 90
    else:
        try:
            tmp = int(tmp.strip())
            maxAgeInDays = tmp
        except:
            print("Dude, no jokes")

while scoreFilter == None:
    tmp = input("Enter minimum score accepted (Press enter for DEFAULT = ALL): ")
    if(tmp.strip() == ""):
        scoreFilter = 0
    else:
        try:
            tmp = int(tmp.strip())
            if(tmp >= 0 and tmp < 100):
                scoreFilter = tmp
            else:
                print("Score value must be between 0 and 99")
        except:
            print("Dude, no jokes")

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

ip_ret = getList(filename)
ip_list = ip_ret["resolved"]
ip_unresolved = ip_ret["unresolved"]
createFile(filetype)
checkIp(ip_list, ip_unresolved, maxAgeInDays, api_key, filetype, scoreFilter)
