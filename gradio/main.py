import gradio as gr
import interface
import rotas
import ospf


def show_pageint():
    return interface.create_interface()

def show_pagerota():
    return rotas.create_routes()

def show_pageospf():
    return ospf.create_ospf()

with gr.Blocks() as main:
    with gr.Tabs():
        with gr.Tab("Interface"):
            show_pageint()
        with gr.Tab("Rota"):
            show_pagerota()
        with gr.Tab("OSPF"):
            show_pageospf()


main.launch()
