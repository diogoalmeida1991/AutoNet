import asyncio, telnetlib3


class Router:
    def __init__(self, hostname, user, password):
        self.hostname = hostname
        self.user = user
        self.password = password
        self.telnet = None
        self.stop = None

    async def start_connection(self):
        #self.telnet[0] = reader
        #self.telnet[1] = writer
        self.telnet = await telnetlib3.open_connection(self.hostname)

    async def authenticate(self, str_user, str_pass, stop):
        await self.telnet[0].readuntil(str_user.encode('utf-8'))
        self.telnet[1].write(self.user + "\n")
        await self.telnet[1].drain()

        await self.telnet[0].readuntil(str_pass.encode('utf-8'))
        self.telnet[1].write(self.password + "\n")
        await self.telnet[1].drain()
        
        self.stop = stop
        await self.telnet[0].readuntil(self.stop.encode('utf-8')) #Necessary to print a second command


    #Mikrotik use this authentication form, it stop in MikroTik string and after in "] >" string
    async def authenticate_mode2(self, str_user, str_pass, stop, stop2):
        await self.telnet[0].readuntil(str_user.encode('utf-8'))
        self.telnet[1].write(self.user + "\n")
        await self.telnet[1].drain()

        await self.telnet[0].readuntil(str_pass.encode('utf-8'))
        self.telnet[1].write(self.password + "\n")
        await self.telnet[1].drain()
        
        await self.telnet[0].readuntil(stop.encode('utf-8'))
        self.stop = stop2
        await self.telnet[1].drain()

        await self.telnet[0].readuntil(self.stop.encode('utf-8'))


    async def send_command(self, command):
        self.telnet[1].write(command + "\n")
        await self.telnet[1].drain()
        output = await self.telnet[0].readuntil(self.stop.encode('utf-8'))
        return output.decode('utf-8')

    #Mikrotik print two times the prompt after send the command
    async def send_command_mode2(self, command):
        self.telnet[1].write(command + "\n")
        await self.telnet[1].drain()
        await self.telnet[0].readuntil(self.stop.encode('utf-8'))

        output = await self.telnet[0].readuntil(self.stop.encode('utf-8'))

        return output.decode('utf-8')

    #Using the writer to disconnect
    async def disconnect(self):
        self.telnet[1].close()

    def connect():
        pass

    def show_int():
        pass

    def show_run():
        pass


class Cisco(Router):
    async def connect(self):
        await self.start_connection()
        await self.authenticate("Username: ", "Password: ", '#')
        print("Authenticado")

    async def remove_term_lenght(self):
        output = await self.send_command('terminal length 0')
        return output
    
    async def show_int(self, interface):
        output = await self.send_command('show interface gigabitethernet ' + interface)
        return output

    async def show_run(self):
        output = await self.send_command('show running-config')
        return output

class Juniper(Router):
    async def connect(self):
        await self.start_connection()
        await self.authenticate("login: ", "Password:", ">")
        print("Authenticado")

    async def remove_term_lenght(self):
        output = await self.send_command('set cli screen-length 0')
        return output

    async def show_int(self, interface):
        output = await self.send_command('show interfaces ' + interface)
        return output

    async def show_run(self):
        output = await self.send_command('show configuration')
        return output

class Nokia(Router):
    async def connect(self):
        await self.start_connection()
        await self.authenticate("Login: ", "Password: ", "A:")
        print("Authenticado")

    async def remove_term_lenght(self):
        output = await self.send_command('environment no more')
        return output

    async def show_int(self, interface):
        output = await self.send_command('show port ' + interface)
        return output

    async def show_run(self):
        output = await self.send_command('admin display-config')
        return output

class Huawei(Router):
    async def connect(self):
        await self.start_connection()
        await self.authenticate("Username:", "Password:", ">" )
        print("Authenticado")

    async def remove_term_lenght(self):
        output = await self.send_command('screen-length 0 temporary')
        return output

    async def show_int(self, interface):
        output = await self.send_command('display interface gigabitethernet ' + interface)
        return output

    async def show_run(self):
        output = await self.send_command('display current-configuration')
        return output

class Mikrotik(Router):
    async def connect(self):
        await self.start_connection()
        await self.authenticate_mode2("Login: ", "Password: ", "MikroTik", "] >")
        await self.telnet[0].readuntil(self.stop.encode('utf-8')) #Necessary to print a second command

    async def remove_term_lenght(self):
        return "Mikrotik nao tem paginacao"        

    async def show_int(self, interface):
        output = await self.send_command_mode2('interface ethernet print detail where name=' + interface + '\r')
        await self.telnet[0].readuntil(self.stop.encode('utf-8')) #Necessary to print a second command
        return output

    async def show_run(self):
        output = await self.send_command_mode2('/export \r')
        await self.telnet[0].readuntil(self.stop.encode('utf-8')) #Necessary to print a second command
        return output

async def main():
    routers = []
    routers.append(Cisco('192.168.10.2', 'admin', 'admin'))
    routers.append(Juniper('192.168.10.1', 'admin', 'Admin1234'))
    routers.append(Nokia('192.168.10.3', 'admin', 'admin'))
    routers.append(Huawei('192.168.10.4', 'Admin123', 'Admin1234'))
    routers.append(Mikrotik('192.168.10.5', 'admin', 'admin'))
    interface = ['1/0', 'ge-0/0/0', '1/1/1', '0/0/0', 'ether1']
    i = 0

    for router in routers:
        await router.connect()
        await router.remove_term_lenght()
        print(await router.show_int(interface[i]))
        print(await router.show_run())
        await router.disconnect()
        i += 1

asyncio.run(main())

