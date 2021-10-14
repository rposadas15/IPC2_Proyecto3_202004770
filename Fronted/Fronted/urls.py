from os import name
from django.urls import path
from aplicacion.views import *

urlpatterns = [    
    path('', Pagina, name='Proyecto3'),
]
