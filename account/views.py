from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, ProfilePrivacyForm
from .models import Profile, Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from actions.utils import create_action
from actions.models import Action
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Q serve per le query complesse
from django.db.models import Q  

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

@login_required
def dashboard(request):
    # Ottieni gli ID degli utenti che l'utente corrente sta seguendo
    following_ids = request.user.following.values_list('id', flat=True)

    # Se l'utente segue qualcuno, ottieni le loro azioni, escludendo le azioni dell'utente stesso
    if following_ids:
        actions = Action.objects.filter(user_id__in=following_ids).exclude(user=request.user)
    else:
        # Se l'utente non segue nessuno, restituisci un QuerySet vuoto
        actions = Action.objects.none()

    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'actions': actions})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            #creo il profilo utente
            profile = Profile.objects.create(user=new_user)

            create_action(new_user, "ha creato un account.")
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        # se sia User model che Profile model sono stati riempiti con dati corretti, allora li salvo nel DB 
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profilo aggiornato con successo')
        else:
            messages.error(request, 'Errore')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})



@login_required
def user_list(request):
    query = request.GET.get('q')
    if query:
        user_list = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query))
    else:
        user_list = User.objects.all()
    
    # Ottieni tutti gli utenti
    paginator = Paginator(user_list, 4)  # Numero di utenti per pagina

    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # Se la pagina non è un intero, mostra la prima pagina
        users = paginator.page(1)
    except EmptyPage:
        # Se la pagina è fuori limite (es. 9999), mostra l'ultima pagina di risultati
        users = paginator.page(paginator.num_pages)

    return render(request, 'account/user/list.html', {'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    profile = get_object_or_404(Profile, user=user)

    # Verifica se l'utente loggato segue il proprietario dell'immagine
    follows = Contact.objects.filter(user_from=request.user, user_to=user).exists()

    # Determina se l'immagine deve essere visibile
    can_view = not profile.private or request.user == user or follows 
    return render(request, 'account/user/detail.html', {'section': 'people', 'user': user, 'profile': profile, 'can_view': can_view})


@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            # prendo l'utente che ha fatto la richiesta     
            user = User.objects.get(id=user_id)
            if action == 'follow':
                # se l'utente ha iniziato a seguire un altro utene, allora creo la relazione nella tabella Contact
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, "ha iniziato a seguire ", user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})

@login_required
def private_profile(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ProfilePrivacyForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Impostazioni sulla privacy del profilo aggiornate con successo')
            return redirect('dashboard')
    else:
        form = ProfilePrivacyForm(instance=profile)
    
    return render(request, 'account/user/profile_privacy.html', {'form': form, 'profile': profile})