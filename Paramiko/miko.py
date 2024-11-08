import paramiko
#import logging
import time

#logging.basicConfig(level=logging.DEBUG)

#Parent class
class Roteador:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.hostname, self.port, self.username, self.password)

    #Used by buffer commands that press space to continue is necessary
    def shell_treatment(self, command):       
        try:
            channel = self.ssh.invoke_shell()
            time.sleep(1)

            channel.send(command + "\n")
            time.sleep(1)

            output = ""

            while True:
                if channel.recv_ready():
                    data=channel.recv(1024).decode("utf-8")
                    output += data

                    if "---- More ----" in data: #Tap space to Huawei command longer results
                        channel.send(" ")
                        time.sleep(0.5)

                    if "Press any key" in data: #Tap space to Nokia command longer results
                        channel.send(" ")
                        time.sleep(0.5)

                    if "(more)" in data: #Tap space to Juniper command longer results
                        channel.send(" ")
                        time.sleep(0.5)
                        
                
                if output.strip().endswith(">") or output.strip().endswith("]") or output.strip().endswith("#"):
                    break

            output = output.split(command, 1)[1]
            return output
        except Exception as e:
            return e
    
    #Used to heritage
    def show_int(self):
        pass

#Children class
class Cisco(Roteador):
    def show_int(self, interface):
        try:
            response = self.ssh.exec_command("show interface gigabitethernet " + interface)[1]
            return response.read().decode()
        except Exception as e:
            return e

#Children class
class Huawei(Roteador):
    def show_int(self, interface):
        command = "display interface gigabitethernet " + interface
        output = self.shell_treatment(command)
        return output

#Children class
class Nokia(Roteador):
    def show_int(self, interface):
        command = "show port " + interface
        output = self.shell_treatment(command)
        return output

#Children class
class Mikrotik(Roteador):
    def show_int(self, interface):
        try:
            response = self.ssh.exec_command('/interface ethernet print detail where name="' + interface + '"')[1]
            return response.read().decode('utf-8')
        except Exception as e:
            return e

#Children class
class Juniper(Roteador):
    def show_int(self, interface):
        try:
            response = self.ssh.exec_command("show interface " + interface)[1]
            return response.read().decode()
        except Exception as e:
            return e


