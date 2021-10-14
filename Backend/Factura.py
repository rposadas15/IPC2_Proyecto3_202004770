class Factura:

    def __init__(self, dia, referencia, nitE, nitR, valor, iva, total, estado):
        self.dia = dia
        self.referencia = referencia
        self.nitE = nitE
        self.nitR = nitR
        self.valor = valor
        self.iva = iva
        self.total = total
        self.estado = estado

    #Get
    def getDia(self):
        return self.dia

    def getReferencia(self):
        return self.referencia

    def getNitE(self):
        return self.nitE

    def getNitR(self):
        return self.nitR

    def getValor(self):
        return self.valor

    def getIva(self):
        return self.iva

    def getTotal(self):
        return self.total

    def getEstado(self):
        return self.estado

    #Set
    def setDia(self, dia):
        self.dia = dia

    def setReferencia(self, referencia):
        self.referencia = referencia

    def setNitE(self, NitE):
        self.nitE = NitE

    def setNitR(self, NitR):
        self.nitR = NitR

    def setValor(self, valor):
        self.valor = valor

    def setIva(self, iva):
        self.iva = iva

    def setTotal(self, total):
        self.total = total

    def setEstado(self, estado):
        self.estado = estado