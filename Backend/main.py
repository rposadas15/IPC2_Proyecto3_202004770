from types import prepare_class
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import xml.etree.ElementTree as ET
from datetime import date, datetime
import re

from Factura import Factura
facturas_correctas = []
#estado = 1 = Aprobado
#estado = 0 = Rechazado

from Datos import Datos
datos_salida = []

app = Flask(__name__)
CORS(app, resources={r"/*": {"origin": "*"}})

puerto = ''
puerto2 = ''

#FACTURAS
@app.route('/Facturas', methods=['GET'])
def ObtenerFacturas():
    global puerto
    if puerto != '' and puerto2 != '':
        nuevo_doc = open(puerto, 'r')
        data = nuevo_doc.readlines()
        nuevo_doc.close()

        nuevo_doc2 = open(puerto2, 'r')
        data2 = nuevo_doc2.readlines()
        nuevo_doc2.close()

        return(jsonify({"Mensaje": data, "Mensaje2": data2}))
    else:
        return(jsonify({"Mensaje": "Aun no se ha ingresado un archivo XML", "Mensaje2": "Esperando archivo de entrada"}))

@app.route('/Facturas', methods=['POST'])
def CrearFacturas():
    global puerto
    puerto = 'facturas.xml'
    
    #LEER XML
    direccion = request.json['direc']
    mismo_doc = open(puerto, 'w')
    data = str(direccion)
    mismo_doc.write(data)
    mismo_doc.close()
    
    #SALIDA XML
    informacion = LeerXML(puerto)
    SeparDatos(informacion)
    Salida()

    return (jsonify({"Mensaje": "Archivo Cargado Correctamente"}))

@app.route('/Facturas', methods=['DELETE'])
def EliminarFacturas():
    global puerto
    global puerto2
    global facturas_correctas
    global datos_salida

    #Entrada
    doc_entrada = open(puerto, 'w')
    doc_entrada.close()

    #Salida
    doc_salida = open(puerto2, 'w')
    doc_salida.close()

    puerto = ''
    puerto2 = ''
    facturas_correctas = []
    datos_salida = []

    '''
    print('Facturas Reinico')
    for a in range(len(facturas_correctas)):
        print(facturas_correctas[a].getDia())
        print(facturas_correctas[a].getReferencia())
        print(facturas_correctas[a].getNitE())
        print(facturas_correctas[a].getNitR())
        print(facturas_correctas[a].getValor())
        print(facturas_correctas[a].getIva())
        print(facturas_correctas[a].getTotal())
        print(facturas_correctas[a].getEstado())
        print('---')

    print('Errores Reinicio')
    for a in range(len(datos_salida)):        
        print(datos_salida[a].getFecha(), 'fecha')
        print(datos_salida[a].getErrorNE(), 'error NE')
        print(datos_salida[a].getErrorNR(), 'error NR')
        print(datos_salida[a].getIva(), 'iva')
        print(datos_salida[a].getTotal(), 'total')
        print(datos_salida[a].getDuplicadoRef(), 'ref duplicada')
        print(datos_salida[a].getTotalFac(), 'total facturas')
        print(datos_salida[a].getFacturasC(), 'facturas correctas')
        print(datos_salida[a].getFacturasE(), 'factuas NIT_E diferentes')
        print(datos_salida[a].getFacturasR(), 'factuas NIT_R diferentes')
        for b in datos_salida[a].tama??o:
            print(b.getDia(), 'tama??o')
        print('---')
    '''
    return jsonify({'Mensaje':'Se reincio el programa, puede iniciar de nuevo'})

def LeerXML(ruta):
    mytree = ET.parse(ruta)
    myroot = mytree.getroot()
    return myroot

def SeparDatos(data):
    global facturas_correctas
    fecha = ''
    bandera1 = False
    bandera2 = False
    bandera3 = False
    bandera4 = False
    bandera5 = False
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
    listaFechas = []
    for x in data:
        for a1 in x.findall('TIEMPO'):
            fecha = Fecha(a1, fecha)
            for a2 in x.findall('REFERENCIA'):
                for a3 in x.findall('NIT_EMISOR'):
                    for a4 in x.findall('NIT_RECEPTOR'):
                        for a5 in x.findall('VALOR'):
                            for a6 in x.findall('IVA'):
                                for a7 in x.findall('TOTAL'):
                                    listaRef.append(a2.text)
                                    listaFE.append(a3.text)
                                    listaFR.append(a4.text)
                                    listaFechas.append(fecha)
                                    nuevo1 = Factura(fecha, a2.text, a3.text, a4.text, a5.text, a6.text, a7.text, '1')
                                    facturas_correctas.append(nuevo1)

    lista_ref = Duplicados(listaRef)

    fechas_buenas = []
    for a in listaFechas:
        if a not in fechas_buenas:
            fechas_buenas.append(a)

    for a in fechas_buenas:        
        nuevo2 = Datos(a, '0', '0', '0', '0', '0', '0', '0', '1', '1')
        datos_salida.append(nuevo2)

    for a in range(len(facturas_correctas)):
        for b in range(len(datos_salida)):
            if datos_salida[b].getFecha() == facturas_correctas[a].getDia():
                eNE, bandera1 = Modulo11(facturas_correctas[a].getNitE(), eNE, bandera1)
                eNR, bandera2 = Modulo11(facturas_correctas[a].getNitR(), eNR, bandera2)
                mI, bandera3 = IVA(facturas_correctas[a].getValor(), facturas_correctas[a].getIva(), mI, bandera3)
                totalM, bandera4 = Total(facturas_correctas[a].getValor(), facturas_correctas[a].getIva(), facturas_correctas[a].getTotal(), totalM, bandera4)
                datos_salida[b].setErrorNE(str(int(datos_salida[b].getErrorNE()) + eNE))
                datos_salida[b].setErrorNR(str(int(datos_salida[b].getErrorNR()) + eNR))
                datos_salida[b].setIva(str(int(datos_salida[b].getIva()) + mI))
                datos_salida[b].setTotal(str(int(datos_salida[b].getTotal()) + totalM))
                datos_salida[b].setTotalFac(str(int(datos_salida[b].getTotalFac()) + 1))
                if not lista_ref:
                    bandera5 = True
                else:                    
                    for c in lista_ref:
                        if c == facturas_correctas[a].getReferencia():
                            datos_salida[b].setDuplicadoRef(str(int(datos_salida[b].getDuplicadoRef()) + 1))
                            facturas_correctas[a].setEstado('0')
                            bandera5 = False
                        else:
                            bandera5 = True
                if bandera1 and bandera2 and bandera3 and bandera4 and bandera5:
                    facturas_correctas[a].setEstado('1')
                    datos_salida[b].tama??o.append(facturas_correctas[a])
                else:
                    facturas_correctas[a].setEstado('0')
            eNE = 0
            eNR = 0
            mI = 0
            totalM = 0
            bandera5 = False

    for a in range(len(facturas_correctas)):
        for b in range(len(datos_salida)):
            if datos_salida[b].getFecha() == facturas_correctas[a].getDia():
                if facturas_correctas[a].getEstado() == '1':
                    datos_salida[b].setFacturasC(str(int(datos_salida[b].getFacturasC()) + 1))

    for a in range(len(datos_salida)):
        for b in datos_salida[a].tama??o:
            for c in datos_salida[a].tama??o:               
                if b.getNitE() != c.getNitE():
                    datos_salida[a].setFacturasE(str(int(datos_salida[a].getFacturasE()) + 1))
                else:
                    pass
                if b.getNitR() != c.getNitR():
                    datos_salida[a].setFacturasR(str(int(datos_salida[a].getFacturasR()) + 1))
                else:
                    pass
    
    '''
    print('Facturas')
    for a in range(len(facturas_correctas)):
        print(facturas_correctas[a].getDia())
        print(facturas_correctas[a].getReferencia())
        print(facturas_correctas[a].getNitE())
        print(facturas_correctas[a].getNitR())
        print(facturas_correctas[a].getValor())
        print(facturas_correctas[a].getIva())
        print(facturas_correctas[a].getTotal())
        print(facturas_correctas[a].getEstado())
        print('---')

    print('Errores')
    for a in range(len(datos_salida)):        
        print(datos_salida[a].getFecha(), 'fecha')
        print(datos_salida[a].getErrorNE(), 'error NE')
        print(datos_salida[a].getErrorNR(), 'error NR')
        print(datos_salida[a].getIva(), 'iva')
        print(datos_salida[a].getTotal(), 'total')
        print(datos_salida[a].getDuplicadoRef(), 'ref duplicada')
        print(datos_salida[a].getTotalFac(), 'total facturas')
        print(datos_salida[a].getFacturasC(), 'facturas correctas')
        print(datos_salida[a].getFacturasE(), 'factuas NIT_E diferentes')
        print(datos_salida[a].getFacturasR(), 'factuas NIT_R diferentes')
        for b in datos_salida[a].tama??o:
            print(b.getDia(), 'tama??o')
        print('---')
    '''

def Modulo11(valor, error, bandera):
    nit = []
    aux_m = 2
    sumatoria = 0
    aux_nit = valor
    aux_nit = aux_nit.replace(' ', '')
    ultimo_valor = aux_nit[-1]
    aux_nit = aux_nit.rstrip(aux_nit[-1])
    if aux_nit.isnumeric():
        if int(aux_nit) > 0:
            for dato in aux_nit:
                nit.append(dato)
            for dato in reversed(nit):
                sumatoria += int(dato) * aux_m
                aux_m += 1
                if aux_m == 8:
                    aux_m = 2
            sumatoria = 11 - sumatoria % 11        
            if sumatoria < 10:
                if ultimo_valor == 'k' or ultimo_valor == 'K':
                    error += 1
                    bandera = False
                else:
                    if int(sumatoria) == int(ultimo_valor):
                        bandera = True
                    else:
                        error += 1
                        bandera = False
            elif sumatoria == 10:
                if ultimo_valor == 'k' or ultimo_valor == 'K':
                    bandera = True
                else:
                    error += 1
                    bandera = False
            elif sumatoria == 11:
                if int(ultimo_valor) == 0:
                    bandera = True
                else:
                    error += 1
                    bandera = False
    else:
        error += 1
        bandera = False
    return error, bandera

def IVA(valor, valor2, iva_mal, bandera):
    dato = float(valor)
    iva = dato * 0.12
    iva = round(iva, 3)
    if iva != float(valor2):
        iva_mal += 1
        bandera = False
    else:
        bandera = True
    return iva_mal, bandera

def Total(valor, valor2, valor3, t_mal, bandera):
    dato = float(valor)
    dato2 = float(valor2)    
    total = dato + dato2
    if total != float(valor3):
        t_mal += 1
        bandera = False
    else:
        bandera = True
    return t_mal, bandera

def Duplicados(valor):
    a = []
    for i in range(len(valor)):
        for j in range(len(valor)):
            if i != j:
                if valor[i] == valor[j] and valor[i] not in a:
                    a.append(valor[i])
    return a

def Fecha(valor, fecha):
    aux_fecha = valor.text
    patronDecimal = "[0-9]+\/[0-9]+\/[0-9]+"
    fecha = re.findall(patronDecimal, aux_fecha)[0]
    return fecha

def Salida():
    global datos_salida
    global facturas_correctas
    global puerto2
    puerto2 = 'autorizaciones.xml'

    root = ET.Element('LISTA_AUTORIZACIONES')
    for a in range(len(datos_salida)):
        doc1 = ET.SubElement(root, 'AUTORIZACION')
        nodo1 = ET.SubElement(doc1, 'FECHA')
        nodo1.text = datos_salida[a].getFecha()
        nodo2 = ET.SubElement(doc1, 'FACTURAS_RECIBIDAS')
        nodo2.text = datos_salida[a].getTotalFac()
        doc2 = ET.SubElement(doc1, 'ERRORES')
        nodo3 = ET.SubElement(doc2, 'NIT_EMISOR')
        nodo3.text = datos_salida[a].getErrorNE()
        nodo4 = ET.SubElement(doc2, 'NIT_RECEPTOR')
        nodo4.text = datos_salida[a].getErrorNR()
        nodo5 = ET.SubElement(doc2, 'IVA')
        nodo5.text = datos_salida[a].getIva()
        nodo6 = ET.SubElement(doc2, 'TOTAL')
        nodo6.text = datos_salida[a].getTotal()
        nodo7 = ET.SubElement(doc2, 'REFERENCIA_DUPLICADA')
        nodo7.text = datos_salida[a].getDuplicadoRef()
        nodo8 = ET.SubElement(doc1, 'FACTURAS_CORRECTAS')
        nodo8.text = datos_salida[a].getFacturasC()
        nodo9 = ET.SubElement(doc1, 'CANTIDAD_EMISORES')
        nodo9.text = datos_salida[a].getFacturasE()
        nodo10 = ET.SubElement(doc1, 'CANTIDAD_RECEPTORES')
        nodo10.text = datos_salida[a].getFacturasR()
        doc3 = ET.SubElement(doc1, 'LISTADO_AUTORIZACIONES')
        for b in datos_salida[a].tama??o:
            doc4 = ET.SubElement(doc3, 'APROBACION')
            nodo12 = ET.SubElement(doc4, 'NIT_EMISOR', ref = b.getReferencia())
            nodo12.text = str(b.getNitE())
            nodo13 = ET.SubElement(doc4, 'CODIGO_APROBACION')
            nodo13.text = Aprobacion(str(b.getDia()))
        
    arbol = ET.ElementTree(root)
    arbol.write('autorizaciones.xml')

def Aprobacion(fecha):
    fecha = fecha.split('/')
    fecha = fecha[:: -1]
    apro = ''
    for a in fecha:
        apro += a
    
    return apro

#GFAFICAS
@app.route('/Grafica', methods=['GET'])
def ObtenerGrafica():
    global facturas_correctas
    global datos_salida
    Datos_Combobox = []
    
    for a in range(len(datos_salida)):
        for b in datos_salida[a].tama??o:
            objeto = {
                'Fecha': b.getDia()
            }
            Datos_Combobox.append(objeto)
    return (jsonify(Datos_Combobox))

@app.route('/Fechas', methods=['POST'])
def CrearGraficasFechas():
    global facturas_correctas
    global datos_salida
    Fechas = []
    FechaI = request.json['Inicio']
    FechaF = request.json['Fin']
    
    aux_FichaI = datetime.strptime(FechaI, '%d/%m/%Y')
    aux_FichaF = datetime.strptime(FechaF, '%d/%m/%Y')

    for a in range(len(datos_salida)):
        aux_total = 0
        aux_iva = 0
        aux_FechaA  = datetime.strptime(facturas_correctas[a].getDia(), '%d/%m/%Y')
        if aux_FichaI <= aux_FechaA and aux_FichaF >= aux_FechaA:
            for b in datos_salida[a].tama??o:
                aux_total += float(b.getTotal())
                aux_iva += float(b.getValor())
                objeto = {
                    'Fecha': b.getDia(),
                    'Total': aux_total,
                    'SinIVA': aux_iva
                }
                Fechas.append(objeto)
    return (jsonify(Fechas))

@app.route('/IVA', methods=['POST'])
def CrearGraficasIVA():
    global facturas_correctas
    Datos_IVA = []
    
    Fecha = request.json['Fecha']
    
    for a in range(len(datos_salida)):
        for b in datos_salida[a].tama??o:
            if b.getDia() == str(Fecha):
                objeto = {
                    'Nit': b.getNitE(),
                    'Total': b.getTotal(),
                    'Valor_IVA': b.getIva()
                }
                Datos_IVA.append(objeto)
    return (jsonify(Datos_IVA))

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 3000, debug = True)