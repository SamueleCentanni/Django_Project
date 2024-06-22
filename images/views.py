from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Immagine aggiunta con successo')

            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    
    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'section': 'images','image': image})
    

@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_like.add(request.user)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})

@login_required
def image_list(request):
    images = Image.objects.all()
    # 8 immagini per volta
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # mostro la prima pagina
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            # se vado oltre il numero di pagine possibile e la richiesta è AJAX,
            # ritorno una pagina vuota
            return HttpResponse('')
        # se vado oltre il numero di pagine, ritorno l'ultima pagina
        images = paginator.page(paginator.num_pages)
    
    if images_only:
        return render(request, 'images/image/list_images.html', {'section': 'images', 'images': images})

    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})