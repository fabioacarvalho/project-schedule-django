from django.shortcuts import render, get_object_or_404
from .models import Contato
from django.core.paginator import Paginator
from django.http import Http404

def index(request):

    contatos = Contato.objects.all()
    paginator = Paginator(contatos, 20)

    page = request.GET.get('page')
    contatos = paginator.get_page(page)

    return render(request, 'contacts/index.html', {
        'contatos': contatos #vai conter todos os dados
    })

def ver_contato(request, contato_id):
    #contato = Contato.objects.get(id=contato_id)
    contato = get_object_or_404(Contato, id=contato_id)

    if not contato.mostra:
        raise Http404()

    return render(request, 'contacts/ver_contato.html', {
        'contato': contato #vai conter todos os dados do contato
    })
    