import paramiko
import os
import json
import getpass
import time

#Config
Config = {
    "ConnectionURL" : "",
    "Username" : "",
    "FileName" : "",
    "Arduino" : ""
}

#Config Read
configFile = open("TFUSConfig.txt", "a")
configFile = open('TFUSConfig.txt', 'r')
configFileText = configFile.read()
if configFileText != "" or input("U wanna change the saved values?[Y/N]: ") == "N":
    config = json.loads(configFileText)
    Config["ConnectionURL"] = config["ConnectionURL"]
    Config["Username"] = config["Username"]
    Config["FileName"] = config["FileName"]
    Config["Arduino"] = config["Arduino"]
    del config
else:
    Config["ConnectionURL"] = input("Enter Connection URL: ")
    Config["Username"] = input("Enter Username: ")
    Config["Password"] = getpass.getpass("Whats your password?")
    Config["FileName"] = input("File Name: ")
    Config["Arduino"] = input("Arduino Processor(Uno: m328p): ")
del configFile
#SSH FT
try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname="tcp://4.tcp.eu.ngrok.io:15480", port=22, username=Config["Username"], password=Config["Password"]) #hostname = Config["ConnectionURL"]
    sftp = client.open_sftp()
    sftp.put(os.path.join(os.getcwd(), Config["FileName"]), '/home/' + Config["Username"] + "/" + Config["FileName"])

    #SSH Exec
    stdin, stdout, stderr = client.exec_command('sudo avrdude -p ' + Config["Arduino"] + ' -c arduino -P /dev/ttyACM0 -b 115200 -U flash:w:' + Config["FileName"])
    print("Script sent to Arduino successfully!")
    stdin.close()
    newOutput = stdout.read()
    while newOutput != "END;":
        print (newOutput)
        newOutput = stdout.read()
    client.close()
except:
    print("An Error occurred during the connection process")
#sudo avrdude -p m328p -c arduino -P /dev/ttyACM0 -b 115200 -U flash:w:Test.ino.hex

