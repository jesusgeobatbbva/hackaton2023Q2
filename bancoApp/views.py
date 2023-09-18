from django.shortcuts               import render, redirect
from django.contrib.auth.forms      import UserCreationForm, AuthenticationForm
from django.contrib.auth.models     import User 
from django.http                    import HttpResponse
from django.contrib.auth            import login, logout, authenticate
from django.db                      import IntegrityError
from .models                        import InformacionBancaria, Transaccion
from django.contrib.auth.decorators import login_required
from datetime                       import datetime
from decimal                        import Decimal


def registro(request):
    if request.method == 'GET':
        return render(  
            request,
            'sesion/registro.html',
            {'form': UserCreationForm} 
        )
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                usuario = User.objects.create_user(
                    username = request.POST['username'],
                    password = request.POST['password1']
                )

                informacionUsuario = InformacionBancaria(
                    usuario=usuario,
                    saldo=0.0
                )
                informacionUsuario.numero_cuenta = informacionUsuario.generar_numero_cuenta()  
                informacionUsuario.save()

                usuario.save()
                login( request, usuario )
                return redirect('perfil')
            except IntegrityError:
                return render(  
                    request,
                    'sesion/registro.html',
                    {
                        'form': UserCreationForm,
                        'error': '¡El usuario ya existe!'
                    } 
                )
        return render(  
                    request,
                    'sesion/registro.html',
                    {
                        'form': UserCreationForm,
                        'error': '¡La constraseña no coincide!'
                    } 
                )

def principal(request):
    return render(
        request,
        'pantallas/principal.html',
    )

@login_required
def perfil(request):
    usuarioActual = request.user

    return render(
        request,
        'pantallas/perfil.html',
        {
            'nombre'       : usuarioActual.username,
            'informacion'  : InformacionBancaria.objects.get( usuario = usuarioActual )
        }
    )

def salir(request):
    logout( request )
    return redirect('principal')

def inicio(request):
    if request.method == 'GET':
        return render(
            request,
            'sesion/inicio.html',
            {'form': AuthenticationForm} 
        )
    else:
        usuario = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if usuario is None:
            return render(
                request,
                'sesion/inicio.html',
                {
                    'form': AuthenticationForm,
                    'error': '¡Datos incorrectos!'
                } 
            )
        else:
            login(request, usuario)
            return redirect( 'perfil' )


@login_required
def deposito(request):
    return render(
        request,
        'operaciones/deposito.html',
    )

@login_required
def retiro(request):
    if request.method == 'GET':
            return render(  
                request,
                'operaciones/retiro.html',
            )
    else:
        cantidad = Decimal(request.POST.get('cantidad', 0.0))
        if cantidad <= 0:
            return render(
                request,
                'operaciones/retiro.html',
                {
                    'error': 'Introduzca una cantidad válida.'
                } 
            )
        
        informacionUsuario = InformacionBancaria.objects.get(usuario=request.user)

        if informacionUsuario.saldo < cantidad:
            return render(
                request,
                'operaciones/retiro.html',
                {
                    'error': 'No tienes saldo suficiente.'
                } 
            )
        else:
            informacionUsuario.saldo -= cantidad
            informacionUsuario.save()

            transaccion = Transaccion(
                usuario=request.user,
                tipo='Retiro',
                monto=cantidad,  
                fecha=datetime.now()
            )
            transaccion.save()
            return redirect( 'perfil' )
       

@login_required
def historial(request):
    transacciones = Transaccion.objects.filter(usuario=request.user).order_by('-fecha') #Más reciente a más antigua
    return render(request, 'operaciones/historial.html', {'transacciones': transacciones})


"""
import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render
from .models import Transaccion

@login_required
def historial(request):
    # Obtén las transacciones para el usuario actual
    transacciones = Transaccion.objects.filter(usuario=request.user).order_by('-fecha')

    # Crear listas de fechas y montos para el gráfico
    fechas = [transaccion.fecha for transaccion in transacciones]
    montos = [transaccion.monto for transaccion in transacciones]

    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(fechas, montos, marker='o')
    plt.xlabel('Fecha')
    plt.ylabel('Monto')
    plt.title('Historial de Transacciones')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Guardar el gráfico en un archivo BytesIO
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    # Convertir el gráfico a base64 para incrustarlo en la plantilla
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    plt.close()

    # Renderizar la plantilla con el gráfico incrustado
    return render(request, 'operaciones/historial.html', {'transacciones': transacciones, 'img_base64': img_base64})

    
    {% extends "base.html" %}

{% block content %}
  <h1>Historial de Transacciones</h1>
  <table>
    <!-- Mostrar tus transacciones en una tabla -->
  </table>

  <!-- Mostrar el gráfico -->
  <img src="data:image/png;base64,{{ img_base64 }}" alt="Gráfico de Transacciones">
{% endblock %}

"""

