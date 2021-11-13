from flask import Flask, request
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
from json import load, dump
import asyncio
import time
import yagmail
app = Flask(__name__)

list = []
def serializer(value):
    return json.dumps(value).encode()

def mail(vend, coci):
    for i in range(0,(len(vend))):
        #initializing the server connection
        yag = yagmail.SMTP(user='Tareasdpythonkafka', password='Tareasdpythonkafka123')
        #sending the email
        yag.send(to=vend[i], subject='Sending Attachment', contents='Please find the image attached', attachments='resume.txt')
        print("Email sent successfully")
    for i in range(0,(len(coci))):
        #initializing the server connection
        yag = yagmail.SMTP(user='Tareasdpythonkafka', password='Tareasdpythonkafka123')
        #sending the email
        yag.send(to=coci[i], subject='Sending Attachment', contents='Please find the image attached', attachments='resume.txt')
        print("Email sent successfully")

@app.route('/')
def main():
    return "Hello World!"

@app.route('/producer', methods = ['POST'])
async def produce():
    if request.method == 'POST':
        n_sopaipa = request.form['n_sopaipa']
        mail_vendedor = request.form['mail_vendedor']
        mail_cocinero = request.form['mail_cocinero']
        producer = AIOKafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=serializer)
        resp = {"Order":[{"numero_sopaipillas":n_sopaipa, "mail_vendedor":mail_vendedor, "mail_cocinero":mail_cocinero}]}
        await producer.start()
        try:
            await producer.send_and_wait("Orders", resp)
        finally:
            await producer.stop()
        return resp

@app.route('/consumer', methods = ['GET'])
async def consume():
    if request.method == 'GET':
        global list
        consumer = AIOKafkaConsumer(
            'Orders',
            # consumer_timeout_ms = 1000,
            auto_offset_reset="earliest",
            bootstrap_servers=['localhost:9092'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        await consumer.start()
        try:
            async for msg in consumer:
                print("consumed: ", msg.topic, msg.partition, msg.offset,
                         msg.key, msg.value, msg.timestamp)
                list.append(msg.value)
        finally:
            await consumer.stop()
            # producer = AIOKafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=serializer)
            # await producer.start()
            # try:
            #     for i in range(0,len(list)):
            #         await producer.send_and_wait("Resume", list[i])
            # finally:
            #     await producer.stop()


@app.route('/resume', methods = ['GET'])
async def resume():
    if request.method == 'GET':
        global list

        n_ordenes = len(list)
        lista = ','.join(map(str, list))
        lista = str(lista).replace("'" ,'"')
        # print(lista)
        aux2 = lista[12:len(lista)-3]
        aux2 = aux2.replace('[','')
        aux2 = aux2.replace(']','')
        aux2 = aux2.replace('}}','}')
        aux2 = aux2.replace('{"Order":','')
        final = lista[0:12] + aux2 + '}]}'
        aux = json.loads(final)
        # print(final)
        # json_list = json.dumps(lista)
        with open('data.json','w', encoding='utf-8') as f:
            json.dump(aux, f, sort_keys = True, indent = 4,
               ensure_ascii = False)
        f.close()
        f = open('data.json',)
        json_file = json.load(f)
        print(json_file)
        vendedores = []
        cocineros = []
        sopaipasvend = []

        # for item in json_file['Order']:
        #     if len(vendedores) == 0:
        #         vendedores.append(item['mail_vendedor'])
        #         cocineros.append(item['mail_cocinero'])
        #         sopaipasvend.append(int(item['numero_sopaipillas']))
        #     for i in range(0,len(vendedores)):
        #         if item['mail_vendedor'] == vendedores[i]:
        #             # print("sopaipas[i] : ",sopaipasvend[i])
        #             # print("item['numero_sopaipillas'] : ",item['numero_sopaipillas'])
        #             sopaipasvend[i] = int(sopaipasvend[i]) + int(item['numero_sopaipillas'])
        #             break
        #         else:
        #             vendedores.append(item['mail_vendedor'])
        #             cocineros.append(item['mail_cocinero'])
        #             sopaipasvend.append(int(item['numero_sopaipillas']))
        for item in json_file['Order']:
            if len(vendedores) == 0:
                vendedores.append(item['mail_vendedor'])
                cocineros.append(item['mail_cocinero'])
                sopaipasvend.append(int(item['numero_sopaipillas']))
            for i in range(0,len(vendedores)):
                if item['mail_vendedor'] == vendedores[i]:
                    sopaipasvend[i] = sopaipasvend[i] + int(item['numero_sopaipillas'])
                    break
                else:
                    vendedores.append(item['mail_vendedor'])
                    cocineros.append(item['mail_cocinero'])
                    sopaipasvend.append(int(item['numero_sopaipillas']))

      
                
        respuesta = []
        producer = AIOKafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=serializer)
        await producer.start()

        for i in range(0,len(vendedores)):
            resp = {"numero_sopaipillas":sopaipasvend[i], "mail_vendedor":vendedores[i], "mail_cocinero":cocineros[i]}
            respuesta.append(resp)
        try:
            for i in range(0,len(respuesta)):
                await producer.send_and_wait("Resume", respuesta[i])
        finally:
            await producer.stop()



            
        # print("ordenes: ", n_ordenes, "sopaipas: ", sopaipas)
        final = ','.join(map(str, respuesta))
        with open('resume.txt','w') as f:
            f.write(final)
        mail(vendedores, cocineros)
        return ''.join(map(str, respuesta))




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)