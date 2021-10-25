class Datos:

    def __init__(self, fecha, errorNE, errorNR, iva, total, duplicadoRef, totalFac, facturasC, facturasE, facturasR):
        self.fecha = fecha
        self.errorNE = errorNE
        self.errorNR = errorNR
        self.iva = iva
        self.total = total
        self.duplicadoRef = duplicadoRef
        self.totalFac = totalFac
        self.facturasC = facturasC
        self.facturasE = facturasE
        self.facturasR = facturasR
        self.tamaño = []
    
    #Get
    def getFecha(self):
        return self.fecha

    def getErrorNE(self):
        return self.errorNE

    def getErrorNR(self):
        return self.errorNR

    def getIva(self):
        return self.iva

    def getTotal(self):
        return self.total

    def getDuplicadoRef(self):
        return self.duplicadoRef

    def getTotalFac(self):
        return self.totalFac

    def getFacturasC(self):
        return self.facturasC

    def getFacturasE(self):
        return self.facturasE

    def getFacturasR(self):
        return self.facturasR

    def getTamaño(self):
        for a in self.tamaño:
            print(a)

    #Set
    def setFecha(self, fecha):
        self.fecha = fecha

    def setErrorNE(self, errorNE):
        self.errorNE = errorNE

    def setErrorNR(self, errorNR):
        self.errorNR = errorNR

    def setIva(self, iva):
        self.iva = iva

    def setTotal(self, total):
        self.total = total

    def setDuplicadoRef(self, duplicadoRef):
        self.duplicadoRef = duplicadoRef

    def setTotalFac(self, totalFac):
        self.totalFac = totalFac

    def setFacturasC(self, facturasC):
        self.facturasC = facturasC

    def setFacturasE(self, facturasE):
        self.facturasE = facturasE

    def setFacturasR(self, facturasR):
        self.facturasR = facturasR