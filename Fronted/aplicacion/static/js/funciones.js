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
    var opciones_inicio_i = document.querySelector('#grafica_iva_inicio')
    var opciones_fin_i = document.querySelector('#grafica_iva_fin')
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
        opciones_fin_i.innerHTML = cadena
    })
  }