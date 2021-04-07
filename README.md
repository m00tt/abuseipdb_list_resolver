# AbuseIPDB-List-Resolver
A Python script that gets a list of IPs/Hosts as input and returns their AbuseIPDB score and others useful information.<br>
Within the limits of the checks allowed by your AbuseIPDB API_KEY :)

# Requirements
You need to create your AbuseIPDB API_KEY (Dude, don't tremble, it's free).<br>
Go to [AbuseIPDB](https://www.abuseipdb.com/) > Login > Account > API > Create Key<br>
If you need to make a lot of requests you can think about buying a paid plan (Account > Plans)<br><br>

Install the following python libraries:
 - `pip install requests`
 - `pip install socket.py`

# Usage steps
 - You have to create a simple .txt file that contains the list of IPs/Hosts (1 item for each line)
 - Run AbuseIPDBlistResolver.py
 - Enter a value for search days (DEFAULT = 90 days)
 - Enter a value for the score filter (DEFAULT = ALL)
 - Enter your AbuseIPDB API_KEY
 - Enter the full path of the .txt file containing the IPs/Hosts list
 - Choose the output file format (0 = Json | 1 = Compact txt)
 - The script will create (or write) the result to AbuseIPDB_result.x file within the path from which the script was launched

# Tips
- "Search days" represents the past days in which the script looks for reports on AbuseIPDB.<br>
- "Score filter" represents the minumum value acceptable as score value.<br>
- "Compact txt" only returns a list of IPs and their score.<br><br>
While generating the results, the script is able to append data into an existing file by adding a Timestamp so that you can distinguish the various searches.<br><br>

**Pay attention**: If the IPs/Hosts are not present on AbuseIPDB Database the value will not be written into the file.

