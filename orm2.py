import tkinter as tk
import random
import math
import sqlite3


#zona declarativa

personas=[]


class Persona:
    def __init__(self):
        self.posx=random.randint(0,768)
        self.posy=random.randint(0,768)
        self.size=10
        self.direccion=random.randint(0,360)
        self.color=self.colorRandom()
        self.identificador=""
        self.energia=100
        self.descanso=100
        self.cantidadEnergia=""
        self.cantidadDescanso=""
        self.edad=self.randomEdad()

    #crear colores aleatorios    
    def colorRandom(self):
         r=random.randint(0,255)
         g=random.randint(0,255)
         b=random.randint(0,255)
         hexadecimal="#{:02x}{:02x}{:02x}".format(r,g,b)
         return hexadecimal
    
    def randomEdad(self):
        self.edad=random.randint(0,99)
        return self.edad
    
    def dibujar (self):
        self.identificador=lienzo.create_rectangle(
            self.posx-self.size/2,
            self.posy-self.size/2,
            self.posx+self.size/2,
            self.posy+self.size/2,
            fill=self.color
        )
        self.cantidadEnergia=lienzo.create_rectangle(
            self.posx-self.size/2,
            self.posy-self.size/2-10,
            self.posx-self.size/2,
            self.posy-self.size/2-8,
            fill="green"
        )
        self.cantidadDescanso=lienzo.create_rectangle(
            self.posx-self.size/2,
            self.posy-self.size/2-16,
            self.posx-self.size/2,
            self.posy-self.size/2,
            fill="red"
        )

        

    def mover(self):
        if self.energia>0:
            self.energia-=0.2
        if self.descanso>0:
            self.descanso-=0.3

        lienzo.move(
             self.identificador,
             math.cos(self.direccion),
             math.sin(self.direccion)
             )
        
        anchoEnergia=(self.energia/100)*self.size
        lienzo.coords(
             self.cantidadEnergia,
             self.posx-self.size/2,
             self.posy-self.size/2-10,
             self.posx-self.size/2+anchoEnergia,
             self.posy-self.size/2-8
             )
        
        anchoDescanso=(self.descanso/100)*self.size
        lienzo.coords(
             self.cantidadDescanso,
             self.posx-self.size/2,
             self.posy-self.size/2-16,
             self.posx-self.size/2+anchoDescanso,
             self.posy-self.size/2-14
             )
        
        self.paredes()
        #actualizar posicion del objeto
        self.posx+=math.cos(self.direccion)
        self.posy+=math.sin(self.direccion)


    #rebotar paredes de la ventana
    def paredes(self):
         if self.posx < 0 or self.posx>768 or self.posy<0 or self.posy>768:
              self.direccion+=math.pi


def guardarEstado():
    print("guardado")
    
#Guardar en SQLite
    conexion=sqlite3.connect("poblacion.sqlite3")
    cursor=conexion.cursor()
    cursor.execute(" DELETE FROM poblacion1")
    conexion.commit()
    for persona in personas:
        cursor.execute('''
                    INSERT INTO poblacion
                    VALUES (
                    NULL,
                    '''+str(persona.posx)+''',
                    '''+str(persona.posy)+''',
                    '''+str(persona.size)+''',
                    '''+str(persona.direccion)+''',
                    "'''+str(persona.color)+'''",
                    "'''+str(persona.identificador)+'''",
                    '''+str(persona.energia)+''',
                    '''+str(persona.descanso)+''',
                    '''+str(persona.edad)+'''
                    )
                    ''')
    conexion.commit()
    conexion.close()

raiz=tk.Tk()

lienzo=tk.Canvas(raiz,width=768,height=768)
lienzo.pack()

boton=tk.Button(raiz,text="guardar",command=guardarEstado)
boton.pack()

#cargar desde SQL
try:
    conexion=sqlite3.connect("poblacion.sqlite3")
    cursor=conexion.cursor()
    cursor.execute('''
                   SELECT * 
                   FROM poblacion1
                   ''')
    while True:
        fila=cursor.fetchone()
        if fila is None:
            break
        persona=Persona()
        persona.posx=fila[1]
        persona.posy=fila[2]
        persona.size=fila[3]
        persona.direccion=fila[4]
        persona.color=fila[5]
        persona.identificador=fila[6]
        persona.energia=fila[7]
        persona.descanso=fila[8]
        persona.edad=fila[9]
        personas.append(persona)
    conexion.close()
    print("Cargado con exito")
except:
    print("error en recuperación")

#introduzco personas en la colección
if len(personas)==0:
    numeroPersonas=50
    for i in range (0, numeroPersonas):
        personas.append(Persona())


#para cada persona en colección las muestro en pantalla
for persona in personas:
    persona.dibujar()


#bucle para mover cada persona en colección
def bucle():
        for persona in personas:
            persona.mover()
        raiz.after(10,bucle)

bucle()



persona=Persona()
persona.dibujar()
raiz.mainloop()