from django.urls import path
from . import views          

urlpatterns = [
    path(''         ,   views.principal,  name='principal'  ),
    path('registro/',   views.registro,   name='registro'   ),
    path('perfil/'  ,   views.perfil,     name='perfil'     ),
    path('salir/'   ,   views.salir,      name='salir'      ),
    path('inicio/'  ,   views.inicio,     name='inicio'     ),

    path('perfil/retiro'        ,   views.retiro,     name='retiro'     ),
    path('perfil/historial'     ,   views.historial,  name='historial'  ),
    path('perfil/deposito'      ,   views.deposito,   name='deposito'   ),

]