from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c

from telegram import Bot #Use the version 13.1 to avoid asynchronous function

#Here use the token. (Search for Botfather)
def gera_bot(arquivo):
    with open(arquivo, "r") as arquivo:
        linhas = arquivo.readlines()
        bot = Bot(token=linhas[0].strip())
    return bot

#Here use the chat ID that the bot will to send a message
chat_id = "-4601814328"

#function to send a Telegram message
def enviar_mensagem(telegram_bot, chat, msg):
    telegram_bot.send_message(chat_id=chat, text=msg)

#Creating engine to receive the alarms
snmp_engine = engine.SnmpEngine()

#Configuring the receptor in port UDP 162
config.addTransport(
        snmp_engine,
        udp.domainName,
        udp.UdpTransport().openServerMode(('0.0.0.0', 162))#Change 0.0.0.0 for your IP
        )

#Security configuration
config.addV1System(snmp_engine, 'area', 'public')

#Function to proccess traps
def trap_analizer(snmp_engine, state, context_engine, context_name, var_binds, cb_ctx):
    bot = gera_bot("token.txt")
    chat_id = "-4601814328"
    #Collect source IP
    source_ip = snmp_engine.observer.getExecutionContext('rfc3412.receiveMessage:request')
    mensagens = []

    for oid, val in var_binds:
        mensagem = source_ip['transportAddress'][0] + ' : ' + oid.prettyPrint() + ' = ' + val.prettyPrint()
        print(mensagem)
        if oid.prettyPrint().startswith("1.3.6.1.2.1.2.2.1.2"):
            mensagem = f"{source_ip['transportAddress'][0]} - Interface: {val.prettyPrint()}"
            enviar_mensagem(bot, chat_id, mensagem)
        if oid.prettyPrint().startswith("1.3.6.1.4.1.9.9.41.1.2.3.1.5"):
            mensagem = f"{source_ip['transportAddress'][0]} - {val.prettyPrint()}"
            enviar_mensagem(bot, chat_id, mensagem)
        if oid.prettyPrint().startswith("1.3.6.1.4.1.9.2.2.1.1.20"):
            mensagem = f"{source_ip['transportAddress'][0]} - {val.prettyPrint()}"
            enviar_mensagem(bot, chat_id, mensagem)


#Create a callback to receive notifications
ntfrcv.NotificationReceiver(snmp_engine, trap_analizer)


#Start main loop
print("Aguardando traps SNMP")
snmp_engine.transportDispatcher.jobStarted(1)#Activate the Dispatcher
try:
    snmp_engine.transportDispatcher.runDispatcher()
except KeyboardInterrupt:
    print("Encerrado pelo usario")
    snmp_engine.transportDispatcher.closeDispatcher()

