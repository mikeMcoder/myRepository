import time
import sys
import os

class FileManager:
    def __init__(self):
        self.fileName= " "
        self.timeStamp = None
        self.header = ""
        self.time = time

    def logDate(self):      #function to log the time
        daytime = self.time.asctime()
        daytimestr = daytime.replace(' ','')
        daytimestr = daytimestr.replace(':','')
        return daytimestr

    def createHeader(self): #header to the main file where the data is saved
        header = ','.join(("timeLapse",\
                      "SerialNumber",\
                      "FirmwareVersion",\
                      "Frequency", \
                      "FrequencyError",\
                      "Power", \
                      "PowerError",\
                      "StatusF",\
                      "StatusW",\
                      "PendingBit", \
                      "PcbT",\
                      "Gmi",\
                      "Age",\
                      "F1",\
                      "F2", \
                      "SiBlock",\
                      "Gmi",\
                      "DemodR",\
                      "Pd",\
                      "FTF",\
                      "Statemachine",\
                      "ResetSource",\
                      "Sled",\
                      "MeasuredTime"
                      "\n"))
        return header
        
        
    
    def createFile(self,nameOffile):
        self.timeStamp = self.logDate()
        self.fileName = nameOffile #+ '_' + self.timeStamp
        self.file = open(self.fileName +  '.txt', 'w')
        self.header = self.createHeader()
        self.file.write(self.header)
        self.file.close()
        return self.file,self.fileName
