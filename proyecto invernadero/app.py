from flask import Flask, render_template, flash, request, redirect, jsonify, url_for, flash,session, escape
from flask_mysqldb import MySQL,MySQLdb
import time
import serial
import board
import adafruit_dht
import RPi.GPIO as GPIO
import smtplib
from email.mime.text import MIMEText

#---------------envio de correos Humedad Alta----------------
'''def correo_humedadM():
    correo_origen = "invernaderoiamia@gmail.com"
    contraseña = "Invernaderoiamia."
    correo_destino = "eldono490@gmail.com"
    msg = MIMEText("Humedad Maxíma superada, Encendiendo Ventilación para regularla")
    msg['Subject'] = 'Humedad Alta'
    msg['From'] = correo_origen
    msg['To'] = correo_destino
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(correo_origen,contraseña)
    server.sendmail(correo_origen,correo_destino,msg.as_string())
    print("correo enviado")
    time.sleep(1.0)
    server.quit()

#-----------------envio de correos Humedad Baja-------------------------
def correo_humedadmin():
    correo_origen = "invernaderoiamia@gmail.com"
    contraseña = "Invernaderoiamia."
    correo_destino = "eldono490@gmail.com"
    msg = MIMEText("Humedad baja, estabilizando")
    msg['Subject'] = 'Humedad Baja'
    msg['From'] = correo_origen
    msg['To'] = correo_destino
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(correo_origen,contraseña)
    server.sendmail(correo_origen,correo_destino,msg.as_string())
    print("correo enviado")
    time.sleep(1.0)
    server.quit()
#envio de correo por temperatura
def correo_temperaturaM():
    correo_origen = "invernaderoiamia@gmail.com"
    contraseña = "Invernaderoiamia."
    correo_destino = "eldono490@gmail.com"
    msg = MIMEText("Temperatura Maxíma superada, Encendiendo Ventilación para su regulación")
    msg['Subject'] = 'Temperatura Alta'
    msg['From'] = correo_origen
    msg['To'] = correo_destino
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(correo_origen,contraseña)
    server.sendmail(correo_origen,correo_destino,msg.as_string())
    print("correo enviado")
    time.sleep(1.0)
    server.quit()
    
#----------------envio de correo por temperatura baja------------------
def correo_temperaturamin():
    correo_origen = "invernaderoiamia@gmail.com"
    contraseña = "Invernaderoiamia."
    correo_destino = "eldono490@gmail.com"
    msg = MIMEText("Temperatura Baja, Encendiendo luz para su regulación")
    msg['Subject'] = 'Temperatura baja'
    msg['From'] = correo_origen
    msg['To'] = correo_destino
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(correo_origen,contraseña)
    server.sendmail(correo_origen,correo_destino,msg.as_string())
    print("correo enviado")
    time.sleep(1.0)
    server.quit() '''
    
GPIO.setmode(GPIO.BCM)
ventilador_temp = 17
ventilador_humedad = 27
luz = 22
bomba = 5
entrada_compuerta = 25 
# definimos el pin para el sensor DHT22
dhtDevice1 = adafruit_dht.DHT22(board.D4)
# definimos el pin para el sensor DHT11
dhtDevice2 = adafruit_dht.DHT11(board.D11)
#pines compuerta
# para quitar los warnigs GPIO.setwarnings(False)
GPIO.setup(ventilador_temp, GPIO.OUT)
GPIO.setup(ventilador_humedad, GPIO.OUT)
GPIO.setup(bomba, GPIO.OUT)
GPIO.setup(luz, GPIO.OUT)
GPIO.setup(entrada_compuerta, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(13,GPIO.OUT)
#iniciamos todos los pines en apagado

GPIO.output(ventilador_temp, GPIO.HIGH)
GPIO.output(ventilador_humedad, GPIO.HIGH)
GPIO.output(luz, GPIO.HIGH)
GPIO.output(bomba, GPIO.HIGH)

#iniciamos aplicacion web con flask 
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'plantas'
mysql = MySQL(app)



        
@app.route('/')
def Index():
    return render_template('index.html')
#-----------------------inicia login / registro----------------------------------

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/action_login', methods=['POST', 'GET'])
def action_login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password'].encode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo =%s AND password = %s',(correo,password))
        usuarios = cur.fetchone()
        if usuarios is None:
            return render_template('login.html')
        else:
            return render_template('modo.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/action_registro', methods=['POST', 'GET'])
def action_registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        correo = request.form['correo']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (usuario, correo, password) VALUES (%s,%s,%s)',
        (usuario, correo, password))
        mysql.connection.commit()
        registro_correcto = cur.fetchone()
        return render_template('modo.html')
        
#-----------------------termina login / registro----------------------------------    
        
@app.route('/modo')
def modo():
    return render_template('modo.html')
    

#-----------------------inicia modo manual----------------------------------

@app.route('/manual')
def manual():
    return render_template('manual.html')

@app.route('/vent1on')
def vent1on():
    GPIO.output(ventilador_temp, GPIO.LOW)
    return render_template('manual.html')

@app.route('/ventoff')
def vent1off():
    GPIO.output(ventilador_temp, GPIO.HIGH)
    return render_template('manual.html')

@app.route('/vent2on')
def vent2on():
    GPIO.output(ventilador_humedad, GPIO.LOW)
    return render_template('manual.html')

@app.route('/vent2off')
def vent2off():
    GPIO.output(ventilador_humedad, GPIO.HIGH)
    return render_template('manual.html')

@app.route('/bombaon')
def bombaon():
    GPIO.output(bomba, GPIO.LOW)
    return render_template('manual.html')

@app.route('/bombaoff')
def bombaoff():
    GPIO.output(bomba, GPIO.HIGH)
    return render_template('manual.html')

@app.route('/luzon')
def luzon():
    GPIO.output(luz, GPIO.LOW)
    return render_template('manual.html')

@app.route('/luzoff')
def luzoff():
    GPIO.output(luz, GPIO.HIGH)
    return render_template('manual.html')

@app.route('/allof')
def alloff():
    GPIO.output(ventilador_temp, GPIO.HIGH)
    GPIO.output(ventilador_humedad, GPIO.HIGH)
    GPIO.output(luz, GPIO.HIGH)
    GPIO.output(bomba, GPIO.HIGH)
    return render_template('manual.html')

@app.route('/info')
def info():
    return render_template('info.html')

#-----------------------termina modo manual----------------------------------

#-----------------------inicia modo automatico---------------------------------- 
def sensor1():
    while True:
        try:
            temperature = dhtDevice1.temperature
            return  temperature
        except:
            print("")
        time.sleep(2.0)
        
def sensor2():
    while True:
        try:
            humidity = dhtDevice2.humidity
            return  humidity
        except:
            print("")
        time.sleep(2.0)
        
@app.route('/automatico')
def automatico():
    GPIO.output(ventilador_temp, GPIO.HIGH)
    GPIO.output(ventilador_humedad, GPIO.HIGH)
    GPIO.output(bomba, GPIO.HIGH)
    GPIO.output(luz, GPIO.HIGH)
    return render_template('home.html')

#-----------------------inicia seleccion de plantas----------------------------------

#-----------------------sección decorativas----------------------------------
@app.route('/decorativas', methods=['POST','GET'])
def decorativas():
    return render_template('Decorativas.html')

#-----------------------termina sección decorativas----------------------------------

@app.route('/medicinales')
def medicinales():
    return render_template('Medicinales.html')

#-----------------------sección frutales / vegetales ----------------------------------

@app.route('/frutalesyvegetales')
def frutalesyvegetales():
    return render_template('FrutalesyVegetales.html')

@app.route('/seleccionvf', methods=['POST','GET'])
def seleccionvf():
    if request.method == 'POST':
        dato = request.form['datof']
        cur = mysql.connection.cursor()
        datos = cur.execute ("SELECT * FROM VF WHERE id = %s",(dato,))
        while datos > 0:
              detalles = cur.fetchall()
              for id in detalles:
                  print("ID:",id[0])
                  print("Tipo:",id[1])
                  print("nombre:",id[2])
                  print("Temperatura Maxima:",id[3])
                  print("Temperatura Minima:",id[4])
                  print("Humedad Maxima:",id[5])
                  print("Humedad Minima:",id[6])
                  print("Humedad Tierra:",id[7])
                  tempMax = id[3]
                  tempMin = id[4]
                  humMax = id[5]
                  humMin = id[6]
                  humt = id[7]
                  while True:
                      sensor1() #esta linea llama a la funcion del sensor DHT22
                      temperature = sensor1()# sacamos los datos de la lectura del sensor DT22
                      print("temperatura dht22",temperature)
                      sensor2() #esta linea llama a la funcion del sensor DHT11
                      humidity = sensor2()# sacamos los datos de la lectura del sensor DT11
                      print("humedad dht22",humidity,"%")
                      #condiciones de cuidado de plantas
                      time.sleep(2.0)
                      #condicion de temperatura maxima y minina
                      if temperature >= tempMax:
                          GPIO.output(ventilador_temp, GPIO.LOW)
                          #correo_temperaturaM()
                      else:
                          GPIO.output(ventilador_temp, GPIO.HIGH)
                          
                      if temperature <= tempMin:
                          GPIO.output(luz, GPIO.LOW)
                          #correo_temperaturamin()
                      else:
                          GPIO.output(luz, GPIO.HIGH)
                     #condicion de humedad Maxima y Minima
                      if humidity >= humMax:
                          GPIO.output(ventilador_humedad, GPIO.LOW)
                          #correo_humedadM()
                      else:
                          GPIO.output(ventilador_humedad, GPIO.HIGH)
                      #incluir riego minimo
                      if humidity <= humMin:
                          print("humedad baja")
                      else:
                          GPIO.output(ventilador_temp, GPIO.HIGH)
                    #termina condiciones de cuidado de plantas
    return render_template('FrutalesyVegetales.html')
#-----------------------termina sección Frutales y Vegetales ----------------------------------
#-----------------------inicia seccion de Decorativas ----------------------------------
@app.route('/selecciondec', methods=['POST','GET'])
def selecciondec():
    if request.method == 'POST':
        dato = request.form['datod']
        print(dato)
        cur = mysql.connection.cursor()
        datos = cur.execute ("SELECT * FROM decorativa WHERE id = %s",(dato,))
        while datos > 0:
              detalles = cur.fetchall()
              for id in detalles:
                  print("ID:",id[0])
                  print("Tipo:",id[1])
                  print("nombre:",id[2])
                  print("Temperatura Maxima:",id[3])
                  print("Temperatura Minima:",id[4])
                  print("Humedad Maxima:",id[5])
                  print("Humedad Minima:",id[6])
                  print("Humedad Tierra:",id[7])
                  tempMax = id[3]
                  tempMin = id[4]
                  humMax = id[5]
                  humMin = id[6]
                  humt = id[7]
                  while True:
                      sensor1() #esta linea llama a la funcion del sensor DHT22
                      temperature = sensor1()# sacamos los datos de la lectura del sensor DT22
                      print("temperatura dht22",temperature)
                      sensor2() #esta linea llama a la funcion del sensor DHT11
                      humidity = sensor2()# sacamos los datos de la lectura del sensor DT11
                      print("humedad dht22",humidity,"%")
                      #condiciones de cuidado de plantas
                      time.sleep(2.0)
                      #condicion de temperatura maxima y minina
                      if temperature >= tempMax:
                          GPIO.output(ventilador_temp, GPIO.LOW)
                          #correo_temperaturaM()
                      else:
                          GPIO.output(ventilador_temp, GPIO.HIGH)
                          
                      if temperature <= tempMin:
                          GPIO.output(luz, GPIO.LOW)
                          #correo_temperaturamin()
                      else:
                          GPIO.output(luz, GPIO.HIGH)
                     #condicion de humedad Maxima y Minima
                      if humidity >= humMax:
                          GPIO.output(ventilador_humedad, GPIO.LOW)
                          #correo_humedadM()
                      else:
                          GPIO.output(ventilador_humedad, GPIO.HIGH)
                      #incluir riego minimo
                      if humidity <= humMin:
                          print("humedad baja")
                      else:
                          GPIO.output(ventilador_temp, GPIO.HIGH)
    return render_template('Decorativas.html')

#-----------------------termina sección Decorativas ----------------------------------
        
#-----------------------inicia sección medicinales ----------------------------------
@app.route('/seleccionmed', methods=['POST','GET'])
def seleccionmed():
    if request.method == 'POST':
        dato = request.form['datom']
        print(dato)
        cur = mysql.connection.cursor()
        datos = cur.execute ("SELECT * FROM medicinal WHERE id = %s",(dato,))
        while datos > 0:
              detalles = cur.fetchall()
              for id in detalles:
                  print("ID:",id[0])
                  print("Tipo:",id[1])
                  print("nombre:",id[2])
                  print("Temperatura Maxima:",id[3])
                  print("Temperatura Minima:",id[4])
                  print("Humedad Maxima:",id[5])
                  print("Humedad Minima:",id[6])
                  print("Humedad Tierra:",id[7])
                  tempMax = id[3]
                  tempMin = id[4]
                  humMax = id[5]
                  humMin = id[6]
                  humt = id[7]
                  while True:
                      sensor1() #esta linea llama a la funcion del sensor DHT22
                      temperature = sensor1()# sacamos los datos de la lectura del sensor DT22
                      print("temperatura dht22",temperature)
                      sensor2() #esta linea llama a la funcion del sensor DHT11
                      humidity = sensor2()# sacamos los datos de la lectura del sensor DT11
                      print("humedad dht22",humidity,"%")
                      #condiciones de cuidado de plantas
                      time.sleep(2.0)
                      #condicion de temperatura maxima y minina
                      if temperature >= tempMax:
                          GPIO.output(ventilador_temp, GPIO.LOW)
                          #correo_temperaturaM()
                      else:
                          GPIO.output(ventilador_temp, GPIO.HIGH)
                          
                      if temperature <= tempMin:
                          GPIO.output(luz, GPIO.LOW)
                          #correo_temperaturamin()
                      else:
                          GPIO.output(luz, GPIO.HIGH)
                     #condicion de humedad Maxima y Minima
                      if humidity >= humMax:
                          GPIO.output(ventilador_humedad, GPIO.LOW)
                          #correo_humedadM()
                      else:
                          GPIO.output(ventilador_humedad, GPIO.HIGH)
                      #incluir riego minimo
                      if humidity <= humMin:
                          print("humedad baja")
                      else:
                          GPIO.output(ventilador_temp, GPIO.HIGH)
    return render_template('Medicinales.html')
#-----------------------termina sección medicinales----------------------------------#
 
    
if __name__ == '__main__':
    app.run(debug=False)
    
