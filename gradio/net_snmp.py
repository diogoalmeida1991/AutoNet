from pysnmp.hlapi import *
import socket

class Roteador_SNMP:
    def __init__(self, host, community):
        self.host = host
        self.community = community

    def snmp_get(self,oid):
        #next and getCmd are library pysnmp functions
        #snmp_binds receive a tupla with error_indicator, error_status, error_index and var_binds
        snmp_binds = next(getCmd(
            SnmpEngine(),
            CommunityData(self.community),
            UdpTransportTarget((self.host, 161)), #Port can to insert here 161
            ContextData(),
            ObjectType(ObjectIdentity(oid))
            ))

        #Return a lot of resources, in this case, return only the binds
        return snmp_binds[3][0][1]

    def snmp_walk(self,oid):
        response = []
        for (_, _, _, var_binds) in nextCmd(
                SnmpEngine(),
                CommunityData(self.community),
                UdpTransportTarget((self.host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
                lexicographicMode=False
                ):
            
            response.append(var_binds[0])
        return response

    def snmp_walk_response(self, oid):
        walk = self.snmp_walk(oid)
        response = []
        for bind in walk:
            response.append(bind[1])
        return response

    def snmp_walk_oid(self, oid):
        walk = self.snmp_walk(oid)
        response = []
        for bind in walk:
            response.append(bind[0])
        return response

    def show_eqpto(self):
        return self.snmp_get('1.3.6.1.2.1.1.1.0')
    
    #Test without walk, this method is slow and use a lot of resources.
    def show_int1(self):
        interfaces = self.snmp_get('1.3.6.1.2.1.2.1.0')
        i = 1
        j = 1
        name_array = []
        status1_array = []
        status2_array = []
        while i<=interfaces:
            name = self.snmp_get('1.3.6.1.2.1.2.2.1.2.' + str(j))
            status1 = self.snmp_get('1.3.6.1.2.1.2.2.1.7.' + str(j)) #1 - up 2 - down
            status2 = self.snmp_get('1.3.6.1.2.1.2.2.1.8.' + str(j)) #1 - up 2 - down
            if len(name) != 0:
                i += 1
                name_array.append(str(name))
                status1_array.append(int(status1))
                status2_array.append(int(status2))
            j += 1
        return(name_array, status1_array, status2_array)

    def show_int(self):
        name = self.snmp_walk_response('1.3.6.1.2.1.2.2.1.2')
        status1 = self.snmp_walk_response('1.3.6.1.2.1.2.2.1.7')
        status2 = self.snmp_walk_response('1.3.6.1.2.1.2.2.1.8')
        description = self.snmp_walk_response('1.3.6.1.2.1.31.1.1.1.18')
        number = self.snmp_walk_oid('1.3.6.1.2.1.2.2.1.2')
        number = [n[-1] for n in self.list_str(number)]
        description = self.list_str(description)
        name = self.list_str(name)
        status1 = self.list_int(status1)
        status2 = self.list_int(status2)
        return(name, description, number, status1, status2)

    def list_int(self, lista):
        new_list = []
        for item in lista:
            new_list.append(int(item))
        return new_list

    def list_str(self, lista):
        new_list = []
        for item in lista:
            new_list.append(str(item))
        return new_list

    def list_bytes(self, lista):
        new_list = []
        for item in lista:
            new_list.append(socket.inet_ntoa(bytes(item)))
        return new_list

    def show_route(self):
        destination = self.snmp_walk_response('1.3.6.1.2.1.4.21.1.1')
        destination = self.list_bytes(destination)
        network = self.snmp_walk_response('1.3.6.1.2.1.4.21.1.11')
        network = self.list_bytes(network)
        interface = self.snmp_walk_response('1.3.6.1.2.1.4.21.1.2')
        interface = self.list_int(interface)
        origin = self.snmp_walk_response('1.3.6.1.2.1.4.21.1.7')
        origin = self.list_bytes(origin)
        type_route = self.snmp_walk_response('1.3.6.1.2.1.4.21.1.8')#3 - direct 4 - indirect
        type_route = self.list_int(type_route)
        protocol = self.snmp_walk_response('1.3.6.1.2.1.4.21.1.9')#2 - local 13 - OSPF 14 - BGP 9 - ISIS
        protocol = self.list_int(protocol)
        return (destination, network, interface, origin, type_route, protocol)

    def show_ospf(self):
        router_id = socket.inet_ntoa(bytes(self.snmp_get('1.3.6.1.2.1.14.1.1.0')))
        enabled = int(self.snmp_get('1.3.6.1.2.1.14.1.2.0'))
        areas = self.snmp_walk_response('1.3.6.1.2.1.14.2.1.1')
        areas = self.list_bytes(areas)
        area_status = self.snmp_walk_response('1.3.6.1.2.1.14.2.1.10')
        area_status = self.list_int(area_status)
        neighbor_ip = self.snmp_walk_response('1.3.6.1.2.1.14.10.1.1')
        neighbor_ip = self.list_bytes(neighbor_ip)
        neighbor_id = self.snmp_walk_response('1.3.6.1.2.1.14.10.1.3')
        neighbor_id = self.list_bytes(neighbor_id)
        ospf_status = self.snmp_walk_response('1.3.6.1.2.1.14.10.1.6')
        ospf_status = self.list_int(ospf_status)
        return (router_id, enabled, areas, area_status, neighbor_ip, neighbor_id, ospf_status)



host = '192.168.10.10'
community = 'public'

Roteador = Roteador_SNMP(host, community)
print(Roteador.show_eqpto())
print(Roteador.show_int())

print(Roteador.show_route())
print(Roteador.show_ospf())
