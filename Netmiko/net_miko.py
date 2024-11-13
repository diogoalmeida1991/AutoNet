from netmiko import ConnectHandler
import logging

#logging.basicConfig(level=logging.DEBUG)
#logger = logging.getLogger("netmiko")

#Platform list: github.com/ktbyers/blob/develop/PLATFORMS.md

class Roteador_SSH:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    def connect(self):
        pass

    def show_int(self):
        pass

    def show_multiples(self):
        pass


class Cisco_SSH(Roteador_SSH):
    def connect(self):
        try:
            cisco = {
                'device_type': 'cisco_ios',
                'host': self.hostname,
                'username': self.username,
                'password': self.password
                }
            self.connection = ConnectHandler(**cisco)
        except Exception as e:
            print(e)
            self.connection = -1

    def show_int(self, interface):
        output = self.connection.send_command('show interface gigabitethernet ' + interface)
        return output

    def show_multiples(self, interface):
        output = self.connection.send_config_set([
            'do show interface gigabitethernet ' + interface,
            'do show processes cpu',
            'do show ssh'
            ])
        return output

class Juniper_SSH(Roteador_SSH):
    def connect(self):
        try:
            juniper = {
                    'device_type': 'juniper_junos',
                    'host': self.hostname,
                    'username': self.username,
                    'password': self.password
                    }
            self.connection = ConnectHandler(**juniper)
        except Exception as e:
            print(e)
            self.connection = -1

    def show_int(self, interface):
        output = self.connection.send_command('show interface ' + interface)
        return output
    
    def show_multiples(self, interface):
        output = self.connection.send_config_set([
            'exit',
            'show interface ' + interface,
            'show system processes detail',
            'config'
            ])
        return output


class Mikrotik_SSH(Roteador_SSH):
    def connect(self):
        try:
            mikrotik = {
                    'device_type': 'mikrotik_routeros',
                    'host': self.hostname,
                    'username': self.username,
                    'password': self.password
                    }
            self.connection = ConnectHandler(**mikrotik)
        except Exception as e:
            print(e)
            self.connection = -1

    def show_int(self, interface):
        output = self.connection.send_command('/interface ethernet print detail where name=' + interface)
        return output
    
    def show_multiples(self, interface):
        output = self.connection.send_config_set([
            '/interface ethernet print detail where name=' + interface,
            '/system resource cpu print',
            ' ' #Necessary to show the last line.
            ])
        return output

class Nokia_SSH(Roteador_SSH):
    def connect(self):
        try:
            nokia = {
                    'device_type': 'nokia_sros',
                    'host': self.hostname,
                    'username': self.username,
                    'password': self.password
                    }
            self.connection = ConnectHandler(**nokia)
        except Exception as e:
            print(e)
            self.connection = -1

    def show_int(self, interface):
        output = self.connection.send_command('show port ' + interface)
        return output
    
    def show_multiples(self, interface):
        output = self.connection.send_config_set([
            'show port ' + interface, 
            'show system cpu'
            ])
        return output

class Huawei_SSH(Roteador_SSH):
    def connect(self):
        try:
            huawei = {
                    'device_type': 'huawei',
                    'host': self.hostname,
                    'username': self.username,
                    'password': self.password
                    }
            self.connection = ConnectHandler(**huawei)
        except Exception as e:
            print(e)
            self.connection = -1
            

    def show_int(self, interface):
        print(self.connection)
        output = self.connection.send_command('display interface gigabitethernet ' + interface)
        return output
    
    def show_multiples(self, interface):
        output = self.connection.send_config_set([
            'display interface gigabitethernet ' + interface,
            'display cpu-usage'
            ])
        return output

class Roteador_telnet:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    def start_connection(self, equipamento):
        try:
            equipamento = {
                    'device_type': equipamento,
                    'host': self.hostname,
                    'username': self.username,
                    'password': self.password
                    }
            self.connection = ConnectHandler(**equipamento)
        except Exception as e:
            print(e)
            self.connection = -1            

    def show_int(self):
        pass

    def show_multiple(self):
        pass

class Cisco_telnet(Roteador_telnet):
    def connect(self):
        self.start_connection('cisco_ios_telnet')

    def show_int(self, interface):
        output = self.connection.send_command('show interface gigabitethernet ' + interface)
        return output

    def show_multiples(self, interface):
        output = self.connection.send_config_set([
            'do show interface gigabitethernet ' + interface,
            'do show users all',
            'do show ssh'
            ])
        return output

class Juniper_telnet(Roteador_telnet):
    def connect(self):
        self.start_connection('juniper_junos_telnet')

    def show_int(self, interface):
        output = self.connection.send_command('show interface ' + interface)
        return output

    def show_multiples(self, interface):
        output = self.connection.send_config_set([
            'exit',
            'show interface ' + interface,
            'show system users',
            'config'
            ])
        return output

class Nokia_telnet(Roteador_telnet):
    def connect(self):
        self.start_connection('nokia_sros_telnet')

    def show_int(self, interface):
        output = self.connection.send_command('show port ' + interface)
        return output

    def show_multiples(self, interface):
        output = self.connection.send_config_set([
            'show port ' + interface,
            'show users'
            ])
        return output

class Huawei_telnet(Roteador_telnet):
    def connect(self):
        self.start_connection('huawei_telnet')

    def show_int(self, interface):
        output = self.connection.send_command('display interface gigabitethernet ' + interface)
        return output

    def show_multiples(self, interface):
        output = self.connection.send_config_set([
            'display interface gigabitethernet ' + interface,
            'display users'
            ])
        return output

#Mikrotik telnet don't work well with netmiko
class Mikrotik_telnet(Roteador_telnet):
    def connect(self):
        equipamento = {
                'device_type': 'generic_telnet',
                'host': self.hostname,
                }

        self.connection = ConnectHandler(**equipamento)
        
        self.connection.send_command_timing('\n') #Technical adjustment
        self.connection.send_command_timing('\n') #Technical adjustment
        self.connection.send_command_timing(self.username + '\n') #Username
        self.connection.send_command_timing(self.password + '\n') #Password
        self.connection.send_command_timing('\n') #Technical adjustment

    def show_int(self, interface):

        output = self.connection.send_command_timing('/interface ethernet print detail where name=' + interface)
        return output

    def show_multiples(self, interface):
        try:
            output = self.connection.send_config_set([
                '/interface ethernet print detail where name=' + interface,
                '/users print'
                ])
            return output
        except Exception as e:
            return e

