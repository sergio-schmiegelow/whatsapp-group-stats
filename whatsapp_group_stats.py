from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from more_itertools import sort_together
import numpy as np

HEADER_LINE = 0
TEXT_LINE = 1
NBEST = 10
#-------------------------------------------------------------------------
def parseFile(filename):
    messagesList = []
    messageDict = None
    with open(filename) as fp:
        line = fp.readline()
        while line:
            #print("-----------")
            #print("Line:",line, end = '')
            try:
                #Header line
                #01/09/2018 18:44
                #0123456789012345
                lineDateTime = datetime.strptime(line[:16], '%d/%m/%Y %H:%M')
                lineType = HEADER_LINE
            except:
                lineType = TEXT_LINE
            if lineType == HEADER_LINE:
                try:
                    memberEndIndex = line[19:].index(':')
                except:
                    #notification line
                    #print("Ignoring member status notification line")
                    line = fp.readline()
                    continue
                #print("DEBUG - lineDateTime = ",lineDateTime)
                member = line[19:][:memberEndIndex]
                #print("DEBUG - member = \"%s\""%member)
                lineText = line[19:][memberEndIndex + 1:]
                #print("messageDict = ", messageDict)
                #print("-------------------------------------------------------------")
                if messageDict is not None:
                    messagesList.append(messageDict)
                messageDict = {'dateTime':lineDateTime, 'member':member, 'text':lineText.strip(' \n')}
            else:
                #TEXT_LINE
                if messageDict is not None:
                    messageDict['text'] += " " + line.strip(' \n')
            line = fp.readline()
    if messageDict is not None:
        messagesList.append(messageDict)
    messagesList.sort(key = lambda x: x['dateTime'])
    return messagesList
#-------------------------------------------------------------------------
def plotMessagesPerDay(messagesList):
    firstDay = messagesList[0]['dateTime'].date()
    lastDay = messagesList[-1]['dateTime'].date()

    #create a dict with all days
    daysDict = {}
    day = firstDay
    while (day <= lastDay):
        #print("day =", day)
        daysDict[day] = 0
        day = day + timedelta(days=1)
    #sum number of messages in each day
    for message in messagesList:
        daysDict[message['dateTime'].date()] += 1
    #convert to lists
    days, numMessages = zip(*daysDict.items())
    sort_together([days, numMessages])
    #print("days =", days)
    #print("numMessages =", numMessages)
    print("Average: %f messages/day"%np.mean(numMessages))
    plt.plot(days, numMessages)
    plt.xticks(rotation=90)
    plt.title("Messages/day")
    plt.show()
#-------------------------------------------------------------------------
def topListByNumberOfMessages(messagesList):
    #create a dict with all members
    membersDict = {}
    for message in messagesList:
        member = message['member']
        if member not in membersDict.keys():
            membersDict[member] = 1
        else:
            membersDict[member] += 1
    #convert to lists
    members, numMessages = zip(*membersDict.items())
    numMessages, members = sort_together([numMessages, members], reverse=True)
    print("Top %d by number of messages:"%NBEST)
    for i in range(NBEST):
        print('%s: %d messages'%(members[i], numMessages[i]))
    print("Average of all members: %f messages"%np.mean(numMessages))
#-------------------------------------------------------------------------
def topListByNumberOfCharacters(messagesList):
    #create a dict with all members
    membersDict = {}
    for message in messagesList:
        member = message['member']
        text = message['text']
        if member not in membersDict.keys():
            membersDict[member] = len(text)
        else:
            membersDict[member] += len(text)
    #convert to lists
    members, numChars = zip(*membersDict.items())
    numChars, members = sort_together([numChars, members], reverse=True)
    print("Top %d by total number of typed characters:"%NBEST)
    for i in range(NBEST):
        print('%s: %d characters'%(members[i], numChars[i]))
    print("Average of all members: %f characters"%np.mean(numChars))
#-------------------------------------------------------------------------
def topListByAverageMessageSize(messagesList):
    #create a dict with all members
    membersDict = {}
    for message in messagesList:
        member = message['member']
        text = message['text']
        if member not in membersDict.keys():
            membersDict[member] = [1, len(text)]
        else:
            membersDict[member][0] += 1
            membersDict[member][1] += len(text)
    #convert to lists
    members, messagesData = zip(*membersDict.items())
    #calculate messages average size:
    averageSizes = []
    for i in range(len(messagesData)):
        averageSizes.append(float(messagesData[i][1])/ messagesData[i][0])
    averageSizes, members = sort_together([averageSizes, members], reverse=True)
    print("Top %d by average message size:"%NBEST)
    for i in range(NBEST):
        print('%s: %1.1f characters'%(members[i], averageSizes[i]))
    print("Average of all members: %f characters"%np.mean(averageSizes))
#-------------------------------------------------------------------------
filename = 'ateel_202003212015.txt'
messagesList = parseFile(filename)

print("--------------------------------------------")
topListByNumberOfMessages(messagesList)
print("--------------------------------------------")
topListByNumberOfCharacters(messagesList)
print("--------------------------------------------")
topListByAverageMessageSize(messagesList)
print("--------------------------------------------")
plotMessagesPerDay(messagesList)
