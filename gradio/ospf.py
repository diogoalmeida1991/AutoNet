import gradio as gr
import pandas as pd
from net_snmp import Roteador_SNMP
from open_ips import archive

def ospf(ip):
    roteador = Roteador_SNMP(ip, "public")
    response = roteador.show_ospf()

    router_id = response[0]

    area = {
            "area": response[2],
            "status": response[3] 
            }

    neighbor = {
            'Neighbor Id': response[5],
            'Neighbor Ip': response[4],
            'Adjacencia': response[6]
            }

    df_area = pd.DataFrame(area)
    df_neighbor = pd.DataFrame(neighbor)

    return router_id, df_area, df_neighbor


def create_ospf():
    ip = archive()
    with gr.Blocks() as page:
        ip_dropdown = gr.Dropdown(choices=ip, label='Escolha o IP')

        router_id = gr.Textbox(interactive=False, value=ospf(ip[0])[0], label='Router ID')

        area_df = gr.DataFrame(value=ospf(ip[0])[1])

        neighbor_df = gr.DataFrame(value=ospf(ip[0])[2])

        ip_dropdown.change(fn=ospf, inputs=ip_dropdown, outputs=[router_id, area_df, neighbor_df])

    return page

if __name__ == "__main__":
    create_ospf().launch()

