# ----------------------------------------------------------------------------------------
# PROGRAMA: <<Parcial final>>
# ----------------------------------------------------------------------------------------
# Descripción: <<Se realizan tres puntos por medio de la imagen de soccer.>>
# ----------------------------------------------------------------------------------------
# Autor:
''' 
# Miguel David Benavides Galindo            md_benavidesg@javeriana.edu.co
'''
# Version: 1.0
# [24.11.2021]
# ----------------------------------------------------------------------------------------
# IMPORTAR MODULOS
import os
import cv2 # opencv version 3.4.2
import numpy as np # numpy version 1.16.3
import random
import mediapipe as mp
import sys

### Definir ruta donde esta la imagen
ruta = "C:/Users/User/Desktop/soccer_game.png"

# ----------------------------------------------------------------------------------------
# PUNTOS DEL PARCIAL A RESOLVER
# ----------------------------------------------------------------------------------------
################################ FUNCION RESPUESTA ################################
def Respuesta(original):  
    points = []
    def click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
    
    image_draw = np.copy(original)
    
    points1 = []
    cv2.namedWindow("Seleccione su respuesta")
    cv2.setMouseCallback("Seleccione su respuesta", click)
    
    point_counter = 0
    print("Presione x, al terminar")
    
    z = True
    while z:
        cv2.imshow("Seleccione su respuesta", image_draw)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("x") or len(points) == 4:
            points1 = points.copy()
            points = []
            break
        if len(points) > point_counter:
            point_counter = len(points)
            if len(points) < 3:
                cv2.circle(image_draw, (points[-1][0], points[-1][1]), 8, [255, 0, 0], -1)
            else:
                cv2.circle(image_draw, (points[-1][0], points[-1][1]), 8, [0, 233, 255], -1)
    del points, key, point_counter, image_draw
    cv2. destroyAllWindows()
    return points1[0:3]


####################### PRIMER PUNTO ####################################
original = cv2.imread(ruta)
image = cv2.resize(original, (1050,720))

# Hue histogram
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
hist_hue = cv2.calcHist([image_hsv], [0], None, [180], [0, 180])

# Hue histogram max and location of max
max_pos = int(hist_hue.argmax())

# Peak mask
lim_inf = (max_pos - 10, 0, 0)
lim_sup = (max_pos + 10, 255, 255)
mask = cv2.inRange(image_hsv, lim_inf, lim_sup)

kernel = np.ones((3,3), np.uint8)
 
img_erosion = cv2.erode(mask, kernel, iterations=2)
img_dilation = cv2.dilate(img_erosion, kernel, iterations=2)

Pix_total = 0
blancos = 0
for j in range(len(mask)):
    for i in range(len(mask[1])):
        Pix_total = Pix_total + 1
        if(mask[j][i]!=0):
            blancos = blancos + 1  
            
print("El porcentaje de pixeles de la imagen que corresponden al césped son:",(blancos/Pix_total)*100)
            
cv2.imshow("Image", img_erosion)
#cv2.imshow("original", image)
cv2.waitKey(0)


####################### SEGUNDO PUNTO ####################################
original = cv2.imread(ruta)
image = cv2.resize(original, (1050,720))

# Hue histogram
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
hist_hue = cv2.calcHist([image_hsv], [0], None, [180], [0, 180])

# Hue histogram max and location of max
max_pos = int(hist_hue.argmax())

# Peak mask
lim_inf = (max_pos - 10, 0, 0)
lim_sup = (max_pos + 10, 255, 255)
mask = cv2.inRange(image_hsv, lim_inf, lim_sup)

kernel = np.ones((3,3), np.uint8)
 
img_erosion = cv2.erode(mask, kernel, iterations=2)
gray = cv2.dilate(img_erosion, kernel, iterations=2)

ret, th = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
(contornos,_) = cv2.findContours(th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cuantos_jugadores = 0
for i in range(len(contornos)):  
    cnt = contornos[i]
    perimetro = cv2.arcLength(cnt, True)    
    x,y,w,h = cv2.boundingRect(cnt)  
    
    if perimetro > 100 and perimetro < 380: 
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 1, cv2.LINE_AA)
        cuantos_jugadores = cuantos_jugadores + 1
        
print("El número de jugadores/arbitros en la cancha es:",cuantos_jugadores)
            
cv2.imshow('contornos', image)
cv2.waitKey(0)


####################### TERCER PUNTO ####################################

original = cv2.imread(ruta)
image = cv2.resize(original, (1050,720))

puntos_respuesta = Respuesta(image)
cv2. destroyAllWindows()

m = (puntos_respuesta[1][1] - puntos_respuesta[0][1])/(puntos_respuesta[1][0]-puntos_respuesta[0][0])
b = puntos_respuesta[1][1] - m*puntos_respuesta[1][0]

y_1 = int(b)
x_1 = 0

y_2 = int(m*(len(image[0])) + b)
x_2 = len(image[0]) 

cv2.line(image,(x_1,y_1),(x_2,y_2),(255,0,0),4)

cv2.circle(image, (puntos_respuesta[1][0], puntos_respuesta[1][1]), 8, [255, 0, 0], -1)
cv2.circle(image, (puntos_respuesta[0][0], puntos_respuesta[0][1]), 8, [255, 0, 0], -1)

nombres_puntos = ["P1","P2","P3"]
colores_puntos = [(255, 0, 0),(255, 0, 0),(0, 233, 255)]
for i in range(len(puntos_respuesta)):
    tipoLetra = cv2.FONT_HERSHEY_COMPLEX_SMALL
    texto = nombres_puntos[i]
    tamañoLetra = 0.7
    colorLetra = colores_puntos[i]
    grosorLetra = 1
    ubicacion = (puntos_respuesta[i][0]+15,puntos_respuesta[i][1]-15)
    cv2.putText(image, texto, ubicacion, tipoLetra, tamañoLetra, colorLetra, grosorLetra, cv2.LINE_AA)
        
b_p2 = puntos_respuesta[2][1] - m*puntos_respuesta[2][0]

y_1_p2 = int(b_p2)
x_1_p2 = 0

y_2_p2 = int(m*(len(image[0])) + b_p2)
x_2_p2 = len(image[0]) 

cv2.line(image,(x_1_p2,y_1_p2),(x_2_p2,y_2_p2),(0, 233, 255),4)

cv2.circle(image, (puntos_respuesta[2][0], puntos_respuesta[2][1]), 8, [0, 233, 255], -1)

cv2.imshow('contornos', image)
cv2.waitKey(0)
# ----------------------------------------------------------------------------------------
# end.
# ----------------------------------------------------------------------------------------