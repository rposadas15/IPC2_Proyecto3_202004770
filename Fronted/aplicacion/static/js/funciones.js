//PDF Archivo de Salida
function PDF(){
    html2canvas($('#pdf')[0], {
      onrendered: function (canvas) {
          var data = canvas.toDataURL();
          var docDefinition = {
              content: [{
                  image: data,
                  width: 500
              }]
          };
          pdfMake.createPdf(docDefinition).download("PDF_Salida.pdf");
      }
  });
}

//PDF Grafica por Fechas e IVA
function PDF_IVA(){
    html2canvas($('#pdf_IVA')[0], {
        onrendered: function (canvas) {
            var data = canvas.toDataURL();
            var docDefinition = {
                content: [{
                    image: data,
                    width: 500
                }]
            };
            pdfMake.createPdf(docDefinition).download("PDF_Grafica_IVA.pdf");
        }
    });
}

//PDF Grafica por Fechas
function PDF_Fechas(){
    html2canvas($('#pdf_Fechas')[0], {
        onrendered: function (canvas) {
            var data = canvas.toDataURL();
            var docDefinition = {
                content: [{
                    image: data,
                    width: 500
                }]
            };
            pdfMake.createPdf(docDefinition).download("PDF__Grafica_Fechas.pdf");
        }
    });
}

//Funcion de resetear programa
function Resetear(){
    var reinicio = {'Del':"yes"}

    fetch(`http://localhost:3000/Facturas`,{
    method: 'DELETE',
    body: JSON.stringify(reinicio),
    headers:{
        'Content-Type':'aplication/json',
        'Access-Control-Allow-Origin':'*',}})

        .then(res => res.json())
        .catch(err => {
        console.error('Error:',err)
        alert("Ocurrio un error, ver consola")
        })
        .then(response => {
        console.log(response);
        //alert(response.Mensaje)
        })
        location.reload()
}

//Combo box de Fechas
function ComboBox(){
    var opciones_inicio_i = document.querySelector('#grafica_iva')
    var opciones_inicio_f = document.querySelector('#grafica_fechas_inicio')
    var opciones_fin_f = document.querySelector('#grafica_fechas_fin')
    var cadena = ''
    
    fetch('http://localhost:3000/Grafica', {
    method: 'GET',
    headers:{
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',}})
    .then(res => res.json())
    .catch(err => {
        console.error('Error:', err)
        alert("Ocurrio un error, ver la consola")
    })
    .then(response =>{
        console.log(response);
        response.forEach(element => {
                cadena += `<option>
                    ${element.Fecha}
                    </option>`
        });
        opciones_inicio_f.innerHTML = cadena
        opciones_fin_f.innerHTML = cadena
        opciones_inicio_i.innerHTML = cadena
    })
}

//Grafica Fechas
function CrearGraficasFechas(){
    var FechaInicio = document.querySelector('#grafica_fechas_inicio').value
    var FechaFin = document.querySelector('#grafica_fechas_fin').value
    //console.log(FechaInicio, FechaFin)
    var Fechas = []
    var Totales = []
    var IVA = []

    objeto = {
        'Inicio': FechaInicio,
        'Fin': FechaFin
    }

    fetch(`http://localhost:3000/Fechas`, {
    method: 'POST',
    body: JSON.stringify(objeto),
    headers:{
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',}})
    .then(res => res.json())
    .catch(err => {
        console.error('Error:', err)
        alert("Ocurrio un error, ver la consola")
    })
    .then(response =>{
        console.log(response);
        response.forEach(element => {
            //console.log(element.Fecha, element.Total, element.SinIVA)
            Fechas.push(element.Fecha)
            Totales.push(element.Total)
            IVA.push(element.SinIVA)
        })
        GenerarGrafica(Fechas, Totales, IVA)
    })
}
    
function GenerarGrafica(Fe, To, IVA){
    var trace1 = {
    x: Fe,
    y: IVA,
    name: 'Sin Iva',
    type: 'bar'
    };
    var trace2 = {
    x: Fe,
    y: To,
    name: 'Total',
    type: 'bar'
    };					
    var data_info = [trace1, trace2];
    var bordes = {barmode: 'group'};
    Plotly.newPlot('GraficaFechas', data_info, bordes);
}

//Grafica IVA
function CrearGraficasIVA(){
    var FechaInicio = document.querySelector('#grafica_iva').value
    //console.log(FechaInicio, FechaFin)
    var NIT = []
    var Totales = []
    var IVA = []

    objeto = {
        'Fecha': FechaInicio,
    }

    fetch(`http://localhost:3000/IVA`, {
    method: 'POST',
    body: JSON.stringify(objeto),
    headers:{
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',}})
    .then(res => res.json())
    .catch(err => {
        console.error('Error:', err)
        alert("Ocurrio un error, ver la consola")
    })
    .then(response =>{
        console.log(response);
        response.forEach(element => {
            //console.log(element.Nit, element.Total, element.Valor_IVA)
            NIT.push(element.Nit)
            Totales.push(element.Total)
            IVA.push(element.Valor_IVA)
        })
        GenerarGrafica2(NIT, Totales, IVA)
    })
}

function GenerarGrafica2(Nit, To, IVA){
    var trace1 = {
    x: Nit,
    y: IVA,
    name: 'Iva Emitido',
    type: 'bar'
    };
    var trace2 = {
    x: Nit,
    y: To,
    name: 'Total',
    type: 'bar'
    };					
    var data_info_2 = [trace1, trace2];
    var bordes_2 = {barmode: 'group'};
    Plotly.newPlot('GraficaIVA', data_info_2, bordes_2);
}