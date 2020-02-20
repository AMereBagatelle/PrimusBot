from mcrcon import MCRcon
from ftplib import FTP
import Constants
import os
import credentials

continuousLogLen = 0
firstTime = True

def sendRconCommand(command):
    with MCRcon(credentials.RCON_IP, credentials.RCON_PASSWORD, port=credentials.RCON_PORT) as mcr:
        output = mcr.command(command)
        return output
        
def readLatestLogLine():
    global continuousLogLen
    global firstTime
    fileChanged = False
    checkLogLen = continuousLogLen
    currentLogLen = os.path.getsize('mcLogData/latest.log')
    ftp = FTP(host=credentials.FTP_HOST)
    ftp.login(user=credentials.FTP_USER, passwd=credentials.FTP_PASS)
    ftp.cwd('logs')
    ftp.sendcmd('TYPE i')
    ftpFileLen = int(ftp.size('latest.log'))
    if (continuousLogLen < ftpFileLen):
        with open('mcLogData/latest.log', 'w+') as fp:
            try:
                ftp.retrbinary('RETR latest.log', lambda data: fp.write(data.decode('UTF-8')), rest=continuousLogLen)
                fileChanged = True
                continuousLogLen += ftpFileLen - continuousLogLen
                print('Getting files')
            except:
                print('Was not able to get files')
    ftp.close()
    if not fileChanged or firstTime:
        print('False')
        firstTime = False
        return False
    else:
        print('True')
        return True