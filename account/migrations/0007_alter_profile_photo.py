# Generated by Django 5.0.6 on 2024-06-23 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='users/default/profile_default_icon.png', upload_to='users/%Y/%m/%d/'),
        ),
    ]
