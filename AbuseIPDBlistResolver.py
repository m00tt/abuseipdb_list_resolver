from datetime import datetime
import socket
import requests
import xlsxwriter
import os
import json


def getList(filename):
    with open(filename, "r") as f:
        ip_list_tmp = f.readlines()
    ip_list_tmp = [x.strip() for x in ip_list_tmp]
    ip_unresolvable = []
    for x in ip_list_tmp:
        try:
            socket.gethostbyname(x)
        except:
            ip_unresolvable.append(x)
    f.close()
    return {"resolved":ip_list_tmp, "unresolved":ip_unresolvable}

def checkIp(ip_list, ip_unresolvable, maxAgeInDays, api_key, filetype, scoreFilter):
    # Defining the api-endpoint
    url = 'https://api.abuseipdb.com/api/v2/check'

    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }
    
    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M:%S")
    if filetype == 0:
        full_path = os.path.realpath(__file__)
        f = open(os.path.dirname(full_path) + "/AbuseIPDB_results.jsonc", 'a+')
        f.write('\n\n\n//'+'Timestamp : '+now+'\n')
    elif filetype == 1:
        full_path = os.path.realpath(__file__)
        f = open(os.path.dirname(full_path) + "/AbuseIPDB_results.txt", 'a+')
        f.write('\n\n\n'+now+'\n')
    elif filetype == 2:
        now = now.replace("/", "-")
        now = now.replace(":", ".")
        full_path = os.path.realpath(__file__)
        f = xlsxwriter.Workbook(os.path.dirname(full_path) + "/AbuseIPDB_results.xlsx")
        worksheet = f.add_worksheet(now)
        worksheet.write('A1', 'Domain')
        worksheet.write('B1', 'IP Address')
        worksheet.write('C1', 'ISP')
        worksheet.write('D1', 'Country Code')
        worksheet.write('E1', 'Score')

    firstTimeJson = True
    lastTimeJson = 0
    xlsx_counter = 2

    for x in ip_list:
        try:    
            queryString = {'ipAddress':socket.gethostbyname(x), 'maxAgeInDays':maxAgeInDays}
        except:
            continue
        response = requests.request(method='GET', url=url, headers=headers, params=queryString)
        # Formatted output
        decodedResponse = json.loads(response.text)
        if filetype == 0:
            if(int(decodedResponse.get("data").get("abuseConfidenceScore")) >= scoreFilter):
                f.write(json.dumps(decodedResponse, sort_keys=True, indent=4))
        elif filetype == 1:
            data = str(decodedResponse.get("data").get("ipAddress"))
            reports = str(decodedResponse.get("data").get("abuseConfidenceScore"))
            if(int(reports)>=scoreFilter):
                str_tmp = "IP Address: " + x + "\t\t\tScore: " + reports + "\n"
                f.writelines(str_tmp)
        elif filetype == 2:
            ip = str(decodedResponse.get("data").get("ipAddress", "null"))
            domain = str(decodedResponse.get("data").get("domain", "null"))
            countryCode = str(decodedResponse.get("data").get("countryCode", "null"))
            isp = str(decodedResponse.get("data").get("isp", "null"))
            reports = str(decodedResponse.get("data").get("abuseConfidenceScore", "null"))
            if(int(reports)>=scoreFilter):
                worksheet.write('A'+str(xlsx_counter), domain)
                worksheet.write('B'+str(xlsx_counter), ip)
                worksheet.write('C'+str(xlsx_counter), isp)
                worksheet.write('D'+str(xlsx_counter), countryCode)
                worksheet.write('E'+str(xlsx_counter), reports)
            xlsx_counter+=1
    
    for x in ip_unresolvable:
        if filetype == 0:
            if firstTimeJson:
                f.writelines('{\n\t"Unresolvable hosts": [')
                firstTimeJson = False
            f.writelines('\n\t\t"'+x+'"')
            if lastTimeJson == len(ip_unresolved)-1:
                f.writelines('\n\t]\n}')
            lastTimeJson += 1
        elif filetype == 1:
            f.writelines("Unresolvable host: "+x+"\n")
        elif filetype == 2:
            worksheet.write('A'+str(xlsx_counter), x)
            worksheet.write('B'+str(xlsx_counter), "Unresolvable host")
            worksheet.write('C'+str(xlsx_counter), "Unresolvable host")
            worksheet.write('D'+str(xlsx_counter), "Unresolvable host")
            worksheet.write('E'+str(xlsx_counter), "Unresolvable host")
            xlsx_counter+=1
            
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
    tmp = input("Enter minimum score accepted (Press ENTER for DEFAULT = ALL): ")
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

api_key = input("Insert your AbuseIPDB API_KEY (Press ENTER to read from your_KEY.txt): ")
api_key = api_key.strip()
if api_key == "":
    full_path = os.path.realpath(__file__)
    f = open(os.path.dirname(full_path) + "/your_KEY.txt", 'r')
    api_key = f.readline()

while filename == None or filename == "":
    filename = input("Enter the full path of the file to import (.txt): ")
    filename = filename.strip()

while filetype != 0 and filetype != 1 and filetype != 2:
    try:
        filetype = int(input("Choose the output format (JSON = 0, COMPACT TXT = 1, XLSX = 2): "))
    except:
        print("Dude, no jokes")

ip_ret = getList(filename)
ip_list = ip_ret["resolved"]
ip_unresolved = ip_ret["unresolved"]
checkIp(ip_list, ip_unresolved, maxAgeInDays, api_key, filetype, scoreFilter)
