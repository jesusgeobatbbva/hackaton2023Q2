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
    if request.method == 'GET':
            return render(  
                request,
                'operaciones/deposito.html',
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
        
        #numeroCuentaOrigen = informacionUsuario.numero_cuenta
        numeroCuentaReceptor = str(request.POST.get('id_destinatario', ''))
        informacionUsuario = InformacionBancaria.objects.get( numero_cuenta = numeroCuentaReceptor)

        
        informacionUsuario.saldo += cantidad
        informacionUsuario.save()
        receptor = InformacionBancaria.objects.get( numero_cuenta = numeroCuentaReceptor )
        transaccion = Transaccion(
                usuario=receptor.usuario,
                tipo='Deposito',
                monto=cantidad,  
                fecha=datetime.now()
            )
        transaccion.save()
        return redirect( 'perfil' )            
          

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


@login_required
def transferencia(request):
    if request.method == 'GET':
            return render(  
                request,
                'operaciones/transferencia.html',
            )
    else:
        cantidad = Decimal(request.POST.get('cantidad', 0.0))
        if cantidad <= 0:
            return render(
                request,
                'operaciones/transferencia.html',
                {
                    'error': 'Introduzca una cantidad válida.'
                }
            )
       
        informacionUsuarioOrigen = InformacionBancaria.objects.get(usuario=request.user)


        if informacionUsuarioOrigen.saldo < cantidad:
            return render(
                request,
                'operaciones/transferencia.html',
                {
                    'error': 'No tienes saldo suficiente.'
                }
            )
        else:
            informacionUsuarioOrigen.saldo -= cantidad
            informacionUsuarioOrigen.save()


            informacionUsuarioDestino = InformacionBancaria.objects.get(numero_cuenta=request.POST.get('destino'))
            informacionUsuarioDestino.saldo += cantidad
            informacionUsuarioDestino.save()


            transaccion_envio = Transaccion(
                usuario=request.user,
                tipo='TransferenciaSaliente',
                monto=cantidad,  
                fecha=datetime.now()
            )
            transaccion_envio.save()


            transaccion_recepcion = Transaccion(
                usuario=informacionUsuarioDestino.usuario,
                tipo='TransferenciaEntrante',
                monto=cantidad,  
                fecha=datetime.now()
            )
            transaccion_recepcion.save()






            return redirect( 'perfil' )
