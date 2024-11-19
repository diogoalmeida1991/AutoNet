import gradio as gr
import pandas as pd
from net_snmp import Roteador_SNMP
from open_ips import archive

def routes(ip):
    roteador=Roteador_SNMP(ip, 'public')
    response_route=roteador.show_route()
    response_int=roteador.show_int()
    interface = []
    prot_list = ['other','local/estatica','netmgmt','icmp','egp','ggp',
                 'hello','rip','is-is','es-is','ciscoIgrp',
                 'bbnSpfIgo','ospf','bgp']
    protocols = []


    for i in response_route[2]:
        if i == 0:
            interface.append("Remoto")
        else:
            interface.append(response_int[0][i-2])
    for i in response_route[5]:
        protocols.append(prot_list[i-1])

    route = {
            'Destino': response_route[0],
            'Sub-rede': response_route[1],
            'Interface': interface,
            'Protocolo': protocols,
            'Saida': response_route[3]
            }
    
    df = pd.DataFrame(route)
    return df

def create_routes():
    ip = archive()
    df_start = routes(ip[0])

    with gr.Blocks() as page:
        ip_dropdown = gr.Dropdown(choices=ip, label="Escolha um IP")

        dataframe_output = gr.DataFrame(df_start)

        ip_dropdown.change(fn=routes, inputs=ip_dropdown, outputs=dataframe_output)

    return page


if __name__ == "__main__":
    create_routes().launch()
