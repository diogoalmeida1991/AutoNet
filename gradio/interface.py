import gradio as gr
import pandas as pd
from net_snmp import Roteador_SNMP
from open_ips import archive


#In gradio is better use dataframe
def createdf_interface(ip):
    roteador = Roteador_SNMP(ip, 'public')
    response = roteador.show_int()
    interface = {
            'Interface': response[0],
            'Description': response[1],
            'Status1': response[3],
            'Status2': response[4]
            }

    df = pd.DataFrame(interface)
    return df

def create_interface():
    ip = archive()
    initial_df = createdf_interface(ip[0])

    with gr.Blocks() as page: #After second element, this line must to be included.
        ip_dropdown = gr.Dropdown(choices=ip, label="Escolha o IP")

        dataframe_output = gr.DataFrame(value=initial_df)#Show after select the IP

        ip_dropdown.change(fn=createdf_interface , inputs=ip_dropdown, outputs=dataframe_output)

    return page

if __name__ == "__main__":
    create_interface().launch()
