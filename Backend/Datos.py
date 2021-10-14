class Datos:

    def __init__(self, errorNE, errorNR, iva, total, duplicadoRef, facturasC, facturasE, facturasR):
        self.errorNE = errorNE
        self.errorNR = errorNR
        self.iva = iva
        self.total = total
        self.duplicadoRef = duplicadoRef
        self.facturasC = facturasC
        self.facturasE = facturasE
        self.facturasR = facturasR
    
    #Get
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

    def getFacturasC(self):
        return self.facturasC

    def getFacturasE(self):
        return self.facturasE

    def getFacturasR(self):
        return self.facturasR

    #Set
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

    def setFacturasC(self, facturasC):
        self.facturasC = facturasC

    def setFacturasE(self, facturasE):
        self.facturasE = facturasE

    def setFacturasR(self, facturasR):
        self.facturasR = facturasR