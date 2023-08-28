from selenium import webdriver
import chromedriver_autoinstaller
import time
import helium as he
import csv

chromedriver_autoinstaller.install()

 # Iniciar el navegador usando Helium
he.start_chrome()


# Abrir el sitio web
he.go_to('https://www.turismocity.com.ar')

# Ingresar los detalles de búsqueda
search_box = he.S("#flights-tab-container > form > div:nth-child(2) > div > div:nth-child(2) > div > div > div > span")
he.wait_until(search_box.exists) 
he.click(search_box)

he.write("Buenos Aires")
time.sleep(2)  
he.press(he.DOWN)  
he.press(he.ENTER) 

search_box2 = he.S("#flights-tab-container > form > div:nth-child(2) > div > div:nth-child(3) > div > div > div > span")
he.wait_until(search_box2.exists) 
he.click(search_box2)

he.write("Madrid")
time.sleep(2)
he.press(he.DOWN)
he.press(he.ENTER)

fechas_baratas = he.find_all(he.S("#flights-tab-container > form > div:nth-child(2) > div > div:nth-child(5) > div > div > div"))
he.click(fechas_baratas[0])

time.sleep(1)

boton_buscar = he.S("#flights-tab-container > form > div:nth-child(4) > div > input")
he.click(boton_buscar)


# Esperar a que carguen los resultados
time.sleep(3)

# Recopilar los precios de los vuelos 
prices_turismocity = []
for price_element in he.find_all(he.S(".priceWrapper")):
    prices_turismocity.append(price_element.web_element.text)


#Ahora va a la web de Almundo
he.go_to('https://almundo.com.ar')

#Busca el lugar de origen del viaje
search_box = he.S(".flights-searchbox__form-input")
he.click(search_box)

he.write("Buenos Aires")
resultado_selector = he.S(".autocomplete_item.ng-star-inserted")
he.wait_until(resultado_selector.exists)  

resultado = he.find_all(resultado_selector)
if resultado:
    he.click(resultado[5])
else:
    print("No se encontraron resultados")

#Busca el lugar de destino
search_box = he.S("#flight-to")
he.click(search_box)

he.write("Madrid")
resultado_selector2 = he.S(".autocomplete_items")
he.wait_until(resultado_selector2.exists)  

resultado2 = he.find_all(resultado_selector2)
if resultado2:
    he.click(resultado2[1])
else:
    print("No se encontraron resultados")


#Tilda la caja de aun no decidi fecha
no_decidi_fecha = he.find_all(he.S(".mb-checkbox__mark"))
he.click(no_decidi_fecha[0])
time.sleep(1)

#Aprieta el boton buscar
boton_buscar = he.S(".mb-button") 

boton = he.find_all(boton_buscar)
if boton:
    he.click(boton[0])
else:
    print("No se encontraron resultados")

time.sleep(5)

# Recopilar los precios de los vuelos
prices_almundo = []
for price_element in he.find_all(he.S(".offer_price_value")):
    prices_almundo.append(price_element.web_element.text)

# Crear y escribir los precios en un archivo CSV
    with open('precios_vuelos.csv', 'w+', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Precios Turismocity', 'Precios Almundo'])  # Escribir encabezados de columna
        for turismocity_price, almundo_price in zip(prices_turismocity, prices_almundo):
            csvwriter.writerow([turismocity_price, almundo_price])

# Cerrar el navegador
he.kill_browser()
    



