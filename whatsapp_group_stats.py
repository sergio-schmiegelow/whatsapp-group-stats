from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from more_itertools import sort_together
import numpy as np
import argparse

HEADER_LINE = 0
TEXT_LINE = 1
#-------------------------------------------------------------------------
def readWordsListFile(stopWordFilename):
    stopWordsList = []
    with open(stopWordFilename, 'rt') as f:
        lines = f.readlines()
        for word in lines:
            word = word.strip().lower()
            if len(word) > 0:
                stopWordsList.append(word)
    return stopWordsList
#-------------------------------------------------------------------------
def parseFile(filename, dateTimeFormat):
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
                lineDateTime = datetime.strptime(line[:16], dateTimeFormat)
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
        daysDict[day] = 0
        day = day + timedelta(days=1)
    #sum number of messages in each day
    for message in messagesList:
        daysDict[message['dateTime'].date()] += 1
    #convert to lists
    days, numMessages = zip(*daysDict.items())
    sort_together([days, numMessages])
    print("Ploting group activity on time")
    print("Average: %f messages/day"%np.mean(numMessages))
    maxIndex = np.argmax(numMessages)
    maxMessages = numMessages[maxIndex]
    maxDay = days[maxIndex]
    print("Day of maximum: %s with %d messages"%(str(maxDay), maxMessages))
    plt.plot(days, numMessages)
    plt.xticks(rotation=45)
    plt.title("Messages/day")
    plt.show()
#-------------------------------------------------------------------------
def topListByNumberOfMessages(messagesList, nBest):
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
    nBest = min(nBest, len(members))
    print("--------------------------------")
    print("Top %d by number of messages:"%nBest)
    print("--------------------------------")
    for i in range(nBest):
        print('%s: %d messages'%(members[i], numMessages[i]))
    print("Average of all members: %f messages"%np.mean(numMessages))
#-------------------------------------------------------------------------
def topListByNumberOfCharacters(messagesList, nBest):
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
    nBest = min(nBest, len(members))
    print("--------------------------------------------")
    print("Top %d by total number of typed characters:"%nBest)
    print("--------------------------------------------")
    for i in range(nBest):
        print('%s: %d characters'%(members[i], numChars[i]))
    print("Average of all members: %f characters"%np.mean(numChars))
#-------------------------------------------------------------------------
def topListByAverageMessageSize(messagesList, nBest):
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
    nBest = min(nBest, len(members))
    print("-----------------------------------------")
    print("Top %d by average message size:"%nBest)
    print("-----------------------------------------")

    for i in range(nBest):
        print('%s: %1.1f characters'%(members[i], averageSizes[i]))
    print("Average of all members: %f characters"%np.mean(averageSizes))
#-------------------------------------------------------------------------
def topListWords(messagesList, wordsToRemove, nBest):
    #create a dict with all members
    wordsDict = {}
    for message in messagesList:
        text = message['text']
        words = text.split()
        for word in words:
            word = word.lower()
            if word not in wordsToRemove:
                if word not in wordsDict.keys():
                    wordsDict[word] = 1
                else:
                    wordsDict[word] += 1
    #convert to lists
    words, occurrences = zip(*wordsDict.items())
    occurrences, words = sort_together([occurrences, words], reverse=True)
    nBest = min(nBest, len(words))
    print("-------------------------")
    print("Top %d used words:"%nBest)
    print("-------------------------")
    for i in range(nBest):
        print('%s: %d occurrences'%(words[i], occurrences[i]))
#-------------------------------------------------------------------------
parser = argparse.ArgumentParser(description='Generate statistics from whatsapp group history')
parser.add_argument('-i', '--inputfile', type = str, required = True, help = 'Whatsapp group exported history file')
parser.add_argument('-n', '--nbest', type = int, required = False, help = 'Number of items of top list (default = 10)', default = 10)
parser.add_argument('-d', '--datetimeformat', type = str, required = False, help = 'Date time parsing format (for datetime.strptime function - language/country dependant - (default = \'%%d/%%m/%%Y %%H:%%M\' - Brazil))', default = '%d/%m/%Y %H:%M')
parser.add_argument('-s', '--notremovestopwords', action = 'store_true', help = 'Do not remove stop words on calculation of top used words')
parser.add_argument('-r', '--removewordsfile', type = str, required = False, help = 'filename with words to remove on calculation of top used words')


ns = parser.parse_args()
inputFile          = ns.inputfile
nBest              = ns.nbest
dateTimeFormat     = ns.datetimeformat
notRemoveStopWords = ns.notremovestopwords
removeWordsFile    = ns.removewordsfile

if notRemoveStopWords:
    wordsToRemove = []
else:
    wordsToRemove = readWordsListFile('stopwords.txt')

if removeWordsFile:
    wordsToRemove += readWordsListFile(removeWordsFile)

messagesList = parseFile(inputFile, dateTimeFormat)

print("")
topListByNumberOfMessages(messagesList, nBest)
print("")
topListByNumberOfCharacters(messagesList, nBest)
print("")
topListByAverageMessageSize(messagesList, nBest)
print("")
topListWords(messagesList, wordsToRemove, nBest)
print("")
plotMessagesPerDay(messagesList)
