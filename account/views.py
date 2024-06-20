from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm

# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None: # verifico che l'utente si sia autenticato con successo
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Autenticazione avvenuta con successo')
                else:
                    return HttpResponse('Errore nell\'autenticazione')
            else:
                return HttpResponse('Login non valido')
    else:
        form=LoginForm()
    return render(request, 'account/login.html', {'form': form})