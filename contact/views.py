from django.shortcuts import render, get_object_or_404, redirect
from .models import Contato
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='login')
def index(request):
    # contatos = Contato.objects.all()
    contatos = Contato.objects.order_by('-id').filter(
        mostra=True
    )
    paginator = Paginator(contatos, 20)

    page = request.GET.get('page')
    contatos = paginator.get_page(page)

    return render(request, 'contacts/index.html', {
        'contatos': contatos #vai conter todos os dados
    })

@login_required(redirect_field_name='login')
def ver_contato(request, contato_id):
    #contato = Contato.objects.get(id=contato_id)
    contato = get_object_or_404(Contato, id=contato_id)

    if not contato.mostra:
        raise Http404()

    return render(request, 'contacts/ver_contato.html', {
        'contato': contato #vai conter todos os dados do contato
    })
    
def busca(request):
    termo = request.GET.get('termo')
    campos = Concat('nome', Value(' '), 'sobrenome')

    if termo is None or not termo:
        messages.add_message(request, messages.ERROR, 'Campo termo não pode ficar vazio!')
        return redirect('index')

    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
    )

    # contatos = Contato.objects.order_by('-id').filter(
    #    Q( nome__icontains=termo) | Q(sobrenome__icontains=termo), #__icontains significa procurar por parte ou parcial
    #     mostra=True
    # )
    paginator = Paginator(contatos, 20)

    page = request.GET.get('page')
    contatos = paginator.get_page(page)

    return render(request, 'contacts/busca.html', {
        'contatos': contatos #vai conter todos os dados
    })