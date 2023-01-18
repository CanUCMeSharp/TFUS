import paramiko
import os
import json

#Config
Config = {
    "IPAdress" : "",
    "Username" : "",
    "Password" : "",
    "FileName" : "",
    "Arduino" : ""
}

#Config Read
configFile = open("TFUSConfig.txt", "a")
configFile = open('TFUSConfig.txt', 'r')
configFileText = configFile.read()
if configFileText != "":
    config = json.loads(configFileText)
    Config["IPAdress"] = config["IPAdress"]
    Config["Username"] = config["Username"]
    Config["Password"] = config["Password"]
    Config["FileName"] = config["FileName"]
    Config["Arduino"] = config["Arduino"]
else:
    Config["IPAdress"] = input("Enter IP-Adress: ")
    Config["Username"] = input("Enter Username: ")
    Config["Password"] = input("Enter password: ")
    Config["FileName"] = input("File Name: ")
    Config["Arduino"] = input("Arduino Processor(Uno: m328p): ")
    configFile.write(json.dumps(Config))

#SSH FT
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname = Config["IPAdress"],username=Config["Username"], password=Config["Password"])
sftp = client.open_sftp()
sftp.put(os.path.join(os.getcwd(), Config["FileName"]), '/home/' + Config["Username"] + "/" + Config["FileName"])

#SSH Exec
stdin, stdout, stderr = client.exec_command('sudo avrdude -p ' + Config["Arduino"] + ' -c arduino -P /dev/ttyACM0 -b 115200 -U flash:w:' + Config["FileName"])
stdin.close()
client.close()

#sudo avrdude -p m328p -c arduino -P /dev/ttyACM0 -b 115200 -U flash:w:Test.ino.hex

