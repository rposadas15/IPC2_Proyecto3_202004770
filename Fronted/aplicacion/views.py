from django.shortcuts import render, redirect
import requests

puerto = 'http://localhost:3000{}'

def Pagina(request):
    if request.method == 'GET':
        direccion = puerto.format('/Facturas')
        data = requests.get(direccion).json()
        context = {
            'data': data,
        }
        return render(request, 'Proyecto3.html', context)

    elif request.method == 'POST':
        document = str(request.FILES['archivo'].read())

        document = document.replace("b'", "")
        document = document.replace("'", "")
        document = document.replace("\\r\\n", "")

        data = {'direc': str(document)}
        direccion = puerto.format('/Facturas')
        requests.post(direccion, json=data)
        return redirect('Proyecto3')