from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm, AddLocalImage, CommentForm
from .models import Image, Comment
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action
import redis
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

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
            create_action(request.user, 'ha aggiunto l\'immagine ', new_item)
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    
    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})

@login_required
def image_comment(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    comments = image.comments.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.image = image
            new_comment.user = request.user
            new_comment.save()
            return redirect('images:detail', id=image.id, slug=image.slug)
    else:
        form = CommentForm()
    
    return render(request, 'images/image/comments.html', {'section': 'comments', 'form': form, 'comments': comments})



def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # increment total image views by 1
    total_views = r.incr(f'image:{image.id}:views')
    # increment image ranking by 1
    r.zincrby('image_ranking', 1, image.id)

    return render(request,
                  'images/image/detail.html',
                  {'section': 'images',
                   'image': image,
                   'total_views': total_views,
                   })


class ImageDeleteView(DeleteView, LoginRequiredMixin, ):
    model = Image
    template_name = 'images/image/delete_img.html'
    context_object_name = 'image'
    success_url = reverse_lazy('images:your_images')
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

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
                create_action(request.user, 'ha messo like a ', image)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})

@login_required
def image_list(request, images=None): 
    if not images:
        images = Image.objects.exclude(user=request.user)
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
        return render(request, 'images/image/list_images.html', {'section': 'images', 'images': images, 'user': User.user})

    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})

@login_required
def user_image_list(request):
    images = Image.objects.filter(user=request.user)
    return image_list(request, images)

@login_required
def image_ranking(request):
    # get image ranking dictionary
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # get most viewed images
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request, 'images/image/ranking.html', {'section': 'images','most_viewed': most_viewed})


@login_required
def image_create_local(request):
    if request.method == 'POST':
        form = AddLocalImage(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Immagine aggiunta con successo')
            create_action(request.user, 'ha aggiunto l\'immagine ', new_item)
            return redirect(new_item.get_absolute_url())
    else:
        form = AddLocalImage(data=request.GET)
    
    return render(request, 'images/image/create_local.html', {'section': 'images', 'form': form})