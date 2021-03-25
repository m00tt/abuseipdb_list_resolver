# AbuseIPDB-List-Resolver
A Python script used to check, for each IPs/Hosts present in a list, the score on AbuseIPDB.<br>
The script allows you to create IPs/Hosts lists to check and get an immediate response regarding the score and other useful information.<br>Within the limits of the checks allowed by your AbuseIPDB API_KEY :)

# Requirements
You need to create your AbuseIPDB API_KEY (Dude, don't tremble, it's free).<br>
Go to https://www.abuseipdb.com/ > Login > Account > API > Create Key<br>
If you need to make a lot of requests you can think about buying a paid plan (Account > Plans)

# Usage steps
 - You have to create a simple .txt file that contains the list of IPs/Hosts (1 item for each line)
 - Run AbuseIPDBlistResolver.py
 - Enter a value for search days (DEFAULT = 90 days)
 - Enter your AbuseIPDB API_KEY
 - Enter the full path of the .txt file containing the IPs/Hosts list
 - Choose the output file format (0 = Json | 1 = Compact txt)
 - The script will create (or write) the result to AbuseIPDB_result.x file within the path from which the script was launched

# Tips
"Search day" represents the past days in which the script looks for reports on AbuseIPDB.<br>
The "Compact txt" will only return a list of IPs and their score.<br>
While generating the results, the script is able to overwrite an existing previous file by adding a Timestamp so that you can distinguish the various searches.<br>
