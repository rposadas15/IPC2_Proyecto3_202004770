from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import xml.etree.ElementTree as ET

from Factura import Factura
facturas = []
#estado = 1 = Aprobado
#estado = 0 = Rechazado

from Datos import Datos
datos_incorrectos = []

app = Flask(__name__)
CORS(app, resources={r"/*": {"origin": "*"}})

puerto = ''

#FACTURAS

@app.route('/Facturas', methods=['GET'])
def ObtenerFacturas():
    global puerto
    if puerto != '':
        nuevo_doc = open(puerto, 'r')
        data = nuevo_doc.read()
        nuevo_doc.close()
        return(jsonify({"Mensaje": data}))
    else:
        return(jsonify({"Mensaje": "Aun no se ha ingresado un archivo XML"}))

@app.route('/Facturas', methods=['POST'])
def CrearFacturas():
    global puerto
    puerto = 'facturas.xml'
    direccion = request.json['direc']
    mismo_doc = open(puerto, 'w')
    data = str(direccion)
    mismo_doc.write(data)
    mismo_doc.close()
    #NUEVO XML
    nuevo_doc = open(puerto, 'r')
    nueva_data = nuevo_doc.read()
    nuevo_doc.close()
    return (jsonify({"Mensaje": nueva_data}))


'''@app.route('/Facturas', methods=['GET'])
def ObtenerFacturas():
    global facturas
    Datos = []
    for persona in facturas:
        objeto = {
            'Lugar-Y-Fecha:': persona.getDia(),
            'Referencia': persona.getReferencia(),
            'Nit-Emisor': persona.getNitE(),
            'Nit-Receptor': persona.getNitR(),
            'Valor': persona.getValor(),
            'IVA':persona.getIva(),
            'Total': persona.getTotal(),
            'Estado': persona.getEstado()
        }
        Datos.append(objeto)
    return(jsonify(Datos))

@app.route('/Facturas', methods=['POST'])
def AgregarFactura(ruta):
    global facturas
    global datos_incorrectos
    eNE = 0
    eNR = 0
    fC = 0
    mI = 0
    totalM = 0
    listaRef = []
    ref = 0
    listaFE = []
    fE = 0
    listaFR = []
    fR = 0

    mytree = ET.parse(ruta)
    myroot = mytree.getroot()
    for x in myroot:
        for a1 in x.findall('TIEMPO'):
                for a2 in x.findall('REFERENCIA'):
                    for a3 in x.findall('NIT_EMISOR'):
                        eNE = Modulo11(a3, eNE)
                        print(eNE)
                        for a4 in x.findall('NIT_RECEPTOR'):
                            eNR = Modulo11(a4, eNR)
                            print(eNR)
                            for a5 in x.findall('VALOR'):                                
                                for a6 in x.findall('IVA'):
                                    mI = IVA(a5, a6, mI)
                                    for a7 in x.findall('TOTAL'):
                                        totalM = TOTAL(a5, a6, a7, totalM)
                                        listaRef.append(a2.text)
                                        listaFE.append(a3.text)
                                        listaFR.append(a4.text)
                                        #nuevo = Factura(a1.text, '-', a2.text, '-', a3.text, '-', a4.text, '-', a5.text, '-', a6.text, '-', a7.text)
                                        #facturas.append(nuevo)

    ref, fE, fR = DUPLICADOS(listaRef, listaFE, listaFR, ref, fE, fR)
                                        
    #print('NE:', eNE,'NR:', eNR, 'MI:', mI , 'TO', totalM, 'FacC:', fC)
    #print('REF:', ref, 'FacE:', fE, 'FacR', fR)

    #nuevo2 = Datos(eNE, eNR, mI, totalM, ref, fC, fE, fR)
    #datos_incorrectos.append(nuevo2)

    return jsonify({'Mensaje':'Se agrego la Factura',})'''

def Modulo11(valor, error):
    nit = []
    aux_m = 2
    sumatoria = 0
    aux_nit = valor.text
    aux_nit = aux_nit.replace(' ', '')
    aux_nit = aux_nit.rstrip(aux_nit[-1])
    if int(aux_nit) > 0:
        for dato in aux_nit:
                nit.append(dato)            
        for dato in reversed(nit):            
            sumatoria += int(dato) * aux_m            
            aux_m += 1
        sumatoria = 11 - sumatoria % 11
        if sumatoria == 10:
            estado = '1'
        else:
            error += 1
            estado = '0'
    return error

def IVA(valor, valor2, iva_mal):
    dato = float(valor.text)
    iva = dato * 0.12
    iva = round(iva, 3)    
    if iva != float(valor2.text):
        iva_mal += 1
    return iva_mal

def TOTAL(valor, valor2, valor3, t_mal):
    dato = float(valor.text)
    dato2 = float(valor2.text)    
    total = dato + dato2
    if total != float(valor3.text):
        t_mal += 1
    return t_mal

def DUPLICADOS(valor, valor2, valor3, a1, b1, c1):
    a = []
    b = []
    c = []
    for i in range(len(valor)):
        for j in range(len(valor)):
            if i != j:
                if valor[i] == valor[j] and valor[i] not in a:
                    a.append(valor[i])
                if valor2[i] == valor2[j] and valor2[i] not in b:
                    b.append(valor2[i])
                else:
                    b1 += 1
                if valor3[i] == valor3[j] and valor3[i] not in c:
                    c.append(valor3[i])
                else:
                    c1 += 1
    a1 = len(a)
    return a1, b1, c1

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 3000, debug = True)