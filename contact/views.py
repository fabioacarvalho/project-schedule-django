from django.shortcuts import render, get_object_or_404
from .models import Contato

def index(request):

    contatos = Contato.objects.all()

    return render(request, 'contacts/index.html', {
        'contatos': contatos #vai conter todos os dados
    })

def ver_contato(request, contato_id):
    #contato = Contato.objects.get(id=contato_id)
    contato = get_object_or_404(Contato, id=contato_id)

    return render(request, 'contacts/ver_contato.html', {
        'contato': contato #vai conter todos os dados do contato
    })
    