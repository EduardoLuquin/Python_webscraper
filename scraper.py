
# Request - Me permite hacer peticiones de informacion de paginas web
# BeautifulSoup - Me permite extraer datos de html y xml, como una especie de parser  
import requests
from bs4 import BeautifulSoup
import smtplib
import time
# Tuve que instalar selemium ya que paginas de amazon, no permiten hacer request sin estar loggeado o en la pagina
import selenium
from selenium import webdriver

import locale
locale.setlocale(locale.LC_ALL,'en_US.UTF8')


def check_price():

    # URL de la pagina de la que estamos haciendo request  
    URL0_var = 'https://www.amazon.com.mx/Hamilton-Beach-80393-Custom-Molino/dp/B0743STL26/ref=sr_1_4?__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1P140CH9Y6HY3&dchild=1&keywords=molino+de+cafe&qid=1608590256&sprefix=molino%2Caps%2C218&sr=8-4'
    print("** URLS obtenidas **")

    # Defino mi "user agent" que busque previamente en Google
    Headers_var = { 
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    
    driver = webdriver.Firefox()
    get = driver.get(URL0_var)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    Price_var = soup.find('span',id="priceblock_ourprice")
    Title_var = soup.find(id="productTitle")
    
    #Matar la instancia del navegador
    driver.quit()
    print(Title_var.text.strip('\n'))
    print(Price_var.text.strip('\n'))

    #Conversion a numerico
    #https://stackoverflow.com/questions/8421922/how-do-i-convert-a-currency-string-to-a-floating-point-number-in-python
    PriceConverted_var = locale.atof(Price_var.text.strip("$"))
    print("Costo del producto convertido:",PriceConverted_var)

    if( PriceConverted_var < 829):
        send_mail()
    else:
        print("Por el momento el producto no tiene oferta:",PriceConverted_var)

    #To Do 
    # Send link and result as return to TelegramBot


"""
 #Esta conversion, es para quitar caracteres raros y hacer float
    #To Do: Trabaja en una funcion para limpiar de manera automatica el string 
    #PriceConverted_var = float(Price_var[1]+Price_var[3:6]) 
    #print("Costo del producto convertido:",PriceConverted_var)

    # La solucion para este problema esta en el mismo video, no puedo hacer request a Amazon de esta manera
    # Verifica si es posible en otra paginas
    print("** Buscando producto ** \n")
    Page_var = requests.get(URL0_var, headers = Headers_var)
    Soup_var = BeautifulSoup(Page_var.content, 'html.parser')
    Title_var = Soup_var.find(id="productTitle").get_text()
    Price_var = Soup_var.find(id="price_inside_buybox").get_text()
    print("Price_var: ",Price_var)
"""


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com',587)
    #Parte del protocolo para mandar mails
    server.ehlo()
    #Encriptar conexion
    server.starttls()
    server.ehlo()

    #Loggear al correo electronico
    server.login('eduardo.partialcount@gmail.com','')

    #Definir contenido del email
    Subject_var = 'Python Script: Producto en oferta'
    Body_var = 'Haz click en el link para ver oferta:'
    Msg_var = f"Subject: {Subject_var}\n\n{Body_var}"

    #Definir Origen y destinatario
    server.sendmail(
        'eduardo.partialcount@gmail.com',
        'quekpanda_14@hotmail.com',
        Msg_var)
    
    print('Email enviado correctamente')

    #Cerrar coneccion con el servidor
    server.quit()

#Cierro el contexto de la funcion principal
#check_price()

#while(True):
    #check_price()
    #Monitorea cada 60 segundos el costo del producto. 
    #Cambiarlo a cada 2 o 3 horas
    #time.sleep(60)

#To Do meter, esto aun servidor 

if __name__ == '__main__':
    #try:
        print('Ejecutando Aplicacion')
        #while True:
        check_price()
    #except KeyboardInterrupt:
        #exit()
