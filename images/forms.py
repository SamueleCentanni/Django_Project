from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {'url': forms.HiddenInput}

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()

        if extension not in valid_extensions:
            raise forms.ValidationError('L\'URL fornito non coincide con una estensione valida (JPEG, JPG)')
        return url   
    
    def save(self, force_insert=False, force_update=False, commit=True):
        # per ora non salvo l'immagine nel DB, perché prima devo sapere chi è l'utente che la sta caricando
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.',1)[1].lower())

        # ora facciamo download immagine
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)

        # per rispettare il comportamento del metodo overridato save -> salviamo solo se commit=True
        if commit:
            image.save()
        return image