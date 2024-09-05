# Segunda Tarea Sistemas Distribuidos

# Prerequisitos

## Instalar Apache Kafka
Descargarlo desde la página oficial
```
https://kafka.apache.org/
```
Descargar la versión:"kafka-2.6.0-src.tgz"

## Es necesario instalar unas librerías, tales como

```
Flask
```
pip install flask
```
Flask[async]
```
pip install flask[async]
```
aiokafka
```
yagmail
```
pip install yagmail
```

# Para usarlo

## Correr Zoopeeker
```
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```
## Correr Servidor
```
.\bin\windows\kafka-server-start.bat .\config\server.properties
```
## Correr Programa
```
python app2.py
```
## Para agregar ordenes

En postman, hay que escribir la dirección
```
http://192.168.8.100:5000/producer
```
Y elegir la opción POST

En la sección Body, Form-data, llenar con las llaves
```
n_sopaipa
mail_vendedor
mail_cocinero
```

# Para ver las ordenes realizadas
En postman, hay que escribir la dirección
```
http://192.168.8.100:5000/consumer
```
Y elegir la opción GET. Este método no retorna nada, pero sube las órdenes procesadas al topic Resume. Después es necesario ingresar la dirección:
```
http://192.168.8.100:5000/resume
```
La cual se encarga de obtener los datos del topic Resume y los envía a los correos indicados.
