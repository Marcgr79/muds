import requests
import os
import json
import argparse

#Declaración de clases
class Usuario:

    #Atributos de la clase
    nombre: str
    apellido: str
    genero: int
    pais: str
    edad: int
    telf: str
    pasw: str

    #Constructor de la clase
    def __init__(self, nombre, apellido, genero, pais, edad, telf, pasw):
        self.nombre = nombre
        self.apellido = apellido
        self.genero = 1 if genero == "male" else 0
        self.pais = pais
        self.edad = edad
        self.telf = telf
        self.pasw = pasw

class Pais:

    #Atributos de la clase
    pais: str
    usuarios: list

    #Atributos constantes de la clase
    edad_min = 20
    edad_max = 35

    #Constructor de la clase
    ### Función que obtiene de la carpeta de "countries" el pais que se le pasa como parametro
    ### Y analiza linea a linea el archivo txt y obtiene los usuarios para guardarlos en una lista
    ### Esta lista será una lista de variables tipo Usuario.

    # self Pais parametro propio de la clase
    # pais str pais del cual se quiere crear un objeto
    def __init__(self, pais):
        self.pais = pais
        self.usuarios = []
        with open(os.path.dirname(os.getcwd())+"/countries/"+pais+'/'+pais+'.txt','r',encoding='utf-8') as archivo:
            for obj in archivo:
                self.usuarios.append(Usuario(**json.loads(obj)))
     
                
    #Método ejemplo de la clase
    ### Función que devuelve los usuarios comprendidos entre la edad_min y la edad_max

    # self Pais parametro propio de la clase
    # return res list lista de usuarios
    def getEncuestaUsuarios(self):
        res = []
        for i in self.users:
            if i.edad >= self.edad_min and i.edad <= self.edad_max:
                res.append(i)
        return res
    

#Declaración de las funciones (métodos) públicas que se van a usar


### Función que descarga los datos de la url proporcionada, y los guarda en un dict
# url str link web hacia la api para descargar los datos (https://randomuser.me/api)
# numero_personas int numero de personas que queremos que se descarguen de una sola llamada
    # maximo de 5000
def descargar_datos(url,numero_personas):
    #url = url +'/?results='+str(numero_personas)
    #raw_data = requests.get(url)
    #results = raw_data.json()
    #results = results['results']
    #return results

    # En vez de hacer esas 5 líneas se puede sintetizar de la siguiente manera
    return requests.get(url+'/?results='+str(numero_personas)).json()['results']

### Función que transforma todos los datos a tipo clase Usuario y los carga en los ficheros locales
# data dict diccionario que contiene todos los usuarios de la descarga
def cargar_datos(data):

    ### Función privada que crea una carpeta si esta no existe
    # lista_paises list lista de str de paises que se han procesado almenos una vez
    # actual str pais que se esta procesando actualmente
    def crear_carpeta(lista_paises,actual):
        #compruebo primero en el set porque es más óptimo
        if not actual in lista_paises and not os.path.exists(os.path.dirname(os.getcwd())+"/countries/"+actual):
            os.mkdir(os.path.dirname(os.getcwd())+"/countries/"+actual)
            lista_paises.add(actual)
    
    ################################################################################
    
    lista_paises = set()
    for i in data:
        newU = Usuario(i['name']['first'],i['name']['last'],i['gender'],i['location']['country'],
                    i['dob']['age'],i['phone'], i['login']['password'])
        pais_actual = i['location']['country']
        crear_carpeta(lista_paises,pais_actual)
        with open(os.path.dirname(os.getcwd())+"/countries/" + pais_actual+ "/"+ pais_actual+ '.txt', 
                  'a',encoding='utf-8') as archivo:
            archivo.write(json.dumps(newU.__dict__)+"\n")

### Función que obtiene una lista con todos los paises distintos
# return list lista de paises
def getListaPaises():
    return os.listdir(os.path.dirname(os.getcwd())+"/countries")

### Función que obtiene todos los usuarios de todos los paises y los guarda almacenados 
### en una lista de objetos tipo Pais, donde cada Pais tendrá su propio atributo
### usuarios que contendre la lista de todos los usuarios del pais
def getTodo():
    toda_data = []
    for c in getListaPaises():
        toda_data.append(Pais(c))
    return toda_data


### Función principal del codigo. Es lo que se ejecuta cuando se lanza el archivo.py
### En esta función se encontrará todo el proceso de carga realizado 4 veces para un total
### de 5000 usuarios por vez y después se procesaran los datos hasta obtenerlo todo.
### Una vez todo, ya se podrá volver a procesar y sacar las estadisticas que hagan falta

def main():
    parser = argparse.ArgumentParser(description="Ejecutar funciones desde la linea de comandos")
    parser.add_argument('--opcion', choices=['todo','especifico'], help='Elige la funcion a ejecutar')
    args = parser.parse_args()
    if args.opcion == 'todo':

        numero_personas = 5000
        url = "https://randomuser.me/api"
        for _ in range(4): 
            #res = descargar_datos(url,numero_personas)
            #cargar_datos(res)
            #Sintetizado en una linea
            cargar_datos(descargar_datos(url,numero_personas))
        
        toda_data = getTodo()
        #El resultado de esto debería de dar el numero total de paises que hay
        print(len(toda_data))

    elif args.opcion == 'especifico':
            nombre_pais = input("Ingrese el nombre del país: ")
            estadistica_genero(nombre_pais)
            estadistica_edades(nombre_pais)
            estadistica_contraseñas(nombre_pais)
    else:
        print("Este es el metodo sin argumentos")

   
def estadistica_genero(nombre_pais):
    pais = Pais(nombre_pais)  

    total_usuarios = len(pais.usuarios)
    total_hombres = sum(1 for usuario in pais.usuarios if usuario.genero == 1)
    total_mujeres = total_usuarios - total_hombres

    porcentaje_hombres = (total_hombres / total_usuarios) * 100
    porcentaje_mujeres = (total_mujeres / total_usuarios) * 100
    
    print(f"Estadísticas para {nombre_pais}:")
    print(f"Total de usuarios: {total_usuarios}")
    print(f"Porcentaje de hombres: {porcentaje_hombres:.2f}%")
    print(f"Porcentaje de mujeres: {porcentaje_mujeres:.2f}%")
    
    #for usuario in pais.usuarios:
    #    print(f"Usuario: {usuario.nombre} {usuario.apellido}, Género: {usuario.genero}")

def estadistica_edades(nombre_pais):
    pais = Pais(nombre_pais)  

    total_usuarios = len(pais.usuarios)
    menores_de_edad = 0
    juventud = 0
    adultez = 0
    personas_mayores = 0

    for usuario in pais.usuarios:
        edad = usuario.edad
        if edad < 18:
            menores_de_edad += 1
        elif 18 <= edad <= 26:
            juventud += 1
        elif 27 <= edad <= 59:
            adultez += 1
        else:
            personas_mayores += 1

    porcentaje_menores_de_edad = (menores_de_edad / total_usuarios) * 100
    porcentaje_juventud = (juventud / total_usuarios) * 100
    porcentaje_adultez = (adultez / total_usuarios) * 100
    porcentaje_personas_mayores = (personas_mayores / total_usuarios) * 100

    print(f"Estadísticas de edades para {nombre_pais}:")
    print(f"Porcentaje de menores de edad: {porcentaje_menores_de_edad:.2f}%")
    print(f"Porcentaje de juventud: {porcentaje_juventud:.2f}%")
    print(f"Porcentaje de adultez: {porcentaje_adultez:.2f}%")
    print(f"Porcentaje de personas mayores: {porcentaje_personas_mayores:.2f}%")  

def contiene_letras_numeros(contraseña):
    tiene_letras = False
    tiene_numeros = False

    for caracter in contraseña:
        if caracter.isalpha():
            tiene_letras = True
        elif caracter.isdigit():
            tiene_numeros = True

    return tiene_letras and tiene_numeros
    
def estadistica_contraseñas(nombre_pais):
    pais = Pais(nombre_pais)  

    total_usuarios = len(pais.usuarios)
    seguridad_baja = 0
    seguridad_media = 0
    seguridad_alta = 0
    seguridad_extrema = 0

    for usuario in pais.usuarios:
        contraseña = usuario.pasw
        longitud_contraseña = len(contraseña)

        if longitud_contraseña < 5:
            seguridad_baja += 1
        elif 5 <= longitud_contraseña <= 8:
            if contiene_letras_numeros(contraseña):
                seguridad_alta += 1
            else:
                seguridad_media += 1
        elif 8 <= longitud_contraseña <= 12:
            if contiene_letras_numeros(contraseña):
                seguridad_extrema += 1
            else:
                seguridad_alta += 1
        else:
            seguridad_extrema += 1

    porcentaje_seguridad_baja = (seguridad_baja / total_usuarios) * 100
    porcentaje_seguridad_media = (seguridad_media / total_usuarios) * 100
    porcentaje_seguridad_alta = (seguridad_alta / total_usuarios) * 100
    porcentaje_seguridad_extrema = (seguridad_extrema / total_usuarios) * 100

    print(f"Estadísticas de contraseñas para {nombre_pais}:")
    print(f"Porcentaje contraseñas débiles: {porcentaje_seguridad_baja:.2f}%")
    print(f"Porcentaje de contraseñas medianamente seguras: {porcentaje_seguridad_media:.2f}%")
    print(f"Porcentaje de contraseñas seguras: {porcentaje_seguridad_alta:.2f}%")
    print(f"Porcentaje de contraseñas extremadamente seguras: {porcentaje_seguridad_extrema:.2f}%")

if __name__ == "__main__":
   main()