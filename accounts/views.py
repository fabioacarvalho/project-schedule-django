from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato

def login(request):
    #Se nada for postado:
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    #coletando dados:
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    #validando usuario:
    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Você fez login com sucesso.')
        return redirect('dashboard')


    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def cadastro(request):
 
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')

    #Pegando os dados:
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    #Validando se possui campos vazios:
    if not nome or not sobrenome or not usuario or not email or not senha or not senha2:
        messages.warning(request, 'Favor preencher todos os campos!')
        return render(request, 'accounts/cadastro.html')

    #Validando e-mail:
    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido!')
        return render(request, 'accounts/cadastro.html')

    #Validando as senhas:
    if len(senha) < 6:
        messages.error(request, 'A senha precisa ter no mínimo 6 caracteres.')
        return render(request, 'accounts/cadastro.html')

    if senha != senha2:
        messages.error(request, 'As senhas precisam ser iguais.')
        return render(request, 'accounts/cadastro.html')

    #Validando usuario:
    if len(usuario) < 5:
        messages.error(request, 'O usuário precisa ter no mínimo 6 caracteres.')
        return render(request, 'accounts/cadastro.html')

    #Validando se e-mail já existe:
    if User.objects.filter(email=email).exists() :
        messages.error(request, 'E-mail já existe.')
        return render(request, 'accounts/cadastro.html')

    #Validando se usuario já existe:
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário já existe.')
        return render(request, 'accounts/cadastro.html')

    

    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
    user.save()

    messages.success(request, 'Usuário registrado com sucesso.')
    
    return redirect('login')

@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', { 'form': form })
    
    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao cadastrar contato.')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', { 'form': form })

    form.save()
    messages.success(request, f'Contato {request.POST.get("nome")} salvo com sucesso.')
    return redirect('dashboard')
