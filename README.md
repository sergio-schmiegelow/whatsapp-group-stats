# whatsapp-group-stats
## What is it?
This is a tool to generate statistics from a WhatsApp group exported history.

## How to use?

```
python3 whatspapp_group_stats -h
usage: whatsapp_group_stats.py [-h] -i INPUTFILE [-n NBEST]
                               [-d DATETIMEFORMAT]

Generate statistics from whatsapp group history

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputfile INPUTFILE
                        whatsapp group exported history file
  -n NBEST, --nbest NBEST
                        Number of items of top list
  -d DATETIMEFORMAT, --datetimeformat DATETIMEFORMAT
                        date time parsing format (for datetime.strptime
                        function - language/country dependant)

```
Example:
```
python3 whatspapp_group_stats -i my_group_history.txt
```

## Output
A set of group statistics. Ex:
```
--------------------------------
Top 10 by number of messages:
--------------------------------
+55 41 xxxx-xxxx: 4421 messages
+55 48 xxxx-xxxx: 3971 messages
John Doe: 2519 messages
Alice Doe: 2123 messages
+1 (408) xxx-xxxx: 2021 messages
+55 48 xxxx-xxxx: 2010 messages
+55 66 xxxx-xxxx: 1998 messages
Pythagoras: 1571 messages
+55 41 xxxx-xxxx: 1549 messages
Archimedes: 1433 messages
Average of all members: 568.628571 messages

--------------------------------------------
Top 10 by total number of typed characters:
--------------------------------------------
+55 41 xxxx-xxxx: 547903 characters
+55 48 xxxx-xxxx: 214173 characters
Pythagoras: 190801 characters
+55 48 xxxx-xxxx: 189623 characters
Alice Doe: 178780 characters
+55 66 xxxx-xxxx: 164167 characters
Eratosthenes: 95697 characters
+55 41 xxxx-xxxx: 84931 characters
Pablo Picasso (EEL): 83617 characters
Archimedes: 82729 characters
Average of all members: 41188.442857 characters

-----------------------------------------
Top 10 by average message size:
-----------------------------------------
+55 27 xxxx-xxxx: 256.0 characters
+55 48 xxxx-xxxx: 157.9 characters
+41 78 xxx xx xx: 152.0 characters
+55 41 xxxx-xxxx: 149.3 characters
+55 48 xxxx-xxxx: 140.8 characters
+55 41 xxxx-xxxx1: 123.9 characters
+55 48 xxxx-xxxx: 116.6 characters
+55 41 xxxx-xxxx: 114.0 characters
+55 48 xxxx-xxxx: 106.6 characters
+55 41 xxxx-xxxx: 97.9 characters
Average of all members: 70.672159 characters

-------------------------
Top 10 used words:
-------------------------
de: 20831 occurrences
que: 10230 occurrences
o: 10030 occurrences
a: 9534 occurrences
e: 8806 occurrences
mídia: 6741 occurrences
<Arquivo: 6709 occurrences
oculto>: 6709 occurrences
do: 5753 occurrences
é: 5122 occurrences


Ploting group activity on time
Average: 51.227799 messages/day

```
A plot of the group activity. Ex:
![alt text](https://raw.githubusercontent.com/sergio-schmiegelow/whatsapp-group-stats/master/example_plot.png "Example plot")
