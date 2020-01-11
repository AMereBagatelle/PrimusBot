import json
from ftplib import FTP

def getPlayerData(outputFolder):
    ftp = FTP(host='na99.pebblehost.com')
    ftp.login(user='brennenputh@gmail.com.78133', passwd='Candace4551')
    ftp.cwd('/world/stats')
    ftp.dir()
    for filename in ftp.nlst():
        with open(outputFolder + '/' + filename, 'w') as newFile:
            ftp.retrbinary('RETR ' + filename, lambda data: newFile.write(data.decode('UTF-8')))
    ftp.cwd('/')
    ftp.dir()
    with open('whitelist.json' , 'w') as fp:
        ftp.retrbinary('RETR whitelist.json', lambda data: fp.write(data.decode('UTF-8')))
    ftp.quit()