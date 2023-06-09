# Generated by Django 3.2.19 on 2023-06-02 22:31

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(choices=[('#0000FF', 'Синий'), ('#FFA500', 'Оранжевый'), ('#008000', 'Зеленый')], default='#0000FF', help_text=('Обязательное для заполнение поле. Максимальная длинна 7 символов.',), image_field=None, max_length=7, samples=None, unique=True, verbose_name='HEX-код'),
        ),
    ]
